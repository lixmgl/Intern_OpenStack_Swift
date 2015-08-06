# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************

import sys
import os
import web
import datetime

import simplejson as json

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

import objectstore

urls = (
    "", "objectstoreWeb",
    "/", "objectstoreWeb",
    "/container/(.*)/object/(.*)", "object",
    "/container/(.*)/object", "object",
    "/container/", "container",
    "/container/(.*)", "container"
)

class objectstoreWeb:
    def GET(self):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
               
        return json.dumps(objectstore.swift_get_containers(auth_token))

class object:
    def GET(self, container_id, object_id):
        return None
    
class container:
    def GET(self, container_id):
        return None
    
app_objectstore = web.application(urls, locals())