"""
====================================================================
docker exec cluster-spark-master spark-submit --master yarn --deploy-mode client ./jobs/local_tests/read_files_from_minio.py

====================================================================
"""
import os

from pyspark import SparkConf
from pyspark.sql import SparkSession

from utils.logger import setup_logger


def sessao_spark(app_name):
    minio_endpoint = "http://minio:9000"
    minio_access_key = "minioadmin"
    minio_secret_key = "minioadmin"
    spark = (
        SparkSession
        .builder
        .appName(app_name)
        .master("yarn")
        .config("spark.executor.memory", "2g")
        .config("spark.executor.cores", "2")
        .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint)
        .config("spark.hadoop.fs.s3a.access.key", minio_access_key)
        .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key)
        .config("spark.hadoop.fs.s3a.multipart.size", "104857600")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.fast.upload", "true")
        .config("spark.hadoop.fs.s3a.connection.maximum", "100")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.adaptive.enabled", True)
        .config("spark.sql.adaptive.coalescePartitions.enabled", True)
        .config("spark.sql.adaptive.skewJoin.enabled", True)
        .getOrCreate()
    )
    return spark

def main():
    spark = sessao_spark('ch01-basic-query-aqe')
    logger = setup_logger()
    logger.info("Iniciando o script.")

    # configs
    logger.info(spark)
    logger.info(f"Configs: {spark.sparkContext.getConf().getAll()}")
    spark.sparkContext.setLogLevel("INFO")
    minio_bucket = "development/landing"

    logger.info("Executando a task.")

    logger.info("Leitura do Arquivo de Clientes.")
    file_clientes = spark.read.parquet(
        f"s3a://{minio_bucket}/postgres/csv/clientes"
    )
    file_clientes.show()

    logger.info("Leitura do Arquivo de Pedidos.")
    file_pedidos = spark.read.parquet(
        f"s3a://{minio_bucket}/redshift/json/estoque"
    )
    file_pedidos.show()

    logger.info("Script concluído.")
    spark.stop()

if __name__ == "__main__":
    main()