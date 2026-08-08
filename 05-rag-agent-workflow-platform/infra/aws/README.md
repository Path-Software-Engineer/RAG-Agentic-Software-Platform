# AWS serverless deployment

This is the production-demo boundary for Software Engineer Project 05. It preserves the local module boundaries while removing always-on infrastructure from the public portfolio profile.

## Topology

```text
Browser
  -> CloudFront (one HTTPS URL, PriceClass_100)
     -> private S3 origin with the compiled SvelteKit SPA
     -> IAM-protected Lambda Function URL for /api/* and /healthz
        -> NestJS public API on port 8080
        -> FastAPI RAG engine on private localhost port 8100
        -> Neon PostgreSQL over TLS
```

The one Lambda image contains two processes but does not collapse their contracts: the browser reaches only NestJS, and NestJS reaches FastAPI through `127.0.0.1`. PostgreSQL remains durable. Redis Streams stay in the complete Docker profile; the AWS demo replays ordered events from PostgreSQL and uses the explicit null publisher to avoid an always-on ElastiCache charge.

CloudFormation passes only `/sf/05/rag-agent-workflow/database-url` to the runtime. The Lambda role can call `ssm:GetParameter` only for that namespaced parameter. At cold start, the container decrypts and validates the pooled Neon URL before migrations, exports it only to the two application processes and never writes or logs it.

The CloudFront Lambda origin uses OAC and `AWS_IAM`. Every browser POST/PATCH body, including multipart uploads, is SHA-256 hashed in the `x-amz-content-sha256` header as required by AWS. The direct Function URL is not public.

## Cost boundary

The stack creates one Lambda function with 1 GiB, reserved concurrency 1 and no provisioned concurrency; one private S3 bucket; one CloudFront distribution; one three-day CloudWatch log group; and one least-privilege execution role. The deploy script creates one private immutable ECR repository and retains only two release images.

It does not create RDS, Aurora, ElastiCache, VPC resources, NAT Gateway, load balancers, EC2, App Runner or provisioned concurrency. Neon is external. AWS Budgets only alert and never impose a hard cap. Lambda is billed by request and duration, while S3, CloudFront, ECR, logs and transfer can still generate small charges.

## Configure the Neon secret

Create a dedicated Neon database such as `sf_p05_rag_agent_workflow`, copy its pooled TLS connection string and run:

```powershell
.\infra\aws\configure-secrets.ps1 `
  -Profile "paths" `
  -Region "us-east-1"
```

The URL must include `sslmode=require`. It is stored as the standard-tier SSM `SecureString` `/sf/05/rag-agent-workflow/database-url` and is never written to Git.

## Preflight

```powershell
.\infra\aws\deploy.ps1 `
  -Profile "paths" `
  -Region "us-east-1" `
  -PreflightOnly
```

Preflight is read-only. It verifies AWS identity, an existing account budget, the SSM parameter, CloudFormation syntax, Docker, Node and the Docker engine.

## Deploy

```powershell
.\infra\aws\deploy.ps1 `
  -Profile "paths" `
  -Region "us-east-1"
```

The script builds and publishes an immutable combined image, applies the CloudFormation stack, compiles SvelteKit against the CloudFront origin, publishes the private SPA, seeds the three controlled sprints and executes remote health, Swagger and allowlist checks.

Interrupted deployments can reuse an existing immutable image:

```powershell
.\infra\aws\deploy.ps1 `
  -Profile "paths" `
  -Region "us-east-1" `
  -ImageTag "GIT_SHA" `
  -ReusePublishedImage
```

## Operate

Read-only smoke:

```powershell
.\infra\aws\deploy.ps1 -Profile "paths" -Region "us-east-1" -SmokeOnly
```

Pause and resume API compute:

```powershell
.\infra\aws\set-api-state.ps1 -State Paused -Profile "paths"
.\infra\aws\set-api-state.ps1 -State Running -Profile "paths"
```

Explicit cleanup:

```powershell
.\infra\aws\destroy.ps1 -Profile "paths" -ConfirmDestroy
```

Add `-DeleteSecret` only when the SSM parameter should also be deleted. The script never deletes the external Neon database.

## Current AWS references

- [AWS Lambda pricing](https://aws.amazon.com/lambda/pricing/)
- [CloudFront pricing](https://aws.amazon.com/cloudfront/pricing/)
- [Amazon ECR pricing](https://aws.amazon.com/ecr/pricing/)
- [AWS Systems Manager pricing](https://aws.amazon.com/systems-manager/pricing/)
- [CloudFront OAC for Lambda Function URLs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-lambda.html)
