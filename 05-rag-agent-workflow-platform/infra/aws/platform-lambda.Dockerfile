FROM public.ecr.aws/awsguru/aws-lambda-adapter:1.0.0 AS lambda-adapter

FROM node:22-bookworm-slim AS api-build
WORKDIR /workspace
COPY package.json package-lock.json ./
COPY backend/nestjs-api/package.json backend/nestjs-api/package.json
COPY frontend/sveltekit-app/package.json frontend/sveltekit-app/package.json
RUN npm ci --workspace @rag-platform/api --include-workspace-root
COPY backend/nestjs-api backend/nestjs-api
RUN npm run build --workspace @rag-platform/api

FROM node:22-bookworm-slim AS api-runtime
WORKDIR /workspace
COPY package.json package-lock.json ./
COPY backend/nestjs-api/package.json backend/nestjs-api/package.json
COPY frontend/sveltekit-app/package.json frontend/sveltekit-app/package.json
RUN npm ci --workspace @rag-platform/api --include-workspace-root --omit=dev

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/tmp \
    PORT=8080 \
    RAG_PORT=8100 \
    AWS_LWA_PORT=8080 \
    AWS_LWA_READINESS_CHECK_PATH=/healthz \
    AWS_LWA_READINESS_CHECK_HEALTHY_STATUS=200-399 \
    AWS_LWA_ASYNC_INIT=true \
    AWS_LWA_INVOKE_MODE=buffered

WORKDIR /app

COPY --from=lambda-adapter /lambda-adapter /opt/extensions/lambda-adapter
COPY --from=api-build /usr/local/bin/node /usr/local/bin/node
COPY --from=api-build /workspace/backend/nestjs-api/dist /app/api/dist
COPY --from=api-build /workspace/backend/nestjs-api/package.json /app/api/package.json
COPY --from=api-runtime /workspace/node_modules /app/api/node_modules

COPY ai-services/rag-agent-service/requirements.lock /app/rag/requirements.lock
RUN python -m pip install --upgrade pip \
    && python -m pip install -r /app/rag/requirements.lock

COPY ai-services/rag-agent-service/app /app/rag/app
COPY database/migrations /app/migrations
COPY infra/aws/migrate.py /app/migrate.py
COPY infra/aws/start-platform.sh /app/start-platform.sh

RUN useradd --create-home --uid 10001 platform \
    && mkdir -p /tmp/sf05-documents \
    && chmod 0555 /app/start-platform.sh \
    && chown -R platform:platform /app /tmp/sf05-documents

USER platform
EXPOSE 8080
CMD ["/app/start-platform.sh"]
