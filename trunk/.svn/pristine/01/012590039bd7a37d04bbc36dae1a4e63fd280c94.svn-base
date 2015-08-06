# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************

from keystoneclient.v2_0 import client
#import keystone.backends.api as db_api

def _format_tenant(tenant):
    return {
        "id": tenant.id,
        "name": tenant.name,
        "description": tenant.description,
        "enabled": tenant.enabled
    }
    
def _format_user(user):
    return {
        "id": user.id,
        "name": user.name,
        "enabled": user.enabled,
        "tenant_id": user.tenantId
    }
    
def _format_role(role):
    return {
        "id": role.id,
        "name": role.name
    }
   
def auth(usr=None, passwd=None, url=None, api="NATIVE", token_id=None, tenant_id=None, tenant_name=None, admin=False, admin_url=None, cache=None):
    if api == "NATIVE":
        keystone = client.Client(username=usr, password=passwd, tenant_name=tenant_name, tenant_id=tenant_id, token=token_id, auth_url=url)
        
        return keystone

def get_token(keystone, usr=None, passwd=None, api="NATIVE", tenant_id=None, tenant_name=None, token_id=None):
    if api == "NATIVE":
        token = keystone.tokens.authenticate(username=usr, password=passwd, tenant_id=tenant_id, tenant_name=tenant_name, token=token_id)
        
        return token
        
def get_tenant_token(keystone, token, tenant_id):
    token = keystone.tokens.authenticate(token=token, tenant_id=tenant_id)
    return token

def list_tenants(keystone, api="NATIVE"):
     if api == "NATIVE":
        tenants = []
        for tenant in keystone.tenants.list():
            tenants.append(_format_tenant(tenant))
        return tenants
            
def create_tenant(keystone, name, description, api="NATIVE"):
    if api == "NATIVE":
        return _format_tenant(keystone.tenants.create(name, description, enabled=True))
        
def delete_tenant(keystone, id, api="NATIVE"):
    if api == "NATIVE":
        remove_tenant_users(keystone, id)
        keystone.tenants.delete(id)
        
def update_tenant(keystone, id, name, description, enabled, api="NATIVE"):
    if api == "NATIVE":
        return _format_tenant(keystone.tenants.update(id, name, description, enabled))
        
def get_tenant(keystone, id, api="NATIVE"):
    if api == "NATIVE":
        return _format_tenant(keystone.tenants.get(id))
        
def disable_tenant(keystone, id, api="NATIVE"):
    if api == "NATIVE":
        tenant = get_tenant(keystone, id, api="NATIVE")
        if tenant.get('enabled'):
            return _format_tenant(keystone.tenants.update(tenant.get('id'), tenant.get('name'), tenant.get('description'), enabled=False))
        
def enable_tenant(keystone, id, api="NATIVE"):
    if api == "NATIVE":
        tenant = get_tenant(keystone, id, api="NATIVE")
        if not tenant.get('enabled'):
            return _format_tenant(keystone.tenants.update(tenant.get('id'), tenant.get('name'), tenant.get('description'), enabled=False))

def list_users(keystone, tenant_id=None, api="NATIVE"):
    if api == "NATIVE":
        users = []
        for user in keystone.users.list(tenant_id):
            users.append(_format_user(user))
        return users

def get_user(keystone, id, api="NATIVE"):
    if api == "NATIVE":
        return _format_user(keystone.users.get(id))
    
def delete_user(keystone, id, api="NATIVE"):
    if api == "NATIVE":
        keystone.users.delete(id)
        
def update_user(keystone, id, name, tenant_id, password="", email="", api="NATIVE"):
    if api == "NATIVE":
        if len(password) > 0:
            update_user_password(keystone, id, password)
        return _format_user(keystone.users.update(id, {'name': name, 'enabled': enabled, 'email': email}))

def create_user(keystone, name, password, email="", tenant_id=None, enabled=True, api="NATIVE"):
    if api == "NATIVE":
        return _format_user(keystone.users.create(name, password, email, tenant_id, enabled))
    
def update_user_password(keystone, id, password, api="NATIVE"):
    if api == "NATIVE":
        return _format_user(keystone.users.update_password(id, password))
    
def update_user_tenant(keystone, id, tenant_id, api="NATIVE"):
    if api == "NATIVE":
        return _format_user(keystone.users.update_tenant(id, tenant_id))
    
def enable_user(keystone, id, api="NATIVE"):
    if api == "NATIVE":
        return _format_user(keystone.users.update_enabled(user_id, enabled=True))
    
def disable_user(keystone, id, api="NATIVE"):
    if api == "NATIVE":
        return _format_user(keystone.users.update_enabled(user_id, enabled=False))
    
def list_roles(keystone, api="NATIVE"):
    if api == "NATIVE":
        roles = []
        for role in keystone.roles.list():
            roles.append(_format_role(role))
        return roles
    
def add_tenant_user(keystone, tenant_id, user, role=None):
    keystone.tenants.add_user(tenant_id, user, role)

def add_tenant_user_role(keystone, tenant_id, user_id, role_id, api="NATIVE"):
    if api == "NATIVE":
        return _format_role(keystone.roles.add_user_role(user_id, role_id, tenant_id))

def remove_tenant_user(keystone, tenant_id, user_id, api="NATIVE"):
    if api == "NATIVE":
        roles = keystone.roles.roles_for_user(user_id, tenant_id)
        for role in roles:
            keystone.roles.remove_user_role(user_id, role.id, tenant_id)
            
def remove_tenant_users(keystone, tenant_id, api="NATIVE"):
    if api == "NATIVE":
        users = list_users(keystone, tenant_id)
        for user in users:
            remove_tenant_user(keystone, tenant_id, user.get(id))