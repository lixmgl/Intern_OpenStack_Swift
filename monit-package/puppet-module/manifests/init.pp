class monit($server_type){
#	$server_type="keystone"
	package { 'monit':
      		ensure => present,
      		before => Package['msendclient'],
    	}	
	package { 'msendclient':
		ensure => present,
		before => File['/etc/monit'],
	}
	file { '/etc/monit':
		ensure => directory,
		recurse => true,
		mode => 0644,
		source => "puppet:///modules/monit/conf/common",
		before => File["monitrc", "customized-monitrc"],
	}
	file { 'monitrc':
		path => "/etc/monit/monitrc",
		ensure => file,
		content => template("monit/monitrc.erb"),
	}
	file { 'customized-monitrc':
		path => "/etc/monit/conf.d/$server_type.rc",
		ensure => file,
		source => "puppet:///modules/monit/conf/customized/$server_type.rc"
	}
	service { 'monit':
     		ensure     => running,
      		enable     => true,
      		hasrestart => true,
      		hasstatus  => true,
      		subscribe  => File['/etc/monit','monitrc', 'customized-monitrc'],
    }
}

