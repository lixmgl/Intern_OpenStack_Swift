'''
Set up the csapi integration test suite
'''

# Import Python libs
#import multiprocessing
import os
#import pwd
import sys
#import shutil
#import signal
#import subprocess

# Import csapi libs
from csapiunittest import TestCase

INTEGRATION_TEST_DIR = os.path.dirname(os.path.normpath(os.path.abspath(__file__)))
CODE_DIR = os.path.dirname(os.path.dirname(INTEGRATION_TEST_DIR))
SCRIPT_DIR = os.path.join(CODE_DIR, 'scripts')

PYEXEC = 'python{0}.{1}'.format(sys.version_info[0], sys.version_info[1])

TMP = os.path.join(INTEGRATION_TEST_DIR, 'tmp')
FILES = os.path.join(INTEGRATION_TEST_DIR, 'files')


class TestDaemon(object):
    '''
    Set up http, libcloud , and run related cases
    '''
    def __enter__(self):
        '''
        Start the env 
        '''
        return self

    def __exit__(self, type, value, traceback):
        '''
        Kill the env
        '''
#        self.sub_minion_process.terminate()
        self._clean()

    def _clean(self):
        '''
        Clean tmp files, etc
        '''
        print "Cleaning up"

