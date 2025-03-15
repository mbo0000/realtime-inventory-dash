FROM flink:1.20.0

# install python3 and pip3
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.4.0-1.20/flink-sql-connector-kafka-3.4.0-1.20.jar && wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/3.2.0-1.19/flink-connector-jdbc-3.2.0-1.19.jar && wget https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

COPY requirements.txt /opt/flink/

RUN pip install --no-cache-dir -r /opt/flink/requirements.txt