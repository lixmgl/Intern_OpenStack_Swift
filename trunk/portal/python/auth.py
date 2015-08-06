# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import web
import sys
import simplejson as json

import util

urls = (
    '/login', 'login',
    '/logout', 'logout',
    '/logininfo', 'logininfo'
)

render_auth = web.template.render('templates', cache=False)

class login:
    def POST(self):
        '''
        Takes form input from the UI and submits the login via a REST post to the API.
        If a token is returned, the function sets a client cookie with the token and tenant ID
        If the login fails, the function returns 401 - Unauthorized.
        '''
        creds = web.input()
        
        params = { "passwordCredentials": { "username": creds.username, "password": creds.password }, "tenantID": util.admin_tenant_id }
        headers = { "Content-type": "application/json", "Accept": "application/json" }
        response = util.APIRequest(host=util.csapi_ip, port=util.csapi_port, path=util.csapi_root+"/identity/token", method="POST", params=params, headers=headers)
        if response:
            token = json.loads(response)['token']
            web.webapi.setcookie('token', token, 86400, util.portal_ip, path=util.portal_root)
            web.webapi.setcookie('tenant_id', util.admin_tenant_id, 86400, util.portal_ip, path=util.portal_root)
        else:
            return web.webapi.Unauthorized()
        
class logininfo:
    def GET(self):
        '''
        A simple function that reads the client cookies and renders a simple HTML template with the data.
        This is used in spadmin.html template in the header bar.
        '''
        token = web.cookies().get('token')
        tenant_id = web.cookies().get('tenant_id')
        return render_auth.logininfo(token, tenant_id)
        
class logout:
    def GET(self):
        '''
        Clears the client cookies and returns the user to the login page.
        '''
        web.setcookie('token', '', -1, util.portal_ip, path=util.portal_root)
        web.setcookie('tenant_id', '', -1, util.portal_ip, path=util.portal_root)
        raise web.seeother(".."+util.portal_root)

app_auth = web.application(urls, locals())