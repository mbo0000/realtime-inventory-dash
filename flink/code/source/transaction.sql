create table transaction (
    id STRING
    , prod_id INT
    , prod_name STRING
    , unit_sold INT
    , reorder_point INT
    , regular_unit_price DECIMAL
    , dt TIMESTAMP(3)
    , WATERMARK FOR dt AS dt - INTERVAL '15' SECOND
) with (
    'connector' = 'kafka'
    , 'topic' = 'sale_transaction'
    , 'properties.bootstrap.servers' = 'kafka:9092'
    , 'properties.group.id' = 'sale_group_1'
    , 'scan.startup.mode' = 'earliest-offset'
    , 'format' = 'json'
)