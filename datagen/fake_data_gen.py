import random
import pandas as pd
import time
from datetime import datetime
from faker import Faker
from confluent_kafka import Producer
import json
import psycopg2
import logging

fake    = Faker()
TOPIC   = 'sale_transaction'

def _get_pg_conn():
    'connect to postgres server'

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
    pg_conn                     = _get_pg_conn()
    query                       = 'select * from faker_gen.products;'
    res                         = pd.read_sql(query, pg_conn)

    res.rename(columns = {'max_inventory':'current_inventory'}, inplace = True)
    pg_conn.close()

    return res

def push_to_kafka(event, topic):
    'push event data to kafka producer'
    producer = Producer({'bootstrap.servers': 'kafka:9092'})
    producer.produce(topic, json.dumps(event).encode('utf-8'))
    producer.flush()

def gen_transac_item(id, n_unit_sold, prod):
    'generate fake transaction data'
    prod_id             = int(prod['id'])
    regular_unit_price  = float(prod['price'])
    transaction = {
            'id'                    : id
            , 'prod_id'             : prod_id
            , 'unit_sold'           : n_unit_sold
            , 'regular_unit_price'  : regular_unit_price
            , 'dt'                  : datetime.now().utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        }
    return transaction

def has_inventory(idx, n_unit, prod):
    return bool(prod.loc[idx, 'current_inventory'] >= n_unit)

def gen_transac_data(prod):
    'gen fake data minicking a sale receipt'
    id              = fake.unique.uuid4() # receipt/transac id
    n_prod          = random.randint(1,10) # number of unique prod per receipt
    curr_item       = set()

    for _ in range(n_prod):
        n_unit_sold = random.randint(1,10) # rand unit sold num per product for each transaction
        rand_prod   = random.randint(0, len(prod)-1) # rand product in the products table

        if not has_inventory(rand_prod, n_unit_sold, prod): # make sure product is in stock
            continue
        if rand_prod in curr_item: # not already in the current cart
            continue 

        curr_item.add(rand_prod)
        prod.loc[rand_prod,'current_inventory'] -= n_unit_sold 
        
        transac     = gen_transac_item(id, n_unit_sold, prod.iloc[rand_prod])
        push_to_kafka(transac, TOPIC)

if __name__ == '__main__':
    
    products = get_products()

    while True:
        gen_transac_data(products)
        time.sleep(random.randint(1,3))