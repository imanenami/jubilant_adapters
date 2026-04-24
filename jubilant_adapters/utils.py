"""Utility & helpers module."""

import logging
from collections.abc import Iterable
from typing import cast

import jubilant
import jubilant_backports as compat

from ._juju_version import JUJU_MAJOR_VERSION
from .typedefs import CT

logger = logging.getLogger(__name__)


def all_statuses_are(expected: str, status: CT.Status, apps: Iterable[str]) -> bool:
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


def all_active_idle(status: CT.Status, *apps: str) -> bool:
    """Return True if all units are active|idle."""
    if JUJU_MAJOR_VERSION == 2:
        status = cast(compat.Status, status)
        return compat.all_agents_idle(status, *apps) and compat.all_active(status, *apps)
    status = cast(jubilant.Status, status)
    return jubilant.all_agents_idle(status, *apps) and jubilant.all_active(status, *apps)


def all_agents_idle(status: CT.Status, *apps: str) -> bool:
    """Report whether all unit agents in *status* (filtered to *apps* if provided) are "idle"."""
    if JUJU_MAJOR_VERSION == 2:
        status = cast(compat.Status, status)
        return compat.all_agents_idle(status, *apps)
    status = cast(jubilant.Status, status)
    return jubilant.all_agents_idle(status, *apps)


def any_error(status: CT.Status, *apps: str) -> bool:
    """Report whether any app or unit in *status* (or in *apps* if provided) is "error"."""
    if JUJU_MAJOR_VERSION == 2:
        status = cast(compat.Status, status)
        return compat.any_error(status, *apps)
    status = cast(jubilant.Status, status)
    return jubilant.any_error(status, *apps)
