"""Tests for UnitAdapter."""

import dataclasses
import json

import pytest
from fixtures import StatusFixtures

from jubilant import Task, TaskError
from jubilant.statustypes import StatusInfo, UnitStatus
from jubilant_adapters.adapters import MachineAdapter, UnitAdapter


@pytest.fixture
def unit_status() -> UnitStatus:
    return StatusFixtures.vm.apps["kafka"].units["kafka/0"]


@pytest.fixture
def unit(mock_juju, unit_status) -> UnitAdapter:
    return UnitAdapter("kafka/0", "kafka", unit_status, mock_juju)


def test_destroy_calls_remove_unit(unit: UnitAdapter, mock_juju):
    unit.destroy(destroy_storage=True, force=True)
    mock_juju.remove_unit.assert_called_once_with("kafka/0", destroy_storage=True, force=True)


def test_destroy_dry_run_skips_removal(unit: UnitAdapter, mock_juju):
    unit.destroy(dry_run=True)
    mock_juju.remove_unit.assert_not_called()


def test_destroy_max_wait_logs_warning(unit: UnitAdapter, mock_juju, caplog):
    with caplog.at_level("WARNING"):
        unit.destroy(max_wait=30)
    assert "max_wait" in caplog.text
    mock_juju.remove_unit.assert_called_once()


def test_remove_is_alias_for_destroy(unit: UnitAdapter, mock_juju):
    unit.remove(destroy_storage=True)
    mock_juju.remove_unit.assert_called_once_with("kafka/0", destroy_storage=True, force=False)


def test_is_leader_from_status_true(mock_juju):
    leader_status = StatusFixtures.vm.apps["kafka"].units["kafka/0"]
    unit = UnitAdapter("kafka/0", "kafka", leader_status, mock_juju)
    assert leader_status.leader is True
    assert unit.is_leader_from_status() is True


def test_is_leader_from_status_false(mock_juju):
    non_leader_status = StatusFixtures.vm.apps["kafka"].units["kafka/1"]
    unit = UnitAdapter("kafka/1", "kafka", non_leader_status, mock_juju)
    assert non_leader_status.leader is False
    assert unit.is_leader_from_status() is False


def test_show_parses_json_for_this_unit(unit: UnitAdapter, mock_juju):
    mock_juju.cli.return_value = json.dumps({"kafka/0": {"relation-info": []}})
    result = unit.show()
    mock_juju.cli.assert_called_once_with("show-unit", "--format", "json", "kafka/0")
    assert result == {"relation-info": []}


def test_show_missing_unit_returns_empty_dict(unit: UnitAdapter, mock_juju):
    mock_juju.cli.return_value = json.dumps({"other/0": {}})
    assert unit.show() == {}


def test_relation_info_skips_items_without_relation_id(unit: UnitAdapter, mock_juju):
    mock_juju.cli.return_value = json.dumps(
        {
            "kafka/0": {
                "relation-info": [
                    {"endpoint": "cluster", "related-endpoint": "cluster"},
                    {
                        "relation-id": 3,
                        "endpoint": "kafka-client",
                        "related-endpoint": "kafka-client-consumer",
                        "related-units": {"app/0": {}},
                    },
                ]
            }
        }
    )
    result = unit.relation_info()
    assert list(result.keys()) == [3]
    rel = result[3]
    assert rel.app == "kafka"
    assert rel.endpoint == "kafka-client"
    assert rel.related_endpoint == "kafka-client-consumer"
    assert rel.raw["relation-id"] == 3


def test_run_action_success(unit: UnitAdapter, mock_juju):
    task = Task(id="1", status="completed", results={"done": "true"})
    mock_juju.run.return_value = task
    action = unit.run_action("get-password", username="admin")
    mock_juju.run.assert_called_once_with(
        "kafka/0", action="get-password", params={"username": "admin"}, wait=600.0
    )
    assert action.status == "completed"
    assert action.results["done"] == "true"


def test_run_action_failure_raises_task_error_is_handled(unit: UnitAdapter, mock_juju):
    task = Task(id="1", status="failed", results={}, message="boom")
    mock_juju.run.side_effect = TaskError(task)
    action = unit.run_action("get-password")
    assert action.status == "failed"
    assert action.task is task


def test_machine_property_updates_status_and_returns_machine_adapter(
    unit: UnitAdapter, mock_juju
):
    mock_juju.status.return_value = StatusFixtures.vm
    machine = unit.machine
    assert isinstance(machine, MachineAdapter)
    assert machine.id == unit.status.machine


def test_public_address(unit: UnitAdapter, unit_status):
    assert unit.public_address == unit_status.public_address


def test_workload_status_updates_status(unit: UnitAdapter, mock_juju):
    new_status = dataclasses.replace(
        StatusFixtures.vm.apps["kafka"].units["kafka/1"],
        workload_status=StatusInfo(current="blocked", message="oops"),
    )
    fake_status = StatusFixtures.vm
    fake_status.apps["kafka"].units["kafka/0"] = new_status
    mock_juju.status.return_value = fake_status
    assert unit.workload_status == "blocked"
    assert unit.workload_status_message == "oops"
