# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************

import sys
import image
import driver
import os
import web
import datetime
from glance.common import client as base_client

import simplejson as json

_endpoint = "http://10.100.32.36:5000/v2.0"
_admin_endpoint = "http://10.100.32.36:35357/v2.0"
_glance_host = "10.100.18.144"

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)


urls = (
    "", "imageWebIndex",
    "/v1/images", "imageWeb",
    "/v1/images/", "imageWeb",
    "/v1/images/detail", "imagedetailWeb",
    "/v1/images/detail/", "imagedetailWeb",
    "/v1/images/(.*)", "imageWeb",
    "/v1/images/(.*)/members", "imageWeb",
    "/v1/images/(.*)/members/", "imageWeb",
    "/v1/images/(.*)/members/(.*)", "imageWeb",
    "/v1/shared_images/(.*)", "sharedImageWeb"
)

class imageWebIndex:
    """
    """
    def GET(self):
        raise web.seeother('/')
    
class imagedetailWeb:
    def GET(self, image_id=''):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        
        return json.dumps(image.get_images_detailed(auth_token), indent=4)

class imageWeb:
    """
    """
    
    def GET(self, image_id=''):
    # User needs to authenticate to get details for image(s)
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        
        if len(image_id) <= 0:
            return json.dumps(image.get_images(auth_token), indent=4)
        else:
            return json.dumps(image.get_image_meta(image_id, auth_token), indent=4)
        
        
    def POST(self, image_id='', image_meta=None):
        """
        This func registers a new VM image and creates an image_id for the image or updates the metadata for an image
        Args: name, image_format, container_format, etc...
        """
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        image_meta = {}
        """
        Image parameters
        """
        image_meta['id'] = web.ctx.env.get('HTTP_X_IMAGE_META_ID', image_id)
        image_meta['name'] = web.ctx.env.get('HTTP_X_IMAGE_META_NAME', None)
        image_meta['distro'] = web.ctx.env.get('HTTP_X_IMAGE_META_DISTRO', None)
        image_meta['status'] = web.ctx.env.get('HTTP_X_IMAGE_META_STATUS', None)
        image_meta['checksum'] = web.ctx.env.get('HTTP_X_IMAGE_META_CHECKSUM', None)
        image_meta['created_at'] = web.ctx.env.get('HTTP_X_IMAGE_META_CREATED_AT', None)
        image_meta['disk_format'] = web.ctx.env.get('HTTP_X_IMAGE_META_DISK_FORMAT', None)
        image_meta['updated_at'] = web.ctx.env.get('HTTP_X_IMAGE_META_UPDATED_AT', None)
        image_meta['owner'] = web.ctx.env.get('HTTP_X_IMAGE_META_OWNER', None)
        image_meta['min_ram'] = web.ctx.env.get('HTTP_X_IMAGE_META_MIN_RAM', None)
        image_meta['container_format'] = web.ctx.env.get('HTTP_X_IMAGE_META_CONTAINER_FORMAT', None)
        image_meta['min_disk'] = web.ctx.env.get('HTTP_X_IMAGE_META_MIN_DISK', None)
        image_meta['size'] = web.ctx.env.get('HTTP_X_IMAGE_META_SIZE', None)
        image_meta['properties'] = web.ctx.env.get('HTTP_X_IMAGE_META_PROPERTIES', None)
        """
        The following are boolean parameters of the selected image
        """
        image_meta['deleted'] = web.ctx.env.get('HTTP_X_IMAGE_META_DELETED', 'false')
        image_meta['protected'] = web.ctx.env.get('HTTP_X_IMAGE_META_PROTECTED', 'false')
        image_meta['is_public'] = web.ctx.env.get('HTTP_X_IMAGE_META_IS_PUBLIC', 'false')
        
        image.update_image_meta(auth_token, image_id, image_meta, image_data=None, features=None)
        
        return json.dumps(image_meta, indent = 4)
    
    def PUT(self):
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        
        image_data = web.data()
        image_meta={}
        """
        Image parameters
        """
        image_meta['id'] = web.ctx.env.get('HTTP_X_IMAGE_META_ID', None)
        image_meta['name'] = web.ctx.env.get('HTTP_X_IMAGE_META_NAME', None)
        image_meta['status'] = web.ctx.env.get('HTTP_X_IMAGE_META_STATUS', None)
        image_meta['checksum'] = web.ctx.env.get('HTTP_X_IMAGE_META_CHECKSUM', None)
        image_meta['created_at'] = web.ctx.env.get('HTTP_X_IMAGE_META_CREATED_AT', None)
        image_meta['disk_format'] = web.ctx.env.get('HTTP_X_IMAGE_META_DISK_FORMAT', None)
        image_meta['updated_at'] = web.ctx.env.get('HTTP_X_IMAGE_META_UPDATED_AT', None)
        image_meta['owner'] = web.ctx.env.get('HTTP_X_IMAGE_META_OWNER', None)
        image_meta['min_ram'] = web.ctx.env.get('HTTP_X_IMAGE_META_MIN_RAM', None)
        image_meta['container_format'] = web.ctx.env.get('HTTP_X_IMAGE_META_CONTAINER_FORMAT', None)
        image_meta['min_disk'] = web.ctx.env.get('HTTP_X_IMAGE_META_MIN_DISK', None)
        image_meta['size'] = web.ctx.env.get('HTTP_X_IMAGE_META_SIZE', None)
        image_meta['properties'] = web.ctx.env.get('HTTP_X_IMAGE_META_PROPERTIES', None)
        """
        Boolean image parameters
        """
        image_meta['deleted'] = web.ctx.env.get('HTTP_X_IMAGE_META_DELETED', 'false')
        image_meta['protected'] = web.ctx.env.get('HTTP_X_IMAGE_META_PROTECTED', 'false')
        image_meta['is_public'] = web.ctx.env.get('HTTP_X_IMAGE_META_IS_PUBLIC', 'false')
            
        new_image_id = image.add_image(auth_token, image_meta, image_data, features=None)
        
        return json.dumps(new_image_id, indent=4)
            
    def DELETE(self, image_id=''):
        """
        This function deletes an image identified by the provided image_id
        """
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        image.delete_image(auth_token, image_id)
        
        return None
        
class sharedImageWeb:
    """
    """
    def GET(self):
        raise web.seeother('/')
    
app_image = web.application(urls, locals())