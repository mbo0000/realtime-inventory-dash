CREATE SCHEMA if not exists faker_gen;

SET search_path TO faker_gen;

-- create tables
create table if not exists products (
    id numeric primary key
    , item_name varchar(255) not null
    , price numeric not null
    , cost_price numeric not null
    , reorder_point numeric
    , description varchar(255)

);

create table if not exists transaction_events (
    id varchar(255) not null
    , prod_id numeric not null
    , unit_sold numeric not null
    , regular_unit_price numeric not null
    , dt TIMESTAMP
);

-- load product data
COPY products from '/docker-entrypoint-initdb.d/products.csv' with (FORMAT csv, HEADER true);
alter table faker_gen.products add column max_inventory numeric default 500;

-- create user for streamlit
create user streamlit_dash with password 'postgres';
grant all privileges on database "postgres" to streamlit_dash;
GRANT USAGE ON SCHEMA faker_gen TO streamlit_dash;
GRANT SELECT ON ALL TABLES IN SCHEMA faker_gen TO streamlit_dash;