# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import os
import web

urls = (
    '/images/(.*)', 'staticimages',
    '/js/(.*)', 'staticjs',
    '/css/(.*)', 'staticcss',
    '/html/(.*)', 'statichtml',
    '/json/(.*)', 'staticjson'
)

class staticimages:
    def GET(self,name):
        '''
        Securely forwards static images.
        '''
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"image/png",
            "jpg":"image/jpeg",
            "gif":"image/gif",
            "ico":"image/x-icon"            }

        if name in os.listdir('static/images'):
            web.header("Content-Type", cType[ext])
            return open('static/images/%s'%name,"rb").read()
        else:
            raise web.notfound()
        
class staticjs:
    def GET(self,name):
        '''
        Securely forwards static javascript.
        '''
        if name in os.listdir('static/js'):
            web.header("Content-Type", "text/javascript")
            return open('static/js/%s'%name,"r").read()
        else:
            raise web.notfound()

class staticcss:
    def GET(self,name):
        '''
        Securely forwards static css.
        '''
        if name in os.listdir('static/css'):
            web.header("Content-Type", "text/css")
            return open('static/css/%s'%name,"r").read()
        else:
            raise web.notfound()

class statichtml:
    def GET(self,name):
        '''
        Securely forwards static html.
        '''
        if name in os.listdir('static/html'):
            web.header("Content-Type", "text/html")
            return open('static/html/%s'%name,"r").read()
        else:
            raise web.notfound()

class staticjson:
    def GET(self,name):
        '''
        Securely forwards static json.
        '''
        if name in os.listdir('static/json'):
            web.header("Content-Type", "application/json")
            return open('static/json/%s'%name,"r").read()
        else:
            raise web.notfound()
                
app_static = web.application(urls, locals())