#!/bin/bash

INST_DIR=/usr/local

if [ $1 ]; then
    if [ $1 == "post" ]; then
        if [ -d ${INST_DIR}.tmp ]; then 
            rm -rf ${INST_DIR} 
            mv ${INST_DIR}.tmp ${INST_DIR}
            exit 0
        else
            echo '${INST_DIR}.tmp does not exist'
            exit 1
        fi            
    fi
fi

echo "Removing previous build..."
if [ -d ${INST_DIR} ]; then 
    mv ${INST_DIR} ${INST_DIR}.tmp 
fi

cd ../whisper-0.9.10
python setup.py build
python setup.py install
