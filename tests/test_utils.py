"""Tests for jubilant_adapters.utils."""

from unittest.mock import MagicMock

from jubilant.statustypes import AppStatus, FormattedBase, ModelStatus, Status, StatusInfo, UnitStatus
from jubilant_adapters import utils


def _status(app_status: str, unit_status: str, num_units: int = 1) -> Status:
    units = {
        f"app/{i}": UnitStatus(
            workload_status=StatusInfo(current=unit_status),
            juju_status=StatusInfo(current="idle"),
        )
        for i in range(num_units)
    }
    return Status(
        model=ModelStatus(name="m", type="iaas", controller="c", cloud="localhost", version="3.6.0"),
        machines={},
        apps={
            "app": AppStatus(
                charm="local:app-0",
                charm_origin="local",
                charm_name="app",
                charm_rev=0,
                exposed=False,
                base=FormattedBase(name="ubuntu", channel="24.04"),
                app_status=StatusInfo(current=app_status),
                units=units,
            )
        },
    )


def test_all_statuses_are_true_when_all_match():
    status = _status("active", "active", num_units=2)
    assert utils.all_statuses_are("active", status, ["app"]) is True


def test_all_statuses_are_false_on_unit_mismatch():
    status = _status("active", "maintenance")
    assert utils.all_statuses_are("active", status, ["app"]) is False


def test_all_statuses_are_false_on_app_mismatch():
    status = _status("maintenance", "active")
    assert utils.all_statuses_are("active", status, ["app"]) is False


def test_all_statuses_are_false_when_app_missing():
    status = _status("active", "active")
    assert utils.all_statuses_are("active", status, ["missing-app"]) is False


def test_all_statuses_are_defaults_to_all_apps_when_none_given():
    status = _status("active", "active")
    assert utils.all_statuses_are("active", status, []) is True


def test_all_active_idle_delegates_to_jubilant_on_juju3(monkeypatch):
    monkeypatch.setattr(utils, "JUJU_MAJOR_VERSION", 3)
    idle = MagicMock(return_value=True)
    active = MagicMock(return_value=True)
    monkeypatch.setattr(utils.jubilant, "all_agents_idle", idle)
    monkeypatch.setattr(utils.jubilant, "all_active", active)
    status = _status("active", "active")
    assert utils.all_active_idle(status, "app") is True
    idle.assert_called_once_with(status, "app")
    active.assert_called_once_with(status, "app")


def test_all_active_idle_delegates_to_compat_on_juju2(monkeypatch):
    monkeypatch.setattr(utils, "JUJU_MAJOR_VERSION", 2)
    idle = MagicMock(return_value=True)
    active = MagicMock(return_value=False)
    monkeypatch.setattr(utils.compat, "all_agents_idle", idle)
    monkeypatch.setattr(utils.compat, "all_active", active)
    status = _status("active", "active")
    assert utils.all_active_idle(status, "app") is False
    idle.assert_called_once_with(status, "app")
    active.assert_called_once_with(status, "app")


def test_all_agents_idle_delegates_to_jubilant_on_juju3(monkeypatch):
    monkeypatch.setattr(utils, "JUJU_MAJOR_VERSION", 3)
    idle = MagicMock(return_value=True)
    monkeypatch.setattr(utils.jubilant, "all_agents_idle", idle)
    status = _status("active", "active")
    assert utils.all_agents_idle(status, "app") is True
    idle.assert_called_once_with(status, "app")


def test_all_agents_idle_delegates_to_compat_on_juju2(monkeypatch):
    monkeypatch.setattr(utils, "JUJU_MAJOR_VERSION", 2)
    idle = MagicMock(return_value=False)
    monkeypatch.setattr(utils.compat, "all_agents_idle", idle)
    status = _status("active", "active")
    assert utils.all_agents_idle(status, "app") is False
    idle.assert_called_once_with(status, "app")


def test_any_error_delegates_to_jubilant_on_juju3(monkeypatch):
    monkeypatch.setattr(utils, "JUJU_MAJOR_VERSION", 3)
    err = MagicMock(return_value=True)
    monkeypatch.setattr(utils.jubilant, "any_error", err)
    status = _status("error", "error")
    assert utils.any_error(status, "app") is True
    err.assert_called_once_with(status, "app")


def test_any_error_delegates_to_compat_on_juju2(monkeypatch):
    monkeypatch.setattr(utils, "JUJU_MAJOR_VERSION", 2)
    err = MagicMock(return_value=False)
    monkeypatch.setattr(utils.compat, "any_error", err)
    status = _status("active", "active")
    assert utils.any_error(status, "app") is False
    err.assert_called_once_with(status, "app")
