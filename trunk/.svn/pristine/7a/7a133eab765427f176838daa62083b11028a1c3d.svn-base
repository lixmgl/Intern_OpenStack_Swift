class cisco-mmonit {

    package { 'cisco-mmonit':
        ensure => installed,
    }

    file { '/etc/init.d/mmonit':
        ensure => 'present',
        source => 'puppet:///modules/cisco-mmonit/mmonit_rc',
        owner => 'root',
        group => 'root',
        mode => 754,
        require => [Package['cisco-mmonit']],
    }

    file { '/opt/mmonit/conf/server.xml':
        ensure => 'present',
        source => 'puppet:///modules/cisco-mmoint/server.xml',
        owner => 'root',
        group => 'root',
        mode => 644,
        require => [Package['cisco-mmonit']],
    }
}

