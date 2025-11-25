import React, { useState } from 'react';

const ModuleInteractionFlows = () => {
  const [selectedFlow, setSelectedFlow] = useState('sync');

  const flows = {
    sync: {
      title: 'Synchronous Communication (Direct API Calls)',
      description: 'Direct method calls within the same process',
      diagram: (
        <div className="space-y-6">
          {/* Flow 1: User Creates Project */}
          <div className="bg-white p-6 rounded-lg border-2 border-blue-400 shadow-lg">
            <h3 className="font-bold text-lg mb-4 text-blue-900">Scenario 1: User Creates Project with File Upload</h3>
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-40 bg-slate-700 text-white p-3 rounded text-center font-semibold">
                  Client
                </div>
                <div className="flex-1 border-t-2 border-blue-500 relative">
                  <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-blue-100 px-3 py-1 rounded text-sm">
                    POST /api/v1/projects
                  </div>
                </div>
                <div className="w-40 bg-blue-500 text-white p-3 rounded text-center font-semibold">
                  Project API
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-40"></div>
                <div className="flex-1 border-t-2 border-green-500 relative">
                  <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-green-100 px-3 py-1 rounded text-sm">
                    Call: ProjectService.create()
                  </div>
                </div>
                <div className="w-40 bg-green-500 text-white p-3 rounded text-center font-semibold">
                  Project Service
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-40"></div>
                <div className="flex-1 border-t-2 border-purple-500 relative">
                  <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-purple-100 px-3 py-1 rounded text-sm">
                    Validate: User exists?
                  </div>
                </div>
                <div className="w-40 bg-purple-500 text-white p-3 rounded text-center font-semibold">
                  User Service
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-40"></div>
                <div className="flex-1 border-t-2 border-orange-500 relative">
                  <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-orange-100 px-3 py-1 rounded text-sm">
                    Save to DB
                  </div>
                </div>
                <div className="w-40 bg-orange-500 text-white p-3 rounded text-center font-semibold">
                  Project Repo
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-40"></div>
                <div className="flex-1 border-t-2 border-teal-500 relative">
                  <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-teal-100 px-3 py-1 rounded text-sm">
                    Event: ProjectCreated
                  </div>
                </div>
                <div className="w-40 bg-teal-500 text-white p-3 rounded text-center font-semibold">
                  Event Bus
                </div>
              </div>

              <div className="bg-blue-50 p-3 rounded text-sm">
                <strong>✅ Advantages:</strong> Simple, immediate response, transactional
                <br />
                <strong>⚠️ Considerations:</strong> Tight coupling, synchronous blocking
              </div>
            </div>
          </div>
        </div>
      )
    },
    async: {
      title: 'Asynchronous Communication (Domain Events)',
      description: 'Event-driven communication via internal event bus',
      diagram: (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border-2 border-purple-400 shadow-lg">
            <h3 className="font-bold text-lg mb-4 text-purple-900">Scenario 2: File Upload Triggers Notifications</h3>
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-40 bg-green-600 text-white p-3 rounded text-center font-semibold">
                  File Service
                </div>
                <div className="flex-1 border-t-2 border-purple-500 relative">
                  <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-purple-100 px-3 py-1 rounded text-sm">
                    1. Upload file
                  </div>
                </div>
                <div className="w-40 bg-orange-600 text-white p-3 rounded text-center font-semibold">
                  File Repository
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-40 bg-green-600 text-white p-3 rounded text-center font-semibold">
                  File Service
                </div>
                <div className="flex-1 border-t-2 border-red-500 relative">
                  <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-red-100 px-3 py-1 rounded text-sm">
                    2. Publish: FileUploadedEvent
                  </div>
                </div>
                <div className="w-40 bg-red-600 text-white p-3 rounded text-center font-semibold">
                  Event Bus
                </div>
              </div>

              <div className="mt-6 space-y-3">
                <div className="font-semibold text-purple-900">3. Event Handlers (Async Subscribers):</div>
                
                <div className="flex items-center gap-4">
                  <div className="w-40 bg-red-600 text-white p-3 rounded text-center font-semibold">
                    Event Bus
                  </div>
                  <div className="flex-1 border-t-2 border-blue-500 relative">
                    <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-blue-100 px-3 py-1 rounded text-sm">
                      Handle FileUploadedEvent
                    </div>
                  </div>
                  <div className="w-40 bg-blue-600 text-white p-3 rounded text-center font-semibold">
                    Notification Handler
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="w-40 bg-red-600 text-white p-3 rounded text-center font-semibold">
                    Event Bus
                  </div>
                  <div className="flex-1 border-t-2 border-yellow-500 relative">
                    <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-yellow-100 px-3 py-1 rounded text-sm">
                      Handle FileUploadedEvent
                    </div>
                  </div>
                  <div className="w-40 bg-yellow-600 text-white p-3 rounded text-center font-semibold">
                    Audit Handler
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="w-40 bg-red-600 text-white p-3 rounded text-center font-semibold">
                    Event Bus
                  </div>
                  <div className="flex-1 border-t-2 border-teal-500 relative">
                    <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 bg-teal-100 px-3 py-1 rounded text-sm">
                      Handle FileUploadedEvent
                    </div>
                  </div>
                  <div className="w-40 bg-teal-600 text-white p-3 rounded text-center font-semibold">
                    Analytics Handler
                  </div>
                </div>
              </div>

              <div className="bg-purple-50 p-3 rounded text-sm mt-4">
                <strong>✅ Advantages:</strong> Loose coupling, scalable, non-blocking
                <br />
                <strong>⚠️ Considerations:</strong> Eventual consistency, harder debugging
              </div>
            </div>
          </div>
        </div>
      )
    },
    orchestration: {
      title: 'Orchestration Pattern (Saga)',
      description: 'Complex workflows coordinated by orchestrator',
      diagram: (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border-2 border-indigo-400 shadow-lg">
            <h3 className="font-bold text-lg mb-4 text-indigo-900">Scenario 3: Complete User Onboarding Workflow</h3>
            <div className="space-y-4">
              <div className="text-center">
                <div className="inline-block bg-indigo-600 text-white p-4 rounded-lg font-bold text-lg">
                  Onboarding Orchestrator
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="space-y-2">
                  <div className="bg-blue-500 text-white p-3 rounded text-center font-semibold">
                    Step 1: Create User
                  </div>
                  <div className="text-sm text-center text-slate-600">
                    ↓ User Service
                  </div>
                  <div className="bg-blue-100 p-2 rounded text-center text-sm">
                    Success ✓
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="bg-green-500 text-white p-3 rounded text-center font-semibold">
                    Step 2: Setup Workspace
                  </div>
                  <div className="text-sm text-center text-slate-600">
                    ↓ File Service
                  </div>
                  <div className="bg-green-100 p-2 rounded text-center text-sm">
                    Success ✓
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="bg-purple-500 text-white p-3 rounded text-center font-semibold">
                    Step 3: Send Welcome
                  </div>
                  <div className="text-sm text-center text-slate-600">
                    ↓ Notification Service
                  </div>
                  <div className="bg-purple-100 p-2 rounded text-center text-sm">
                    Success ✓
                  </div>
                </div>
              </div>

              <div className="border-t-4 border-dashed border-red-400 my-6"></div>

              <div className="bg-red-50 p-4 rounded">
                <h4 className="font-semibold text-red-900 mb-2">Compensating Transactions (Rollback):</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-3">
                    <span className="text-red-600 font-bold">❌</span>
                    <span>If Step 3 fails → Delete workspace (Step 2 compensation)</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-red-600 font-bold">❌</span>
                    <span>If Step 2 fails → Deactivate user (Step 1 compensation)</span>
                  </div>
                </div>
              </div>

              <div className="bg-indigo-50 p-3 rounded text-sm">
                <strong>✅ Advantages:</strong> Complex workflow management, rollback support
                <br />
                <strong>⚠️ Considerations:</strong> More complex implementation
              </div>
            </div>
          </div>
        </div>
      )
    },
    shared_kernel: {
      title: 'Shared Kernel Pattern',
      description: 'Common utilities and interfaces shared across modules',
      diagram: (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border-2 border-yellow-400 shadow-lg">
            <h3 className="font-bold text-lg mb-4 text-yellow-900">Shared Components Architecture</h3>
            
            <div className="text-center mb-6">
              <div className="inline-block bg-yellow-600 text-white p-4 rounded-lg font-bold text-lg">
                Shared Kernel
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-3">
                <h4 className="font-semibold text-yellow-800">Core Domain:</h4>
                <div className="space-y-2">
                  <div className="bg-yellow-50 p-3 rounded border border-yellow-300">
                    <div className="font-semibold text-sm">BaseEntity</div>
                    <div className="text-xs text-slate-600">id, created_at, updated_at</div>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded border border-yellow-300">
                    <div className="font-semibold text-sm">AggregateRoot</div>
                    <div className="text-xs text-slate-600">Domain events handling</div>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded border border-yellow-300">
                    <div className="font-semibold text-sm">ValueObject</div>
                    <div className="text-xs text-slate-600">Immutable values</div>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded border border-yellow-300">
                    <div className="font-semibold text-sm">Result&lt;T&gt;</div>
                    <div className="text-xs text-slate-600">Success/Failure handling</div>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="font-semibold text-yellow-800">Shared Interfaces:</h4>
                <div className="space-y-2">
                  <div className="bg-yellow-50 p-3 rounded border border-yellow-300">
                    <div className="font-semibold text-sm">IRepository&lt;T&gt;</div>
                    <div className="text-xs text-slate-600">CRUD operations</div>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded border border-yellow-300">
                    <div className="font-semibold text-sm">IUnitOfWork</div>
                    <div className="text-xs text-slate-600">Transaction management</div>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded border border-yellow-300">
                    <div className="font-semibold text-sm">IEventBus</div>
                    <div className="text-xs text-slate-600">Event publishing</div>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded border border-yellow-300">
                    <div className="font-semibold text-sm">ILogger</div>
                    <div className="text-xs text-slate-600">Logging abstraction</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-4 gap-4">
              <div className="bg-blue-100 p-3 rounded text-center">
                <div className="font-semibold text-sm text-blue-900">User Module</div>
                <div className="text-xs text-slate-600 mt-1">Uses shared kernel</div>
              </div>
              <div className="bg-green-100 p-3 rounded text-center">
                <div className="font-semibold text-sm text-green-900">File Module</div>
                <div className="text-xs text-slate-600 mt-1">Uses shared kernel</div>
              </div>
              <div className="bg-purple-100 p-3 rounded text-center">
                <div className="font-semibold text-sm text-purple-900">Project Module</div>
                <div className="text-xs text-slate-600 mt-1">Uses shared kernel</div>
              </div>
              <div className="bg-orange-100 p-3 rounded text-center">
                <div className="font-semibold text-sm text-orange-900">Notification</div>
                <div className="text-xs text-slate-600 mt-1">Uses shared kernel</div>
              </div>
            </div>

            <div className="bg-yellow-50 p-3 rounded text-sm mt-4">
              <strong>✅ Benefits:</strong> Code reuse, consistency, reduced duplication
              <br />
              <strong>⚠️ Rule:</strong> Minimize shared kernel - only truly common code
            </div>
          </div>
        </div>
      )
    }
  };

  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-50 to-slate-100 p-8 overflow-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-2 text-slate-800">
          Module Interaction & Communication Flows
        </h1>
        <p className="text-center text-slate-600 mb-8">
          Communication patterns in Modular Monolith
        </p>

        {/* Navigation Tabs */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {Object.entries(flows).map(([key, flow]) => (
            <button
              key={key}
              onClick={() => setSelectedFlow(key)}
              className={`px-6 py-3 rounded-lg font-medium transition-all whitespace-nowrap ${
                selectedFlow === key
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                  : 'bg-white text-slate-700 border-2 border-slate-300 hover:border-indigo-400'
              }`}
            >
              {flow.title}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="bg-gradient-to-br from-indigo-50 to-purple-50 border-2 border-indigo-300 rounded-lg p-6 mb-6">
          <h2 className="text-2xl font-bold text-indigo-900 mb-2">
            {flows[selectedFlow].title}
          </h2>
          <p className="text-slate-700">{flows[selectedFlow].description}</p>
        </div>

        {flows[selectedFlow].diagram}

        {/* Communication Comparison */}
        <div className="mt-8 bg-white border-2 border-slate-300 rounded-lg p-6 shadow-lg">
          <h2 className="text-xl font-bold text-slate-800 mb-4">📊 Communication Patterns Comparison</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-100">
                <tr>
                  <th className="px-4 py-2 text-left font-semibold">Pattern</th>
                  <th className="px-4 py-2 text-left font-semibold">Use When</th>
                  <th className="px-4 py-2 text-left font-semibold">Advantages</th>
                  <th className="px-4 py-2 text-left font-semibold">Disadvantages</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-slate-200">
                  <td className="px-4 py-3 font-semibold text-blue-700">Synchronous</td>
                  <td className="px-4 py-3">Immediate response needed</td>
                  <td className="px-4 py-3 text-green-700">Simple, Transactional</td>
                  <td className="px-4 py-3 text-red-700">Tight coupling, Blocking</td>
                </tr>
                <tr className="border-t border-slate-200 bg-slate-50">
                  <td className="px-4 py-3 font-semibold text-purple-700">Async Events</td>
                  <td className="px-4 py-3">Side effects, notifications</td>
                  <td className="px-4 py-3 text-green-700">Loose coupling, Scalable</td>
                  <td className="px-4 py-3 text-red-700">Eventual consistency</td>
                </tr>
                <tr className="border-t border-slate-200">
                  <td className="px-4 py-3 font-semibold text-indigo-700">Orchestration</td>
                  <td className="px-4 py-3">Complex workflows</td>
                  <td className="px-4 py-3 text-green-700">Rollback support, Clear flow</td>
                  <td className="px-4 py-3 text-red-700">Complex implementation</td>
                </tr>
                <tr className="border-t border-slate-200 bg-slate-50">
                  <td className="px-4 py-3 font-semibold text-yellow-700">Shared Kernel</td>
                  <td className="px-4 py-3">Common utilities</td>
                  <td className="px-4 py-3 text-green-700">Code reuse, Consistency</td>
                  <td className="px-4 py-3 text-red-700">Can create coupling</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Best Practices */}
        <div className="mt-8 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400 rounded-lg p-6">
          <h2 className="text-xl font-bold text-green-900 mb-4">✅ Best Practices</h2>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="space-y-2">
              <div className="flex items-start gap-2">
                <span className="text-green-600 font-bold">1.</span>
                <span>Use synchronous calls for critical operations requiring immediate feedback</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-green-600 font-bold">2.</span>
                <span>Use async events for notifications, auditing, and analytics</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-green-600 font-bold">3.</span>
                <span>Implement circuit breakers for external service calls</span>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-start gap-2">
                <span className="text-green-600 font-bold">4.</span>
                <span>Keep shared kernel minimal - only truly common code</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-green-600 font-bold">5.</span>
                <span>Use orchestration for complex multi-step workflows</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-green-600 font-bold">6.</span>
                <span>Always implement proper error handling and logging</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModuleInteractionFlows;