# Orbit NoSQL: operations

This package defines a provider contract and has no runtime connection settings of its own. Install
`orbit-data`, `orbit-nosql`, and the selected provider adapter separately. Configure endpoints,
credentials, TLS, pools, timeouts, retries, and health checks through that adapter's documented
configuration; there are no `ORBIT_*` environment variables defined here.

## Application wiring

Construct and validate the provider database during application startup, then register it as an
application-scoped managed resource when using Core. The owning application must await
`database.aclose()` during shutdown. The provider's README should describe startup behavior, health
checking, and cleanup failure semantics. Repository facades are cheap synchronous objects, but
their operations depend on the live database resource.

Avoid closing one provider client from multiple independent lifecycle hooks. This interface
requires concurrent close callers to join the same cleanup and caller cancellation not to abandon
resource release.

## CRUD, limits, and scale

The returned repository follows `orbit-data` semantics for `get`, `list`, `add`, `update`, and
`delete`. `list(limit=...)` is a bounded single read; it is not cursor pagination, does not promise
an ordering across calls, and does not provide a cross-call snapshot. Providers should impose a
finite maximum list size. Use a vendor-supported cursor, streaming query, or export tool for large
collections and document the provider dependency.

The capability does not define multi-document transactions, consistency levels, write concern,
index creation, automatic schema creation, retries, or durability. Confirm the specific adapter's
behavior before depending on those guarantees. Retry only operations that are safe under the
provider's idempotency and consistency model.

## Readiness and failure handling

Creating a repository facade is synchronous and is not evidence that the database is reachable or
the collection exists. Use an explicit provider health check or a bounded startup operation if the
application must fail fast. Avoid unbounded startup retries. Translate errors at the application
boundary without logging credentials, complete documents, query parameters, or raw provider
response bodies.

## Pre-release operational checks

In a disposable environment using the actual adapter, validate connection limits, timeout behavior,
cancelled operations, shutdown while work is in flight, client cleanup, and provider-specific
consistency and durability expectations. Exercise backup and restore, index deployment, and
credential rotation according to the backend. Contract tests in this repository do not validate a
live database.
