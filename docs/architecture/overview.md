# Orbit NoSQL: architecture and contracts

## Package boundaries

`orbit-nosql` is the provider-neutral capability for NoSQL collection repositories. `orbit-data`
provides the CRUD protocol shared by SQL and NoSQL implementations. This package defines how an
application obtains a typed repository for a logical collection and how the database resource is
closed; it contains no database driver, connection pool, credentials, or Core integration.

```text
application module
       │ NoSQLDatabase / Repository[Model, Key]
       ▼
 orbit-nosql ─────────────── orbit-data
       ▲
       │ implements this capability
 orbit-nosql-mongo ─────── MongoDB async client
```

Provider packages own their SDK, connection configuration, error handling, native query features,
and provider-specific lifecycle. Core may manage a provider resource through its container, but
neither Core nor this contract starts a provider implicitly. A Redis-backed key/value repository
must also keep Redis-specific semantics visible; sharing a CRUD interface does not make Redis a
document database.

## Models and logical collections

The current contract uses Pydantic `BaseModel` subclasses for entities. This gives providers a
common validation and serialization boundary. It also means callers must account for Pydantic's
serialization rules and provider restrictions; a type annotation alone does not guarantee that
every Python value can be represented in every backend.

`NoSQLDatabase.repository(collection, model, key_field="id")` synchronously returns a facade that
implements `orbit_data.Repository`. The call is for dependency wiring and is not a connection or
readiness check. Providers must validate collection and key-field names and document whether
collection access creates anything remotely. `key_field` identifies the entity property used as
the repository key; adapters document how it maps to their native key representation.

```python
from pydantic import BaseModel
from orbit_nosql import NoSQLDatabase


class Session(BaseModel):
    id: str
    owner_id: str


def session_repository(database: NoSQLDatabase):
    return database.repository("sessions", Session)


async def load_session(database: NoSQLDatabase, session_id: str) -> Session | None:
    return await session_repository(database).get(session_id)
```

The CRUD method semantics come from the separately installed `orbit-data` dependency. The shared
NoSQL layer does not add filters, cursor pagination, ordering,
transactions, indexes, watches, or multi-document guarantees.

## Resource lifecycle

The provider database owns its client or pool. Application shutdown must call and await
`aclose()`. Successful close is idempotent; concurrent close calls wait for the same cleanup, and
cancelling a waiter must not abandon resource release. Repositories are tied to the database
resource and are invalid after close. A concrete adapter documents what happens when provider
cleanup itself fails.

When Core manages the provider, register the database as one application-scoped resource and let
Core own the shutdown call. Avoid separately closing the same provider client from both application
lifespan and a module teardown hook.

## Explicitly provider-specific behavior

Do not infer a common query language, transaction scope, isolation level, consistency model,
collection creation policy, secondary-index behavior, pagination guarantees, or durability from
this interface. If an application needs one of those features, use a provider-specific API or an
additional capability whose contract defines it. Record any loss of portability at the call site.

## Source layout and compatibility

- `src/orbit_nosql/contracts.py`: `NoSQLDatabase` structural protocol.
- `src/orbit_nosql/__init__.py`: stable import surface for this alpha version.

The project declares Python `>=3.11,<3.15`, Pydantic `>=2.8,<3`, and `orbit-data>=0.1.0a1,<0.2`.
Its API is in alpha and can change before a stable release. See `pyproject.toml` for the
authoritative dependency and version declarations.
