# Copyright (c) – 2016, Edward Balduf. All rights reserved.
class packstack::cinder::backend::solidfire ()
{
    $solidfire_backend_name = 'solidfire'

    cinder::backend::solidfire { $solidfire_backend_name :
      san_ip              => lookup('CONFIG_CINDER_SOLIDFIRE_LOGIN'),
      san_login           => lookup('CONFIG_CINDER_SOLIDFIRE_PASSWORD'),
      san_password        => lookup('CONFIG_CINDER_SOLIDFIRE_HOSTNAME'),
      volume_backend_name => $solidfire_backend_name,
      manage_volume_type  => true,
    }

    ensure_packages(['iscsi-initiator-utils'], {'ensure' => 'present'})
}
