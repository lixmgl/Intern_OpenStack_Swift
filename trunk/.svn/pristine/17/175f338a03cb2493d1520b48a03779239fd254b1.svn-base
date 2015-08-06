class cisco-monit {

    package { 'cisco-monit':
        ensure => installed,
    }

    file { '/etc/init.d/monit':
        ensure => 'present',
        source => 'puppet:///modules/cisco-monit/monit_rc',
        owner => 'root',
        group => 'root',
        mode => 754,
        require => [Package['cisco-monit']],
    }

    file { '/opt/monit/etc/monitrc':
        ensure => 'present',
        source => 'puppet:///modules/cisco-monit/monitrc',
        owner => 'root',
        group => 'root',
        mode => 644,
        require => [Package['cisco-monit']],
    }
}

