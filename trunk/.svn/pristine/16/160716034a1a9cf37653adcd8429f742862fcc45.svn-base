#!/bin/bash

INST_DIR=/opt/csapi

echo "Removing previous build..."
if [ -d ${INST_DIR} ]; then 
    rm -rf ${INST_DIR}
fi
    
echo "Creating Directory..."    
mkdir ${INST_DIR}

echo "Copying files..."
cp -r ../csapi-12.05/* ${INST_DIR} 

if [ -d $INST_DIR ]; then 
    echo "Success." 
    exit 0 
else 
    echo "Build failure."
    exit 2 
fi