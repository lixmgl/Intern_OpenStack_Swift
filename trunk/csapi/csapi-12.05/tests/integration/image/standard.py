import sys
from csapiunittest import TestLoader, TextTestRunner
from image import ComputeNodes 
import unittest2
import integration
from integration import TestDaemon

class StdTest(unittest2.TestCase):
    def setUp(self):
        unittest2.TestCase.setUp(self)
        self.testclass = ComputeNodes()

    def tearDown(self):
        unittest2.TestCase.tearDown(self)
        self.testclass.close()

    def test_get_junk(self):
        ret = self.testclass.get_junk()
        self.assertTrue(ret)

    def test_set_junk(self):
        ret = self.testclass.set_junk()
        self.assertTrue(ret)

if __name__ == "__main__":
    loader = TestLoader()
    tests = loader.loadTestsFromTestCase(StdTest)
    print('Setting up environment')
    with TestDaemon():
        auth = TextTestRunner(verbosity=1).run(tests)
        sys.exit(auth.wasSuccessful())
