"""Tests for LegacyExtensions (excluding build_charm, covered in test_build_charm.py)."""

from jubilant_adapters.adapters import LegacyExtensions, ModelAdapter


def test_fast_forward_sets_and_restores_interval(mock_juju):
    ext = LegacyExtensions(mock_juju)
    with ext.fast_forward():
        mock_juju.model_config.assert_called_once_with({"update-status-hook-interval": "10s"})
    assert mock_juju.model_config.call_args_list[1][0][0] == {
        "update-status-hook-interval": "5m"
    }


def test_fast_forward_custom_intervals(mock_juju):
    ext = LegacyExtensions(mock_juju)
    with ext.fast_forward(fast_interval="1s", slow_interval="1m"):
        pass
    assert mock_juju.model_config.call_args_list[0][0][0] == {
        "update-status-hook-interval": "1s"
    }
    assert mock_juju.model_config.call_args_list[1][0][0] == {
        "update-status-hook-interval": "1m"
    }


def test_model_property_returns_model_adapter_for_same_juju(mock_juju):
    ext = LegacyExtensions(mock_juju)
    model = ext.model
    assert isinstance(model, ModelAdapter)
    assert model._juju is mock_juju


def test_model_full_name_is_cached(mock_juju):
    mock_juju.model = "first-model"
    ext = LegacyExtensions(mock_juju)
    assert ext.model_full_name == "first-model"
    mock_juju.model = "second-model"
    assert ext.model_full_name == "first-model"
