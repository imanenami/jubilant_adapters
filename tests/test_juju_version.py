"""Tests for jubilant_adapters._juju_version."""

import json
import subprocess

import pytest

from jubilant_adapters._juju_version import JujuController, get_current_controller


def test_major_version_parses_leading_component():
    controller = JujuController(name="my-controller", version="3.6.21")
    assert controller.major_version == 3


def test_major_version_juju2():
    controller = JujuController(name="my-controller", version="2.9.45")
    assert controller.major_version == 2


def test_get_current_controller_returns_none_on_called_process_error(monkeypatch):
    def _raise(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "juju controllers")

    monkeypatch.setattr("jubilant_adapters._juju_version._execute", _raise)
    assert get_current_controller() is None


def test_get_current_controller_returns_none_when_no_current_controller(monkeypatch):
    monkeypatch.setattr(
        "jubilant_adapters._juju_version._execute",
        lambda *a, **kw: json.dumps({"current-controller": "", "controllers": {}}),
    )
    assert get_current_controller() is None


def test_get_current_controller_returns_controller_when_present(monkeypatch):
    monkeypatch.setattr(
        "jubilant_adapters._juju_version._execute",
        lambda *a, **kw: json.dumps(
            {
                "current-controller": "my-controller",
                "controllers": {"my-controller": {"agent-version": "3.6.21"}},
            }
        ),
    )
    controller = get_current_controller()
    assert controller == JujuController(name="my-controller", version="3.6.21")


@pytest.mark.parametrize(
    "sample",
    [
        "juju controllers --format json",
    ],
)
def test_execute_shells_out_and_raises_on_missing_binary(sample):
    from jubilant_adapters._juju_version import _execute

    with pytest.raises(subprocess.CalledProcessError):
        _execute("__definitely_not_a_real_command__ 2>/dev/null")
