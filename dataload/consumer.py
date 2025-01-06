import time
from confluent_kafka import Consumer
import psycopg2
import json
import logging

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

def load_data(event, conn):
    'push consumer event data into db'
    event_dict          = json.loads(event)
    id                  = event_dict['id']
    prod_id             = event_dict['prod_id']
    unit_sold           = event_dict['unit_sold']
    regular_unit_price  = event_dict['regular_unit_price']
    dt                  = event_dict['dt']
    
    try:
        conn.cursor().execute(f"insert into postgres.faker_gen.transaction_events (id, prod_id, unit_sold, regular_unit_price, dt) values('{id}', '{prod_id}', '{unit_sold}', '{regular_unit_price}', '{dt}'::timestamp);")
        conn.commit()
    except psycopg2.Error as e:
        logging.error(f'Postgres Error msg: {e}')
    finally:
        pass

if __name__ == '__main__':
    pg_conn = _get_pg_conn()

    # Create a consumer instance
    consumer_config = {
        'bootstrap.servers': 'kafka:9092',  # Replace with Kafka broker address
        'group.id': 'fake_data',  # Define a consumer group ID for effective load balance
        'auto.offset.reset': 'earliest'  # Read from beginning if no previous offset
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe([TOPIC])
    
    try:
        while pg_conn:
            msg = consumer.poll(0.5)  # Poll for messages with 0.5 second timeout

            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            event = msg.value().decode('utf-8')
            load_data(event, pg_conn)
            print(event)
    except KeyboardInterrupt:
        consumer.close()
        pg_conn.close()