import sys
from csapiunittest import TestLoader, TextTestRunner
from compute import ComputeNodes 
import image
import testdriver
import unittest2
import integration
from integration import TestDaemon
from configParse import Parse

class StdTest(unittest2.TestCase):
    def setUp(self):
        unittest2.TestCase.setUp(self)
        conn = testdriver.libcloud_driver_password("admin", "secrete", "admin", "10.100.18.144")
        self.comuptetest = ComputeNodes(conn)

    def tearDown(self):
        unittest2.TestCase.tearDown(self)
        self.comuptetest.close()

    def test_get_token(self):
        ret = self.comuptetest.get_token()
        print "\nToken:", ret
        self.assertTrue(ret)

    def test_get_token_expire(self):
        ret = self.comuptetest.get_token_expire()
        print "\nToken expire: ", ret
        self.assertTrue(ret)

    def test_get_endpoints(self):
        ret = self.comuptetest.get_endpoints()
        print "\nEndpoints: ", ret
        self.assertTrue(ret)

    def test_get_nodes(self):
        ret = self.comuptetest.get_nodes()
        print "\nNodes: \n", ret
        self.assertTrue(ret)

    def test_get_node(self):
        ret = self.comuptetest.get_node("test")
        print "\nNode:", ret
        self.assertTrue(ret)

#    def test_reboot_node(self):
#        node = self.comuptetest.get_node("test")
#        ret = self.comuptetest.get_node(node.uuid)
#        print "\nReboot:", ret
#
#    def test_delete_node(self):
#        node = self.comuptetest.get_node("test")
#        ret = self.comuptetest.delete_node(node.uuid)
#        print "\nDelete:", ret
#
#    def test_create_node(self):
#        compute_nodes = self.comuptetest.create_node("test", "Ubuntu 12.04 cloudimg amd64", "tiny", 2)
#        ret = self.comuptetest.get_node(node.uuid)
#        print "\nCreate:", ret
#        self.assertTrue(ret)
#
#    def test_get_private_ips(self):
#        node = self.comuptetest.get_node("ubuntu_small")
#        ret = self.comuptetest.get_private_ips(node.uuid)
#        print "PRIVATE_IP: \n", ret
#        self.assertTrue(ret)
#
#    def test_get_public_ips(self):
#        ret = self.comuptetest.get_public_ips()
#        print "PUBLIC_IP: \n", ret
#        self.assertTrue(ret)

if __name__ == "__main__":
    loader = TestLoader()
    tests = loader.loadTestsFromTestCase(StdTest)
    with TestDaemon():
        compute = TextTestRunner(verbosity=1).run(tests)
        sys.exit(compute.wasSuccessful())
