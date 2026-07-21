"""Tests for MachineAdapter."""

import pytest
from fixtures import StatusFixtures

from jubilant_adapters.adapters import MachineAdapter


@pytest.fixture
def machine(mock_juju) -> MachineAdapter:
    mock_juju.status.return_value = StatusFixtures.vm
    return MachineAdapter("2", mock_juju)


def test_dns_name(machine: MachineAdapter):
    assert machine.dns_name == "10.148.75.116"


def test_id(machine: MachineAdapter):
    assert machine.id == "2"


def test_agent_status(machine: MachineAdapter):
    assert machine.agent_status == "started"


def test_hostname(machine: MachineAdapter):
    assert machine.hostname == "juju-f4a349-2"


def test_status(machine: MachineAdapter):
    assert machine.status == "running"


def test_status_message(machine: MachineAdapter):
    assert machine.status_message == "Running"


def test_destroy_without_force(machine: MachineAdapter, mock_juju):
    machine.destroy()
    mock_juju.cli.assert_called_once_with("remove-machine", "2")


def test_destroy_with_force(machine: MachineAdapter, mock_juju):
    machine.destroy(force=True)
    mock_juju.cli.assert_called_once_with("remove-machine", "2", "--force")


def test_remove_is_alias_for_destroy(machine: MachineAdapter, mock_juju):
    machine.remove(force=True)
    mock_juju.cli.assert_called_once_with("remove-machine", "2", "--force")


def test_ssh_not_implemented(machine: MachineAdapter):
    with pytest.raises(NotImplementedError):
        machine.ssh("ls")
