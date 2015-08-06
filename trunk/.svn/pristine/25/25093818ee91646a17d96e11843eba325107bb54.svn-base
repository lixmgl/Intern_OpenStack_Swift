# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import web
import util
import simplejson as json

urls = (
        '', 'Object',
        '/', 'Object'
)

render_object = web.template.render('templates', cache=False)

class Object:
    def GET(self):
        return render_object.object() 
    
    
app_object = web.application(urls, locals())