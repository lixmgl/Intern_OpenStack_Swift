#!/bin/bash

INST_DIR=/opt/collectd
JAR=/usr/bin/jar
JAVAC=/usr/lib/debug/usr/lib/jvm/java-6-openjdk-amd64/bin/javac

export JAR
export JAVAC

echo "Removing previous build..."
if [ -d ${INST_DIR} ]; then 
    rm -rf ${INST_DIR}
fi

mkdir -p ${INST_DIR}/var/lib
mkdir -p ${INST_DIR}/var/run

cd ../collectd-5.1.0

echo "Removing old build artifacts..."
./clean.sh

echo "Building collectd..."
./build.sh
./configure --enable-python --with-java=/usr/lib/jvm/java-6-openjdk-amd64/jre --prefix=${INST_DIR}

echo "Compiling..."
make

echo "Finishing build to directory ${INST_DIR}"
make install 

cp ../build/collectd_rc ${INST_DIR}/bin