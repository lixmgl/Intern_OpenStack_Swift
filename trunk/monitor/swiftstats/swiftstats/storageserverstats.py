'''
Created on Mar 13, 2012

@author: autumn
'''
from swiftstats.swiftclient import Connection, http_connection
import urlparse
import eventlet

try:
    import simplejson as json
except ImportError:
    import json
    
class StorageServerStats:
    def __init__(self, recon_endpoints, org_prefix, item, logger):
        self.recon_endpoints = recon_endpoints
        self.org_prefix = org_prefix
        self.logger = logger
        self.item = item
    
    def __http_call__(self, url):
        (parsed, conn) = http_connection(url)
        conn.request('GET', parsed.path, '', {})
        resp = conn.getresponse()
        return json.loads(resp.read())
        
    def __stats__(self, recon_endpoint, ret):
        """
        Param : item = mem|sockstat|....
        """
        url = "/".join([recon_endpoint, 'recon', self.item])
        self.logger.debug("start __stats__ for : %s" % (url))
        try:
            resp = (self.__http_call__(url))
            self.logger.debug("response : %s" % str(resp))
            for (key, value) in resp.items():
                parsed = urlparse.urlparse(url)
                host = parsed.netloc.split(':')[0].replace('.','_')
                number = 0
                if isinstance(value, int) or isinstance(value, float):
                    number = value
                elif isinstance(value, str):
                    number = int(value.split()[0])
                ret.append("%s.server.%s.%s.%s:%.2f|g" % (self.org_prefix, host, self.item, key, number))
        except Exception as e:
            self.logger.exception(e) 
    
    def stats(self):
        #self.logger.debug("Begin stats")
        pool = eventlet.GreenPool(100)
        ret = list()
        self.logger.debug("recon_endpoints : %s" % str(self.recon_endpoints))
        for recon_endpoint in self.recon_endpoints:
            self.logger.debug("spawn for %s/%s" % (recon_endpoint, self.item))
            pool.spawn(self.__stats__,recon_endpoint, ret)
        pool.waitall()
        return ret
    
class ReplicationTimeStats(StorageServerStats):
    def __init__(self, recon_endpoints, org_prefix, logger):
        self.recon_endpoints = recon_endpoints
        self.org_prefix = org_prefix
        self.logger = logger
        self.item = 'replication'
    
    def __stats__(self, recon_endpoint, ret):
        """
        Param : item = mem|sockstat|....
        """
        url = "/".join([recon_endpoint, 'recon', self.item])
        self.logger.debug("start __stats__ for : %s" % (url))
        try:
            resp = (self.__http_call__(url))
            self.logger.debug("response : %s" % str(resp))
            for (key, value) in resp.items():
                parsed = urlparse.urlparse(url)
                host = parsed.netloc.split(':')[0].replace('.','_')
                number = 0
                if isinstance(value, int) or isinstance(value, float):
                    number = value
                elif isinstance(value, str):
                    number = int(value.split()[0])
                ret.append("%s.server.%s.%s.%s:%d|g" % (self.org_prefix, host, self.item, key, number*60))
        except Exception as e:
            self.logger.exception(e) 

class MemStats(StorageServerStats):
    
    def __init__(self, recon_endpoints, org_prefix, logger):
        self.recon_endpoints = recon_endpoints
        self.org_prefix = org_prefix
        self.logger = logger
        self.item = 'mem'
        
    def __stats__(self, recon_endpoint, ret):
        url = "/".join([recon_endpoint, 'recon', self.item])
        self.logger.debug("start __stats__ for : %s" % (url))
        try:
            resp = (self.__http_call__(url))
            self.logger.debug("response : %s" % str(resp))
            for (key, value) in resp.items():
                parsed = urlparse.urlparse(url)
                host = parsed.netloc.split(':')[0].replace('.','_')
                number = 0
                if isinstance(value, int)  or isinstance(value, float):
                    number = value
                elif isinstance(value, str):
                    number = int(value.split()[0])
                ret.append("%s.server.%s.%s.%s:%d|g" % (self.org_prefix, host, self.item, key, number*1024))
        except Exception as e:
            self.logger.exception(e) 

class DiskusageStats(StorageServerStats):
    def __init__(self, recon_endpoints, org_prefix, logger):
        self.recon_endpoints = recon_endpoints
        self.org_prefix = org_prefix
        self.logger = logger
        self.item = 'diskusage'
        
    def __stats__(self, recon_endpoint, ret):
        url = "/".join([recon_endpoint, 'recon', self.item])
        self.logger.debug("start __stats__ for : %s" % (url))
        try:
            parsed = urlparse.urlparse(url)
            host = parsed.netloc.split(':')[0].replace('.','_')
            resp = (self.__http_call__(url))
            self.logger.debug("response : %s" % str(resp))
            mounted_disk_num = 0
            unmounted_disk_num = 0
            
            for record in resp:
                device = ''
                for (key, value) in record.items():
                    if key == 'mounted':
                        if value == True:
                            mounted_disk_num += 1
                        else:
                            unmounted_disk_num += 1
                    elif key == "device":
                        device = value
                    else:
                        number = 0
                        if isinstance(value, int)  or isinstance(value, float):
                            number = value
                        elif isinstance(value, str):
                            number = int(value.split()[0])
                        ret.append("%s.server.%s.%s.%s.%s:%d|g" % (self.org_prefix, host, self.item, key, device, number))
            ret.append("%s.server.%s.%s.%s:%d|g" % (self.org_prefix, host, self.item, "mounted_disk_num",mounted_disk_num))
            ret.append("%s.server.%s.%s.%s:%d|g" % (self.org_prefix, host, self.item, "unmounted_disk_num",unmounted_disk_num))
        except Exception as e:
            self.logger.exception(e) 
                

class LoadStats(StorageServerStats):
    """
    # curl --url http://10.100.18.126:6000/recon/load
    {"15m": 0.81999999999999995, "1m": 0.62, "5m": 0.83999999999999997, "processes": 632, "tasks": "3/285"}
    """
    def __init__(self, recon_endpoints, org_prefix, logger):
        self.recon_endpoints = recon_endpoints
        self.org_prefix = org_prefix
        self.logger = logger
        self.item = 'load'
        
    def __stats__(self, recon_endpoint, ret):
        url = "/".join([recon_endpoint, 'recon', self.item])
        self.logger.debug("start __stats__ for : %s" % (url))
        try:
            resp = (self.__http_call__(url))
            parsed = urlparse.urlparse(url)
            host = parsed.netloc.split(':')[0].replace('.','_')
            self.logger.debug("response : %s" % str(resp))
            for (key, value) in resp.items():
                if key[-1] == 'm':
                    ret.append("%s.server.%s.%s.%sinutes_average:%.5f|g" % (self.org_prefix, host, self.item, key, value*100))
                elif key == "tasks":
                    tmpList = value.split('/')
                    runnung_tasks = int(tmpList[0])
                    total_tasks = int(tmpList[1])
                    ret.append("%s.server.%s.%s.%s:%d|g" % (self.org_prefix, host, self.item, 'running_tasks', runnung_tasks))
                    ret.append("%s.server.%s.%s.%s:%d|g" % (self.org_prefix, host, self.item, 'total_tasks', total_tasks))
                else:
                    ret.append("%s.server.%s.%s.%s:%d|g" % (self.org_prefix, host, self.item, key, value))
        except Exception as e:
            self.logger.exception(e) 
