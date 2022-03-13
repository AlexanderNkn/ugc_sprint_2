FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY ["requirements.txt", "kafka_clickhouse_waiter.sh", "./"]

RUN apt update && apt install -y netcat \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* \
    && chmod +x /usr/src/code/kafka_clickhouse_waiter.sh

ENTRYPOINT ["/usr/src/code/kafka_clickhouse_waiter.sh"]

COPY ["etl_kafka_clickhouse.py", "./"]

CMD ["python3", "etl_kafka_clickhouse.py"]
