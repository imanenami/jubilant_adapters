"""Shared fixtures for adapter tests."""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_juju() -> MagicMock:
    """A MagicMock standing in for a `jubilant.Juju` client."""
    return MagicMock()
