from jubilant.statustypes import (
    AppStatus,
    AppStatusRelation,
    CombinedStorage,
    ControllerStatus,
    EntityStatus,
    FilesystemAttachment,
    FilesystemAttachments,
    FilesystemInfo,
    FormattedBase,
    MachineStatus,
    ModelStatus,
    NetworkInterface,
    Status,
    StatusInfo,
    StorageAttachments,
    StorageInfo,
    UnitStatus,
    UnitStorageAttachment,
)

status = Status(
  model=ModelStatus(
    name='jubilant-afafde17',
    type='iaas',
    controller='github-pr-82dd9-lxd',
    cloud='localhost',
    version='3.6.21',
    region='localhost',
    model_status=StatusInfo(current='available', since='07 May 2026 07:20:20Z'),
  ),
  machines={
    '0': MachineStatus(
      juju_status=StatusInfo(current='started', since='07 May 2026 07:21:12Z', version='3.6.21'),
      hostname='juju-f4a349-0',
      dns_name='10.148.75.114',
      ip_addresses=['10.148.75.114'],
      instance_id='juju-f4a349-0',
      machine_status=StatusInfo(current='running', message='Running', since='07 May 2026 07:20:29Z'),
      modification_status=StatusInfo(current='applied', since='07 May 2026 07:20:29Z'),
      base=FormattedBase(name='ubuntu', channel='24.04'),
      network_interfaces={
        'eth0': NetworkInterface(
          ip_addresses=['10.148.75.114'],
          mac_address='00:16:3e:47:fe:09',
          is_up=True,
          gateway='10.148.75.1',
          space='alpha',
        ),
      },
      constraints='arch=amd64',
      hardware='arch=amd64 cores=0 mem=0M availability-zone=github-runner virt-type=container',
    ),
    '1': MachineStatus(
      juju_status=StatusInfo(current='started', since='07 May 2026 07:21:16Z', version='3.6.21'),
      hostname='juju-f4a349-1',
      dns_name='10.148.75.207',
      ip_addresses=['10.148.75.207'],
      instance_id='juju-f4a349-1',
      machine_status=StatusInfo(current='running', message='Running', since='07 May 2026 07:20:36Z'),
      modification_status=StatusInfo(current='applied', since='07 May 2026 07:20:35Z'),
      base=FormattedBase(name='ubuntu', channel='24.04'),
      network_interfaces={
        'eth0': NetworkInterface(
          ip_addresses=['10.148.75.207'],
          mac_address='00:16:3e:78:0b:3a',
          is_up=True,
          gateway='10.148.75.1',
          space='alpha',
        ),
      },
      constraints='arch=amd64',
      hardware='arch=amd64 cores=0 mem=0M availability-zone=github-runner virt-type=container',
    ),
    '2': MachineStatus(
      juju_status=StatusInfo(current='started', since='07 May 2026 07:21:13Z', version='3.6.21'),
      hostname='juju-f4a349-2',
      dns_name='10.148.75.116',
      ip_addresses=['10.148.75.116'],
      instance_id='juju-f4a349-2',
      machine_status=StatusInfo(current='running', message='Running', since='07 May 2026 07:20:36Z'),
      modification_status=StatusInfo(current='applied', since='07 May 2026 07:20:32Z'),
      base=FormattedBase(name='ubuntu', channel='24.04'),
      network_interfaces={
        'eth0': NetworkInterface(
          ip_addresses=['10.148.75.116'],
          mac_address='00:16:3e:15:73:19',
          is_up=True,
          gateway='10.148.75.1',
          space='alpha',
        ),
      },
      constraints='arch=amd64',
      hardware='arch=amd64 cores=0 mem=0M availability-zone=github-runner virt-type=container',
    ),
    '3': MachineStatus(
      juju_status=StatusInfo(current='started', since='07 May 2026 07:21:19Z', version='3.6.21'),
      hostname='juju-f4a349-3',
      dns_name='10.148.75.95',
      ip_addresses=['10.148.75.95'],
      instance_id='juju-f4a349-3',
      machine_status=StatusInfo(current='running', message='Running', since='07 May 2026 07:20:42Z'),
      modification_status=StatusInfo(current='applied', since='07 May 2026 07:20:37Z'),
      base=FormattedBase(name='ubuntu', channel='24.04'),
      network_interfaces={
        'eth0': NetworkInterface(
          ip_addresses=['10.148.75.95'],
          mac_address='00:16:3e:c1:15:87',
          is_up=True,
          gateway='10.148.75.1',
          space='alpha',
        ),
      },
      constraints='arch=amd64',
      hardware='arch=amd64 cores=0 mem=0M availability-zone=github-runner virt-type=container',
    ),
    '4': MachineStatus(
      juju_status=StatusInfo(current='started', since='07 May 2026 07:32:50Z', version='3.6.21'),
      hostname='juju-f4a349-4',
      dns_name='10.148.75.123',
      ip_addresses=['10.148.75.123'],
      instance_id='juju-f4a349-4',
      machine_status=StatusInfo(current='running', message='Running', since='07 May 2026 07:32:15Z'),
      modification_status=StatusInfo(current='applied', since='07 May 2026 07:32:13Z'),
      base=FormattedBase(name='ubuntu', channel='24.04'),
      network_interfaces={
        'eth0': NetworkInterface(
          ip_addresses=['10.148.75.123'],
          mac_address='00:16:3e:bc:e9:29',
          is_up=True,
          gateway='10.148.75.1',
          space='alpha',
        ),
      },
      constraints='arch=amd64',
      hardware='arch=amd64 cores=0 mem=0M availability-zone=github-runner virt-type=container',
    ),
    '5': MachineStatus(
      juju_status=StatusInfo(current='started', since='07 May 2026 07:43:25Z', version='3.6.21'),
      hostname='juju-f4a349-5',
      dns_name='10.148.75.12',
      ip_addresses=['10.148.75.12'],
      instance_id='juju-f4a349-5',
      machine_status=StatusInfo(current='running', message='Running', since='07 May 2026 07:42:42Z'),
      modification_status=StatusInfo(current='applied', since='07 May 2026 07:42:42Z'),
      base=FormattedBase(name='ubuntu', channel='24.04'),
      network_interfaces={
        'eth0': NetworkInterface(
          ip_addresses=['10.148.75.12'],
          mac_address='00:16:3e:24:44:82',
          is_up=True,
          gateway='10.148.75.1',
          space='alpha',
        ),
      },
      constraints='arch=amd64',
      hardware='arch=amd64 cores=0 mem=0M availability-zone=github-runner virt-type=container',
    ),
    '6': MachineStatus(
      juju_status=StatusInfo(current='started', since='07 May 2026 07:43:25Z', version='3.6.21'),
      hostname='juju-f4a349-6',
      dns_name='10.148.75.60',
      ip_addresses=['10.148.75.60'],
      instance_id='juju-f4a349-6',
      machine_status=StatusInfo(current='running', message='Running', since='07 May 2026 07:42:48Z'),
      modification_status=StatusInfo(current='applied', since='07 May 2026 07:42:44Z'),
      base=FormattedBase(name='ubuntu', channel='24.04'),
      network_interfaces={
        'eth0': NetworkInterface(
          ip_addresses=['10.148.75.60'],
          mac_address='00:16:3e:3e:c0:fc',
          is_up=True,
          gateway='10.148.75.1',
          space='alpha',
        ),
      },
      constraints='arch=amd64',
      hardware='arch=amd64 cores=0 mem=0M availability-zone=github-runner virt-type=container',
    ),
  },
  apps={
    'app': AppStatus(
      charm='local:application-0',
      charm_origin='local',
      charm_name='application',
      charm_rev=0,
      exposed=False,
      base=FormattedBase(name='ubuntu', channel='24.04'),
      app_status=StatusInfo(current='active', since='07 May 2026 07:32:56Z'),
      relations={
        'cluster': [
          AppStatusRelation(related_app='app', interface='cluster', scope='global'),
        ],
        'kafka-client-admin': [
          AppStatusRelation(related_app='kafka', interface='kafka_client', scope='global'),
        ],
      },
      units={
        'app/0': UnitStatus(
          workload_status=StatusInfo(current='active', since='07 May 2026 07:32:56Z'),
          juju_status=StatusInfo(current='idle', since='07 May 2026 08:13:10Z', version='3.6.21'),
          leader=True,
          machine='4',
          public_address='10.148.75.123',
        ),
      },
      endpoint_bindings={
        '': 'alpha',
        'cluster': 'alpha',
        'kafka-client-admin': 'alpha',
        'kafka-client-consumer': 'alpha',
        'kafka-client-producer': 'alpha',
        'kafka-client-v1': 'alpha',
      },
    ),
    'controller': AppStatus(
      charm='local:kafka-1',
      charm_origin='local',
      charm_name='kafka',
      charm_rev=1,
      exposed=False,
      base=FormattedBase(name='ubuntu', channel='24.04'),
      app_status=StatusInfo(current='active', message='machine system settings are not optimal - see logs for info', since='07 May 2026 08:14:36Z'),
      relations={
        'cluster': [
          AppStatusRelation(related_app='controller', interface='cluster', scope='global'),
        ],
        'peer-cluster': [
          AppStatusRelation(related_app='kafka', interface='peer_cluster', scope='global'),
        ],
        'refresh-v-three': [
          AppStatusRelation(related_app='controller', interface='refresh-v-three', scope='global'),
        ],
        'restart': [
          AppStatusRelation(related_app='controller', interface='rolling_op', scope='global'),
        ],
      },
      units={
        'controller/0': UnitStatus(
          workload_status=StatusInfo(current='active', message='machine system settings are not optimal - see logs for info', since='07 May 2026 08:14:37Z'),
          juju_status=StatusInfo(current='idle', since='07 May 2026 08:13:06Z', version='3.6.21'),
          leader=True,
          machine='3',
          open_ports=['9098/tcp'],
          public_address='10.148.75.95',
        ),
      },
      version='4.1.1',
      endpoint_bindings={
        '': 'alpha',
        'certificates': 'alpha',
        'client-cas': 'alpha',
        'cluster': 'alpha',
        'cos-agent': 'alpha',
        'kafka-client': 'alpha',
        'oauth': 'alpha',
        'peer-certificates': 'alpha',
        'peer-cluster': 'alpha',
        'peer-cluster-orchestrator': 'alpha',
        'refresh-v-three': 'alpha',
        'restart': 'alpha',
      },
    ),
    'kafka': AppStatus(
      charm='local:kafka-0',
      charm_origin='local',
      charm_name='kafka',
      charm_rev=0,
      exposed=False,
      base=FormattedBase(name='ubuntu', channel='24.04'),
      app_status=StatusInfo(
        current='maintenance',
        message='Apache Kafka cluster is scaling, it is advised to postpone potentially disruptive actions like refresh.',
        since='07 May 2026 08:18:51Z',
      ),
      relations={
        'cluster': [
          AppStatusRelation(related_app='kafka', interface='cluster', scope='global'),
        ],
        'kafka-client': [
          AppStatusRelation(related_app='app', interface='kafka_client', scope='global'),
        ],
        'peer-cluster-orchestrator': [
          AppStatusRelation(related_app='controller', interface='peer_cluster', scope='global'),
        ],
        'refresh-v-three': [
          AppStatusRelation(related_app='kafka', interface='refresh-v-three', scope='global'),
        ],
        'restart': [
          AppStatusRelation(related_app='kafka', interface='rolling_op', scope='global'),
        ],
      },
      units={
        'kafka/0': UnitStatus(
          workload_status=StatusInfo(
            current='maintenance',
            message='Apache Kafka cluster is scaling, it is advised to postpone potentially disruptive actions like refresh.',
            since='07 May 2026 08:12:45Z',
          ),
          juju_status=StatusInfo(current='idle', since='07 May 2026 08:36:22Z', version='3.6.21'),
          leader=True,
          machine='0',
          open_ports=['9092/tcp', '19093/tcp'],
          public_address='10.148.75.114',
        ),
        'kafka/1': UnitStatus(
          workload_status=StatusInfo(
            current='maintenance',
            message='Apache Kafka cluster is scaling, it is advised to postpone potentially disruptive actions like refresh.',
            since='07 May 2026 08:15:37Z',
          ),
          juju_status=StatusInfo(current='idle', since='07 May 2026 08:22:07Z', version='3.6.21'),
          machine='1',
          open_ports=['9092/tcp', '19093/tcp'],
          public_address='10.148.75.207',
        ),
        'kafka/2': UnitStatus(
          workload_status=StatusInfo(
            current='maintenance',
            message='Apache Kafka cluster is scaling, it is advised to postpone potentially disruptive actions like refresh.',
            since='07 May 2026 08:19:17Z',
          ),
          juju_status=StatusInfo(current='idle', since='07 May 2026 08:22:07Z', version='3.6.21'),
          machine='2',
          open_ports=['9092/tcp', '19093/tcp'],
          public_address='10.148.75.116',
        ),
        'kafka/3': UnitStatus(
          workload_status=StatusInfo(current='error', message='hook failed: "restart-relation-departed"', since='07 May 2026 08:12:05Z'),
          juju_status=StatusInfo(current='idle', since='07 May 2026 08:12:05Z', version='3.6.21'),
          machine='5',
          open_ports=['9092/tcp', '19093/tcp'],
          public_address='10.148.75.12',
        ),
        'kafka/4': UnitStatus(
          workload_status=StatusInfo(
            current='maintenance',
            message='Apache Kafka cluster is scaling, it is advised to postpone potentially disruptive actions like refresh.',
            since='07 May 2026 08:16:08Z',
          ),
          juju_status=StatusInfo(current='idle', since='07 May 2026 08:22:07Z', version='3.6.21'),
          machine='6',
          open_ports=['9092/tcp', '19093/tcp'],
          public_address='10.148.75.60',
        ),
      },
      version='4.1.1',
      endpoint_bindings={
        '': 'alpha',
        'certificates': 'alpha',
        'client-cas': 'alpha',
        'cluster': 'alpha',
        'cos-agent': 'alpha',
        'kafka-client': 'alpha',
        'oauth': 'alpha',
        'peer-certificates': 'alpha',
        'peer-cluster': 'alpha',
        'peer-cluster-orchestrator': 'alpha',
        'refresh-v-three': 'alpha',
        'restart': 'alpha',
      },
    ),
  },
  storage=CombinedStorage(
    storage={
      'data/0': StorageInfo(
        kind='filesystem',
        status=EntityStatus(current='attached', since='07 May 2026 07:21:14Z'),
        persistent=False,
        life='alive',
        attachments=StorageAttachments(
          units={
            'kafka/0': UnitStorageAttachment(machine='0', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/0', life='alive'),
          },
        ),
      ),
      'data/1': StorageInfo(
        kind='filesystem',
        status=EntityStatus(current='attached', since='07 May 2026 07:21:17Z'),
        persistent=False,
        life='alive',
        attachments=StorageAttachments(
          units={
            'kafka/1': UnitStorageAttachment(machine='1', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/1', life='alive'),
          },
        ),
      ),
      'data/2': StorageInfo(
        kind='filesystem',
        status=EntityStatus(current='attached', since='07 May 2026 07:21:15Z'),
        persistent=False,
        life='alive',
        attachments=StorageAttachments(
          units={
            'kafka/2': UnitStorageAttachment(machine='2', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/2', life='alive'),
          },
        ),
      ),
      'data/3': StorageInfo(
        kind='filesystem',
        status=EntityStatus(current='attached', since='07 May 2026 07:21:21Z'),
        persistent=False,
        life='alive',
        attachments=StorageAttachments(
          units={
            'controller/0': UnitStorageAttachment(machine='3', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/3', life='alive'),
          },
        ),
      ),
      'data/4': StorageInfo(
        kind='filesystem',
        status=EntityStatus(current='attached', since='07 May 2026 07:43:27Z'),
        persistent=False,
        life='alive',
      ),
      'data/5': StorageInfo(
        kind='filesystem',
        status=EntityStatus(current='attached', since='07 May 2026 07:43:27Z'),
        persistent=False,
        life='alive',
        attachments=StorageAttachments(
          units={
            'kafka/4': UnitStorageAttachment(machine='6', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/5', life='alive'),
          },
        ),
      ),
    },
    filesystems={
      '0/0': FilesystemInfo(
        size=98121,
        provider_id='0/0',
        storage='data/0',
        attachments=FilesystemAttachments(
          machines={
            '0': FilesystemAttachment(mount_point='/var/snap/charmed-kafka/common/var/lib/kafka/data/0', read_only=False, life='alive'),
          },
          units={
            'kafka/0': UnitStorageAttachment(machine='0', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/0', life='alive'),
          },
        ),
        pool='rootfs',
        life='alive',
        status=EntityStatus(current='attached', since='07 May 2026 07:21:14Z'),
      ),
      '1/1': FilesystemInfo(
        size=98121,
        provider_id='1/1',
        storage='data/1',
        attachments=FilesystemAttachments(
          machines={
            '1': FilesystemAttachment(mount_point='/var/snap/charmed-kafka/common/var/lib/kafka/data/1', read_only=False, life='alive'),
          },
          units={
            'kafka/1': UnitStorageAttachment(machine='1', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/1', life='alive'),
          },
        ),
        pool='rootfs',
        life='alive',
        status=EntityStatus(current='attached', since='07 May 2026 07:21:17Z'),
      ),
      '2/2': FilesystemInfo(
        size=98121,
        provider_id='2/2',
        storage='data/2',
        attachments=FilesystemAttachments(
          machines={
            '2': FilesystemAttachment(mount_point='/var/snap/charmed-kafka/common/var/lib/kafka/data/2', read_only=False, life='alive'),
          },
          units={
            'kafka/2': UnitStorageAttachment(machine='2', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/2', life='alive'),
          },
        ),
        pool='rootfs',
        life='alive',
        status=EntityStatus(current='attached', since='07 May 2026 07:21:15Z'),
      ),
      '3/3': FilesystemInfo(
        size=98121,
        provider_id='3/3',
        storage='data/3',
        attachments=FilesystemAttachments(
          machines={
            '3': FilesystemAttachment(mount_point='/var/snap/charmed-kafka/common/var/lib/kafka/data/3', read_only=False, life='alive'),
          },
          units={
            'controller/0': UnitStorageAttachment(machine='3', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/3', life='alive'),
          },
        ),
        pool='rootfs',
        life='alive',
        status=EntityStatus(current='attached', since='07 May 2026 07:21:21Z'),
      ),
      '5/4': FilesystemInfo(
        size=98121,
        provider_id='5/4',
        storage='data/4',
        attachments=FilesystemAttachments(
          machines={
            '5': FilesystemAttachment(mount_point='/var/snap/charmed-kafka/common/var/lib/kafka/data/4', read_only=False, life='alive'),
          },
        ),
        pool='rootfs',
        life='alive',
        status=EntityStatus(current='attached', since='07 May 2026 07:43:27Z'),
      ),
      '6/5': FilesystemInfo(
        size=98121,
        provider_id='6/5',
        storage='data/5',
        attachments=FilesystemAttachments(
          machines={
            '6': FilesystemAttachment(mount_point='/var/snap/charmed-kafka/common/var/lib/kafka/data/5', read_only=False, life='alive'),
          },
          units={
            'kafka/4': UnitStorageAttachment(machine='6', location='/var/snap/charmed-kafka/common/var/lib/kafka/data/5', life='alive'),
          },
        ),
        pool='rootfs',
        life='alive',
        status=EntityStatus(current='attached', since='07 May 2026 07:43:27Z'),
      ),
    },
  ),
  controller=ControllerStatus(timestamp='09:09:45Z'),
)
