#!/bin/sh

# This script performs incremental upgrade of previous m/monit versions (such as schema changes, etc.)


MMONIT_HOME=`dirname ${0}`/..
DBTYPE=""
DBUSER="mmonit"
DBPASSWORD=""
DBNAME="mmonit"
DBSERV="localhost"
DBPORT=""
DBTOOL=""
VERSION_OLD="2.3.4"
MMONIT_OLD="$MMONIT_HOME/../mmonit-$VERSION_OLD"
SCHEMA_VERSION=6


help()
{
       /bin/echo "Usage: $0 [-h] -t {mysql|postgresql|sqlite} [-u dbuser] [-d dbname] [-s dbserver] [-p dbport] [-x path_to_dbutility]";
       /bin/echo " -h Print this text";
       /bin/echo " -t Database type (mysql, postgresql or sqlite)";
       /bin/echo " -u Database user for mysql/postgresql (default: mmonit)";
       /bin/echo " -d Database name for mysql/postgresql (default: mmonit)";
       /bin/echo " -s Database server hostname or IP address for mysql/postgresql (default: localhost)";
       /bin/echo " -p Database server port for mysql/postgresql (default: 3306/mysql, 5432/postgresql)";
       /bin/echo " -x Database utility path (default: '$MMONIT_HOME/bin/sqlite3' for sqlite, 'mysql' for mysql, 'psql' for postgresql)";
       exit 0;
}


getpassword()
{
        /bin/echo -n  "Please enter database password for database user $DBUSER [$DBPASSWORD]: "
        stty -echo
        read DBPASSWORD
        stty echo
}


while getopts "hd:t:u:s:p:x:" c
do
case $c in
        t) case $OPTARG in
                mysql)
                        DBTYPE=$OPTARG;
                        DBPORT=3306;
                        DBTOOL="mysql";
                        ;;
                postgresql)
                        DBTYPE=$OPTARG;
                        DBPORT=5432;
                        DBTOOL="psql";
                        ;;
                sqlite)
                        DBTYPE=$OPTARG;
                        DBTOOL="$MMONIT_HOME/bin/sqlite3";
                        ;;
                *) 
                        /bin/echo "Unknow database type: $OPTARG"; 
                        exit 1;
                        ;;
           esac;;
        d) DBNAME=$OPTARG;;
        u) DBUSER=$OPTARG;;
        s) DBSERV=$OPTARG;;
        p) DBPORT=$OPTARG;;
        x) DBTOOL=$OPTARG;;
        *) help;;
esac
done


if test x$DBTYPE = "x"
then
        /bin/echo "Error: -t option required"
        help
fi


/bin/echo -n  "Please enter the path to mmonit-$VERSION_OLD directory [$MMONIT_OLD]: "
read MMONIT_CUSTOM
if [ "$MMONIT_CUSTOM" != "" ]
then
        MMONIT_OLD=$MMONIT_CUSTOM
fi


# update schema:
/bin/echo "Upgrading database scheme ... "
case $DBTYPE in

mysql)
getpassword
OLD_SCHEMA_VERSION=`$DBTOOL -h $DBSERV -P $DBPORT -u $DBUSER --password=$DBPASSWORD -D $DBNAME -N -s -e "SELECT schemaversion FROM mmonit"`
if [ $OLD_SCHEMA_VERSION -ne $SCHEMA_VERSION ]
then
echo "START TRANSACTION;
ALTER TABLE host ADD COLUMN eventscount INTEGER DEFAULT 0;
ALTER TABLE service ADD COLUMN eventscount INTEGER DEFAULT 0;
UPDATE host SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=host.id);
UPDATE service SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=service.hostid AND event.service_nameid=service.nameid);
UPDATE mmonit SET schemaversion=$SCHEMA_VERSION;
COMMIT;" | $DBTOOL -h $DBSERV -P $DBPORT -u $DBUSER --password=$DBPASSWORD -D $DBNAME
fi
;;

postgresql)
getpassword
OLD_SCHEMA_VERSION=`PGPASSWORD="$DBPASSWORD" $DBTOOL -h $DBSERV -p $DBPORT -U $DBUSER $DBNAME -q -t -c "SELECT schemaversion FROM mmonit"`
if [ $OLD_SCHEMA_VERSION -ne $SCHEMA_VERSION ]
then
echo "BEGIN TRANSACTION;
ALTER TABLE host ADD COLUMN eventscount INTEGER DEFAULT 0;
ALTER TABLE service ADD COLUMN eventscount INTEGER DEFAULT 0;
UPDATE host SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=host.id);
UPDATE service SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=service.hostid AND event.service_nameid=service.nameid);
UPDATE mmonit SET schemaversion=$SCHEMA_VERSION;
COMMIT;" | PGPASSWORD="$DBPASSWORD" $DBTOOL -h $DBSERV -p $DBPORT -U $DBUSER $DBNAME 2>&1 | grep ERROR
fi
;;

sqlite)
cp $MMONIT_OLD/db/mmonit.db $MMONIT_HOME/db/
OLD_SCHEMA_VERSION=`$DBTOOL $MMONIT_HOME/db/mmonit.db "SELECT schemaversion FROM mmonit"`
if [ $OLD_SCHEMA_VERSION -ne $SCHEMA_VERSION ]
then
$DBTOOL $MMONIT_HOME/db/mmonit.db "PRAGMA foreign_keys=OFF; BEGIN TRANSACTION;
ALTER TABLE host ADD COLUMN eventscount INTEGER DEFAULT 0;
ALTER TABLE service ADD COLUMN eventscount INTEGER DEFAULT 0;
UPDATE host SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=host.id);
UPDATE service SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=service.hostid AND event.service_nameid=service.nameid);
UPDATE mmonit SET schemaversion=$SCHEMA_VERSION;
COMMIT;"
fi
;;

esac
/bin/echo done


/bin/echo -n "Copying configuration files from $MMONIT_OLD/conf/ to $MMONIT_HOME/conf/ ... "
cp $MMONIT_OLD/conf/* $MMONIT_HOME/conf/
/bin/echo done

