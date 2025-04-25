class packstack::nova::sched ()
{
    include packstack::nova::cache
    include nova::scheduler::filter
    class { 'nova::scheduler':
      enabled => true,
    }

    Keystone_endpoint <||> -> Service['nova-scheduler']
    Keystone_service <||> -> Service['nova-scheduler']

}
