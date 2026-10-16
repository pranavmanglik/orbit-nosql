"""Structural contract tests for NoSQL provider resources."""

import inspect
from inspect import iscoroutinefunction
from typing import get_args, get_origin, get_type_hints

from orbit_data import Repository

from orbit_nosql import NoSQLDatabase


class _Database:
    def repository(self, collection, model, *, key_field="id"):
        raise NotImplementedError

    async def aclose(self):
        return None


def test_database_protocol_is_structural() -> None:
    """NoSQL adapters satisfy the contract without inheriting implementation classes."""
    assert isinstance(_Database(), NoSQLDatabase)
    result = get_type_hints(NoSQLDatabase.repository)["return"]
    assert get_origin(result) is Repository
    assert len(get_args(result)) == 2


def test_repository_creation_is_synchronous_and_defaults_to_id_key() -> None:
    """Adapters return a lightweight repository facade and use the conventional key field."""
    parameters = inspect.signature(NoSQLDatabase.repository).parameters
    assert parameters["collection"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert parameters["model"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert parameters["key_field"].default == "id"
    assert not iscoroutinefunction(NoSQLDatabase.repository)


def test_database_cleanup_is_async() -> None:
    """Provider-owned clients are released through an awaitable lifecycle method."""
    assert iscoroutinefunction(NoSQLDatabase.aclose)
