"""Tests for jubilant_adapters/__init__.py: JujuFixture, temp_model_fixture, gather."""

import subprocess
from unittest.mock import MagicMock

import pytest

from jubilant import CLIError
from jubilant_adapters import JujuFixture, gather, temp_model_fixture
from jubilant_adapters.adapters import LegacyExtensions


def test_gather_is_a_noop():
    assert gather(1, 2, 3) is None


def test_ext_property_returns_legacy_extensions():
    juju = JujuFixture(model="testing")
    assert isinstance(juju.ext, LegacyExtensions)
    assert juju.ext._juju is juju


def test_old_cli_success(monkeypatch):
    juju = JujuFixture(model="testing")
    monkeypatch.setattr(juju, "cli", lambda *cmd, **kw: "output")
    returncode, stdout, stderr = juju.old_cli("status")
    assert (returncode, stdout, stderr) == (0, "output", "")


def test_old_cli_translates_cli_error(monkeypatch):
    juju = JujuFixture(model="testing")
    error = CLIError(returncode=2, cmd="status", output="out", stderr="err")

    def _raise(*cmd, **kw):
        raise error

    monkeypatch.setattr(juju, "cli", _raise)
    returncode, stdout, stderr = juju.old_cli("status")
    assert (returncode, stdout, stderr) == (2, "out", "err")


def test_juju_is_alias_for_old_cli(monkeypatch):
    juju = JujuFixture(model="testing")
    monkeypatch.setattr(juju, "cli", lambda *cmd, **kw: "output")
    assert juju.juju("status") == (0, "output", "")


def test_temp_model_fixture_adds_and_destroys_model(monkeypatch):
    fake_juju = MagicMock()
    fake_juju.model = "jubilant-deadbeef"
    monkeypatch.setattr("jubilant_adapters.JujuFixture", lambda: fake_juju)

    with temp_model_fixture() as juju:
        assert juju is fake_juju
        fake_juju.add_model.assert_called_once()
        args, kwargs = fake_juju.add_model.call_args
        assert args[0].startswith("jubilant-")

    fake_juju._cli.assert_called_once_with(
        "destroy-model",
        "jubilant-deadbeef",
        "--no-prompt",
        "--destroy-storage",
        "--force",
        include_model=False,
        timeout=600,
    )
    assert fake_juju.model is None


def test_temp_model_fixture_keep_skips_destroy(monkeypatch):
    fake_juju = MagicMock()
    fake_juju.model = "jubilant-deadbeef"
    monkeypatch.setattr("jubilant_adapters.JujuFixture", lambda: fake_juju)

    with temp_model_fixture(keep=True) as juju:
        assert juju is fake_juju

    fake_juju._cli.assert_not_called()


def test_temp_model_fixture_swallows_timeout_on_destroy(monkeypatch):
    fake_juju = MagicMock()
    fake_juju.model = "jubilant-deadbeef"
    fake_juju._cli.side_effect = subprocess.TimeoutExpired(cmd="destroy-model", timeout=600)
    monkeypatch.setattr("jubilant_adapters.JujuFixture", lambda: fake_juju)

    with temp_model_fixture():
        pass  # Should not raise despite the destroy call timing out.


def test_temp_model_fixture_cleans_up_when_body_raises(monkeypatch):
    fake_juju = MagicMock()
    fake_juju.model = "jubilant-deadbeef"
    monkeypatch.setattr("jubilant_adapters.JujuFixture", lambda: fake_juju)

    with pytest.raises(RuntimeError):
        with temp_model_fixture():
            raise RuntimeError("boom")

    fake_juju._cli.assert_called_once()
