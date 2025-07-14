# Project: Cluster with Docker Compose

## Services

- **MinIO**: S3-compatible storage service.
  - Required buckets:
    - `development` (landing zone)
      - `development/landing/...` (Spark writes data here)
    - `spark-data` (spark data)
      - `spark-data/spark-events`
      - `spark-data/spark-libs`

- **Hive Metastore**: Centralized metadata repository for Spark and Hive.
  - Uses PostgreSQL as the backend database
  - Stores table schemas, partitions, and storage locations
  - Enables data catalog functionality for Spark SQL

- **PostgreSQL**: Database backend for Hive Metastore.

## How to start the services

```bash
docker compose -f docker-compose.yml up -d --scale cluster-spark-worker=3
```

## Usage with Spark

- Spark does not create buckets automatically, only directories inside existing buckets.
- Make sure the `development` and `spark-data` buckets exist in MinIO before running Spark scripts.
- Directories (paths) are created automatically by Spark during write operations.
- With Hive Metastore, you can create managed and external tables that persist metadata across Spark sessions.

## Hive Metastore Integration

The Hive Metastore service provides:
- **Persistent metadata storage**: Table schemas and locations are stored in PostgreSQL
- **Cross-session data access**: Tables created in one Spark session are available in others
- **Data catalog functionality**: Use `SHOW TABLES`, `DESCRIBE TABLE`, etc.
- **Partition management**: Automatic partition discovery and management

### Creating tables with Hive Metastore:
```sql
-- Create external table pointing to MinIO
CREATE TABLE IF NOT EXISTS my_table (
    id INT,
    name STRING,
    created_at TIMESTAMP
) USING DELTA
LOCATION 's3a://development/tables/my_table'
```

## Spark Deploy Modes

### Client Mode (`--deploy-mode client`)
- Driver runs on the client machine (where you execute spark-submit)
- Easier for development and debugging (logs appear directly in terminal)
- Has access to local configurations and dependencies
- Better for interactive development

### Cluster Mode (`--deploy-mode cluster`)
- Driver runs on the YARN cluster
- Better for production environments
- All dependencies must be available on cluster nodes
- Logs are available through YARN ResourceManager UI
- More robust for long-running jobs

## Adding new JARs

To add new JARs (libraries) for Spark jobs:

1. Place your JAR files in the `spark-libs` folder inside the `spark-data` bucket.
2. Example: Upload `my-library.jar` to `spark-libs` using the MinIO console or `mc` CLI:
   ```bash
   mc cp my-library.jar minio/spark-data/spark-libs/
   ```
3. JARs are automatically loaded via `spark-defaults.conf` configuration.

## How to run a Spark job

To execute a Spark job in the cluster:

### Client Mode (Development)
```bash
docker exec cluster-spark-master spark-submit --master yarn --deploy-mode client /path/to/your_script.py
```

### Cluster Mode (Production)
```bash
docker exec cluster-spark-master spark-submit --master yarn --deploy-mode cluster /path/to/your_script.py
```

### Example scripts:
- **Upload files to MinIO:**
  ```bash
  docker exec cluster-spark-master spark-submit --master yarn --deploy-mode client ./jobs/local_tests/upload_files_to_minio.py
  ```
- **Read files from MinIO:**
  ```bash
  docker exec cluster-spark-master spark-submit --master yarn --deploy-mode client ./jobs/local_tests/read_files_from_minio.py
  ```

## Configuration Files

- `config/spark/spark-defaults-yarn.conf`: Default Spark configuration for YARN mode
- `config/hadoop/*.xml`: Hadoop configuration files
- `config/spark/jupyter.dockerfile`: Jupyter notebook with Spark integration
- `config/hive/`: Hive Metastore configuration files

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
- `jobs/local_tests/upload_files_to_minio.py`: Spark script that reads local files and writes to MinIO.
- `jobs/local_tests/read_files_from_minio.py`: Spark script that reads files from MinIO.
- `config/spark/`: Spark configuration files including spark-defaults for YARN.
- `config/hadoop/`: Hadoop configuration files.
- `config/hive/`: Hive Metastore configuration files.

## Access

MinIO Console: [http://localhost:9001](http://localhost:9001)  
Spark History: [http://localhost:18080](http://localhost:18080)  
YARN ResourceManager: [http://localhost:8088](http://localhost:8088)  
Hive Metastore: Available via Spark SQL (no direct web UI)

## Best Practices

- **Environment Variables:** Store sensitive information (e.g., access keys) in environment variables or secret managers, not directly in code.
- **Version Control:** Keep your Docker Compose, Spark scripts, and configuration files under version control (e.g., Git).
- **Resource Management:** Adjust Spark worker memory and cores in `docker-compose.yml` according to your workload and available hardware.
- **Monitoring:** Use Spark History Server, YARN ResourceManager UI, and MinIO Console to monitor job execution and storage usage.
- **Error Handling:** Always check logs for errors after running jobs. Handle exceptions in your Spark scripts to avoid silent failures.
- **Data Organization:** Organize your data in MinIO buckets using clear and consistent folder structures for easier management and access.
- **Dependencies:** Document and manage Python and JAR dependencies for reproducibility. Use requirements.txt for Python and keep JARs versioned.
- **Security:** If exposing services outside localhost, configure authentication and network policies for MinIO and Spark.
- **Deploy Mode:** Use client mode for development/debugging and cluster mode for production.
- **Hive Metastore:** Use external tables for data stored in MinIO to maintain data location flexibility.
- **Table Management:** Regularly clean up unused tables and partitions to maintain Metastore performance.

## Troubleshooting

- If you get `NoSuchBucket` errors, verify that the required buckets (`development`, `spark-data`) exist in MinIO.
- For permission issues, check your MinIO access/secret keys and bucket policies.
- For Spark job failures, review the YARN ResourceManager logs and Spark History Server for details.
- If cluster mode fails but client mode works, check that all dependencies are available on cluster nodes.
- Event logs are stored in `s3a://spark-data/spark-events` and accessible via Spark History Server.
- **Hive Metastore issues:** Check PostgreSQL container logs if tables are not persisting or metadata queries fail.
- **Connection errors:** Ensure Hive Metastore service is running before starting Spark jobs that access tables.
- **Schema evolution:** When table schemas change, use `REFRESH TABLE` or `MSCK REPAIR TABLE` to update metadata.

