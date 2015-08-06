'''
Created on Mar 12, 2012

@author: autumn
'''

from swift.common.client import *
import time


    
if __name__ == "__main__":
    end_point = "https://10.100.18.149:5000/v1.0"
    #end_point = "https://10.120.6.13:5001/v1.0"
    #end_point = "https://10.100.18.125:8080/auth/v1.0"
    """
    identity = "admin"
    credential = "secrete"
    #identity = "system:root"
    #credential = "testpass"
    start_time = time.time()
    
    print "Before connecting"
    swift_client = Connection(end_point, identity, credential)
    print "After connecting"
    
    headers = swift_client.head_account()
    print("headers = %s" % str(headers))

    (header, conList) = swift_client.get_account()
    
    
    print ("header : %s" % str(header))
    for con in conList:
        print ("[container] %s" % str(con))
        
    end_time = time.time()
    
    print "Cost time : %.5f seconds" % (end_time - start_time)
    """
    
    #"""
    identity = "healthcheck"
    credential = "health@check123"
    swift_client = Connection(end_point, identity, credential)
    
    (head, content) = swift_client.get_object("healthcheck", "healthcheck.txt")
    print "Header : \t%s" % str(head)
    print "Content: \t%s" % str(content)
    #"""
    
    
        