'''
Created on Jul 23, 2012

@author: autumn
'''

import os
import sys
import shutil
import fileinput
from swiftconsole.common.utils import exec_command
from swiftconsole.ui.outputformatter import *
from swiftconsole.common.utils import exec_command_alone


#update_replace a line in a particular file
def replace_all(file1,searchExp,replaceExp):
    for line in fileinput.input(file1, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
            sys.stdout.write(line)
        
            
            
'''
def turn_on_rebalance():
    """
    1. Turn on "enforce-rebalance" flag on puppet master
    2. Send command to ringbuilder server to refresh puppet agent, so that it starts ring rebuilding
    3. Send command to all storage node and proxy node to refresh puppet agent
    
    """
    cmd= "rm /etc/swift/enforce-rebalance"
    exec_command_alone(cmd)
    cmd="cp /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp.bk"
    exec_command_alone(cmd)
    try:    
        replace_all("/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp","$enforce_rebalance = 'no'","$enforce_rebalance = 'yes'")
        cmd= "puppet agent -t"
        exec_command(cmd)
        replace_all("/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp","$enforce_rebalance = 'yes'","$enforce_rebalance = 'no'")
    except:
        cmd="cp /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp.bk /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
        exec_command_alone(cmd)
    finally:
        cmd="rm /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp.bk"
        exec_command_alone(cmd)
    
  '''
            

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

def turn_on_flag(item):
    """
    Turn on rebalance flag on puppet master server in file "/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
    """
    
    
    ring_config_file = "/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
    bk_file = __backup_file__(ring_config_file)
    
    try:
        f = open(ring_config_file, 'rb')
        tmp_str = f.read()
        f.close()
        
        
        if item == "rebalance":
            tmp_str = tmp_str.replace("$enforce_rebalance = 'no'", "$enforce_rebalance = 'yes'")
    
        
        if item == "remove":
            tmp_str = tmp_str.replace("$enable_node_remove = 'no'", "$enable_node_remove = 'yes'")
        
        
        f = open(ring_config_file, 'wb')
        f.write(tmp_str)
        f.close()
    
    except:
        cmd="cp bk_file /etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
        exec_command(cmd) 
        
    finally :
        os.remove(bk_file)
    
def turn_off_flag(item):
    """
    Turn off rebalance flag on puppet master server in file "/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
    """
    ring_config_file = "/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
    bk_file = __backup_file__(ring_config_file)
    
    f = open(ring_config_file, 'rb')
    tmp_str = f.read()
    f.close()
    
    if item =="rebalance":  
        tmp_str = tmp_str.replace("$enforce_rebalance = 'yes'", "$enforce_rebalance = 'no'")
        
    if item =="remove":
        tmp_str = tmp_str.replace("$enable_node_remove = 'yes'", "$enable_node_remove = 'no'")
        
    
    f = open(ring_config_file, 'wb')
    f.write(tmp_str)
    f.close()
    
    os.remove(bk_file)
    

    
def ring_rebalance():
    try:
        cmd= "rm /etc/swift/enforce-rebalance"
        exec_command_alone(cmd)
    except FileNotExist:
        
        print"File does not exist : %s" % cmd
        continue
    
    try:
        turn_on_rebalance()
    except FileNotExist:
        print "Sorry that file does not exist"
        sys.exit(1)
            
    cmd= "puppet agent -t"
    exec_command(cmd)       
    
    try:
        turn_off_rebalance()
    except FileNotExist:
        print" sorry this file does not exist"
        sys.exit(1)      


__proxy_node_cfg__ = """
node '%s' {
  class {'openstack::swift_base':
    swift_shared_secret => $swift_shared_secret
  }
  class { 'openstack::swift_proxy':
    swift_local_net_ip => $swift_local_net_ip,
    auth_host => $keystone_auth,
    db_host => $db_host,
  }
}
"""

__storage_node_cfg__ = """
node '%s' {
  class {'openstack::swift_base':
    swift_shared_secret => $swift_shared_secret
  }
  class {'openstack::swift_storage':
    swift_zone => %d,
    swift_local_net_ip => $swift_local_net_ip
  }
}
"""

    
def add_node(node, servertype, zone=0):
    """
    Add node into /etc/puppet/manifests/site.pp 
    Param:
      node : Host name
      servertype: storagenode | proxy
    """
    if servertype == 'proxy':
        cfg = __proxy_node_cfg__ % node
    elif servertype == 'storagenode':
        cfg = __storage_node_cfg__ % (node, zone)
    
    site_cfg = "/etc/puppet/manifests/site.pp"
    bk_file = __backup_file__(site_cfg)
    
    f = open(site_cfg, 'a')
    f.write(cfg)
    f.close()
    
    os.remove(bk_file)
    

def remove_node(node, servertype, zone=0):
    """
    Remove node from /etc/puppet/manifests/site.pp 
    Param:
      node : Host name
      servertype: storagenode | proxy
    """
    if servertype == 'proxy':
        cfg = __proxy_node_cfg__ % node
    elif servertype == 'storagenode':
        cfg = __storage_node_cfg__ % (node, zone)
    
    site_cfg = "/etc/puppet/manifests/site.pp"
    bk_file = __backup_file__(site_cfg)
    
    f = open(site_cfg, 'rb')
    tmpstr = f.read()
    f.close()
    
    tmpstr.replace(cfg, '')
    
    f = open(site_cfg, 'wb')
    f.write(tmpstr)
    f.close()
    
    os.remove(bk_file)   

            
 
def remove_device_append(item):
    
    remove_config_file="/etc/puppet/modules/openstack/files/remove-devices.conf"
    bk_file = __backup_file__(remove_config_file)
    tmp_str = item
    f = open(remove_config_file, 'a')
    f.write(tmp_str)
    f.close()
    
    os.remove(bk_file) 
    
          
def remove_device_config():
    
    try:
        turn_on_remove()
    except FileNotExist:
        print "Sorry that file does not exist"
    
    cmd= "puppet agent -t"
    exec_command(cmd)       
    
    try:
        turn_off_remove()
    except FileNotExist:
        print" sorry this file does not exist"
               
def add_device_delete(item):
    
    remove_config_file="/etc/puppet/modules/openstack/files/add-devices.conf"
    bk_file = __backup_file__(add_config_file)
    tmp_str = item
    delete_devices(remove_config_file,item)
    os.remove(bk_file) 
    
    
          
def add_device_config():
    
    try:
         turn_off_flag("remove")
    except FileNotExist:
        print "Sorry that file does not exist"
    
    cmd= "puppet agent -t"
    exec_command(cmd)       
         
        
def delete_devices(file,item):
    f=open(file,"r")
    lines=f.readlines()
    f.close()
    f=open(file,"w")
    for line in lines:
        if line!=item:
            f.write(line)
    f.close()
    
def all_status(names,status):
    data = {}
    data['container-server'] = 'container-replicator'
    data['container-server'] = 'container-updator'
    data['container-server'] = 'container-auditor'
    data['container-server'] = 'container-sync'
    data['account-server'] = 'container-replicator'
    data['account-server'] = 'container-auditor'
    data['account-server'] = 'container-reaper'
    data['object-server'] = 'container-replicator'
    data['object-server'] = 'container-updator'
    data['object-server'] = 'container-auditor'
    
for key, value in data.iteritems():
    print "%s:%s" % (key, value)
    
def netstatus():            
            
        
            