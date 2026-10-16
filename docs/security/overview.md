# Orbit NoSQL: security

`orbit-nosql` defines types and lifecycle expectations; it does not connect to a database or enforce
authorization. Secure transport, credentials, access control, query behavior, and stored data are
responsibilities of the chosen provider adapter and deployment.

## Data and authorization boundaries

Pydantic validation checks model shape, not whether a caller may access a record. Enforce tenant,
user, and administrative authorization in application services before invoking the repository.
Do not treat a collection name, key field, or successful model validation as an access-control
decision.

Treat model fields as potentially sensitive. Avoid credentials and access tokens in entity keys or
diagnostic text. Configure serializers and provider logging so secrets and personal data are not
written to logs or traces. Review BSON/JSON serialization behavior for custom model serializers and
aliases before storing sensitive fields.

## Provider configuration

Use a dedicated database identity with the minimum collection permissions required. Store and
rotate credentials through an approved secret-management mechanism. Require verified TLS for
remote database connections and review certificate handling, network allow-lists, pool limits,
encryption-at-rest, backup protection, and retention in the provider package and deployment.

## Failure and lifecycle behavior

`RepositoryConflictError` has a fixed provider-neutral message. Other failures are provider-specific;
applications must avoid logging raw exceptions when the driver may include query values, document
contents, connection strings, or credentials. Close the database during application shutdown and
verify cleanup behavior after cancellation and provider errors.

## Vulnerability reporting

Follow the repository [security policy](../../SECURITY.md) for private reporting. This guidance
does not certify any provider adapter or deployment as secure.
