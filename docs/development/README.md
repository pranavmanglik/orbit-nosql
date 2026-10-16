# Orbit NoSQL: development

This repository owns one small shared capability protocol. Keep provider behavior out of this
package and coordinate contract changes with every provider checkout that implements
`NoSQLDatabase`, including Python and non-Python adapters that expose the same published service
contract.

## Local setup and checks

From the repository root:

```bash
python -m pip install -e '.[dev]' build
pytest
ruff check src tests
ruff format --check src tests
mypy
python -m build
```

Tests here are structural contract tests and do not require MongoDB or another NoSQL service. They
do not prove that a concrete adapter validates inputs, closes resources safely, or honors the
shared repository semantics. Validate those behaviors in each adapter's own test suite.

## Contract changes

Before changing `NoSQLDatabase`, inspect its provider consumers and state which compatibility
guarantees all of them must implement. Keep the synchronous repository factory free of network
I/O; put connection establishment and readiness checks in provider construction or explicit
health APIs. Preserve the provider-neutral entity and key types, and document where provider
serialization or key representations constrain them.

Add focused tests for structural conformance, method sync/async shape, defaults, and public exports.
When behavior changes, update the README, API docstrings, architecture, operations, security, and
development guidance together. Include migration notes for affected adapters, even during
alpha, so maintainers can update the ecosystem coherently.

## Contribution and release evidence

Follow the repository contribution guide, code of conduct, governance, and security policy. Keep
examples runnable and fixtures free of real credentials or production records. Report exact local
checks and versions; do not infer hosted CI, provider compatibility, or production readiness from
this package's protocol checks alone.
