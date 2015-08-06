# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************

import web
from configParse import Parse
import simplejson as json

urls = (
    "/section/(.*)/param/(.*)", "configWeb",
    "/section/(.*)", "configWeb"
)

class configWeb:
    def GET(self, section="", param=""):
        
        parser = Parse("properties.cfg") 
        web.header("Content-Type", "application/json")
        
        if len(section) > 0 and len(param) > 0:
            return json.dumps(parser.get_value(section, param), indent=4)
        elif len(section) > 0:
            return json.dumps(parser.get_section(section), indent=4)
        else:
            return web.BadRequest()
        
app_config = web.application(urls, locals())


