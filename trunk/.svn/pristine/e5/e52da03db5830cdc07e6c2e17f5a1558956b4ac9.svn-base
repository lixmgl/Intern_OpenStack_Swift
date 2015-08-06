1. Introduction
   To prevent the DoS attack on openstack SSL ports, we need to install the traffic server in front of each service as the SSL reverse proxy.
   To support multiple ports in one server, multiple instances should be run.
   The archtecture likes the following:
   SSL on  10.100.18.135:5000 -----> /usr/local/trafficserver001  ---> 127.0.0.1:5001 (Application server)
   SSL on  10.100.18.135:6000 -----> /usr/local/trafficserver002  ---> 127.0.0.1:35358(Application server)

2. Installation
   Upload the package trafficserver001.tar.gz, trafficserver002.tar.gz to the target server under dir "/usr/local" and decompress them.

3. Configuration
   The two files need to be cofngiured:
   3.1. /usr/local/trafficserver001/etc/trafficserver/records.config
        The following items may need to be changed:
        CONFIG proxy.config.ssl.server_port INT 5000
        CONFIG proxy.config.ssl.server.cert.filename STRING ca.cer
        CONFIG proxy.config.ssl.server.private_key.filename STRING ca.key
        
   
   3.2. /usr/local/trafficserver001/etc/trafficserver/remap.config
        Add the remap rules as the following:
        map https://10.100.18.149:5000/ http://127.0.0.1:5001/
        reverse_map  http://127.0.0.1:5001/ https://10.100.18.149:5000/
      
4. Start/stop the service:
   /usr/local/trafficserver001/bin/trafficserver start|stop|restart
   /usr/local/trafficserver002/bin/trafficserver start|stop|restart
   Note: The restart command does not work!!! So please use start and stop to replace it.
   
   

