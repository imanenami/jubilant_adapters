"""Tests for LegacyExtensions.build_charm."""
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from jubilant_adapters.adapters import LegacyExtensions

CHARM_NAME = "my-charm"


@pytest.fixture
def ext(tmp_path):
    mock_juju = MagicMock()
    mock_juju._temp_dir = str(tmp_path)
    return LegacyExtensions(mock_juju)


def _make_charm_dir(
    parent: Path,
    name: str = CHARM_NAME,
    use_charmcraft_yaml: bool = False,
    charmcraft_name: str | None = None,
) -> Path:
    charm_dir = parent / "charm"
    charm_dir.mkdir(exist_ok=True)
    (charm_dir / "metadata.yaml").write_text(yaml.dump({"name": name}))
    if use_charmcraft_yaml:
        data = {"name": charmcraft_name} if charmcraft_name else {}
        (charm_dir / "charmcraft.yaml").write_text(yaml.dump(data))
    return charm_dir


def _place_charm_file(charm_dir: Path, name: str = CHARM_NAME, suffix: str = "ubuntu-22.04-amd64") -> Path:
    charm_file = charm_dir / f"{name}_{suffix}.charm"
    charm_file.write_bytes(b"")
    return charm_file


class TestBuildCharm:
    def test_reads_name_from_charmcraft_yaml(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path, use_charmcraft_yaml=True, charmcraft_name="cc-name")
        _place_charm_file(charm_dir, "cc-name")
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value=""):
            result = ext.build_charm(charm_dir)
        assert "cc-name" in result.name

    def test_reads_name_from_metadata_when_charmcraft_yaml_missing(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        _place_charm_file(charm_dir, CHARM_NAME)
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value=""):
            result = ext.build_charm(charm_dir)
        assert CHARM_NAME in result.name

    def test_reads_name_from_metadata_when_charmcraft_yaml_has_no_name(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path, use_charmcraft_yaml=True, charmcraft_name=None)
        _place_charm_file(charm_dir, CHARM_NAME)
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value=""):
            result = ext.build_charm(charm_dir)
        assert CHARM_NAME in result.name

    def test_command_without_optional_args(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        _place_charm_file(charm_dir, CHARM_NAME)
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value="") as mock:
            ext.build_charm(charm_dir)
        assert mock.call_args[0][0] == "charmcraft pack"

    def test_command_includes_bases_index(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        _place_charm_file(charm_dir, CHARM_NAME)
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value="") as mock:
            ext.build_charm(charm_dir, bases_index=1)
        assert "--bases-index=1" in mock.call_args[0][0]

    def test_command_includes_verbosity(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        _place_charm_file(charm_dir, CHARM_NAME)
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value="") as mock:
            ext.build_charm(charm_dir, verbosity="debug")
        assert "--verbosity=debug" in mock.call_args[0][0]

    def test_returns_first_charm_by_default(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        _place_charm_file(charm_dir, CHARM_NAME, "ubuntu-22.04-amd64")
        _place_charm_file(charm_dir, CHARM_NAME, "ubuntu-20.04-amd64")
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value=""):
            result = ext.build_charm(charm_dir)
        assert isinstance(result, Path)

    def test_return_all_returns_list_of_paths(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        _place_charm_file(charm_dir, CHARM_NAME, "ubuntu-22.04-amd64")
        _place_charm_file(charm_dir, CHARM_NAME, "ubuntu-20.04-amd64")
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value=""):
            result = ext.build_charm(charm_dir, return_all=True)
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(p, Path) for p in result)

    def test_charm_files_moved_to_temp_dir(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        _place_charm_file(charm_dir, CHARM_NAME)
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value=""):
            result = ext.build_charm(charm_dir)
        assert result.parent != charm_dir

    def test_raises_runtime_error_on_build_failure(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        error = subprocess.CalledProcessError(1, "charmcraft pack", output="out", stderr="err")
        with patch("jubilant_adapters.adapters.subprocess.check_output", side_effect=error):
            with pytest.raises(RuntimeError, match="Failed to build charm"):
                ext.build_charm(charm_dir)

    def test_runtime_error_includes_charm_path(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        error = subprocess.CalledProcessError(1, "charmcraft pack", output="", stderr="")
        with patch("jubilant_adapters.adapters.subprocess.check_output", side_effect=error):
            with pytest.raises(RuntimeError, match=str(charm_dir)):
                ext.build_charm(charm_dir)

    def test_reads_log_file_on_build_failure(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        log_file = tmp_path / "build.log"
        log_file.write_text("detailed log contents")
        stderr_msg = f"Failed to build charm blah full execution logs in '{log_file}'"
        error = subprocess.CalledProcessError(1, "charmcraft pack", output="", stderr=stderr_msg)
        with patch("jubilant_adapters.adapters.subprocess.check_output", side_effect=error):
            with pytest.raises(RuntimeError, match="detailed log contents"):
                ext.build_charm(charm_dir)

    def test_missing_log_file_still_raises_runtime_error(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        stderr_msg = "Failed to build charm blah full execution logs in '/nonexistent/path/build.log'"
        error = subprocess.CalledProcessError(1, "charmcraft pack", output="", stderr=stderr_msg)
        with patch("jubilant_adapters.adapters.subprocess.check_output", side_effect=error):
            with pytest.raises(RuntimeError, match="Failed to build charm"):
                ext.build_charm(charm_dir)

    def test_raises_file_not_found_when_no_charms_produced(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        with patch("jubilant_adapters.adapters.subprocess.check_output", return_value=""):
            with pytest.raises(FileNotFoundError, match=r".*\.charm"):
                ext.build_charm(charm_dir)

    def test_use_cache_delegates_to_get_cached_build(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        expected = charm_dir / f"{CHARM_NAME}_amd64.charm"
        with patch.object(ext, "_get_cached_build", return_value=expected) as mock_cached:
            result = ext.build_charm(charm_dir, use_cache=True)
        mock_cached.assert_called_once_with(charm_path=charm_dir)
        assert result == expected


class TestGetCachedBuild:
    def test_returns_single_matching_charm(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        charm_file = _place_charm_file(charm_dir, CHARM_NAME, "amd64")
        with patch(
            "jubilant_adapters.adapters.subprocess.run",
            return_value=MagicMock(stdout="amd64\n"),
        ):
            result = ext._get_cached_build(charm_dir)
        assert result == charm_file.resolve()

    def test_arm64_architecture_is_accepted(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        charm_file = _place_charm_file(charm_dir, CHARM_NAME, "arm64")
        with patch(
            "jubilant_adapters.adapters.subprocess.run",
            return_value=MagicMock(stdout="arm64\n"),
        ):
            result = ext._get_cached_build(charm_dir)
        assert result == charm_file.resolve()

    def test_raises_when_no_charm_found(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        with patch(
            "jubilant_adapters.adapters.subprocess.run",
            return_value=MagicMock(stdout="amd64\n"),
        ):
            with pytest.raises(ValueError, match="Unable to find .charm file"):
                ext._get_cached_build(charm_dir)

    def test_raises_when_multiple_charms_found(self, ext, tmp_path):
        charm_dir = _make_charm_dir(tmp_path)
        _place_charm_file(charm_dir, CHARM_NAME, "amd64")
        _place_charm_file(charm_dir, "other-charm", "amd64")
        with patch(
            "jubilant_adapters.adapters.subprocess.run",
            return_value=MagicMock(stdout="amd64\n"),
        ):
            with pytest.raises(ValueError, match="More than one matching"):
                ext._get_cached_build(charm_dir)
