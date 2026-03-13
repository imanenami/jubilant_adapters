import pytest

from jubilant_adapters.adapters import JujuFixture

TEST_MODEL = "testing"


def _mock_cli(*args, **kwargs) -> tuple[str, str]:
    print(" ".join(args))
    return "success", ""


@pytest.fixture(autouse=True)
def juju() -> JujuFixture:
    _juju = JujuFixture(model=TEST_MODEL)
    _juju._cli = _mock_cli
    return _juju


def test_model_adapter(juju: JujuFixture, capsys: pytest.CaptureFixture):
    juju.ext.model.deploy("iman", channel="1/stable")
    captured = capsys.readouterr()
    assert "deploy iman" in captured.out
    assert "--channel 1/stable" in captured.out
    print(captured)
