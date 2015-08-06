import sys
from swift.common.client import *
    
class PostNodeTest:
    """
    post node test class
    """
    def __init__(self, identity, credential, end_point="https://10.100.18.149:5000/v1.0"):
        self.identity = identity
        self.credential = credential
        self.end_point = end_point
        self.swift_client = Connection(self.end_point, self.identity, self.credential)
    
    def upload_object(self, container, contents):
        """
        upload 100 objects via authentication node
        """
        objlist = list()
          
        content_length = len(contents)
          
        for i in range(100):
            obj = "b" + str(i)
            print "put container %s" % obj
            head = self.swift_client.put_object(container, obj, contents, content_length)
            print "Header : \t\n%s\n" % str(head)
            objlist.append(obj)
        
        return objlist
            
            
    def delete_object(self, container):
        """
        delete 100 objects via authentication node
        """
        #objlist = list()
          
        #swift_client = Connection(self.end_point, self.identity, self.credential)
          
        for i in range(100):
            obj = "b" + str(i)
            print "delete container %s" % obj
            head = self.swift_client.delete_object(container, obj)
            print "Header : \t\n%s\n" % str(head)
            #objlist.remove(obj)
        
        #return objlist
    
if __name__ == '__main__':
    end_point = "https://10.100.18.149:5000/v1.0"
    identity = 'test'
    credential = 'pass1234'
    content = 'just for testing'
    container = "test0"
    
    test = PostNodeTest(identity, credential, end_point)
    test.upload_object(container, content)
    test.delete_object(container)
    
    
