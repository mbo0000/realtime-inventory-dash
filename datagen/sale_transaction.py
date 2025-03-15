import random
import pandas as pd
import time
from datetime import datetime,timezone
from faker import Faker
from confluent_kafka import Producer
import json
import psycopg2
import logging

fake            = Faker()
products_info   = {}
PRODUCER        = Producer({'bootstrap.servers': 'kafka:9092'})
MAX_UNIT        = 500

def _get_pg_conn():
    # connect to postgres server

    attempts = 3
    while attempts > 0:
        try:
            conn = psycopg2.connect(
                dbname      = "postgres",
                user        = "postgres",
                password    = "postgres",
                host        = "postgres"
            )
            print('authenticated')
            return conn
        except psycopg2.OperationalError as e:
            logging.error(e)
            attempts -= 1
            logging.info('Re-attempt to connect to Postgres')
            time.sleep(5)
    return None

def get_products():
    # get product data from pg
    pg_conn                     = _get_pg_conn()
    query                       = 'select * from faker_gen.products;'
    res                         = pd.read_sql(query, pg_conn)

    pg_conn.close()

    return res

def init_shipment(prod):
    # init shipment info, only once at startup
    for index, row in prod.iterrows():
        gen_inventory_shipment(row)

def init_products_info(prod):
    # init prod info, only once at startup
    for index, row in prod.iterrows():
        item_id = row['id']
        products_info[item_id] = {
            'unit_sold' : 0
            , 'unit_shipment' : 0
        }

def push_to_kafka(event, topic):
    # push event data to kafka producer
    PRODUCER.produce(topic, json.dumps(event).encode('utf-8'))
    PRODUCER.flush()

def gen_inventory_shipment(item):
    # generate shipment detail when inventory is low or init shipments at startup

    item_id         = item['id']
    reorder_point   = item['reorder_point']
    total_unit_sold = products_info[item_id]['unit_sold'] # all time sold
    total_shipment  = products_info[item_id]['unit_shipment'] # all time shipment

    if (total_shipment - total_unit_sold) > reorder_point:
        return 

    shipment = {
        'id'              : fake.unique.uuid4()
        , 'prod_id'       : int(item_id)
        , 'unit_received' : MAX_UNIT
        , 'dt'            : datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    }

    products_info[item_id]['unit_shipment'] += MAX_UNIT
    push_to_kafka(shipment, 'inventory_shipment')

def gen_transac_item(id, n_unit_sold, prod):
    # generate fake transaction data
    item_id             = int(prod['id'])
    item_name           = str(prod['item_name'])
    reorder_point       = int(prod['reorder_point'])
    regular_unit_price  = float(prod['price'])

    transaction = {
            'id'                    : id
            , 'prod_id'             : item_id
            , 'prod_name'           : item_name
            , 'unit_sold'           : n_unit_sold
            , 'reorder_point'       : reorder_point
            , 'regular_unit_price'  : regular_unit_price
            , 'dt'                  : datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        }

    products_info[item_id]['unit_sold'] += n_unit_sold
    push_to_kafka(transaction, 'sale_transaction')

def gen_transac_data(prod):
    # gen fake data minicking a sale receipt

    id              = fake.unique.uuid4() # receipt/transac id
    n_prod          = random.randint(1,10) # number of unique items per receipt
    curr_item       = set()

    for _ in range(n_prod):
        n_unit_sold = random.randint(1,10) # rand unit sold num per product for each transaction
        rand_prod   = random.randint(0, len(prod)-1) # rand product in the products table

        if rand_prod in curr_item: # not already in the current cart
            continue 

        curr_item.add(rand_prod)
        item = prod.iloc[rand_prod]
   
        gen_transac_item(id, n_unit_sold, item)
        gen_inventory_shipment(item)

if __name__ == '__main__':
    
    products = get_products()

    init_products_info(products)
    init_shipment(products)

    while True:
        time.sleep(random.randint(1,3))
        gen_transac_data(products)