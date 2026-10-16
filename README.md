# Orbit NoSQL

`orbit-nosql` is the provider-neutral NoSQL capability layer. `orbit-data` is the common repository
contract shared by SQL and NoSQL implementations. This package defines how an application obtains
an `orbit_data.Repository` for a named logical collection, using a Pydantic model as the entity
type, without importing a vendor driver.

Providers live in separate packages. `orbit-nosql-mongo` supplies a document collection implementation;
`orbit-cache-redis` may expose a key-value backed repository alongside its separate cache capability.
The capability does not claim that transactions, secondary indexes, query languages, consistency,
or collection semantics are identical across NoSQL systems. Provider-specific features remain
explicit on their provider packages.

```python
from pydantic import BaseModel
from orbit_nosql import NoSQLDatabase


class Session(BaseModel):
    id: str
    owner_id: str


async def load_session(database: NoSQLDatabase, session_id: str) -> Session | None:
    sessions = database.repository("sessions", Session)
    return await sessions.get(session_id)
```

The returned repository follows `orbit-data` CRUD semantics. Its `list(limit=...)` operation is one
bounded read, not cursor pagination. This capability does not promise cross-provider query
languages, transaction support, index management, or consistent ordering across calls. Provider
packages own client startup, configuration, and shutdown. Close the database with
`await database.aclose()` or register it as an application-managed resource. Successful close is
idempotent. Concurrent close callers wait for the same cleanup, and cancellation of a caller is
propagated after owned resource cleanup finishes. Repositories created from a database are valid
only while that database resource remains open.

```bash
pip install orbit-data orbit-nosql orbit-nosql-mongo
```

This package is in alpha and its API is not stable. It declares support for Python 3.11 through
3.14; see CI results for the Python versions actually validated by each change.

Licensed under Apache-2.0.

## Documentation

The package-specific guides cover [architecture](docs/architecture/overview.md), [operations and security](docs/operations/README.md), and [development](docs/development/README.md), with [security guidance](docs/security/overview.md). The [documentation index](docs/README.md) links to the full package overview and project policies.

