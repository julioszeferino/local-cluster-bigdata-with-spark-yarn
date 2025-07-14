FROM python:3.11-bullseye as spark-base
LABEL maintainer="Julio Zeferino <julioszeferino@gmail.com>"
LABEL description="Base image for Apache Spark with Python 3.11 on Debian Bullseye"
LABEL version="1.0"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo \
    curl \
    vim \
    nano \
    unzip \
    rsync \
    openjdk-11-jdk \
    build-essential \
    software-properties-common \
    ssh \
    dos2unix && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"}

RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}

RUN curl https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz -o spark-3.5.0-bin-hadoop3.tgz \
 && tar xvzf spark-3.5.0-bin-hadoop3.tgz --directory /opt/spark --strip-components 1 \
 && rm -rf spark-3.5.0-bin-hadoop3.tgz

FROM spark-base as pyspark

ADD requirements/requirements.txt .
RUN pip3 install -r requirements.txt

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
ENV PATH="${PATH}:${JAVA_HOME}/bin"

ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"
ENV SPARK_HOME="/opt/spark"
ENV SPARK_MASTER="spark://cluster-spark-master:7077"
ENV SPARK_MASTER_HOST="cluster-spark-master"
ENV SPARK_MASTER_PORT=7077
ENV PYSPARK_PYTHON=python3
ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

ADD config/spark/spark-defaults.conf "$SPARK_HOME/conf"
ADD entrypoint.sh .
ADD jars/*.jar "$SPARK_HOME/jars/"

RUN dos2unix entrypoint.sh

RUN chmod u+x entrypoint.sh && \
    chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

ENTRYPOINT ["/opt/spark/entrypoint.sh"]
