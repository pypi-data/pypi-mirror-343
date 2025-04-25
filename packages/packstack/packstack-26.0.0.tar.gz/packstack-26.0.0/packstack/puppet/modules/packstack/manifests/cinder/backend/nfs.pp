class packstack::cinder::backend::nfs ()
{
    ensure_packages(['nfs-utils'], {'ensure' => 'present'})

    cinder::backend::nfs { 'nfs':
      nfs_servers          => lookup('CONFIG_CINDER_NFS_MOUNTS', { merge => 'unique' }),
      require              => Package['nfs-utils'],
      nfs_shares_config    => '/etc/cinder/nfs_shares.conf',
      nfs_snapshot_support => true,
      manage_volume_type   => true,
    }
}
