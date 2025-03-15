import streamlit as st
from confluent_kafka import Consumer
import pandas as pd
import json
import ast
from datetime import datetime

st.set_page_config(
    page_title="Inventory tracker",
    page_icon=":shopping_bags:", 
    layout='wide'
)


consumer_config = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'fake_sale_data_4',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
consumer.subscribe(['sale_info'])
placeholder = st.empty()

df = pd.DataFrame()

try:
    while True:
        msg = consumer.poll(0.5)  # Poll for messages with 0.5 second timeout

        if msg is None or not msg.value(): # ensure msg.value() is not none otherwise unable to process new messages
            print('No message')
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        event = msg.value().decode('utf-8')
        with placeholder:
            mdict = ast.literal_eval(event)
            tmp = {k:[mdict[k]] for k in mdict}
            cur_item = pd.DataFrame.from_dict(tmp)
            
            if len(df) > 0:
                df.drop(df[df['prod_id'] == mdict['prod_id']].index, inplace=True)   

            df = pd.concat([df, cur_item], ignore_index = True)
            st.dataframe(df, hide_index = True)

except Exception as e:
    print(e)
    
consumer.close()