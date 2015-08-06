# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import web
import util
import simplejson as json

urls = (
        '', 'Health',
        '/', 'Health'
)

render_health = web.template.render('templates', cache=False)

class Health:
    def GET(self):
        return render_health.health()
    
app_health = web.application(urls, locals())