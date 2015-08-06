class statsdpy{
	package { 'python-statsdpy':
      		ensure => present,
      		before => File['/etc/statsdpy'],
    	}	
	file { '/etc/statsdpy':
		ensure => directory,
		recurse => true,
		mode => 0644,
		source => "puppet:///modules/statsdpy/conf",	
	}
	file { '/var/log/statsdpy':
		ensure => directory,
                mode => 0644,
		before => Service['statsdpy'],
	}
	service { 'statsdpy':
      		ensure     => running,
      		enable     => true,
      		hasrestart => true,
      		hasstatus  => true,
      		subscribe  => File['/etc/statsdpy'],
    }
}

