# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import web
import util
import simplejson as json

urls = (
        '', 'Image',
        '/', 'Image',
        '/images.json', 'imagejson',
        '/edit', 'imageedit',
        '/new', 'imagenew',
        '/delete', 'imagedelete'
)

render_image = web.template.render('templates', cache=False)

class Image:
    def GET(self):
        '''
        Renders the image template.
        '''
        return render_image.image() 
    
class imagejson:
    def GET(self):
        '''
        Gets a list of images via the csapi and returns the dojo IFWS formatted JSON.
        '''
        token = web.cookies().get('token')
        tenant_id = web.cookies().get('tenant_id')
        images = []
        
        headers = { "Accept": "application/json", "X-Auth-Token": token, "X-Auth-Tenant-ID": tenant_id }
        response = util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/image/v1/images/detail", "GET", None, headers)
        images = json.loads(response)
            
        items = {} 
        items['totalCount'] = len(images)
        items['identifier'] = "image_id"
        items['items'] = images
        
        body = json.dumps(items, indent=4)
        web.header("Content-Type", "application/json")
        
        return body
    

class imageedit:
    def POST(self):
        '''
        Uses input from the image table and the csapi to update image data.
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
        
        
class imagenew:
    def POST(self):
        '''
        Uses input from the image table and the csapi to create a new image.
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
        

class imagedelete:
    def POST(self):
        '''
        Uses input from the image table and the csapi to delete an image.
        '''
        image = web.input()
        
        token = web.cookies().get('token')
        tenant_id = web.cookies().get('tenant_id')
        
        headers = { "X-Auth-Token": token, "X-Auth-Tenant-ID": tenant_id }
        response = util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/image/v1/images/"+image.id, "DELETE", None, headers)
        if response:
            return web.ok()
        else:
            return web.BadRequest()
    
    
app_image = web.application(urls, locals())