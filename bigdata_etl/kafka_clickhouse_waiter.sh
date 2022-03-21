#!/bin/sh

echo "Waiting for Kafka db..."
while ! nc -z broker 29092; do
  sleep 30
done
echo "Kafka db started"

echo "Waiting for ClickHouse db..."
while ! nc -z clickhouse-node1 9000; do
  sleep 30
done
while ! nc -z clickhouse-node2 9000; do
  sleep 30
done
while ! nc -z clickhouse-node3 9000; do
  sleep 30
done
while ! nc -z clickhouse-node4 9000; do
  sleep 30
done
echo "ClickHouse db started"

echo "Waiting for control center..."
while ! nc -z control-center 9021; do
  sleep 30
done
echo "control-center started"

exec "$@"
