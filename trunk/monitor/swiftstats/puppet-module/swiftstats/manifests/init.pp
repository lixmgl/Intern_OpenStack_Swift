class swiftstats{
	package { 'python-swiftstats':
      		ensure => present,
      		before => File['/etc/swiftstats'],
    	}	
	file { '/etc/swiftstats':
		ensure => directory,
		recurse => true,
		mode => 0644,
		source => "puppet:///modules/swiftstats/conf",	
	}
	file { '/var/log/swiftstats':
		ensure => directory,
                mode => 0644,
		before => Service['swiftstats'],
	}
	service { 'swiftstats':
      		ensure     => running,
      		enable     => true,
      		hasrestart => true,
      		hasstatus  => true,
      		subscribe  => File['/etc/swiftstats'],
    }
}

