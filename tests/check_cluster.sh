#!/bin/bash
# Load environment variables
if [ -f ../.env ]; then
  source ../.env
fi

MINIO_HOST="localhost"
MINIO_PORT="9000"

echo "Testing MinIO at http://${MINIO_HOST}:${MINIO_PORT}/minio/health/live ..."

if curl -sf "http://${MINIO_HOST}:${MINIO_PORT}/minio/health/live" > /dev/null; then
  echo "MinIO is running correctly."
else
  echo "MinIO is not responding correctly."
  exit 1
fi
