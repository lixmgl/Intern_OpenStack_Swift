'''
Created on Jun 24, 2012

@author: autumn
'''

import sys
from struct import unpack_from

from swift.common.bufferedhttp import http_connect
from swift.common.utils import hash_path

class NodeTest:
    """
    Node test class
    """
    
    def __init__(self, nodetype, address, port, part_shift=14):
        self.nodetype = nodetype
        self.address = address
        self.port = port
        self.part_shift = part_shift
    
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
        
        node = {'zone': 3, 'weight': 100.0, 'ip': self.address, 
                'id': 3, 'meta': '', 'device': 'sda6', 'port': self.port}
        
        headers = dict()
        partition = self.__get_partition__(account, container, object, self.part_shift)
        
        path = "/%s/%s/%s" % (account, container, object)
        method = "GET"
        conn = http_connect(node['ip'], node['port'],#class
                        node['device'], partition, method, path,
                        #headers=headers,
                        #query_string=''
                        )
        
        resp = conn.getresponse()
        status = resp.status
        headers = resp.getheaders()
        content = resp.read()

        return (status, headers, content)#http's return value, headers contain more information and could be verified later, content is the file content.
    
    def put_object(self, account, container, object, content):#put a file to server
        """
        PUT object into a standalone node
        """
        
        pass
    
    def delete_object(self, account, container, object):#opposite to get
        """
        DELETE object from a standalone node
        """
        
        pass
    
    def get_container(self, account, container):
        """
        GET container information from a standalone node
        """
        
        pass
    
    def put_container(self, account, container):
        """
        PUT container information from a standalone node
        """
        
        pass
    
    def delete_container(self, account, container):
        """
        DELETE container information from a standalone node
        """
        
        pass    

    def get_account(self, account):
        """
        GET account information from a standalone node
        """
        
        pass
    
    def put_account(self, account):
        """
        PUT account information from a standalone node
        """
        
        pass
    
    def delete_account(self, account):
        """
        DELETE account information from a standalone node
        """
        
        pass 
    
if __name__ == '__main__':#package to command line use shellscript or been 
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
    
    node_test = NodeTest('storage', "10.100.18.126", 6000)
    status, headers, content = node_test.get_object("AUTH_74a6a2e705e74158bda736f5c8c6c89d", "test1", "obj1")
    print "Response:\n================================================="
    print "status \t\t : %d" % status
    print "headers \t : %s" % str(headers)
    print "content \t : %s" % content

    
    
    

