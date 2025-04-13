create table current_inventory (
    prod_id INT
    , prod_name STRING
    , regular_unit_price DECIMAL(10,2)
    , reorder_point INT
    , total_sold INT
    , unit_left INT
    , PRIMARY KEY (prod_id) NOT ENFORCED
) with (
    'connector'                         = 'upsert-kafka'
    , 'topic'                           = 'sale_info'
    , 'properties.bootstrap.servers'    = 'kafka:9092'
    , 'key.format'                      = 'json'
    , 'value.format'                    = 'json'
)