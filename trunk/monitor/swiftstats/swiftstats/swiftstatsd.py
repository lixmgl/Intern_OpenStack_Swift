'''
Created on Mar 9, 2012

@author: autumn
'''

from swiftstats.daemonutils import Daemon, readconf
from swiftstats.storageserverstats import *
import logging.config
import optparse
import socket
import time
import sys
import os


class SwiftStatsServer:
    def __init__(self, conf):
        logging.config.fileConfig(conf.get("log_config", "/etc/swiftstats/log.conf"))
        self.logger = logging.getLogger("default")
        self.formatter = logging.Formatter('%(name)s: %(message)s')
        self.conf = conf
        self.statsd_host = conf.get('statsd_host', '127.0.0.1')
        self.statsd_port = int(conf.get('statsd_port', '8125'))
        self.swift_endpoint = conf.get('swift_endpoint', 'http://127.0.0.1/5000/v1.0')
        self.swift_user = conf.get('swift_user', 'admin')
        self.swift_passwd = conf.get('swift_passwd', 'secrete')
        self.account = self.swift_user
        self.collect_interval = int(conf.get('collect_interval', 10))
        self.org_prefix = conf.get('org_prefix', 'swiftstatsd')
        self.statsd_connection = None
        self.statsd_addr = (self.statsd_host, self.statsd_port)
        self.swift_connection = None
        self.swift_recon_endpoint = conf.get('swift_recon_endpoint', 'http://127.0.0.1:8080/recon')
        recon_endpoints_conf = conf.get('recon_endpoints', '/etc/swiftstats/recon_endpoints.conf')
        self.recon_endpoints = list()
        try:
            if os.path.exists(recon_endpoints_conf):
                f = open(recon_endpoints_conf, 'r')
                self.logger.debug("Config file opened")
                for line in f:
                    self.recon_endpoints.append(line.strip())
            else:
                self.logger.error("recon_endpoints_conf does not exist : %s" % recon_endpoints_conf)
        except Exception as e:
            self.logger.exception(e)
        
    def init_connections(self):
        if (self.statsd_connection == None):    
            self.statsd_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if(self.swift_connection == None):
            self.swift_connection = Connection(self.swift_endpoint, self.swift_user, self.swift_passwd)
            self.logger.debug("Connected to swift %s:%s@%s" % (self.swift_user, self.swift_passwd, self.swift_endpoint))
        
    def account_stats(self):
        ret = list()
        try:
            
            headers = self.swift_connection.head_account();
            #print("headers = %s" % str(headers))
            byte_used = int(headers['x-account-bytes-used'])
            num_of_containers = int(headers['x-account-container-count'])
            num_of_objs = int(headers['x-account-object-count'])
            diskusage = self.diskusage_stats(self.account)
            total_space = diskusage['total']
            usage_percent = (float(diskusage['used']) / total_space) * 100
            ret.append("%s.account_%s.byte_used:%d|g" % (self.org_prefix, self.account, byte_used))
            ret.append("%s.account_%s.num_of_containers:%d|g" % (self.org_prefix, self.account, num_of_containers))
            ret.append("%s.account_%s.num_of_objects:%d|g" % (self.org_prefix, self.account, num_of_objs))
            ret.append("%s.account_%s.total_space:%d|g" % (self.org_prefix, self.account, total_space))
            ret.append("%s.account_%s.diskusage_percent:%.5f|g" % (self.org_prefix, self.account, usage_percent))
        except Exception as err:
            self.logger.critical("Failed on call swift head_account : %s" % err)
        finally:
            return ret



    def get_containers(self):
        ret = list()
        try:
            (header, conList) = self.swift_connection.get_account()
            for con in conList:
                #print("container: %s" % str(con))
                ret.append(con['name'])
        except Exception as err:
            self.logger.critical("Failed on call client with get_account : %s" % err)
        finally:
            return ret
        
    def container_stats(self, container):
        ret = list()
        try:
            headers = self.swift_connection.head_container(container);
            byte_used = int(headers['x-container-bytes-used'])
            num_of_objs = int(headers['x-container-object-count'])
            ret.append("%s.account_%s.container_%s.byte_used:%d|g" % (self.org_prefix, self.account, container, byte_used))
            ret.append("%s.account_%s.container_%s.num_of_objects:%d|g" % (self.org_prefix, self.account, container, num_of_objs))
        except Exception as err:
            self.logger.critical("Failed on call client with head_container : %s" % err)
        finally:
            return ret
        
    def diskusage_stats(self, account):
        url = '/'.join([self.swift_recon_endpoint, 'diskusage', account])
        #self.logger.debug('URL = %s' % url)
        (parsed, conn) = http_connection(url)
        conn.request('GET', parsed.path, '', {})
        resp = conn.getresponse()
        resp_data = resp.read()
        #self.logger.debug('response = %s' % resp_data)
        usage = json.loads(resp_data)
        return usage


    def send_to_statsd(self, statList):
        for line in statList:
            self.logger.debug("Stat: [%s]" % line)
            self.statsd_connection.sendto(line, self.statsd_addr)

    def run(self):
        while(True):
            try:
                self.init_connections()
                self.send_to_statsd(self.account_stats())
                
                containerList = self.get_containers()
                for con in containerList:
                    containerStatsList = self.container_stats(con)
                    self.send_to_statsd(containerStatsList)

                sockStats = StorageServerStats(self.recon_endpoints, self.org_prefix, 'sockstat', self.logger)
                self.send_to_statsd(sockStats.stats())
                    
                memStats = MemStats(self.recon_endpoints, self.org_prefix, self.logger)
                self.send_to_statsd(memStats.stats())
                
                loadStats = LoadStats(self.recon_endpoints, self.org_prefix, self.logger)
                self.send_to_statsd(loadStats.stats())
                
                quarantinedStats = StorageServerStats(self.recon_endpoints, self.org_prefix, 'quarantined', self.logger)
                self.send_to_statsd(quarantinedStats.stats())
                
                asyncStats = StorageServerStats(self.recon_endpoints, self.org_prefix, 'async', self.logger)
                self.send_to_statsd(asyncStats.stats())
                
                replicationTimeStats = ReplicationTimeStats(self.recon_endpoints, self.org_prefix, self.logger)
                self.send_to_statsd(replicationTimeStats.stats())
                
                diskUsageStats = DiskusageStats(self.recon_endpoints, self.org_prefix, self.logger)
                self.send_to_statsd(diskUsageStats.stats())
                
            except Exception as err:
                self.logger.critical("Failed : %s" % err)
            finally:
                time.sleep(5)
            
class SwiftStatsd(Daemon):
    def run(self, conf):
        server = SwiftStatsServer(conf)
        server.run()
        
   
def run_server():
    usage = '''
    %prog start|stop|restart [--conf=/path/to/some.conf]
    '''
    args = optparse.OptionParser(usage)
    args.add_option('--foreground', '-f', action="store_true",
        help="Run in foreground")
    args.add_option('--conf', default="./swiftstatsd.conf",
        help="path to config. default = /etc/swiftstatsd/swiftstatsd.conf")
    options, arguments = args.parse_args()

    if len(sys.argv) <= 1:
        args.print_help()
        sys.exit(1)

    if not os.path.isfile(options.conf):
        print "Couldn't find a config"
        args.print_help()
        sys.exit(1)
        
    if options.foreground:
        print "Running in foreground."
        conf = readconf(options.conf)
        statsd = SwiftStatsServer(conf['main'])
        statsd.run()
        sys.exit(0)
        
    if len(sys.argv) >= 2:
        swiftstatsddaemon = SwiftStatsd('/var/run/swiftstatsd.pid')
        if 'start' == sys.argv[1]:
            conf = readconf(options.conf)
            swiftstatsddaemon.start(conf['main'])
        elif 'stop' == sys.argv[1]:
            swiftstatsddaemon.stop()
        elif 'restart' == sys.argv[1]:
            swiftstatsddaemon.restart()
        else:
            args.print_help()
            sys.exit(2)
        sys.exit(0)
    else:
        args.print_help()
        sys.exit(2)

if __name__ == '__main__':
    run_server()
     

    
