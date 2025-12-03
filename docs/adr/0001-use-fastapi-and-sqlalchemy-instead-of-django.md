# ADR 001 – Use FastAPI & SQLAlchemy Instead of Django
## Status

**Accepted** — 2025-11-27
This decision is approved and forms part of the core technical architecture.

## Context

We need to choose a **backend framework and ORM** for our next-generation platform, which must support:

- High-performance APIs (sync + async capable)

- Clear separation of layers for Clean Architecture / DDD

- Modular structure for multi-domain systems (CRM, WMS, ERP…)

- Flexibility to choose custom components (auth, admin, background jobs…)

- Excellent developer experience and rapid iteration

- Scalability for high-traffic, API-heavy workloads

- Ability to integrate seamlessly with modern tooling (Pydantic, OpenAPI, async workers, microservices patterns)

Two major options were evaluated:

1. **Django + Django ORM**

2. **FastAPI + SQLAlchemy (with Pydantic)**

Django provides batteries-included features (admin, ORM, forms, auth), but its design is tightly coupled, synchronous-first, and less ideal for highly modular, microservice-aligned, event-driven, or API-centric architectures.

Our system prioritizes **API-first architecture**, domain-driven modularity, high throughput, maintainability, and long-term performance.

## Decision

We will adopt:

- **FastAPI** as the main backend web framework

- **SQLAlchemy** (2.0, async) as the ORM and data layer

- **Pydantic** (v2) for schema validation and serialization

- **Alembic** for migrations

This stack will be used to build a **Clean Architecture**–style **modular monolith** or **microservices**, depending on future scaling needs.

**Django will not be used** for this platform.

## Rationale
### 1. Performance & Async-First Architecture

FastAPI is designed around **ASGI**, providing:

- True async request handling

- High benchmark performance

- Lower latency and better concurrency

- Native integration with modern async libraries (httpx, aiokafka, redis async, etc.)

Django, while improving, is still fundamentally **WSGI + synchronous-first**, limiting concurrency and requiring workarounds for async performance.

### 2. Clean Architecture & DDD Alignment

FastAPI + SQLAlchemy allows total control over:

- Folder structure

- Domain layers (domain → application → infrastructure → API)

- Dependency injection

- Repository pattern

- Unit of Work pattern

- Event dispatching

Django enforces a monolithic "apps" model with hidden coupling via:

- Models tied tightly to the ORM

- Signals tied to persistence

- Business logic often leaking into models/views

- Limited flexibility for service layers

For complex enterprise systems, FastAPI provides **superior architectural freedom.**

### 3. SQLAlchemy Is More Powerful than Django ORM

SQLAlchemy provides:

- Fully expressive query builder

- Async ORM + Core

- Rich relationship configuration

- Better performance optimization (lazy/eager options)

- Database-agnostic advanced features

- Clear separation between ORM and domain models

Django ORM is simpler but more limiting:

- Harder to express advanced joins

- Limited async capability

- Model = business = persistence layer (tight coupling)

- Less suitable for DDD + repository patterns

### 4. API-First Development

FastAPI automatically generates:

- **OpenAPI docs**

- **Swagger UI**

- **ReDoc**

- **Request/response validation**

Django Rest Framework (DRF) is powerful, but:

- Requires heavy config

- Is slower

- Is not async-native

- Adds another layer of complexity on top of Django core

FastAPI’s built-in OpenAPI is **cleaner, faster, and more modern.**

### 5. Modularity & Microservice Alignment

FastAPI aligns well with:

- Modular monolith patterns

- Microservices

- Event-driven architectures

- Message brokers (Kafka, RabbitMQ, NATS)

- Async workers (Celery, RQ, Dramatiq async)

Django’s ecosystem is more oriented toward:

- Traditional monoliths

- Server-rendered applications

- Admin dashboards

### 6. Developer Experience

FastAPI provides:

- Modern Python type hints everywhere

- Pydantic validation

- Automatic API docs

- Lightweight, fast startup

- Flexible customization

Django offers speed of development for CRUD or admin-heavy apps, but becomes restrictive in enterprise-grade or system-integrator environments.

### 7. Ecosystem Flexibility



FastAPI allows us to choose best-in-class components:


| Component   | FastAPI Ecosystem                          | Django                           |
| ----------- | ------------------------------------------ | -------------------------------- |
| Auth        | Customizable (JWT, OAuth2, Keycloak, etc.) | Built-in, but rigid              |
| Admin       | Optional: React Admin, custom UI           | Built-in Admin (tightly coupled) |
| ORM         | SQLAlchemy                                 | Django ORM only                  |
| Task Queue  | Dramatiq, Celery, RQ                       | Celery (common, but sync)        |
| Repos & UoW | Easy                                       | Hard, unnatural                  |
| Event Bus   | Kafka, NATS, Rabbit                        | Not native                       |

FastAPI = choose optimal tools
Django = accept tight coupling

## Alternatives Considered
### Option A: Django + Django ORM (Rejected)

**Pros**

- Admin panel built-in

- Fast CRUD prototyping

- Mature ecosystem

- Great documentation

**Cons**

- Sync-first architecture is limiting

- Django ORM is less flexible

- Hard to apply Clean Architecture

- Tight coupling between model → view → ORM

- Heavy for API-only or service-oriented backends

- Does not align with microservices/cloud-native patterns

**Reason Rejected:**
Does not meet architectural flexibility, async performance goals, or DDD modularity needs.

### Option B: Django + DRF (Rejected)

**Pros**

- Powerful Serializer system

- Mature community

- Widely used in enterprise apps

**Cons**

- DRF adds another layer of complexity

- Still synchronous at the core

- Slow performance versus FastAPI

- Not suitable for async-heavy workloads (WebSockets, streaming)

**Reason Rejected:**
Clear performance and architecture limitations.

### Option C: Flask + SQLAlchemy (Rejected)

**Pros**

- Lightweight

- SQLAlchemy native

**Cons**

- No built-in validation

- No auto docs

- No async support

- Requires more boilerplate than FastAPI

**Reason Rejected:**
FastAPI provides everything Flask has + async + Pydantic + OpenAPI.

## Consequences
### Positive

- Better performance for API-heavy workloads

- Clean Architecture fits naturally

- More maintainable domain logic

- Easier scaling (worker pools, microservices)

- Future-proof async support

- Very strong OpenAPI and schema validation

- Flexible ecosystem for enterprise systems

- Better integration for modern DevOps (CI/CD, Docker, Kubernetes, autoscaling)

### Negative / Trade-offs

- No built-in admin panel (need custom UI or 3rd party)

- Requires more initial boilerplate

- Steeper learning curve for developers used to Django

- Must manage own architecture conventions (no framework "magic")

## Decision Outcome

FastAPI + SQLAlchemy is chosen as the backend foundation.
This aligns best with our architectural principles:

- Domain-Driven Design

- Clean Architecture

- API-first

- High-performance async applications

- Modularity for long-term growth

This decision will shape all future modules and domain design.

## References

- FastAPI Docs: https://fastapi.tiangolo.com/

- SQLAlchemy 2.0 Docs: https://docs.sqlalchemy.org/en/20/

- Pydantic v2: https://docs.pydantic.dev/

- Alembic migrations