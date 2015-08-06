# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************

import web
import httplib
import re

import simplejson as json
from configParse import Parse

parser = Parse("properties.cfg") 
_endpoint = parser.get_value("AUTH", "auth_service")
_admin_endpoint = parser.get_value("AUTH", "auth_admin")
admin_user_id = parser.get_value("ADMIN", "admin_user_id")
admin_role_id = parser.get_value("ADMIN", "admin_role_id")
object_ip = parser.get_value("OBJECT", "object_ip")
object_port = parser.get_value("OBJECT", "object_port")
object_root = parser.get_value("OBJECT", "object_root")

import identity

urls = (
    "/tenant", "tenant",
    "/tenant/(.*)", "tenant",
    "/token", "tokenWeb",
    "/user", "user",
    "/user/(.*)", "user"
)

class tenant:
    def GET(self, tenant_id=''):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        auth_tenant_name = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_NAME', None)
        
        keystone = identity.auth(token_id=auth_token, tenant_id=auth_tenant_id, tenant_name=auth_tenant_name, url=_endpoint, api="NATIVE", admin=True, admin_url=_admin_endpoint)
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
    
    def DELETE(self, tenant_id=''):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        auth_tenant_name = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_NAME', None)
        
        keystone = identity.auth(token_id=auth_token, tenant_id=auth_tenant_id, tenant_name=auth_tenant_name, url=_endpoint, api="NATIVE", admin=True, admin_url=_admin_endpoint)
        keystone.management_url = _admin_endpoint
        
        if len(tenant_id) > 0:
            identity.delete_tenant(keystone, tenant_id, "NATIVE")
        else:
            return web.badrequest()
        
    def POST(self, tenant_id=''):
        new_tenant = json.loads(web.data())
        
        _headers = {}
        has_meta = False
        fix_header_pre = re.compile('^HTTP_(.*$)')
        fix_header_dash = re.compile('_')
        
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        auth_tenant_name = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_NAME', None)
        
        for key, value in web.ctx.get('environ').items():
            if "META" in key:
                has_meta = True
                _header = fix_header_pre.match(key).group(1)
                _header = fix_header_dash.sub('-', _header)
                _headers[_header.lower()] = value
                     
        keystone = identity.auth(token_id=auth_token, tenant_id=auth_tenant_id, tenant_name=auth_tenant_name, url=_endpoint, api="NATIVE", admin=True, admin_url=_admin_endpoint)
        keystone.management_url = _admin_endpoint
       
        if has_meta:
            id_response = identity.create_tenant(keystone, new_tenant.get('tenant').get('name'), new_tenant.get('tenant').get('description'), "NATIVE")
            new_tenant['id'] = id_response.get('id')
            
            identity.add_tenant_user(keystone, new_tenant.get('id'), admin_user_id, admin_role_id)
            new_token = identity.get_tenant_token(keystone, auth_token, new_tenant.get('id'))
            
            headers = { "X-Auth-Token": new_token.id, "Accept": "application/json" }
            headers.update(_headers)
            conn = httplib.HTTPConnection(object_ip, object_port)
            conn.request("PUT", object_root+"/AUTH_"+new_tenant.get('id'), None, headers)
            response = conn.getresponse()
            conn.close() 
            
            if response.status >= 200 or response.status <= 299:
                return json.dumps(id_response)
            else:
                return response.status
        else:
            if len(tenant_id) <= 0:
                return identity.create_tenant(keystone, new_tenant.get('tenant').get('name'), new_tenant.get('tenant').get('description'), "NATIVE")
            else:
                return identity.update_tenant(keystone, tenant_id, new_tenant.get('tenant').get('name'), new_tenant.get('tenant').get('description'), new_tenant.get('tenant').get('enabled'), "NATIVE")
        
class tokenWeb:
    def POST(self):
        creds = json.loads(web.data())
      
        username = None
        password = None 
        passwd_creds = creds.get('passwordCredentials', None)
        if passwd_creds != None:
            username = creds.get('passwordCredentials').get('username', None)
            password = creds.get('passwordCredentials').get('password', None)
        tenant_id = creds.get('tenantID', None)
        tenant_name = creds.get('tenantName', None)
        token_id = creds.get('tokenID', None)
        
        keystone = identity.auth(usr=username, passwd=password, token_id=token_id, tenant_id=tenant_id, tenant_name=tenant_name, url=_endpoint, api="NATIVE")
        token = identity.get_token(keystone, usr=username, passwd=password, api="NATIVE", tenant_id=tenant_id, tenant_name=tenant_name, token_id=token_id)
        
        if token == -1:
            return web.webUnauthorized()
        
        auth_token = {}
        auth_token['token'] = token.id
        
        body = json.dumps(auth_token)
        web.header("Content-Type", "application/json")
        
        return body
    
class user:
    def GET(self, user_id=''):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        auth_tenant_name = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_NAME', None)
        
        keystone = identity.auth(token_id=auth_token, tenant_id=auth_tenant_id, tenant_name=auth_tenant_name, url=_endpoint, api="NATIVE", admin=True, admin_url=_admin_endpoint)
        keystone.management_url = _admin_endpoint
        
        if len(user_id) <= 0:
            user = identity.list_users(keystone)
        else:
            user = identity.get_user(keystone, user_id)
            
        body = json.dumps(user, indent=4)
        web.header("Content-Type", "application/json")
        
        return body
    
    def POST(self, user_id=''):
        new_user = json.loads(web.data())
        
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        auth_tenant_name = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_NAME', None)
        
        keystone = identity.auth(token_id=auth_token, tenant_id=auth_tenant_id, tenant_name=auth_tenant_name, url=_endpoint, api="NATIVE", admin=True, admin_url=_admin_endpoint)
        keystone.management_url = _admin_endpoint
        
        if len(user_id) <= 0:
            return identity.create_user(keystone, 
                                        new_user.get('user').get('name'), 
                                        new_user.get('user').get('password'), 
                                        new_user.get('user').get('email'), 
                                        new_user.get('user').get('tenant_id'), 
                                        new_user.get('user').get('enabled'), 
                                        "NATIVE")
        else:
            return identity.update_user(keystone, 
                                        user_id, 
                                        new_user.get('user').get('name'), 
                                        new_user.get('user').get('tenant_id'), 
                                        new_user.get('user').get('password'), 
                                        new_user.get('user').get('email'), 
                                        "NATIVE")
            
    def DELETE(self, user_id=''):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        auth_tenant_name = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_NAME', None)
        
        keystone = identity.auth(token_id=auth_token, tenant_id=auth_tenant_id, tenant_name=auth_tenant_name, url=_endpoint, api="NATIVE", admin=True, admin_url=_admin_endpoint)
        keystone.management_url = _admin_endpoint
        
        if len(user_id) > 0:
            identity.delete_user(keystone, user_id, "NATIVE")
        else:
            return web.badrequest() 
        
class tenantUser:
    def GET(self, tenant_id, user_id):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        auth_tenant_name = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_NAME', None)
        
        keystone = identity.auth(token_id=auth_token, tenant_id=auth_tenant_id, tenant_name=auth_tenant_name, url=_endpoint, api="NATIVE", admin=True, admin_url=_admin_endpoint)
        keystone.management_url = _admin_endpoint 
        
        if len(user_id) <= 0:
            user = identity.list_users(tenant_id)
        else:
            user = identity.get_user(user_id)
            
        body = json.dumps(user, indent=4)
        web.header("Content-Type", "application/json")
        
        return body
        
app_identity = web.application(urls, locals())

