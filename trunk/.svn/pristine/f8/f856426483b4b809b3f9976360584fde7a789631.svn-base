#!/bin/bash

PROJECT=swiftstats
VERSION=0.0.1
PACKAGE=${PROJECT}-${VERSION}

EXIT_VAL=0

rm -fr .gitignore .project .pydevproject
find . -name .svn -exec rm -fr {} \; > /dev/null 2>&1
chmod a+x bin/*

python setup.py --command-packages=stdeb.command sdist_dsc
chmod a+rx postinst postrm
cp -fr postinst postrm deb_dist/${PACKAGE}/debian/
cd deb_dist/${PACKAGE}
dpkg-buildpackage -rfakeroot -uc -us

PKG_ROOT="../../../packages"
PKG_PATH="$PKG_ROOT/${PACKAGE}_`date +%m-%d-%y-%H-%M-%S`"
mkdir -p $PKG_PATH

echo "Move packages to $PKG_PATH ......."
mv ../*.deb $PKG_PATH
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