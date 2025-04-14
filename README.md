# 🛍️ Realtime Inventory Dashboard
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Apache Flink](https://img.shields.io/badge/Apache%20Flink-E6526F?style=for-the-badge&logo=Apache%20Flink&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

This project involves creating an end-to-end streaming data pipeline, from ingestion to visualization. The goal is to develop a near-real-time inventory dashboard for a retail store, enabling employees to monitor daily transactions and inventory levels effectively.

![Diagram](https://github.com/mbo0000/realtime-inventory-dash/blob/main/images/dashboard.png)

## Objectives
- generate fake sale data, as source, using a python script
- produce and consume messages via Kafka
- data processing via Flink
- create visualization for inventory in realtime 

## Requirements
- Docker
- Streamlit
- Flink
- Kafka

## Design Architecture
![Diagram](https://github.com/mbo0000/realtime-inventory-dash/blob/main/images/pipeline_architecture.png)

- __Data Source__: [A Python script](https://github.com/mbo0000/realtime-inventory-dash/blob/main/datagen/sale_transaction.py) will generate fake sales transaction data, simulating simplified POS data from store checkouts. Additionally, the script will produce inventory shipment data when stock levels are low. The generated data will be pushed to Kafka topics.
- __Stream__: Kafka will be used as a messaging broker to stream sales data, inventory shipment, and inventory level data as they are generated at their sources.
- __Process__: Stream data from Kafka will be processed in a [Flink job](https://github.com/mbo0000/realtime-inventory-dash/blob/main/flink/code/job.py) to aggregate inventory and shipment data as [current inventory](https://github.com/mbo0000/realtime-inventory-dash/blob/main/flink/code/process/current_inventory.sql). The aggregated data will then be upserted back into Kafka  
- __BI Solution__: using Streamlit to provide a realtime inventory [monitoring dashboard](https://github.com/mbo0000/realtime-inventory-dash/blob/main/streamlit_dash/app.py) by subscribing to the inventory level topic.

### Considerations
- __Memory__: Keep in mind the available memory size, as aggregated data will be stored in-memory and forwarded to Kafka. If state management is needed, consider using a dedicated database like RocksDB for storing processed data. However, this would increase latency due to disk reads. For this project, state management is not required.
- __Flink Watermarking__: In real-world applications, stream data often originates from multiple sources and may arrive out of order. Watermarking in the data sources enables Flink to wait for a specified duration to include late-arriving data in processing. In this project, event time is used for watermarking in [sale transaction](https://github.com/mbo0000/realtime-inventory-dash/blob/main/flink/code/source/transaction.sql) and [inventory shipment](https://github.com/mbo0000/realtime-inventory-dash/blob/main/flink/code/source/inventory_shipment.sql) sources. Processed time should be considered if system-generated timestamps are required instead of event-driven timestamps.


## How to run project

1. Clone repo:

   ```
   git clone https://github.com/mbo0000/realtime-inventory-dash.git
   cd realtime-inventory-dash
   ```


2. Spin up infra

   ```
   make up 
   ```
   wait until execution is completed in terminal. DO NOT press any key to continue.

3. Open visualization

   ```
   make viz 
   ```
   or http://localhost:8501/

4. Tear down infra when ready:

   ```
   Ctrl + c
   make down
   ```

## Future Works:
- Employ persistent data storage solution for state management(e.g rockDB and Postgres)
- Monitor backpressure to prevent out-of-memory issues caused by data being generated faster than the system can process.
