from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
import os
import time

JARS = [
    'file:///opt/flink/flink-sql-connector-kafka-3.4.0-1.20.jar'
    , 'file:///opt/flink/flink-connector-jdbc-3.2.0-1.19.jar'
    , 'file:///opt/flink/postgresql-42.7.3.jar'
]

def read_sql(dir, file_name):
    # read ddl sql file
    current_file_dir    = os.path.dirname(os.path.abspath(__file__))
    file_path           = os.path.join(current_file_dir, dir + '/' + file_name)
    
    with open(file_path, 'r') as file:
        return file.read()

def main():
    # config
    stream_env = StreamExecutionEnvironment.get_execution_environment()
    stream_env.enable_checkpointing(10 * 1000)
    stream_env.get_checkpoint_config().set_checkpoint_timeout(
        5 * 1000
    )
    stream_env.get_checkpoint_config().set_min_pause_between_checkpoints(
        5 * 1000
    )

    for jar in JARS:
        stream_env.add_jars(jar)

    table_env = StreamTableEnvironment.create(stream_env)
    job_config = table_env.get_config().get_configuration()
    job_config.set_string("pipeline.name", 'sale_data')

    # add source
    table_env.execute_sql(read_sql('source', 'transaction.sql'))
    table_env.execute_sql(read_sql('source', 'inventory_shipment.sql'))

    # add sink
    table_env.execute_sql(read_sql('sink', 'sale_transaction.sql'))
    table_env.execute_sql(read_sql('sink', 'inventory_shipment_pg.sql'))
    table_env.execute_sql(read_sql('sink', 'current_inventory.sql'))

    # run process query
    st_exec = table_env.create_statement_set()\
        .add_insert_sql(read_sql('process', 'sale_transaction.sql'))\
        .add_insert_sql(read_sql('process', 'inventory_shipment.sql'))\
        .add_insert_sql(read_sql('process', 'current_inventory.sql'))\
        .execute()

    # print
    table_env.from_path('current_inventory').execute().print()

if __name__ == '__main__':
    main()