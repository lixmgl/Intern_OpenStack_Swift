#!/bin/sh
PROJECT=swiftstats
VERSION=V1.0

echo "Start installing $PROJECT $VERSION ....."

WORK_DIR=/etc/swiftstats
LOG_DIR=$WORK_DIR/logs

if [ ! -d "$LOG_DIR" ]
then
	mkdir -p $LOG_DIR
fi

cp -f ./etc/*.conf $WORK_DIR

chmod 755 bin/*

echo "Creating auto restart script....."
cp -f ./bin/swiftstatsd /etc/init.d

AUTO_START_LINK="/etc/rc5.d/S99swiftstatsd"
if [ -z "$AUTO_START_LINK" ];then
	rm -f "$AUTO_START_LINK"
fi
ln -s /etc/init.d/swiftstatsd /etc/rc5.d/S99swiftstatsd

python setup.py install > /dev/null 2>&1

echo "Install $PROJECT $VERSION completed successfully!"
