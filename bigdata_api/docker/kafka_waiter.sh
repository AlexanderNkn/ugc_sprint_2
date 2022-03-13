#!/bin/sh

if [ "$KAFKA_DB" = "kafka" ]
then
    echo "Waiting for Kafka db..."

    while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
      sleep 0.1
    done

    echo "Kafka db started"
fi

exec "$@"
