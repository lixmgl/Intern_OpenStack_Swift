import os
import sys

if sys.version_info[0:2] < (2, 7):
    try:
        from unittest2 import TestLoader, TextTestRunner,\
                              TestCase, expectedFailure, \
                              TestSuite
    except ImportError:
        print("You need to install unittest2 to run the csapitests")
        sys.exit(1)
else:
    from unittest import TestLoader, TextTestRunner,\
                         TestCase, expectedFailure, \
                         TestSuite

# Set up paths
TEST_DIR = os.path.dirname(os.path.normpath(os.path.abspath(__file__)))
CSAPI_LIBS = os.path.dirname(TEST_DIR)

for dir_ in [TEST_DIR, CSAPI_LIBS]:
    if not dir_ in sys.path:
        sys.path.insert(0, dir_)

