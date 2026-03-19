"""Utility & helpers module."""

import logging
from collections.abc import Iterable

from jubilant import (
    Status,
    all_active,
    all_agents_idle,
)

logger = logging.getLogger(__name__)


def all_statuses_are(expected: str, status: Status, apps: Iterable[str]) -> bool:
    """Return True if all units and apps have the `expected` status."""
    if not apps:
        apps = status.apps

    for app in apps:
        app_info = status.apps.get(app)
        if app_info is None:
            return False
        if app_info.app_status.current != expected:
            return False
        for unit_info in status.get_units(app).values():
            if unit_info.workload_status.current != expected:
                return False
    return True


def all_active_idle(status: Status, *apps: str) -> bool:
    """Return True if all units are active|idle."""
    return all_agents_idle(status, *apps) and all_active(status, *apps)


def unit_name_to_app(name: str) -> str:
    """Convert unit name to app name."""
    return name.split("/")[0]
