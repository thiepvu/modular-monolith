import React, { useState } from 'react';

const ModuleDependencyFlows = () => {
  const [selectedView, setSelectedView] = useState('dependency_rules');

  const views = {
    dependency_rules: {
      title: 'Dependency Rules & Principles',
      description: 'Core principles for managing module dependencies',
      content: (
        <div className="space-y-6">
          {/* The Dependency Rule */}
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-6 rounded-lg shadow-lg">
            <h3 className="text-2xl font-bold mb-4">🎯 The Dependency Rule</h3>
            <div className="text-lg mb-4">
              Source code dependencies must point only <strong>inward</strong> toward higher-level policies.
            </div>
            <div className="bg-white/10 p-4 rounded text-base">
              Nothing in an inner circle can know anything about something in an outer circle.
            </div>
          </div>

          {/* Concentric Circles */}
          <div className="bg-white p-6 rounded-lg border-2 border-indigo-400 shadow-lg">
            <h3 className="font-bold text-xl text-indigo-900 mb-4">Clean Architecture Layers</h3>
            <div className="flex justify-center items-center">
              <div className="relative w-[500px] h-[500px]">
                {/* Domain Layer - Center */}
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 bg-gradient-to-br from-purple-500 to-purple-700 rounded-full flex items-center justify-center shadow-xl z-40">
                  <div className="text-center text-white">
                    <div className="font-bold text-sm">Domain</div>
                    <div className="text-xs">Entities</div>
                    <div className="text-xs">Business Rules</div>
                  </div>
                </div>

                {/* Application Layer */}
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center shadow-lg z-30">
                  <div className="text-center text-white mt-20">
                    <div className="font-bold text-sm">Application</div>
                    <div className="text-xs">Use Cases</div>
                  </div>
                </div>

                {/* Infrastructure Layer */}
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center shadow-lg z-20">
                  <div className="text-center text-white mt-32">
                    <div className="font-bold text-sm">Infrastructure</div>
                    <div className="text-xs">DB, APIs, Files</div>
                  </div>
                </div>

                {/* Presentation Layer */}
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center shadow-lg z-10">
                  <div className="text-center text-white mt-44">
                    <div className="font-bold text-sm">Presentation</div>
                    <div className="text-xs">Controllers, APIs</div>
                  </div>
                </div>

                {/* Arrows pointing inward */}
                <div className="absolute top-4 left-1/2 transform -translate-x-1/2 text-white font-bold z-50">
                  ↓ Dependencies
                </div>
              </div>
            </div>
            <div className="mt-6 text-center text-slate-700 font-semibold">
              Dependencies flow inward: Presentation → Application → Domain ← Infrastructure
            </div>
          </div>

          {/* Allowed vs Not Allowed */}
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-green-50 border-2 border-green-400 rounded-lg p-6">
              <h3 className="font-bold text-lg text-green-900 mb-4">✅ Allowed Dependencies</h3>
              <div className="space-y-3 text-sm">
                <div className="bg-white p-3 rounded border border-green-300">
                  <div className="font-semibold text-green-800">Presentation → Application</div>
                  <div className="text-slate-600">Controllers call use case services</div>
                </div>
                <div className="bg-white p-3 rounded border border-green-300">
                  <div className="font-semibold text-green-800">Application → Domain</div>
                  <div className="text-slate-600">Use cases work with entities</div>
                </div>
                <div className="bg-white p-3 rounded border border-green-300">
                  <div className="font-semibold text-green-800">Infrastructure → Domain</div>
                  <div className="text-slate-600">Repositories implement interfaces</div>
                </div>
                <div className="bg-white p-3 rounded border border-green-300">
                  <div className="font-semibold text-green-800">Infrastructure → Application</div>
                  <div className="text-slate-600">Implement application interfaces</div>
                </div>
              </div>
            </div>

            <div className="bg-red-50 border-2 border-red-400 rounded-lg p-6">
              <h3 className="font-bold text-lg text-red-900 mb-4">❌ Forbidden Dependencies</h3>
              <div className="space-y-3 text-sm">
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold text-red-800">Domain → Application</div>
                  <div className="text-slate-600">Entities can't depend on use cases</div>
                </div>
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold text-red-800">Domain → Infrastructure</div>
                  <div className="text-slate-600">No ORM, DB, or framework code</div>
                </div>
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold text-red-800">Domain → Presentation</div>
                  <div className="text-slate-600">No HTTP, REST, or API code</div>
                </div>
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold text-red-800">Application → Presentation</div>
                  <div className="text-slate-600">Use cases shouldn't know about HTTP</div>
                </div>
              </div>
            </div>
          </div>

          {/* Dependency Inversion Principle */}
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-400 rounded-lg p-6">
            <h3 className="font-bold text-xl text-purple-900 mb-4">🔄 Dependency Inversion Principle (DIP)</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-purple-800 mb-3">Without DIP (Bad):</h4>
                <div className="bg-white p-4 rounded border-2 border-purple-300 font-mono text-sm">
                  <div className="text-green-600">// Application Layer</div>
                  <div className="text-blue-600">class UserService {'{'}</div>
                  <div className="ml-4 text-red-600">// Direct dependency!</div>
                  <div className="ml-4">constructor(</div>
                  <div className="ml-8 text-red-600">repo: PostgresUserRepo</div>
                  <div className="ml-4">) {'{}'}</div>
                  <div>{'}'}</div>
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-purple-800 mb-3">With DIP (Good):</h4>
                <div className="bg-white p-4 rounded border-2 border-purple-300 font-mono text-sm">
                  <div className="text-green-600">// Application Layer</div>
                  <div className="text-blue-600">class UserService {'{'}</div>
                  <div className="ml-4 text-green-600">// Depends on interface!</div>
                  <div className="ml-4">constructor(</div>
                  <div className="ml-8 text-green-600">repo: IUserRepository</div>
                  <div className="ml-4">) {'{}'}</div>
                  <div>{'}'}</div>
                </div>
              </div>
            </div>
            <div className="mt-4 bg-purple-100 p-3 rounded text-sm text-purple-900">
              <strong>Key Principle:</strong> High-level modules should not depend on low-level modules. Both should depend on abstractions (interfaces).
            </div>
          </div>
        </div>
      )
    },
    module_boundaries: {
      title: 'Module Boundaries & Coupling',
      description: 'How modules should interact with each other',
      content: (
        <div className="space-y-6">
          {/* Module Interaction Matrix */}
          <div className="bg-white p-6 rounded-lg border-2 border-blue-400 shadow-lg">
            <h3 className="font-bold text-xl text-blue-900 mb-4">📊 Module Interaction Matrix</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm border-collapse">
                <thead>
                  <tr className="bg-blue-100">
                    <th className="border-2 border-blue-300 p-3 text-left">From / To</th>
                    <th className="border-2 border-blue-300 p-3 text-center">User</th>
                    <th className="border-2 border-blue-300 p-3 text-center">File</th>
                    <th className="border-2 border-blue-300 p-3 text-center">Project</th>
                    <th className="border-2 border-blue-300 p-3 text-center">Notification</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="border-2 border-blue-300 p-3 font-semibold bg-blue-50">User</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-slate-200">-</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-red-100">❌ Direct</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-red-100">❌ Direct</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-green-100">✅ Event</td>
                  </tr>
                  <tr>
                    <td className="border-2 border-blue-300 p-3 font-semibold bg-blue-50">File</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-yellow-100">⚠️ Query</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-slate-200">-</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-yellow-100">⚠️ Query</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-green-100">✅ Event</td>
                  </tr>
                  <tr>
                    <td className="border-2 border-blue-300 p-3 font-semibold bg-blue-50">Project</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-yellow-100">⚠️ Query</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-yellow-100">⚠️ Query</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-slate-200">-</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-green-100">✅ Event</td>
                  </tr>
                  <tr>
                    <td className="border-2 border-blue-300 p-3 font-semibold bg-blue-50">Notification</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-yellow-100">⚠️ Query</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-red-100">❌ Direct</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-red-100">❌ Direct</td>
                    <td className="border-2 border-blue-300 p-3 text-center bg-slate-200">-</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="mt-4 grid grid-cols-3 gap-3 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-green-100 border-2 border-green-400 rounded"></div>
                <span><strong>✅ Event:</strong> Async via events</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-yellow-100 border-2 border-yellow-400 rounded"></div>
                <span><strong>⚠️ Query:</strong> Read-only queries OK</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-red-100 border-2 border-red-400 rounded"></div>
                <span><strong>❌ Direct:</strong> Not allowed</span>
              </div>
            </div>
          </div>

          {/* Coupling Types */}
          <div className="bg-white p-6 rounded-lg border-2 border-purple-400 shadow-lg">
            <h3 className="font-bold text-xl text-purple-900 mb-4">🔗 Types of Module Coupling</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-3">
                <div className="bg-green-50 border-2 border-green-400 rounded-lg p-4">
                  <h4 className="font-bold text-green-900 mb-2">✅ Acceptable Coupling</h4>
                  <div className="space-y-2 text-sm text-slate-700">
                    <div className="flex items-start gap-2">
                      <span className="font-bold text-green-700">1.</span>
                      <div>
                        <strong>Data Coupling:</strong> Modules share simple data (IDs, primitives)
                        <div className="text-xs text-slate-500 mt-1">Example: Pass user_id between modules</div>
                      </div>
                    </div>
                    <div className="flex items-start gap-2">
                      <span className="font-bold text-green-700">2.</span>
                      <div>
                        <strong>Message Coupling:</strong> Communication via events/messages
                        <div className="text-xs text-slate-500 mt-1">Example: UserCreatedEvent</div>
                      </div>
                    </div>
                    <div className="flex items-start gap-2">
                      <span className="font-bold text-green-700">3.</span>
                      <div>
                        <strong>Interface Coupling:</strong> Depend on shared interfaces
                        <div className="text-xs text-slate-500 mt-1">Example: IRepository, IEventBus</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div className="bg-red-50 border-2 border-red-400 rounded-lg p-4">
                  <h4 className="font-bold text-red-900 mb-2">❌ Avoid These Couplings</h4>
                  <div className="space-y-2 text-sm text-slate-700">
                    <div className="flex items-start gap-2">
                      <span className="font-bold text-red-700">1.</span>
                      <div>
                        <strong>Content Coupling:</strong> Module A modifies Module B's data
                        <div className="text-xs text-slate-500 mt-1">Example: Direct database access across modules</div>
                      </div>
                    </div>
                    <div className="flex items-start gap-2">
                      <span className="font-bold text-red-700">2.</span>
                      <div>
                        <strong>Common Coupling:</strong> Sharing global state
                        <div className="text-xs text-slate-500 mt-1">Example: Global variables, singletons</div>
                      </div>
                    </div>
                    <div className="flex items-start gap-2">
                      <span className="font-bold text-red-700">3.</span>
                      <div>
                        <strong>Control Coupling:</strong> Module A controls Module B's flow
                        <div className="text-xs text-slate-500 mt-1">Example: Passing flags to change behavior</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Anti-Corruption Layer */}
          <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-400 rounded-lg p-6">
            <h3 className="font-bold text-xl text-yellow-900 mb-4">🛡️ Anti-Corruption Layer (ACL)</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-yellow-800 mb-3">What is ACL?</h4>
                <div className="bg-white p-4 rounded border-2 border-yellow-300 text-sm text-slate-700">
                  A translation layer that prevents external concepts from leaking into your domain model.
                  <div className="mt-3 space-y-2">
                    <div>• Translates external DTOs to domain entities</div>
                    <div>• Protects domain from third-party changes</div>
                    <div>• Isolates external API peculiarities</div>
                  </div>
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-yellow-800 mb-3">Example Structure:</h4>
                <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs">
                  <div className="text-slate-400">// External API Response</div>
                  <div>interface StripeCustomer {'{'}</div>
                  <div className="ml-4">id: string;</div>
                  <div className="ml-4">email: string;</div>
                  <div>{'}'}</div>
                  <div className="mt-2 text-slate-400">// ACL Adapter</div>
                  <div className="text-blue-400">class StripeACL {'{'}</div>
                  <div className="ml-4">toDomain(stripe: StripeCustomer)</div>
                  <div className="ml-6">: User {'{'}</div>
                  <div className="ml-8">return User.create(</div>
                  <div className="ml-10">stripe.email</div>
                  <div className="ml-8">);</div>
                  <div className="ml-6">{'}'}</div>
                  <div>{'}'}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Context Mapping */}
          <div className="bg-white p-6 rounded-lg border-2 border-indigo-400 shadow-lg">
            <h3 className="font-bold text-xl text-indigo-900 mb-4">🗺️ Context Mapping Patterns</h3>
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div className="bg-indigo-50 border-2 border-indigo-300 rounded-lg p-4">
                  <h4 className="font-bold text-indigo-900 mb-2">Partnership</h4>
                  <div className="text-slate-700 mb-2">
                    Two modules evolve together with coordinated changes
                  </div>
                  <div className="text-xs bg-white p-2 rounded border border-indigo-200">
                    User ⇄ Authentication<br/>
                    (tightly integrated)
                  </div>
                </div>

                <div className="bg-green-50 border-2 border-green-300 rounded-lg p-4">
                  <h4 className="font-bold text-green-900 mb-2">Customer/Supplier</h4>
                  <div className="text-slate-700 mb-2">
                    Upstream provides services to downstream
                  </div>
                  <div className="text-xs bg-white p-2 rounded border border-green-200">
                    User → Project<br/>
                    (Project depends on User)
                  </div>
                </div>

                <div className="bg-purple-50 border-2 border-purple-300 rounded-lg p-4">
                  <h4 className="font-bold text-purple-900 mb-2">Published Language</h4>
                  <div className="text-slate-700 mb-2">
                    Well-documented shared protocol
                  </div>
                  <div className="text-xs bg-white p-2 rounded border border-purple-200">
                    Domain Events<br/>
                    (JSON Schema defined)
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },
    best_practices: {
      title: 'Best Practices & Patterns',
      description: 'Proven patterns for module organization',
      content: (
        <div className="space-y-6">
          {/* Module Structure Best Practices */}
          <div className="bg-white p-6 rounded-lg border-2 border-green-400 shadow-lg">
            <h3 className="font-bold text-xl text-green-900 mb-4">📁 Module Structure Best Practices</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-green-800 mb-3">✅ DO</h4>
                <div className="space-y-2 text-sm">
                  <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                    <strong>Keep modules self-contained</strong>
                    <div className="text-slate-600 mt-1">Each module should work independently</div>
                  </div>
                  <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                    <strong>Define clear public APIs</strong>
                    <div className="text-slate-600 mt-1">Explicit entry points via interfaces</div>
                  </div>
                  <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                    <strong>Use dependency injection</strong>
                    <div className="text-slate-600 mt-1">Wire dependencies at application startup</div>
                  </div>
                  <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                    <strong>Communicate via events</strong>
                    <div className="text-slate-600 mt-1">For cross-module side effects</div>
                  </div>
                  <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                    <strong>Keep domain pure</strong>
                    <div className="text-slate-600 mt-1">No framework dependencies in domain</div>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="font-semibold text-red-800 mb-3">❌ DON'T</h4>
                <div className="space-y-2 text-sm">
                  <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                    <strong>Don't share database tables</strong>
                    <div className="text-slate-600 mt-1">Each module owns its data</div>
                  </div>
                  <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                    <strong>Don't import other module internals</strong>
                    <div className="text-slate-600 mt-1">Only use public interfaces</div>
                  </div>
                  <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                    <strong>Don't create circular dependencies</strong>
                    <div className="text-slate-600 mt-1">A → B → A is forbidden</div>
                  </div>
                  <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                    <strong>Don't bypass the domain layer</strong>
                    <div className="text-slate-600 mt-1">Always go through use cases</div>
                  </div>
                  <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                    <strong>Don't share ORM entities</strong>
                    <div className="text-slate-600 mt-1">Use DTOs for cross-module data</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Code Organization Patterns */}
          <div className="bg-gradient-to-r from-blue-50 to-cyan-50 border-2 border-blue-400 rounded-lg p-6">
            <h3 className="font-bold text-xl text-blue-900 mb-4">🏗️ Code Organization Patterns</h3>
            <div className="space-y-4">
              
              {/* Pattern 1: Public API */}
              <div className="bg-white p-4 rounded-lg border-2 border-blue-300">
                <h4 className="font-semibold text-blue-900 mb-3">1. Explicit Public API (Module Facade)</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-sm text-slate-700 mb-2">Each module exports a single entry point:</div>
                    <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs">
                      <div className="text-slate-400">// user_management/index.ts</div>
                      <div className="text-blue-400">export interface UserModuleAPI {'{'}</div>
                      <div className="ml-4">getUserById(id: UUID): User;</div>
                      <div className="ml-4">validateUser(id: UUID): bool;</div>
                      <div>{'}'}</div>
                      <div className="mt-2 text-yellow-400">// Only expose what's needed</div>
                      <div>export const UserModule:</div>
                      <div className="ml-4">UserModuleAPI = ...</div>
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-slate-700 mb-2">Other modules import facade only:</div>
                    <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs">
                      <div className="text-slate-400">// project_management/service.ts</div>
                      <div className="text-purple-400">import</div>
                      <div className="ml-2">{'{ UserModule }'}</div>
                      <div className="ml-2">from '@modules/user';</div>
                      <div className="mt-2 text-green-400">// ✅ Use public API</div>
                      <div>const user = UserModule</div>
                      <div className="ml-4">.getUserById(id);</div>
                      <div className="mt-2 text-red-400">// ❌ Don't import internals</div>
                      <div className="text-red-500">import {'{ UserRepository }'}</div>
                      <div className="ml-2 text-red-500">from '@modules/user/infra'</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Pattern 2: Interface Segregation */}
              <div className="bg-white p-4 rounded-lg border-2 border-blue-300">
                <h4 className="font-semibold text-blue-900 mb-3">2. Interface Segregation</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-sm font-semibold text-red-800 mb-2">❌ Fat Interface (Bad)</div>
                    <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs">
                      <div className="text-red-400">// Too many responsibilities</div>
                      <div>interface IUserService {'{'}</div>
                      <div className="ml-4">createUser();</div>
                      <div className="ml-4">updateUser();</div>
                      <div className="ml-4">deleteUser();</div>
                      <div className="ml-4">sendEmail();</div>
                      <div className="ml-4">generateReport();</div>
                      <div className="ml-4">exportData();</div>
                      <div>{'}'}</div>
                    </div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-green-800 mb-2">✅ Segregated Interfaces (Good)</div>
                    <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs">
                      <div className="text-green-400">// Small, focused interfaces</div>
                      <div>interface IUserQuery {'{'}</div>
                      <div className="ml-4">getUserById(id);</div>
                      <div>{'}'}</div>
                      <div className="mt-2">interface IUserCommand {'{'}</div>
                      <div className="ml-4">createUser();</div>
                      <div className="ml-4">updateUser();</div>
                      <div>{'}'}</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Pattern 3: DTO Pattern */}
              <div className="bg-white p-4 rounded-lg border-2 border-blue-300">
                <h4 className="font-semibold text-blue-900 mb-3">3. Data Transfer Objects (DTOs)</h4>
                <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs">
                  <div className="text-slate-400">// Never share domain entities across modules</div>
                  <div className="text-red-400">// ❌ BAD: Sharing entity</div>
                  <div className="text-red-500">projectService.create(userEntity);</div>
                  <div className="mt-2 text-green-400">// ✅ GOOD: Use DTOs</div>
                  <div>interface UserDTO {'{'}</div>
                  <div className="ml-4">id: UUID;</div>
                  <div className="ml-4">email: string;</div>
                  <div className="ml-4">name: string;</div>
                  <div>{'}'}</div>
                  <div className="mt-2">projectService.create(userDto);</div>
                </div>
              </div>
            </div>
          </div>

          {/* Testing Best Practices */}
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-400 rounded-lg p-6">
            <h3 className="font-bold text-xl text-purple-900 mb-4">🧪 Testing Module Dependencies</h3>
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div className="bg-white p-4 rounded border-2 border-purple-300">
                <h4 className="font-bold text-purple-900 mb-2">Unit Tests</h4>
                <div className="text-slate-700 space-y-2">
                  <div>• Test each layer in isolation</div>
                  <div>• Mock all dependencies</div>
                  <div>• No database/network calls</div>
                  <div>• Fast execution (&lt;1s)</div>
                </div>
                <div className="mt-3 bg-purple-50 p-2 rounded text-xs">
                  Example: Test UserService with mocked IUserRepository
                </div>
              </div>

              <div className="bg-white p-4 rounded border-2 border-purple-300">
                <h4 className="font-bold text-purple-900 mb-2">Integration Tests</h4>
                <div className="text-slate-700 space-y-2">
                  <div>• Test module boundaries</div>
                  <div>• Real database (test DB)</div>
                  <div>• Module interactions</div>
                  <div>• Medium speed (~5s)</div>
                </div>
                <div className="mt-3 bg-purple-50 p-2 rounded text-xs">
                  Example: Test User → Project interaction via events
                </div>
              </div>

              <div className="bg-white p-4 rounded border-2 border-purple-300">
                <h4 className="font-bold text-purple-900 mb-2">Architecture Tests</h4>
                <div className="text-slate-700 space-y-2">
                  <div>• Enforce dependency rules</div>
                  <div>• Check layer violations</div>
                  <div>• Detect circular deps</div>
                  <div>• Run in CI/CD</div>
                </div>
                <div className="mt-3 bg-purple-50 p-2 rounded text-xs">
                  Example: ArchUnit to verify Domain doesn't import Infrastructure
                </div>
              </div>
            </div>
          </div>

          {/* Refactoring Strategies */}
          <div className="bg-gradient-to-r from-orange-50 to-red-50 border-2 border-orange-400 rounded-lg p-6">
            <h3 className="font-bold text-xl text-orange-900 mb-4">🔄 Refactoring from Monolith to Modular Monolith</h3>
            <div className="space-y-3">
              <div className="bg-white p-4 rounded border-2 border-orange-300">
                <div className="flex items-start gap-3">
                  <div className="bg-orange-500 text-white font-bold rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">1</div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-orange-900 mb-1">Identify Bounded Contexts</h4>
                    <div className="text-sm text-slate-700">Analyze your domain and find natural boundaries based on business capabilities</div>
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 rounded border-2 border-orange-300">
                <div className="flex items-start gap-3">
                  <div className="bg-orange-500 text-white font-bold rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">2</div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-orange-900 mb-1">Extract Module by Module</h4>
                    <div className="text-sm text-slate-700">Start with the most isolated context (e.g., Notifications) and gradually extract others</div>
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 rounded border-2 border-orange-300">
                <div className="flex items-start gap-3">
                  <div className="bg-orange-500 text-white font-bold rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">3</div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-orange-900 mb-1">Replace Direct Calls with Events</h4>
                    <div className="text-sm text-slate-700">Convert synchronous cross-module calls to asynchronous event-driven communication</div>
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 rounded border-2 border-orange-300">
                <div className="flex items-start gap-3">
                  <div className="bg-orange-500 text-white font-bold rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">4</div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-orange-900 mb-1">Separate Database Schemas</h4>
                    <div className="text-sm text-slate-700">Move each module's tables to separate schemas (still in same database initially)</div>
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 rounded border-2 border-orange-300">
                <div className="flex items-start gap-3">
                  <div className="bg-orange-500 text-white font-bold rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">5</div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-orange-900 mb-1">Add Architecture Tests</h4>
                    <div className="text-sm text-slate-700">Prevent regression by enforcing module boundaries with automated tests</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },
    tools_enforcement: {
      title: 'Tools & Enforcement',
      description: 'Automated tools to enforce dependency rules',
      content: (
        <div className="space-y-6">
          {/* Architecture Testing Tools */}
          <div className="bg-white p-6 rounded-lg border-2 border-teal-400 shadow-lg">
            <h3 className="font-bold text-xl text-teal-900 mb-4">🛠️ Architecture Testing Tools</h3>
            <div className="grid grid-cols-2 gap-6">
              
              {/* Python Tools */}
              <div className="space-y-4">
                <h4 className="font-semibold text-teal-800 bg-teal-100 p-2 rounded">Python / FastAPI</h4>
                
                <div className="bg-teal-50 border-2 border-teal-300 rounded-lg p-4">
                  <h5 className="font-bold text-teal-900 mb-2">1. Import Linter</h5>
                  <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs mb-2">
                    <div className="text-slate-400"># pyproject.toml</div>
                    <div>[tool.importlinter]</div>
                    <div>root_package = "src"</div>
                    <div>[tool.importlinter.contracts.1]</div>
                    <div>name = "Domain independence"</div>
                    <div>type = "forbidden"</div>
                    <div>source_modules = [</div>
                    <div className="ml-4">"src.modules.*.domain"</div>
                    <div>]</div>
                    <div>forbidden_modules = [</div>
                    <div className="ml-4">"src.modules.*.infrastructure",</div>
                    <div className="ml-4">"fastapi"</div>
                    <div>]</div>
                  </div>
                  <div className="text-sm text-slate-700">
                    Prevents domain layer from importing infrastructure or framework code
                  </div>
                </div>

                <div className="bg-teal-50 border-2 border-teal-300 rounded-lg p-4">
                  <h5 className="font-bold text-teal-900 mb-2">2. Pytest with Custom Rules</h5>
                  <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs mb-2">
                    <div className="text-slate-400"># tests/architecture/test_dependencies.py</div>
                    <div className="text-purple-400">def</div>
                    <div className="ml-2">test_no_circular_deps():</div>
                    <div className="ml-4">deps = analyze_imports()</div>
                    <div className="ml-4 text-blue-400">assert</div>
                    <div className="ml-6">not has_cycles(deps)</div>
                  </div>
                </div>

                <div className="bg-teal-50 border-2 border-teal-300 rounded-lg p-4">
                  <h5 className="font-bold text-teal-900 mb-2">3. Dependency Cruiser</h5>
                  <div className="text-sm text-slate-700 mb-2">
                    Visualizes and validates dependencies
                  </div>
                  <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs">
                    <div>pip install dependency-cruiser</div>
                    <div>depcruiser src/ --output-type dot</div>
                  </div>
                </div>
              </div>

              {/* TypeScript/NestJS Tools */}
              <div className="space-y-4">
                <h4 className="font-semibold text-blue-800 bg-blue-100 p-2 rounded">TypeScript / NestJS</h4>
                
                <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-4">
                  <h5 className="font-bold text-blue-900 mb-2">1. ESLint with Custom Rules</h5>
                  <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs mb-2">
                    <div className="text-slate-400">// .eslintrc.js</div>
                    <div>module.exports = {'{'}</div>
                    <div className="ml-4">rules: {'{'}</div>
                    <div className="ml-8 text-yellow-400">'no-restricted-imports'</div>
                    <div className="ml-8">: [</div>
                    <div className="ml-12">'error',</div>
                    <div className="ml-12">{'{'}</div>
                    <div className="ml-16">patterns: [</div>
                    <div className="ml-20 text-red-400">'**/infrastructure/**',</div>
                    <div className="ml-20 text-red-400">'**/presentation/**'</div>
                    <div className="ml-16">]</div>
                    <div className="ml-12">{'}'}</div>
                    <div className="ml-8">]</div>
                    <div className="ml-4">{'}'}</div>
                    <div>{'}'}</div>
                  </div>
                </div>

                <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-4">
                  <h5 className="font-bold text-blue-900 mb-2">2. ts-arch</h5>
                  <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs mb-2">
                    <div className="text-slate-400">// tests/architecture.spec.ts</div>
                    <div className="text-purple-400">import</div>
                    <div className="ml-2">{'{ filesOfProject }'}</div>
                    <div className="ml-2">from 'ts-arch';</div>
                    <div className="mt-2">describe('Architecture', () => {'{'}</div>
                    <div className="ml-4">it('domain has no deps', () => {'{'}</div>
                    <div className="ml-8">const files = filesOfProject();</div>
                    <div className="ml-8">files.inFolder('domain')</div>
                    <div className="ml-10">.shouldNot()</div>
                    <div className="ml-10">.dependOnFiles()</div>
                    <div className="ml-10">.inFolder('infrastructure');</div>
                    <div className="ml-4">{'}'})</div>
                    <div>{'}'});</div>
                  </div>
                </div>

                <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-4">
                  <h5 className="font-bold text-blue-900 mb-2">3. Madge</h5>
                  <div className="text-sm text-slate-700 mb-2">
                    Detect circular dependencies
                  </div>
                  <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs">
                    <div>npx madge --circular src/</div>
                    <div>npx madge --image graph.svg src/</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* CI/CD Integration */}
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-400 rounded-lg p-6">
            <h3 className="font-bold text-xl text-indigo-900 mb-4">⚙️ CI/CD Integration</h3>
            <div className="bg-white p-4 rounded-lg border-2 border-indigo-300">
              <h4 className="font-semibold text-indigo-900 mb-3">GitHub Actions Example</h4>
              <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs overflow-x-auto">
                <div className="text-slate-400"># .github/workflows/architecture-tests.yml</div>
                <div>name: Architecture Tests</div>
                <div>on: [push, pull_request]</div>
                <div className="mt-2">jobs:</div>
                <div className="ml-4">architecture:</div>
                <div className="ml-8">runs-on: ubuntu-latest</div>
                <div className="ml-8">steps:</div>
                <div className="ml-12">- uses: actions/checkout@v3</div>
                <div className="mt-2 ml-12">- name: Install dependencies</div>
                <div className="ml-16">run: npm install</div>
                <div className="mt-2 ml-12">- name: Check circular dependencies</div>
                <div className="ml-16">run: npx madge --circular src/</div>
                <div className="mt-2 ml-12">- name: Validate imports</div>
                <div className="ml-16">run: npm run lint:imports</div>
                <div className="mt-2 ml-12">- name: Run architecture tests</div>
                <div className="ml-16">run: npm run test:architecture</div>
                <div className="mt-2 ml-12 text-red-400">- name: Fail on violations</div>
                <div className="ml-16 text-red-400">if: failure()</div>
                <div className="ml-16 text-red-400">run: echo "Architecture rules violated!"</div>
              </div>
            </div>
          </div>

          {/* Visualization Tools */}
          <div className="bg-white p-6 rounded-lg border-2 border-yellow-400 shadow-lg">
            <h3 className="font-bold text-xl text-yellow-900 mb-4">📊 Dependency Visualization</h3>
            <div className="grid grid-cols-2 gap-6">
              <div className="bg-yellow-50 border-2 border-yellow-300 rounded-lg p-4">
                <h4 className="font-bold text-yellow-900 mb-2">Dependency Graph</h4>
                <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs mb-3">
                  <div className="text-slate-400"># Generate dependency graph</div>
                  <div>pydeps src/</div>
                  <div className="ml-4">--max-bacon=2</div>
                  <div className="ml-4">--cluster</div>
                  <div className="ml-4">--rankdir LR</div>
                  <div className="ml-4">-o deps.svg</div>
                </div>
                <div className="text-sm text-slate-700">
                  Creates visual diagram showing module dependencies
                </div>
              </div>

              <div className="bg-yellow-50 border-2 border-yellow-300 rounded-lg p-4">
                <h4 className="font-bold text-yellow-900 mb-2">Module Metrics</h4>
                <div className="bg-slate-900 text-green-400 p-3 rounded font-mono text-xs mb-3">
                  <div className="text-slate-400"># Calculate coupling metrics</div>
                  <div>radon cc src/</div>
                  <div className="ml-4">-a</div>
                  <div className="ml-4">--total-average</div>
                </div>
                <div className="text-sm text-slate-700">
                  Measures code complexity and coupling
                </div>
              </div>
            </div>
          </div>

          {/* Pre-commit Hooks */}
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400 rounded-lg p-6">
            <h3 className="font-bold text-xl text-green-900 mb-4">🪝 Pre-commit Hooks</h3>
            <div className="bg-white p-4 rounded-lg border-2 border-green-300">
              <div className="bg-slate-900 text-green-400 p-4 rounded font-mono text-xs overflow-x-auto">
                <div className="text-slate-400"># .pre-commit-config.yaml</div>
                <div>repos:</div>
                <div className="ml-4">- repo: local</div>
                <div className="ml-8">hooks:</div>
                <div className="ml-12">- id: check-architecture</div>
                <div className="ml-16">name: Check Architecture Rules</div>
                <div className="ml-16">entry: python scripts/check_deps.py</div>
                <div className="ml-16">language: system</div>
                <div className="ml-16">pass_filenames: false</div>
                <div className="mt-2 ml-12">- id: no-circular-deps</div>
                <div className="ml-16">name: Check Circular Dependencies</div>
                <div className="ml-16">entry: madge --circular src/</div>
                <div className="ml-16">language: node</div>
              </div>
              <div className="mt-4 text-sm text-slate-700">
                Runs automatically before each commit, preventing violations from being committed
              </div>
            </div>
          </div>

          {/* Metrics Dashboard */}
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-400 rounded-lg p-6">
            <h3 className="font-bold text-xl text-purple-900 mb-4">📈 Architecture Metrics Dashboard</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-white p-4 rounded border-2 border-purple-300 text-center">
                <div className="text-3xl font-bold text-purple-600">87%</div>
                <div className="text-sm text-slate-600 mt-1">Test Coverage</div>
              </div>
              <div className="bg-white p-4 rounded border-2 border-purple-300 text-center">
                <div className="text-3xl font-bold text-green-600">0</div>
                <div className="text-sm text-slate-600 mt-1">Circular Deps</div>
              </div>
              <div className="bg-white p-4 rounded border-2 border-purple-300 text-center">
                <div className="text-3xl font-bold text-blue-600">12</div>
                <div className="text-sm text-slate-600 mt-1">Module Count</div>
              </div>
              <div className="bg-white p-4 rounded border-2 border-purple-300 text-center">
                <div className="text-3xl font-bold text-orange-600">A</div>
                <div className="text-sm text-slate-600 mt-1">Code Quality</div>
              </div>
            </div>
            <div className="mt-4 text-sm text-slate-600">
              Track these metrics over time using SonarQube, CodeClimate, or custom scripts
            </div>
          </div>
        </div>
      )
    }
  };

  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-50 to-slate-100 p-8 overflow-auto">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-2 text-slate-800">
          Module Dependency Flows & Best Practices
        </h1>
        <p className="text-center text-slate-600 mb-8">
          Managing dependencies in Clean Architecture
        </p>

        {/* Navigation */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {Object.entries(views).map(([key, view]) => (
            <button
              key={key}
              onClick={() => setSelectedView(key)}
              className={`px-6 py-3 rounded-lg font-medium transition-all whitespace-nowrap ${
                selectedView === key
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                  : 'bg-white text-slate-700 border-2 border-slate-300 hover:border-indigo-400'
              }`}
            >
              {view.title}
            </button>
          ))}
        </div>

        {/* Content Header */}
        <div className="bg-gradient-to-br from-indigo-50 to-purple-50 border-2 border-indigo-300 rounded-lg p-6 mb-6">
          <h2 className="text-2xl font-bold text-indigo-900 mb-2">
            {views[selectedView].title}
          </h2>
          <p className="text-slate-700">{views[selectedView].description}</p>
        </div>

        {/* Content */}
        {views[selectedView].content}

        {/* Summary Card */}
        <div className="mt-8 bg-gradient-to-r from-slate-700 to-slate-800 text-white rounded-lg p-6 shadow-lg">
          <h2 className="text-xl font-bold mb-4">🎯 Key Takeaways</h2>
          <div className="grid grid-cols-2 gap-6 text-sm">
            <div className="space-y-2">
              <div className="flex items-start gap-2">
                <span className="text-yellow-400">✓</span>
                <span>Dependencies must point inward toward the domain</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-yellow-400">✓</span>
                <span>Use interfaces to invert dependencies</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-yellow-400">✓</span>
                <span>Communicate between modules via events</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-yellow-400">✓</span>
                <span>Keep domain layer pure and framework-agnostic</span>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-start gap-2">
                <span className="text-yellow-400">✓</span>
                <span>Define explicit public APIs for each module</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-yellow-400">✓</span>
                <span>Use DTOs for cross-module data transfer</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-yellow-400">✓</span>
                <span>Enforce rules with automated architecture tests</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-yellow-400">✓</span>
                <span>Visualize dependencies to spot violations early</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModuleDependencyFlows;