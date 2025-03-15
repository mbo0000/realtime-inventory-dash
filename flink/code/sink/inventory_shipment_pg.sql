create table inventory_shipment_pg (
    id STRING
    , prod_id INT
    , unit_received INT
    , dt TIMESTAMP(3) 
) with (
    'connector' = 'jdbc'
    , 'url' = 'jdbc:postgresql://postgres:5432/postgres'
    , 'table-name' = 'faker_gen.inventory_shipment'
    , 'username' = 'postgres'
    , 'password' = 'postgres'
    , 'driver' = 'org.postgresql.Driver'
)