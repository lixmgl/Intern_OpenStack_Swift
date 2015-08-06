# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import web
import util
import simplejson as json

urls = (
        '', 'Compute',
        '/', 'Compute',
        '/compute.json', 'computejson',
        '/new', 'computenew',
        '/edit', 'computeedit',
        '/delete', 'computedelete'
)

render_compute = web.template.render('templates', cache=False)

class Compute:
    def GET(self):
        return render_compute.compute()
    
class computejson:
    def GET(self):
        '''
        Gets a list of compute images via the csapi and returns the dojo IFWS formatted JSON.
        '''
        token = web.cookies().get('token')
        tenant_id = web.cookies().get('tenant_id')
        compute_nodes = []
        
        headers = { "Accept": "application/json", "X-Auth-Token": token, "X-Auth-Tenant-ID": tenant_id }
        response = util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/compute/", "GET", None, headers)
        compute_nodes = json.loads(response)
            
        items = {} 
        items['totalCount'] = len(compute_nodes)
        items['identifier'] = "uuid"
        items['items'] = compute_nodes
        
        body = json.dumps(items, indent=4)
        web.header("Content-Type", "application/json")
        
        return body
    
class computenew:
    def GET(self):
        return web.BadRequest()
    
class computeedit:
    def GET(self):
        return web.BadRequest()
    
class computedelete:
    def GET(self):
        return web.BadRequest()
    
app_compute = web.application(urls, locals())