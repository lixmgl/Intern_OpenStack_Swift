'''
Created on Jun 29, 2012
 
@author: autumn
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
 
##################################################################
# For testing
if __name__ == '__main__':
    #returncode, output, errors, interval = exec_command(['get_ring_device', 'account', '10.100.18.103'])
    #returncode, output, errors, interval = exec_command(["mount | grep '/srv/node' | awk '{print $1}' | awk -F\/ '{print $3}'"])
    #returncode, output, errors, interval = exec_command(["salt -G 'servertype:swift-storagenode' mount.active"])
    returncode, output, errors, interval = exec_command(["ls"])
    print "[%d] output: %s" % (returncode, output)
    """
    obj = eval(output)
    for node in obj.itekeys():
        print "[Node] : %s" % node
    """
 
