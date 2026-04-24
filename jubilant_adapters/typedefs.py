"""Type and Data Class definitions."""

import logging
from dataclasses import dataclass
from typing import Any, TypedDict

from .utils import unit_name_to_app

logger = logging.getLogger(__name__)


class CT:
    """Python types defined for compatibility reasons."""

    Constraints = Any
    Devices = Any
    ShowUnitOutput = dict

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
        apps = {unit_name_to_app(unit_name) for unit_name in self.raw["related-units"]}
        return not bool(apps - {self.app})

    @property
    def requires(self) -> RequiresInfo:
        """Return the requires side info of the relation."""
        name = self.raw.get("related-endpoint", "")
        app = ""
        if related_units := self.raw.get("related-units", {}):
            app = unit_name_to_app(next(iter(related_units)))

        return RequiresInfo(name=name, application_name=app)
