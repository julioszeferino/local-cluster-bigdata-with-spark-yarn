# Project: Cluster with Docker Compose

## Services

- **MinIO**: S3-compatible storage service.
  - Buckets created:
    - `$MINIO_BUCKET_LANDING` (landing zone)
    - `$MINIO_BUCKET_SPARK` (spark data)
      - `$MINIO_BUCKET_SPARK/spark-events`
      - `$MINIO_BUCKET_SPARK/spark-libs`

## How to start the services

```bash
docker-compose up -d
```

## Testing the MinIO service and buckets

A test script is available at `tests/check_cluster.sh` to check if MinIO is running and if the buckets/folders are created.

Run the script after starting the containers:

```bash
bash tests/check_cluster.sh
```

If everything is working, you will see success messages for MinIO and each bucket/folder.

## Project structure

- `docker-compose.yml`: Service configuration and bucket/folder creation.
- `tests/check_cluster.sh`: Script to test MinIO and bucket/folder existence.

## Access

MinIO Console: [http://localhost:9001](http://localhost:9001)