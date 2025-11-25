import React, { useState } from 'react';

const UseCaseFlows = () => {
  const [selectedUseCase, setSelectedUseCase] = useState('user_registration');

  const useCases = {
    user_registration: {
      title: 'User Registration & Onboarding',
      description: 'Complete user signup flow with email verification',
      actors: ['Client', 'API Gateway', 'User Service', 'Email Service', 'Database', 'Event Bus'],
      steps: [
        { actor: 0, to: 1, action: 'POST /api/v1/users/register', detail: '{ email, password, name }' },
        { actor: 1, to: 2, action: 'RegisterUserCommand', detail: 'Validate & create user' },
        { actor: 2, to: 2, action: 'Validate Email Format', detail: 'Business rules check', type: 'internal' },
        { actor: 2, to: 4, action: 'Check Email Exists', detail: 'SELECT * FROM users WHERE email = ?' },
        { actor: 4, to: 2, action: 'Email not found ✓', detail: '', type: 'return' },
        { actor: 2, to: 2, action: 'Hash Password', detail: 'bcrypt.hash()', type: 'internal' },
        { actor: 2, to: 2, action: 'Create User Entity', detail: 'User.create()', type: 'internal' },
        { actor: 2, to: 4, action: 'INSERT INTO users', detail: 'Save to database' },
        { actor: 4, to: 2, action: 'User created ✓', detail: 'Return user_id', type: 'return' },
        { actor: 2, to: 5, action: 'Publish: UserRegisteredEvent', detail: '{ user_id, email, timestamp }' },
        { actor: 5, to: 3, action: 'Handle UserRegisteredEvent', detail: 'Send welcome email' },
        { actor: 3, to: 3, action: 'Generate verification token', detail: 'JWT token', type: 'internal' },
        { actor: 3, to: 3, action: 'Render email template', detail: 'Welcome email with link', type: 'internal' },
        { actor: 3, to: 3, action: 'Send via SMTP', detail: 'Email provider', type: 'internal' },
        { actor: 2, to: 1, action: 'Return Success', detail: '{ user_id, status: pending }', type: 'return' },
        { actor: 1, to: 0, action: '201 Created', detail: '{ id, email, verification_required: true }', type: 'return' },
      ],
      notes: [
        { after: 5, text: 'Async: Email sent in background', position: 'right' },
        { after: 10, text: 'Event-driven: Loose coupling', position: 'right' }
      ]
    },
    file_upload: {
      title: 'File Upload with Processing',
      description: 'Upload file, validate, store in S3, and create thumbnails',
      actors: ['Client', 'API Gateway', 'File Service', 'Storage (S3)', 'Worker Queue', 'Database'],
      steps: [
        { actor: 0, to: 1, action: 'POST /api/v1/files/upload', detail: 'Multipart form-data' },
        { actor: 1, to: 2, action: 'UploadFileCommand', detail: 'File metadata + binary' },
        { actor: 2, to: 2, action: 'Validate File', detail: 'Size, type, virus scan', type: 'internal' },
        { actor: 2, to: 2, action: 'Generate unique filename', detail: 'UUID + extension', type: 'internal' },
        { actor: 2, to: 3, action: 'Upload to S3', detail: 'PUT s3://bucket/files/uuid.jpg' },
        { actor: 3, to: 2, action: 'S3 URL returned ✓', detail: 'https://s3.../uuid.jpg', type: 'return' },
        { actor: 2, to: 5, action: 'INSERT INTO files', detail: 'Save metadata' },
        { actor: 5, to: 2, action: 'File record created ✓', detail: 'file_id', type: 'return' },
        { actor: 2, to: 4, action: 'Enqueue: ProcessFileJob', detail: '{ file_id, type: thumbnail }' },
        { actor: 2, to: 1, action: 'Return Success', detail: '{ file_id, url, status: processing }', type: 'return' },
        { actor: 1, to: 0, action: '201 Created', detail: '{ id, url, processing: true }', type: 'return' },
        { actor: 4, to: 4, action: 'Worker picks job', detail: 'Celery/Bull worker', type: 'async' },
        { actor: 4, to: 3, action: 'Download original', detail: 'GET from S3', type: 'async' },
        { actor: 4, to: 4, action: 'Generate thumbnail', detail: 'PIL/Sharp resize', type: 'async' },
        { actor: 4, to: 3, action: 'Upload thumbnail', detail: 'PUT s3://.../thumb_uuid.jpg', type: 'async' },
        { actor: 4, to: 5, action: 'UPDATE files', detail: 'thumbnail_url, status: completed', type: 'async' },
      ],
      notes: [
        { after: 8, text: 'Async processing in background', position: 'right' },
        { after: 11, text: 'Worker processes independently', position: 'left' }
      ]
    },
    project_task_creation: {
      title: 'Create Project Task with Notifications',
      description: 'Create task in project and notify team members',
      actors: ['Client', 'API Gateway', 'Project Service', 'User Service', 'Notification Service', 'Database'],
      steps: [
        { actor: 0, to: 1, action: 'POST /api/v1/projects/:id/tasks', detail: '{ title, assignee_id, due_date }' },
        { actor: 1, to: 2, action: 'CreateTaskCommand', detail: 'Task details' },
        { actor: 2, to: 3, action: 'Validate Project Access', detail: 'Check user permission' },
        { actor: 3, to: 5, action: 'Get User Role', detail: 'SELECT role FROM project_members' },
        { actor: 5, to: 3, action: 'Role: owner ✓', detail: '', type: 'return' },
        { actor: 3, to: 2, action: 'Permission granted ✓', detail: '', type: 'return' },
        { actor: 2, to: 3, action: 'Validate Assignee', detail: 'Check assignee exists in project' },
        { actor: 3, to: 5, action: 'Check assignee membership', detail: 'SELECT * FROM project_members' },
        { actor: 5, to: 3, action: 'Member found ✓', detail: '', type: 'return' },
        { actor: 3, to: 2, action: 'Assignee valid ✓', detail: '', type: 'return' },
        { actor: 2, to: 2, action: 'Create Task Entity', detail: 'Task.create()', type: 'internal' },
        { actor: 2, to: 5, action: 'INSERT INTO tasks', detail: 'Save task' },
        { actor: 5, to: 2, action: 'Task created ✓', detail: 'task_id', type: 'return' },
        { actor: 2, to: 4, action: 'Send Notification', detail: 'TaskAssignedNotification' },
        { actor: 4, to: 5, action: 'Get user preferences', detail: 'Check notification settings' },
        { actor: 4, to: 4, action: 'Send Email', detail: 'SMTP send', type: 'internal' },
        { actor: 4, to: 5, action: 'Log notification', detail: 'INSERT INTO notifications' },
        { actor: 2, to: 1, action: 'Return Success', detail: '{ task_id, status: created }', type: 'return' },
        { actor: 1, to: 0, action: '201 Created', detail: '{ id, title, assignee, due_date }', type: 'return' },
      ],
      notes: [
        { after: 5, text: 'Authorization check', position: 'right' },
        { after: 13, text: 'Notification sent async', position: 'right' }
      ]
    },
    authentication: {
      title: 'User Authentication (JWT)',
      description: 'Login with email/password and receive JWT token',
      actors: ['Client', 'API Gateway', 'Auth Service', 'User Service', 'Database', 'Redis Cache'],
      steps: [
        { actor: 0, to: 1, action: 'POST /api/v1/auth/login', detail: '{ email, password }' },
        { actor: 1, to: 2, action: 'LoginCommand', detail: 'Credentials' },
        { actor: 2, to: 3, action: 'Get User by Email', detail: 'Find user' },
        { actor: 3, to: 4, action: 'SELECT * FROM users', detail: 'WHERE email = ? AND deleted_at IS NULL' },
        { actor: 4, to: 3, action: 'User found ✓', detail: 'User data', type: 'return' },
        { actor: 3, to: 2, action: 'Return User', detail: '{ id, email, password_hash, ... }', type: 'return' },
        { actor: 2, to: 2, action: 'Verify Password', detail: 'bcrypt.compare()', type: 'internal' },
        { actor: 2, to: 2, action: 'Generate JWT', detail: 'jwt.sign({ user_id, exp: 7d })', type: 'internal' },
        { actor: 2, to: 2, action: 'Generate Refresh Token', detail: 'UUID', type: 'internal' },
        { actor: 2, to: 5, action: 'Store Session', detail: 'SET session:{token} = user_id' },
        { actor: 5, to: 2, action: 'Session stored ✓', detail: 'TTL: 7 days', type: 'return' },
        { actor: 2, to: 4, action: 'Update last_login_at', detail: 'UPDATE users SET last_login_at' },
        { actor: 2, to: 1, action: 'Return Tokens', detail: '{ access_token, refresh_token }', type: 'return' },
        { actor: 1, to: 0, action: '200 OK', detail: '{ access_token, refresh_token, expires_in }', type: 'return' },
        { actor: 0, to: 0, action: 'Store tokens', detail: 'localStorage / secure cookie', type: 'internal' },
      ],
      notes: [
        { after: 6, text: 'Password verification', position: 'right' },
        { after: 9, text: 'Session cached in Redis', position: 'left' }
      ]
    },
    saga_pattern: {
      title: 'Distributed Transaction (Saga)',
      description: 'Purchase course with payment and enrollment',
      actors: ['Client', 'API Gateway', 'Order Orchestrator', 'Payment Service', 'Enrollment Service', 'Notification'],
      steps: [
        { actor: 0, to: 1, action: 'POST /api/v1/orders/purchase', detail: '{ course_id, payment_method }' },
        { actor: 1, to: 2, action: 'PurchaseCourseCommand', detail: 'Start saga' },
        { actor: 2, to: 2, action: 'Create Order', detail: 'status: pending', type: 'internal' },
        { actor: 2, to: 3, action: 'Step 1: Process Payment', detail: '{ amount, method }' },
        { actor: 3, to: 3, action: 'Charge customer', detail: 'External payment gateway', type: 'internal' },
        { actor: 3, to: 2, action: 'Payment Success ✓', detail: '{ transaction_id, status: paid }', type: 'return' },
        { actor: 2, to: 4, action: 'Step 2: Enroll User', detail: '{ user_id, course_id }' },
        { actor: 4, to: 4, action: 'Create enrollment', detail: 'INSERT INTO enrollments', type: 'internal' },
        { actor: 4, to: 2, action: 'Enrollment Success ✓', detail: '{ enrollment_id }', type: 'return' },
        { actor: 2, to: 5, action: 'Step 3: Send Confirmation', detail: 'Welcome email' },
        { actor: 5, to: 2, action: 'Email Sent ✓', detail: '', type: 'return' },
        { actor: 2, to: 2, action: 'Update Order', detail: 'status: completed', type: 'internal' },
        { actor: 2, to: 1, action: 'Saga Complete ✓', detail: '{ order_id, status }', type: 'return' },
        { actor: 1, to: 0, action: '201 Created', detail: '{ order_id, enrollment_id }', type: 'return' },
      ],
      notes: [
        { after: 3, text: '🔷 Saga Step 1', position: 'left' },
        { after: 6, text: '🔷 Saga Step 2', position: 'left' },
        { after: 9, text: '🔷 Saga Step 3', position: 'left' }
      ],
      compensation: [
        { step: 6, action: 'If Enrollment Fails → Refund Payment', detail: 'Compensate Step 1' },
        { step: 9, action: 'If Email Fails → Log error (non-critical)', detail: 'Rollback not needed' }
      ]
    },
    cqrs_pattern: {
      title: 'CQRS: Read & Write Separation',
      description: 'Separate paths for commands (write) and queries (read)',
      actors: ['Client', 'API Gateway', 'Command Handler', 'Write DB', 'Event Bus', 'Query Handler', 'Read DB'],
      steps: [
        { actor: 0, to: 1, action: 'POST /api/v1/posts (Write)', detail: '{ title, content }', type: 'write' },
        { actor: 1, to: 2, action: 'CreatePostCommand', detail: 'Handle write', type: 'write' },
        { actor: 2, to: 3, action: 'INSERT INTO posts', detail: 'Master DB (write)', type: 'write' },
        { actor: 3, to: 2, action: 'Post created ✓', detail: 'post_id', type: 'return' },
        { actor: 2, to: 4, action: 'Publish: PostCreatedEvent', detail: 'Event sourcing', type: 'write' },
        { actor: 4, to: 5, action: 'Handle PostCreatedEvent', detail: 'Update read model', type: 'async' },
        { actor: 5, to: 6, action: 'Update Materialized View', detail: 'Denormalized data', type: 'async' },
        { actor: 2, to: 1, action: 'Command Success', detail: '{ post_id }', type: 'return' },
        { actor: 1, to: 0, action: '201 Created', detail: '{ id }', type: 'return' },
        { actor: 0, to: 0, action: '--- Wait 100ms ---', detail: 'Eventual consistency', type: 'wait' },
        { actor: 0, to: 1, action: 'GET /api/v1/posts/:id (Read)', detail: 'Fetch post', type: 'read' },
        { actor: 1, to: 5, action: 'GetPostQuery', detail: 'Handle read', type: 'read' },
        { actor: 5, to: 6, action: 'SELECT FROM posts_view', detail: 'Read replica / cache', type: 'read' },
        { actor: 6, to: 5, action: 'Post data', detail: 'Optimized for reading', type: 'return' },
        { actor: 5, to: 1, action: 'Query Result', detail: '{ post with relations }', type: 'return' },
        { actor: 1, to: 0, action: '200 OK', detail: '{ id, title, content, ... }', type: 'return' },
      ],
      notes: [
        { after: 4, text: '✍️ Write Path: Command', position: 'left' },
        { after: 10, text: '📖 Read Path: Query', position: 'right' },
        { after: 6, text: 'Async sync to read model', position: 'right' }
      ]
    }
  };

  const currentUseCase = useCases[selectedUseCase];

  const getActorColor = (index, type) => {
    const colors = {
      write: ['bg-red-500', 'bg-red-600', 'bg-red-700', 'bg-red-800'],
      read: ['bg-blue-500', 'bg-blue-600', 'bg-blue-700', 'bg-blue-800'],
      default: ['bg-slate-600', 'bg-blue-600', 'bg-green-600', 'bg-purple-600', 'bg-orange-600', 'bg-teal-600', 'bg-pink-600']
    };
    
    if (type === 'write' && index <= 4) return colors.write[Math.min(index, 3)];
    if (type === 'read' && index >= 4) return colors.read[Math.min(index - 4, 3)];
    return colors.default[index % colors.default.length];
  };

  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-50 to-slate-100 p-8 overflow-auto">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-2 text-slate-800">
          Specific Use Case Flows
        </h1>
        <p className="text-center text-slate-600 mb-8">
          Sequence diagrams for common scenarios
        </p>

        {/* Use Case Tabs */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {Object.entries(useCases).map(([key, useCase]) => (
            <button
              key={key}
              onClick={() => setSelectedUseCase(key)}
              className={`px-6 py-3 rounded-lg font-medium transition-all whitespace-nowrap ${
                selectedUseCase === key
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                  : 'bg-white text-slate-700 border-2 border-slate-300 hover:border-blue-400'
              }`}
            >
              {useCase.title}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-300 rounded-lg p-6 mb-6">
          <h2 className="text-2xl font-bold text-blue-900 mb-2">
            {currentUseCase.title}
          </h2>
          <p className="text-slate-700">{currentUseCase.description}</p>
        </div>

        {/* Sequence Diagram */}
        <div className="bg-white rounded-lg border-2 border-slate-300 shadow-lg p-8 overflow-x-auto">
          <div className="min-w-[1000px]">
            {/* Actors */}
            <div className="flex justify-between mb-8 px-4">
              {currentUseCase.actors.map((actor, index) => (
                <div key={index} className="flex flex-col items-center w-32">
                  <div className={`${getActorColor(index, currentUseCase.steps.find(s => s.actor === index || s.to === index)?.type)} text-white px-4 py-3 rounded-lg font-semibold text-center text-sm shadow-md min-h-[60px] flex items-center justify-center`}>
                    {actor}
                  </div>
                  <div className="w-0.5 bg-slate-300 h-8"></div>
                </div>
              ))}
            </div>

            {/* Steps */}
            <div className="space-y-3 relative">
              {currentUseCase.steps.map((step, index) => {
                const note = currentUseCase.notes?.find(n => n.after === index);
                const isReturn = step.type === 'return';
                const isInternal = step.type === 'internal';
                const isAsync = step.type === 'async';
                const isWait = step.type === 'wait';
                const isWrite = step.type === 'write';
                const isRead = step.type === 'read';

                const actorWidth = 130; // Width between actors
                const leftPos = step.actor * actorWidth + 65;
                const rightPos = step.to * actorWidth + 65;

                return (
                  <div key={index} className="relative" style={{ height: '60px' }}>
                    {/* Lifelines */}
                    {currentUseCase.actors.map((_, i) => (
                      <div
                        key={i}
                        className="absolute w-0.5 bg-slate-200 top-0 bottom-0"
                        style={{ left: `${i * actorWidth + 65}px` }}
                      />
                    ))}

                    {isWait ? (
                      <div className="absolute left-1/2 transform -translate-x-1/2 top-1/2 -translate-y-1/2">
                        <div className="bg-yellow-100 border-2 border-yellow-400 px-4 py-2 rounded font-semibold text-yellow-900">
                          {step.action}
                        </div>
                      </div>
                    ) : (
                      <>
                        {/* Arrow */}
                        <svg
                          className="absolute top-4"
                          style={{
                            left: `${Math.min(leftPos, rightPos)}px`,
                            width: `${Math.abs(rightPos - leftPos)}px`,
                            height: '40px'
                          }}
                        >
                          <defs>
                            <marker
                              id={`arrow-${index}`}
                              markerWidth="10"
                              markerHeight="10"
                              refX="9"
                              refY="3"
                              orient="auto"
                              markerUnits="strokeWidth"
                            >
                              <path
                                d="M0,0 L0,6 L9,3 z"
                                fill={isReturn ? '#64748b' : isAsync ? '#8b5cf6' : isWrite ? '#ef4444' : isRead ? '#3b82f6' : '#0ea5e9'}
                              />
                            </marker>
                          </defs>
                          <line
                            x1={leftPos < rightPos ? 0 : Math.abs(rightPos - leftPos)}
                            y1="15"
                            x2={leftPos < rightPos ? Math.abs(rightPos - leftPos) : 0}
                            y2="15"
                            stroke={isReturn ? '#64748b' : isAsync ? '#8b5cf6' : isWrite ? '#ef4444' : isRead ? '#3b82f6' : '#0ea5e9'}
                            strokeWidth={isAsync ? '1' : '2'}
                            strokeDasharray={isReturn || isAsync ? '5,5' : '0'}
                            markerEnd={`url(#arrow-${index})`}
                          />
                        </svg>

                        {/* Action Label */}
                        <div
                          className="absolute top-0"
                          style={{
                            left: `${(leftPos + rightPos) / 2 - 100}px`,
                            width: '200px'
                          }}
                        >
                          <div className={`text-center text-sm font-semibold px-2 py-1 rounded ${
                            isInternal ? 'bg-purple-100 text-purple-900' :
                            isAsync ? 'bg-purple-100 text-purple-800' :
                            isReturn ? 'text-slate-600' :
                            isWrite ? 'bg-red-100 text-red-900' :
                            isRead ? 'bg-blue-100 text-blue-900' :
                            'bg-sky-100 text-sky-900'
                          }`}>
                            {step.action}
                          </div>
                          {step.detail && (
                            <div className="text-center text-xs text-slate-500 mt-1">
                              {step.detail}
                            </div>
                          )}
                        </div>
                      </>
                    )}

                    {/* Note */}
                    {note && (
                      <div
                        className={`absolute top-8 ${
                          note.position === 'right' ? 'right-0' : 'left-0'
                        }`}
                      >
                        <div className="bg-yellow-50 border-2 border-yellow-400 px-3 py-2 rounded text-sm font-semibold text-yellow-900 shadow-md">
                          💡 {note.text}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Compensation (Saga only) */}
            {currentUseCase.compensation && (
              <div className="mt-12 pt-8 border-t-4 border-dashed border-red-400">
                <h3 className="text-lg font-bold text-red-900 mb-4">🔄 Compensating Transactions</h3>
                <div className="space-y-3">
                  {currentUseCase.compensation.map((comp, index) => (
                    <div key={index} className="bg-red-50 border-2 border-red-300 rounded-lg p-4">
                      <div className="font-semibold text-red-900 mb-1">❌ {comp.action}</div>
                      <div className="text-sm text-slate-600">{comp.detail}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Legend */}
        <div className="mt-8 bg-slate-100 border-2 border-slate-300 rounded-lg p-6">
          <h3 className="font-bold text-lg text-slate-800 mb-4">Legend</h3>
          <div className="grid grid-cols-4 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <svg width="40" height="20">
                <line x1="0" y1="10" x2="40" y2="10" stroke="#0ea5e9" strokeWidth="2" markerEnd="url(#arrow)" />
              </svg>
              <span>Synchronous call</span>
            </div>
            <div className="flex items-center gap-2">
              <svg width="40" height="20">
                <line x1="0" y1="10" x2="40" y2="10" stroke="#64748b" strokeWidth="2" strokeDasharray="5,5" markerEnd="url(#arrow)" />
              </svg>
              <span>Return value</span>
            </div>
            <div className="flex items-center gap-2">
              <svg width="40" height="20">
                <line x1="0" y1="10" x2="40" y2="10" stroke="#8b5cf6" strokeWidth="1" strokeDasharray="5,5" markerEnd="url(#arrow)" />
              </svg>
              <span>Async/Event</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-purple-100 border border-purple-300 rounded"></div>
              <span>Internal operation</span>
            </div>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="mt-8 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400 rounded-lg p-6">
          <h2 className="text-xl font-bold text-green-900 mb-4">⚡ Performance Considerations</h2>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div className="bg-white p-4 rounded border-2 border-green-300">
              <div className="font-semibold text-green-900 mb-2">Response Time Goals</div>
              <div className="space-y-1 text-slate-700">
                <div>• User Registration: &lt;500ms</div>
                <div>• File Upload: &lt;2s (up to 10MB)</div>
                <div>• Task Creation: &lt;300ms</div>
                <div>• Authentication: &lt;200ms</div>
              </div>
            </div>
            <div className="bg-white p-4 rounded border-2 border-green-300">
              <div className="font-semibold text-green-900 mb-2">Database Queries</div>
              <div className="space-y-1 text-slate-700">
                <div>• Use indexes on foreign keys</div>
                <div>• Limit N+1 queries with joins</div>
                <div>• Cache frequent reads (Redis)</div>
                <div>• Use connection pooling</div>
              </div>
            </div>
            <div className="bg-white p-4 rounded border-2 border-green-300">
              <div className="font-semibold text-green-900 mb-2">Optimization Tips</div>
              <div className="space-y-1 text-slate-700">
                <div>• Async for non-critical tasks</div>
                <div>• Pagination for large lists</div>
                <div>• CDN for static assets</div>
                <div>• Rate limiting per endpoint</div>
              </div>
            </div>
          </div>
        </div>

        {/* Error Handling */}
        <div className="mt-8 bg-gradient-to-r from-red-50 to-rose-50 border-2 border-red-400 rounded-lg p-6">
          <h2 className="text-xl font-bold text-red-900 mb-4">🚨 Error Handling Strategy</h2>
          <div className="grid grid-cols-2 gap-6 text-sm">
            <div>
              <h3 className="font-semibold text-red-800 mb-3">Common Error Scenarios:</h3>
              <div className="space-y-2">
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold">Validation Errors (400)</div>
                  <div className="text-slate-600">Return detailed field errors to client</div>
                </div>
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold">Not Found (404)</div>
                  <div className="text-slate-600">Resource doesn't exist or deleted</div>
                </div>
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold">Permission Denied (403)</div>
                  <div className="text-slate-600">User lacks required permissions</div>
                </div>
              </div>
            </div>
            <div>
              <h3 className="font-semibold text-red-800 mb-3">Recovery Strategies:</h3>
              <div className="space-y-2">
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold">Retry with Backoff</div>
                  <div className="text-slate-600">For transient failures (network, DB)</div>
                </div>
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold">Circuit Breaker</div>
                  <div className="text-slate-600">Stop calling failing services</div>
                </div>
                <div className="bg-white p-3 rounded border border-red-300">
                  <div className="font-semibold">Dead Letter Queue</div>
                  <div className="text-slate-600">Store failed async jobs for retry</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UseCaseFlows;