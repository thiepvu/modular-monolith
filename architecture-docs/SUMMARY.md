# Complete Architecture Documentation Summary

> **Modular Monolith with Clean Architecture**  
> FastAPI/NestJS • PostgreSQL • Domain-Driven Design • Production-Ready Patterns

---

## 📚 Table of Contents

1. [Application Architecture](#1-application-architecture)
2. [Database Schema Design](#2-database-schema-design)
3. [Module Interaction Flows](#3-module-interaction-flows)
4. [Deployment Architecture](#4-deployment-architecture)
5. [Specific Use Case Flows](#5-specific-use-case-flows)
6. [Module Dependency Flows & Best Practices](#6-module-dependency-flows--best-practices)
7. [Migration & Seed Best Practices](#7-migration--seed-best-practices)
8. [Quick Reference](#8-quick-reference)

---

## 1. Application Architecture

### Overview
Clean Architecture implementation with 4 distinct layers and modular organization by bounded contexts.

### Key Concepts

#### **4-Layer Architecture**
```
Presentation Layer (Controllers, Routes, API)
        ↓
Application Layer (Use Cases, Commands, Queries)
        ↓
Domain Layer (Entities, Business Logic)
        ↑
Infrastructure Layer (Database, External Services)
```

#### **Bounded Contexts (Modules)**
- **User Management**: Authentication, user CRUD, profiles, roles
- **File Management**: Upload, download, versioning, permissions
- **Project Management**: Projects, tasks, teams, timeline
- **Notification**: Email, SMS, push notifications, templates

### Layer Responsibilities

| Layer | Responsibilities | Dependencies | Examples |
|-------|-----------------|--------------|----------|
| **Presentation** | HTTP handling, validation, serialization | → Application | Controllers, Routes, DTOs |
| **Application** | Business workflows, orchestration | → Domain | Services, Commands, Queries |
| **Domain** | Pure business logic, rules | None (pure) | Entities, Value Objects, Events |
| **Infrastructure** | Database, external APIs, file system | → Domain, Application | Repositories, ORM models |

### Design Patterns

✅ **Repository Pattern** - Abstract data access  
✅ **Unit of Work Pattern** - Transaction management  
✅ **CQRS Pattern** - Command/Query separation  
✅ **Domain Events** - Decouple domain logic  
✅ **Factory Pattern** - Complex object creation  
✅ **Specification Pattern** - Reusable business rules  

### Project Structure
```
src/
├── modules/
│   ├── user_management/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── value_objects/
│   │   │   ├── events/
│   │   │   └── exceptions/
│   │   ├── application/
│   │   │   ├── commands/
│   │   │   ├── queries/
│   │   │   ├── services/
│   │   │   └── dto/
│   │   ├── infrastructure/
│   │   │   ├── persistence/
│   │   │   │   ├── models.py
│   │   │   │   └── repositories/
│   │   │   └── migrations/
│   │   └── presentation/
│   │       └── api/
│   │           └── v1/
│   │               ├── controllers/
│   │               ├── schemas/
│   │               └── routes.py
│   ├── file_management/
│   ├── project_management/
│   └── notification/
└── shared/
    ├── domain/
    ├── infrastructure/
    └── utils/
```

---

## 2. Database Schema Design

### Schema Organization Strategy

**Approach**: Single PostgreSQL database with separate schemas per module

```sql
CREATE SCHEMA IF NOT EXISTS user_management;
CREATE SCHEMA IF NOT EXISTS file_management;
CREATE SCHEMA IF NOT EXISTS project_management;
CREATE SCHEMA IF NOT EXISTS notification;
```

### Key Tables by Module

#### **User Management Schema**
- `users` - User accounts with authentication
- `roles` - Role definitions with permissions (JSONB)
- `user_roles` - Many-to-many relationship
- `user_sessions` - Active JWT sessions

#### **File Management Schema**
- `files` - File metadata and storage paths
- `folders` - Hierarchical folder structure
- `file_versions` - Version history
- `file_permissions` - Access control

#### **Project Management Schema**
- `projects` - Project details with budget tracking
- `project_members` - Team membership
- `tasks` - Task assignments with time tracking
- `task_comments` - Threaded discussions

#### **Notification Schema**
- `notifications` - User notifications
- `notification_preferences` - User settings
- `email_logs` - Delivery tracking

#### **Audit Schema**
- `audit_logs` - Complete audit trail
- `domain_events` - Event sourcing support

### Design Principles

✅ **UUID Primary Keys** - Distributed system ready  
✅ **Soft Deletes** - `deleted_at` column pattern  
✅ **Audit Timestamps** - `created_at`, `updated_at`  
✅ **JSONB Fields** - Flexible data storage  
✅ **Proper Indexes** - Performance optimized  
✅ **Foreign Keys** - Referential integrity  

### Recommended Indexes

```sql
-- User lookups
CREATE INDEX idx_users_email ON user_management.users(email);
CREATE INDEX idx_users_username ON user_management.users(username);

-- File queries
CREATE INDEX idx_files_uploaded_by ON file_management.files(uploaded_by);
CREATE INDEX idx_files_folder_name ON file_management.files(folder_id, name);

-- Project queries
CREATE INDEX idx_projects_owner ON project_management.projects(owner_id);
CREATE INDEX idx_tasks_project ON project_management.tasks(project_id);

-- Notification queries
CREATE INDEX idx_notifications_user_read 
  ON notification.notifications(user_id, is_read);

-- Concurrent creation for production
CREATE INDEX CONCURRENTLY idx_users_email 
  ON user_management.users(email);
```

---

## 3. Module Interaction Flows

### Communication Patterns

#### **1. Synchronous Communication (Direct Calls)**
- **Use When**: Immediate response needed
- **Example**: User creates project → validate user exists
- **Advantages**: Simple, transactional, immediate feedback
- **Disadvantages**: Tight coupling, blocking

#### **2. Asynchronous Communication (Events)**
- **Use When**: Side effects, notifications, analytics
- **Example**: File uploaded → send notification, create audit log
- **Advantages**: Loose coupling, scalable, non-blocking
- **Disadvantages**: Eventual consistency, harder debugging

#### **3. Orchestration (Saga Pattern)**
- **Use When**: Complex multi-step workflows
- **Example**: User onboarding → create account, setup workspace, send welcome
- **Advantages**: Rollback support, clear workflow management
- **Disadvantages**: More complex implementation

#### **4. Shared Kernel**
- **Use When**: Common utilities across modules
- **Example**: BaseEntity, IRepository, Result<T>
- **Advantages**: Code reuse, consistency
- **Rule**: Keep minimal - only truly common code

### Module Interaction Matrix

| From/To | User | File | Project | Notification |
|---------|------|------|---------|--------------|
| **User** | - | ❌ Direct | ❌ Direct | ✅ Event |
| **File** | ⚠️ Query | - | ⚠️ Query | ✅ Event |
| **Project** | ⚠️ Query | ⚠️ Query | - | ✅ Event |
| **Notification** | ⚠️ Query | ❌ Direct | ❌ Direct | - |

**Legend:**
- ✅ Event: Async via events (recommended)
- ⚠️ Query: Read-only queries (acceptable)
- ❌ Direct: Not allowed

---

## 4. Deployment Architecture

### Environment Comparison

| Aspect | Development | Staging | Production |
|--------|------------|---------|------------|
| **Infrastructure** | Docker Compose | Kubernetes (Small) | Kubernetes (HA) |
| **Replicas** | 1 per service | 2 per service | 3-10 (auto-scale) |
| **Database** | Local PostgreSQL | RDS (Single-AZ) | RDS (Multi-AZ + Replicas) |
| **Deployment** | Manual / Hot reload | CI/CD Auto | Blue-Green / Canary |
| **Monitoring** | Logs only | Basic metrics | Full observability stack |
| **Cost (AWS)** | ~$35/mo | ~$185/mo | ~$975/mo |

### Docker Compose (Development)

```yaml
version: '3.8'
services:
  api:
    build: .
    ports: ["8000:8000"]
    depends_on: [postgres, redis]
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
  
  postgres:
    image: postgres:15
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
  
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
  
  worker:
    build: .
    command: celery worker -A app.worker
    depends_on: [postgres, redis]
```

### Kubernetes (Production)

**Key Components:**
- **Ingress Layer**: NGINX with SSL/TLS, rate limiting
- **Application Layer**: API (3-10 replicas), Workers (2-5), Scheduler (1)
- **Data Layer**: PostgreSQL (Primary-Replica), Redis Cluster, S3/MinIO
- **Observability**: Prometheus, Grafana, Loki, Jaeger

```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: registry/app:v1.0.0
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2Gi
```

### CI/CD Pipeline (6 Stages)

1. **Source**: Git push triggers webhook
2. **Build**: Compile, build Docker image, push to registry
3. **Test**: Unit, integration, E2E tests, code coverage
4. **Security**: Container scan, SAST, dependency check
5. **Deploy**: Dev (auto), Staging (manual), Production (blue-green)
6. **Monitor**: Metrics, alerts, automatic rollback on errors

---

## 5. Specific Use Case Flows

### Use Case 1: User Registration & Onboarding

**Flow:**
1. Client → POST /api/v1/users/register
2. API → Validate email format, check uniqueness
3. API → Hash password, create user entity
4. API → Save to database
5. API → Publish UserRegisteredEvent
6. Notification → Handle event, send welcome email
7. API → Return 201 Created

**Response Time Goal**: <500ms

### Use Case 2: File Upload with Processing

**Flow:**
1. Client → POST /api/v1/files/upload (multipart)
2. API → Validate file (size, type, virus scan)
3. API → Upload to S3, save metadata
4. API → Enqueue ProcessFileJob (thumbnail generation)
5. API → Return 201 Created (processing: true)
6. Worker → Download, resize, upload thumbnail (async)
7. Worker → Update file status to completed

**Response Time Goal**: <2s (upload), background processing

### Use Case 3: Project Task Creation with Notifications

**Flow:**
1. Client → POST /api/v1/projects/:id/tasks
2. API → Validate project access (check user role)
3. API → Validate assignee exists in project
4. API → Create task entity, save to database
5. API → Send TaskAssignedNotification
6. Notification → Check user preferences, send email
7. API → Return 201 Created

**Response Time Goal**: <300ms

### Use Case 4: Authentication (JWT)

**Flow:**
1. Client → POST /api/v1/auth/login (email, password)
2. API → Find user by email
3. API → Verify password (bcrypt.compare)
4. API → Generate JWT token (7 days expiry)
5. API → Store session in Redis (with TTL)
6. API → Update last_login_at timestamp
7. API → Return access_token + refresh_token

**Response Time Goal**: <200ms

### Use Case 5: Distributed Transaction (Saga)

**Example: Purchase Course**

**Flow:**
1. Client → POST /api/v1/orders/purchase
2. Orchestrator → Step 1: Process payment (external gateway)
3. Orchestrator → Step 2: Enroll user in course
4. Orchestrator → Step 3: Send confirmation email
5. Orchestrator → Update order status to completed
6. Orchestrator → Return 201 Created

**Compensating Transactions:**
- If Step 2 fails → Refund payment (compensate Step 1)
- If Step 3 fails → Log error (non-critical, no compensation)

### Use Case 6: CQRS Pattern

**Write Path (Command):**
1. POST /api/v1/posts → CreatePostCommand
2. Command → Save to Write DB (master)
3. Command → Publish PostCreatedEvent
4. Event Handler → Update Read Model (materialized view)

**Read Path (Query):**
1. GET /api/v1/posts/:id → GetPostQuery
2. Query → Read from Read DB (replica/cache)
3. Query → Return optimized denormalized data

---

## 6. Module Dependency Flows & Best Practices

### The Dependency Rule

**Core Principle**: Dependencies point only **inward** toward higher-level policies.

```
Presentation → Application → Domain ← Infrastructure
```

**Nothing in an inner circle can know anything about something in an outer circle.**

### Allowed Dependencies

✅ **Presentation → Application**: Controllers call use cases  
✅ **Application → Domain**: Use cases work with entities  
✅ **Infrastructure → Domain**: Repositories implement interfaces  
✅ **Infrastructure → Application**: Implement application interfaces  

### Forbidden Dependencies

❌ **Domain → Application**: Entities can't depend on use cases  
❌ **Domain → Infrastructure**: No ORM, DB, or framework code  
❌ **Domain → Presentation**: No HTTP, REST, or API code  
❌ **Application → Presentation**: Use cases shouldn't know about HTTP  

### Dependency Inversion Principle (DIP)

**Bad (Direct Dependency):**
```python
class UserService:
    def __init__(self, repo: PostgresUserRepo):  # ❌ Concrete class
        self.repo = repo
```

**Good (Depends on Abstraction):**
```python
class UserService:
    def __init__(self, repo: IUserRepository):  # ✅ Interface
        self.repo = repo
```

### Module Boundaries Best Practices

#### **DO:**
- ✓ Keep modules self-contained
- ✓ Define clear public APIs (Module Facade)
- ✓ Use dependency injection
- ✓ Communicate via events for side effects
- ✓ Keep domain pure (no framework dependencies)

#### **DON'T:**
- ✗ Share database tables between modules
- ✗ Import other module internals
- ✗ Create circular dependencies (A → B → A)
- ✗ Bypass the domain layer
- ✗ Share ORM entities (use DTOs instead)

### Tools for Enforcement

**Python:**
- Import Linter - Prevent forbidden imports
- Pytest - Custom architecture tests
- Dependency Cruiser - Visualize dependencies

**TypeScript:**
- ESLint with custom rules
- ts-arch - Architecture testing
- Madge - Detect circular dependencies

**CI/CD Integration:**
```yaml
# .github/workflows/architecture-tests.yml
- name: Check circular dependencies
  run: npx madge --circular src/
- name: Validate imports
  run: npm run lint:imports
- name: Run architecture tests
  run: npm run test:architecture
```

---

## 7. Migration & Seed Best Practices

### Migration Strategy

**Hybrid Approach**: Central migrations + Module-specific templates

```
project/
├── alembic/versions/           # Central (executed)
│   ├── 001_init_schemas.py
│   ├── 002_user_tables.py
│   └── 003_cross_module_fks.py
└── src/modules/
    └── user_management/
        └── infrastructure/
            └── migrations/     # Module-specific (reference)
```

### Migration Naming Convention

**Pattern**: `{timestamp}_{module}_{action}_{table}.py`

**Examples:**
- ✅ `20240115_002_user_create_users_table.py`
- ✅ `20240116_003_user_add_email_verified.py`
- ✅ `20240117_001_file_create_files_table.py`
- ❌ `migration1.py`
- ❌ `update_users.py`

### Safe Column Addition (3-Step Pattern)

```python
# Step 1: Add nullable column
op.add_column('users',
    sa.Column('phone_number', sa.String(20), nullable=True)  # Initially nullable
)

# Step 2: Backfill data
op.execute("""
    UPDATE users 
    SET phone_number = '000-000-0000' 
    WHERE phone_number IS NULL
""")

# Step 3: Make NOT NULL
op.alter_column('users', 'phone_number', nullable=False)
```

### Index Creation (Production-Safe)

```python
# ❌ WRONG - Blocks writes
op.create_index('idx_users_email', 'users', ['email'])

# ✅ CORRECT - Non-blocking
op.execute("""
    CREATE INDEX CONCURRENTLY idx_users_email 
    ON users(email)
""")
```

### Zero-Downtime Deployment (Expand-Contract)

**Timeline:**
- **Week 1**: Add new column (nullable), start dual-write, backfill
- **Week 2**: Monitor data consistency, fix issues
- **Week 3**: Switch reads to new column
- **Week 4**: Drop old column (after verification)

### Seed Data Organization

```
scripts/seed/
├── essential/           # Production-safe
│   ├── 001_roles.py
│   ├── 002_permissions.py
│   └── 003_admin_user.py
├── development/         # Dev/Staging only
│   ├── users.py
│   ├── projects.py
│   └── files.py
└── test/               # Automated testing
    ├── fixtures.py
    └── factories.py
```

### Idempotent Seed Pattern

```python
def seed_roles(session):
    # Check if exists first
    existing = session.query(Role).filter_by(name='admin').first()
    
    if existing:
        # Update if needed
        existing.permissions = ['all']
    else:
        # Create new
        role = Role(name='admin', permissions=['all'])
        session.add(role)
```

### Migration Best Practices Checklist

**Before Deployment:**
- [ ] Run migration on fresh database (local)
- [ ] Run downgrade to test rollback
- [ ] Run upgrade again after downgrade
- [ ] Test with realistic data volume
- [ ] Test on staging with production-like data
- [ ] Create database backup
- [ ] Have rollback plan ready

**Production Deployment:**
- [ ] Schedule maintenance window
- [ ] Notify users (if downtime expected)
- [ ] Monitor during & after deploy
- [ ] Verify data integrity
- [ ] Check application logs

---

## 8. Quick Reference

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI / NestJS | API framework |
| **ORM** | SQLAlchemy / TypeORM | Database abstraction |
| **Database** | PostgreSQL 15+ | Primary data store |
| **Cache** | Redis 7+ | Session & caching |
| **Queue** | Celery / Bull | Async job processing |
| **Storage** | S3 / MinIO | File storage |
| **Container** | Docker | Containerization |
| **Orchestration** | Kubernetes | Production deployment |
| **CI/CD** | GitHub Actions | Automation |
| **Monitoring** | Prometheus + Grafana | Observability |
| **Tracing** | Jaeger | Distributed tracing |

### Key Commands

```bash
# Migrations
alembic upgrade head                    # Run migrations
alembic downgrade -1                    # Rollback one
alembic revision --autogenerate -m "msg" # Create migration
alembic current                         # Show version
alembic history                         # Show history

# Seeds
python scripts/seed.py --env=development
python scripts/seed.py --essential-only
python scripts/seed.py --module=user_management

# Database
make migrate                            # Run migrations
make rollback                           # Rollback
make seed                              # Seed database
make db-reset                          # Fresh start

# Docker
docker-compose up -d                   # Start services
docker-compose logs -f api             # View logs
docker-compose exec api bash           # Enter container

# Kubernetes
kubectl apply -f k8s/                  # Deploy
kubectl get pods                       # List pods
kubectl logs -f pod-name               # View logs
kubectl exec -it pod-name -- bash      # Enter pod
```

### Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| User Registration | <500ms | Including email queue |
| Authentication | <200ms | JWT generation + Redis |
| File Upload | <2s | Up to 10MB, async processing |
| Task Creation | <300ms | With notifications |
| API Response (P95) | <500ms | 95th percentile |
| Database Query | <100ms | With proper indexes |

### Security Checklist

- [x] JWT with refresh tokens (7 day expiry)
- [x] Password hashing (bcrypt, 12 rounds)
- [x] SQL injection prevention (parameterized queries)
- [x] CORS configured properly
- [x] Rate limiting (per IP, per user)
- [x] Input validation (all endpoints)
- [x] HTTPS/TLS in production
- [x] Secrets in environment variables
- [x] Database credentials rotated
- [x] API keys in secure storage
- [x] Audit logging enabled
- [x] RBAC implemented

### Code Quality Standards

| Metric | Target | Tool |
|--------|--------|------|
| Test Coverage | >80% | pytest / jest |
| Code Complexity | <10 | radon / complexity-report |
| Linting | 0 errors | flake8 / eslint |
| Type Coverage | 100% | mypy / TypeScript |
| Security Score | A | Snyk / SonarQube |
| Documentation | All public APIs | Sphinx / TypeDoc |

---

## Project Links & Resources

### Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **NestJS**: https://nestjs.com/
- **Clean Architecture**: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- **Domain-Driven Design**: https://martinfowler.com/tags/domain%20driven%20design.html

### Tools
- **Alembic** (Python migrations): https://alembic.sqlalchemy.org/
- **TypeORM** (Node migrations): https://typeorm.io/
- **Kubernetes**: https://kubernetes.io/docs/
- **Docker**: https://docs.docker.com/

### Interactive Documentation
- Access all diagrams: Open `build/index.html` after running `npm run build`
- Development mode: `npm start` (with hot reload)

---

## License

This architecture documentation is provided as-is for educational and production use.

---

## Contributing

This is a comprehensive architecture guide. For questions or improvements:
1. Review the interactive diagrams
2. Check specific use case flows
3. Reference the best practices sections
4. Follow the technology stack conventions

---

**Last Updated**: 2025-01-15  
**Version**: 1.0.0  
**Status**: Production Ready ✅