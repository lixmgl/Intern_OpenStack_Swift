class csapi(csapi){
    package { 'csapi':
        ensure => present,
    }	
    file { '/opt/csapi':
        ensure => directory,
        recurse => true,
        mode => 0644,
        source => "puppet:///modules/csapi/conf/customized",
        before => File["csapi.vhost", "csapi.vhost"],
    }
    file { 'csapi.vhost':
        path => "/etc/apache2/sites-available/csapi.vhost",
        ensure => file,
        source => "puppet:///modules/csapi/conf/customized/csapi.vhost"
    }
}