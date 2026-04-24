import json
import subprocess
from dataclasses import dataclass


def _execute(cmd, cwd: str | None = None, env: dict | None = None, timeout: int = 120) -> str:
    """Execute a command using shell and raise on error."""
    return subprocess.check_output(
        cmd,
        shell=True,
        universal_newlines=True,
        stderr=subprocess.PIPE,
        cwd=cwd,
        env=env,
        timeout=timeout,
    )


@dataclass
class JujuController:
    """Juju controller data repr."""

    name: str
    version: str

    @property
    def major_version(self) -> int:
        """Return the major Juju version."""
        return int(self.version.split(".")[0])


def get_current_controller() -> JujuController | None:
    """Return the current Juju controller."""
    try:
        raw = _execute("juju controllers --format json")
    except subprocess.CalledProcessError:
        return None
    _json = json.loads(raw)
    current_controller = _json.get("current-controller", "")
    if not current_controller:
        return None
    return JujuController(
        name=current_controller,
        version=_json.get("controllers", {}).get(current_controller, {}).get("agent-version"),
    )


JUJU_CONTROLLER = get_current_controller()
JUJU_MAJOR_VERSION = JUJU_CONTROLLER.major_version if JUJU_CONTROLLER else 3
