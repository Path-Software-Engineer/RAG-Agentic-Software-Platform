#!/bin/sh
set -eu

python /app/migrate.py

cd /app/rag
uvicorn app.main:app \
  --host 127.0.0.1 \
  --port "${RAG_PORT:-8100}" \
  --workers 1 \
  --no-access-log &
rag_pid=$!

cleanup() {
  kill "$rag_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

attempt=1
while [ "$attempt" -le 30 ]; do
  if python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:${RAG_PORT:-8100}/healthz', timeout=2)" >/dev/null 2>&1; then
    break
  fi
  if ! kill -0 "$rag_pid" 2>/dev/null; then
    echo "The private RAG service stopped during startup." >&2
    exit 1
  fi
  attempt=$((attempt + 1))
  sleep 1
done

if [ "$attempt" -gt 30 ]; then
  echo "The private RAG service did not become ready." >&2
  exit 1
fi

cd /app/api
exec node dist/main.js
