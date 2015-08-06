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
    "/(.*)", "tenant"
)

class tenant:
    def GET(self, tenant_id):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        
        keystone = identity.auth(token_id=auth_token, tenant_id=auth_tenant_id, url=_endpoint, api="NATIVE", admin=True, admin_url="http://10.100.32.36:35357/v2.0")
        keystone.management_url = _admin_endpoint
        
        if len(tenant_id) <= 0:
            tenant = identity.list_tenants(keystone, "NATIVE")
        else:
            tenant = identity.get_tenant(keystone, tenant_id, "NATIVE")
            
        if tenant is None:
            return web.unauthorized()
       
        body = json.dumps(tenant, indent=4)
        web.header("Content-Type", "application/json")
        return body
    
    def DELETE(self, tenant_id):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        
        keystone = identity.auth(token_id=auth_token, tenant_id=auth_tenant_id, url=_endpoint, api="NATIVE", admin=True, admin_url="http://10.100.32.36:35357/v2.0")
        keystone.management_url = _admin_endpoint
        
        if len(tenant_id) > 0:
            identity.delete_tenant(keystone, tenant_id, "NATIVE")
        else:
            return web.badrequest()
        
app_tenant = web.application(urls, locals())