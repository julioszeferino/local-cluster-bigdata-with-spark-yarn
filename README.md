# Project: Cluster with Docker Compose

## Services

- **MinIO**: S3-compatible storage service.
  - Required buckets:
    - `development` (landing zone)
      - `development/landing/...` (Spark writes data here)
    - `$MINIO_BUCKET_SPARK` (spark data)
      - `$MINIO_BUCKET_SPARK/spark-events`
      - `$MINIO_BUCKET_SPARK/spark-libs`

## How to start the services

```bash
docker compose -f docker-compose.yml up -d --scale cluster-spark-worker=1
```

## Usage with Spark

- Spark does not create buckets automatically, only directories inside existing buckets.
- Make sure the `development` bucket exists in MinIO before running Spark scripts that write to `s3a://development/landing/...`.
- Directories (paths) are created automatically by Spark during write operations.

## Adding new JARs

To add new JARs (libraries) for Spark jobs:

1. Place your JAR files in the `spark-libs` folder inside the `$MINIO_BUCKET_SPARK` bucket.
2. Example: Upload `my-library.jar` to `spark-libs` using the MinIO console or `mc` CLI:
   ```bash
   mc cp my-library.jar minio/$MINIO_BUCKET_SPARK/spark-libs/
   ```
3. When submitting a Spark job, reference the JARs using the `--jars` option:
   ```bash
   spark-submit --jars s3a://$MINIO_BUCKET_SPARK/spark-libs/my-library.jar ...
   ```

## How to run a Spark job

To execute a Spark job in the cluster:

1. Copy your Python script to the master container or mount it via Docker.
2. Use `spark-submit` to run the job:
   ```bash
   docker exec cluster-spark-master spark-submit --deploy-mode client /path/to/your_script.py
   ```
   - Example for the provided test script:
     ```bash
     docker exec cluster-spark-master spark-submit --deploy-mode client ./jobs/local_tests/upload_files_to_minio.py
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
- `jobs/local_tests/upload_files_to_minio.py`: Spark script that reads local files and writes to MinIO (requires bucket existence).

## Access

MinIO Console: [http://localhost:9001](http://localhost:9001)  
Spark History: [http://localhost:18080](http://localhost:18080)

## Best Practices

- **Environment Variables:** Store sensitive information (e.g., access keys) in environment variables or secret managers, not directly in code.
- **Version Control:** Keep your Docker Compose, Spark scripts, and configuration files under version control (e.g., Git).
- **Resource Management:** Adjust Spark worker memory and cores in `docker-compose.yml` according to your workload and available hardware.
- **Monitoring:** Use Spark History Server and MinIO Console to monitor job execution and storage usage.
- **Error Handling:** Always check logs for errors after running jobs. Handle exceptions in your Spark scripts to avoid silent failures.
- **Data Organization:** Organize your data in MinIO buckets using clear and consistent folder structures for easier management and access.
- **Dependencies:** Document and manage Python and JAR dependencies for reproducibility. Use requirements.txt for Python and keep JARs versioned.
- **Security:** If exposing services outside localhost, configure authentication and network policies for MinIO and Spark.

## Troubleshooting

- If you get `NoSuchBucket` errors, verify that the required bucket exists in MinIO.
- For permission issues, check your MinIO access/secret keys and bucket policies.
- For Spark job failures, review the Spark History Server and container logs for details.

