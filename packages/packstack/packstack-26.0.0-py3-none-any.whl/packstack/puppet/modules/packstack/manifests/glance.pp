class packstack::glance ()
{
    create_resources(packstack::firewall, lookup('FIREWALL_GLANCE_RULES', undef, undef, {}))

    # glance option bind_host requires address without brackets
    $bind_host = lookup('CONFIG_IP_VERSION') ? {
      'ipv6'  => '::0',
      default => '0.0.0.0',
      # TO-DO(mmagr): Add IPv6 support when hostnames are used
    }

    $default_store = lookup('CONFIG_GLANCE_BACKEND') ? {
      'swift' => 'swift',
      default => 'file',
    }

    class { 'glance::api::authtoken':
      www_authenticate_uri => lookup('CONFIG_KEYSTONE_PUBLIC_URL_VERSIONLESS'),
      auth_url             => lookup('CONFIG_KEYSTONE_ADMIN_URL'),
      password             => lookup('CONFIG_GLANCE_KS_PW'),
    }

    class { 'glance::api::logging':
      debug => lookup('CONFIG_DEBUG_MODE'),
    }

    class { 'glance::api::db':
      database_connection => os_database_connection({
        'dialect'  => 'mysql+pymysql',
        'host'     => lookup('CONFIG_MARIADB_HOST_URL'),
        'username' => 'glance',
        'password' => lookup('CONFIG_GLANCE_DB_PW'),
        'database' => 'glance',
      })
    }

    class { 'glance::api':
      service_name     => 'httpd',
      enabled_backends => ["${default_store}:${default_store}", "http:http"],
      default_backend  => $default_store,
    }
    class { 'glance::wsgi::apache':
      bind_host => $bind_host,
      workers   => lookup('CONFIG_SERVICE_WORKERS'),
    }

    glance::backend::multistore::http { 'http': }
}
