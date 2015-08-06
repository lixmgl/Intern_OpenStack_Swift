#!/bin/bash

INST_DIR=/opt/collectd-plugins

echo "Removing previous build..."
if [ -d ${INST_DIR} ]; then 
    rm -rf ${INST_DIR}
fi
    
echo "Creating Directory..."    
mkdir ${INST_DIR}

cd ../collectd-carbon-writer-5.1.0

echo "Copying files..."
cp ./carbon_writer.py ${INST_DIR} 

if [ -d $INST_DIR ]; then 
    echo "Success." 
    exit 0 
else 
    echo "Build failure."
    exit 2 
fi    