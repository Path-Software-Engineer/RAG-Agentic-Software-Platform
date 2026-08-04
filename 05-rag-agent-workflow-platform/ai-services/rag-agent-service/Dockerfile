FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY ai-services/rag-agent-service/requirements.lock ./requirements.lock
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.lock

COPY ai-services/rag-agent-service/app ./app
COPY ai-services/rag-agent-service/tests ./tests
COPY ai-services/rag-agent-service/pyproject.toml ./pyproject.toml
RUN mkdir -p /app/storage/documents && useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /app

USER appuser
EXPOSE 8100
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100"]
