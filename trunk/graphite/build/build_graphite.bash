#!/bin/bash

INST_DIR=/opt/graphite

echo "Removing previous build..."
if [ -d ${INST_DIR} ]; then 
    rm -rf ${INST_DIR}
fi
    
echo "Creating Directory..."    
mkdir ${INST_DIR}

cd ../carbon-0.10.0
python setup.py build
python setup.py install --prefix=/opt/graphite

cd ../graphite-web-0.10.0
python setup.py build
python setup.py install --prefix=/opt/graphite 

#cd ../ceres-0.10.0
#python setup.py build
#python setup.py install --prefix=/opt/graphite

#cd ../whisper-0.9.10
#python setup.py build
#python setup.py install --prefix=/opt/graphite

cp ../build/graphite_rc ${INST_DIR}/bin