# Complete Generator Usage Guide

## 🎯 Two Powerful Generators

### 1. **Project Generator** 
Creates the entire project structure

### 2. **Module Generator** 
Scaffolds new bounded context modules

---

## 🚀 Quick Start (5 Steps)

### Step 1: Generate Project Structure

```bash
# Save "Smart Project Generator" as generate_project.py
python generate_project.py

# Enter project name (e.g., my-awesome-api)
# This creates complete directory structure
```

### Step 2: Copy File Contents

```bash
cd my-awesome-api

# Open CHECKLIST.md
# Copy content from conversation artifacts (Steps 1-11)
# Follow the checklist to ensure all files are copied
```

### Step 3: Save Module Generator

```bash
# Save "Module Generator CLI" artifact as:
scripts/generate_module.py

# Make executable (Linux/Mac)
chmod +x scripts/generate_module.py
```

### Step 4: Setup Project

```bash
# Install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Setup database
createdb modular_db
python scripts/migrate.py --upgrade
python scripts/seed.py
```

### Step 5: Start Building!

```bash
# Start server
python src/main.py

# Visit: http://localhost:8000/api/docs
```

---

## 📦 What You Get

### From Project Generator:
- ✅ Complete directory structure (70+ directories)
- ✅ All `__init__.py` files
- ✅ CHECKLIST.md (what to copy)
- ✅ QUICKSTART.md (setup guide)
- ✅ Ready for content from artifacts

### From Module Generator:
- ✅ Complete module in seconds
- ✅ All layers pre-configured
- ✅ REST API endpoints
- ✅ CRUD operations
- ✅ Clean Architecture compliance

---

## 🎨 Creating New Modules

### Example 1: File Management

```bash
python scripts/generate_module.py

Module name: file_management
Entity name: File

✓ Module generated!
```

**What gets created:**
- Domain: `File` entity with business logic
- Application: Service with CRUD operations
- Infrastructure: SQLAlchemy model + repository
- Presentation: REST API endpoints
- Location: `src/modules/file_management/`

**Endpoints created:**
- `POST /api/v1/files` - Upload file
- `GET /api/v1/files` - List files
- `GET /api/v1/files/{id}` - Get file
- `PUT /api/v1/files/{id}` - Update file
- `DELETE /api/v1/files/{id}` - Delete file

### Example 2: Project Management

```bash
python scripts/generate_module.py

Module name: projects
Entity name: Project  # or leave empty

✓ Module generated!
```

**Endpoints created:**
- `POST /api/v1/projects`
- `GET /api/v1/projects`
- `GET /api/v1/projects/{id}`
- `PUT /api/v1/projects/{id}`
- `DELETE /api/v1/projects/{id}`

### Example 3: Notifications

```bash
python scripts/generate_module.py

Module name: notifications
Entity name: Notification

✓ Module generated!
```

---

## 🔄 Complete Workflow

### 1. Generate Project (One Time)

```bash
# Download and run project generator
python generate_project.py

# Copy files from artifacts following CHECKLIST.md
# Setup environment and database
```

### 2. Add User Module (Already Included)

The project comes with a complete User Management module as an example.

**Test it:**
```bash
# Start server
python src/main.py

# Create user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 3. Generate New Modules (As Needed)

```bash
# Generate module
python scripts/generate_module.py

# Customize domain logic
# Add to migrations/env.py
# Create migration
python scripts/migrate.py --create "Add {module} tables"

# Run migration
python scripts/migrate.py --upgrade

# Test API
# Endpoints auto-discovered at http://localhost:8000/api/docs
```

### 4. Repeat Step 3 for Each Module

Build your application module by module!

---

## 📋 Checklist for Each New Module

### After Generating Module:

- [ ] Review generated files in `src/modules/{module_name}/`
- [ ] Customize entity business logic
- [ ] Add value objects if needed
- [ ] Add custom exceptions
- [ ] Update DTOs with your fields
- [ ] Add custom repository queries
- [ ] **Import model in migrations/env.py**
- [ ] Create migration
- [ ] Run migration
- [ ] Test API endpoints
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Write E2E tests
- [ ] Update documentation

---

## 🎯 Real-World Examples

### E-Commerce Platform

```bash
# 1. Generate project
python generate_project.py

# 2. Generate modules
python scripts/generate_module.py  # products
python scripts/generate_module.py  # orders
python scripts/generate_module.py  # cart
python scripts/generate_module.py  # payments
python scripts/generate_module.py  # inventory

# 3. Customize each module
# 4. Create migrations
# 5. Build your business!
```

### Content Management System

```bash
# Generate modules
python scripts/generate_module.py  # articles
python scripts/generate_module.py  # comments
python scripts/generate_module.py  # categories
python scripts/generate_module.py  # media
python scripts/generate_module.py  # tags
```

### Project Management Tool

```bash
# Generate modules
python scripts/generate_module.py  # projects
python scripts/generate_module.py  # tasks
python scripts/generate_module.py  # teams
python scripts/generate_module.py  # milestones
python scripts/generate_module.py  # time_tracking
```

---

## 💡 Pro Tips

### Module Naming
✅ Use **plural**: `projects`, `files`, `users`
✅ Use **snake_case**: `file_management`, `user_profiles`
❌ Avoid: `Project`, `file-management`, `UserModule`

### Entity Naming
✅ Use **singular**: `Project`, `File`, `User`
✅ Use **PascalCase**: `FileUpload`, `UserProfile`
❌ Avoid: `project`, `file_upload`, `userProfile`

### Development Flow
1. Generate module
2. Customize domain first
3. Then application layer
4. Then infrastructure
5. Test presentation layer
6. Write tests

### Migration Best Practice
Always add model import BEFORE creating migration:

```python
# src/infrastructure/migrations/env.py

# Add this line
from src.modules.your_module.infrastructure.persistence.models import YourModel
```

Then create migration:
```bash
python scripts/migrate.py --create "Add your_module tables"
```

---

## 🔧 Customization Examples

### Adding Custom Fields

**1. Update Entity:**
```python
# domain/entities/file.py
def __init__(self, name: str, path: str, size: int, mime_type: str, ...):
    self._name = name
    self._path = path
    self._size = size
    self._mime_type = mime_type
```

**2. Update Model:**
```python
# infrastructure/persistence/models.py
class FileModel(BaseModel):
    name = Column(String(255))
    path = Column(String(500))
    size = Column(Integer)
    mime_type = Column(String(100))
```

**3. Update DTOs:**
```python
# application/dto/file_dto.py
class FileCreateDTO(DTO):
    name: str
    path: str
    size: int
    mime_type: str
```

**4. Create Migration:**
```bash
python scripts/migrate.py --create "Add file fields"
python scripts/migrate.py --upgrade
```

### Adding Business Logic

```python
# domain/entities/file.py

def can_be_shared(self) -> bool:
    """Check if file can be shared"""
    return self._size < 100_000_000 and not self._is_deleted

def share_with(self, user_id: UUID) -> None:
    """Share file with user"""
    if not self.can_be_shared():
        raise FileException("File cannot be shared")
    
    self.add_domain_event(FileSharedEvent(self.id, user_id))
```

---

## 📊 Project Structure After Generation

```
your-project/
├── src/
│   ├── core/                    # ✅ From project generator
│   ├── config/                  # ✅ From project generator
│   ├── shared/                  # ✅ From project generator
│   ├── infrastructure/          # ✅ From project generator
│   ├── bootstrapper/            # ✅ From project generator
│   └── modules/
│       ├── user_management/     # ✅ Included example
│       ├── file_management/     # 🆕 From module generator
│       ├── projects/            # 🆕 From module generator
│       └── notifications/       # 🆕 From module generator
├── tests/                       # ✅ From project generator
├── scripts/
│   ├── migrate.py              # ✅ From project generator
│   ├── seed.py                 # ✅ From project generator
│   └── generate_module.py      # ✅ Module generator
├── docs/                        # ✅ From project generator
└── requirements.txt             # ✅ From project generator
```

---

## 🎉 You're Ready!

### What You Have:
1. ✅ **Project Generator** - Creates foundation
2. ✅ **Module Generator** - Scaffolds new modules
3. ✅ **Complete Example** - User management module
4. ✅ **Documentation** - Everything you need

### What You Can Do:
1. 🚀 Generate projects in minutes
2. 🎨 Add modules in seconds
3. 📦 Follow Clean Architecture
4. 🔄 Scale easily
5. 🧪 Test thoroughly
6. 🚢 Deploy confidently

### Next Steps:
1. Run project generator
2. Copy files from artifacts
3. Setup environment
4. Generate your first module
5. Build your application!

---

## 📞 Quick Reference

### Project Setup
```bash
python generate_project.py
cd your-project
# Copy files from artifacts
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
createdb modular_db
python scripts/migrate.py --upgrade
python scripts/seed.py
python src/main.py
```

### Generate Module
```bash
python scripts/generate_module.py
# Follow prompts
# Edit migrations/env.py
python scripts/migrate.py --create "Add module"
python scripts/migrate.py --upgrade
```

### Test
```bash
pytest                    # All tests
pytest tests/unit/       # Unit tests
pytest tests/e2e/        # E2E tests
pytest --cov=src         # With coverage
```

---

**Happy Building! 🚀**

You now have everything you need to build a production-ready API with Clean Architecture!