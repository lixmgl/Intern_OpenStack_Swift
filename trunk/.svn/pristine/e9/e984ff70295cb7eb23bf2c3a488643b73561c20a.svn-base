# ********************************************************************   
# *        Copyright (c) 2009-2012 Cisco Systems, Inc.   
# *        All rights reserved.   
# ********************************************************************
import web
import json
import driver
import worker
import compute
import image

urls = (
    "", "computeWebIndex",
    "/(.*)", "computeWeb"
)

class computeWebIndex(object):
    def GET(self):
        raise web.seeother('/')

class computeWeb(object):
    def format_node(self, node):
        if len(node.private_ips) < 1:
            return {
                "uuid": node.uuid,
                "host": "nova5",
                "name": node.name,
                "state": node.state,
                "private": "",
                "public": "",
                "console": "<a href=http://10.100.18.144:6080/vnc_auto.html?token=384a8cf2-9cc4-4c17-bb5e-32ee6bba9b5b&amp;title=chad_centos(33660365-b3d5-4dbe-aff6-acb578da8155)  target='_blank'> Console </a>",
                "dashboard": "<a href=/portal/charts/ target='_blank'> Dashboard </a>",
            }
        if len(node.private_ips) < 2:
            return {
                "uuid": node.uuid,
                "host": "nova5",
                "name": node.name,
                "state": node.state,
                "private": node.private_ips[0],
                "public": "",
                "console": "<a href=http://10.100.18.144:6080/vnc_auto.html?token=384a8cf2-9cc4-4c17-bb5e-32ee6bba9b5b&amp;title=chad_centos(33660365-b3d5-4dbe-aff6-acb578da8155)  target='_blank'> Console </a>",
                "dashboard": "<a href=/portal/charts/ target='_blank'> Dashboard </a>",
            }
        else:
            return {
                "uuid": node.uuid,
                "host": "nova5",
                "name": node.name,
                "state": node.state,
                "private": node.private_ips[0],
                "public": node.private_ips[1],
                "console": "<a href=http://10.100.18.144:6080/vnc_auto.html?token=384a8cf2-9cc4-4c17-bb5e-32ee6bba9b5b&amp;title=chad_centos(33660365-b3d5-4dbe-aff6-acb578da8155)  target='_blank'> Console </a>",
                "dashboard": "<a href=/portal/charts/ target='_blank'> Dashboard </a>",
            }
    def GET(self, tenant_id=''):
        i=0
        nodes = []
        auth_token = web.ctx.get('environ').get('HTTP_X_AUTH_TOKEN', None)
        auth_tenant_id = web.ctx.get('environ').get('HTTP_X_AUTH_TENANT_ID', None)
        conn = driver.libcloud_driver_token(None, None, auth_tenant_id, auth_token)
        compute_nodes = compute.ComputeNodes(conn)
        node = compute_nodes.get_nodes()
        
        while i < len(node):
            nodes.append(self.format_node(node[i]))
            i += 1

        if conn is None:
            return web.unauthorized()
       
        body = json.dumps(nodes, indent=4)
        web.header("Content-Type", "application/json")
        return body 
        
    def POST(self, Compute):
        creds = json.loads(web.data())
        name = creds.get('Compute').get('name')
        tenant_id = creds.get('Compute').get('tenant_id') 
        username = creds.get('Compute').get('username')
        password = creds.get('Compute').get('password')
        count = creds.get('Compute').get('count')
        os = creds.get('Compute').get('image')
        flavor = creds.get('Compute').get('flavor')
        send_auth = creds.get('Compute').get('auth_key')
        token = creds.get('Compute').get('token') 
        if token is None: 
            conn = driver.libcloud_driver_token(None, None, tenant_id, token)
        else: 
            conn = driver.libcloud_driver_password(username, password, tenant_id)
        compute_nodes = compute.ComputeNodes(conn)
        image_nodes = image.ComputeImages(conn)
        nodes = compute_nodes.get_nodes()  
        imageList = image_nodes.get_images() 
        sizeList = image_nodes.get_sizes() 
        send_size = image_nodes.get_size(flavor) 
        send_image = image_nodes.get_image(os) 

        i = 0 
        w = worker.WorkerQueue() 
        w.start()

        while i < int(count): 
            w.send(compute_nodes.create_node(name, send_image, send_size, send_auth))
            i += 1
        w.close() 
        
    def DELETE(self, Compute):
        print "delete..."
        creds = json.loads(web.data())
        
        node_search = creds.get('Compute').get('node')
        tenant_id = creds.get('Compute').get('tenant_id') 
        username = creds.get('Compute').get('username')
        password = creds.get('Compute').get('password')
        token = creds.get('Compute').get('token') 
        
        if token is None: 
            conn = driver.libcloud_driver_token(None, None, tenant_id, token)
        else: 
            conn = driver.libcloud_driver_password(username, password, tenant_id)
            
        compute_nodes = compute.ComputeNodes(conn)
        nodes = compute_nodes.get_nodes()  
        node = compute_nodes.get_node(node_search)  
        
        w = worker.WorkerQueue() 
        w.start()
        i = 0
        
        while i < len(nodes): 
            if node_search == nodes[i].name:
                w.send(compute_nodes.delete_node(nodes[i]))
            elif node_search == nodes[i].uuid:
                w.send(compute_nodes.delete_node(nodes[i]))
            elif node_search in nodes[i].private_ips:
                w.send(compute_nodes.delete_node(nodes[i]))
            elif node_search in nodes[i].public_ips:
                w.send(compute_nodes.delete_node(nodes[i]))
            i += 1
            
        w.close() 
        
    def PUT(self, Compute):
        creds = json.loads(web.data())
        
        node_search = creds.get('Compute').get('node')
        tenant_id = creds.get('Compute').get('tenant_id') 
        username = creds.get('Compute').get('username')
        password = creds.get('Compute').get('password')
        token = creds.get('Compute').get('token') 
        if token is None: 
            conn = driver.libcloud_driver_token(None, None, tenant_id, token)
        else: 
            conn = driver.libcloud_driver_password(username, password, tenant_id)
        compute_nodes = compute.ComputeNodes(conn)
        nodes = compute_nodes.get_nodes()  
        node = compute_nodes.get_node(node_search)  
        
        w = worker.WorkerQueue() 
        w.start()
        i = 0
        
        while i < len(nodes): 
            if node_search == nodes[i].name:
                w.send(compute_nodes.reboot_node(nodes[i]))
            elif node_search == nodes[i].uuid:
                w.send(compute_nodes.reboot_node(nodes[i]))
            elif node_search in nodes[i].private_ips:
                w.send(compute_nodes.reboot_node(nodes[i]))
            elif node_search in nodes[i].public_ips:
                w.send(compute_nodes.reboot_node(nodes[i]))
            i += 1
            
        w.close() 

app_compute = web.application(urls, locals())
