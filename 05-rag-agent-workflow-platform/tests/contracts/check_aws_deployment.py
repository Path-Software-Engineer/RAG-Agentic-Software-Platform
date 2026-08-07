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
    dockerfile = require("infra/aws/platform-lambda.Dockerfile")
    launcher = require("infra/aws/start-platform.sh")
    migration = require("infra/aws/migrate.py")
    secrets = require("infra/aws/configure-secrets.ps1")
    client = require("frontend/sveltekit-app/src/lib/api.ts")
    rag_main = require("ai-services/rag-agent-service/app/main.py")
    attributes = require(".gitattributes")

    assert_contains(
        template,
        [
            "AWS::Lambda::Function",
            "ReservedConcurrentExecutions: 1",
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
            'REDIS_URL: ""',
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
        ],
        "deployment script",
    )
    assert_contains(
        dockerfile,
        [
            "aws-lambda-adapter:1.0.0",
            "node:22-bookworm-slim",
            "python:3.12-slim",
            "start-platform.sh",
            "USER platform",
        ],
        "combined Lambda image",
    )
    assert_contains(
        launcher,
        ["python /app/migrate.py", "uvicorn app.main:app", "exec node dist/main.js"],
        "Lambda launcher",
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
