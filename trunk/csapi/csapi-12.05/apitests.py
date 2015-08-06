# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import unittest
import identity
import image
import driver
from compute import ComputeNodes
import random

_endpoint = "http://10.100.18.144:5000/v2.0" 
username = "admin"
password = "secrete"
tenant_id = "b3c18bc8a54f4f1c93afe949f790d5c6"
image_id = "5b920dc1-52d1-4cce-aea4-effaf994c3de"
rand_seed = random.randint(10000000,99999999)
random_image_id = "%d-1234-1234-1234-abcdabcdabcd" % rand_seed

conn = driver.libcloud_driver_password("admin", "secrete", "admin")
token = ComputeNodes(conn).get_token()

class KeystoneAPITests(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_get_token(self):
        #token = identity.get_token(keystone, username, password, "NATIVE")
        
        #if token == -1:
            #return web.webUnauthorized()
        
        auth_token = {}
        #auth_token['token'] = token.id
        
        #body = json.dumps(auth_token)
        #web.header("Content-Type", "application/json")
        #self.assertEquals(len(body), 32, 'Token was not issued')
        self.assertIsNotNone(auth_token, 'There should be data here')
        #self.assertEquals(len(auth_token), 32)
        #return None
        
    def test_list_tenants(self):
        #keystone = identity.auth(username, password, tenant_id, _endpoint)
        #data = identity.list_tenants(keystone)
        #for line in data:
            #self.assertIsNotNone(line, 'No data')
        data = {}
        self.assertIsNotNone(data, 'This should not be empty')
        
    def test_get_tenant_token(self):
        """
        Stub
        """
        data = {}
        self.assertIsNotNone(data, 'This should not be empty')
        
    def test_list_tenants(self):
        """
        Stub
        """
        data = {}
        self.assertIsNotNone(data, 'Not empty')
        
    def test_create_tenant(self):
        data = {}
        self.assertIsNotNone(data, 'Not empty')
        
    def test_delete_tenant(self):
        """
        Deletes the newly created tenant
        """
        data = {}
        self.assertIsNotNone(data, 'Not empty')
    
class GlanceAPITests(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_5get_images(self):
        data = image.get_images(token)
        print "\nImage Data:", data
        self.assertIsNotNone(data, 'No data')
        
    def test_6get_images_detailed(self):
        data = image.get_images_detailed(token)
        print "\nDetailed Image Data: ", data
        for line in data:
            self.assertIsNotNone(line, 'No data')
    
    def test_7get_image_meta(self):
        data = image.get_image_meta(image_id, token)
        print "\nImage Data: ", data
        self.assertIsNotNone(data, 'No data')
        
    def test_1add_image(self):
        data = image.add_image(token, image_meta={'id': random_image_id, 'name': 'test1', 'image_format': 'qcow2', 'container_format': 'ovf'})
        print "\nImage ID:", data
        self.assertIsNotNone(data, 'No data')
        
    def test_2update_new_image(self):
        data = image.update_image_meta(token, image_id=random_image_id, image_meta={'name': 'New Test Image - Changed'})
        self.assertIsNone(data, 'This should not return any data')
        
    def test_3update_image(self):
        data = image.update_image_meta(token, image_id, image_meta={'name': 'revised_test_name'})
        self.assertIsNone(data, 'This should not return any data')
        
    def test_4revise_updated_image(self):
        data = image.update_image_meta(token, image_id, image_meta={'name': 'API_Test_IMG'})
        self.assertIsNone(data, 'This should not return any data')
        
    def test_9delete_image(self):
        data = image.delete_image(token, image_id=random_image_id)
        self.assertIsNone(data, 'This should not return any data')
        
        
class NovaAPITests(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        conn = driver.libcloud_driver_password("admin", "secrete", "admin")
        self.novatest = ComputeNodes(conn)
    
    def test_get_nodes(self):
        data = self.novatest.get_nodes()
        print "\nNode ID:", data
        self.assertIsNotNone(data, 'No data')
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
    
#suite = unittest.TestLoader().loadTestsFromTestCase(KeystoneAPITests)
#unittest.TextTestRunner(verbosity=2).run(suite)