import React from 'react';

const ArchitectureDiagram = () => {
  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-50 to-slate-100 p-8 overflow-auto">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-2 text-slate-800">
          Modular Monolith with Clean Architecture
        </h1>
        <p className="text-center text-slate-600 mb-8">
          FastAPI/NestJS • PostgreSQL • Domain-Driven Design
        </p>

        {/* Main Architecture Container */}
        <div className="space-y-8">
          
          {/* Layer 1: Presentation/API Layer */}
          <div className="bg-blue-50 border-2 border-blue-400 rounded-lg p-6 shadow-lg">
            <h2 className="text-xl font-bold text-blue-800 mb-4 flex items-center">
              <span className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-3">1</span>
              Presentation Layer (API)
            </h2>
            <div className="grid grid-cols-4 gap-4">
              {['User Management', 'File Management', 'Project Management', 'Notification'].map((module) => (
                <div key={module} className="bg-white p-4 rounded border border-blue-300">
                  <h3 className="font-semibold text-blue-900 mb-2">{module}</h3>
                  <div className="space-y-1 text-sm text-slate-700">
                    <div>• Controllers</div>
                    <div>• Routes (v1, v2)</div>
                    <div>• Request/Response DTOs</div>
                    <div>• Validation</div>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 p-3 bg-blue-100 rounded text-sm">
              <strong>Responsibilities:</strong> HTTP handling, API versioning, Swagger docs, Request validation, Response serialization
            </div>
          </div>

          {/* Arrow Down */}
          <div className="flex justify-center">
            <div className="text-4xl text-slate-400">↓</div>
          </div>

          {/* Layer 2: Application Layer */}
          <div className="bg-green-50 border-2 border-green-400 rounded-lg p-6 shadow-lg">
            <h2 className="text-xl font-bold text-green-800 mb-4 flex items-center">
              <span className="bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-3">2</span>
              Application Layer (Use Cases)
            </h2>
            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-3">
                <div className="bg-white p-4 rounded border border-green-300">
                  <h3 className="font-semibold text-green-900 mb-2">Commands (Write)</h3>
                  <div className="space-y-1 text-sm text-slate-700">
                    <div>• CreateUserCommand</div>
                    <div>• UpdateProjectCommand</div>
                    <div>• DeleteFileCommand</div>
                  </div>
                </div>
                <div className="bg-white p-4 rounded border border-green-300">
                  <h3 className="font-semibold text-green-900 mb-2">Queries (Read)</h3>
                  <div className="space-y-1 text-sm text-slate-700">
                    <div>• GetUserQuery</div>
                    <div>• ListProjectsQuery</div>
                    <div>• SearchFilesQuery</div>
                  </div>
                </div>
              </div>
              <div className="space-y-3">
                <div className="bg-white p-4 rounded border border-green-300">
                  <h3 className="font-semibold text-green-900 mb-2">Services</h3>
                  <div className="space-y-1 text-sm text-slate-700">
                    <div>• UserService</div>
                    <div>• ProjectService</div>
                    <div>• NotificationService</div>
                  </div>
                </div>
                <div className="bg-white p-4 rounded border border-green-300">
                  <h3 className="font-semibold text-green-900 mb-2">Interfaces</h3>
                  <div className="space-y-1 text-sm text-slate-700">
                    <div>• IUserRepository</div>
                    <div>• IUnitOfWork</div>
                    <div>• IEmailService</div>
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-4 p-3 bg-green-100 rounded text-sm">
              <strong>Responsibilities:</strong> Business workflows, CQRS pattern, Use case orchestration, DTOs mapping
            </div>
          </div>

          {/* Arrow Down */}
          <div className="flex justify-center">
            <div className="text-4xl text-slate-400">↓</div>
          </div>

          {/* Layer 3: Domain Layer */}
          <div className="bg-purple-50 border-2 border-purple-400 rounded-lg p-6 shadow-lg">
            <h2 className="text-xl font-bold text-purple-800 mb-4 flex items-center">
              <span className="bg-purple-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-3">3</span>
              Domain Layer (Business Logic)
            </h2>
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-white p-4 rounded border border-purple-300">
                <h3 className="font-semibold text-purple-900 mb-2">Entities</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>• User</div>
                  <div>• Project</div>
                  <div>• File</div>
                  <div>• AggregateRoot</div>
                </div>
              </div>
              <div className="bg-white p-4 rounded border border-purple-300">
                <h3 className="font-semibold text-purple-900 mb-2">Value Objects</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>• Email</div>
                  <div>• Money</div>
                  <div>• DateRange</div>
                  <div>• Address</div>
                </div>
              </div>
              <div className="bg-white p-4 rounded border border-purple-300">
                <h3 className="font-semibold text-purple-900 mb-2">Domain Events</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>• UserCreated</div>
                  <div>• ProjectUpdated</div>
                  <div>• FileUploaded</div>
                </div>
              </div>
              <div className="bg-white p-4 rounded border border-purple-300">
                <h3 className="font-semibold text-purple-900 mb-2">Exceptions</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>• DomainException</div>
                  <div>• ValidationError</div>
                  <div>• BusinessRuleError</div>
                </div>
              </div>
            </div>
            <div className="mt-4 p-3 bg-purple-100 rounded text-sm">
              <strong>Responsibilities:</strong> Pure business logic, Domain rules, Invariants, No external dependencies (DB, ORM, API)
            </div>
          </div>

          {/* Arrow Up */}
          <div className="flex justify-center">
            <div className="text-4xl text-slate-400">↑</div>
          </div>

          {/* Layer 4: Infrastructure Layer */}
          <div className="bg-orange-50 border-2 border-orange-400 rounded-lg p-6 shadow-lg">
            <h2 className="text-xl font-bold text-orange-800 mb-4 flex items-center">
              <span className="bg-orange-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-3">4</span>
              Infrastructure Layer (Implementation)
            </h2>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-white p-4 rounded border border-orange-300">
                <h3 className="font-semibold text-orange-900 mb-2">Persistence</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>• SQLAlchemy/TypeORM</div>
                  <div>• Repository Impl</div>
                  <div>• UnitOfWork Impl</div>
                  <div>• ORM Models</div>
                </div>
              </div>
              <div className="bg-white p-4 rounded border border-orange-300">
                <h3 className="font-semibold text-orange-900 mb-2">External Services</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>• Email Service</div>
                  <div>• File Storage (S3)</div>
                  <div>• Cache (Redis)</div>
                  <div>• Message Queue</div>
                </div>
              </div>
              <div className="bg-white p-4 rounded border border-orange-300">
                <h3 className="font-semibold text-orange-900 mb-2">Database</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>• Migrations (Alembic)</div>
                  <div>• Seeders</div>
                  <div>• PostgreSQL</div>
                  <div>• Transactions</div>
                </div>
              </div>
            </div>
            <div className="mt-4 p-3 bg-orange-100 rounded text-sm">
              <strong>Responsibilities:</strong> Database access, External APIs, File system, Caching, Message brokers
            </div>
          </div>

          {/* Cross-Cutting Concerns */}
          <div className="bg-slate-50 border-2 border-slate-400 rounded-lg p-6 shadow-lg">
            <h2 className="text-xl font-bold text-slate-800 mb-4">
              Cross-Cutting Concerns & Shared Kernel
            </h2>
            <div className="grid grid-cols-5 gap-4">
              <div className="bg-white p-3 rounded border border-slate-300 text-center">
                <div className="font-semibold text-slate-800 mb-1">Logging</div>
                <div className="text-xs text-slate-600">Structured logs</div>
              </div>
              <div className="bg-white p-3 rounded border border-slate-300 text-center">
                <div className="font-semibold text-slate-800 mb-1">Authentication</div>
                <div className="text-xs text-slate-600">JWT, OAuth</div>
              </div>
              <div className="bg-white p-3 rounded border border-slate-300 text-center">
                <div className="font-semibold text-slate-800 mb-1">Authorization</div>
                <div className="text-xs text-slate-600">RBAC, Policies</div>
              </div>
              <div className="bg-white p-3 rounded border border-slate-300 text-center">
                <div className="font-semibold text-slate-800 mb-1">Error Handling</div>
                <div className="text-xs text-slate-600">Global handlers</div>
              </div>
              <div className="bg-white p-3 rounded border border-slate-300 text-center">
                <div className="font-semibold text-slate-800 mb-1">IoC Container</div>
                <div className="text-xs text-slate-600">Dependency Injection</div>
              </div>
            </div>
          </div>

          {/* Dependency Flow */}
          <div className="bg-gradient-to-r from-slate-700 to-slate-800 text-white rounded-lg p-6 shadow-lg">
            <h2 className="text-xl font-bold mb-4">🔄 Dependency Flow Rule</h2>
            <div className="flex items-center justify-center space-x-4 text-lg">
              <span className="bg-blue-600 px-4 py-2 rounded">Presentation</span>
              <span>→</span>
              <span className="bg-green-600 px-4 py-2 rounded">Application</span>
              <span>→</span>
              <span className="bg-purple-600 px-4 py-2 rounded font-bold">Domain</span>
              <span>←</span>
              <span className="bg-orange-600 px-4 py-2 rounded">Infrastructure</span>
            </div>
            <p className="mt-4 text-center text-slate-300">
              Dependencies point inward. Domain layer has NO dependencies. Infrastructure implements interfaces defined in Application.
            </p>
          </div>

          {/* Bounded Contexts */}
          <div className="bg-indigo-50 border-2 border-indigo-400 rounded-lg p-6 shadow-lg">
            <h2 className="text-xl font-bold text-indigo-800 mb-4">
              📦 Bounded Contexts (Modules)
            </h2>
            <div className="grid grid-cols-4 gap-4">
              {[
                { name: 'User Management', items: ['Authentication', 'User CRUD', 'Profiles', 'Roles'] },
                { name: 'File Management', items: ['Upload', 'Download', 'Versioning', 'Permissions'] },
                { name: 'Project Management', items: ['Projects', 'Tasks', 'Teams', 'Timeline'] },
                { name: 'Notification', items: ['Email', 'SMS', 'Push', 'Templates'] }
              ].map((module) => (
                <div key={module.name} className="bg-white p-4 rounded border border-indigo-300">
                  <h3 className="font-semibold text-indigo-900 mb-2">{module.name}</h3>
                  <ul className="space-y-1 text-sm text-slate-700">
                    {module.items.map((item) => (
                      <li key={item}>• {item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
            <div className="mt-4 p-3 bg-indigo-100 rounded text-sm">
              Each module is self-contained with its own Domain → Application → Infrastructure → Presentation layers
            </div>
          </div>

          {/* Key Patterns */}
          <div className="bg-yellow-50 border-2 border-yellow-400 rounded-lg p-6 shadow-lg">
            <h2 className="text-xl font-bold text-yellow-800 mb-4">
              🎯 Design Patterns Implemented
            </h2>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-white p-4 rounded border border-yellow-300">
                <h3 className="font-semibold text-yellow-900 mb-2">Structural</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>✓ Repository Pattern</div>
                  <div>✓ Unit of Work</div>
                  <div>✓ Factory Pattern</div>
                  <div>✓ Adapter Pattern</div>
                </div>
              </div>
              <div className="bg-white p-4 rounded border border-yellow-300">
                <h3 className="font-semibold text-yellow-900 mb-2">Behavioral</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>✓ CQRS Pattern</div>
                  <div>✓ Domain Events</div>
                  <div>✓ Specification Pattern</div>
                  <div>✓ Strategy Pattern</div>
                </div>
              </div>
              <div className="bg-white p-4 rounded border border-yellow-300">
                <h3 className="font-semibold text-yellow-900 mb-2">Architectural</h3>
                <div className="space-y-1 text-sm text-slate-700">
                  <div>✓ Clean Architecture</div>
                  <div>✓ DDD</div>
                  <div>✓ Dependency Injection</div>
                  <div>✓ Result Pattern</div>
                </div>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-slate-600">
          <p>💡 Technology Stack: FastAPI/NestJS • SQLAlchemy/TypeORM • PostgreSQL • Alembic • Pydantic/class-validator</p>
        </div>
      </div>
    </div>
  );
};

export default ArchitectureDiagram;