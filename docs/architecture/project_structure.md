# Project Structure
"""
project-root/
├── src/
│   ├── core/                          # Shared kernel
│   │   ├── __init__.py
│   │   ├── domain/                    # Core domain primitives
│   │   │   ├── __init__.py
│   │   │   ├── base_entity.py
│   │   │   ├── base_aggregate.py
│   │   │   ├── value_objects.py
│   │   │   └── events.py
│   │   ├── application/               # Core application layer
│   │   │   ├── __init__.py
│   │   │   ├── base_service.py
│   │   │   ├── base_command.py
│   │   │   ├── base_query.py
│   │   │   └── dto.py
│   │   ├── interfaces/                # Ports/Interfaces
│   │   │   ├── __init__.py
│   │   │   ├── repositories.py
│   │   │   ├── unit_of_work.py
│   │   │   └── services.py
│   │   └── exceptions/
│   │       ├── __init__.py
│   │       ├── base_exceptions.py
│   │       └── error_codes.py
│   │
│   ├── modules/                       # Bounded Contexts
│   │   ├── __init__.py
│   │   ├── user_management/
│   │   │   ├── __init__.py
│   │   │   ├── domain/               # Domain layer (pure business logic)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── entities/
│   │   │   │   │   ├── user.py
│   │   │   │   │   └── role.py
│   │   │   │   ├── value_objects/
│   │   │   │   │   ├── email.py
│   │   │   │   │   └── password.py
│   │   │   │   ├── events/
│   │   │   │   │   └── user_events.py
│   │   │   │   └── exceptions/
│   │   │   │       └── user_exceptions.py
│   │   │   │
│   │   │   ├── application/          # Application layer (use cases)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── commands/
│   │   │   │   │   ├── create_user.py
│   │   │   │   │   └── update_user.py
│   │   │   │   ├── queries/
│   │   │   │   │   ├── get_user.py
│   │   │   │   │   └── list_users.py
│   │   │   │   ├── services/
│   │   │   │   │   └── user_service.py
│   │   │   │   └── dto/
│   │   │   │       ├── user_dto.py
│   │   │   │       └── mappers.py
│   │   │   │
│   │   │   ├── infrastructure/       # Infrastructure layer
│   │   │   │   ├── __init__.py
│   │   │   │   ├── persistence/
│   │   │   │   │   ├── models.py    # SQLAlchemy ORM models
│   │   │   │   │   ├── repositories/
│   │   │   │   │   │   └── user_repository.py
│   │   │   │   │   └── unit_of_work.py
│   │   │   │   └── migrations/      # Alembic migrations
│   │   │   │       └── versions/
│   │   │   │
│   │   │   └── presentation/         # Presentation layer (API)
│   │   │       ├── __init__.py
│   │   │       ├── api/
│   │   │       │   ├── v1/
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── controllers/
│   │   │       │   │   │   └── user_controller.py
│   │   │       │   │   ├── schemas/
│   │   │       │   │   │   └── user_schemas.py
│   │   │       │   │   └── routes.py
│   │   │       │   └── v2/
│   │   │       └── dependencies.py
│   │   │
│   │   ├── file_management/          # Same structure as user_management
│   │   ├── project_management/       # Same structure
│   │   └── notification/             # Same structure
│   │
│   ├── infrastructure/                # Shared infrastructure
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   ├── session.py
│   │   │   └── base.py
│   │   ├── migrations/               # Central migrations
│   │   │   ├── alembic.ini
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions/
│   │   ├── seeds/                    # Central seeding
│   │   │   ├── __init__.py
│   │   │   └── seed_runner.py
│   │   ├── logging/
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   └── cache/
│   │       └── redis_client.py
│   │
│   ├── shared/                        # Shared utilities
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── base_controller.py
│   │   │   ├── response.py
│   │   │   ├── pagination.py
│   │   │   ├── error_handler.py
│   │   │   └── versioning.py
│   │   ├── validation/
│   │   │   └── validators.py
│   │   └── utils/
│   │       ├── datetime_utils.py
│   │       └── string_utils.py
│   │
│   ├── bootstrapper/                  # IoC Container & App Orchestration
│   │   ├── __init__.py
│   │   ├── container.py              # Dependency Injection
│   │   ├── app_factory.py            # Application factory
│   │   └── module_loader.py          # Dynamic module loading
│   │
│   ├── config/                        # Configuration
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── environments/
│   │   │   ├── development.py
│   │   │   ├── production.py
│   │   │   └── testing.py
│   │   └── logging_config.py
│   │
│   └── main.py                        # Application entry point
│
├── tests/                             # Test structure mirrors src/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/                           # Utility scripts
│   ├── migrate.py
│   ├── seed.py
│   └── generate_types.py
│
├── docs/                              # Documentation
│   ├── architecture/
│   ├── api/
│   └── development/
│
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── README.md
"""