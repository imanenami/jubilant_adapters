"""Tests for jubilant_adapters.typedefs."""

from jubilant_adapters.typedefs import RelationInfo


def test_endpoints_returns_both_sides():
    rel = RelationInfo(app="kafka", endpoint="cluster", related_endpoint="cluster", raw={})
    endpoints = rel.endpoints
    assert [e.name for e in endpoints] == ["cluster", "cluster"]


def test_id_returns_relation_id_from_raw():
    rel = RelationInfo(app="kafka", endpoint="e1", related_endpoint="e2", raw={"relation-id": 5})
    assert rel.id == 5


def test_id_returns_none_when_missing():
    rel = RelationInfo(app="kafka", endpoint="e1", related_endpoint="e2", raw={})
    assert rel.id is None


def test_is_peer_true_when_related_units_share_app():
    rel = RelationInfo(
        app="kafka",
        endpoint="cluster",
        related_endpoint="cluster",
        raw={"related-units": {"kafka/1": {}, "kafka/2": {}}},
    )
    assert rel.is_peer is True


def test_is_peer_false_when_related_units_are_different_app():
    rel = RelationInfo(
        app="kafka",
        endpoint="kafka-client",
        related_endpoint="kafka-client-consumer",
        raw={"related-units": {"app/0": {}}},
    )
    assert rel.is_peer is False


def test_requires_builds_app_from_first_related_unit():
    rel = RelationInfo(
        app="kafka",
        endpoint="kafka-client",
        related_endpoint="kafka-client-consumer",
        raw={"related-endpoint": "kafka-client-consumer", "related-units": {"app/0": {}}},
    )
    requires = rel.requires
    assert requires.name == "kafka-client-consumer"
    assert requires.application_name == "app"


def test_requires_defaults_when_no_related_units():
    rel = RelationInfo(app="kafka", endpoint="e1", related_endpoint="e2", raw={})
    requires = rel.requires
    assert requires.name == ""
    assert requires.application_name == ""
