# ADR 003 – Manage the Unit of Work (UoW) at the Controller Layer
## Status

**Accepted** — 2025-11-27
This decision defines how transactional boundaries are created across all modules.

## Context

In a Clean Architecture + DDD + Modular Monolith system using FastAPI + SQLAlchemy 2.0 (async), we must define **where and how a Unit of Work (UoW)** should be initialized and controlled.

We have these requirements:

- Ensure **transactional consistency** across multiple repositories within a use case

- Prevent partial writes when multiple repository calls occur

- Ensure **atomic operations** within API requests

- Maintain a clear separation between:

- Domain layer (no knowledge of transactions)

- Application layer (use cases, orchestration)

- Infrastructure layer (repositories, DB persistence)

- Avoid implicit hidden transactions

- Allow future migration to:

- Event sourcing

- Saga patterns

- Distributed UoW across microservices

The question:
**Where should the Unit of Work be instantiated and managed?**

Options evaluated:

- **Inside each repository**

- **Inside the application service/use case**

- **Inside a global middleware**

- **At the controller layer** (per-request scope)

## Decision

We will **create and manage the Unit of Work at the Controller Layer**, per HTTP request.

### This means:

- Controller initializes UoW (dependency injection)

- Controller passes UoW into application service / use case

- Use cases retrieve repositories from UoW

- Upon completion of the use case:

- Controller commits or rolls back the UoW

- UoW is scoped to one request, ensuring atomicity

## Rationale
### 1. Prevent repositories from silently managing transactions

If each repository manages its own session:

- No single transaction context

- Cannot ensure atomicity across multiple repository calls

- Leads to inconsistent writes


Managing UoW inside repositories is an anti-pattern.

### 2. Application services should be pure orchestration

Use cases should not:

- Open/close DB sessions

- Commit transactions

- Manage infrastructure concerns

Clean Architecture principle:

- Application layer should not know how persistence works.

### 3. Using middleware to manage UoW lacks fine-grained commit control

Middleware-based transactions:

- Cannot selectively commit/rollback

- Harder to debug in multi-step use cases

- Does not work well for streaming / long-running workflows

- Forces all requests into one transaction, even read-only

Middlewares are too generic for domain-driven logic.

### 4. Controllers naturally represent request boundaries

HTTP request boundary = Transaction boundary.

A controller is the ideal place to:

- Start UoW

- Pass it downward

- Commit or rollback based on use-case success or exception

This matches common enterprise standards.

### 5. Explicit dependency injection

Controller-level UoW aligns perfectly with FastAPI design:

This ensures:

- Clean DI

- Single transaction

- Explicit transaction ownership

- Easy testability

### 6. Supports future microservices migration

If later we move to microservices:

- The controller-level UoW maps cleanly to API gateway responsibilities

- Each service maintains its own atomic transaction

- Easy adoption of sagas and distributed UoW

## Alternatives Considered
### Option A: UoW inside repositories (Rejected)

**Cons**

- No global transaction

- Risk of partial writes

- Violates DDD + repository patterns

- Repositories too “smart” → hard to test

**Reason Rejected:**
Breaks atomicity and violates architecture principles.

### Option B: UoW inside application service/use case (Rejected)

**Pros**

- Close to business logic

**Cons**

- Adds infrastructure responsibility to use cases

- Mixes concerns

- Makes use cases hard to test

- Prevents multiple use cases from sharing a transaction

**Reason Rejected:**
Breaks Clean Architecture layering.

### Option C: UoW handled globally in framework middleware (Rejected)

**Pros**

- Transparent

- Automatically applied

**Cons**

- Cannot handle fine-grained commits

- Hard to support multi-step domain logic

- Overly generic

- Unexpected behavior for developers

**Reason Rejected:**
Not aligned with domain-event-driven flows.

### Option D: UoW controlled at controller level (Accepted)

**Pros**

- Clear transaction boundary

- Explicit DI

- Full control over commit/rollback

- Cleanest separation of layers

- Use cases stay business-focused

- Repositories stay persistence-focused

**Reason Accepted:**
Best alignment with Clean Architecture, DDD, and FastAPI design.

## Consequences
### Positive

- Guaranteed atomicity per request

- Clear boundary responsibility

- Simple, predictable transactional behavior

- Use cases remain pure and testable

- Repositories remain simple (no transaction logic)

- Easy debugging and monitoring

- Future microservice migration friendly

### Negative

- Controller logic becomes slightly more verbose

- Developers must follow DI convention strictly

- Need consistent template across all modules

## Decision Outcome

We standardize on:

- UoW = created at controller

- Repository instances = created inside UoW

- Service/use case = receives UoW as a parameter

- Controller commits or rolls back the UoW

- No repository or service may control transactions

This pattern becomes mandatory across all modules.

## References

- Martin Fowler – Unit of Work Pattern

- Robert C. Martin – Clean Architecture

- Eric Evans – Domain-Driven Design

- SQLAlchemy Unit of Work patterns

- FastAPI DI and lifespan docs