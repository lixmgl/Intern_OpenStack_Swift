# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************

import sys
import os
import web
import datetime

import simplejson as json

_endpoint = "http://10.100.18.144:5000/v2.0"
_admin_endpoint = "http://10.100.18.144:35357/v2.0"

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

import identity

urls = (
    "/.*", "tokenWeb"
)

class tokenWeb:
    def POST(self):
        creds = json.loads(web.data())
        username = creds.get('passwordCredentials').get('username')
        password = creds.get('passwordCredentials').get('password')
        
        keystone = identity.auth(usr=username, passwd=password, url=_endpoint, api="NATIVE")
        token = identity.get_token(keystone, username, password, "NATIVE")
        
        if token == -1:
            return web.webUnauthorized()
        
        auth_token = {}
        auth_token['token'] = token.id
        
        body = json.dumps(auth_token)
        web.header("Content-Type", "application/json")
        
        return body
    
app_token = web.application(urls, locals())