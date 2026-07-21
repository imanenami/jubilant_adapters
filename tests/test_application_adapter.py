"""Tests for ApplicationAdapter."""

import copy

import pytest
from fixtures import StatusFixtures

from jubilant_adapters.adapters import ApplicationAdapter, UnitAdapter


@pytest.fixture
def app(mock_juju) -> ApplicationAdapter:
    mock_juju.status.return_value = StatusFixtures.vm
    return ApplicationAdapter("kafka", mock_juju)


def test_add_unit_returns_newly_added_units(mock_juju):
    status_pre = StatusFixtures.vm
    status_post = copy.deepcopy(status_pre)
    from jubilant.statustypes import StatusInfo, UnitStatus

    status_post.apps["kafka"].units["kafka/5"] = UnitStatus(
        workload_status=StatusInfo(current="active"),
        juju_status=StatusInfo(current="idle"),
        machine="0",
        public_address="10.0.0.5",
    )
    mock_juju.status.side_effect = [status_pre, status_post]

    app = ApplicationAdapter("kafka", mock_juju)
    added = app.add_unit(count=1)

    mock_juju.add_unit.assert_called_once_with("kafka", num_units=1, to=None, attach_storage=None)
    assert len(added) == 1
    assert added[0].name == "kafka/5"
    assert isinstance(added[0], UnitAdapter)


def test_add_units_is_alias_for_add_unit(mock_juju):
    status = StatusFixtures.vm
    mock_juju.status.side_effect = [status, status]
    app = ApplicationAdapter("kafka", mock_juju)
    added = app.add_units(count=0)
    assert added == []


def test_destroy_waits_by_default(app: ApplicationAdapter, mock_juju):
    app.destroy()
    mock_juju.remove_application.assert_called_once_with(
        "kafka", destroy_storage=False, force=False
    )
    mock_juju.wait.assert_called_once()


def test_destroy_no_wait_skips_wait_call(app: ApplicationAdapter, mock_juju):
    app.destroy(no_wait=True)
    mock_juju.wait.assert_not_called()


def test_destroy_unit(app: ApplicationAdapter, mock_juju):
    app.destroy_unit("kafka/0", "kafka/1")
    mock_juju.remove_unit.assert_called_once_with("kafka/0", "kafka/1", destroy_storage=True)


def test_destroy_units_is_alias(app: ApplicationAdapter, mock_juju):
    app.destroy_units("kafka/0")
    mock_juju.remove_unit.assert_called_once_with("kafka/0", destroy_storage=True)


def test_refresh_forwards_args(app: ApplicationAdapter, mock_juju):
    app.refresh(channel="latest/edge", revision=5)
    mock_juju.refresh.assert_called_once_with(
        "kafka", channel="latest/edge", force=False, path=None, resources=None, revision=5
    )


def test_remove_relation(app: ApplicationAdapter, mock_juju):
    app.remove_relation("cluster", "kafka:peer-cluster")
    mock_juju.remove_relation.assert_called_once_with("cluster", "kafka:peer-cluster")


def test_scale_raises_without_args(app: ApplicationAdapter):
    with pytest.raises(ValueError, match="Must provide either scale or scale_change"):
        app.scale()


def test_scale_absolute(app: ApplicationAdapter, mock_juju):
    app.scale(scale=3)
    mock_juju.cli.assert_called_once_with("scale-application", "kafka", "3")


def test_scale_change_computes_relative_scale(app: ApplicationAdapter, mock_juju):
    # StatusFixtures.vm kafka app has 5 units.
    app.scale(scale_change=2)
    mock_juju.cli.assert_called_once_with("scale-application", "kafka", "7")


def test_scale_change_floors_at_one(app: ApplicationAdapter, mock_juju):
    app.scale(scale_change=-100)
    mock_juju.cli.assert_called_once_with("scale-application", "kafka", "1")


def test_set_config(app: ApplicationAdapter, mock_juju):
    app.set_config({"foo": "bar"})
    mock_juju.config.assert_called_once_with("kafka", values={"foo": "bar"})


def test_units_property(app: ApplicationAdapter):
    units = app.units
    assert {u.name for u in units} == set(StatusFixtures.vm.apps["kafka"].units)
    assert all(isinstance(u, UnitAdapter) for u in units)


def test_status_property(app: ApplicationAdapter):
    assert app.status == "maintenance"


def test_status_message_property(app: ApplicationAdapter):
    assert "scaling" in app.status_message


def test_relations_property_delegates_to_units(app: ApplicationAdapter, mock_juju):
    mock_juju.cli.return_value = "{}"
    relations = list(app.relations)
    assert relations == []
