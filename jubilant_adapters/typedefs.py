"""Type and Data Class definitions."""

import logging
from dataclasses import dataclass
from typing import Any, TypedDict

import jubilant
import jubilant_backports as compat

logger = logging.getLogger(__name__)


def _unit_name_to_app(name: str) -> str:
    """Convert unit name to app name."""
    return name.split("/")[0]


class CT:
    """Python types defined for compatibility reasons."""

    ConfigValue = jubilant.ConfigValue | compat.ConfigValue
    Constraints = Any
    Devices = Any
    Juju = jubilant.Juju | compat.Juju
    ShowUnitOutput = dict
    Status = jubilant.Status | compat.Status
    Task = jubilant.Task | compat.Task | compat.ExecTask

    class StorageInfo(TypedDict):
        """JSON type of Storage returned by `juju list-storage`."""

        key: str
        attachments: dict[str, dict]
        kind: str
        life: str
        persistent: bool


@dataclass
class Endpoint:
    """Data model for endpoint info of a relation."""

    name: str


@dataclass
class RequiresInfo:
    """Data model for requires info of a relation."""

    application_name: str
    name: str


@dataclass
class RelationInfo:
    """Data model for `juju show-unit`:`relation-info` section."""

    app: str
    endpoint: str
    related_endpoint: str
    raw: dict[str, Any]

    @property
    def endpoints(self) -> list[Endpoint]:
        """Relation endpoints."""
        return [Endpoint(self.endpoint), Endpoint(self.related_endpoint)]

    @property
    def id(self) -> int | None:
        """Relation Identifier."""
        return self.raw.get("relation-id")

    @property
    def is_peer(self) -> bool:
        """Is this a peer relation?"""
        apps = {_unit_name_to_app(unit_name) for unit_name in self.raw["related-units"]}
        return not bool(apps - {self.app})

    @property
    def requires(self) -> RequiresInfo:
        """Return the requires side info of the relation."""
        name = self.raw.get("related-endpoint", "")
        app = ""
        if related_units := self.raw.get("related-units", {}):
            app = _unit_name_to_app(next(iter(related_units)))

        return RequiresInfo(name=name, application_name=app)
