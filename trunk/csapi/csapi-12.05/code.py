# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************

import sys
import os
import web

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

import identityWeb
import computeWeb
import imageWeb
import configWeb
import objectstoreWeb

urls = (
    "/identity", identityWeb.app_identity,
    "/compute", computeWeb.app_compute,
    "/image", imageWeb.app_image,
    "/config", configWeb.app_config,
    "/objectstore", objectstoreWeb.app_objectstore
)

app = web.application(urls, locals())
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()      