'''
Created on Jul 18, 2012

@author: Tameem
'''

import time
import subprocess as sub

def exec_command(param_list):
    """
    Execute a command:
      @param param_list: ['cmd param1 param2']
    """
    s_time = time.time()
    p = sub.Popen(param_list, stdout = sub.PIPE, stderr = sub.PIPE, shell=True)
    output, errors = p.communicate()
    p.wait()
    e_time  = time.time()
    interval = e_time - s_time
    return (p.returncode, output, errors, interval)

def exec_command_alone(param_list):
    """
    Execute a command:
      @param param_list: ['cmd param1 param2']
    """
    s_time = time.time()
    p = sub.Popen(param_list, stdout = sub.PIPE, stderr = sub.PIPE, shell=True)
    output, errors = p.communicate()
    p.wait()
    e_time  = time.time()
    interval = e_time - s_time
    return (output)

########################################################################
# Testing
"""
if __name__ == '__main__':
    #cmd = "swift-ring-builder /etc/swift/account.builder"
    cmd = "salt 'ciswift001.webex.com' puppet.run"
    retcode, output, errors, interval = exec_command([cmd])
    print "retcode : %d \noutput: \n%r" % (retcode, output)
    
    tmplist = output.split(':', 1)
    node = tmplist[0]
    obj = eval(tmplist[1])
    print "node : %s " % node
    #print "obj : %r" % obj
    for k, v in obj.iteritems():
        print "%s : %s" % (k, str(v))
"""

