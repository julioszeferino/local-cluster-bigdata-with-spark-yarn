CREATE SCHEMA minio.bronze WITH (location = 's3a://production/bronze/');
CREATE SCHEMA minio.silver WITH (location = 's3a://production/silver/');
CREATE SCHEMA minio.gold WITH (location = 's3a://production/gold/');


-- CREATE TABLE IF NOT EXISTS minio.bronze.vendas (
--     indicador_id BIGINT,
--     indicador_nome VARCHAR
-- )
-- WITH (
--     format = 'PARQUET',
--     external_location = 's3a://data-lake/bronze/vendas/'
-- );