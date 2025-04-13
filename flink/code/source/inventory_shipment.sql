create table inventory_shipment (
    id STRING
    , prod_id INT
    , unit_received INT
    , dt TIMESTAMP(3) 
    , WATERMARK FOR dt AS dt - INTERVAL '15' SECOND
) with (
    'connector'                         = 'kafka'
    , 'topic'                           = 'inventory_shipment'
    , 'properties.bootstrap.servers'    = 'kafka:9092'
    , 'properties.group.id'             = 'shipment_group_1'
    , 'scan.startup.mode'               = 'earliest-offset'
    , 'format'                          = 'json'
)