class cisco-graphite {

    package { 'cisco-ceres':
        ensure => installed,
    }

    package { 'cisco-whisper':
        ensure => installed,
    }

    package { 'cisco-graphite':
        ensure => installed,
    }

    package { 'mysql-server':
        ensure => installed,
    }

    package { 'apache2':
        ensure => installed,
    }

    service { 'apache2':
        ensure => 'running',
        enable => 'true',
        require => Package['apache2'],
    }

    service { 'mysql':
        ensure => 'running',
        enable => 'true',
        require => Package['mysql-server'],
    }

    file { '/etc/init.d/graphite':
        ensure => 'present',
        source => 'puppet:///modules/cisco-graphite/graphite_rc',
        owner => 'root',
        group => 'root',
        mode => 754,
        require => [Package['cisco-graphite']],
    }

    file { '/opt/graphite/bin/graphite_finish.bash':
        ensure => 'present',
        source => 'puppet:///modules/cisco-graphite/graphite_finish.bash',
        owner => 'root',
        group => 'root',
        mode => 750,
        require => [Package['cisco-graphite']],
    }

    file { '/opt/graphite/conf/carbon.conf':
        ensure => 'present',
        source => 'puppet:///modules/cisco-graphite/carbon.conf',
        owner => 'root',
        group => 'root',
        mode => 644,
        require => [Package['cisco-graphite']],
    }

    file { '/opt/graphite/conf/graphite.wsgi':
        ensure => 'present',
        source => 'puppet:///modules/cisco-graphite/graphite.wsgi',
        owner => 'root',
        group => 'root',
        mode => 644,
        require => [Package['cisco-graphite']],
    }

    file { '/opt/graphite/conf/stoage-schemas.conf':
        ensure => 'present',
        source => 'puppet:///modules/cisco-graphite/storage-schemas.conf',
        owner => 'root',
        group => 'root',
        mode => 644,
        require => [Package['cisco-graphite']],
    }

    file { '/etc/apache2/sites-available/graphite':
        notify => Service['apache2'],
        ensure => 'present',
        source => 'puppet:///modules/cisco-graphite/graphite.vhost',
        owner => 'www-data',
        group => 'www-data',
        mode => 644,
        require => [Package['apache2'], Package['cisco-graphite']],
    }
}

