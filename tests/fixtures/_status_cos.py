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
    ModelStatus,
    OfferStatus,
    RemoteAppStatus,
    RemoteEndpoint,
    Status,
    StatusInfo,
    StorageAttachments,
    StorageInfo,
    UnitStatus,
    UnitStorageAttachment,
    VolumeAttachment,
    VolumeAttachments,
    VolumeInfo,
)

status = Status(
    model=ModelStatus(
        name="cos",
        type="caas",
        controller="k8s",
        cloud="microk8s",
        version="3.6.11",
        region="localhost",
        model_status=StatusInfo(current="available", since="14 Mar 2026 06:59:00+01:00"),
    ),
    machines={},
    apps={
        "alertmanager": AppStatus(
            charm="alertmanager-k8s",
            charm_origin="charmhub",
            charm_name="alertmanager-k8s",
            charm_rev=180,
            exposed=False,
            base=FormattedBase(name="ubuntu", channel="20.04"),
            charm_channel="1/edge",
            charm_version="6c6907f",
            scale=1,
            provider_id="77d6093e-debd-4eef-8f32-7ab33b7c1af7",
            address="10.152.183.94",
            app_status=StatusInfo(current="active", since="17 Dec 2025 07:12:13+01:00"),
            relations={
                "alerting": [
                    AppStatusRelation(
                        related_app="loki", interface="alertmanager_dispatch", scope="global"
                    ),
                    AppStatusRelation(
                        related_app="prometheus", interface="alertmanager_dispatch", scope="global"
                    ),
                ],
                "catalogue": [
                    AppStatusRelation(
                        related_app="catalogue", interface="catalogue", scope="global"
                    ),
                ],
                "grafana-dashboard": [
                    AppStatusRelation(
                        related_app="grafana", interface="grafana_dashboard", scope="global"
                    ),
                ],
                "grafana-source": [
                    AppStatusRelation(
                        related_app="grafana", interface="grafana_datasource", scope="global"
                    ),
                ],
                "ingress": [
                    AppStatusRelation(related_app="traefik", interface="ingress", scope="global"),
                ],
                "replicas": [
                    AppStatusRelation(
                        related_app="alertmanager", interface="alertmanager_replica", scope="global"
                    ),
                ],
                "self-metrics-endpoint": [
                    AppStatusRelation(
                        related_app="prometheus", interface="prometheus_scrape", scope="global"
                    ),
                ],
            },
            units={
                "alertmanager/0": UnitStatus(
                    workload_status=StatusInfo(
                        current="active", since="17 Dec 2025 07:12:13+01:00"
                    ),
                    juju_status=StatusInfo(
                        current="idle", since="25 Mar 2026 14:15:03+01:00", version="3.6.11"
                    ),
                    leader=True,
                    address="10.1.81.37",
                    provider_id="alertmanager-0",
                ),
            },
            version="0.27.0",
            endpoint_bindings={
                "": "alpha",
                "alerting": "alpha",
                "catalogue": "alpha",
                "certificates": "alpha",
                "grafana-dashboard": "alpha",
                "grafana-source": "alpha",
                "ingress": "alpha",
                "karma-dashboard": "alpha",
                "remote-configuration": "alpha",
                "replicas": "alpha",
                "self-metrics-endpoint": "alpha",
                "tracing": "alpha",
            },
        ),
        "catalogue": AppStatus(
            charm="catalogue-k8s",
            charm_origin="charmhub",
            charm_name="catalogue-k8s",
            charm_rev=87,
            exposed=False,
            base=FormattedBase(name="ubuntu", channel="20.04"),
            charm_channel="1/edge",
            scale=1,
            provider_id="97787760-33bd-47d6-abd2-6bc8c2b407b1",
            address="10.152.183.214",
            app_status=StatusInfo(current="active", since="14 Mar 2026 06:59:09+01:00"),
            relations={
                "catalogue": [
                    AppStatusRelation(
                        related_app="alertmanager", interface="catalogue", scope="global"
                    ),
                    AppStatusRelation(related_app="grafana", interface="catalogue", scope="global"),
                    AppStatusRelation(
                        related_app="prometheus", interface="catalogue", scope="global"
                    ),
                ],
                "ingress": [
                    AppStatusRelation(related_app="traefik", interface="ingress", scope="global"),
                ],
                "replicas": [
                    AppStatusRelation(
                        related_app="catalogue", interface="catalogue_replica", scope="global"
                    ),
                ],
            },
            units={
                "catalogue/0": UnitStatus(
                    workload_status=StatusInfo(
                        current="active", since="31 Jan 2026 07:21:32+01:00"
                    ),
                    juju_status=StatusInfo(
                        current="idle", since="25 Mar 2026 14:14:56+01:00", version="3.6.11"
                    ),
                    leader=True,
                    address="10.1.81.39",
                    provider_id="catalogue-0",
                ),
            },
            endpoint_bindings={
                "": "alpha",
                "catalogue": "alpha",
                "catalogue-item": "alpha",
                "certificates": "alpha",
                "ingress": "alpha",
                "replicas": "alpha",
                "tracing": "alpha",
            },
        ),
        "grafana": AppStatus(
            charm="grafana-k8s",
            charm_origin="charmhub",
            charm_name="grafana-k8s",
            charm_rev=160,
            exposed=False,
            base=FormattedBase(name="ubuntu", channel="20.04"),
            charm_channel="1/edge",
            charm_version="rev151-8-g6624bd3",
            scale=1,
            provider_id="b59215fa-1384-4aa7-a976-fd276175f4ce",
            address="10.152.183.200",
            app_status=StatusInfo(current="active", since="24 Feb 2026 09:17:39+01:00"),
            relations={
                "catalogue": [
                    AppStatusRelation(
                        related_app="catalogue", interface="catalogue", scope="global"
                    ),
                ],
                "grafana": [
                    AppStatusRelation(
                        related_app="grafana", interface="grafana_peers", scope="global"
                    ),
                ],
                "grafana-dashboard": [
                    AppStatusRelation(
                        related_app="alertmanager", interface="grafana_dashboard", scope="global"
                    ),
                    AppStatusRelation(
                        related_app="loki", interface="grafana_dashboard", scope="global"
                    ),
                    AppStatusRelation(
                        related_app="prometheus", interface="grafana_dashboard", scope="global"
                    ),
                ],
                "grafana-source": [
                    AppStatusRelation(
                        related_app="alertmanager", interface="grafana_datasource", scope="global"
                    ),
                    AppStatusRelation(
                        related_app="loki", interface="grafana_datasource", scope="global"
                    ),
                    AppStatusRelation(
                        related_app="prometheus", interface="grafana_datasource", scope="global"
                    ),
                ],
                "ingress": [
                    AppStatusRelation(
                        related_app="traefik", interface="traefik_route", scope="global"
                    ),
                ],
                "metrics-endpoint": [
                    AppStatusRelation(
                        related_app="prometheus", interface="prometheus_scrape", scope="global"
                    ),
                ],
                "replicas": [
                    AppStatusRelation(
                        related_app="grafana", interface="grafana_replicas", scope="global"
                    ),
                ],
            },
            units={
                "grafana/0": UnitStatus(
                    workload_status=StatusInfo(
                        current="active", since="24 Feb 2026 09:17:39+01:00"
                    ),
                    juju_status=StatusInfo(
                        current="idle", since="25 Mar 2026 14:20:12+01:00", version="3.6.11"
                    ),
                    leader=True,
                    address="10.1.81.33",
                    provider_id="grafana-0",
                ),
            },
            version="9.5.21",
            endpoint_bindings={
                "": "alpha",
                "catalogue": "alpha",
                "certificates": "alpha",
                "charm-tracing": "alpha",
                "database": "alpha",
                "grafana": "alpha",
                "grafana-auth": "alpha",
                "grafana-dashboard": "alpha",
                "grafana-metadata": "alpha",
                "grafana-source": "alpha",
                "ingress": "alpha",
                "metrics-endpoint": "alpha",
                "oauth": "alpha",
                "profiling-endpoint": "alpha",
                "receive-ca-cert": "alpha",
                "replicas": "alpha",
                "workload-tracing": "alpha",
            },
        ),
        "loki": AppStatus(
            charm="loki-k8s",
            charm_origin="charmhub",
            charm_name="loki-k8s",
            charm_rev=207,
            exposed=False,
            base=FormattedBase(name="ubuntu", channel="20.04"),
            charm_channel="1/edge",
            charm_version="rev197-5-g5a125e58",
            scale=1,
            provider_id="c254889a-2882-44f6-bd97-499e506b173a",
            address="10.152.183.126",
            app_status=StatusInfo(current="active", since="12 Feb 2026 17:21:40+01:00"),
            relations={
                "alertmanager": [
                    AppStatusRelation(
                        related_app="alertmanager",
                        interface="alertmanager_dispatch",
                        scope="global",
                    ),
                ],
                "grafana-dashboard": [
                    AppStatusRelation(
                        related_app="grafana", interface="grafana_dashboard", scope="global"
                    ),
                ],
                "grafana-source": [
                    AppStatusRelation(
                        related_app="grafana", interface="grafana_datasource", scope="global"
                    ),
                ],
                "ingress": [
                    AppStatusRelation(
                        related_app="traefik", interface="ingress_per_unit", scope="global"
                    ),
                ],
                "metrics-endpoint": [
                    AppStatusRelation(
                        related_app="prometheus", interface="prometheus_scrape", scope="global"
                    ),
                ],
                "replicas": [
                    AppStatusRelation(related_app="loki", interface="loki_replica", scope="global"),
                ],
            },
            units={
                "loki/0": UnitStatus(
                    workload_status=StatusInfo(
                        current="active", since="12 Feb 2026 17:21:40+01:00"
                    ),
                    juju_status=StatusInfo(
                        current="idle", since="25 Mar 2026 14:15:28+01:00", version="3.6.11"
                    ),
                    leader=True,
                    address="10.1.81.63",
                    provider_id="loki-0",
                ),
            },
            version="2.9.15",
            endpoint_bindings={
                "": "alpha",
                "alertmanager": "alpha",
                "catalogue": "alpha",
                "certificates": "alpha",
                "charm-tracing": "alpha",
                "grafana-dashboard": "alpha",
                "grafana-source": "alpha",
                "ingress": "alpha",
                "logging": "alpha",
                "metrics-endpoint": "alpha",
                "replicas": "alpha",
                "send-datasource": "alpha",
                "workload-tracing": "alpha",
            },
        ),
        "prometheus": AppStatus(
            charm="prometheus-k8s",
            charm_origin="charmhub",
            charm_name="prometheus-k8s",
            charm_rev=247,
            exposed=False,
            base=FormattedBase(name="ubuntu", channel="20.04"),
            charm_channel="1/edge",
            charm_version="24d374c",
            scale=1,
            provider_id="8b427d61-ef8f-4229-ba60-015cc1cbb2e2",
            address="10.152.183.137",
            app_status=StatusInfo(current="active", since="26 Jan 2026 14:11:59+01:00"),
            relations={
                "alertmanager": [
                    AppStatusRelation(
                        related_app="alertmanager",
                        interface="alertmanager_dispatch",
                        scope="global",
                    ),
                ],
                "catalogue": [
                    AppStatusRelation(
                        related_app="catalogue", interface="catalogue", scope="global"
                    ),
                ],
                "grafana-dashboard": [
                    AppStatusRelation(
                        related_app="grafana", interface="grafana_dashboard", scope="global"
                    ),
                ],
                "grafana-source": [
                    AppStatusRelation(
                        related_app="grafana", interface="grafana_datasource", scope="global"
                    ),
                ],
                "ingress": [
                    AppStatusRelation(
                        related_app="traefik", interface="ingress_per_unit", scope="global"
                    ),
                ],
                "metrics-endpoint": [
                    AppStatusRelation(
                        related_app="alertmanager", interface="prometheus_scrape", scope="global"
                    ),
                    AppStatusRelation(
                        related_app="grafana", interface="prometheus_scrape", scope="global"
                    ),
                    AppStatusRelation(
                        related_app="loki", interface="prometheus_scrape", scope="global"
                    ),
                    AppStatusRelation(
                        related_app="traefik", interface="prometheus_scrape", scope="global"
                    ),
                ],
                "prometheus-peers": [
                    AppStatusRelation(
                        related_app="prometheus", interface="prometheus_peers", scope="global"
                    ),
                ],
            },
            units={
                "prometheus/0": UnitStatus(
                    workload_status=StatusInfo(
                        current="active", since="26 Jan 2026 14:11:59+01:00"
                    ),
                    juju_status=StatusInfo(
                        current="idle", since="25 Mar 2026 14:19:57+01:00", version="3.6.11"
                    ),
                    leader=True,
                    address="10.1.81.47",
                    provider_id="prometheus-0",
                ),
            },
            version="2.52.0",
            endpoint_bindings={
                "": "alpha",
                "alertmanager": "alpha",
                "catalogue": "alpha",
                "certificates": "alpha",
                "charm-tracing": "alpha",
                "grafana-dashboard": "alpha",
                "grafana-source": "alpha",
                "ingress": "alpha",
                "metrics-endpoint": "alpha",
                "prometheus-api": "alpha",
                "prometheus-peers": "alpha",
                "receive-remote-write": "alpha",
                "self-metrics-endpoint": "alpha",
                "send-datasource": "alpha",
                "workload-tracing": "alpha",
            },
        ),
        "traefik": AppStatus(
            charm="traefik-k8s",
            charm_origin="charmhub",
            charm_name="traefik-k8s",
            charm_rev=254,
            exposed=False,
            base=FormattedBase(name="ubuntu", channel="20.04"),
            charm_channel="latest/stable",
            charm_version="1ec7fcb",
            can_upgrade_to="ch:amd64/traefik-k8s-281",
            scale=1,
            provider_id="8b9d908a-9f40-40c0-bfee-19560c857454",
            address="10.152.183.155",
            app_status=StatusInfo(
                current="active",
                message="Serving at http://10.160.219.1",
                since="08 May 2026 11:20:41+02:00",
            ),
            relations={
                "ingress": [
                    AppStatusRelation(
                        related_app="alertmanager", interface="ingress", scope="global"
                    ),
                    AppStatusRelation(related_app="catalogue", interface="ingress", scope="global"),
                ],
                "ingress-per-unit": [
                    AppStatusRelation(
                        related_app="loki", interface="ingress_per_unit", scope="global"
                    ),
                    AppStatusRelation(
                        related_app="prometheus", interface="ingress_per_unit", scope="global"
                    ),
                ],
                "metrics-endpoint": [
                    AppStatusRelation(
                        related_app="prometheus", interface="prometheus_scrape", scope="global"
                    ),
                ],
                "peers": [
                    AppStatusRelation(
                        related_app="traefik", interface="traefik_peers", scope="global"
                    ),
                ],
                "traefik-route": [
                    AppStatusRelation(
                        related_app="grafana", interface="traefik_route", scope="global"
                    ),
                ],
            },
            units={
                "traefik/0": UnitStatus(
                    workload_status=StatusInfo(
                        current="active",
                        message="Serving at http://10.160.219.1",
                        since="08 May 2026 11:20:41+02:00",
                    ),
                    juju_status=StatusInfo(
                        current="idle", since="25 Mar 2026 14:19:57+01:00", version="3.6.11"
                    ),
                    leader=True,
                    address="10.1.81.35",
                    provider_id="traefik-0",
                ),
            },
            version="2.11.0",
            endpoint_bindings={
                "": "alpha",
                "certificates": "alpha",
                "charm-tracing": "alpha",
                "experimental-forward-auth": "alpha",
                "grafana-dashboard": "alpha",
                "ingress": "alpha",
                "ingress-per-unit": "alpha",
                "logging": "alpha",
                "metrics-endpoint": "alpha",
                "peers": "alpha",
                "receive-ca-cert": "alpha",
                "traefik-route": "alpha",
                "upstream-ingress": "alpha",
                "workload-tracing": "alpha",
            },
        ),
        "yra": AppStatus(
            charm="hydra",
            charm_origin="charmhub",
            charm_name="hydra",
            charm_rev=395,
            exposed=False,
            base=FormattedBase(name="ubuntu", channel="22.04"),
            charm_channel="latest/edge",
            can_upgrade_to="ch:amd64/hydra-401",
            scale=1,
            provider_id="f897e228-3ad4-4519-8885-d01e274dcddc",
            address="10.152.183.59",
            app_status=StatusInfo(
                current="blocked",
                message="Missing integration pg-database",
                since="08 May 2026 11:19:09+02:00",
            ),
            relations={
                "hydra": [
                    AppStatusRelation(related_app="yra", interface="hydra_peers", scope="global"),
                ],
            },
            units={
                "yra/0": UnitStatus(
                    workload_status=StatusInfo(
                        current="blocked",
                        message="Missing integration pg-database",
                        since="08 May 2026 11:19:09+02:00",
                    ),
                    juju_status=StatusInfo(
                        current="idle", since="25 Mar 2026 14:15:05+01:00", version="3.6.11"
                    ),
                    leader=True,
                    address="10.1.81.24",
                    provider_id="yra-0",
                ),
            },
            version="v2.3.0",
            endpoint_bindings={
                "": "alpha",
                "grafana-dashboard": "alpha",
                "hydra": "alpha",
                "hydra-endpoint-info": "alpha",
                "hydra-token-hook": "alpha",
                "internal-route": "alpha",
                "logging": "alpha",
                "metrics-endpoint": "alpha",
                "oauth": "alpha",
                "pg-database": "alpha",
                "public-route": "alpha",
                "tracing": "alpha",
                "ui-endpoint-info": "alpha",
            },
        ),
    },
    app_endpoints={
        "data-oauth-integrator": RemoteAppStatus(
            url="lxd:admin/doi.data-oauth-integrator",
            endpoints={
                "hydra-token-hook": RemoteEndpoint(interface="hydra_token_hook", role="provider"),
            },
            life="dead",
            app_status=StatusInfo(
                current="terminated",
                message="offer has been removed",
                since="18 Jan 2026 09:16:58+01:00",
            ),
        ),
    },
    offers={
        "alertmanager-karma-dashboard": OfferStatus(
            app="alertmanager",
            endpoints={
                "karma-dashboard": RemoteEndpoint(interface="karma_dashboard", role="provider"),
            },
            charm="ch:amd64/alertmanager-k8s-180",
        ),
        "grafana-dashboards": OfferStatus(
            app="grafana",
            endpoints={
                "grafana-dashboard": RemoteEndpoint(interface="grafana_dashboard", role="requirer"),
            },
            charm="ch:amd64/grafana-k8s-160",
            total_connected_count=1,
            active_connected_count=1,
        ),
        "loki-logging": OfferStatus(
            app="loki",
            endpoints={
                "logging": RemoteEndpoint(interface="loki_push_api", role="provider"),
            },
            charm="ch:amd64/loki-k8s-207",
            total_connected_count=1,
            active_connected_count=1,
        ),
        "prometheus-receive-remote-write": OfferStatus(
            app="prometheus",
            endpoints={
                "receive-remote-write": RemoteEndpoint(
                    interface="prometheus_remote_write", role="provider"
                ),
            },
            charm="ch:amd64/prometheus-k8s-247",
            total_connected_count=1,
            active_connected_count=1,
        ),
        "traefik": OfferStatus(
            app="traefik",
            endpoints={
                "ingress": RemoteEndpoint(interface="ingress", role="provider"),
            },
            charm="ch:amd64/traefik-k8s-254",
            total_connected_count=4,
            active_connected_count=4,
        ),
        "traefik-route": OfferStatus(
            app="traefik",
            endpoints={
                "traefik-route": RemoteEndpoint(interface="traefik_route", role="provider"),
            },
            charm="ch:amd64/traefik-k8s-254",
            total_connected_count=3,
            active_connected_count=3,
        ),
    },
    storage=CombinedStorage(
        storage={
            "active-index-directory/2": StorageInfo(
                kind="filesystem",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:38:14+01:00"),
                persistent=False,
                life="alive",
                attachments=StorageAttachments(
                    units={
                        "loki/0": UnitStorageAttachment(life="alive"),
                    },
                ),
            ),
            "configurations/5": StorageInfo(
                kind="filesystem",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:37:45+01:00"),
                persistent=False,
                life="alive",
                attachments=StorageAttachments(
                    units={
                        "traefik/0": UnitStorageAttachment(life="alive"),
                    },
                ),
            ),
            "data/0": StorageInfo(
                kind="filesystem",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:37:56+01:00"),
                persistent=False,
                life="alive",
                attachments=StorageAttachments(
                    units={
                        "alertmanager/0": UnitStorageAttachment(life="alive"),
                    },
                ),
            ),
            "database/1": StorageInfo(
                kind="filesystem",
                status=EntityStatus(current="attached", since="26 Jan 2026 13:37:58+01:00"),
                persistent=False,
                life="alive",
                attachments=StorageAttachments(
                    units={
                        "grafana/0": UnitStorageAttachment(life="alive"),
                    },
                ),
            ),
            "database/4": StorageInfo(
                kind="filesystem",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:37:54+01:00"),
                persistent=False,
                life="alive",
                attachments=StorageAttachments(
                    units={
                        "prometheus/0": UnitStorageAttachment(life="alive"),
                    },
                ),
            ),
            "loki-chunks/3": StorageInfo(
                kind="filesystem",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:38:14+01:00"),
                persistent=False,
                life="alive",
                attachments=StorageAttachments(
                    units={
                        "loki/0": UnitStorageAttachment(life="alive"),
                    },
                ),
            ),
        },
        filesystems={
            "0": FilesystemInfo(
                size=2048,
                provider_id="be8786d2-62ac-435b-b10c-889d654f3cb9",
                volume="0",
                storage="data/0",
                attachments=FilesystemAttachments(
                    containers={
                        "alertmanager/0": FilesystemAttachment(
                            mount_point="/var/lib/juju/storage/data/0",
                            read_only=False,
                            life="alive",
                        ),
                    },
                    units={
                        "alertmanager/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:37:56+01:00"),
            ),
            "1": FilesystemInfo(
                size=2048,
                provider_id="0fd2299f-658d-4eab-b5da-6626c2123d68",
                volume="1",
                storage="database/1",
                attachments=FilesystemAttachments(
                    containers={
                        "grafana/0": FilesystemAttachment(
                            mount_point="/var/lib/juju/storage/database/0",
                            read_only=False,
                            life="alive",
                        ),
                    },
                    units={
                        "grafana/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="26 Jan 2026 13:37:58+01:00"),
            ),
            "2": FilesystemInfo(
                size=2048,
                provider_id="37d8976b-9b79-4ab9-b38c-177a119f8d33",
                volume="2",
                storage="active-index-directory/2",
                attachments=FilesystemAttachments(
                    containers={
                        "loki/0": FilesystemAttachment(
                            mount_point="/var/lib/juju/storage/active-index-directory/0",
                            read_only=False,
                            life="alive",
                        ),
                    },
                    units={
                        "loki/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:38:14+01:00"),
            ),
            "3": FilesystemInfo(
                size=10240,
                provider_id="5001c042-85c3-42a0-a198-9acaf7cf43a5",
                volume="3",
                storage="loki-chunks/3",
                attachments=FilesystemAttachments(
                    containers={
                        "loki/0": FilesystemAttachment(
                            mount_point="/var/lib/juju/storage/loki-chunks/0",
                            read_only=False,
                            life="alive",
                        ),
                    },
                    units={
                        "loki/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:38:14+01:00"),
            ),
            "4": FilesystemInfo(
                size=10240,
                provider_id="b406222a-c38e-4396-9c64-cd97d0239e30",
                volume="4",
                storage="database/4",
                attachments=FilesystemAttachments(
                    containers={
                        "prometheus/0": FilesystemAttachment(
                            mount_point="/var/lib/juju/storage/database/0",
                            read_only=False,
                            life="alive",
                        ),
                    },
                    units={
                        "prometheus/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:37:54+01:00"),
            ),
            "5": FilesystemInfo(
                size=1024,
                provider_id="55a9e13f-a7e4-40c6-a4aa-c2b484655ff3",
                volume="5",
                storage="configurations/5",
                attachments=FilesystemAttachments(
                    containers={
                        "traefik/0": FilesystemAttachment(
                            mount_point="/var/lib/juju/storage/configurations/0",
                            read_only=False,
                            life="alive",
                        ),
                    },
                    units={
                        "traefik/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:37:45+01:00"),
            ),
        },
        volumes={
            "0": VolumeInfo(
                size=2048,
                persistent=True,
                provider_id="pvc-be8786d2-62ac-435b-b10c-889d654f3cb9",
                storage="data/0",
                attachments=VolumeAttachments(
                    containers={
                        "alertmanager/0": VolumeAttachment(read_only=False, life="alive"),
                    },
                    units={
                        "alertmanager/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:37:56+01:00"),
            ),
            "1": VolumeInfo(
                size=2048,
                persistent=True,
                provider_id="pvc-0fd2299f-658d-4eab-b5da-6626c2123d68",
                storage="database/1",
                attachments=VolumeAttachments(
                    containers={
                        "grafana/0": VolumeAttachment(read_only=False, life="alive"),
                    },
                    units={
                        "grafana/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="26 Jan 2026 13:37:58+01:00"),
            ),
            "2": VolumeInfo(
                size=2048,
                persistent=True,
                provider_id="pvc-37d8976b-9b79-4ab9-b38c-177a119f8d33",
                storage="active-index-directory/2",
                attachments=VolumeAttachments(
                    containers={
                        "loki/0": VolumeAttachment(read_only=False, life="alive"),
                    },
                    units={
                        "loki/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:38:14+01:00"),
            ),
            "3": VolumeInfo(
                size=10240,
                persistent=True,
                provider_id="pvc-5001c042-85c3-42a0-a198-9acaf7cf43a5",
                storage="loki-chunks/3",
                attachments=VolumeAttachments(
                    containers={
                        "loki/0": VolumeAttachment(read_only=False, life="alive"),
                    },
                    units={
                        "loki/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:38:14+01:00"),
            ),
            "4": VolumeInfo(
                size=10240,
                persistent=True,
                provider_id="pvc-b406222a-c38e-4396-9c64-cd97d0239e30",
                storage="database/4",
                attachments=VolumeAttachments(
                    containers={
                        "prometheus/0": VolumeAttachment(read_only=False, life="alive"),
                    },
                    units={
                        "prometheus/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:37:54+01:00"),
            ),
            "5": VolumeInfo(
                size=1024,
                persistent=True,
                provider_id="pvc-55a9e13f-a7e4-40c6-a4aa-c2b484655ff3",
                storage="configurations/5",
                attachments=VolumeAttachments(
                    containers={
                        "traefik/0": VolumeAttachment(read_only=False, life="alive"),
                    },
                    units={
                        "traefik/0": UnitStorageAttachment(life="alive"),
                    },
                ),
                pool="kubernetes",
                life="alive",
                status=EntityStatus(current="attached", since="11 Mar 2026 23:37:45+01:00"),
            ),
        },
    ),
    controller=ControllerStatus(timestamp="11:22:37+02:00"),
)
