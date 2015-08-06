#!/bin/bash

# VARS
PROJECT="portal"
REPO="http://jabber-svn.cisco.com/svn/projects/cloud incubation/trunk"
DEST_IP="10.100.18.140"
DEST_DIR="/opt/dashboard"
DEST_USR="www-data"
DEST_GRP="www-data"

# STANDARD DEPLOY
svn co "$REPO/$PROJECT"
tar cf - $PROJECT/ | ssh $DEST_IP "cd $DEST_DIR;sudo tar xf -"
ssh $DEST_IP "sudo chown -R $DEST_USR:$DEST_GRP $DEST_DIR"

# EXTRAS
ssh $DEST_IP "sudo service apache2 restart"