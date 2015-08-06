from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.common.openstack import OpenStackBaseConnection
from configParse import Parse

parser = Parse("properties.cfg") 
host = parser.get_value("HOST", "host")

auth_service = parser.get_value("AUTH", "auth_service")
compute_service = parser.get_value("COMPUTE", "compute_service")
image_service = parser.get_value("IMAGE", "image_service")

auth_admin = parser.get_value("AUTH", "auth_admin")
auth_ip = parser.get_value("AUTH", "auth_ip")
auth_port = parser.get_value("AUTH", "auth_port")
auth_admin_port = parser.get_value("AUTH", "auth_admin_port")
auth_servcie_name = parser.get_value("AUTH", "auth_service_name")
auth_password_version = parser.get_value("AUTH", "auth_password_version")
auth_token_version = parser.get_value("AUTH", "auth_token_version")

def libcloud_driver_password(username, password, project):
    Driver = get_driver(Provider.OPENSTACK)
    conn = Driver(username, password, host=host, port=8774, secure=False, ex_tenant_name=project, 
                    ex_force_auth_version='2.0_password', ex_force_service_name='Compute Service', 
                    ex_force_auth_url=auth_service, ex_force_service_region="RegionOne")
    return conn

def libcloud_driver_identity(username, password, project):
    Driver = get_driver(Provider.OPENSTACK)
    conn = Driver(username, password, host=auth_host, port=auth_port, secure=False, ex_tenant_name=project, 
                    ex_force_auth_version='2.0_password', ex_force_service_name='Identity Service', 
                    ex_force_auth_url=auth_service, ex_force_service_region="RegionOne")
    return conn

def libcloud_driver_token(username, password, project, token):
    Driver = get_driver(Provider.OPENSTACK)
    conn = Driver(username, password, host=host, port=8774, secure=False, ex_tenant_name=project, 
                    ex_force_auth_version='2.0', ex_force_service_name='Compute Service', 
                    ex_force_auth_url=auth_service, 
                    ex_force_base_url=compute_service+project,
                    ex_force_auth_token='{token}'.format(token=token))
    return conn

def libcloud_driver_token_image(username, password, project, token):
    Driver = get_driver(Provider.OPENSTACK)
    conn = Driver(username, password, host=host, port=9292, secure=False, ex_tenant_name=project, 
                    ex_force_auth_version='2.0', ex_force_service_name='Image Service', 
                    ex_force_auth_url=auth_service, 
                    ex_force_base_url=image_service+"b0e0f0aaabc44ebba254dfc1fd8e30ad/",
                    ex_force_auth_token='{token}'.format(token=token))
    return conn


    
def ec2_driver(): 
    print "EC2"
        
def native_driver(): 
    print "Native" 