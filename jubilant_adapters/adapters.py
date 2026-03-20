"""Adapters which use Jubilant to provide libjuju-compliant API."""

import json
import logging
import re
import subprocess
import tempfile
from collections import UserDict, defaultdict
from collections.abc import Callable, Iterable, Mapping
from contextlib import contextmanager
from functools import cached_property
from os import PathLike
from pathlib import Path
from typing import Any, Literal

import yaml
from jubilant import (
    ConfigValue,
    Juju,
    Status,
    Task,
    TaskError,
    all_agents_idle,
    any_error,
)
from jubilant.statustypes import UnitStatus

from .typedefs import CT, RelationInfo
from .utils import all_active_idle, all_statuses_are

logger = logging.getLogger(__name__)


def gather(*calls: Any) -> None:
    """Placeholder function to replace asyncio.gather calls."""
    pass


class LibjujuStatusDict(UserDict):
    """Legacy status object conformant with libjuju model."""

    def __init__(self, status: Status):
        super().__init__()
        self._jubilant_status = status
        self.data = self._transform()

    def _transform(self) -> dict[str, Any]:
        status = defaultdict(lambda: {})
        for app, app_status in self._jubilant_status.apps.items():
            status["applications"][app] = self.obj_to_dict(app_status)
            status["applications"][app]["units"] = {}
            for unit, unit_status in app_status.units.items():
                status["applications"][app]["units"][unit] = self.obj_to_dict(unit_status)
        return status

    @staticmethod
    def obj_to_dict(obj: Any) -> dict[str, Any]:
        """Return a dict repr. of an object."""
        ret = {}
        for k in dir(obj):
            if not k.startswith("_"):
                ret[k.replace("_", "-")] = getattr(obj, k)
        return ret


class ActionAdapter:
    """Action model adapter for libjuju."""

    def __init__(self, task: Task, failed: bool = False):
        self.task = task
        self.status = "failed" if failed else "succeeded"
        self.results = task.results
        self.results["return-code"] = task.return_code

    def wait(self) -> "ActionAdapter":
        """Mock wait, since jubilant actions are sync."""
        return self


class MachineAdapter:
    """Machine model adapter for libjuju."""

    def __init__(self, id_: str, juju: Juju):
        self.id = id_
        self._juju = juju

    def destroy(self, force=False):
        """Remove this machine from the model."""
        cmd_args = ["remove-machine", self.id]
        if force:
            cmd_args.append("--force")
        self._juju.cli(*cmd_args)

    remove = destroy

    def ssh(
        self,
        command,
        user="ubuntu",
        proxy=False,
        ssh_opts=None,
        wait_for_active=False,
        timeout=None,
    ):
        """Execute a command over SSH on this machine."""
        raise NotImplementedError("ssh method is not implemented yet.")

    @property
    def agent_status(self) -> str:
        """Return the machine agent status, e.g. 'started', 'running', etc."""
        return self._juju.status().machines[self.id].machine_status.current

    @property
    def dns_name(self) -> str | None:
        """Get the DNS name for this machine."""
        return self._juju.status().machines[self.id].dns_name

    @property
    def hostname(self) -> str | None:
        """Get the hostname for this machine, e.g. juju-8149c9-2."""
        return self._juju.status().machines[self.id].hostname


class UnitAdapter:
    """Unit model adapter for libjuju."""

    def __init__(self, name: str, app: str, status: UnitStatus, juju: Juju):
        self.app = app
        self.name = name
        self.status = status
        self._juju = juju

    def _update_status(self) -> None:
        """Update unit status."""
        self.status = self._juju.status().apps[self.app].units[self.name]

    def destroy(
        self,
        destroy_storage: bool = False,
        dry_run: bool = False,
        force: bool = False,
        max_wait: float | None = None,
    ):
        """Destroy this unit."""
        if dry_run:
            return

        if max_wait:
            logger.warning("UnitAdapter::destroy does not support max_wait arg.")

        self._juju.remove_unit(self.name, destroy_storage=destroy_storage, force=force)

    def is_leader_from_status(self) -> bool:
        """Check to see if this unit is the leader."""
        return self.status.leader

    def relation_info(self) -> dict[int, RelationInfo]:
        """Return the unit `relation-info` for `juju show-unit` output."""
        ret = {}
        for item in self.show().get("relation-info", []):
            if not (_id := item.get("relation-id")):
                continue

            ret[_id] = RelationInfo(
                app=self.app,
                endpoint=item.get("endpoint", ""),
                related_endpoint=item.get("related-endpoint", ""),
                raw=dict(item),
            )

        return ret

    remove = destroy

    def run_action(self, action_name: str, **params) -> ActionAdapter:
        """Run an action on this unit."""
        failed = False
        try:
            task = self._juju.run(self.name, action=action_name, params=dict(params), wait=600.0)
        except TaskError as e:
            task = e.task
            failed = True
        return ActionAdapter(task, failed=failed)

    def show(self) -> CT.ShowUnitOutput:
        """Return the parsed `show-unit` command."""
        raw = self._juju.cli("show-unit", "--format", "json", self.name)
        return json.loads(raw).get(self.name, {})

    @property
    def machine(self) -> MachineAdapter:
        """Return the machine which hosts this unit."""
        self._update_status()
        return MachineAdapter(self.status.machine, self._juju)

    @property
    def public_address(self) -> str:
        """Unit public address."""
        return self.status.public_address

    @property
    def workload_status(self) -> str:
        """Return workload status."""
        self._update_status()
        return self.status.workload_status.current

    @property
    def workload_status_message(self) -> str:
        """Return workload status message."""
        self._update_status()
        return self.status.workload_status.message


class ApplicationAdapter:
    """Application model adapter for libjuju."""

    def __init__(self, name: str, juju: Juju):
        self.name = name
        self._juju = juju

    def add_unit(
        self,
        count: int = 1,
        to: str | Iterable[str] | None = None,
        attach_storage: Iterable[str] = [],
    ) -> Iterable[UnitAdapter]:
        """Add one or more units to this application."""
        _attach_storage = attach_storage if attach_storage else None
        units_pre = set(self._juju.status().apps[self.name].units)
        self._juju.add_unit(self.name, num_units=count, to=to, attach_storage=_attach_storage)
        self._juju.wait(lambda status: len(status.apps[self.name].units) == len(units_pre) + count)
        status_post = self._juju.status()
        units_post = set(status_post.apps[self.name].units)
        added_units = units_post - units_pre
        return [
            UnitAdapter(u, self.name, status_post.apps[self.name].units[u], self._juju)
            for u in added_units
        ]

    add_units = add_unit

    def destroy(
        self, destroy_storage: bool = False, force: bool = False, no_wait: bool = False
    ) -> None:
        """Destroy the application."""
        self._juju.remove_application(self.name, destroy_storage=destroy_storage, force=force)

        if no_wait:
            return

        self._juju.wait(
            lambda status: self.name not in status.apps,
            timeout=1000,
        )

    def destroy_unit(self, *unit_names: str) -> None:
        """Destroy units by name."""
        self._juju.remove_unit(*unit_names, destroy_storage=True)

    destroy_units = destroy_unit

    def refresh(
        self,
        channel: str | None = None,
        force: bool = False,
        force_series: bool = False,
        force_units: bool = False,
        path: Path | str | None = None,
        resources: dict[str, str] | None = None,
        revision: int | None = None,
        switch: str | None = None,
    ):
        """Refresh the charm for this application."""
        self._juju.refresh(
            self.name,
            channel=channel,
            force=force,
            path=path,
            resources=resources,
            revision=revision,
        )

    def remove_relation(
        self, local_relation: str, remote_relation: str, block_until_done: bool = False
    ) -> None:
        """Remove a relation to another application."""
        self._juju.remove_relation(local_relation, remote_relation)

    def scale(self, scale: int | None = None, scale_change: int | None = None):
        """Set or adjust the scale of this (K8s) application."""
        if not any([scale, scale_change]):
            raise ValueError("Must provide either scale or scale_change")

        if scale_change:
            scale = len(self._juju.status().apps[self.name].units) + scale_change
            scale = max(1, scale)

        self._juju.cli("scale-application", self.name, f"{scale}")

    def set_config(self, config: Mapping[str, ConfigValue]) -> None:
        """Set configuration options for this application."""
        self._juju.config(self.name, values=config)

    @property
    def relations(self) -> Iterable[RelationInfo]:
        """Application relations."""
        return ModelAdapter.get_relations(self.units).values()

    @property
    def units(self) -> list[UnitAdapter]:
        """Application units."""
        units = self._juju.status().apps[self.name].units
        return [
            UnitAdapter(name=unit_name, app=self.name, status=unit_status, juju=self._juju)
            for unit_name, unit_status in units.items()
        ]

    @property
    def status(self) -> str:
        """Return current app status."""
        return self._juju.status().apps[self.name].app_status.current

    @property
    def status_message(self) -> str:
        """Return the app status message."""
        return self._juju.status().apps[self.name].app_status.message


class ModelAdapter:
    """Adapter for libjuju `Model` objects."""

    def __init__(self, juju: Juju, wait_delay: float = 3.0):
        self._juju = juju
        self._delay = wait_delay

    def add_machine(
        self,
        spec: str | None = None,
        constraints: list[str] | None = None,
        disks: list[str] | None = None,
        series: str | None = None,
    ) -> None:
        """Start a new, empty machine."""
        cmd_args = []
        if series:
            cmd_args += ["--series", series]
        if constraints:
            cmd_args += ["--constraints", " ".join(constraints)]
        if disks:
            cmd_args += ["--disks", " ".join(disks)]
        if spec:
            cmd_args += [spec]
        self._juju.cli("add-machine", *cmd_args)

    def add_secret(
        self, name: str, data_args: Iterable[str], file: str = "", info: str = ""
    ) -> None:
        """Adds a secret with a list of key values.

        Equivalent to the cli command:
        juju add-secret [options] <name> [key[#base64|#file]=value...]

        :param name str: The name of the secret to be added.
        :param data_args []str: The key value pairs to be added into the secret.
        :param file str: A path to a yaml file containing secret key values.
        :param info str: The secret description.
        """
        if file:
            raise NotImplementedError("file argument is not supported.")

        content = {}
        for arg in data_args:
            k, v = arg.split("=")
            content[k] = v

        self._juju.add_secret(name, content=content, info=info)

    def block_until(
        self, *conditions: Callable, timeout: float | None = None, wait_period: float = 0.5
    ) -> None:
        """Return only after all conditions are true."""
        # set a large enough timeout if no timeout is provided
        _timeout = timeout if timeout else 1800  # 30 min.
        # Adjust delay proportional to timeout to restrict `juju status` calls to 180.
        # Min. delay will be 5s.
        _delay = max(5, _timeout // 180)
        self._juju.wait(
            lambda status: all(c() for c in conditions),
            timeout=_timeout,
            successes=1,
            delay=_delay,
        )

    def deploy(
        self,
        entity_url: str,
        application_name: str | None = None,
        bind: dict[str, str] = {},  # noqa
        channel: str | None = None,
        config: dict[str, ConfigValue] | None = None,
        constraints: CT.Devices = None,
        force: bool = False,
        num_units: int = 1,
        overlays: list[str] | None = None,
        base: str | None = None,
        resources: dict[str, str] | None = None,
        series: str | None = None,
        revision: str | int | None = None,
        storage: Mapping[str, str] | None = None,
        to: str | None = None,
        devices: CT.Devices = None,
        trust: bool = False,
        attach_storage: list[str] | None = None,
    ) -> None:
        """Deploy a new service or bundle.

        :param str entity_url: Charm or bundle to deploy. Charm url or file path
        :param str application_name: Name to give the service
        :param dict bind: <charm endpoint>:<network space> pairs
        :param str channel: Charm store channel from which to retrieve
            the charm or bundle, e.g. 'edge'
        :param dict config: Charm configuration dictionary
        :param constraints: Service constraints
        :type constraints: :class:`juju.Constraints`
        :param bool force: Allow charm to be deployed to a machine running
            an unsupported series
        :param int num_units: Number of units to deploy
        :param [] overlays: Bundles to overlay on the primary bundle, applied in order
        :param str base: The base on which to deploy
        :param dict resources: <resource name>:<file path> pairs
        :param str series: Series on which to deploy DEPRECATED: use --base (with Juju 3.1)
        :param int revision: specifying a revision requires a channel
            for future upgrades for charms.
            For bundles, revision and channel are mutually exclusive.
        :param dict storage: optional storage constraints, in the form of `{label: constraint}`.
            The label is a string specified by the charm, while the constraint is
            a constraints.StorageConstraintsDict, or a string following
            `the juju storage constraint directive format <https://juju.is/docs/juju/storage-constraint>`_,
            specifying the storage pool, number of volumes, and size of each volume.
        :param to: Placement directive as a string. For example:

            '23' - place on machine 23
            'lxd:7' - place in new lxd container on machine 7
            '24/lxd/3' - place in container 3 on machine 24

            If None, a new machine is provisioned.
        :param devices: charm device constraints
        :param bool trust: Trust signifies that the charm should be deployed
            with access to trusted credentials. Hooks run by the charm can access
            cloud credentials and other trusted access credentials.

        :param str[] attach_storage: Existing storage to attach to the deployed unit
            (not available on k8s models)
        """
        _overlays = list(overlays) if overlays else []
        # For compatibility with libjuju num_units=0 for subordinate charms
        kwargs = {}
        if num_units > 0:
            kwargs = {"num_units": num_units}
        _revision = int(revision) if revision else None
        self._juju.deploy(
            entity_url,
            app=application_name,
            attach_storage=attach_storage,
            base=base,
            bind=bind,
            channel=channel,
            config=config,
            constraints=constraints,
            force=force,
            overlays=_overlays,
            resources=resources,
            revision=_revision,
            storage=storage,
            to=to,
            trust=trust,
            **kwargs,
        )

    def destroy_unit(
        self,
        unit_id: str,
        destroy_storage: bool = False,
        dry_run: bool = False,
        force: bool = False,
        max_wait: float | None = None,
    ) -> None:
        """Destroy units by name."""
        self._juju.remove_unit(unit_id, destroy_storage=destroy_storage, force=force)

    def get_machines(self) -> list[str]:
        """Return list of machines in this model."""
        return list(self.machines.keys())

    def get_status(self, filters=None, utc: bool = False) -> LibjujuStatusDict:
        """Return the status of the model.

        :param str filters: Optional list of applications, units, or machines
            to include, which can use wildcards ('*').
        :param bool utc: Deprecated, display time as UTC in RFC3339 format

        """
        if any([filters, utc]):
            raise NotImplementedError("filters and utc arguments are not supported.")

        return LibjujuStatusDict(self._juju.status())

    def grant_secret(self, secret_name: str, application: str, *applications: str):
        """Grants access to a secret to the specified applications."""
        apps = [application, *applications]
        self._juju.grant_secret(secret_name, apps)

    def list_storage(self, filesystem: bool = False, volume: bool = False) -> list[CT.StorageInfo]:
        """Lists storage details."""
        raw = self._juju.cli("list-storage", "--format", "json")
        json_ = json.loads(raw)
        ret = []
        for storage_key, storage_details in json_.get("storage", {}).items():
            ret.append({"key": storage_key, **storage_details})

        return ret

    def integrate(self, relation1: str, relation2: str) -> RelationInfo:
        """Create the `relation1` <-> `relation2` integration."""
        relation_ids_pre = {relation.id for relation in self.relations}
        self._juju.integrate(relation1, relation2)
        logger.debug("Waiting for relation to be added.")
        self._juju.wait(
            lambda status: len(list(self.relations)) > len(relation_ids_pre), successes=1, delay=5
        )
        relations_post = list(self.relations)
        relation_ids_post = {relation.id for relation in relations_post}
        rel_id = next(iter(relation_ids_post - relation_ids_pre))
        return next(iter(relation for relation in relations_post if relation.id == rel_id))

    add_relation = integrate
    relate = integrate

    def remove_application(
        self,
        app_name: str,
        block_until_done: bool = False,
        force: bool = False,
        destroy_storage: bool = False,
        no_wait: bool = False,
        timeout: float | None = None,
    ) -> None:
        """Removes the given application from the model.

        :param str app_name: Name of the application
        :param bool force: Completely remove an application and all its dependencies. (=false)
        :param bool destroy_storage: Destroy storage attached to application unit. (=false)
        :param bool no_wait: Rush through application removal without waiting for each
            individual step to complete (=false)
        :param bool block_until_done: Ensure the app is removed from the
        model when returned
        :param int timeout: Raise asyncio.exceptions.TimeoutError if the application is not removed
        within the timeout period.
        """
        self._juju.remove_application(app_name, destroy_storage=destroy_storage, force=force)
        if not block_until_done:
            return

        self._juju.wait(
            lambda status: app_name not in status.apps,
            delay=self._delay,
            timeout=timeout,
        )

    def set_config(self, config: Mapping[str, ConfigValue]) -> None:
        """Set configuration options for this application."""
        self._juju.model_config(values=config)

    def update_secret(
        self,
        name: str,
        data_args: list[str] | None = None,
        new_name: str | None = None,
        file: str = "",
        info: str | None = None,
    ):
        """Update a secret with a list of key values, or info."""
        if file:
            raise NotImplementedError("file argument is not supported.")

        content = {}
        for arg in data_args or []:
            k, v = arg.split("=")
            content[k] = v

        self._juju.update_secret(name, content=content, info=info, name=new_name)

    # TODO: add support for wait_for_... args
    def wait_for_idle(
        self,
        apps: Iterable[str] | None = None,
        raise_on_error: bool = True,
        raise_on_blocked: bool = False,
        wait_for_active: bool = False,
        timeout: float | None = 10 * 60,
        idle_period: float = 15,
        check_freq: float = 0.5,
        status: str | None = None,
        wait_for_at_least_units: int | None = None,
        wait_for_exact_units: int | None = None,
    ) -> None:
        """Wait for applications in the model to settle into an idle state.

        :param Iterable[str]|None apps: Optional list of specific app names to wait on.
            If given, all apps must be present in the model and idle, while other
            apps in the model can still be busy. If not given, all apps currently
            in the model must be idle.

        :param bool raise_on_error: If True, then any unit or app going into
            "error" status immediately raises either a JujuAppError or a JujuUnitError.
            Note that machine or agent failures will always raise an exception (either
            JujuMachineError or JujuAgentError), regardless of this param. The default
            is True.

        :param bool raise_on_blocked: If True, then any unit or app going into
            "blocked" status immediately raises either a JujuAppError or a JujuUnitError.
            The default is False.

        :param bool wait_for_active: If True, then also wait for all unit workload
            statuses to be "active" as well. The default is False.

        :param float timeout: How long to wait, in seconds, for the bundle settles
            before raising an asyncio.TimeoutError. If None, will wait forever.
            The default is 10 minutes.

        :param float idle_period: How long, in seconds, the agent statuses of all
            units of all apps need to be `idle`. This delay is used to ensure that
            any pending hooks have a chance to start to avoid false positives.
            The default is 15 seconds.
            Exact behaviour is undefined for very small values and 0.

        :param float check_freq: How frequently, in seconds, to check the model.
            The default is every half-second.

        :param str status: The status to wait for. If None, not waiting.
            The default is None (not waiting for any status).

        :param int wait_for_at_least_units: The least number of units to go into the idle
        state. wait_for_idle will return after that many units are available (across all the
        given applications).
            The default is 1 unit.

        :param int wait_for_exact_units: The exact number of units to be expected before
            going into the idle state. (e.g. useful for scaling down).
            When set, takes precedence over the `wait_for_units` parameter.
        """

        def _all_idle_with_status(juju_status: Status, *apps: str):
            return all_agents_idle(juju_status, *apps) and all_statuses_are(
                status or "active", juju_status, apps
            )

        if status == "active" or wait_for_active:
            wait_func = all_active_idle
        elif not status:
            wait_func = all_agents_idle
        else:
            wait_func = _all_idle_with_status

        error_func = any_error if raise_on_error else None
        delay = check_freq if check_freq else self._delay
        _apps = apps if apps else list(self._juju.status().apps)

        self._juju.wait(
            lambda juju_status: wait_func(juju_status, *_apps),
            error=error_func,
            delay=delay,
            timeout=timeout,
            successes=int((idle_period) / delay),
        )

        if not wait_for_exact_units:
            return

        self._juju.wait(
            lambda status: (
                sum(len(status.apps[app].units) for app in _apps) == wait_for_exact_units
            ),
            error=error_func,
            delay=delay,
            timeout=timeout,
            successes=1,
        )

    @property
    def applications(self) -> dict[str, ApplicationAdapter]:
        """Return a mapping of application name: Application objects."""
        apps = self._juju.status().apps
        return {app: ApplicationAdapter(app, self._juju) for app in apps}

    @property
    def machines(self) -> dict[str, MachineAdapter]:
        """Return a mapping of machine id: Machine objects."""
        machines = self._juju.status().machines
        return {machine: MachineAdapter(machine, self._juju) for machine in machines}

    @property
    def relations(self) -> Iterable[RelationInfo]:
        """Return a map of relation-id:Relation for all relations currently in the model."""
        return self.get_relations(self.units.values()).values()

    @property
    def units(self) -> dict[str, UnitAdapter]:
        """Return a dict mapping of unit name: UnitAdapter objects for current model."""
        ret = {}
        for app in self.applications.values():
            for unit in app.units:
                ret[unit.name] = unit
        return ret

    @staticmethod
    def get_relations(units: Iterable[UnitAdapter]) -> dict[int, RelationInfo]:
        """Return a map of relation-id: RelationInfo for all relations currently in the model."""
        ret = {}
        for unit in units:
            for rel_id, rel_info in unit.relation_info().items():
                ret[rel_id] = rel_info

        return ret


class LegacyExtensions:
    """pytest-operator & python-libjuju extensions for Jubilant."""

    def __init__(self, juju: Juju):
        self._juju = juju

    @contextmanager
    def fast_forward(self, fast_interval: str = "10s", slow_interval: str | None = None):
        """Temporarily speed up update-status firing rate for the current model."""
        self._juju.model_config({"update-status-hook-interval": fast_interval})
        yield
        interval = slow_interval or "5m"
        self._juju.model_config({"update-status-hook-interval": interval})

    @property
    def model(self) -> ModelAdapter:
        """python-libjuju model adapter."""
        return ModelAdapter(self._juju)

    @cached_property
    def model_full_name(self) -> str:
        """Return model name."""
        return f"{self._juju.model}"

    def _get_cached_build(self, charm_path: str | PathLike) -> Path:
        charm_path = Path(charm_path)
        architecture = subprocess.run(
            ["dpkg", "--print-architecture"],
            capture_output=True,
            check=True,
            encoding="utf-8",
        ).stdout.strip()
        assert architecture in ("amd64", "arm64")
        packed_charms = list(charm_path.glob(f"*{architecture}.charm"))
        if len(packed_charms) == 1:
            # python-libjuju's model.deploy() & juju deploy files expect local charms
            # to begin with `./` or `/` to distinguish them from Charmhub charms.
            return packed_charms[0].resolve(strict=True)
        if len(packed_charms) > 1:
            raise ValueError(
                f"More than one matching .charm file found "
                f"at {charm_path=} for {architecture=}: {packed_charms}."
            )
        raise ValueError(f"Unable to find .charm file for {architecture=} at {charm_path=}")

    def build_charm(  # noqa: C901
        self,
        charm_path: str | Path,
        bases_index: int | None = None,
        verbosity: Literal["quiet", "brief", "verbose", "debug", "trace"] | None = None,
        return_all: bool = False,
        use_cache: bool = False,
    ) -> Path | list[Path]:
        """Builds a single charm."""
        if use_cache:
            return self._get_cached_build(charm_path=charm_path)

        temp_base = self._juju._temp_dir
        charms_dst_dir = Path(tempfile.mkdtemp(dir=temp_base, prefix="ja-build-"))
        charms_dst_dir.mkdir(exist_ok=True)
        charm_path = Path(charm_path)
        charm_abs = Path(charm_path).absolute()
        metadata_path = charm_path / "metadata.yaml"
        charmcraft_path = charm_path / "charmcraft.yaml"
        charmcraft_yaml_exists = charmcraft_path.exists()
        charm_name = None
        if charmcraft_yaml_exists:
            charmcraft_yaml = yaml.safe_load(charmcraft_path.read_text())
            if "name" in charmcraft_yaml:
                charm_name = charmcraft_yaml["name"]
        if charm_name is None:
            charm_name = yaml.safe_load(metadata_path.read_text())["name"]

        # Handle newer, operator framework charms.
        cmd = ["charmcraft", "pack"]
        if bases_index is not None:
            cmd.append(f"--bases-index={bases_index}")
        if verbosity:
            cmd.append(f"--verbosity={verbosity}")

        logger.info(f"Building charm {charm_name}")

        try:
            stdout = subprocess.check_output(
                " ".join(cmd), cwd=charm_abs, universal_newlines=True, shell=True
            )
            stderr = ""
            returncode = 0
        except subprocess.CalledProcessError as e:
            stdout = e.stdout
            stderr = e.stderr
            returncode = e.returncode

        if returncode == 0:
            logger.info(f"Built charm {charm_name}")
        else:
            logger.info(
                f"Charm build for {charm_name} completed with errors (return code={returncode})"
            )

        if returncode != 0:
            m = re.search(r"Failed to build charm.*full execution logs in '([^']+)'", stderr)
            if m:
                try:
                    stderr = Path(m.group(1)).read_text()
                except FileNotFoundError:
                    logger.error(f"Failed to read full build log from {m.group(1)}")
            raise RuntimeError(
                f"Failed to build charm at path `{charm_path}`:\n"
                f"    command used: `{' '.join(cmd)}`\n"
                f"    stdout: {stdout or '(null)'}\n"
                f"    stderr: {stderr or '(null)'}\n"
            )

        # If charmcraft.yaml has multiple bases
        # then multiple charms would be generated, rename them all
        charms = list(charm_abs.glob(f"{charm_name}*.charm"))
        for idx, charm_file_src in enumerate(charms):
            charm_file_dst = charms_dst_dir / charm_file_src.name
            charms[idx] = charm_file_src.rename(charm_file_dst)

        if not charms:
            raise FileNotFoundError(f"No such file in '{charm_path}/*.charm'")
        if charms and not return_all:
            # Even though we may have multiple *.charm file,
            # for backwards compatibility we can - only return one.
            return charms[0]
        return charms
