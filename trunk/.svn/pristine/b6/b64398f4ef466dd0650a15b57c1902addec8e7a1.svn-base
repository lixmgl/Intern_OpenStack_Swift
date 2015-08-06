#!/bin/sh

# This script performs incremental upgrade of previous m/monit versions (such as schema changes, etc.)


MMONIT_HOME=`dirname ${0}`/..
DBTYPE=""
DBUSER="mmonit"
DBNAME="mmonit"
DBSERV="localhost"
DBPORT=""
DBTOOL=""
VERSION_OLD="2.2.1"
MMONIT_OLD="$MMONIT_HOME/../mmonit-$VERSION_OLD"


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
/bin/echo -n "Upgrading database scheme ... "
case $DBTYPE in

mysql)
echo "START TRANSACTION;
ALTER TABLE jabberserver ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE mmonit ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE host ADD COLUMN platformswap INTEGER DEFAULT 0;
ALTER TABLE host ADD COLUMN swap REAL DEFAULT 0;
CREATE TABLE name (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  INDEX name_index (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
INSERT INTO name (name) SELECT hostname FROM host;
INSERT INTO name (name) SELECT name FROM hostgroup WHERE name NOT IN (SELECT name FROM name);
INSERT INTO name (name) SELECT name FROM service WHERE name NOT IN (SELECT name FROM name);
INSERT INTO name (name) SELECT name FROM servicegroup WHERE name NOT IN (SELECT name FROM name);
ALTER TABLE host ADD COLUMN nameid INTEGER NOT NULL;
UPDATE host SET nameid=(SELECT name.id FROM name WHERE hostname=name.name);
ALTER TABLE host DROP COLUMN hostname;
ALTER TABLE host ADD FOREIGN KEY nameid_fk (nameid) REFERENCES name (id) ON DELETE CASCADE;
ALTER TABLE hostgroup ADD COLUMN nameid INTEGER NOT NULL;
UPDATE hostgroup SET nameid=(SELECT name.id FROM name WHERE hostgroup.name=name.name);
ALTER TABLE hostgroup DROP COLUMN name;
ALTER TABLE hostgroup ADD FOREIGN KEY nameid_fk (nameid) REFERENCES name (id) ON DELETE CASCADE;
DELETE FROM rulerow WHERE servicegroupid=(SELECT id FROM servicegroup WHERE name='All');
DELETE FROM servicegroup WHERE name='All';
UPDATE event SET serviceid=(SELECT name.id FROM service, name WHERE service.id=event.serviceid AND service.name=name.name);
UPDATE rulerow SET serviceid=(SELECT name.id FROM service, name WHERE service.id=rulerow.serviceid AND service.name=name.name) WHERE serviceid != -1;
UPDATE rulerow SET servicegroupid=(SELECT name.id FROM servicegroup, name WHERE servicegroup.id=rulerow.servicegroupid AND servicegroup.name=name.name) WHERE servicegroupid != -1;
ALTER TABLE event MODIFY COLUMN message TEXT NOT NULL;
ALTER TABLE event DROP INDEX serviceid_index;
ALTER TABLE event CHANGE COLUMN serviceid service_nameid INTEGER NOT NULL;
ALTER TABLE event ADD INDEX service_nameid_index (service_nameid);
ALTER TABLE event ADD FOREIGN KEY service_nameid_fk (service_nameid) REFERENCES name (id) ON DELETE CASCADE;
ALTER TABLE event DROP INDEX collected_sec_index;
ALTER TABLE event CHANGE COLUMN collected_sec collectedsec INTEGER NOT NULL;
ALTER TABLE event CHANGE COLUMN collected_usec collectedusec INTEGER NOT NULL;
ALTER TABLE event ADD INDEX collectedsec_index (collectedsec);
ALTER TABLE rulerow CHANGE COLUMN serviceid service_nameid INTEGER DEFAULT -1;
ALTER TABLE rulerow CHANGE COLUMN servicegroupid servicegroup_nameid INTEGER DEFAULT -1;
DROP TABLE groupedservice;
DROP TABLE service;
DROP TABLE servicegroup;
CREATE TABLE service (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  nameid INTEGER NOT NULL,
  hostid INTEGER NOT NULL,
  type INTEGER NOT NULL,
  status INTEGER NOT NULL,
  monitoringstate INTEGER NOT NULL,
  monitoringmode INTEGER NOT NULL,
  statusmodified INTEGER DEFAULT 0,
  eventscount INTEGER DEFAULT 0,
  FOREIGN KEY nameid_fk (nameid) REFERENCES name (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE servicegroup (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  nameid INTEGER NOT NULL,
  hostid INTEGER NOT NULL,
  FOREIGN KEY nameid_fk (nameid) REFERENCES name (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE groupedservices (
  servicegroupid INTEGER NOT NULL,
  service_nameid INTEGER NOT NULL,
  PRIMARY KEY(servicegroupid, service_nameid),
  FOREIGN KEY servicegroupid_fk (servicegroupid) REFERENCES servicegroup (id) ON DELETE CASCADE,
  FOREIGN KEY service_nameid_fk (service_nameid) REFERENCES name (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE mmonit CHANGE schema_version schemaversion INTEGER NOT NULL;
UPDATE mmonit SET schemaversion=6;
/* Column rename */
ALTER TABLE messageformat CHANGE messagefrom sender VARCHAR(255);
ALTER TABLE message CHANGE messagetype type INTEGER;
ALTER TABLE message CHANGE messagefrom sender VARCHAR(255);
ALTER TABLE message CHANGE messagesubject subject VARCHAR(255);
ALTER TABLE message CHANGE messagebody body TEXT;
ALTER TABLE messagerecipients CHANGE messageto recipient VARCHAR(255) NOT NULL;
ALTER TABLE host CHANGE COLUMN ipaddr_in ipaddrin VARCHAR(255) NOT NULL;
ALTER TABLE host CHANGE COLUMN ipaddr_out ipaddrout VARCHAR(255);
ALTER TABLE host CHANGE COLUMN port_in portin INTEGER;
ALTER TABLE host CHANGE COLUMN port_out portout INTEGER DEFAULT -1;
ALTER TABLE host CHANGE COLUMN statusModified statusmodified INTEGER;
ALTER TABLE host CHANGE COLUMN serviceModified servicemodified INTEGER DEFAULT 0;
ALTER TABLE host CHANGE COLUMN serviceSkew serviceskew INTEGER DEFAULT 3;
ALTER TABLE host CHANGE COLUMN serviceUp serviceup INTEGER DEFAULT 0;
ALTER TABLE host CHANGE COLUMN serviceDown servicedown INTEGER DEFAULT 0;
ALTER TABLE host CHANGE COLUMN serviceUnmonitorAuto serviceunmonitorauto INTEGER;
ALTER TABLE host CHANGE COLUMN serviceUnmonitorManual serviceunmonitormanual INTEGER;
ALTER TABLE host CHANGE COLUMN cpuUser cpuuser REAL DEFAULT 0;
ALTER TABLE host CHANGE COLUMN cpuSystem cpusystem REAL DEFAULT 0;
ALTER TABLE host CHANGE COLUMN cpuWait cpuwait REAL DEFAULT 0;
ALTER TABLE host CHANGE COLUMN cpuTotal cputotal REAL DEFAULT 0;
ALTER TABLE host CHANGE COLUMN statusHeartbeat statusheartbeat INTEGER DEFAULT 1;
ALTER TABLE host ADD COLUMN eventscount INTEGER DEFAULT 0;
UPDATE host SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=host.id);
UPDATE service SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=service.hostid AND event.service_nameid=service.nameid);
COMMIT;" | $DBTOOL -h $DBSERV -P $DBPORT -u $DBUSER -p -D $DBNAME
;;

postgresql)
echo "BEGIN TRANSACTION;
ALTER TABLE host ADD COLUMN platformswap INTEGER DEFAULT 0;
ALTER TABLE host ADD COLUMN swap REAL DEFAULT 0;
CREATE TABLE name (
  id SERIAL PRIMARY KEY,
  name CHARACTER VARYING(255) NOT NULL,
  CONSTRAINT name_name_unique UNIQUE (name)
);
CREATE INDEX name_index ON name (name);
INSERT INTO name (name) SELECT hostname FROM host;
INSERT INTO name (name) SELECT name FROM hostgroup WHERE name NOT IN (SELECT name FROM name);
INSERT INTO name (name) SELECT name FROM service WHERE name NOT IN (SELECT name FROM name);
INSERT INTO name (name) SELECT name FROM servicegroup WHERE name NOT IN (SELECT name FROM name);
ALTER TABLE host ADD COLUMN nameid INTEGER;
UPDATE host SET nameid=(SELECT name.id FROM name WHERE hostname=name.name);
ALTER TABLE host ALTER COLUMN nameid SET NOT NULL;
ALTER TABLE host DROP COLUMN hostname;
ALTER TABLE host ADD CONSTRAINT nameid_fk FOREIGN KEY(nameid) REFERENCES name(id) MATCH FULL ON DELETE CASCADE;
ALTER TABLE hostgroup ADD COLUMN nameid INTEGER;
UPDATE hostgroup SET nameid=(SELECT name.id FROM name WHERE hostgroup.name=name.name);
ALTER TABLE hostgroup ALTER COLUMN nameid SET NOT NULL;
ALTER TABLE hostgroup DROP COLUMN name;
ALTER TABLE hostgroup ADD CONSTRAINT nameid_fk FOREIGN KEY(nameid) REFERENCES name(id) MATCH FULL ON DELETE CASCADE;
ALTER TABLE hostgroup ADD CONSTRAINT hostgroup_nameid_unique UNIQUE (nameid);
DELETE FROM rulerow WHERE servicegroupid=(SELECT id FROM servicegroup WHERE name='All');
DELETE FROM servicegroup WHERE name='All';
ALTER TABLE event ALTER COLUMN message TYPE TEXT;
UPDATE event SET serviceid=(SELECT name.id FROM service, name WHERE service.id=event.serviceid AND service.name=name.name);
UPDATE rulerow SET serviceid=(SELECT name.id FROM service, name WHERE service.id=rulerow.serviceid AND service.name=name.name) WHERE serviceid != -1;
UPDATE rulerow SET servicegroupid=(SELECT name.id FROM servicegroup, name WHERE servicegroup.id=rulerow.servicegroupid AND servicegroup.name=name.name) WHERE servicegroupid != -1;
DROP INDEX collected_sec_index;
ALTER TABLE event RENAME COLUMN collected_sec TO collectedsec;
ALTER TABLE event RENAME COLUMN collected_usec TO collectedusec;
CREATE INDEX collectedsec_index ON event(collectedsec);
DROP INDEX serviceid_index;
ALTER TABLE event RENAME COLUMN serviceid TO service_nameid;
CREATE INDEX service_nameid_index ON event(service_nameid);
ALTER TABLE event ADD CONSTRAINT service_nameid_fk FOREIGN KEY (service_nameid) REFERENCES name (id) MATCH FULL ON DELETE CASCADE;
ALTER TABLE rulerow RENAME COLUMN serviceid TO service_nameid;
ALTER TABLE rulerow RENAME COLUMN servicegroupid TO servicegroup_nameid;
DROP TABLE groupedservice;
DROP TABLE service;
DROP TABLE servicegroup;
CREATE TABLE service (
  id SERIAL PRIMARY KEY,
  nameid INTEGER NOT NULL,
  hostid INTEGER NOT NULL,
  type INTEGER NOT NULL,
  status INTEGER NOT NULL,
  monitoringstate INTEGER NOT NULL,
  monitoringmode INTEGER NOT NULL,
  statusmodified INTEGER DEFAULT 0,
  eventscount INTEGER DEFAULT 0,
  CONSTRAINT nameid_fk FOREIGN KEY (nameid) REFERENCES name (id) MATCH FULL ON DELETE CASCADE
);
CREATE TABLE servicegroup (
  id SERIAL PRIMARY KEY,
  nameid INTEGER NOT NULL,
  hostid INTEGER NOT NULL,
  CONSTRAINT nameid_fk FOREIGN KEY (nameid) REFERENCES name (id) MATCH FULL ON DELETE CASCADE
);
CREATE TABLE groupedservices (
  servicegroupid INTEGER NOT NULL,
  service_nameid INTEGER NOT NULL,
  PRIMARY KEY(servicegroupid, service_nameid),
  CONSTRAINT servicegroupid_fk FOREIGN KEY (servicegroupid) REFERENCES servicegroup (id) MATCH FULL ON DELETE CASCADE,
  CONSTRAINT service_nameid_fk FOREIGN KEY (service_nameid) REFERENCES name (id) MATCH FULL ON DELETE CASCADE
);
ALTER TABLE mmonit RENAME schema_version TO schemaversion;
UPDATE mmonit SET schemaversion=6;
/* Column rename */
ALTER TABLE messageformat RENAME COLUMN messagefrom TO sender;
ALTER TABLE message RENAME COLUMN messagetype TO type;
ALTER TABLE message RENAME COLUMN messagefrom TO sender;
ALTER TABLE message RENAME COLUMN messagesubject TO subject;
ALTER TABLE message RENAME COLUMN messagebody TO body;
ALTER TABLE messagerecipients RENAME COLUMN messageto TO recipient;
ALTER TABLE host RENAME COLUMN ipaddr_in TO ipaddrin;
ALTER TABLE host RENAME COLUMN ipaddr_out TO ipaddrout;
ALTER TABLE host RENAME COLUMN port_in TO portin;
ALTER TABLE host RENAME COLUMN port_out TO portout;
ALTER TABLE host ADD COLUMN eventscount INTEGER DEFAULT 0;
UPDATE host SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=host.id);
UPDATE service SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=service.hostid AND event.service_nameid=service.nameid);
COMMIT;" | $DBTOOL -h $DBSERV -p $DBPORT -U $DBUSER $DBNAME 2>&1 | grep ERROR
;;

sqlite)
cp $MMONIT_OLD/db/mmonit.db $MMONIT_HOME/db/
$DBTOOL $MMONIT_HOME/db/mmonit.db "PRAGMA foreign_keys=OFF; BEGIN TRANSACTION;
DROP TRIGGER f_userroles1;
DROP TRIGGER f_userroles2;
DROP TRIGGER f_userroles3;
DROP TRIGGER f_userroles4;
DROP TRIGGER f_groupedhost1;
DROP TRIGGER f_groupedhost2;
DROP TRIGGER f_event1;
DROP TRIGGER f_eventnotice1;
DROP TRIGGER f_eventnotice2;
DROP TRIGGER f_groupedservice1;
DROP TRIGGER f_groupedservice2;
DROP TRIGGER f_rulerow1;
DROP TRIGGER f_actionrow1;
DROP TRIGGER f_messagerecipients;
DROP TRIGGER d_users1;
DROP TRIGGER d_roles1;
DROP TRIGGER d_hostgroup1;
DROP TRIGGER d_service1;
DROP TRIGGER d_servicegroup1;
DROP TRIGGER d_rule1;
DROP TRIGGER d_message;
DELETE FROM groupedhost WHERE hostid NOT IN (SELECT id FROM host);
DELETE FROM event WHERE hostid NOT IN (SELECT id FROM host);
CREATE TABLE name (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL
);
CREATE INDEX name_index ON name(name);
INSERT INTO name (name) SELECT hostname FROM host;
INSERT INTO name (name) SELECT name FROM hostgroup WHERE name NOT IN (SELECT name FROM name);
INSERT INTO name (name) SELECT name FROM service WHERE name NOT IN (SELECT name FROM name);
INSERT INTO name (name) SELECT name FROM servicegroup WHERE name NOT IN (SELECT name FROM name);
CREATE TEMPORARY TABLE host_backup (
  id INTEGER PRIMARY KEY,
  status CHAR(1) NOT NULL,
  nameid INTEGER NOT NULL,
  monitid VARCHAR(255) UNIQUE NOT NULL,
  ipaddrin VARCHAR(255) NOT NULL,
  ipaddrout VARCHAR(255),
  portin INTEGER,
  portout INTEGER DEFAULT -1,
  uname VARCHAR(255),
  password VARCHAR(255),
  usessl CHAR(1),
  description TEXT,
  poll INTEGER DEFAULT 0,
  statusmodified INTEGER,
  servicemodified INTEGER DEFAULT 0,
  serviceskew INTEGER DEFAULT 3,
  serviceup INTEGER DEFAULT 0,
  servicedown INTEGER DEFAULT 0,
  serviceunmonitorauto INTEGER,
  serviceunmonitormanual INTEGER,
  version VARCHAR(20),
  platformname VARCHAR(255),
  platformrelease VARCHAR(255),
  platformversion VARCHAR(255),
  platformmachine VARCHAR(255),
  platformcpu INTEGER DEFAULT 0,
  platformmemory INTEGER DEFAULT 0,
  platformswap INTEGER DEFAULT 0,
  cpuuser REAL DEFAULT 0,
  cpusystem REAL DEFAULT 0,
  cpuwait REAL DEFAULT 0,
  cputotal REAL DEFAULT 0,
  memory REAL DEFAULT 0,
  swap REAL DEFAULT 0,
  statusheartbeat INTEGER DEFAULT 1,
  eventscount INTEGER DEFAULT 0
);
INSERT INTO host_backup SELECT id, status, (SELECT name.id FROM name WHERE host.hostname=name.name), monitid, ipaddr_in, ipaddr_out, port_in, port_out, uname, password, usessl, description, poll, statusModified, serviceModified, serviceSkew, serviceUp, serviceDown, serviceUnmonitorAuto, serviceUnmonitorManual, version, platformname, platformrelease, platformversion, platformmachine, platformcpu, platformmemory, 0, cpuUser, cpuSystem, cpuWait, cpuTotal, memory, 0, statusheartbeat, 0 FROM host;
DROP TABLE host;
CREATE TABLE host (
  id INTEGER PRIMARY KEY,
  status CHAR(1) NOT NULL,
  nameid INTEGER NOT NULL,
  monitid VARCHAR(255) UNIQUE NOT NULL,
  ipaddrin VARCHAR(255) NOT NULL,
  ipaddrout VARCHAR(255),
  portin INTEGER,
  portout INTEGER DEFAULT -1,
  uname VARCHAR(255),
  password VARCHAR(255),
  usessl CHAR(1),
  description TEXT,
  poll INTEGER DEFAULT 0,
  statusmodified INTEGER,
  servicemodified INTEGER DEFAULT 0,
  serviceskew INTEGER DEFAULT 3,
  serviceup INTEGER DEFAULT 0,
  servicedown INTEGER DEFAULT 0,
  serviceunmonitorauto INTEGER,
  serviceunmonitormanual INTEGER,
  version VARCHAR(20),
  platformname VARCHAR(255),
  platformrelease VARCHAR(255),
  platformversion VARCHAR(255),
  platformmachine VARCHAR(255),
  platformcpu INTEGER DEFAULT 0,
  platformmemory INTEGER DEFAULT 0,
  platformswap INTEGER DEFAULT 0,
  cpuuser REAL DEFAULT 0,
  cpusystem REAL DEFAULT 0,
  cpuwait REAL DEFAULT 0,
  cputotal REAL DEFAULT 0,
  memory REAL DEFAULT 0,
  swap REAL DEFAULT 0,
  statusheartbeat INTEGER DEFAULT 1,
  eventscount INTEGER DEFAULT 0,
  FOREIGN KEY(nameid) REFERENCES name(id) ON DELETE CASCADE
);
INSERT INTO host SELECT * FROM host_backup;
DROP TABLE host_backup;
CREATE TEMPORARY TABLE hostgroup_backup (
  id INTEGER PRIMARY KEY,
  nameid INTEGER UNIQUE NOT NULL,
  description TEXT
);
INSERT INTO hostgroup_backup SELECT id, (SELECT name.id FROM name WHERE hostgroup.name=name.name), description FROM hostgroup;
DROP TABLE hostgroup;
CREATE TABLE hostgroup (
  id INTEGER PRIMARY KEY,
  nameid INTEGER UNIQUE NOT NULL,
  description TEXT,
  FOREIGN KEY(nameid) REFERENCES name(id) ON DELETE CASCADE
);
INSERT INTO hostgroup SELECT * FROM hostgroup_backup;
DROP TABLE hostgroup_backup;
CREATE TEMPORARY TABLE userroles_backup (
  uname VARCHAR(20) NOT NULL,
  role VARCHAR(20)  NOT NULL
);
INSERT INTO userroles_backup SELECT uname, role FROM userroles;
DROP TABLE userroles;
CREATE TABLE userroles (
  uname VARCHAR(20) NOT NULL,
  role VARCHAR(20)  NOT NULL,
  PRIMARY KEY(uname, role),
  FOREIGN KEY(role) REFERENCES roles(role) ON DELETE CASCADE,
  FOREIGN KEY(uname) REFERENCES users(uname) ON DELETE CASCADE
);
INSERT INTO userroles SELECT * FROM userroles_backup;
DROP TABLE userroles_backup;
CREATE TEMPORARY TABLE groupedhost_backup (
  groupid INTEGER NOT NULL,
  hostid  INTEGER NOT NULL
);
INSERT INTO groupedhost_backup SELECT groupid, hostid FROM groupedhost;
DROP TABLE groupedhost;
CREATE TABLE groupedhost (
  groupid INTEGER NOT NULL,
  hostid  INTEGER NOT NULL,
  PRIMARY KEY(groupid, hostid),
  FOREIGN KEY(groupid) REFERENCES hostgroup(id) ON DELETE CASCADE,
  FOREIGN KEY(hostid) REFERENCES host(id) ON DELETE CASCADE
);
INSERT INTO groupedhost SELECT * FROM groupedhost_backup;
DROP TABLE groupedhost_backup;
DELETE FROM rulerow WHERE servicegroupid=(SELECT id FROM servicegroup WHERE name='All');
DELETE FROM servicegroup WHERE name='All';
UPDATE event SET serviceid=(SELECT name.id FROM service, name WHERE service.id=event.serviceid AND service.name=name.name);
UPDATE rulerow SET serviceid=(SELECT name.id FROM service, name WHERE service.id=rulerow.serviceid AND service.name=name.name) WHERE serviceid != -1;
UPDATE rulerow SET servicegroupid=(SELECT name.id FROM servicegroup, name WHERE servicegroup.id=rulerow.servicegroupid AND servicegroup.name=name.name) WHERE servicegroupid != -1;
DROP TABLE service;
DROP TABLE servicegroup;
CREATE TABLE service (
  id INTEGER PRIMARY KEY,
  nameid INTEGER NOT NULL,
  hostid INTEGER NOT NULL,
  type INTEGER NOT NULL,
  status INTEGER NOT NULL,
  monitoringstate INTEGER NOT NULL,
  monitoringmode INTEGER NOT NULL,
  statusmodified INTEGER DEFAULT 0,
  eventscount INTEGER DEFAULT 0,
  FOREIGN KEY(nameid) REFERENCES name(id) ON DELETE CASCADE
);
CREATE TABLE servicegroup (
  id INTEGER PRIMARY KEY,
  nameid INTEGER NOT NULL,
  hostid INTEGER NOT NULL,
  FOREIGN KEY(nameid) REFERENCES name(id) ON DELETE CASCADE
);
DROP TABLE groupedservice;
CREATE TABLE groupedservices (
  servicegroupid INTEGER NOT NULL,
  service_nameid INTEGER NOT NULL,
  PRIMARY KEY(servicegroupid, service_nameid),
  FOREIGN KEY(servicegroupid) REFERENCES servicegroup(id) ON DELETE CASCADE,
  FOREIGN KEY(service_nameid) REFERENCES name(id) ON DELETE CASCADE
);
CREATE TEMPORARY TABLE event_backup (
  id INTEGER PRIMARY KEY,
  hostid INTEGER NOT NULL,
  collectedsec INTEGER NOT NULL,
  collectedusec INTEGER NOT NULL,
  service_nameid INTEGER NOT NULL,
  servicetype INTEGER NOT NULL,
  event INTEGER NOT NULL,
  state INTEGER NOT NULL,
  action INTEGER NOT NULL,
  message TEXT NOT NULL,
  hasnotice INTEGER
);
INSERT INTO event_backup SELECT id, hostid, collected_sec, collected_usec, serviceid, servicetype, event, state, action, message, hasnotice FROM event;
DROP TABLE event;
CREATE TABLE event (
  id INTEGER PRIMARY KEY,
  hostid INTEGER NOT NULL,
  collectedsec INTEGER NOT NULL,
  collectedusec INTEGER NOT NULL,
  service_nameid INTEGER NOT NULL,
  servicetype INTEGER NOT NULL,
  event INTEGER NOT NULL,
  state INTEGER NOT NULL,
  action INTEGER NOT NULL,
  message TEXT NOT NULL,
  hasnotice INTEGER,
  FOREIGN KEY(hostid) REFERENCES host(id) ON DELETE CASCADE,
  FOREIGN KEY(service_nameid) REFERENCES name(id) ON DELETE CASCADE
);
INSERT INTO event SELECT * FROM event_backup;
DROP TABLE event_backup;
CREATE INDEX hostid_index ON event(hostid);
CREATE INDEX collectedsec_index ON event(collectedsec);
CREATE INDEX service_nameid_index ON event(service_nameid);
CREATE INDEX servicetype_index ON event(servicetype);
CREATE INDEX state_index ON event(state);
CREATE TEMPORARY TABLE eventnotice_backup (
  eventid INTEGER NOT NULL,
  date INTEGER NOT NULL,
  uname VARCHAR(20) NOT NULL,
  notice TEXT NOT NULL
);
INSERT INTO eventnotice_backup SELECT eventid, date, uname, notice FROM eventnotice;
DROP TABLE eventnotice;
CREATE TABLE eventnotice (
  eventid INTEGER NOT NULL,
  date INTEGER NOT NULL,
  uname VARCHAR(20) NOT NULL,
  notice TEXT NOT NULL,
  FOREIGN KEY(eventid) REFERENCES event(id) ON DELETE CASCADE,
  FOREIGN KEY(uname) REFERENCES users(uname) ON DELETE CASCADE
);
INSERT INTO eventnotice SELECT * FROM eventnotice_backup;
DROP TABLE eventnotice_backup;
CREATE INDEX eventid_index ON eventnotice(eventid);
CREATE TEMPORARY TABLE rulerow_backup (
  id INTEGER PRIMARY KEY,
  ruleid INTEGER NOT NULL,
  hostid INTEGER DEFAULT -1,
  hostgroupid INTEGER DEFAULT -1,
  service_nameid INTEGER DEFAULT -1,
  servicegroup_nameid INTEGER DEFAULT -1,
  eventstate INTEGER DEFAULT -1
);
INSERT INTO rulerow_backup SELECT id, ruleid, hostid, hostgroupid, serviceid, servicegroupid, eventstate FROM rulerow;
DROP TABLE rulerow;
CREATE TABLE rulerow (
  id INTEGER PRIMARY KEY,
  ruleid INTEGER NOT NULL,
  hostid INTEGER DEFAULT -1,
  hostgroupid INTEGER DEFAULT -1,
  service_nameid INTEGER DEFAULT -1,
  servicegroup_nameid INTEGER DEFAULT -1,
  eventstate INTEGER DEFAULT -1,
  FOREIGN KEY(ruleid) REFERENCES rule(id) ON DELETE CASCADE
);
INSERT INTO rulerow SELECT * FROM rulerow_backup;
DROP TABLE rulerow_backup;
CREATE TEMPORARY TABLE actionrow_backup (
  id INTEGER PRIMARY KEY,
  ruleid INTEGER NOT NULL,
  selectedtarget INTEGER NOT NULL,
  target TEXT NOT NULL,
  targetoption TEXT
);
INSERT INTO actionrow_backup SELECT id, ruleid, selectedtarget, target, targetoption FROM actionrow;
DROP TABLE actionrow;
CREATE TABLE actionrow (
  id INTEGER PRIMARY KEY,
  ruleid INTEGER NOT NULL,
  selectedtarget INTEGER NOT NULL,
  target TEXT NOT NULL,
  targetoption TEXT,
  FOREIGN KEY(ruleid) REFERENCES rule(id) ON DELETE CASCADE
);
INSERT INTO actionrow SELECT * FROM actionrow_backup;
DROP TABLE actionrow_backup;
ALTER TABLE messageformat RENAME TO tmp_messageformat;
CREATE TABLE messageformat (
  id INTEGER PRIMARY KEY,
  description VARCHAR(255),
  sender VARCHAR(255),
  subject VARCHAR(255), 
  message TEXT, 
  isdefault CHAR(1)
);
INSERT INTO messageformat SELECT * FROM tmp_messageformat;
DROP TABLE tmp_messageformat;
ALTER TABLE message RENAME TO tmp_message;
CREATE TABLE message (
  id INTEGER PRIMARY KEY,
  type INTEGER, 
  sender VARCHAR(255),
  subject VARCHAR(255),
  body TEXT,
  created INTEGER,
  retry INTEGER
);
INSERT INTO message SELECT * FROM tmp_message;
DROP TABLE tmp_message;
CREATE TEMPORARY TABLE messagerecipients_backup (
  messageid INTEGER NOT NULL,
  recipient VARCHAR(255) NOT NULL
);
INSERT INTO messagerecipients_backup SELECT messageid, messageto FROM messagerecipients;
DROP TABLE messagerecipients;
CREATE TABLE messagerecipients (
  messageid INTEGER NOT NULL,
  recipient VARCHAR(255) NOT NULL,
  FOREIGN KEY(messageid) REFERENCES message(id) ON DELETE CASCADE
);
INSERT INTO messagerecipients SELECT * FROM messagerecipients_backup;
DROP TABLE messagerecipients_backup;
DROP TABLE mmonit;
CREATE TABLE mmonit (
  schemaversion INTEGER NOT NULL
);
INSERT INTO mmonit (schemaversion) VALUES (6);
UPDATE host SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=host.id);
UPDATE service SET eventscount=(SELECT COUNT(*) FROM event WHERE event.hostid=service.hostid AND event.service_nameid=service.nameid);
COMMIT;"
;;

esac
/bin/echo done


/bin/echo -n "Copying configuration files from $MMONIT_OLD/conf/ to $MMONIT_HOME/conf/ ... "
cp $MMONIT_OLD/conf/* $MMONIT_HOME/conf/
/bin/echo done


/bin/echo -n "Updating configuration file $MMONIT_HOME/conf/server.xml to enable sqlite foreign keys ... "
perl -p -i -e "s/sqlite:\/\/\/db\/mmonit.db\?synchronous=normal&cache_size=10000/sqlite:\/\/\/db\/mmonit.db\?synchronous=normal&heap_limit=8000&foreign_keys=on/g" $MMONIT_HOME/conf/server.xml
/bin/echo done


