CREATE SCHEMA if not exists faker_gen;

SET search_path TO faker_gen;

-- create tables
create table products (
    id numeric primary key
    , item_name varchar(255) not null
    , price numeric not null
    , cost_price numeric not null
    , reorder_point numeric
    , description varchar(255)
);

create table inventory_shipment (
    id varchar(255) primary key
    , prod_id numeric
    , unit_received numeric
    , dt TIMESTAMP 
);

create table sale_transaction (
    id varchar(255) not null
    , prod_id numeric not null
    , prod_name varchar(255)
    , unit_sold numeric not null
    , reorder_point numeric 
    , regular_unit_price numeric not null
    , dt TIMESTAMP
);

-- init product data
COPY products from '/docker-entrypoint-initdb.d/products.csv' with (FORMAT csv, HEADER true);
alter table faker_gen.products add column max_inventory numeric default 0;

-- create user for streamlit
create user streamlit_dash with password 'postgres';
grant all privileges on database "postgres" to streamlit_dash;
GRANT USAGE ON SCHEMA faker_gen TO streamlit_dash;
GRANT SELECT ON ALL TABLES IN SCHEMA faker_gen TO streamlit_dash;