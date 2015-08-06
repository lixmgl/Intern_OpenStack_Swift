# swiftstatsd #

It connects to swift service, pull the statistic information from swift and feeds it into statsd. Then statsd will
send it to graphite.

### Configuration ###

swiftstatsd sample config(/etc/swiftstats/swiftstatsd.conf):

    [main]
    #statsd host and port to connect too.
    #statsd_host = 127.0.0.1
    #statsd_port = 8125
    #swift service endpoint and user /passwd
    #swift_endpoint = https://10.100.18.149:5000/v2.0
    #swift_user = admin
    #swift_passwd = secrete
    #How often(seconds) to collect stats and send to statsd 
    #collect_interval = 10
    #orgniation  prefix will be added to the key of each event
    #org_prefix=cisco.swift
     
 log.conf config(/etc/swiftstats/log.conf):
 By default, the log file is under dir "/etc/swiftstats/logs". It needs 3 MB space for rotating logs.

 - Change "graphite_host" to your own graphite host
 - Change "swift_endpoint" to you own swift endpoint
 
 ### Installation ###
1. On puppet master server, copy all the directory  "puppet-module/swiftstats" to "/etc/puppet/modules";
2. Add the following line into the file "/etc/puppet/manifests/site.pp":
   include swiftstats
3. On puppet slave server, restart puppet agent to enforce the new module is reloaded.
 
### Event Types ###

The following events will be sent to statsd:

#### swift account usage ####

    cisco.swift.account_myaccount.num_of_bytes_used:1024|c
    cisco.swift.account_myaccount.num_of_containers:3|c
    cisco.swift.account_myaccount.container_container1.num_of_bytes_used:1024|c
    cisco.swift.account_myaccount.container_container1.num_of_objects:300|c
	cisco.swift.account_myaccount.quota:1234555|c
	cisco.swift.account_myaccount.container_container1.quota:44444|c
	

#### percentage ####

 	cisco.swift.account_myaccount.container_container1.space_percentage:14.4|c
 	cisco.swift.account_myaccount.space_percentage:23|c