"""Jubilant adapters."""

import logging
import secrets
import subprocess
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from typing import Any

from adapters import LegacyExtensions
from jubilant import (
    CLIError,
    ConfigValue,
    Juju,
)

logger = logging.getLogger(__name__)


def gather(*calls: Any) -> None:
    """Placeholder function to replace asyncio.gather calls."""
    pass


class JujuFixture(Juju):
    """Juju Fixture object with legacy extension."""

    def __init__(self, *, model=None, wait_timeout=3 * 60, cli_binary=None):
        super().__init__(model=model, wait_timeout=wait_timeout, cli_binary=cli_binary)

    @property
    def ext(self) -> LegacyExtensions:
        """pytest-operator & python-libjuju extensions."""
        return LegacyExtensions(self)

    def old_cli(self, *cmd: str, **kwargs: Any) -> tuple[int, str, str]:
        """Old method signature compatible with `ops_test.juju`."""
        try:
            stdout = self.cli(*cmd)
            stderr = ""
            returncode = 0
        except CLIError as e:
            stdout = e.output
            stderr = e.stderr
            returncode = e.returncode

        return returncode, stdout, stderr

    juju = old_cli


@contextmanager
def temp_model_fixture(
    keep: bool = False,
    controller: str | None = None,
    cloud: str | None = None,
    config: Mapping[str, ConfigValue] | None = None,
    credential: str | None = None,
) -> Generator[JujuFixture]:
    """Context manager to create a temporary model for running tests in."""
    juju = JujuFixture()
    model = "jubilant-" + secrets.token_hex(4)  # 4 bytes (8 hex digits) should be plenty
    juju.add_model(model, cloud=cloud, controller=controller, config=config, credential=credential)
    try:
        yield juju
    finally:
        if not keep:
            assert juju.model is not None
            try:
                # We're not using juju.destroy_model() here, as Juju doesn't provide a way
                # to specify the timeout for the entire model destruction operation.
                args = ["destroy-model", juju.model, "--no-prompt", "--destroy-storage", "--force"]
                juju._cli(*args, include_model=False, timeout=10 * 60)
                juju.model = None
            except subprocess.TimeoutExpired as exc:
                logger.error(
                    "timeout destroying model: %s\nStdout:\n%s\nStderr:\n%s",
                    exc,
                    exc.stdout,
                    exc.stderr,
                )
