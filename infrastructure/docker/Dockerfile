FROM python:3.8.9-slim

RUN apt-get update && \
    apt-get -y install git findutils build-essential unzip wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD . .

RUN pip3 install keyrings.google-artifactregistry-auth==0.0.3 --index-url=https://pypi.org/simple/
RUN pip3 install --upgrade pip && \
    pip3 install --require-hashes -r requirements.txt --no-deps --disable-pip-version-check && \
    pip3 cache purge

# for testing to work, the base image has to have spark<=3.1, >=3.0
# spark>=3.0 is required by python3.8
# spark <=3.1 is required by pydeequ (deequ)

# add java
COPY --from=adoptopenjdk/openjdk8 opt/java opt/java
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH=$PATH:$JAVA_HOME/bin

# add spark
ADD https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz .
RUN rm -rf /opt/spark && \
    tar -xzf spark-3.2.0-bin-hadoop3.2.tgz -C /opt && \
    mv /opt/spark-3.2.0-bin-hadoop3.2/ /opt/spark
ENV SPARK_HOME="/opt/spark"

# add shaded gcs connector
ADD https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/hadoop3-2.2.2/gcs-connector-hadoop3-2.2.2-shaded.jar /opt/spark/jars/gcs-connector-hadoop3-latest.jar
