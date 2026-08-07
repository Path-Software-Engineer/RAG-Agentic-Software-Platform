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

The Lambda uses 1 GiB, reserved concurrency 1, no provisioned concurrency, a 60-second timeout and the included 512 MiB ephemeral filesystem. Document bodies, chunks and evidence remain durable in PostgreSQL; local file writes are disposable ingestion artifacts under `/tmp`.

CloudFront uses private origins. Browser request bodies are hashed with SHA-256 before POST/PATCH calls because Lambda Function URL OAC does not accept unsigned payloads. The frontend, API and Swagger share one HTTPS origin.

The stack does not create RDS, Aurora, ElastiCache, EC2, App Runner, ECS, VPC, NAT Gateway, load balancers or GPUs. ECR retains only two immutable images and logs expire after three days. External Neon data is never deleted by AWS cleanup scripts.

This topology minimizes idle cost but cannot guarantee a zero invoice. AWS Budgets only notify. Current commands, operational controls and official pricing references are maintained in [the AWS runbook](../infra/aws/README.md).
