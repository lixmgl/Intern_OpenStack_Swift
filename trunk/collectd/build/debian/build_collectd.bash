#!/bin/bash

##preq
echo "Installing pre-requisites..."
sudo apt-get -y install flex bison automake make autoconf libtool libgcrypt11-dev pkg-config

##collectd
echo "Cloning collectd..."
git clone git://git.verplant.org/collectd.git

echo "Building collectd"
cd collectd

./build.sh
./configure --enable-python --with-python=/usr/bin/python --prefix=/opt/collectd

echo "Running tests"
make test

echo "Compiling"
make

echo "Installing collectd"
make install 
