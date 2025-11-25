import React, { useState } from 'react';

const DatabaseSchema = () => {
  const [selectedModule, setSelectedModule] = useState('all');

  const modules = {
    users: {
      name: 'User Management',
      color: 'bg-blue-100 border-blue-400',
      textColor: 'text-blue-900',
      tables: [
        {
          name: 'users',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'email', type: 'VARCHAR(255)', constraints: 'UNIQUE, NOT NULL' },
            { name: 'username', type: 'VARCHAR(100)', constraints: 'UNIQUE, NOT NULL' },
            { name: 'password_hash', type: 'VARCHAR(255)', constraints: 'NOT NULL' },
            { name: 'first_name', type: 'VARCHAR(100)', constraints: '' },
            { name: 'last_name', type: 'VARCHAR(100)', constraints: '' },
            { name: 'avatar_url', type: 'VARCHAR(500)', constraints: '' },
            { name: 'is_active', type: 'BOOLEAN', constraints: 'DEFAULT true' },
            { name: 'is_verified', type: 'BOOLEAN', constraints: 'DEFAULT false' },
            { name: 'last_login_at', type: 'TIMESTAMP', constraints: '' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'updated_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'deleted_at', type: 'TIMESTAMP', constraints: '' },
          ]
        },
        {
          name: 'roles',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'name', type: 'VARCHAR(50)', constraints: 'UNIQUE, NOT NULL' },
            { name: 'description', type: 'TEXT', constraints: '' },
            { name: 'permissions', type: 'JSONB', constraints: '' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'updated_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        },
        {
          name: 'user_roles',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'user_id', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'role_id', type: 'UUID', constraints: 'FK → roles.id' },
            { name: 'assigned_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'assigned_by', type: 'UUID', constraints: 'FK → users.id' },
          ]
        },
        {
          name: 'user_sessions',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'user_id', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'token', type: 'VARCHAR(500)', constraints: 'UNIQUE, NOT NULL' },
            { name: 'ip_address', type: 'INET', constraints: '' },
            { name: 'user_agent', type: 'TEXT', constraints: '' },
            { name: 'expires_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        }
      ]
    },
    files: {
      name: 'File Management',
      color: 'bg-green-100 border-green-400',
      textColor: 'text-green-900',
      tables: [
        {
          name: 'files',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'name', type: 'VARCHAR(255)', constraints: 'NOT NULL' },
            { name: 'original_name', type: 'VARCHAR(255)', constraints: 'NOT NULL' },
            { name: 'mime_type', type: 'VARCHAR(100)', constraints: 'NOT NULL' },
            { name: 'size_bytes', type: 'BIGINT', constraints: 'NOT NULL' },
            { name: 'storage_path', type: 'VARCHAR(500)', constraints: 'NOT NULL' },
            { name: 'storage_provider', type: 'VARCHAR(50)', constraints: 'NOT NULL' },
            { name: 'checksum', type: 'VARCHAR(64)', constraints: '' },
            { name: 'uploaded_by', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'folder_id', type: 'UUID', constraints: 'FK → folders.id' },
            { name: 'is_public', type: 'BOOLEAN', constraints: 'DEFAULT false' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'updated_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'deleted_at', type: 'TIMESTAMP', constraints: '' },
          ]
        },
        {
          name: 'folders',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'name', type: 'VARCHAR(255)', constraints: 'NOT NULL' },
            { name: 'parent_id', type: 'UUID', constraints: 'FK → folders.id' },
            { name: 'path', type: 'VARCHAR(1000)', constraints: 'NOT NULL' },
            { name: 'created_by', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'updated_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        },
        {
          name: 'file_versions',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'file_id', type: 'UUID', constraints: 'FK → files.id' },
            { name: 'version_number', type: 'INTEGER', constraints: 'NOT NULL' },
            { name: 'storage_path', type: 'VARCHAR(500)', constraints: 'NOT NULL' },
            { name: 'size_bytes', type: 'BIGINT', constraints: 'NOT NULL' },
            { name: 'checksum', type: 'VARCHAR(64)', constraints: '' },
            { name: 'uploaded_by', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        },
        {
          name: 'file_permissions',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'file_id', type: 'UUID', constraints: 'FK → files.id' },
            { name: 'user_id', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'permission_type', type: 'VARCHAR(20)', constraints: 'NOT NULL' },
            { name: 'granted_by', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        }
      ]
    },
    projects: {
      name: 'Project Management',
      color: 'bg-purple-100 border-purple-400',
      textColor: 'text-purple-900',
      tables: [
        {
          name: 'projects',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'name', type: 'VARCHAR(255)', constraints: 'NOT NULL' },
            { name: 'description', type: 'TEXT', constraints: '' },
            { name: 'status', type: 'VARCHAR(50)', constraints: 'NOT NULL' },
            { name: 'priority', type: 'VARCHAR(20)', constraints: '' },
            { name: 'start_date', type: 'DATE', constraints: '' },
            { name: 'end_date', type: 'DATE', constraints: '' },
            { name: 'budget', type: 'DECIMAL(15,2)', constraints: '' },
            { name: 'owner_id', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'updated_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'deleted_at', type: 'TIMESTAMP', constraints: '' },
          ]
        },
        {
          name: 'project_members',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'project_id', type: 'UUID', constraints: 'FK → projects.id' },
            { name: 'user_id', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'role', type: 'VARCHAR(50)', constraints: 'NOT NULL' },
            { name: 'joined_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        },
        {
          name: 'tasks',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'project_id', type: 'UUID', constraints: 'FK → projects.id' },
            { name: 'title', type: 'VARCHAR(255)', constraints: 'NOT NULL' },
            { name: 'description', type: 'TEXT', constraints: '' },
            { name: 'status', type: 'VARCHAR(50)', constraints: 'NOT NULL' },
            { name: 'priority', type: 'VARCHAR(20)', constraints: '' },
            { name: 'assigned_to', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'due_date', type: 'TIMESTAMP', constraints: '' },
            { name: 'estimated_hours', type: 'DECIMAL(10,2)', constraints: '' },
            { name: 'actual_hours', type: 'DECIMAL(10,2)', constraints: '' },
            { name: 'created_by', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'updated_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        },
        {
          name: 'task_comments',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'task_id', type: 'UUID', constraints: 'FK → tasks.id' },
            { name: 'user_id', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'content', type: 'TEXT', constraints: 'NOT NULL' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
            { name: 'updated_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        }
      ]
    },
    notifications: {
      name: 'Notification',
      color: 'bg-orange-100 border-orange-400',
      textColor: 'text-orange-900',
      tables: [
        {
          name: 'notifications',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'user_id', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'type', type: 'VARCHAR(50)', constraints: 'NOT NULL' },
            { name: 'title', type: 'VARCHAR(255)', constraints: 'NOT NULL' },
            { name: 'message', type: 'TEXT', constraints: 'NOT NULL' },
            { name: 'data', type: 'JSONB', constraints: '' },
            { name: 'is_read', type: 'BOOLEAN', constraints: 'DEFAULT false' },
            { name: 'read_at', type: 'TIMESTAMP', constraints: '' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        },
        {
          name: 'notification_preferences',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'user_id', type: 'UUID', constraints: 'FK → users.id, UNIQUE' },
            { name: 'email_enabled', type: 'BOOLEAN', constraints: 'DEFAULT true' },
            { name: 'push_enabled', type: 'BOOLEAN', constraints: 'DEFAULT true' },
            { name: 'sms_enabled', type: 'BOOLEAN', constraints: 'DEFAULT false' },
            { name: 'preferences', type: 'JSONB', constraints: '' },
            { name: 'updated_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        },
        {
          name: 'email_logs',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'recipient', type: 'VARCHAR(255)', constraints: 'NOT NULL' },
            { name: 'subject', type: 'VARCHAR(255)', constraints: 'NOT NULL' },
            { name: 'template', type: 'VARCHAR(100)', constraints: '' },
            { name: 'status', type: 'VARCHAR(50)', constraints: 'NOT NULL' },
            { name: 'error_message', type: 'TEXT', constraints: '' },
            { name: 'sent_at', type: 'TIMESTAMP', constraints: '' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        }
      ]
    },
    audit: {
      name: 'Audit & Events',
      color: 'bg-red-100 border-red-400',
      textColor: 'text-red-900',
      tables: [
        {
          name: 'audit_logs',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'user_id', type: 'UUID', constraints: 'FK → users.id' },
            { name: 'entity_type', type: 'VARCHAR(100)', constraints: 'NOT NULL' },
            { name: 'entity_id', type: 'UUID', constraints: 'NOT NULL' },
            { name: 'action', type: 'VARCHAR(50)', constraints: 'NOT NULL' },
            { name: 'old_values', type: 'JSONB', constraints: '' },
            { name: 'new_values', type: 'JSONB', constraints: '' },
            { name: 'ip_address', type: 'INET', constraints: '' },
            { name: 'user_agent', type: 'TEXT', constraints: '' },
            { name: 'created_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        },
        {
          name: 'domain_events',
          columns: [
            { name: 'id', type: 'UUID', constraints: 'PK' },
            { name: 'event_type', type: 'VARCHAR(100)', constraints: 'NOT NULL' },
            { name: 'aggregate_id', type: 'UUID', constraints: 'NOT NULL' },
            { name: 'aggregate_type', type: 'VARCHAR(100)', constraints: 'NOT NULL' },
            { name: 'event_data', type: 'JSONB', constraints: 'NOT NULL' },
            { name: 'metadata', type: 'JSONB', constraints: '' },
            { name: 'version', type: 'INTEGER', constraints: 'NOT NULL' },
            { name: 'occurred_at', type: 'TIMESTAMP', constraints: 'NOT NULL' },
          ]
        }
      ]
    }
  };

  const filteredModules = selectedModule === 'all' 
    ? Object.values(modules) 
    : [modules[selectedModule]];

  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-50 to-slate-100 p-8 overflow-auto">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-2 text-slate-800">
          Database Schema Design
        </h1>
        <p className="text-center text-slate-600 mb-6">
          PostgreSQL • Multi-Schema Approach • Bounded Contexts
        </p>

        {/* Filter Buttons */}
        <div className="flex justify-center gap-2 mb-8 flex-wrap">
          <button
            onClick={() => setSelectedModule('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              selectedModule === 'all'
                ? 'bg-slate-700 text-white'
                : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-100'
            }`}
          >
            All Modules
          </button>
          {Object.entries(modules).map(([key, module]) => (
            <button
              key={key}
              onClick={() => setSelectedModule(key)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedModule === key
                  ? 'bg-slate-700 text-white'
                  : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-100'
              }`}
            >
              {module.name}
            </button>
          ))}
        </div>

        {/* Schema Info Box */}
        <div className="bg-indigo-50 border-2 border-indigo-400 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-indigo-900 mb-3">📐 Schema Organization Strategy</h2>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <h3 className="font-semibold text-indigo-800 mb-2">Single Database Approach:</h3>
              <ul className="space-y-1 text-slate-700">
                <li>• All modules in one PostgreSQL database</li>
                <li>• Separate schemas per bounded context</li>
                <li>• Schema: <code className="bg-indigo-100 px-2 py-0.5 rounded">user_management</code>, <code className="bg-indigo-100 px-2 py-0.5 rounded">file_management</code>, etc.</li>
                <li>• Easier migrations and transactions</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-indigo-800 mb-2">Key Features:</h3>
              <ul className="space-y-1 text-slate-700">
                <li>• UUID primary keys for distributed systems</li>
                <li>• Soft delete support (deleted_at)</li>
                <li>• Audit timestamps (created_at, updated_at)</li>
                <li>• JSONB for flexible data storage</li>
                <li>• Foreign keys with proper constraints</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Tables */}
        <div className="space-y-8">
          {filteredModules.map((module) => (
            <div key={module.name} className="space-y-4">
              <div className={`${module.color} border-2 rounded-lg p-4`}>
                <h2 className={`text-2xl font-bold ${module.textColor} mb-2`}>
                  {module.name}
                </h2>
                <p className="text-sm text-slate-600">
                  Schema: <code className="bg-white px-2 py-1 rounded">
                    {module.name.toLowerCase().replace(/ /g, '_')}
                  </code>
                </p>
              </div>

              {module.tables.map((table) => (
                <div key={table.name} className="bg-white border-2 border-slate-300 rounded-lg overflow-hidden shadow-md">
                  <div className="bg-slate-700 text-white px-4 py-3">
                    <h3 className="text-lg font-bold font-mono">
                      📋 {table.name}
                    </h3>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-slate-100">
                        <tr>
                          <th className="px-4 py-2 text-left text-sm font-semibold text-slate-700 w-1/4">
                            Column Name
                          </th>
                          <th className="px-4 py-2 text-left text-sm font-semibold text-slate-700 w-1/4">
                            Data Type
                          </th>
                          <th className="px-4 py-2 text-left text-sm font-semibold text-slate-700 w-1/2">
                            Constraints
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {table.columns.map((column, idx) => (
                          <tr 
                            key={column.name}
                            className={`${idx % 2 === 0 ? 'bg-white' : 'bg-slate-50'} border-t border-slate-200`}
                          >
                            <td className="px-4 py-2 font-mono text-sm text-slate-800 font-medium">
                              {column.name}
                            </td>
                            <td className="px-4 py-2 font-mono text-sm text-blue-700">
                              {column.type}
                            </td>
                            <td className="px-4 py-2 text-sm text-slate-600">
                              {column.constraints || <span className="text-slate-400">—</span>}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>

        {/* Indexes & Performance */}
        <div className="mt-8 bg-yellow-50 border-2 border-yellow-400 rounded-lg p-6">
          <h2 className="text-xl font-bold text-yellow-900 mb-4">⚡ Recommended Indexes</h2>
          <div className="grid grid-cols-2 gap-6 text-sm">
            <div>
              <h3 className="font-semibold text-yellow-800 mb-2">Primary Indexes:</h3>
              <ul className="space-y-1 text-slate-700 font-mono text-xs">
                <li>• CREATE INDEX idx_users_email ON users(email)</li>
                <li>• CREATE INDEX idx_users_username ON users(username)</li>
                <li>• CREATE INDEX idx_files_uploaded_by ON files(uploaded_by)</li>
                <li>• CREATE INDEX idx_projects_owner ON projects(owner_id)</li>
                <li>• CREATE INDEX idx_tasks_project ON tasks(project_id)</li>
                <li>• CREATE INDEX idx_tasks_assigned ON tasks(assigned_to)</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-yellow-800 mb-2">Composite & Special Indexes:</h3>
              <ul className="space-y-1 text-slate-700 font-mono text-xs">
                <li>• CREATE INDEX idx_files_folder_name ON files(folder_id, name)</li>
                <li>• CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read)</li>
                <li>• CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id)</li>
                <li>• CREATE INDEX idx_domain_events_aggregate ON domain_events(aggregate_type, aggregate_id)</li>
                <li>• CREATE INDEX idx_files_created ON files(created_at DESC)</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Relationships Diagram */}
        <div className="mt-8 bg-gradient-to-r from-slate-700 to-slate-800 text-white rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4">🔗 Key Relationships</h2>
          <div className="grid grid-cols-2 gap-6 text-sm">
            <div>
              <h3 className="font-semibold text-slate-200 mb-2">One-to-Many:</h3>
              <ul className="space-y-1 text-slate-300">
                <li>• users → files (uploaded_by)</li>
                <li>• users → projects (owner_id)</li>
                <li>• projects → tasks</li>
                <li>• folders → files</li>
                <li>• tasks → task_comments</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-slate-200 mb-2">Many-to-Many:</h3>
              <ul className="space-y-1 text-slate-300">
                <li>• users ↔ roles (via user_roles)</li>
                <li>• users ↔ projects (via project_members)</li>
                <li>• users ↔ files (via file_permissions)</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Migration Strategy */}
        <div className="mt-8 bg-green-50 border-2 border-green-400 rounded-lg p-6">
          <h2 className="text-xl font-bold text-green-900 mb-4">🔄 Migration Strategy</h2>
          <div className="space-y-3 text-sm text-slate-700">
            <div className="bg-white p-4 rounded border border-green-300">
              <h3 className="font-semibold text-green-800 mb-2">1. Central Migration Management:</h3>
              <code className="text-xs bg-green-100 px-2 py-1 rounded block">
                alembic/versions/ → One migration file references all module schemas
              </code>
            </div>
            <div className="bg-white p-4 rounded border border-green-300">
              <h3 className="font-semibold text-green-800 mb-2">2. Module-Specific Migrations:</h3>
              <code className="text-xs bg-green-100 px-2 py-1 rounded block">
                src/modules/user_management/infrastructure/migrations/
              </code>
            </div>
            <div className="bg-white p-4 rounded border border-green-300">
              <h3 className="font-semibold text-green-800 mb-2">3. Seed Data per Module:</h3>
              <code className="text-xs bg-green-100 px-2 py-1 rounded block">
                python scripts/seed.py --module=user_management
              </code>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-slate-600">
          <p>💡 This schema supports: Multi-tenancy, Soft Deletes, Audit Logging, Event Sourcing, CQRS</p>
          <p className="mt-2">Total Tables: {Object.values(modules).reduce((sum, m) => sum + m.tables.length, 0)} | 
          Supports horizontal scaling with UUID keys</p>
        </div>
      </div>
    </div>
  );
};

export default DatabaseSchema;