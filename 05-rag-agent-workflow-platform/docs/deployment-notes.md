# Deployment Notes

Project 05 has two official profiles.

## Complete local profile

Docker Compose runs SvelteKit, NestJS, FastAPI, PostgreSQL/pgvector and transient Redis Streams as separate services. This is the authoritative integration and architecture-validation profile.

## AWS portfolio profile

```text
CloudFront
  -> private S3 compiled SPA
  -> IAM-protected Lambda Function URL
       -> NestJS public API
       -> private localhost FastAPI
       -> Neon PostgreSQL over TLS
```

The AWS profile deliberately removes an always-on Redis service. PostgreSQL remains authoritative for ordered trace replay, and FastAPI selects the explicit null publisher when `REDIS_URL` is empty. This is a deployment-profile decision, not removal of the Redis integration from the complete architecture.

The Lambda uses 1 GiB, no provisioned concurrency, a 60-second timeout and the included 512 MiB ephemeral filesystem. The deploy script inspects regional unreserved concurrency and requests a one-execution reservation only when AWS can preserve its unreserved minimum. Restricted new accounts omit the per-function reservation and remain bounded by their smaller regional quota. Document bodies, chunks and evidence remain durable in PostgreSQL; local file writes are disposable ingestion artifacts under `/tmp`.

The Neon URL remains a standard-tier SSM `SecureString`. CloudFormation supplies only its parameter name; the Lambda role has a resource-scoped `ssm:GetParameter` permission and the runtime requests decryption during cold start. This avoids both plaintext infrastructure parameters and unsupported secure dynamic references in Lambda environment properties.

CloudFront uses private origins. Browser request bodies are hashed with SHA-256 before POST/PATCH calls because Lambda Function URL OAC does not accept unsigned payloads. The frontend, API and Swagger share one HTTPS origin.

The stack does not create RDS, Aurora, ElastiCache, EC2, App Runner, ECS, VPC, NAT Gateway, load balancers or GPUs. ECR retains only two immutable images and logs expire after three days. External Neon data is never deleted by AWS cleanup scripts.

This topology minimizes idle cost but cannot guarantee a zero invoice. AWS Budgets only notify. Current commands, operational controls and official pricing references are maintained in [the AWS runbook](../infra/aws/README.md).
