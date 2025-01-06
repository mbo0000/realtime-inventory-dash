FROM python:3.11-slim

WORKDIR /opt/dataload

COPY requirements.txt /opt/dataload/

RUN pip install --no-cache-dir -r /opt/dataload/requirements.txt

CMD ["tail" "-F" "anything"]