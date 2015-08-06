# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
from glance import client as glance_client
from configParse import Parse

parser = Parse("properties.cfg") 
_glance_host = parser.get_value("IMAGE", "image_ip") 
_glance_port = parser.get_value("IMAGE", "image_port")

def get_images(token):
    glance = glance_client.Client(_glance_host, int(_glance_port), auth_tok=token)
    images = []
    for image in glance.get_images():
        images.append(_format_image(image))
    return images

def get_images_detailed(token):
    glance = glance_client.Client(_glance_host, int(_glance_port), auth_tok=token)
    images = []
    for image in glance.get_images_detailed():
        images.append(_format_image_detailed(image))
    return images

def get_image_meta(image_id, token):
    glance = glance_client.Client(_glance_host, int(_glance_port), auth_tok=token)
    #return _format_image_detailed(glance.get_image_meta(image_id))
    return glance.get_image_meta(image_id)

def update_image_meta(token, image_id, image_meta=None, image_data=None, features=None):
    glance=glance_client.Client(_glance_host, int(_glance_port), auth_tok=token)
    glance.update_image(image_id, image_meta, image_data=None, features=None)
    return None

def add_image(token, image_meta=None, image_data=None, features=None):
    glance=glance_client.Client(_glance_host, int(_glance_port), auth_tok=token)
    #image_meta = glance.get_image_meta(image_id)
    new_image_id = glance.add_image(image_meta, image_data, features=None)
    #return [image_meta, header_data]
    #return image_meta
    return new_image_id

def delete_image(token, image_id):
    glance = glance_client.Client(_glance_host, int(_glance_port), auth_tok=token)
    glance.delete_image(image_id)
    return None

class ComputeImages(object):       
    def __init__(self, conn):
        self.conn = conn 
        
    def get_images(self):
        images = []
        for image in self.conn.list_images():
            images.append(image)
        return images
    
    def get_sizes(self):
        return self.conn.list_sizes() 
        
    def get_image(self, search):    
        """search by image name|id returning first instance 
        of the 'image' found"""
        images = self.conn.list_images() 
        i = 0; 
        while i < len(images):
            if search in images[i].name:
                return images[i] 
            elif search in images[i].id:
                return nodes[i] 
            i += 1  
        for image in self.conn.list_images():
            images=glance_client.get_images_detailed(image_id)
            return images
        
    def get_size(self, search):    
        """searh by name|id|ram|disk returning first instance 
        found"""
        sizes = self.conn.list_sizes() 
        i = 0; 
        while i < len(sizes):
            if search in sizes[i].name:
                return sizes[i] 
            elif search in sizes[i].id:
                return sizes[i] 
            elif search in str(sizes[i].ram):
                return sizes[i] 
            elif search in str(sizes[i].disk):
                return sizes[i] 
            i += 1  
            
def _format_image(image):
    return {
        'image_id': image['id'],
        'image_name': image['name']
    }
    
def _format_image_detailed(image):
    return {
        'image_id': image['id'],
        'image_name': image['name'],
        'image_format': image['disk_format'],
        'container_format': image['container_format'],
        'image_created': image['created_at'],
        'image_size': image['size']
    }