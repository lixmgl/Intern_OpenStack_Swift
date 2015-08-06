#!/bin/bash

INST_DIR=/opt/mmonit

echo "Removing previous build..."
if [ -d ${INST_DIR} ]; then 
    rm -rf ${INST_DIR}
fi

mkdir -p ${INST_DIR}

cp -r ../mmonit-2.4/* ${INST_DIR}
cp mmonit_rc ${INST_DIR}/bin

echo "Finishing build to directory ${INST_DIR}"
