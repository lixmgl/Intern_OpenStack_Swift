'''
Created on Jun 24, 2012

@author: autumn
'''

import sys
from struct import unpack_from

from swift.common.bufferedhttp import http_connect
from swift.common.utils import hash_path
from swift.proxy.server import ObjectController

class NodeTest:
    """
    Node test class
    """
    
    def __init__(self, nodetype, address, port, part_shift = 14):
        self.nodetype = nodetype
        self.address = address
        self.port = port
        self.part_shift = part_shift
        self.node = {'zone': 3, 'weight': 100.0, 'ip': address, 
                'id': 3, 'meta': '', 'device': 'sda6', 'port': port}
    
    def __get_partition__(self, account, container, obj, part_shift):
        """
        Internal method to calculate partition with MD5 hash 
        """
        
        key = hash_path(account, container, obj, raw_digest=True)
        part = unpack_from('>I', key)[0] >> part_shift
        return part
    
    def get_object(self, account, container, object):
        """
        GET object from a standalone node
        """   
        headers = dict()
        partition = self.__get_partition__(account, container, object, self.part_shift)
        
        path = "/%s/%s/%s" % (account, container, object)
        method = "GET"
        conn = http_connect(self.node['ip'], self.node['port'],
                        self.node['device'], partition, method, path,
                        #headers=headers,
                        #query_string=''
                        )
        
        resp = conn.getresponse()
        status = resp.status
        headers = resp.getheaders()
        content = resp.read()

        return (status, headers, content)
    
    def put_object(self, account, container, object, content=None):
        """
        PUT object into a standalone node
        """      
        headers = {'Content-Length': '17', 'X-Forwarded-Host': '10.100.18.125:8080',
                   'X-Auth-Token': 'e4fae830001f41539e1463cd3d534705',
                   'X-User-Name': u'admin', 'Authorization': 'Basic admin',
                   'X-User': u'1fd90f8c10bc497fb2d5a5f501db9825',
                   'X-Container-Host': '10.100.18.128:6001',
                   'X-Container-Partition': 46957, 'Host': '127.0.0.1:8081',
                   'X-User-Id': u'1fd90f8c10bc497fb2d5a5f501db9825',
                   'X-Timestamp': '1340906486.32280',
                   'X-Forwarded-Server': 'swft001.webex.com',
                   'X-Object-Meta-Mtime': '1340745008.39',
                   'X-Tenant': u'74a6a2e705e74158bda736f5c8c6c89d',
                   'Accept-Encoding': 'identity',
                   'X-Role': u'Admin,KeystoneServiceAdmin', 'Connection': 'close',
                   'X-Authorization': u'Proxy admin',
                   'X-Forwarded-For': '10.100.18.125',
                   'X-Roles': u'Admin,KeystoneServiceAdmin',
                   'X-Tenant-Id': u'74a6a2e705e74158bda736f5c8c6c89d',
                   'X-Container-Device': 'sda6', 'Expect': '100-continue',
                   'X-Trans-Id': 'txc17ed111b3ac41fdb3e66f27efa6a4e7',
                   'X-Identity-Status': 'Confirmed',
                   'Content-Type': 'application/octet-stream',
                   'X-Tenant-Name': u'admin'}
        
        partition = self.__get_partition__(account, container, object, self.part_shift)
        
        path = "/%s/%s/%s" % (account, container, object)
        method = "PUT"
        conn = http_connect(self.node['ip'], self.node['port'],
                        self.node['device'], partition, method, path,
                        headers=headers
                        #query_string=''
                        )

        chunk = "openstack great!\n"
        conn.send(chunk)

        chunk = "0\r\n\r\n"
        conn.send(chunk)
        
        resp = conn.getresponse()
        status = resp.status
        headers = resp.getheaders()
        content = resp.read()

        return (status, headers, content)
    
    def delete_object(self, account, container, object):
        """
        DELETE object from a standalone node
        """
        headers = {'X-Timestamp': '1340832923.64154'}
        partition = self.__get_partition__(account, container, object, self.part_shift)               
        path = "/%s/%s/%s" % (account, container, object)
        method = "DELETE"       

        conn = http_connect(self.node['ip'], self.node['port'],
               self.node['device'], partition, 
               method, path, headers=headers)
               
        resp = conn.getresponse()
        status = resp.status
        headers = resp.getheaders()        
        content = resp.read()        

        return (status, headers, content)
    
    def get_container(self, account, container):
        """
        GET container information from a standalone node
        """                
        headers = dict()
        partition = self.__get_partition__(account, container, None, self.part_shift)
        
        path = "/%s/%s" % (account, container)
        method = "GET"
        conn = http_connect(self.node['ip'], self.node['port'],
                        self.node['device'], partition, method, path,
                        #headers=headers,
                        #query_string=''
                        )
        
        resp = conn.getresponse()
        status = resp.status
        headers = resp.getheaders()
        content = resp.read()

        return (status, headers, content)
    
    def put_container(self, account, container):
        """
        PUT container information from a standalone node
        """        
        headers = {'X-Account-Partition': 114472, 'X-Account-Device': 'sda6',
                   'Connection': 'close', 'X-Timestamp': '1340832923.64154',
                   'x-trans-id': 'tx8b4a90530e28434a87372baf19c507ac',
                   'X-Account-Host': '10.100.18.126:6002'}
        
        partition = self.__get_partition__(account, container, None, self.part_shift)
        
        path = "/%s/%s" % (account, container)
        method = "PUT"
        conn = http_connect(self.node['ip'], self.node['port'],
                        self.node['device'], partition, method, path,
                        headers=headers
                        #query_string=''
                        )
        
        resp = conn.getresponse()
        status = resp.status
        headers = resp.getheaders()
        content = resp.read()

        return (status, headers, content)
    
    def delete_container(self, account, container):
        """
        DELETE container information from a standalone node
        """
        headers = dict()
        partition = self.__get_partition__(account, container, None, self.part_shift)
        path = "/%s/%s/%s" % (account, container)        
        method = "DELETE"        

        conn = http_connect(self.node['ip'], self.node['port'], 
               self.node['device'], partition, method, path)

        resp = conn.getresponse()
        status = resp.status
        headers = resp.getheaders()
        content = resp.read()

        return (status, headers, content)      

    def get_account(self, account):
        """
        GET account information from a standalone node
        """        
        headers = dict()
        partition = self.__get_partition__(account, None, None, self.part_shift)
        
        path = "/%s" % account
        method = "GET"
        conn = http_connect(self.node['ip'], self.node['port'],
                        self.node['device'], partition, method, path,
                        #headers=headers,
                        #query_string=''
                        )
        
        resp = conn.getresponse()
        status = resp.status
        headers = resp.getheaders()
        content = resp.read()

        return (status, headers, content)
    
    def put_account(self, account):
        """
        PUT account information from a standalone node
        """        
        headers = {'Connection': 'close', 'X-Timestamp': '1340838357.96764',
                   'X-Trans-Id': 'txeed165fe7b1f4e158fe564475e4acfee'}
        
        partition = self.__get_partition__(account, None, None, self.part_shift)
        
        path = "/%s" % account
        method = "PUT"
        conn = http_connect(self.node['ip'], self.node['port'],
                        self.node['device'], partition, method, path,
                        headers=headers
                        #query_string=''
                        )
        
        resp = conn.getresponse()
        status = resp.status
        headers = resp.getheaders()
        content = resp.read()

        return (status, headers, content)
    
    def delete_account(self, account):
        """
        DELETE account information from a standalone node
        """
        headers = dict()
        partition = self.__get_partition__(account, None, None, self.part_shift)  
        path = "/%s/%s/%s" % account        
        method = "DELETE"        

        conn = http_connect(self.node['ip'], self.node['port'],
               self.node['device'], partition, method, path)

        resp = conn.getresponse()        
        status = resp.status        
        headers = resp.getheaders()        
        content = resp.read()        

        return (status, headers, content) 
    
if __name__ == '__main__':
    """
    Main function of swift.nodetest
    """
    
    """
    if len(sys.argv) not in [4,5]:
        print ("Usage : %s nodetype ipaddress port [part_shift]" % sys.argv[0])
        print ("nodetype = proxy | storage")
        print ("part_shift is 14 by default.")
        sys.exit(0)
    
    nodetype = sys.argv[1]
    address = sys.argv[2]
    port = int(sys.argv[3])
    part_shift = 14
    if len(sys.argv) == 5:
        part_shift = int(sys.argv[4])
    """
    """
    node_test1 = NodeTest('storage', "10.100.18.126", 6000)
    status, headers, content = node_test1.get_object("AUTH_74a6a2e705e74158bda736f5c8c6c89d", "test1", "obj1")
    print "obj response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    """
    """
    node_test2 = NodeTest('storage', "10.100.18.126", 6001)
    status, headers, content = node_test2.get_container("AUTH_74a6a2e705e74158bda736f5c8c6c89d", "test1")
    print "\ncontainer response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content   
    """
    """
    node_test3 = NodeTest('storage', "10.100.18.126", 6002)
    status, headers, content = node_test3.get_account("AUTH_74a6a2e705e74158bda736f5c8c6c89d")
    print "\naccount response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    """

    """
    node_test4 = NodeTest('storage', "10.100.18.126", 6001)
    status, headers, content = node_test4.put_container("AUTH_74a6a2e705e74158bda736f5c8c6c89d", "test1")
    print "\nput container response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    """
    """
    node_test5 = NodeTest('storage', "10.100.18.126", 6002)
    status, headers, content = node_test5.put_account("AUTH_7e59458700a447fdb7adbd014e6a8954")
    print "\nput container response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    """
    node_test6 = NodeTest('storage', "10.100.18.126", 6000)
    status, headers, content = node_test6.put_object("AUTH_74a6a2e705e74158bda736f5c8c6c89d", "test1", "obj2")
    print "\nput obj response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content

    status, headers, content = node_test6.get_object("AUTH_74a6a2e705e74158bda736f5c8c6c89d", "test1", "obj2")
    print "\nget obj response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content

    status, headers, content = node_test6.delete_object("AUTH_74a6a2e705e74158bda736f5c8c6c89d", "test1", "obj2")
    print "\ndelete obj response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content

    status, headers, content = node_test6.get_object("AUTH_74a6a2e705e74158bda736f5c8c6c89d", "test1", "obj2")
    print "\nget obj response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content

