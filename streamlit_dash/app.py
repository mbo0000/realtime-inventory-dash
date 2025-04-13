import streamlit as st
from confluent_kafka import Consumer
import altair as alt
import ast
import pandas as pd
from dataclasses import dataclass

st.set_page_config(
    page_title="Inventory tracker",
    page_icon=":shopping_bags:", 
    layout='wide'
)

TOPICS = ['sale_info']

# -----------------------------------------------------------------------------

def get_consumer_config():
    consumer = Consumer({
        'bootstrap.servers'     : 'kafka:9092'
        , 'group.id'            : 'sale_group_2'
        , 'auto.offset.reset'   : 'latest'
    })
    return consumer

def update_df(event, df):

    mdict       = ast.literal_eval(event)
    tmp         = {k:[mdict[k]] for k in mdict}
    cur_item    = pd.DataFrame.from_dict(tmp)
    
    if len(df) > 0:
        df = df[df['prod_id'] != mdict['prod_id']] 

    df = pd.concat([df, cur_item], ignore_index = True)
    return df


def main():
    consumer = get_consumer_config()
    consumer.subscribe(TOPICS)

    df      = pd.DataFrame()
    cont    = st.empty()

    while True:
        msg = consumer.poll(0.5)  # Poll for messages with 0.5 second timeout

        if msg is None or not msg.value(): # ensure msg.value() is not none otherwise unable to process new messages
            print('No message')
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
    
        event   = msg.value().decode('utf-8')
        df      = update_df(event, df)

        with cont.container():

            chart1, chart2 = st.columns(2)
            with chart1:
                st.subheader("Inventory Level", divider="red")
                st.altair_chart(
                    # Layer 1: Bar chart.
                    alt.Chart(df)
                    .mark_bar(
                        orient="horizontal",
                    )
                    .encode(
                        x="unit_left",
                        y="prod_name",
                    )

                    # Layer 2: Chart showing the reorder point.
                    + alt.Chart(df)
                    .mark_point(
                        shape="diamond",
                        filled=True,
                        size=50,
                        color="salmon",
                        opacity=1,
                    )
                    .encode(
                        x="reorder_point",
                        y="prod_name",
                    ),
                    use_container_width=True,
                )
                st.caption("NOTE: The :diamonds: location shows the reorder point.")

            with chart2:
                st.subheader("Best sellers", divider="orange")
                st.altair_chart(
                    alt.Chart(df)
                    .mark_bar(orient="horizontal")
                    .encode(
                        x="total_sold",
                        y=alt.Y("prod_name").sort("-x"),
                    ),
                    use_container_width=True,
                )

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()