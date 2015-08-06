
'''
Created on Jun 24, 2012

@author: autumn
'''

import sys
import time

from random import Random
from struct import unpack_from

from swift.common.bufferedhttp import http_connect
from swift.common.utils import hash_path
from swift.proxy.server import ObjectController

CHUNK_SIZE = 1024

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
                'id': 3, 'meta': '', 'device': 'sda7', 'port': port}

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

    def put_object(self, account, container, object, content=''):
        """
        PUT object into a standalone node
        """
        headers = {'Content-Length': '%d' % len(content), 
                   'X-Timestamp': '%f' % time.time(),
                   'X-Object-Meta-Mtime': '%f' % time.time(),
                   'X-Container-Device': 'sda7', 'Expect': '100-continue',
                   'Content-Type': 'application/octet-stream'} 
        
        partition = self.__get_partition__(account, container, object, self.part_shift)

        path = "/%s/%s/%s" % (account, container, object)
        method = "PUT"
        conn = http_connect(self.node['ip'], self.node['port'],
                        self.node['device'], partition, method, path,
                        headers=headers
                        #query_string=''
                        )

        length = len(content)
        point = 0
        while (point < length):
            chunk = content[point:point+CHUNK_SIZE]
            #print "point = %d : %s" % (point, chunk)
            conn.send(chunk)
            point += CHUNK_SIZE

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
        
        headers = {'X-Timestamp': '%f' % time.time()}

        partition = self.__get_partition__(account, container, object, self.part_shift)
        path = "/%s/%s/%s" % (account, container, object)
        method = "DELETE"

        conn = http_connect(self.node['ip'], self.node['port'],
               self.node['device'], partition, method, path, headers=headers)

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
        partition = self.__get_partition__(account, container, None, self.part_shift)
        headers = {'X-Account-Partition': partition, 'X-Account-Device': 'sda7',
                   'Connection': 'close', 'X-Timestamp': '%f' % time.time()
                   }

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
        headers = {'X-Timestamp': '%f' % time.time()}
        partition = self.__get_partition__(account, container, None, self.part_shift)
        path = "/%s/%s" % (account, container)
        method = "DELETE"

        conn = http_connect(self.node['ip'], self.node['port'],
               self.node['device'], partition, method, path,
                headers=headers
               )

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
        headers = {'Connection': 'close', 'X-Timestamp': '%f' % time.time(),
                   #'X-Trans-Id': 'txeed165fe7b1f4e158fe564475e4acfee'
                   }

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
        headers = {'X-Timestamp': '%f' % time.time()}
        partition = self.__get_partition__(account, None, None, self.part_shift)
        path = "/%s" % account
        method = "DELETE"

        conn = http_connect(self.node['ip'], self.node['port'],
               self.node['device'], partition, method, path,
                headers=headers
               )

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
    
    server = '10.100.18.128'
    account_port = 6002
    container_port = 6001
    object_port = 6000
    
    r = Random()
    account = 'AUTH_7e59458700a447fdb7adbd%d' % r.randint(1000000000, 9000000000)
    container = 'my_container_01'
    object = 'my_object_02'
    the_content = "This is the test object 02!"
    
    t1 = NodeTest('storage', server, account_port)
    status, headers, content  = t1.put_account(account)
    print "put account response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    
    status, headers, content  = t1.get_account(account)
    print "\nget account response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    
    t2 = NodeTest('storage', server, container_port)
    status, headers, content  = t2.put_container(account, container)
    print "\nput container response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    
    status, headers, content  = t2.get_container(account, container)
    print "\nget container response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    
    t3 = NodeTest('storage', server, object_port)
    status, headers, content  = t3.put_object(account, container, object, the_content)
    print "\nput object response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    
    status, headers, content  = t3.get_object(account, container, object)
    print "\nget object response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    
    status, headers, content  = t3.delete_object(account, container, object)
    print "\ndelete object response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    
    status, headers, content  = t2.delete_container(account, container)
    print "\ndelete container response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content
    
    status, headers, content  = t1.delete_account(account)
    print "\ndelete account response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content

    status, headers, content  = t3.get_object(account, container, object)
    print "\nget object response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content

    status, headers, content  = t2.get_container(account, container)
    print "\nget container response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content

    status, headers, content  = t1.get_account(account)
    print "\nget account response:\n================================================="
    print "status\t: %d" % status
    print "headers\t: %s" % str(headers)
    print "content\t:\n%s" % content