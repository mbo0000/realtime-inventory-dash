create table sale_transaction (
    id STRING
    , prod_id INT
    , prod_name STRING
    , unit_sold INT
    , reorder_point INT
    , regular_unit_price DECIMAL(10,2)
    , dt TIMESTAMP(3)
) with (
    'connector' = 'jdbc'
    , 'url' = 'jdbc:postgresql://postgres:5432/postgres'
    , 'table-name' = 'faker_gen.sale_transaction'
    , 'username' = 'postgres'
    , 'password' = 'postgres'
    , 'driver' = 'org.postgresql.Driver'
)