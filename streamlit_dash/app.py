import streamlit as st
import altair as alt
import time

st.set_page_config(
    page_title="Inventory tracker",
    page_icon=":shopping_bags:", 
    layout='wide'
)

# -----------------------------------------------------------------------------
def connect_db():
    """Connects to the local postgres db."""
    return st.connection("postgresql", type="sql")

def execute(conn):
    cont = st.empty()
    sales = '''
            select 
                te.prod_id
                , p.item_name
                , p.reorder_point
                , sum(te.unit_sold) units_sold
                , p.max_inventory - sum(te.unit_sold) as units_left
                , round(sum(te.unit_sold) * regular_unit_price, 2) as unit_sale
            from 
                faker_gen.transaction_events as te
                join faker_gen.products as p on te.prod_id = p.id
            group by 1, p.max_inventory, p.reorder_point, p.item_name, te.regular_unit_price
            ;
            '''

    while True:
        df = conn.query(sales, ttl="1")

        with cont.container():
            chart1, chart2 = st.columns(2)
            with chart1:
                st.subheader("Units left", divider="red")
                st.altair_chart(
                    # Layer 1: Bar chart.
                    alt.Chart(df)
                    .mark_bar(
                        orient="horizontal",
                    )
                    .encode(
                        x="units_left",
                        y="item_name",
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
                        y="item_name",
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
                        x="units_sold",
                        y=alt.Y("item_name").sort("-x"),
                    ),
                    use_container_width=True,
                )

        time.sleep(1)

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    conn = connect_db()
    execute(conn)










# https://blog.streamlit.io/how-to-build-a-real-time-live-dashboard-with-streamlit/
# https://share.streamlit.io/template-preview/00b8b074-cd51-45f1-90d5-2f9af46686ee
# https://kafka.apache.org/quickstart#quickstart_send