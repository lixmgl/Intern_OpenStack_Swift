# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
from libcloud.compute.drivers.dummy import DummyNodeDriver
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment
from libcloud.compute.base import NodeAuthPassword
from libcloud.compute.base import NodeAuthSSHKey
import os
import time

class ComputeNodes(object):    
    """Constructor for the compute driver connection"""
    def __init__(self, conn): 
        self.conn = conn 
        
    def get_token(self): 
        """Get auth token""" 
        #this is a hack to get the token.  a token will not be returned until some 
        #method is called on the driver.
        self.conn.list_nodes()
        return self.conn.connection.auth_token
    
    def get_token_expire(self): 
        """Get auth expire date""" 
        self.conn.list_nodes()
        return self.conn.connection.auth_token_expires
    
    def get_endpoints(self): 
        """Get endpoints""" 
        self.conn.list_nodes()
        return self.conn.connection.service_catalog
    
    def get_nodes(self):    
        """returns a list of all nodes assigned to tenant"""
        return self.conn.list_nodes()
    
    def get_private_ips(self, node):    
        """Return a list of private IPs from 'node'""" 
        return node.private_ips
    
    def get_public_ips(self, node):    
        """Return a list of private IPs from 'node'""" 
        return node.public_ips
    
    def get_node(self, search):    
        """searh by node name|uuid|ip returning first instance 
        of the 'node' found"""
        nodes = self.conn.list_nodes() 
        i = 0; 
        while i < len(nodes):
            if search == nodes[i].name:
                return nodes[i] 
            elif search == nodes[i].uuid:
                return nodes[i] 
            elif search in nodes[i].private_ips:
                return nodes[i] 
            elif search in nodes[i].public_ips:
                return nodes[i] 
            i += 1 
        
    def delete_node(self, node):
        """Delete a 'node'.  Returns True on success"""
        return node.destroy()
    
    def create_node(self, name, image, size, keyname):    
        """Create a 'node'.  Returns a node object on success"""
        if keyname: 
            return self.conn.create_node(name=name, image=image, size=size, ex_keyname=keyname)
        else:
            return self.conn.create_node(name=name, image=image, size=size)
    
    def deploy_node(self, name, image, size, pubkey):    
        """Create a 'node'.  Returns a node object on success"""
        s = ScriptDeployment('echo "nameserver 4.2.2.1" >> /etc/resolv.conf')
        s1 = ScriptDeployment('yum -y install httpd')
        s2 = ScriptDeployment('service httpd start')
        msd = MultiStepDeployment([SSHKeyDeployment(pubkey), s, s1, s2])
        
        return self.conn.deploy_node(name=name, image=image, size=size, deploy=msd, ssh_password="boxgrinder")
    
    def reboot_node(self, node):
        """Reboot a 'node'. Returns True on success"""
        return node.reboot() 