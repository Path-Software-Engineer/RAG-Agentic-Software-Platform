from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def require(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        raise AssertionError(f"Required AWS artifact is missing: {path}")
    return target.read_text(encoding="utf-8")


def assert_contains(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        raise AssertionError(f"{label} is missing: {', '.join(missing)}")


def main() -> None:
    template = require("infra/aws/template.yaml")
    deploy = require("infra/aws/deploy.ps1")
    api_state = require("infra/aws/set-api-state.ps1")
    dockerfile = require("infra/aws/platform-lambda.Dockerfile")
    launcher = require("infra/aws/start-platform.sh")
    runtime_secret = require("infra/aws/load_runtime_secret.py")
    migration = require("infra/aws/migrate.py")
    requirements = require("ai-services/rag-agent-service/requirements.lock")
    secrets = require("infra/aws/configure-secrets.ps1")
    client = require("frontend/sveltekit-app/src/lib/api.ts")
    rag_main = require("ai-services/rag-agent-service/app/main.py")
    attributes = require(".gitattributes")

    assert_contains(
        template,
        [
            "AWS::Lambda::Function",
            "UseReservedConcurrency:",
            "ApplyReservedConcurrency:",
            'ReservedConcurrentExecutions: !If [ApplyReservedConcurrency, 1, !Ref "AWS::NoValue"]',
            "MemorySize: 1024",
            "Timeout: 60",
            "AWS::Lambda::Url",
            "AuthType: AWS_IAM",
            "OriginAccessControlOriginType: lambda",
            "AWS::CloudFront::Distribution",
            "PriceClass: PriceClass_100",
            "AWS::S3::Bucket",
            "RetentionInDays: 3",
            'DATABASE_POOL_MAX: "3"',
            "DATABASE_URL_PARAMETER_NAME: !Ref DatabaseUrlParameterName",
            'REDIS_URL: ""',
            "Action: ssm:GetParameter",
            "parameter${DatabaseUrlParameterName}",
            "- Key: path\n          Value: software-engineer",
            '- Key: plan\n          Value: "05"',
        ],
        "CloudFormation template",
    )
    forbidden = [
        "AWS::RDS::",
        "AWS::ElastiCache::",
        "AWS::EC2::NatGateway",
        "AWS::ElasticLoadBalancingV2::",
        "AWS::AppRunner::",
        "ProvisionedConcurrencyConfig",
    ]
    present = [token for token in forbidden if token in template]
    if present:
        raise AssertionError(
            f"Always-on or forbidden AWS resources detected: {present}"
        )
    if "{{resolve:ssm-secure:" in template:
        raise AssertionError(
            "Lambda environment variables cannot consume an SSM SecureString "
            "dynamic reference."
        )

    assert_contains(
        deploy,
        [
            "describe-budgets",
            "get-parameter",
            "validate-template",
            "scanOnPush=true",
            "IMMUTABLE",
            "Keep only two immutable release images",
            'Invoke-Native -Command "docker"',
            '"buildx", "build"',
            'Invoke-Native -Command "npm"',
            '"run", "build", "--workspace", "@rag-platform/web"',
            "seed-agent-demo.ps1",
            "SmokeOnly",
            '"lambda", "get-account-settings"',
            "AccountLimit.UnreservedConcurrentExecutions",
            "UseReservedConcurrency=$useReservedConcurrency",
            "CloudFormation failed. Fetching failed Project 05 resource events.",
        ],
        "deployment script",
    )
    assert_contains(
        api_state,
        [
            'ValidateSet("Running", "Paused")',
            "--reserved-concurrent-executions 0",
            "get-account-settings",
            "AccountLimit.UnreservedConcurrentExecutions",
            "--reserved-concurrent-executions 1",
            "delete-function-concurrency",
        ],
        "quota-aware Lambda state script",
    )
    assert_contains(
        dockerfile,
        [
            "aws-lambda-adapter:1.0.0",
            "node:22-bookworm-slim",
            "python:3.12-slim",
            "load_runtime_secret.py",
            "start-platform.sh",
            "USER platform",
        ],
        "combined Lambda image",
    )
    assert_contains(
        launcher,
        [
            "DATABASE_URL_PARAMETER_NAME",
            "python /app/load_runtime_secret.py",
            "python /app/migrate.py",
            "uvicorn app.main:app",
            "exec node dist/main.js",
        ],
        "Lambda launcher",
    )
    assert_contains(
        runtime_secret,
        [
            'boto3.client("ssm")',
            "get_parameter(Name=parameter_name, WithDecryption=True)",
            "sys.stdout.write(load_database_url(parameter_name))",
            'parameter_name.startswith("/sf/05/")',
            'parse_qs(parsed.query).get("sslmode") != ["require"]',
        ],
        "runtime secret loader",
    )
    if "boto3==1.43.53" not in requirements:
        raise AssertionError(
            "The AWS SDK runtime dependency is not reproducibly pinned."
        )

    namespace: dict[str, object] = {"__name__": "aws_runtime_secret_test"}
    exec(compile(runtime_secret, "load_runtime_secret.py", "exec"), namespace)

    class FakeSsmClient:
        def __init__(self) -> None:
            self.request: dict[str, object] = {}

        def get_parameter(self, **kwargs: object) -> dict[str, object]:
            self.request = kwargs
            return {
                "Parameter": {
                    "Value": "postgresql://user:password@host/db?sslmode=require"
                }
            }

    fake_ssm = FakeSsmClient()
    loader = namespace["load_database_url"]
    assert callable(loader)
    loaded_url = loader("/sf/05/rag-agent-workflow/database-url", fake_ssm)
    if loaded_url != "postgresql://user:password@host/db?sslmode=require":
        raise AssertionError("The runtime loader changed the decrypted database URL.")
    if fake_ssm.request.get("WithDecryption") is not True:
        raise AssertionError(
            "The runtime loader did not request SecureString decryption."
        )
    try:
        loader("/another/project/database-url", fake_ssm)
    except RuntimeError as error:
        if "outside the Project 05 namespace" not in str(error):
            raise
    else:
        raise AssertionError(
            "The runtime loader accepted a parameter outside Project 05."
        )
    assert_contains(
        migration,
        ["pg_advisory_lock", 'glob("*.sql")', "psycopg.connect"],
        "migration runner",
    )
    assert_contains(
        secrets,
        ["Read-Host", "-AsSecureString", "SecureString", "sslmode=require"],
        "secret configurator",
    )
    assert_contains(
        client,
        ["x-amz-content-sha256", "crypto.subtle.digest", "documentMultipart"],
        "browser integrity adapter",
    )
    if "new FormData" in client:
        raise AssertionError(
            "Native FormData cannot provide the exact CloudFront payload hash."
        )
    assert_contains(
        rag_main, ["NullEventPublisher", "settings.redis_url.strip()"], "RAG profile"
    )
    if "infra/aws/*.sh text eol=lf" not in attributes:
        raise AssertionError("Linux launch scripts are not pinned to LF line endings.")

    print("OK - cost-bounded AWS serverless deployment package check passed")
    print("Topology: CloudFront + private S3 + protected Lambda + Neon PostgreSQL")
    print("Always-on AWS data or compute services: none")


if __name__ == "__main__":
    main()
