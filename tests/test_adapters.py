"""Basic adapter tests."""

import pytest
from fixtures import StatusFixtures

from jubilant import Task
from jubilant_adapters import JujuFixture
from jubilant_adapters.adapters import ActionAdapter, LibjujuStatusDict, MachineAdapter

TEST_MODEL = "testing"


def _mock_cli(*args, **kwargs) -> tuple[str, str]:
    print(" ".join(args))
    return "success", ""


@pytest.fixture(autouse=True)
def juju() -> JujuFixture:
    _juju = JujuFixture(model=TEST_MODEL)
    _juju._cli = _mock_cli
    return _juju


def test_deploy(juju: JujuFixture, capsys: pytest.CaptureFixture):
    juju.ext.model.deploy("iman", channel="1/stable")
    captured = capsys.readouterr()
    assert "deploy iman" in captured.out
    assert "--channel 1/stable" in captured.out
    print(captured)


def test_add_secret(juju: JujuFixture, capsys: pytest.CaptureFixture):
    juju.ext.model.add_secret("test", data_args=["user=pass", "foo=bar"])
    captured = capsys.readouterr()
    cmd_args = captured.out.split()
    assert "add-secret" in cmd_args
    assert "--file" in cmd_args


def test_status_dict():
    status_dict = LibjujuStatusDict(StatusFixtures.cos)
    assert "applications" in status_dict
    assert "traefik/0" in status_dict["applications"]["traefik"]["units"]


def test_action():
    task = Task(id="12", status="completed", results={"done": "true"})
    action = ActionAdapter(task=task)
    action.wait()
    assert action.results["done"] == "true"


def test_machine(juju: JujuFixture):
    status = StatusFixtures.vm
    juju.status = lambda: status
    machine = MachineAdapter("2", juju)
    assert machine.dns_name == "10.148.75.116"
    assert machine.id == "2"
    assert machine.agent_status == "started"
    assert machine.status == "running"
    assert machine.status_message == "Running"
