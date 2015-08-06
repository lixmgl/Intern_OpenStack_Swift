#!/bin/sh

PROJECT=msendclient
VERSION=0.0.1
ARCH=all

find . -name .svn -exec rm -fr {} \;

PACKAGE_NAME=${PROJECT}_${VERSION}-0ubuntu2_${ARCH}.deb

dpkg-deb --build ${PROJECT}

PKG_ROOT="./packages"
PKG_PATH="$PKG_ROOT/${PROJECT}_`date +%m-%d-%y-%H-%M-%S`"
mkdir -p $PKG_PATH

echo "Move packages to $PKG_PATH ......."
mv ${PROJECT}.deb $PKG_PATH/${PACKAGE_NAME}
TMP_VAL=$?
if [ $TMP_VAL -ne 0 ]
then
	echo "No package was generated......"
	exit $TMP_VAL
fi

echo ""
echo ""
echo "==========================================================================="
echo "The follwoing packages were generated successfully:"
echo ""
for pkg in `ls $PKG_PATH/`
do
	echo $pkg
done
echo "==========================================================================="
echo ""
echo ""