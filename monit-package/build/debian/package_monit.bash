#!/bin/bash

PACKAGE_DIR=/opt/packages/monit
INST_DIR=/opt/monit
PROJECT=monit
VERSION=5.4
ARCH=amd64

echo "Creating ${PACKAGE_DIR}"
if [ ! -d ${PACKAGE_DIR} ]; then 
    mkdir -p ${PACKAGE_DIR};
fi 

echo "Re-creating project directory ${PROJECT}..."
rm -rf ./${PROJECT}
mkdir -p ./${PROJECT}${INST_DIR}

echo "Copying package directory from build..."
cp -r ${INST_DIR}/* ./${PROJECT}${INST_DIR}

echo "Copying control and post install..."
mkdir -p ./${PROJECT}/DEBIAN
cp ./control ./${PROJECT}/DEBIAN
cp ./postinst ./${PROJECT}/DEBIAN

echo "Creating package..."
dpkg-deb --build ./${PROJECT}

echo "Moving package to ${PACKAGE_DIR}..."
mv ./${PROJECT}.deb ${PACKAGE_DIR}/cisco-${PROJECT}_${VERSION}_${ARCH}.deb

echo "Cleaning up..."
rm -rf ./${PROJECT}

if [ -f ${PACKAGE_DIR}/cisco-${PROJECT}_${VERSION}_${ARCH}.deb ]; then
    echo "Package created."
    exit 0
else
    echo "Package was not created."
    exit 2
fi