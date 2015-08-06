#!/bin/sh
#
# M/MONIT SQLITE TO SQL EXPORT
#


MMONIT_HOME=`dirname ${0}`/..
SQLITE="$MMONIT_HOME/bin/sqlite3"
DBPATH="$MMONIT_HOME/db/mmonit.db"
DBTYPE=""


help() {
       /bin/echo "Usage: $0 -t {mysql|postgresql} [-h]";
       /bin/echo "Options are as follows:";
       /bin/echo "    -t Target database type (mysql or postgresql)";
       /bin/echo "    -h Print this text";
       /bin/echo "Use this script to dump data from a M/Monit SQLite database into a MySQL or a PostgreSQL database.";
       /bin/echo "Examples:";
       /bin/echo "    Export to MySQL: ./upgrade/migrate_db.sh -t mysql | mysql -u mmonit mmonit -p";
       /bin/echo "    Export to PostgreSQL: ./upgrade/migrate_db.sh -t postgresql | psql -U mmonit mmonit 2>&1 | grep ERROR";
       exit 0;
}


error() { 
        /bin/echo "Error: $1"; 
        exit 1; 
}


predump() {
        /bin/echo "DELETE FROM session;";
        /bin/echo "DELETE FROM name;";
        /bin/echo "DELETE FROM messagerecipients;";
        /bin/echo "DELETE FROM message;";
        /bin/echo "DELETE FROM messagequeue;";
        /bin/echo "DELETE FROM messageformat;";
        /bin/echo "DELETE FROM jabberserver;";
        /bin/echo "DELETE FROM mailserver;";
        /bin/echo "DELETE FROM actionrow;";
        /bin/echo "DELETE FROM rulerow;";
        /bin/echo "DELETE FROM rule;";
        /bin/echo "DELETE FROM groupedservices;";
        /bin/echo "DELETE FROM servicegroup;";
        /bin/echo "DELETE FROM service;";
        /bin/echo "DELETE FROM eventnotice;";
        /bin/echo "DELETE FROM event;";
        /bin/echo "DELETE FROM groupedhost;";
        /bin/echo "DELETE FROM hostgroup;";
        /bin/echo "DELETE FROM host;";
        /bin/echo "DELETE FROM userroles;";
        /bin/echo "DELETE FROM roles;";
        /bin/echo "DELETE FROM users;";
        /bin/echo "DELETE FROM mmonit;";
}


dump() {
$SQLITE $DBPATH << ELO
.mode insert users
SELECT * FROM users;
.mode insert roles
SELECT * FROM roles;
.mode insert userroles
SELECT * FROM userroles;
.mode insert name
SELECT * FROM name;
.mode insert host
SELECT * FROM host;
.mode insert hostgroup
SELECT * FROM hostgroup;
.mode insert groupedhost
SELECT * FROM groupedhost;
.mode insert event
SELECT * FROM event;
.mode insert eventnotice
SELECT * FROM eventnotice;
.mode insert service
SELECT * FROM service;
.mode insert servicegroup
SELECT * FROM servicegroup;
.mode insert groupedservices 
SELECT * FROM groupedservices;
.mode insert rule
SELECT * FROM rule;
.mode insert rulerow
SELECT * FROM rulerow;
.mode insert actionrow
SELECT * FROM actionrow;
.mode insert mailserver
SELECT * FROM mailserver;
.mode insert jabberserver
SELECT * FROM jabberserver;
.mode insert messageformat
SELECT * FROM messageformat;
.mode insert messagequeue
SELECT * FROM messagequeue;
.mode insert message
SELECT * FROM message;
.mode insert messagerecipients
SELECT * FROM messagerecipients;
.mode insert session
SELECT * FROM session;
.mode insert mmonit
SELECT * FROM mmonit;
ELO
}


postdump() {
        if test $DBTYPE = "postgresql"
        then
                /bin/echo "SELECT setval('actionrow_id_seq',        (SELECT max(id) + 1      FROM actionrow));";
                /bin/echo "SELECT setval('event_id_seq',            (SELECT max(id) + 1      FROM event));";
                /bin/echo "SELECT setval('groupedhost_groupid_seq', (SELECT max(groupid) + 1 FROM groupedhost));";
                /bin/echo "SELECT setval('host_id_seq',             (SELECT max(id) + 1      FROM host));";
                /bin/echo "SELECT setval('hostgroup_id_seq',        (SELECT max(id) + 1      FROM hostgroup));";
                /bin/echo "SELECT setval('jabberserver_id_seq',     (SELECT max(id) + 1      FROM jabberserver));";
                /bin/echo "SELECT setval('mailserver_id_seq',       (SELECT max(id) + 1      FROM mailserver));";
                /bin/echo "SELECT setval('message_id_seq',          (SELECT max(id) + 1      FROM message));";
                /bin/echo "SELECT setval('messageformat_id_seq',    (SELECT max(id) + 1      FROM messageformat));";
                /bin/echo "SELECT setval('name_id_seq',             (SELECT max(id) + 1      FROM name));";
                /bin/echo "SELECT setval('rule_id_seq',             (SELECT max(id) + 1      FROM rule));";
                /bin/echo "SELECT setval('rulerow_id_seq',          (SELECT max(id) + 1      FROM rulerow));";
                /bin/echo "SELECT setval('service_id_seq',          (SELECT max(id) + 1      FROM service));";
                /bin/echo "SELECT setval('servicegroup_id_seq',     (SELECT max(id) + 1      FROM servicegroup));";
        fi
}


while getopts ":ht:" c
do
case $c in
        t) case $OPTARG in
                mysql | postgresql)
                        DBTYPE=$OPTARG;
                        ;;
                *)
                        /bin/echo "Unknow database type: $OPTARG";
                        exit 1;
                        ;;
           esac;;
        *) help;;
esac
done


if test x$DBTYPE = "x"
then
        /bin/echo "Error: -t option required"
        help
fi


if [ ! -e "$DBPATH" ]
then
        error "SQLite database file '$DBPATH' does not exist";
else 
        predump;
        dump;
        postdump;
fi

exit;

