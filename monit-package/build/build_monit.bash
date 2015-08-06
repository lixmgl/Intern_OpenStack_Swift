#!/bin/bash

INST_DIR=/opt/monit

echo "Removing previous build..."
if [ -d ${INST_DIR} ]; then
    rm -rf ${INST_DIR}
fi

cd ../monit-5.4

echo "Removing old build artifacts..."
make clean

echo "Building monit..."
#./autogen.sh
#aclocal-1.11
./configure --with-ssl-lib-dir=/lib/x86_64-linux-gnu --prefix=${INST_DIR}

echo "Compiling..."
make

echo "Finishing build to directory ${INST_DIR}"
make install

mkdir ${INST_DIR}/etc

cp ../build/monitrc ${INST_DIR}/etc
cp ../build/monit ${INST_DIR}/etc 
cp ../build/monit_rc ${INST_DIR}/bin