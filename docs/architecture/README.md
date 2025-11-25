# Architecture Documentation

## Overview

This application follows **Clean Architecture** principles combined with **Domain-Driven Design (DDD)** in a **Modular Monolith** structure.

## Architecture Layers

### 1. Domain Layer (Core Business Logic)

**Location**: `src/modules/{module}/domain/`

**Purpose**: Contains pure business logic with no external dependencies.

**Components**:
- **Entities**: Objects with identity and lifecycle
- **Value Objects**: Immutable objects defined by their attributes
- **Domain Events**: Events that represent something important in the domain
- **Aggregates**: Cluster of entities and value objects
- **Domain Services**: Operations that don't naturally fit in entities

**Rules**:
- ❌ No dependencies on infrastructure
- ❌ No ORM annotations
- ❌ No framework-specific code
- ✅ Pure Python classes
- ✅ Business rules validation
- ✅ Domain events emission

### 2. Application Layer (Use Cases)

**Location**: `src/modules/{module}/application/`

**Purpose**: Orchestrates domain objects to fulfill use cases.

**Components**:
- **Services**: Application services coordinating use cases
- **Commands**: Write operations
- **Queries**: Read operations
- **DTOs**: Data Transfer Objects
- **Mappers**: Convert between domain and DTOs

**Rules**:
- ✅ Can depend on domain layer
- ✅ Defines interfaces for infrastructure
- ❌ No direct database access
- ❌ No HTTP concerns

### 3. Infrastructure Layer (Technical Details)

**Location**: `src/modules/{module}/infrastructure/`

**Purpose**: Implements technical concerns and external dependencies.

**Components**:
- **Repositories**: Database access implementation
- **ORM Models**: SQLAlchemy models
- **External Services**: API clients, file storage
- **Migrations**: Database migrations

**Rules**:
- ✅ Implements interfaces from application layer
- ✅ ORM-specific code here
- ✅ Database queries
- ❌ No business logic

### 4. Presentation Layer (API)

**Location**: `src/modules/{module}/presentation/`

**Purpose**: Handles HTTP requests/responses.

**Components**:
- **Controllers**: Handle HTTP logic
- **Routes**: Define endpoints
- **Request Schemas**: Input validation
- **Response Schemas**: Output formatting

**Rules**:
- ✅ HTTP-specific code
- ✅ Validation
- ✅ Serialization
- ❌ No business logic
- ❌ No database access

## Dependency Flow

```
Presentation Layer
       ↓
Application Layer
       ↓
Domain Layer
       ↑
Infrastructure Layer
```

**Key Principle**: Dependencies point inward. Inner layers never depend on outer layers.

## Modular Monolith Structure

### Bounded Contexts

Each module represents a **Bounded Context** in DDD:

```
src/modules/
├── user_management/     # User bounded context
├── file_management/     # File bounded context
├── project_management/  # Project bounded context
└── notification/        # Notification bounded context
```

### Module Structure

```
module_name/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── events/
│   └── exceptions/
├── application/
│   ├── commands/
│   ├── queries/
│   ├── services/
│   └── dto/
├── infrastructure/
│   ├── persistence/
│   │   ├── models.py
│   │   └── repositories/
│   └── migrations/
└── presentation/
    └── api/
        └── v1/
            ├── controllers/
            ├── schemas/
            └── routes.py
```

## Design Patterns

### 1. Repository Pattern

**Purpose**: Abstract data access logic.

```python
class IRepository(ABC):
    async def get_by_id(self, id: UUID) -> Optional[TEntity]:
        pass
    
    async def add(self, entity: TEntity) -> TEntity:
        pass
```

### 2. Unit of Work Pattern

**Purpose**: Manage transactions across multiple repositories.

```python
async with UnitOfWork(session):
    user = await user_repository.add(user)
    # Transaction automatically committed on success
```

### 3. Domain Events Pattern

**Purpose**: Decouple domain logic through events.

```python
user = User.create(email, username)
# user.domain_events contains UserCreatedEvent
```

### 4. Factory Pattern

**Purpose**: Complex object creation.

```python
user = User.create(
    email="user@example.com",
    username="user"
)
```

### 5. Specification Pattern

**Purpose**: Reusable business rules.

```python
class ActiveUserSpecification:
    def is_satisfied_by(self, user: User) -> bool:
        return user.is_active and not user.is_deleted
```

## Cross-Cutting Concerns

### Logging

- JSON structured logging
- Correlation IDs for request tracking
- Different log levels per environment

### Error Handling

- Custom exception hierarchy
- Centralized exception handling
- Consistent error responses

### Validation

- Pydantic models for API validation
- Domain validation in entities
- Business rule validation in domain services

### Authentication & Authorization

- JWT-based authentication
- Role-based access control
- Permission checking in controllers

## Best Practices

### Domain Layer

1. Keep entities pure - no infrastructure dependencies
2. Use value objects for complex values
3. Emit domain events for important actions
4. Validate business rules in entities
5. Use meaningful ubiquitous language

### Application Layer

1. Use DTOs for data transfer
2. Keep services thin - orchestration only
3. Use mappers explicitly
4. Handle domain events here
5. Define repository interfaces

### Infrastructure Layer

1. Implement repository interfaces
2. Keep ORM models separate from entities
3. Use async operations
4. Handle infrastructure errors
5. Migrations in version control

### Presentation Layer

1. Validate input early
2. Use dependency injection
3. Return consistent responses
4. Document endpoints
5. Version your API

## Testing Strategy

### Unit Tests

- Test domain logic in isolation
- Mock external dependencies
- Fast execution
- High coverage for business logic

### Integration Tests

- Test with real database
- Test repository implementations
- Test API endpoints
- Use test containers

### E2E Tests

- Test complete user flows
- Test cross-module interactions
- Performance testing
- Security testing

## Performance Considerations

1. **Database**:
   - Connection pooling
   - Query optimization
   - Proper indexing
   - Async operations

2. **API**:
   - Response pagination
   - Caching (Redis)
   - Compression
   - Rate limiting

3. **Application**:
   - Lazy loading
   - Batch operations
   - Background tasks
   - Resource cleanup

## Security

1. **Authentication**: JWT tokens
2. **Authorization**: Role-based access
3. **Input Validation**: Pydantic models
4. **SQL Injection**: Parameterized queries (SQLAlchemy)
5. **CORS**: Configured middleware
6. **Secrets**: Environment variables
7. **HTTPS**: Production requirement

## Scalability

### Horizontal Scaling

- Stateless application design
- External session storage (Redis)
- Database connection pooling
- Load balancer ready

### Vertical Scaling

- Async operations
- Efficient queries
- Resource optimization
- Monitoring and profiling

### Future Microservices

The modular structure allows easy extraction of modules into microservices:

1. Extract module code
2. Add message bus for events
3. Implement API gateway
4. Split database