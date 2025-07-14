FROM python:3.11-bullseye as spark-base
LABEL maintainer="Julio Zeferino <julioszeferino@gmail.com>"
LABEL description="Base image for Apache Spark Yarn with Python 3.11 on Debian Bullseye"
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
      ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"}

RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}

RUN curl https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz -o spark-3.5.0-bin-hadoop3.tgz \
 && tar xvzf spark-3.5.0-bin-hadoop3.tgz --directory /opt/spark --strip-components 1 \
 && rm -rf spark-3.5.0-bin-hadoop3.tgz

RUN curl https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz -o hadoop-3.3.6.tar.gz \
 && tar xfz hadoop-3.3.6.tar.gz --directory /opt/hadoop --strip-components 1 \
 && rm -rf hadoop-3.3.6.tar.gz

FROM spark-base as pyspark

RUN pip3 install --upgrade pip
COPY requirements/requirements.txt .
RUN pip3 install -r requirements.txt

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

ENV PATH="$SPARK_HOME/sbin:/opt/spark/bin:${PATH}"
ENV PATH="$HADOOP_HOME/bin:$HADOOP_HOME/sbin:${PATH}"
ENV PATH="${PATH}:${JAVA_HOME}/bin"

ENV SPARK_MASTER="spark://cluster-spark-master:7077"
ENV SPARK_MASTER_HOST cluster-spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3
ENV HADOOP_CONF_DIR="$HADOOP_HOME/etc/hadoop"
ENV HADOOP_CLASSPATH="/opt/hadoop/share/hadoop/tools/lib/*"

ENV LD_LIBRARY_PATH="$HADOOP_HOME/lib/native:${LD_LIBRARY_PATH}"

ENV YARN_RESOURCEMANAGER_USER="root"
ENV YARN_NODEMANAGER_USER="root"

RUN echo "export JAVA_HOME=${JAVA_HOME}" >> "$HADOOP_HOME/etc/hadoop/hadoop-env.sh"

COPY config/spark/spark-defaults-yarn.conf "$SPARK_HOME/conf/spark-defaults.conf"
COPY config/hadoop/*.xml "$HADOOP_HOME/etc/hadoop/"

RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

COPY jars/*.jar "$SPARK_HOME/jars/"
COPY jars/hadoop-aws-*.jar /opt/hadoop/share/hadoop/tools/lib/
COPY jars/aws-java-sdk-bundle-*.jar /opt/hadoop/share/hadoop/tools/lib/

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 22

ENTRYPOINT ["./entrypoint.sh"]

