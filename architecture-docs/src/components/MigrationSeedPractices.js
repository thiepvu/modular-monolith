// src/components/MigrationSeedPractices.js
import React, { useState } from 'react';

const MigrationSeedPractices = () => {
  const [selectedView, setSelectedView] = useState('migration_strategy');

  const views = {
    migration_strategy: {
      title: 'Migration Strategy & Architecture',
      description: 'How to organize and manage database migrations',
    },
    migration_patterns: {
      title: 'Migration Patterns & Examples',
      description: 'Common migration patterns with code examples',
    },
    seed_strategy: {
      title: 'Seed Data Strategy',
      description: 'Managing initial and test data',
    },
    best_practices: {
      title: 'Best Practices & Guidelines',
      description: 'Production-ready migration and seed patterns',
    },
    tools_automation: {
      title: 'Tools & Automation',
      description: 'Automate migration and seed management',
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-br from-green-50 to-teal-50 border-2 border-green-300 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-green-900 mb-2">
          {views[selectedView].title}
        </h2>
        <p className="text-slate-700">{views[selectedView].description}</p>
      </div>

      {/* Navigation */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {Object.entries(views).map(([key, view]) => (
          <button
            key={key}
            onClick={() => setSelectedView(key)}
            className={`px-6 py-3 rounded-lg font-medium transition-all whitespace-nowrap ${
              selectedView === key
                ? 'bg-gradient-to-r from-green-600 to-teal-600 text-white shadow-lg'
                : 'bg-white text-slate-700 border-2 border-slate-300 hover:border-green-400'
            }`}
          >
            {view.title}
          </button>
        ))}
      </div>

      {/* Content */}
      {selectedView === 'migration_strategy' && <MigrationStrategy />}
      {selectedView === 'migration_patterns' && <MigrationPatterns />}
      {selectedView === 'seed_strategy' && <SeedStrategy />}
      {selectedView === 'best_practices' && <BestPractices />}
      {selectedView === 'tools_automation' && <ToolsAutomation />}

      {/* Summary Card */}
      <div className="bg-gradient-to-r from-slate-700 to-slate-800 text-white rounded-lg p-6 shadow-lg">
        <h2 className="text-xl font-bold mb-4">🎯 Key Principles</h2>
        <div className="grid grid-cols-3 gap-6 text-sm">
          <div className="space-y-2">
            <div className="font-bold text-yellow-400 mb-2">Safety First:</div>
            <div>• Always test locally</div>
            <div>• Backup before production</div>
            <div>• Write reversible migrations</div>
            <div>• Use transactions</div>
          </div>
          <div className="space-y-2">
            <div className="font-bold text-yellow-400 mb-2">Performance:</div>
            <div>• Create indexes concurrently</div>
            <div>• Process data in batches</div>
            <div>• Avoid table locks</div>
            <div>• Monitor query times</div>
          </div>
          <div className="space-y-2">
            <div className="font-bold text-yellow-400 mb-2">Organization:</div>
            <div>• Schema per module</div>
            <div>• Consistent naming</div>
            <div>• Idempotent seeds</div>
            <div>• Automate with CI/CD</div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Migration Strategy Component
const MigrationStrategy = () => (
  <div className="space-y-6">
    {/* Migration Architecture */}
    <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow-lg">
      <h3 className="text-2xl font-bold mb-4">🏗️ Migration Architecture</h3>
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white/10 p-4 rounded">
          <h4 className="font-bold mb-2">Central vs Distributed</h4>
          <div className="text-sm space-y-2">
            <div>✅ <strong>Central:</strong> One migration folder, references all modules</div>
            <div>✅ <strong>Distributed:</strong> Each module has its own migrations</div>
            <div>💡 <strong>Recommended:</strong> Hybrid approach</div>
          </div>
        </div>
        <div className="bg-white/10 p-4 rounded">
          <h4 className="font-bold mb-2">Schema Organization</h4>
          <div className="text-sm space-y-2">
            <div>• Separate schema per module</div>
            <div>• Schema: user_management, file_management</div>
            <div>• Easier to extract to microservices later</div>
          </div>
        </div>
      </div>
    </div>

    {/* Hybrid Structure */}
    <div className="bg-white p-6 rounded-lg border-2 border-blue-400 shadow-lg">
      <h3 className="font-bold text-xl text-blue-900 mb-4">📁 Recommended Hybrid Structure</h3>
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold text-blue-800 mb-3">Folder Structure:</h4>
          <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs">
            <div className="text-slate-400"># Project Root</div>
            <div>project/</div>
            <div>├── alembic/</div>
            <div>│   ├── versions/</div>
            <div className="text-yellow-400">│   │   ├── 001_init_schemas.py</div>
            <div className="text-yellow-400">│   │   ├── 002_user_tables.py</div>
            <div className="text-yellow-400">│   │   └── 003_cross_module_fks.py</div>
            <div>│   └── env.py</div>
            <div>├── src/</div>
            <div>│   └── modules/</div>
            <div>│       ├── user_management/</div>
            <div>│       │   └── infrastructure/</div>
            <div>│       │       └── persistence/</div>
            <div className="text-green-400">│       │           ├── models.py</div>
            <div className="text-purple-400">│       │           └── migrations/</div>
            <div>│       ├── file_management/</div>
            <div>│       └── project_management/</div>
            <div>└── scripts/</div>
            <div className="text-blue-400">    ├── migrate.py</div>
            <div className="text-blue-400">    └── seed.py</div>
          </div>
        </div>
        <div className="space-y-4">
          <div className="bg-yellow-50 border-2 border-yellow-300 rounded p-4">
            <h5 className="font-semibold text-yellow-900 mb-2">Central (alembic/versions/)</h5>
            <div className="text-sm text-slate-700 space-y-1">
              <div>• Schema creation migrations</div>
              <div>• Cross-module foreign keys</div>
              <div>• Global database changes</div>
              <div>• Executed in order</div>
            </div>
          </div>
          <div className="bg-purple-50 border-2 border-purple-300 rounded p-4">
            <h5 className="font-semibold text-purple-900 mb-2">Module-Specific</h5>
            <div className="text-sm text-slate-700 space-y-1">
              <div>• Migration templates</div>
              <div>• Module-specific SQL scripts</div>
              <div>• Documentation</div>
              <div>• Not executed directly</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    {/* Naming Convention */}
    <div className="bg-white p-6 rounded-lg border-2 border-purple-400 shadow-lg">
      <h3 className="font-bold text-xl text-purple-900 mb-4">📝 Naming Conventions</h3>
      <div className="space-y-4">
        <div className="bg-purple-50 border-2 border-purple-300 rounded p-4">
          <h4 className="font-semibold text-purple-900 mb-3">Migration File Names:</h4>
          <div className="space-y-2 text-sm">
            <div className="bg-white p-3 rounded border border-purple-200 font-mono">
              <strong>Pattern:</strong> {'{timestamp}_{module}_{action}_{table}.py'}
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-white p-3 rounded border border-purple-200">
                <div className="font-mono text-xs text-green-600">✅ Good Examples:</div>
                <div className="font-mono text-xs mt-2 space-y-1">
                  <div>20240115_001_init_schemas.py</div>
                  <div>20240115_002_user_create_users.py</div>
                  <div>20240116_001_file_create_files.py</div>
                </div>
              </div>
              <div className="bg-white p-3 rounded border border-purple-200">
                <div className="font-mono text-xs text-red-600">❌ Bad Examples:</div>
                <div className="font-mono text-xs mt-2 space-y-1">
                  <div>migration1.py</div>
                  <div>update_users.py</div>
                  <div>fix.py</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    {/* Schema-per-Module */}
    <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-400 rounded-lg p-6">
      <h3 className="font-bold text-xl text-indigo-900 mb-4">🗂️ Schema-per-Module Pattern</h3>
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold text-indigo-800 mb-3">Implementation:</h4>
          <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs">
            <div className="text-slate-400"># Create schemas migration</div>
            <div className="text-purple-400">def upgrade():</div>
            <div className="ml-4">op.execute(</div>
            <div className="ml-8 text-yellow-400">"CREATE SCHEMA IF NOT EXISTS"</div>
            <div className="ml-8 text-yellow-400">" user_management"</div>
            <div className="ml-4">)</div>
            <div className="ml-4">op.execute(</div>
            <div className="ml-8 text-yellow-400">"CREATE SCHEMA IF NOT EXISTS"</div>
            <div className="ml-8 text-yellow-400">" file_management"</div>
            <div className="ml-4">)</div>
          </div>
        </div>
        <div className="space-y-3">
          <div className="bg-white p-3 rounded border-2 border-indigo-300">
            <h5 className="font-semibold text-indigo-900 mb-2">✅ Benefits:</h5>
            <ul className="text-sm text-slate-700 space-y-1">
              <li>• Logical separation</li>
              <li>• Easier permissions</li>
              <li>• Clear boundaries</li>
              <li>• Simplifies extraction</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
);

// Migration Patterns Component
const MigrationPatterns = () => (
  <div className="space-y-6">
    {/* Basic Table Creation */}
    <div className="bg-white p-6 rounded-lg border-2 border-green-400 shadow-lg">
      <h3 className="font-bold text-xl text-green-900 mb-4">1️⃣ Basic Table Creation</h3>
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold text-green-800 mb-3">Python (Alembic):</h4>
          <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs overflow-x-auto">
            <div className="text-slate-400">"""create users table"""</div>
            <div className="text-purple-400">from alembic import op</div>
            <div className="text-purple-400">import sqlalchemy as sa</div>
            <div className="mt-2 text-purple-400">def upgrade():</div>
            <div className="ml-4">op.create_table(</div>
            <div className="ml-8 text-yellow-400">'users',</div>
            <div className="ml-8">sa.Column('id', sa.UUID(),</div>
            <div className="ml-12">primary_key=True),</div>
            <div className="ml-8">sa.Column('email',</div>
            <div className="ml-12">sa.String(255),</div>
            <div className="ml-12">nullable=False,</div>
            <div className="ml-12">unique=True),</div>
            <div className="ml-8">schema='user_management'</div>
            <div className="ml-4">)</div>
            <div className="mt-2 text-purple-400">def downgrade():</div>
            <div className="ml-4">op.drop_table('users',</div>
            <div className="ml-8">schema='user_management')</div>
          </div>
        </div>
        <div>
          <h4 className="font-semibold text-blue-800 mb-3">TypeScript (TypeORM):</h4>
          <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs overflow-x-auto">
            <div className="text-purple-400">import {'{ MigrationInterface,'}</div>
            <div className="ml-4">QueryRunner, Table {'}'}</div>
            <div className="ml-2">from "typeorm";</div>
            <div className="mt-2 text-purple-400">export class</div>
            <div className="ml-2">CreateUsersTable</div>
            <div className="ml-4 text-purple-400">implements</div>
            <div className="ml-6">MigrationInterface {'{'}</div>
            <div className="mt-2 ml-4 text-purple-400">async up(</div>
            <div className="ml-6">queryRunner: QueryRunner</div>
            <div className="ml-4">) {'{'}</div>
            <div className="ml-6 text-purple-400">await</div>
            <div className="ml-8">queryRunner.createTable(</div>
            <div className="ml-10 text-purple-400">new Table({'{'}</div>
            <div className="ml-12">name: "users",</div>
            <div className="ml-12">schema: "user_management",</div>
            <div className="ml-12">columns: [...]</div>
            <div className="ml-10">{'}'})</div>
            <div className="ml-8">);</div>
            <div className="ml-4">{'}'}</div>
            <div>{'}'}</div>
          </div>
        </div>
      </div>
    </div>

    {/* Adding Column */}
    <div className="bg-white p-6 rounded-lg border-2 border-blue-400 shadow-lg">
      <h3 className="font-bold text-xl text-blue-900 mb-4">2️⃣ Adding Column (Safe Pattern)</h3>
      <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 mb-4">
        <div className="font-bold text-yellow-900 mb-2">⚠️ Multi-Step Pattern for Production:</div>
        <div className="text-sm text-slate-700">
          When adding a NOT NULL column to a large table, use this safe pattern to avoid downtime
        </div>
      </div>
      <div className="space-y-4">
        <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs">
          <div className="text-slate-400"># Step 1: Add column as nullable</div>
          <div className="text-purple-400">def upgrade():</div>
          <div className="ml-4">op.add_column('users',</div>
          <div className="ml-8">sa.Column('phone_number',</div>
          <div className="ml-12">sa.String(20),</div>
          <div className="ml-12">nullable=True  # Initially nullable!</div>
          <div className="ml-8">)</div>
          <div className="ml-4">)</div>
          <div className="mt-2 text-slate-400"># Step 2: Backfill data</div>
          <div className="ml-4">op.execute("""</div>
          <div className="ml-8 text-yellow-400">UPDATE users</div>
          <div className="ml-8 text-yellow-400">SET phone_number = '000-000-0000'</div>
          <div className="ml-8 text-yellow-400">WHERE phone_number IS NULL</div>
          <div className="ml-4">""")</div>
          <div className="mt-2 text-slate-400"># Step 3: Make it NOT NULL</div>
          <div className="ml-4">op.alter_column('users',</div>
          <div className="ml-8">'phone_number',</div>
          <div className="ml-8">nullable=False)</div>
        </div>
        <div className="grid grid-cols-3 gap-3 text-sm">
          <div className="bg-green-50 border-2 border-green-300 rounded p-3">
            <div className="font-bold text-green-900 mb-1">✅ Step 1:</div>
            <div className="text-slate-700">No data loss, deployment safe</div>
          </div>
          <div className="bg-blue-50 border-2 border-blue-300 rounded p-3">
            <div className="font-bold text-blue-900 mb-1">📊 Step 2:</div>
            <div className="text-slate-700">Fill existing rows, monitor progress</div>
          </div>
          <div className="bg-purple-50 border-2 border-purple-300 rounded p-3">
            <div className="font-bold text-purple-900 mb-1">🔒 Step 3:</div>
            <div className="text-slate-700">Enforce constraint safely</div>
          </div>
        </div>
      </div>
    </div>

    {/* Index Creation */}
    <div className="bg-white p-6 rounded-lg border-2 border-purple-400 shadow-lg">
      <h3 className="font-bold text-xl text-purple-900 mb-4">3️⃣ Index Creation (Concurrent)</h3>
      <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
        <div className="font-bold text-red-900 mb-2">🚨 Critical for Production:</div>
        <div className="text-sm text-slate-700">
          Always create indexes CONCURRENTLY on production to avoid table locks
        </div>
      </div>
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold text-purple-800 mb-3">❌ Wrong (Blocks writes):</h4>
          <div className="bg-slate-900 text-red-400 p-4 rounded font-mono text-xs">
            <div className="text-slate-400"># DON'T DO THIS!</div>
            <div className="text-purple-400">def upgrade():</div>
            <div className="ml-4">op.create_index(</div>
            <div className="ml-8 text-yellow-400">'idx_users_email',</div>
            <div className="ml-8 text-yellow-400">'users',</div>
            <div className="ml-8">['email']</div>
            <div className="ml-4">)</div>
            <div className="mt-2 text-red-400"># Table locked!</div>
          </div>
        </div>
        <div>
          <h4 className="font-semibold text-green-800 mb-3">✅ Correct (Non-blocking):</h4>
          <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs">
            <div className="text-slate-400"># Safe for production</div>
            <div className="text-purple-400">def upgrade():</div>
            <div className="ml-4">op.execute("""</div>
            <div className="ml-8 text-yellow-400">CREATE INDEX CONCURRENTLY</div>
            <div className="ml-8 text-yellow-400">idx_users_email</div>
            <div className="ml-8 text-yellow-400">ON users(email)</div>
            <div className="ml-4">""")</div>
            <div className="mt-2 text-green-400"># No lock!</div>
          </div>
        </div>
      </div>
    </div>

    {/* Data Migration */}
    <div className="bg-white p-6 rounded-lg border-2 border-orange-400 shadow-lg">
      <h3 className="font-bold text-xl text-orange-900 mb-4">4️⃣ Data Migration (Batch Processing)</h3>
      <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs overflow-x-auto">
        <div className="text-slate-400">"""migrate user roles"""</div>
        <div className="text-purple-400">def upgrade():</div>
        <div className="ml-4">connection = op.get_bind()</div>
        <div className="ml-4">batch_size = 1000</div>
        <div className="ml-4">offset = 0</div>
        <div className="mt-2 ml-4 text-purple-400">while True:</div>
        <div className="ml-8"># Fetch batch</div>
        <div className="ml-8">users = connection.execute(</div>
        <div className="ml-12 text-yellow-400">"""SELECT id, roles_json</div>
        <div className="ml-12 text-yellow-400">FROM users</div>
        <div className="ml-12 text-yellow-400">LIMIT %(limit)s</div>
        <div className="ml-12 text-yellow-400">OFFSET %(offset)s""",</div>
        <div className="ml-12">{'{'}"limit": batch_size,</div>
        <div className="ml-12">"offset": offset{'}'})</div>
        <div className="ml-8">.fetchall()</div>
        <div className="mt-2 ml-8 text-purple-400">if not users:</div>
        <div className="ml-12 text-purple-400">break</div>
        <div className="mt-2 ml-8"># Process batch</div>
        <div className="ml-8 text-purple-400">for user in users:</div>
        <div className="ml-12"># Process each user</div>
        <div className="ml-12">...</div>
        <div className="mt-2 ml-8">offset += batch_size</div>
        <div className="ml-8">print(f"Migrated {'{'} offset{'}'} users")</div>
      </div>
      <div className="mt-4 bg-orange-50 p-3 rounded border-2 border-orange-300 text-sm">
        <strong className="text-orange-900">Best Practices:</strong>
        <ul className="mt-2 space-y-1 text-slate-700">
          <li>• Process in batches (1000-5000 rows)</li>
          <li>• Add logging/progress tracking</li>
          <li>• Test with subset first</li>
        </ul>
      </div>
    </div>
  </div>
);

// Seed Strategy Component
const SeedStrategy = () => (
  <div className="space-y-6">
    {/* Seed Architecture */}
    <div className="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-lg shadow-lg">
      <h3 className="text-2xl font-bold mb-4">🌱 Seed Data Architecture</h3>
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div className="bg-white/10 p-4 rounded">
          <h4 className="font-bold mb-2">Essential Seeds</h4>
          <div className="space-y-1">
            <div>• Roles & permissions</div>
            <div>• System configurations</div>
            <div>• Reference data</div>
            <div>• Default admin user</div>
          </div>
        </div>
        <div className="bg-white/10 p-4 rounded">
          <h4 className="font-bold mb-2">Development Seeds</h4>
          <div className="space-y-1">
            <div>• Test users</div>
            <div>• Sample projects</div>
            <div>• Demo data</div>
            <div>• Edge cases</div>
          </div>
        </div>
        <div className="bg-white/10 p-4 rounded">
          <h4 className="font-bold mb-2">Test Seeds</h4>
          <div className="space-y-1">
            <div>• Integration test data</div>
            <div>• E2E test scenarios</div>
            <div>• Performance test data</div>
            <div>• Isolated per test</div>
          </div>
        </div>
      </div>
    </div>

    {/* Seed Organization */}
    <div className="bg-white p-6 rounded-lg border-2 border-green-400 shadow-lg">
      <h3 className="font-bold text-xl text-green-900 mb-4">📁 Seed Organization</h3>
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold text-green-800 mb-3">Folder Structure:</h4>
          <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs">
            <div>scripts/seed/</div>
            <div className="text-yellow-400">├── essential/</div>
            <div className="text-yellow-400">│   ├── 001_roles.py</div>
            <div className="text-yellow-400">│   └── 002_admin_user.py</div>
            <div className="text-blue-400">├── development/</div>
            <div className="text-blue-400">│   ├── users.py</div>
            <div className="text-blue-400">│   └── projects.py</div>
            <div className="text-purple-400">└── test/</div>
            <div className="text-purple-400">    └── fixtures.py</div>
          </div>
        </div>
        <div className="space-y-3">
          <div className="bg-yellow-50 border-2 border-yellow-300 rounded p-3">
            <h5 className="font-semibold text-yellow-900 mb-2">Essential</h5>
            <div className="text-sm text-slate-700">
              • Runs in all environments<br/>
              • Idempotent (safe to re-run)<br/>
              • Required for app
            </div>
          </div>
          <div className="bg-blue-50 border-2 border-blue-300 rounded p-3">
            <h5 className="font-semibold text-blue-900 mb-2">Development</h5>
            <div className="text-sm text-slate-700">
              • Only dev/staging<br/>
              • Rich sample data<br/>
              • Makes testing easier
            </div>
          </div>
        </div>
      </div>
    </div>

    {/* Idempotent Pattern */}
    <div className="bg-white p-6 rounded-lg border-2 border-purple-400 shadow-lg">
      <h3 className="font-bold text-xl text-purple-900 mb-4">🔁 Idempotent Seed Pattern</h3>
      <div className="bg-purple-50 border-l-4 border-purple-500 p-4 mb-4">
        <div className="font-bold text-purple-900 mb-2">💡 Key Principle:</div>
        <div className="text-sm text-slate-700">
          Seeds should be safe to run multiple times without creating duplicates
        </div>
      </div>
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold text-red-800 mb-3">❌ Non-Idempotent:</h4>
          <div className="bg-slate-900 text-red-400 p-4 rounded font-mono text-xs">
            <div className="text-purple-400">def seed_roles(session):</div>
            <div className="ml-4"># Creates duplicates!</div>
            <div className="ml-4">admin_role = Role(</div>
            <div className="ml-8">name='admin'</div>
            <div className="ml-4">)</div>
            <div className="ml-4">session.add(admin_role)</div>
          </div>
        </div>
        <div>
          <h4 className="font-semibold text-green-800 mb-3">✅ Idempotent:</h4>
          <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs">
            <div className="text-purple-400">def seed_roles(session):</div>
            <div className="ml-4"># Check if exists</div>
            <div className="ml-4">existing = session.query(Role)</div>
            <div className="ml-8">.filter_by(name='admin')</div>
            <div className="ml-8">.first()</div>
            <div className="mt-2 ml-4 text-purple-400">if not existing:</div>
            <div className="ml-8">role = Role(name='admin')</div>
            <div className="ml-8">session.add(role)</div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

// Best Practices Component
const BestPractices = () => (
  <div className="space-y-6">
    {/* Migration Best Practices */}
    <div className="bg-white p-6 rounded-lg border-2 border-blue-400 shadow-lg">
      <h3 className="font-bold text-xl text-blue-900 mb-4">✅ Migration Best Practices</h3>
      <div className="grid grid-cols-2 gap-6">
        <div className="space-y-3">
          <h4 className="font-semibold text-blue-800 bg-blue-100 p-2 rounded">DO's</h4>
          
          <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
            <div className="font-semibold text-green-900">✓ Always write downgrade()</div>
            <div className="text-sm text-slate-700 mt-1">Every migration must be reversible</div>
          </div>

          <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
            <div className="font-semibold text-green-900">✓ Test migrations locally</div>
            <div className="text-sm text-slate-700 mt-1">Run up → down → up cycle</div>
          </div>

          <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
            <div className="font-semibold text-green-900">✓ Use transactions</div>
            <div className="text-sm text-slate-700 mt-1">Wrap migrations in transactions</div>
          </div>

          <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
            <div className="font-semibold text-green-900">✓ Backup before production</div>
            <div className="text-sm text-slate-700 mt-1">Always take DB snapshot</div>
          </div>
        </div>

        <div className="space-y-3">
          <h4 className="font-semibold text-red-800 bg-red-100 p-2 rounded">DON'Ts</h4>
          
          <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
            <div className="font-semibold text-red-900">✗ Never edit old migrations</div>
            <div className="text-sm text-slate-700 mt-1">Create new ones instead</div>
          </div>

          <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
            <div className="font-semibold text-red-900">✗ Don't add NOT NULL directly</div>
            <div className="text-sm text-slate-700 mt-1">Use 3-step pattern</div>
          </div>

          <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
            <div className="font-semibold text-red-900">✗ Don't create indexes synchronously</div>
            <div className="text-sm text-slate-700 mt-1">Always use CONCURRENTLY</div>
          </div>

          <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
            <div className="font-semibold text-red-900">✗ Don't skip testing on staging</div>
            <div className="text-sm text-slate-700 mt-1">Always test first</div>
          </div>
        </div>
      </div>
    </div>

    {/* Zero-Downtime */}
    <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-400 rounded-lg p-6">
      <h3 className="font-bold text-xl text-purple-900 mb-4">🚀 Zero-Downtime Deployment</h3>
      <div className="space-y-4">
        <div className="bg-white border-2 border-purple-300 rounded p-4">
          <h4 className="font-semibold text-purple-900 mb-3">Expand-Contract Pattern:</h4>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div className="space-y-2">
              <div className="font-bold text-purple-800">1. Expand</div>
              <div className="bg-purple-50 p-3 rounded">
                <div className="mb-2">Add new column/table</div>
                <div className="text-xs text-slate-600">
                  • Make nullable<br/>
                  • Both old & new exist
                </div>
              </div>
            </div>
            <div className="space-y-2">
              <div className="font-bold text-blue-800">2. Migrate</div>
              <div className="bg-blue-50 p-3 rounded">
                <div className="mb-2">Dual-write phase</div>
                <div className="text-xs text-slate-600">
                  • Write to both<br/>
                  • Backfill old data
                </div>
              </div>
            </div>
            <div className="space-y-2">
              <div className="font-bold text-green-800">3. Contract</div>
              <div className="bg-green-50 p-3 rounded">
                <div className="mb-2">Remove old</div>
                <div className="text-xs text-slate-600">
                  • Stop writing to old<br/>
                  • Drop old column
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-purple-100 p-4 rounded border-2 border-purple-300">
          <h5 className="font-semibold text-purple-900 mb-2">Example Timeline:</h5>
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-3">
              <div className="bg-purple-600 text-white px-3 py-1 rounded font-bold">Week 1</div>
              <div>Add new column, start dual-write</div>
            </div>
            <div className="flex items-center gap-3">
              <div className="bg-blue-600 text-white px-3 py-1 rounded font-bold">Week 2</div>
              <div>Monitor: Verify data consistency</div>
            </div>
            <div className="flex items-center gap-3">
              <div className="bg-green-600 text-white px-3 py-1 rounded font-bold">Week 3</div>
              <div>Switch reads to new column</div>
            </div>
            <div className="flex items-center gap-3">
              <div className="bg-orange-600 text-white px-3 py-1 rounded font-bold">Week 4</div>
              <div>Drop old column</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    {/* Checklist */}
    <div className="bg-white p-6 rounded-lg border-2 border-green-400 shadow-lg">
      <h3 className="font-bold text-xl text-green-900 mb-4">✓ Pre-Deployment Checklist</h3>
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold text-green-800 mb-3 bg-green-100 p-2 rounded">Local Testing:</h4>
          <div className="space-y-2 text-sm">
            <label className="flex items-center gap-2 bg-green-50 p-2 rounded">
              <input type="checkbox" className="w-4 h-4" />
              <span>Run migration on fresh database</span>
            </label>
            <label className="flex items-center gap-2 bg-green-50 p-2 rounded">
              <input type="checkbox" className="w-4 h-4" />
              <span>Run downgrade to test rollback</span>
            </label>
            <label className="flex items-center gap-2 bg-green-50 p-2 rounded">
              <input type="checkbox" className="w-4 h-4" />
              <span>Test with realistic data volume</span>
            </label>
            <label className="flex items-center gap-2 bg-green-50 p-2 rounded">
              <input type="checkbox" className="w-4 h-4" />
              <span>Verify application still works</span>
            </label>
          </div>
        </div>
        <div>
          <h4 className="font-semibold text-blue-800 mb-3 bg-blue-100 p-2 rounded">Production:</h4>
          <div className="space-y-2 text-sm">
            <label className="flex items-center gap-2 bg-blue-50 p-2 rounded">
              <input type="checkbox" className="w-4 h-4" />
              <span>Create database backup</span>
            </label>
            <label className="flex items-center gap-2 bg-blue-50 p-2 rounded">
              <input type="checkbox" className="w-4 h-4" />
              <span>Test backup restore</span>
            </label>
            <label className="flex items-center gap-2 bg-blue-50 p-2 rounded">
              <input type="checkbox" className="w-4 h-4" />
              <span>Have rollback plan ready</span>
            </label>
            <label className="flex items-center gap-2 bg-blue-50 p-2 rounded">
              <input type="checkbox" className="w-4 h-4" />
              <span>Monitor during & after deploy</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
);

// Tools & Automation Component
const ToolsAutomation = () => (
  <div className="space-y-6">
    {/* CLI Tools */}
    <div className="bg-white p-6 rounded-lg border-2 border-teal-400 shadow-lg">
      <h3 className="font-bold text-xl text-teal-900 mb-4">🛠️ Custom CLI Tools</h3>
      <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs overflow-x-auto">
        <div className="text-slate-400">#!/bin/bash</div>
        <div className="text-slate-400"># scripts/db-cli.sh</div>
        <div className="mt-2 text-purple-400">case $1 in</div>
        <div className="ml-4">migrate)</div>
        <div className="ml-8">alembic upgrade head</div>
        <div className="ml-8">;;</div>
        <div className="ml-4">rollback)</div>
        <div className="ml-8">alembic downgrade -1</div>
        <div className="ml-8">;;</div>
        <div className="ml-4">seed)</div>
        <div className="ml-8">python scripts/seed.py --env=$2</div>
        <div className="ml-8">;;</div>
        <div className="ml-4">status)</div>
        <div className="ml-8">alembic current</div>
        <div className="ml-8">;;</div>
        <div className="text-purple-400">esac</div>
      </div>
      <div className="mt-4 bg-teal-50 p-3 rounded text-sm">
        <strong>Usage:</strong>
        <div className="mt-2 font-mono text-xs">
          <div>$ ./scripts/db-cli.sh migrate</div>
          <div>$ ./scripts/db-cli.sh seed development</div>
        </div>
      </div>
    </div>

    {/* CI/CD Integration */}
    <div className="bg-white p-6 rounded-lg border-2 border-blue-400 shadow-lg">
      <h3 className="font-bold text-xl text-blue-900 mb-4">⚙️ CI/CD Integration</h3>
      <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs overflow-x-auto">
        <div className="text-slate-400"># .github/workflows/migration-check.yml</div>
        <div>name: Migration Check</div>
        <div>on: [pull_request]</div>
        <div className="mt-2">jobs:</div>
        <div className="ml-4">validate-migration:</div>
        <div className="ml-8">runs-on: ubuntu-latest</div>
        <div className="ml-8">services:</div>
        <div className="ml-12">postgres:</div>
        <div className="ml-16">image: postgres:15</div>
        <div className="mt-2 ml-8">steps:</div>
        <div className="ml-12">- uses: actions/checkout@v3</div>
        <div className="ml-12">- name: Run migrations</div>
        <div className="ml-16">run: alembic upgrade head</div>
        <div className="ml-12">- name: Test rollback</div>
        <div className="ml-16">run: alembic downgrade -1</div>
        <div className="ml-12">- name: Re-run migration</div>
        <div className="ml-16">run: alembic upgrade head</div>
      </div>
    </div>

    {/* Makefile */}
    <div className="bg-white p-6 rounded-lg border-2 border-purple-400 shadow-lg">
      <h3 className="font-bold text-xl text-purple-900 mb-4">📝 Makefile Shortcuts</h3>
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold text-purple-800 mb-3">Makefile:</h4>
          <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs">
            <div className="text-slate-400"># Makefile</div>
            <div>migrate:</div>
            <div className="ml-4">@echo "🚀 Running migrations..."</div>
            <div className="ml-4">alembic upgrade head</div>
            <div className="mt-2">rollback:</div>
            <div className="ml-4">@echo "⏪ Rolling back..."</div>
            <div className="ml-4">alembic downgrade -1</div>
            <div className="mt-2">seed:</div>
            <div className="ml-4">@echo "🌱 Seeding..."</div>
            <div className="ml-4">python scripts/seed.py</div>
            <div className="mt-2">db-reset:</div>
            <div className="ml-4">alembic downgrade base</div>
            <div className="ml-4">alembic upgrade head</div>
            <div className="ml-4">python scripts/seed.py</div>
          </div>
        </div>
        <div>
          <h4 className="font-semibold text-blue-800 mb-3">package.json:</h4>
          <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs">
            <div className="text-slate-400">// package.json</div>
            <div>{'{'}</div>
            <div className="ml-4">"scripts": {'{'}</div>
            <div className="ml-8">"migration:run":</div>
            <div className="ml-10">"typeorm migration:run",</div>
            <div className="ml-8">"migration:revert":</div>
            <div className="ml-10">"typeorm migration:revert",</div>
            <div className="ml-8">"seed:run":</div>
            <div className="ml-10">"ts-node scripts/seed.ts",</div>
            <div className="ml-8">"db:reset":</div>
            <div className="ml-10">"npm run migration:revert &&"</div>
            <div className="ml-10">"npm run migration:run &&"</div>
            <div className="ml-10">"npm run seed:run"</div>
            <div className="ml-4">{'}'}</div>
            <div>{'}'}</div>
          </div>
        </div>
      </div>
    </div>

    {/* Docker Integration */}
    <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-400 rounded-lg p-6">
      <h3 className="font-bold text-xl text-indigo-900 mb-4">🐳 Docker Integration</h3>
      <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs overflow-x-auto">
        <div className="text-slate-400"># docker-compose.yml</div>
        <div>version: '3.8'</div>
        <div>services:</div>
        <div className="ml-4">app:</div>
        <div className="ml-8">build: .</div>
        <div className="ml-8">depends_on:</div>
        <div className="ml-12">db:</div>
        <div className="ml-16">condition: service_healthy</div>
        <div className="ml-8">command: |</div>
        <div className="ml-12">echo "🚀 Running migrations..."</div>
        <div className="ml-12">alembic upgrade head</div>
        <div className="ml-12">echo "🌱 Seeding database..."</div>
        <div className="ml-12">python scripts/seed.py --essential-only</div>
        <div className="ml-12">echo "✅ Starting app..."</div>
        <div className="ml-12">uvicorn main:app --host 0.0.0.0</div>
      </div>
      <div className="mt-4 bg-indigo-50 p-3 rounded text-sm">
        <strong>This ensures:</strong>
        <ul className="mt-2 space-y-1 text-slate-700">
          <li>• Database ready before migrations</li>
          <li>• Migrations complete before app starts</li>
          <li>• Essential seeds loaded</li>
        </ul>
      </div>
    </div>
  </div>
);

export default MigrationSeedPractices;