"""
====================================================================
docker exec cluster-spark-master spark-submit --master yarn --deploy-mode client ./jobs/local_tests/read_files_with_hive.py

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

    hive_metastore_uri = "thrift://hive-metastore:9083"

    spark = (
        SparkSession
        .builder
        .appName(app_name)
        .master("yarn") 
        .config("spark.executor.memory", "2g")
        .config("spark.executor.cores", "2")
        .config("hive.metastore.uris", hive_metastore_uri)
        .config("spark.sql.catalogImplementation", "hive")
        .config("spark.hadoop.fs.s3a.endpoint", f"{minio_endpoint}")
        .config("spark.hadoop.fs.s3a.access.key", f"{minio_access_key}")
        .config("spark.hadoop.fs.s3a.secret.key", f"{minio_secret_key}")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.sql.warehouse.dir", "s3a://production/warehouse")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.catalog.local", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.catalog.local.warehouse", "s3a://production/warehouse")
        .enableHiveSupport()
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
    spark.sparkContext.setLogLevel("ERROR")

    logger.info("Executando a task.")

    # eu quero testar as funcionalidades do Hive, como criar tabelas usando delta
    # verificar tabelas e etc, para ver se esta tudo funcionando corretamente
    logger.info("Leitura do Arquivo de Clientes.")
    file_clientes = spark.read.parquet(
        f"s3a://development/landing/postgres/csv/clientes"
    )
    file_clientes.show()

    logger.info("Criando tabela Hive para Clientes.")
    file_clientes.createOrReplaceTempView("clientes")

    logger.info("Executando consulta Hive.")
    query = """
    SELECT * FROM clientes
    """
    result = spark.sql(query)
    result.show()

    spark.sql("CREATE DATABASE IF NOT EXISTS landing_development")

    logger.info("Salvando resultado em tabela Delta.")
    result.write.format("delta").mode("overwrite").saveAsTable("landing_development.clientes_delta")

    logger.info("Tabela Delta criada com sucesso.")
    delta_result = spark.read.format("delta").table("landing_development.clientes_delta")
    delta_result.show()
    

    logger.info("Script concluído.")
    spark.stop()

if __name__ == "__main__":
    main()