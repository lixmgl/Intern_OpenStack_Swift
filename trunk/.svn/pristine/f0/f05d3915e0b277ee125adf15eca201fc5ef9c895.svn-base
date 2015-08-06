# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************

from swift.common import client as client
import cloudfiles
from configParse import Parse

parser = Parse("properties.cfg") 
_object_ip = parser.get_value("OBJECT", "object_ip") 
_object_port = parser.get_value("OBJECT", "object_port")
_object_root = parser.get_value("OBJECT", "object_root")
_object_url = parser.get_value("OBJECT", "object_service")

class SwiftAuthentication(object):
    """ Auth container in the format CloudFiles expects. """
    def __init__(self, storage_url, auth_token):
        self.storage_url = storage_url
        self.auth_token = auth_token

    def authenticate(self):
        return (self.storage_url, '', self.auth_token)

def swift_api(token):
    endpoint = _object_url
    auth = SwiftAuthentication(endpoint, token)
    return cloudfiles.get_connection(auth=auth)

def swift_get_containers(token, marker=None):
    limit = 1000
    containers = swift_api(token).get_all_containers(limit=limit + 1,
                                                       marker=marker)
    if(len(containers) > limit):
        return (containers[0:-1], True)
    else:
        return (containers, False)






