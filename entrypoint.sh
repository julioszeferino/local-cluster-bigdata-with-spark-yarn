#!/bin/bash

SPARK_WORKLOAD=$1

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"

/etc/init.d/ssh start

if [ "$SPARK_WORKLOAD" == "master" ];
then
  echo "Starting ResourceManager..."
  yarn --daemon start resourcemanager
  echo "ResourceManager started."

elif [ "$SPARK_WORKLOAD" == "worker" ];
then
  echo "Starting Worker..."
  yarn --daemon start nodemanager
  echo "Worker started."

elif [ "$SPARK_WORKLOAD" == "history" ];
then
  echo "Starting History Server..."
  start-history-server.sh
  echo "History Server started."
fi

tail -f /dev/null
