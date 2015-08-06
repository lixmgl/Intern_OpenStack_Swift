'''
Created on Jul 18, 2012

@author: autumn
'''

from swiftconsole.common.utils import exec_command
from swiftconsole.ui.outputformatter import *
from swiftconsole.common.utils import exec_command_alone
import fileinput
import sys


import os
import sys
import shutil

"""
>>>>>>> .r509

class FileNotExist(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def __backup_file__(path):
    if os.path.isfile(path) == False:
        raise FileNotExist("File does not exist : %s" % path)
    
    bk_file = "%s.%d"
    shutil.copyfile(path, bk_file)
    return bk_file

def __print_ouput__(output):
    lines = output.split('\n')
    for line in lines:
        dict_obj = eval(line)
        for node, ret in dict_obj:
            ret_code = ret['retcode']
            if ret_code == 0:
                print "%s (OK) : %s" % (node, ret['output'])
            else:
                print "%s (ERR) : %s" % (node, ret['errors'])
"""

def __normalize_ret__(output, type='dict'):
    data = []
    if type == 'dict':
        obj = eval(output)
        for node, ret in obj.iteritems():
            _retcode = str(ret['retcode'])
            _output = '\n'.join([ret['output'], ret['errors']])
            line = [node, _retcode, _output]
            data.append(line)
    elif type == 'str':
        for line in output.split("\n"):
            if len(line) == 0:
                continue
            tmplist = line.split(":", 1)
            #print "tmplist = %r" % tmplist
            node = tmplist[0]
            ret = eval(tmplist[1])
            _retcode = str(ret['retcode'])
            _output = '\n'.join([ret['stdout'], ret['stderr']])
            line = [node, _retcode, _output]
            data.append(line)
    return data

#@tameem_update
def print_output_multiple(cmd):
    output = exec_command_alone(cmd)
    str1 = str(output)
    i = str1.splitlines()
    for part in i:
        type = part.partition(':')[0]
        type1 = repr(type)
        cmd = "salt %s puppet.run" % type1
        print_formatted_output(cmd)
     
        
#@tameem_update   
def print_formatted_output(cmd):
        data=[]
        retcode, output, errors, interval =exec_command([cmd])
        tmplist = output.split(':', 1)
        node = tmplist[0]
        obj = eval(tmplist[1])
        msg = obj['stdout']
        line1 = [node, str(retcode), msg]
        data.append(line1)
        title = ['node', 'status', 'message']
        width = 30, 7, 60
        formatter = OutputFormatter(data, title, width)
        formatter.print_dict()

#@tameem update
def replace_all(file1,searchExp,replaceExp):
    for line in fileinput.input(file1, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
            sys.stdout.write(line)



'''



        
#@tameem_update
def push_config(servertype):
    """
    Params:
      servertype: The server type which needs to run puppet refresh. It could be storage-node/proxy-node
    """
    if servertype == 'storagenode':
        cmd="salt -G 'servertype:swift-storagenode' test.ping"
        print_output_multiple(cmd)
    
    
    if servertype == 'proxy':
        cmd="salt -G 'servertype:swift-proxy' test.ping"
 
        print_output_multiple(cmd)

#@tameem_update
def push_ring():
    """
    Just run step 3 of rebuild_ring
    """
    cmd="salt -G 'servertype:swift-storagenode' test.ping"
    print_output_multiple(cmd)
    cmd="salt -G 'servertype:swift-proxy' test.ping"
    print_output_multiple(cmd)        
'''



def show_ring(ring):
    """
    Params:
        ring: The ring name, could be account/container/object
    """
    cmd = "salt -G 'servertype:swift-ringbuilder' ringinfor.%s_ring" % ring
    consolecmd = "show-ring %s" % ring
    __run_cmd_print__(cmd, consolecmd)

        

def push_config(servertype):
    """
    Params:
      servertype: The server type which needs to run puppet refresh. It could be storage-node/proxy-node
    """
    
    cmd = "salt -G 'servertype:swift-%s' puppet.run" % servertype
    consolecmd = "push-ring %s" % servertype
    __run_cmd_print__(cmd, consolecmd, 'str')
   
        
    
def rebuild_ring():
    """
    Multiple steps:
    1. Turn on the "enforce-rebuild" flag on puppet master server
    2. Send command to ringbuilder server to refresh puppet agent, so that it starts ring rebuilding
    3. Send command to all storage node and proxy node to refresh puppet agent
    """
    
    pass
    
    
    
    

def push_ring():
    """
    Just run step 3 of rebuild_ring
    """
    cmd="salt -G 'servertype:swift-storagenode' test.ping"
    print_output_multiple(cmd)
    cmd="salt -G 'servertype:swift-proxy' test.ping"
    print_output_multiple(cmd)
    
    
    

def rebalance_ring():
    """
    1. Turn on "enforce-rebalance" flag on puppet master
    2. Send command to ringbuilder server to refresh puppet agent, so that it starts ring rebuilding
    3. Send command to all storage node and proxy node to refresh puppet agent
    
    """
    
    
    cmd= "rm /etc/swift/enforce-rebalance "
    exec_command_alone(cmd)
    cmd="cp /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp.bk"
    exec_command_alone(cmd)
    try:    
        replace_all("/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp","$enforce_rebalance = 'no'","$enforce_rebalance = 'yes'")
        cmd= "puppet agent -t"
        __run_cmd_print__(cmd)
        replace_all("/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp","$enforce_rebalance = 'yes'","$enforce_rebalance = 'no'")
        
    except:
        cmd="cp /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp.bk /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
        exec_command_alone(cmd)
    
    finally:
        cmd="rm /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp.bk"
        exec_command_alone(cmd)
    
    push_ring()
        
        

def remove_device(devices):
    """
    Params:
      devices: The list of devices which we want to remove
      ['IP:PORT/sda6',.....]
      
    Steps:
      1. Add removed devices into "remove_devices.conf" on puppet master;
      2. Turn on "remove" flag on puppet master;
      3. Send command to ringbuilder server to refresh puppet agent, so that it starts ring rebuilding
      4. Send command to all storage node and proxy node to refresh puppet agent
    """
   
    for item in devices:
     cmd="salt -G 'servertype:swift-puppet-master'ring.remove_device_append(%s)"%item
     cmd="salt -G 'servertype:swift-puppet-master' ring.remove_device_config()"
    __run_cmd_print__(cmd)
    push_config('ringbuilder')
    push_ring()

def add_device(ring, devices):
    """
    Params:
      ring : object|container|account
      devices: The list of devices which we want to add into the ring
      ['IP:PORT/sda6',.....]
      
    Steps:
      1. Remove devices from "remove_devices.conf" on puppet master;
      2. Turn off "remove" flag on puppet master;
      3. Send command to ringbuilder server to refresh puppet agent, so that it starts ring rebuilding
      4. Send command to all storage node and proxy node to refresh puppet agent
    """
    
    for item in devices:
     cmd="salt -G 'servertype:swift-%s'ring.add_device_delete(%s)"%ring,item
     exec_command(cmd)
    cmd="salt -G 'servertype:swift-%s' ring.add_device_config()"%ring
    exec_command(cmd)
    push_config('ringbuilder')
    push_ring() 

def remove_storagenode(node):
    """
    Params:
        node : The hostname of the storage node which we are going to remove from ring
    steps:
    1. Remove node from puppet master
    2. Send command to ringbuilder server to refresh puppet agent, so that it starts ring rebuilding
    3. Send command to all storage node and proxy node to refresh puppet agent 
    """
    option="storagenode"
    remove_node(node,option,zone)
    push_config(ringbiulder)
    push_ring()
        
   

def __run_cmd_print__(cmd, consolecmd, rettype='dict'):
    """
    Params:
      cmd : The shell command line which will be run by python
      consolecmd : The console command line, which will show in result, i.e. "show-ring account"
      rettype : The return type of cmd.
        str : The result likes "node : {.....}"
        dict: The resule likes "{'node' : {.....}}"
    """
    
    retcode, output, errors, interval = exec_command(cmd)
    data = __normalize_ret__(output, rettype)

    title = ['node', 'retcode', 'message']
    width = (30, 10, 88)
    
    formatter = OutputFormatter(data,title, width, cmd=consolecmd)
    formatter.print_dict()
    
def add_storagenode(node, zone):
    """
    Params:
        node : The hostname of the storage node which we are going to adding into the ring
        zone: The zone which this server should be added to
    steps:
    1. Start the puppet agent on the node
    2. Add the storage node into the site.pp on puppet master
    3. Send command to ringbuilder server to refresh puppet agent, so that it starts ring rebuilding
    4. Send command to all storage node and proxy node to refresh puppet agent 
    """
   
   
    cmd = "salt'%s' service.restart puppet" % node
    __run_cmd_print__(cmd)
    option="storagenode"
    add_node(node,option,zone)
    push_config(ringbiulder)
    push_ring()
    
def add_proxy(node):
    """
    Params:
        node : The hostname of the proxy node which we are going to be added
    Steps:
    1. Add node into "site.pp" on puppet master
    2. Run "puppet agent -t" on the newly-added node
    """  
    pass

def remove_proxy(node):
    """
    Params:
        node : The hostname of the proxy node which we are going to be removed
    Steps:
    1. remove node into "site.pp" on puppet master
    """  
    pass


def node_status(servertype):
    """
    Params:
        servertype: Could be proxy-node/storage-node/all
    Steps:
    Gather type, process status information from each server and display
    """
    all_status(servertype,status)
    exec_command(cmd)
    
if __name__ == '__main__':
    show_ring('account')
    #show_ring('container')
    #show_ring('object')
    #"""
    #add_storagenode('ciswift004.webex.com')
    #push_config('proxy')
    push_config('storagenode')
    #push_ring()
    #"""
    

