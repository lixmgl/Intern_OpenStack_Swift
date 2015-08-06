# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import web
import util
import simplejson as json

urls = (
        '', 'Project',
        '/', 'Project',
        '/project.json', 'projjson',
        '/edit', 'projedit',
        '/delete', 'projdelete',
        '/new', 'projnew'
)

render_project = web.template.render('templates', cache=False)

class Project:
    def GET(self):
        '''
        Renders the project template.
        '''
        return render_project.project() 
    
class projjson:
    def GET(self):
        '''
        Gets a list of projects via the csapi and returns the dojo IFWS formatted JSON.
        '''
        token = web.cookies().get('token')
        tenant_id = web.cookies().get('tenant_id')
        tenants = []
        
        headers = { "Accept": "application/json", "X-Auth-Token": token, "X-Auth-Tenant-ID": tenant_id }
        response = util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/identity/tenant", "GET", None, headers)
        tenants = json.loads(response)
            
        items = {} 
        items['totalCount'] = len(tenants)
        items['identifier'] = "id"
        items['items'] = tenants
        
        body = json.dumps(items, indent=4)
        web.header("Content-Type", "application/json")
        
        return body

class projedit:
    def POST(self):
        '''
        Uses input from the project table and the csapi to update image data.
        '''
        project = web.input()
        
        token = web.cookies().get('token')
        tenant_id = web.cookies().get('tenant_id')
        
        headers = { "Accept": "application/json", "X-Auth-Token": token, "X-Auth-Tenant-ID": tenant_id }
        params = {"tenant": {"name": project.name, "description": project.description, "enabled": project.enabled}}
        response = util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/identity/tenant/"+project.id, "POST", params, headers)
        if response:
            return web.ok()
        else:
            return web.BadRequest()    
        
class projnew:
    def POST(self):
        '''
        Uses input from the project table and the csapi to create a new project.
        '''
        project = web.input()
        
        token = web.cookies().get('token')
        tenant_id = web.cookies().get('tenant_id')
        
        headers = { "Accept": "application/json", "X-Auth-Token": token, "X-Auth-Tenant-ID": tenant_id }
        params = {"tenant": {"name": project.name, "description": project.description}}
        response = util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/identity/tenant/", "POST", params, headers)
        if response:
            return web.ok()
        else:
            return web.BadRequest()
        
class projdelete:
    def POST(self):
        '''
        Uses input from the project table and the csapi to delete a project.
        '''
        project = web.input()
        
        token = web.cookies().get('token')
        tenant_id = web.cookies().get('tenant_id')
        
        headers = { "X-Auth-Token": token, "X-Auth-Tenant-ID": tenant_id }
        response = util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/identity/tenant/"+project.id, "DELETE", None, headers)
        if response:
            return web.ok()
        else:
            return web.BadRequest()
    
app_project = web.application(urls, locals())