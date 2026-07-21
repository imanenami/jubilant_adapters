"""Tests for ModelAdapter."""

import json
from unittest.mock import MagicMock

import pytest
from fixtures import StatusFixtures

from jubilant.statustypes import AppStatus, FormattedBase, ModelStatus, Status, StatusInfo, UnitStatus
from jubilant_adapters.adapters import ApplicationAdapter, MachineAdapter, ModelAdapter, UnitAdapter
from jubilant_adapters.typedefs import RelationInfo


@pytest.fixture
def model(mock_juju) -> ModelAdapter:
    return ModelAdapter(mock_juju)


def _single_unit_status(name: str = "app", app_status: str = "active", num_units: int = 1) -> Status:
    units = {
        f"{name}/{i}": UnitStatus(
            workload_status=StatusInfo(current="active"),
            juju_status=StatusInfo(current="idle"),
            machine=str(i),
            public_address=f"10.0.0.{i}",
        )
        for i in range(num_units)
    }
    return Status(
        model=ModelStatus(name="m", type="iaas", controller="c", cloud="localhost", version="3.6.0"),
        machines={},
        apps={
            name: AppStatus(
                charm=f"local:{name}-0",
                charm_origin="local",
                charm_name=name,
                charm_rev=0,
                exposed=False,
                base=FormattedBase(name="ubuntu", channel="24.04"),
                app_status=StatusInfo(current=app_status),
                units=units,
            )
        },
    )


def test_add_machine_no_args(model: ModelAdapter, mock_juju):
    model.add_machine()
    mock_juju.cli.assert_called_once_with("add-machine")


def test_add_machine_all_args(model: ModelAdapter, mock_juju):
    model.add_machine(spec="lxd:0", constraints=["mem=1G", "cores=2"], disks=["1G"], series="jammy")
    mock_juju.cli.assert_called_once_with(
        "add-machine", "--series", "jammy", "--constraints", "mem=1G cores=2", "--disks", "1G", "lxd:0"
    )


def test_add_secret_parses_key_values(model: ModelAdapter, mock_juju):
    mock_juju.add_secret.return_value = "secret:abc"
    result = model.add_secret("test", data_args=["user=pass", "foo=bar"], info="a secret")
    mock_juju.add_secret.assert_called_once_with(
        "test", content={"user": "pass", "foo": "bar"}, info="a secret"
    )
    assert result == "secret:abc"


def test_add_secret_file_not_implemented(model: ModelAdapter):
    with pytest.raises(NotImplementedError):
        model.add_secret("test", data_args=[], file="secrets.yaml")


def test_block_until_default_timeout(model: ModelAdapter, mock_juju):
    condition = MagicMock(return_value=True)
    model.block_until(condition)
    _, kwargs = mock_juju.wait.call_args
    assert kwargs["timeout"] == 1800
    assert kwargs["delay"] == 10
    assert kwargs["successes"] == 1
    ready = mock_juju.wait.call_args[0][0]
    assert ready(None) is True
    condition.assert_called_once()


def test_block_until_explicit_timeout_sets_delay(model: ModelAdapter, mock_juju):
    model.block_until(lambda: True, timeout=900)
    _, kwargs = mock_juju.wait.call_args
    assert kwargs["timeout"] == 900
    assert kwargs["delay"] == 5


def test_block_until_condition_false_makes_ready_false(model: ModelAdapter, mock_juju):
    model.block_until(lambda: False, lambda: True)
    ready = mock_juju.wait.call_args[0][0]
    assert ready(None) is False


def test_deploy_default_num_units(model: ModelAdapter, mock_juju):
    model.deploy("kafka")
    _, kwargs = mock_juju.deploy.call_args
    assert kwargs["num_units"] == 1


def test_deploy_num_units_zero_omits_kwarg(model: ModelAdapter, mock_juju):
    model.deploy("kafka", num_units=0)
    _, kwargs = mock_juju.deploy.call_args
    assert "num_units" not in kwargs


def test_deploy_revision_converted_to_int(model: ModelAdapter, mock_juju):
    model.deploy("kafka", revision="5")
    _, kwargs = mock_juju.deploy.call_args
    assert kwargs["revision"] == 5


def test_deploy_series_mapped_to_base_on_juju3(model: ModelAdapter, mock_juju, monkeypatch):
    monkeypatch.setattr("jubilant_adapters.adapters.JUJU_MAJOR_VERSION", 3)
    model.deploy("kafka", series="jammy")
    _, kwargs = mock_juju.deploy.call_args
    assert kwargs["base"] == "ubuntu@22.04"


def test_deploy_series_ignored_on_juju2(model: ModelAdapter, mock_juju, monkeypatch):
    monkeypatch.setattr("jubilant_adapters.adapters.JUJU_MAJOR_VERSION", 2)
    model.deploy("kafka", series="jammy")
    _, kwargs = mock_juju.deploy.call_args
    assert kwargs["base"] is None


def test_deploy_overlays_default_to_empty_list(model: ModelAdapter, mock_juju):
    model.deploy("kafka")
    _, kwargs = mock_juju.deploy.call_args
    assert kwargs["overlays"] == []


def test_deploy_passes_entity_url_and_kwargs(model: ModelAdapter, mock_juju):
    model.deploy("kafka", application_name="my-kafka", channel="latest/edge", trust=True)
    args, kwargs = mock_juju.deploy.call_args
    assert args[0] == "kafka"
    assert kwargs["app"] == "my-kafka"
    assert kwargs["channel"] == "latest/edge"
    assert kwargs["trust"] is True


def test_destroy_unit(model: ModelAdapter, mock_juju):
    model.destroy_unit("kafka/0", destroy_storage=True, force=True)
    mock_juju.remove_unit.assert_called_once_with("kafka/0", destroy_storage=True, force=True)


def test_get_machines(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = StatusFixtures.vm
    assert set(model.get_machines()) == set(StatusFixtures.vm.machines.keys())


def test_get_status_returns_libjuju_status_dict(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = StatusFixtures.cos
    status_dict = model.get_status()
    assert "applications" in status_dict


@pytest.mark.parametrize("kwargs", [{"filters": "app*"}, {"utc": True}])
def test_get_status_raises_on_unsupported_args(model: ModelAdapter, kwargs):
    with pytest.raises(NotImplementedError):
        model.get_status(**kwargs)


def test_grant_secret(model: ModelAdapter, mock_juju):
    model.grant_secret("my-secret", "app1", "app2")
    mock_juju.grant_secret.assert_called_once_with("my-secret", ["app1", "app2"])


def test_list_storage(model: ModelAdapter, mock_juju):
    mock_juju.cli.return_value = json.dumps(
        {"storage": {"data/0": {"kind": "filesystem", "life": "alive", "persistent": False}}}
    )
    result = model.list_storage()
    mock_juju.cli.assert_called_once_with("list-storage", "--format", "json")
    assert result == [{"key": "data/0", "kind": "filesystem", "life": "alive", "persistent": False}]


def test_integrate_returns_new_relation_info(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = _single_unit_status("kafka")
    mock_juju.cli.side_effect = [
        json.dumps({"kafka/0": {"relation-info": []}}),
        json.dumps(
            {
                "kafka/0": {
                    "relation-info": [
                        {
                            "relation-id": 7,
                            "endpoint": "kafka-client",
                            "related-endpoint": "kafka-client-consumer",
                            "related-units": {"app/0": {}},
                        }
                    ]
                }
            }
        ),
    ]

    result = model.integrate("kafka:kafka-client", "app:kafka-client-consumer")

    mock_juju.integrate.assert_called_once_with("kafka:kafka-client", "app:kafka-client-consumer")
    assert isinstance(result, RelationInfo)
    assert result.id == 7


def test_add_relation_and_relate_are_aliases_for_integrate(model: ModelAdapter):
    assert model.add_relation == model.integrate
    assert model.relate == model.integrate


def test_integrate_timeout_falls_back_to_best_effort_relation_info(model: ModelAdapter, mock_juju):
    mock_juju.cli.return_value = json.dumps({"app1/0": {"relation-info": []}})
    status_with_units = _single_unit_status("app1", num_units=1)
    status_no_units = _single_unit_status("app2", num_units=0)
    combined = Status(
        model=status_with_units.model,
        machines={},
        apps={**status_with_units.apps, **status_no_units.apps},
    )
    mock_juju.status.return_value = combined
    mock_juju.wait.side_effect = TimeoutError

    result = model.integrate("app1:endpoint", "app2:endpoint")

    assert result.app == "app1"
    assert result.raw == {}


def test_remove_application_without_block(model: ModelAdapter, mock_juju):
    model.remove_application("kafka")
    mock_juju.remove_application.assert_called_once_with("kafka", destroy_storage=False, force=False)
    mock_juju.wait.assert_not_called()


def test_remove_application_blocks_until_removed(model: ModelAdapter, mock_juju):
    model.remove_application("kafka", block_until_done=True, timeout=42)
    mock_juju.wait.assert_called_once()
    _, kwargs = mock_juju.wait.call_args
    assert kwargs["timeout"] == 42
    assert kwargs["delay"] == model._delay


def test_set_config(model: ModelAdapter, mock_juju):
    model.set_config({"foo": "bar"})
    mock_juju.model_config.assert_called_once_with(values={"foo": "bar"})


def test_update_secret_file_not_implemented(model: ModelAdapter):
    with pytest.raises(NotImplementedError):
        model.update_secret("test", file="secrets.yaml")


def test_update_secret_parses_data_args(model: ModelAdapter, mock_juju):
    model.update_secret("test", data_args=["user=pass"], new_name="renamed", info="desc")
    mock_juju.update_secret.assert_called_once_with(
        "test", content={"user": "pass"}, info="desc", name="renamed"
    )


def test_wait_for_idle_wires_all_agents_idle_by_default(model: ModelAdapter, mock_juju, monkeypatch):
    mock_juju.status.return_value = _single_unit_status("kafka")
    agents_idle = MagicMock(return_value=True)
    monkeypatch.setattr("jubilant_adapters.adapters.all_agents_idle", agents_idle)
    model.wait_for_idle()
    ready = mock_juju.wait.call_args[0][0]
    assert ready(_single_unit_status("kafka")) is True
    agents_idle.assert_called_once_with(_single_unit_status("kafka"), "kafka")


def test_wait_for_idle_wires_all_active_idle_when_wait_for_active(model: ModelAdapter, mock_juju, monkeypatch):
    mock_juju.status.return_value = _single_unit_status("kafka")
    active_idle = MagicMock(return_value=True)
    monkeypatch.setattr("jubilant_adapters.adapters.all_active_idle", active_idle)
    model.wait_for_idle(wait_for_active=True)
    ready = mock_juju.wait.call_args[0][0]
    ready(_single_unit_status("kafka"))
    active_idle.assert_called_once()


def test_wait_for_idle_uses_explicit_status(model: ModelAdapter, mock_juju, monkeypatch):
    mock_juju.status.return_value = _single_unit_status("kafka")
    agents_idle = MagicMock(return_value=True)
    statuses_are = MagicMock(return_value=True)
    monkeypatch.setattr("jubilant_adapters.adapters.all_agents_idle", agents_idle)
    monkeypatch.setattr("jubilant_adapters.adapters.all_statuses_are", statuses_are)
    model.wait_for_idle(status="blocked")
    ready = mock_juju.wait.call_args[0][0]
    ready(_single_unit_status("kafka"))
    agents_idle.assert_called_once()
    statuses_are.assert_called_once_with("blocked", _single_unit_status("kafka"), ("kafka",))


def test_wait_for_idle_error_func_none_when_raise_on_error_false(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = _single_unit_status("kafka")
    model.wait_for_idle(raise_on_error=False)
    _, kwargs = mock_juju.wait.call_args
    assert kwargs["error"] is None


def test_wait_for_idle_check_freq_zero_falls_back_to_delay(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = _single_unit_status("kafka")
    model.wait_for_idle(check_freq=0)
    _, kwargs = mock_juju.wait.call_args
    assert kwargs["delay"] == model._delay


def test_wait_for_idle_timeout_defaults_when_none(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = _single_unit_status("kafka")
    model.wait_for_idle(timeout=None)
    _, kwargs = mock_juju.wait.call_args
    assert kwargs["timeout"] == 600.0


def test_wait_for_idle_apps_default_to_all_model_apps(model: ModelAdapter, mock_juju, monkeypatch):
    status = _single_unit_status("kafka")
    mock_juju.status.return_value = status
    called = MagicMock(return_value=True)
    monkeypatch.setattr("jubilant_adapters.adapters.all_agents_idle", called)
    model.wait_for_idle()
    ready = mock_juju.wait.call_args[0][0]
    ready(status)
    called.assert_called_once_with(status, "kafka")


def test_wait_for_idle_second_wait_when_exact_units(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = _single_unit_status("kafka")
    model.wait_for_idle(wait_for_exact_units=2)
    assert mock_juju.wait.call_count == 2
    ready = mock_juju.wait.call_args_list[1][0][0]
    status_two_units = _single_unit_status("kafka", num_units=2)
    assert ready(status_two_units) is True
    status_one_unit = _single_unit_status("kafka", num_units=1)
    assert ready(status_one_unit) is False


def test_applications_property(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = StatusFixtures.cos
    apps = model.applications
    assert set(apps) == set(StatusFixtures.cos.apps)
    assert all(isinstance(a, ApplicationAdapter) for a in apps.values())


def test_machines_property(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = StatusFixtures.vm
    machines = model.machines
    assert set(machines) == set(StatusFixtures.vm.machines)
    assert all(isinstance(m, MachineAdapter) for m in machines.values())


def test_units_property_flattens_all_apps(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = StatusFixtures.vm
    units = model.units
    expected = set()
    for app_status in StatusFixtures.vm.apps.values():
        expected.update(app_status.units)
    assert set(units) == expected
    assert all(isinstance(u, UnitAdapter) for u in units.values())


def test_relations_property_uses_get_relations(model: ModelAdapter, mock_juju):
    mock_juju.status.return_value = _single_unit_status("kafka")
    mock_juju.cli.return_value = json.dumps({"kafka/0": {"relation-info": []}})
    assert list(model.relations) == []


def test_get_relations_static_method_merges_unit_relations():
    unit1 = MagicMock(spec=UnitAdapter)
    unit1.relation_info.return_value = {1: RelationInfo("app", "e1", "e2", raw={})}
    unit2 = MagicMock(spec=UnitAdapter)
    unit2.relation_info.return_value = {2: RelationInfo("app2", "e3", "e4", raw={})}
    result = ModelAdapter.get_relations([unit1, unit2])
    assert set(result) == {1, 2}
