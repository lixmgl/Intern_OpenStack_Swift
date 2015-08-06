#!/bin/sh

if [ $# -ne 4 ];then
    echo "Usage: $0 SEVERITY  CELL_NAME MESSAGE OBJ_CLASS"    
    echo "  SEVERITY = INFO | WARNING | MAJOR | MINOR | CRITICAL"
    exit 0
fi
SEVERITY="$1"  
CELL_NAME="$2" 
MESSAGE="$3" 
OBJ_CLASS="$4"
    
cd /opt/bmc/msend.d/
/opt/bmc/msend.d/msend.pl -n $CELL_NAME -r $SEVERITY -a SNMP_ENTERPRISE -b "mc_object_class='$OBJ_CLASS'" -m "$MESSAGE"

