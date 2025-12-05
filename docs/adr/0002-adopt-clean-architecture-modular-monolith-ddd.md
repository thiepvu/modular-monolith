# ADR 002 – Adopt a Clean Architecture Modular Monolith with Domain-Driven Design (DDD)
## Status

**Accepted** — 2025-11-27
This decision defines the system-wide architectural foundation, applicable to all backend services and domains.

## Context

**We need a backend architecture that:**

- Can scale across **multiple domains** (Users, Files, Projects, Auth, Notifications…)

- Supports **high complexity** with long-term maintainability

- Enforces clear boundaries between business logic and infrastructure

- Supports future scaling into separate services or bounded contexts if needed

- Minimizes accidental coupling between modules

- Promotes high cohesion inside each domain

- Avoids premature microservices complexity

- Enables parallel team development

- Ensures predictable behavior and low technical debt

**The business roadmap suggests:**

- 5–10 domains immediately

- 20+ modules in long term

- Multi-team parallel development

- Event-driven integration (Kafka or RabbitMQ)

- High API throughput

**We must select an architecture that:**

- Encourages domain modeling

- Separates application layers clearly

- Allows modules to evolve independently

- Scales vertically first, horizontally later

- Avoids microservices pitfalls (distributed transactions, complexity, infra overhead)

Two main approaches were considered:

1. **Microservices from day one**

2. **Modular Monolith with Clean Architecture + DDD**

## Decision

We adopt a **Clean Architecture Modular Monolith** following **Domain-Driven Design (DDD)** principles.

Key aspects:

- System is **one deployable application** (monolith)

- Codebase is divided into **bounded contexts** (modules)

- Each module has its **own internal Clean Architecture layers**:

- **Domain layer** (Entities, Aggregates, Value Objects, Domain Events)

- **Application layer** (Use Cases, DTO, Services)

- **Infrastructure layer** (ORM, DB, external systems, repositories)

- **Presentation layer** (Controllers, API endpoints)

Modules communicate via:

- **Domain Events**

- **Application Services**

- **Publish/subscribe patterns**

- No module is allowed to reach into another module’s domain logic directly

- Most dependencies point inward toward the domain (as Clean Architecture dictates)

- Future microservices can be extracted by splitting modules out

This is the **foundation** for long-term enterprise-level architecture.

## Rationale
### 1. Better Manage Complex Business Logic

- Clean Architecture isolates the core business logic.

- Business logic becomes framework-agnostic

- No HTTP, no ORM logic inside domain or application core

- Entities and aggregates remain pure and testable

- Use cases are deterministic and isolated

This is essential for systems like CRM/ERP/WMS where rules are dynamic and complex.

### 2. Avoid Premature Microservices

- Microservices from day 1 create unnecessary problems:

- Distributed transactions

- Eventual consistency everywhere

- DevOps + infra overhead

- Difficult debugging across services

- Cross-service data synchronization

- Increased latency

- Too many repos, pipelines, containers

A modular monolith avoids those until the system and team are mature.

### 3. Enforce Clear Module Boundaries

Each module is a bounded context, for example:

/modules
   /auth
   /user
   /file
   /project
   /notification


Each contains **its own domain model and application logic.**

This provides:

- High cohesion

- Low coupling

- Independent evolution

- Easy team separation

- Easier long-term scaling

You get **microservice-like isolation** without distributed complexity.

### 4. Clean Architecture is Ideal for Long-Term Maintainability

It ensures:

- UI/Transport frameworks can change without touching business logic

- Database implementations can be replaced (PostgreSQL → MySQL → NoSQL)

- Domain logic is not tied to infrastructure details

- New modules/contexts can be added easily

- Easy unit testing due to isolated pure logic

- This boosts maintainability for 5–10 years.

### 5. DDD Helps With Complex Domain Modeling

We need:

- Aggregates

- Value Objects

- Domain Events

- Repositories

- Domain Services

These patterns help manage complexity in:
- User management flow
- File management flow
- Project management flow
- Tasks pipeline flow

### 6. Easy Path to Microservices Later

If scaling requires splitting modules into microservices, each module’s boundaries are already:

- Clear

- Explicit

- Self-contained

- Independent

- Extraction becomes straightforward:

- Move module folder → into new repo

- Create API around existing use cases

- Keep domain model unchanged

This is microservices by evolution, not by force.

### 7. Aligns With Modern Python Stack (FastAPI + SQLAlchemy + Pydantic)

FastAPI fits perfectly:

- Layered architecture

- Dependency injection

- Routers per module

- Application services as dependencies

- Event handlers

- Pydantic models for request/response

SQLAlchemy also fits:

- Repositories

- Unit of Work pattern

- Infrastructure layers

- Async pipelines

This combination naturally supports Clean Architecture.

## Alternatives Considered
### Option A: Microservices Architecture (Rejected)

**Pros**

- Independent deployability

- Team autonomy

- Fine-grained scaling

**Cons**

- Operational complexity

- Network latency

- Debugging difficulty

- Expensive infra

- Harder local development

- Distributed transactions and consistency issues

**Reason Rejected:**
Team size and domain requirements do not justify the massive overhead.

### Option B: Traditional Monolith Without Modular Boundaries (Rejected)

**Pros**

- Easy to implement initially

- Fast initial development

**Cons**

- Hard to scale as complexity grows

- Logic leaks across modules

- Poor separation of concerns

- Technical debt accumulates fast

- Difficult to extract future microservices

**Reason Rejected:**
Not maintainable for enterprise-grade systems.

### Option C: MVC Framework Coupled Architecture (Django-style) (Rejected)

**Pros**

- Rapid CRUD development

- Strong ecosystem

**Cons**

- Tight coupling: Model = DB = Business logic

- Hard to enforce clean module boundaries

- Violates domain purity (fat models, fat views)

- Difficult DDD modeling

**Reason Rejected:**
Not suitable for enterprise Clean Architecture + DDD goals.

## Consequences
### Positive

- Highly modular, maintainable codebase

- Business logic independent of frameworks

- Strong encapsulation and boundaries

- Easier testing

- Smooth transition to microservices later

- Clear separation of domain/application/infrastructure

- Teams can work on modules independently

- Robust long-term design suitable for 5–10 years of growth

### Negative / Trade-offs

- Requires stricter coding standards

- More boilerplate than a simple MVC framework

- Team must understand DDD and Clean Architecture principles

- Requires architects to enforce boundaries

- Might feel slower initially

- Needs more code reviews for consistency

## Decision Outcome

The **Clean Architecture Modular Monolith with DDD** becomes the mandatory architectural foundation.

It ensures:

- Long-term scalability

- Predictability

- Maintainability

- Enterprise-grade domain modeling

- Clear evolution path into microservices

All future modules must follow the standard 4-layer structure.

## References

- Robert C. Martin – Clean Architecture

- Eric Evans – Domain-Driven Design

- Vernon – Implementing DDD

- ThoughtWorks Technology Radar – Modular Monoliths

- FastAPI documentation

- SQLAlchemy architecture guidelines