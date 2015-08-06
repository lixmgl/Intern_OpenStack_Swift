# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import web
import util
import simplejson as json

urls = (
        '', 'Metrics',
        '/', 'Metrics'
)

render_metrics = web.template.render('templates', cache=False)

class Metrics:
    def GET(self):
        return render_metrics.metrics()
    
app_metrics = web.application(urls, locals())