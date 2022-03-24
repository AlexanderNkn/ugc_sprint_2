#!/bin/sh

sleep 10 && mongo --host mongodb://mongo1:27017 config-replica.js && \
sleep 10 && mongo --host mongodb://mongo1:27017 config-data.js
# exponential back off as kafka connect starts
curl --connect-timeout 5 \
     --max-time 10 \
     --retry 10 \
     --retry-delay 0 \
     --retry-max-time 80 \
     --retry-connrefused \
     -X POST -H "Content-Type: application/json" --data @sink-movie-likes-connector.json http://connect:8083/connectors -w "\n"
curl -X POST -H "Content-Type: application/json" --data @sink-review-likes-connector.json http://connect:8083/connectors -w "\n"
curl -X POST -H "Content-Type: application/json" --data @sink-reviews-connector.json http://connect:8083/connectors -w "\n"
curl -X POST -H "Content-Type: application/json" --data @sink-bookmarks-delete-connector.json http://connect:8083/connectors -w "\n"
curl -X POST -H "Content-Type: application/json" --data @sink-bookmarks-add-connector.json http://connect:8083/connectors -w "\n"
# print all connectors added to kafka connect
curl -X GET http://connect:8083/connectors
