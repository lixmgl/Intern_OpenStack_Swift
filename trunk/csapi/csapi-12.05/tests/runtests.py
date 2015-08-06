#!/usr/bin/env python
'''
Discover all instances of unittest.TestCase in this directory.
'''
# Import python libs
import sys
import os
import optparse

import csapiunittest
from integration import TestDaemon

try:
    import xmlrunner
except ImportError:
    pass

TEST_DIR = os.path.dirname(os.path.normpath(os.path.abspath(__file__)))
PNUM = 50

def run_suite(opts, path, display_name, suffix='[!_]*.py'):
    '''
    Execute a unit test suite
    '''
    loader = csapiunittest.TestLoader()
    if opts.name:
        tests = loader.loadTestsFromName(opts.name)
    else:
        tests = loader.discover(path, suffix, TEST_DIR)
    print('~' * PNUM)
    print('Starting {0} Tests'.format(display_name))
    print('~' * PNUM)
    if opts.xmlout:
        runner = xmlrunner.XMLTestRunner(output='test-reports').run(tests)
    else:
        runner = csapiunittest.TextTestRunner(
            verbosity=opts.verbosity).run(tests)
    return runner.wasSuccessful()


def run_integration_suite(opts, suite_folder, display_name):
    '''
    Run an integration test suite
    '''
    path = os.path.join(TEST_DIR, 'integration', suite_folder)
    return run_suite(opts, path, display_name)


def run_integration_tests(opts):
    '''
    Execute the integration tests suite
    '''
    print('~' * PNUM)
    print('Setting csapi to execute tests')
    print('~' * PNUM)
    status = []
    if not any([opts.compute, opts.auth, opts.image,
                opts.storage]):
        return status
    with TestDaemon():
        if opts.name:
            results = run_suite(opts, '', opts.name)
            status.append(results)
        if opts.compute:
            status.append(run_integration_suite(opts, 'compute', 'Compute'))
        if opts.auth:
            status.append(run_integration_suite(opts, 'auth', 'Auth'))
        if opts.image:
            status.append(run_integration_suite(opts, 'image', 'Image'))
        if opts.storage:
            status.append(run_integration_suite(opts, 'storage', 'Storage'))
    return status

def run_unit_tests(opts):
    '''
    Execute the unit tests
    '''
    if not opts.unit:
        return [True]
    status = []
    results = run_suite(
        opts, os.path.join(TEST_DIR, 'unit'), 'Unit', '*_test.py')
    status.append(results)
    return status

def parse_opts():
    '''
    Parse command line options for running specific tests
    '''
    parser = optparse.OptionParser()
    parser.add_option('-c',
            '--compute',
            '--compute-tests',
            dest='compute',
            default=False,
            action='store_true',
            help='Run tests for compute')
    parser.add_option('-a',
            '--auth',
            '--auth-tests',
            dest='auth',
            default=False,
            action='store_true',
            help='Run tests for auth')
    parser.add_option('-i',
            '--image',
            '--image-tests',
            dest='image',
            default=False,
            action='store_true',
            help='Run tests for image')
    parser.add_option('-s',
            '--storage',
            dest='storage',
            default=False,
            action='store_true',
            help='Run storage tests')
    parser.add_option('-v', 
            '--verbose',
            dest='verbosity',
            default=1,
            action='count',
            help='Verbose output')
    parser.add_option('-x',
            '--xml',
            dest='xmlout',
            default=False,
            action='store_true',
            help='XML output')
    parser.add_option('-n',
            '--name',
            dest='name',
            default='',
            help='Specific test name to run')

    options, _ = parser.parse_args()
    if not any((options.compute, options.auth,
                options.image, options.storage)):
        options.compute = True
        options.auth = True
        options.image = True
        options.storage = True
        options.runner = True
    return options


if __name__ == '__main__':
    opts = parse_opts()
    overall_status = []
    status = run_integration_tests(opts)
    overall_status.extend(status)
#    status = run_unit_tests(opts)
#    overall_status.extend(status)
    false_count = overall_status.count(False)
    if false_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)
