class cisco-collectd {

    package { 'cisco-collectd':
        ensure => installed,
    }

    package { 'cisco-collectd-plugins':
        ensure => installed,
    }

    file { '/etc/init.d/collectd':
        ensure => 'present',
        source => 'puppet:///modules/cisco-collectd/collectd_rc',
        owner => 'root',
        group => 'root',
        mode => 754,
        require => [Package['cisco-collectd']],
    }

    file { '/opt/collectd/etc/collectd.conf':
        ensure => 'present',
        source => 'puppet:///modules/cisco-collectd/collectd.conf',
        owner => 'root',
        group => 'root',
        mode => 644,
        require => [Package['cisco-collectd']],
    }
}

