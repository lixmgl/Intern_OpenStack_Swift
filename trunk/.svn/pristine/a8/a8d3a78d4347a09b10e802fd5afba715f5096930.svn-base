# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************

import httplib
import ConfigParser
import simplejson as json
import web

class Parse(object):    
    """  Class to parse config file"""
    def __init__(self, file): 
        self.file = file 
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(self.file)

    def get_section(self, section):
        """Returns a section of the config file""" 
        section_list = []
        data = self.Config.items(section) 
        for line in data:
            section_list.append(line)
        return section_list
        
    def get_value(self, section, value):
        """Returns a specific value"""
        i = 0
        section_list = self.get_section(section)
        while i < len(section_list):
            if section_list[i][0] == value:
                return section_list[i][1]
            i += 1
            
def APIRequest(host="localhost", port=80, path="/", method="GET", params=None, headers={}):
    '''
    A function that uses httplib to make simple calls.  
    Mostly useful for REST API requests that take/return JSON 
    '''
    _headers = { "Content-type": "application/json", "Accept": "application/json" }
    _headers.update(headers)
    conn = httplib.HTTPConnection(host, port)
    conn.request(method, path, json.dumps(params), _headers)
    response = conn.getresponse()
    _data = response.read()
    conn.close()
    
    return _data

config = Parse("properties.cfg")
csapi_ip = config.get_value("CSAPI", "csapi_ip")
csapi_port = config.get_value("CSAPI", "csapi_port")
csapi_root = config.get_value("CSAPI", "csapi_root")
admin_tenant_id = json.loads(APIRequest(csapi_ip, csapi_port, csapi_root+"/config/section/ADMIN/param/admin_tenant_id", "GET"))
portal_ip = json.loads(APIRequest(csapi_ip, csapi_port, csapi_root+"/config/section/PORTAL/param/portal_ip", "GET"))
portal_port = json.loads(APIRequest(csapi_ip, csapi_port, csapi_root+"/config/section/PORTAL/param/portal_port", "GET"))
portal_root = json.loads(APIRequest(csapi_ip, csapi_port, csapi_root+"/config/section/PORTAL/param/portal_root", "GET"))