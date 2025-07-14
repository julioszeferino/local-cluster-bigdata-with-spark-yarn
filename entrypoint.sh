#!/bin/bash

SPARK_WORKLOAD=$1

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"

if [ "$SPARK_WORKLOAD" == "master" ]; then
  # cp /opt/spark/jars_personalizados/*.jar /opt/spark/jars/
  start-master.sh -p 7077
elif [ "$SPARK_WORKLOAD" == "worker" ]; then
  start-worker.sh spark://cluster-spark-master:7077
elif [ "$SPARK_WORKLOAD" == "history" ]; then
  start-history-server.sh
fi
