# Copyright 2026-present Orbit Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Provider-neutral NoSQL resource contract built on Orbit's shared data repository."""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from orbit_data import Repository
from pydantic import BaseModel

EntityT = TypeVar("EntityT", bound=BaseModel)
KeyT = TypeVar("KeyT", contravariant=True)


@runtime_checkable
class NoSQLDatabase(Protocol):
    """Create typed repositories for Pydantic models in logical collections.

    ``repository`` is a synchronous factory for a lightweight facade; it does not promise that a
    remote collection exists or that schema/index setup has completed. Implementations validate
    collection and key-field names and must document whether requesting a repository can create a
    collection or make a network request. The model is a Pydantic ``BaseModel`` subclass used for
    document validation and serialization; providers must document any restrictions on supported
    field types, aliases, custom serializers, and key conversion.

    A returned repository must satisfy ``orbit_data.Repository`` and is bound to this database's
    lifecycle. It must not be retained or used after the database is closed. The database owns its
    client or pool and releases it through ``aclose``. Successful close is idempotent; concurrent
    callers must await the same cleanup operation. Caller cancellation must not abandon owned
    resource cleanup, although it must eventually propagate to the caller.

    This contract does not unify query/filter languages, transactions, index management,
    collection creation, read consistency, ordering, pagination, or durability. These are
    provider-specific capabilities and must not be inferred from the shared CRUD repository.
    """

    def repository(
        self,
        collection: str,
        model: type[EntityT],
        *,
        key_field: str = "id",
    ) -> Repository[EntityT, KeyT]:
        """Return a typed CRUD facade for ``collection`` and ``model``.

        ``collection`` names one provider collection, while ``key_field`` identifies the entity
        field used by ``Repository.get``, ``update``, and ``delete``. The default is ``"id"``.
        Implementations should validate both strings and define how the selected field maps to the
        provider's native key (for example a MongoDB document's ``_id``). This method is
        synchronous so object wiring does not require network I/O; provider initialization and
        connectivity checks belong to construction or explicit health checks.
        """

    async def aclose(self) -> None:
        """Release this database's client or pool and wait for cleanup to finish.

        Concurrent callers await the same close operation. A successful close is idempotent.
        Cancellation of a caller must not abandon the owned cleanup task; after cleanup completes,
        cancellation propagates. Provider cleanup failures remain visible, but their messages must
        not contain credentials or other sensitive configuration.
        """


__all__ = ["NoSQLDatabase"]
