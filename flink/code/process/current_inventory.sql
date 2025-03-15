insert into 
    current_inventory
select
    t.prod_id
    , t.prod_name
    , t.regular_unit_price
    , t.reorder_point
    , t.total_sold
    , (s.total_received - t.total_sold) as unit_left
from (
    select
        prod_id
        , prod_name
        , regular_unit_price
        , reorder_point
        , sum(unit_sold) as total_sold
    from transaction
    group by 
        prod_id
        , prod_name
        , regular_unit_price
        , reorder_point
) as t join (
    select 
        prod_id
        , sum(unit_received) as total_received
    from inventory_shipment
    group by prod_id
) as s on t.prod_id = s.prod_id

;