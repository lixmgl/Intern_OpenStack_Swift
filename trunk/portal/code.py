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

import python.util as util

import python.static as static
import python.auth as auth
import python.compute as compute
import python.image as image
import python.charts as charts
import python.object as object
import python.project as project
import python.metrics as metrics
import python.health as health

render = web.template.render('templates', cache=False)

urls = (
    '/', 'index',
    '/main', 'main',
    '/spadmin', 'spadmin',
    '/auth', auth.app_auth,
    '/static', static.app_static,
    '/compute', compute.app_compute,
    '/image', image.app_image,
    '/charts', charts.app_charts,
    '/object', object.app_object,
    '/project', project.app_project,
    '/metrics', metrics.app_metrics,
    '/health', health.app_health
)

product_version = json.loads(util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/config/section/VERSION/param/product_version", "GET"))
product_name = json.loads(util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/config/section/VERSION/param/product_name", "GET"))
org_name = json.loads(util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/config/section/VERSION/param/org_name", "GET"))

app = web.application(urls, globals())

class index:
    def GET(self):
        '''
        Renders the login page.
        TODO: If cookies are active, this should forward to main...
        '''
        return render.index(org_name, product_name, product_version)
    
class main:    
    def GET(self):
        '''
        Currently, this just redirects to the spadmin class.
        This class can be updated to do any pre-render logic, i.e. role based variables, loading user settings, etc.
        '''
        raise web.seeother('/spadmin')

class spadmin:
    def GET(self):
        '''
        Discovers module/plugin definitions and passes them to the spadmin template to be rendered.
        '''
        headers = { "Accept": "application/json" }
        modules = json.loads(util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/config/section/MODULES", "GET", None, headers))
        xmodules = []
        for module in modules:
            xmodule = json.loads(util.APIRequest(util.csapi_ip, util.csapi_port, util.csapi_root+"/config/section/MODULES/param/"+module[0], "GET", None, headers))
            web.webapi.debug(xmodule)
            xmodules.insert(len(xmodules), json.loads(xmodule))

        return render.spadmin(xmodules)
    
application = app.wsgifunc()

if __name__ == "__main__":
    app.run() 