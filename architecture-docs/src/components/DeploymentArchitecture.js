import React, { useState } from 'react';

const DeploymentArchitecture = () => {
  const [selectedEnv, setSelectedEnv] = useState('docker');

  const environments = {
    docker: {
      title: 'Docker Compose (Development)',
      description: 'Local development and testing environment',
      diagram: (
        <div className="space-y-6">
          {/* Docker Compose Architecture */}
          <div className="bg-white p-6 rounded-lg border-2 border-blue-400 shadow-lg">
            <h3 className="font-bold text-lg mb-4 text-blue-900">Docker Compose Stack</h3>
            
            <div className="grid grid-cols-2 gap-6">
              {/* Application Services */}
              <div className="space-y-3">
                <h4 className="font-semibold text-blue-800 bg-blue-100 p-2 rounded">Application Services</h4>
                
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-lg shadow">
                  <div className="font-bold mb-2">🚀 api-service</div>
                  <div className="text-sm space-y-1 text-blue-50">
                    <div>• Image: app:latest</div>
                    <div>• Port: 8000:8000</div>
                    <div>• Env: development</div>
                    <div>• Volumes: ./src:/app/src</div>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-lg shadow">
                  <div className="font-bold mb-2">🔄 worker-service</div>
                  <div className="text-sm space-y-1 text-green-50">
                    <div>• Image: app:latest</div>
                    <div>• Command: celery worker</div>
                    <div>• Queue: async tasks</div>
                    <div>• Workers: 4</div>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-4 rounded-lg shadow">
                  <div className="font-bold mb-2">⏰ scheduler-service</div>
                  <div className="text-sm space-y-1 text-purple-50">
                    <div>• Image: app:latest</div>
                    <div>• Command: celery beat</div>
                    <div>• Cron jobs</div>
                    <div>• Scheduled tasks</div>
                  </div>
                </div>
              </div>

              {/* Infrastructure Services */}
              <div className="space-y-3">
                <h4 className="font-semibold text-orange-800 bg-orange-100 p-2 rounded">Infrastructure Services</h4>
                
                <div className="bg-gradient-to-r from-slate-600 to-slate-700 text-white p-4 rounded-lg shadow">
                  <div className="font-bold mb-2">🐘 postgres</div>
                  <div className="text-sm space-y-1 text-slate-200">
                    <div>• Image: postgres:15</div>
                    <div>• Port: 5432:5432</div>
                    <div>• Volume: pgdata</div>
                    <div>• Health check enabled</div>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-red-500 to-red-600 text-white p-4 rounded-lg shadow">
                  <div className="font-bold mb-2">🔴 redis</div>
                  <div className="text-sm space-y-1 text-red-50">
                    <div>• Image: redis:7-alpine</div>
                    <div>• Port: 6379:6379</div>
                    <div>• Cache & Queue</div>
                    <div>• Persistence: AOF</div>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-orange-500 to-orange-600 text-white p-4 rounded-lg shadow">
                  <div className="font-bold mb-2">🗄️ minio (S3)</div>
                  <div className="text-sm space-y-1 text-orange-50">
                    <div>• Image: minio/minio</div>
                    <div>• Port: 9000:9000</div>
                    <div>• Console: 9001:9001</div>
                    <div>• Volume: minio-data</div>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-yellow-500 to-yellow-600 text-white p-4 rounded-lg shadow">
                  <div className="font-bold mb-2">📊 prometheus</div>
                  <div className="text-sm space-y-1 text-yellow-50">
                    <div>• Image: prom/prometheus</div>
                    <div>• Port: 9090:9090</div>
                    <div>• Metrics collection</div>
                    <div>• Scrape interval: 15s</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Docker Compose File Example */}
            <div className="mt-6 bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
              <div className="text-slate-400"># docker-compose.yml</div>
              <div>version: '3.8'</div>
              <div>services:</div>
              <div className="ml-4">api:</div>
              <div className="ml-8">build: .</div>
              <div className="ml-8">ports: ["8000:8000"]</div>
              <div className="ml-8">depends_on: [postgres, redis]</div>
              <div className="ml-8">environment:</div>
              <div className="ml-12">- DATABASE_URL=postgresql://...</div>
              <div className="ml-12">- REDIS_URL=redis://redis:6379</div>
            </div>
          </div>
        </div>
      )
    },
    kubernetes: {
      title: 'Kubernetes (Production)',
      description: 'Production-ready orchestration with auto-scaling',
      diagram: (
        <div className="space-y-6">
          {/* Kubernetes Architecture */}
          <div className="bg-white p-6 rounded-lg border-2 border-green-400 shadow-lg">
            <h3 className="font-bold text-lg mb-4 text-green-900">Kubernetes Cluster</h3>
            
            <div className="space-y-6">
              {/* Ingress Layer */}
              <div>
                <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-3 rounded-t-lg font-bold">
                  🌐 Ingress Layer
                </div>
                <div className="bg-blue-50 p-4 rounded-b-lg border-2 border-blue-200">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white p-3 rounded border border-blue-300">
                      <div className="font-semibold text-blue-900 mb-2">Ingress Controller (NGINX)</div>
                      <div className="text-sm text-slate-600">
                        • SSL/TLS termination<br/>
                        • Load balancing<br/>
                        • Rate limiting<br/>
                        • Path-based routing
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-blue-300">
                      <div className="font-semibold text-blue-900 mb-2">Routes</div>
                      <div className="text-sm text-slate-600">
                        • api.domain.com → API Service<br/>
                        • cdn.domain.com → Static Files<br/>
                        • admin.domain.com → Admin UI
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Application Layer */}
              <div>
                <div className="bg-gradient-to-r from-purple-600 to-purple-700 text-white p-3 rounded-t-lg font-bold">
                  🚀 Application Layer
                </div>
                <div className="bg-purple-50 p-4 rounded-b-lg border-2 border-purple-200">
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-white p-3 rounded border border-purple-300">
                      <div className="font-semibold text-purple-900 mb-2">API Deployment</div>
                      <div className="text-sm text-slate-600">
                        • Replicas: 3-10<br/>
                        • CPU: 500m-2000m<br/>
                        • Memory: 512Mi-2Gi<br/>
                        • HPA enabled
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-purple-300">
                      <div className="font-semibold text-purple-900 mb-2">Worker Deployment</div>
                      <div className="text-sm text-slate-600">
                        • Replicas: 2-5<br/>
                        • CPU: 1000m-3000m<br/>
                        • Memory: 1Gi-4Gi<br/>
                        • Queue-based scaling
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-purple-300">
                      <div className="font-semibold text-purple-900 mb-2">Scheduler Deployment</div>
                      <div className="text-sm text-slate-600">
                        • Replicas: 1<br/>
                        • CPU: 100m<br/>
                        • Memory: 128Mi<br/>
                        • Singleton pattern
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Data Layer */}
              <div>
                <div className="bg-gradient-to-r from-orange-600 to-orange-700 text-white p-3 rounded-t-lg font-bold">
                  💾 Data Layer
                </div>
                <div className="bg-orange-50 p-4 rounded-b-lg border-2 border-orange-200">
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-white p-3 rounded border border-orange-300">
                      <div className="font-semibold text-orange-900 mb-2">PostgreSQL StatefulSet</div>
                      <div className="text-sm text-slate-600">
                        • Primary-Replica setup<br/>
                        • PersistentVolumeClaim<br/>
                        • Automated backups<br/>
                        • Connection pooling
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-orange-300">
                      <div className="font-semibold text-orange-900 mb-2">Redis Cluster</div>
                      <div className="text-sm text-slate-600">
                        • Master-Slave<br/>
                        • Sentinel for HA<br/>
                        • Cache + Queue<br/>
                        • AOF + RDB persistence
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-orange-300">
                      <div className="font-semibold text-orange-900 mb-2">Object Storage</div>
                      <div className="text-sm text-slate-600">
                        • S3 / MinIO<br/>
                        • Bucket policies<br/>
                        • CDN integration<br/>
                        • Lifecycle rules
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Observability */}
              <div>
                <div className="bg-gradient-to-r from-yellow-600 to-yellow-700 text-white p-3 rounded-t-lg font-bold">
                  📊 Observability Stack
                </div>
                <div className="bg-yellow-50 p-4 rounded-b-lg border-2 border-yellow-200">
                  <div className="grid grid-cols-4 gap-3">
                    <div className="bg-white p-3 rounded border border-yellow-300 text-center">
                      <div className="font-semibold text-yellow-900 mb-1">Prometheus</div>
                      <div className="text-xs text-slate-600">Metrics</div>
                    </div>
                    <div className="bg-white p-3 rounded border border-yellow-300 text-center">
                      <div className="font-semibold text-yellow-900 mb-1">Grafana</div>
                      <div className="text-xs text-slate-600">Dashboards</div>
                    </div>
                    <div className="bg-white p-3 rounded border border-yellow-300 text-center">
                      <div className="font-semibold text-yellow-900 mb-1">Loki</div>
                      <div className="text-xs text-slate-600">Logs</div>
                    </div>
                    <div className="bg-white p-3 rounded border border-yellow-300 text-center">
                      <div className="font-semibold text-yellow-900 mb-1">Jaeger</div>
                      <div className="text-xs text-slate-600">Tracing</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* K8s Manifest Example */}
            <div className="mt-6 bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
              <div className="text-slate-400"># api-deployment.yaml</div>
              <div>apiVersion: apps/v1</div>
              <div>kind: Deployment</div>
              <div>metadata:</div>
              <div className="ml-4">name: api-service</div>
              <div>spec:</div>
              <div className="ml-4">replicas: 3</div>
              <div className="ml-4">selector:</div>
              <div className="ml-8">matchLabels: {"{"} app: api {"}"}</div>
              <div className="ml-4">template:</div>
              <div className="ml-8">spec:</div>
              <div className="ml-12">containers:</div>
              <div className="ml-16">- name: api</div>
              <div className="ml-20">image: registry/app:v1.0.0</div>
              <div className="ml-20">resources:</div>
              <div className="ml-24">requests: {"{"} cpu: 500m, memory: 512Mi {"}"}</div>
              <div className="ml-24">limits: {"{"} cpu: 2000m, memory: 2Gi {"}"}</div>
            </div>
          </div>
        </div>
      )
    },
    cicd: {
      title: 'CI/CD Pipeline',
      description: 'Automated build, test, and deployment pipeline',
      diagram: (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border-2 border-indigo-400 shadow-lg">
            <h3 className="font-bold text-lg mb-4 text-indigo-900">GitOps CI/CD Flow</h3>
            
            <div className="space-y-4">
              {/* Stage 1: Source */}
              <div className="flex items-center gap-4">
                <div className="w-32 bg-slate-700 text-white p-3 rounded text-center font-semibold">
                  1. Source
                </div>
                <div className="flex-1 bg-slate-100 p-4 rounded border-2 border-slate-300">
                  <div className="font-semibold text-slate-900 mb-2">Git Repository (GitHub/GitLab)</div>
                  <div className="text-sm text-slate-600">
                    • Developer pushes code → main/develop branch<br/>
                    • Webhook triggers pipeline<br/>
                    • Branch protection rules enforced
                  </div>
                </div>
              </div>

              {/* Stage 2: Build */}
              <div className="flex items-center gap-4">
                <div className="w-32 bg-blue-600 text-white p-3 rounded text-center font-semibold">
                  2. Build
                </div>
                <div className="flex-1 bg-blue-50 p-4 rounded border-2 border-blue-300">
                  <div className="font-semibold text-blue-900 mb-2">GitHub Actions / Jenkins</div>
                  <div className="text-sm text-slate-600">
                    • Install dependencies (pip/npm install)<br/>
                    • Compile/transpile code<br/>
                    • Build Docker image: app:$SHA<br/>
                    • Push to container registry
                  </div>
                </div>
              </div>

              {/* Stage 3: Test */}
              <div className="flex items-center gap-4">
                <div className="w-32 bg-green-600 text-white p-3 rounded text-center font-semibold">
                  3. Test
                </div>
                <div className="flex-1 bg-green-50 p-4 rounded border-2 border-green-300">
                  <div className="font-semibold text-green-900 mb-2">Automated Testing Suite</div>
                  <div className="grid grid-cols-2 gap-3 text-sm text-slate-600">
                    <div>
                      • Unit tests (pytest/jest)<br/>
                      • Integration tests<br/>
                      • Code coverage (&gt;80%)
                    </div>
                    <div>
                      • Linting (flake8/eslint)<br/>
                      • Security scan (Snyk)<br/>
                      • E2E tests (optional)
                    </div>
                  </div>
                </div>
              </div>

              {/* Stage 4: Security */}
              <div className="flex items-center gap-4">
                <div className="w-32 bg-red-600 text-white p-3 rounded text-center font-semibold">
                  4. Security
                </div>
                <div className="flex-1 bg-red-50 p-4 rounded border-2 border-red-300">
                  <div className="font-semibold text-red-900 mb-2">Security Scanning</div>
                  <div className="text-sm text-slate-600">
                    • Container image scan (Trivy)<br/>
                    • Dependency vulnerability check<br/>
                    • SAST (Static Application Security Testing)<br/>
                    • License compliance check
                  </div>
                </div>
              </div>

              {/* Stage 5: Deploy */}
              <div className="flex items-center gap-4">
                <div className="w-32 bg-purple-600 text-white p-3 rounded text-center font-semibold">
                  5. Deploy
                </div>
                <div className="flex-1 bg-purple-50 p-4 rounded border-2 border-purple-300">
                  <div className="font-semibold text-purple-900 mb-2">ArgoCD / Flux (GitOps)</div>
                  <div className="grid grid-cols-3 gap-3 text-sm text-slate-600">
                    <div>
                      <strong>Dev:</strong><br/>
                      • Auto-deploy on merge<br/>
                      • Testing environment
                    </div>
                    <div>
                      <strong>Staging:</strong><br/>
                      • Manual approval<br/>
                      • Pre-prod validation
                    </div>
                    <div>
                      <strong>Production:</strong><br/>
                      • Blue-Green deploy<br/>
                      • Canary release (10%)
                    </div>
                  </div>
                </div>
              </div>

              {/* Stage 6: Monitor */}
              <div className="flex items-center gap-4">
                <div className="w-32 bg-yellow-600 text-white p-3 rounded text-center font-semibold">
                  6. Monitor
                </div>
                <div className="flex-1 bg-yellow-50 p-4 rounded border-2 border-yellow-300">
                  <div className="font-semibold text-yellow-900 mb-2">Observability & Alerts</div>
                  <div className="text-sm text-slate-600">
                    • Prometheus metrics scraping<br/>
                    • Grafana dashboards for visualization<br/>
                    • PagerDuty/Slack alerts on failures<br/>
                    • Automatic rollback on error rate spike
                  </div>
                </div>
              </div>
            </div>

            {/* GitHub Actions Example */}
            <div className="mt-6 bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
              <div className="text-slate-400"># .github/workflows/deploy.yml</div>
              <div>name: CI/CD Pipeline</div>
              <div>on: [push, pull_request]</div>
              <div>jobs:</div>
              <div className="ml-4">build:</div>
              <div className="ml-8">runs-on: ubuntu-latest</div>
              <div className="ml-8">steps:</div>
              <div className="ml-12">- uses: actions/checkout@v3</div>
              <div className="ml-12">- name: Build Docker image</div>
              <div className="ml-16">run: docker build -t app:$SHA .</div>
              <div className="ml-12">- name: Run tests</div>
              <div className="ml-16">run: pytest --cov=. tests/</div>
              <div className="ml-12">- name: Push to registry</div>
              <div className="ml-16">run: docker push registry/app:$SHA</div>
            </div>
          </div>
        </div>
      )
    },
    infrastructure: {
      title: 'Infrastructure as Code',
      description: 'Terraform/Pulumi for cloud infrastructure',
      diagram: (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg border-2 border-teal-400 shadow-lg">
            <h3 className="font-bold text-lg mb-4 text-teal-900">Cloud Infrastructure (AWS/GCP/Azure)</h3>
            
            <div className="space-y-6">
              {/* Network Layer */}
              <div>
                <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-3 rounded-t-lg font-bold">
                  🌐 Network Layer
                </div>
                <div className="bg-blue-50 p-4 rounded-b-lg border-2 border-blue-200">
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div className="bg-white p-3 rounded border border-blue-300">
                      <div className="font-semibold text-blue-900 mb-2">VPC</div>
                      <div className="text-slate-600">
                        • CIDR: 10.0.0.0/16<br/>
                        • Multi-AZ setup<br/>
                        • Public/Private subnets
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-blue-300">
                      <div className="font-semibold text-blue-900 mb-2">Load Balancer</div>
                      <div className="text-slate-600">
                        • ALB/NLB<br/>
                        • SSL termination<br/>
                        • Health checks
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-blue-300">
                      <div className="font-semibold text-blue-900 mb-2">CloudFront CDN</div>
                      <div className="text-slate-600">
                        • Global edge locations<br/>
                        • Static asset caching<br/>
                        • DDoS protection
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Compute Layer */}
              <div>
                <div className="bg-gradient-to-r from-purple-600 to-purple-700 text-white p-3 rounded-t-lg font-bold">
                  ⚙️ Compute Layer
                </div>
                <div className="bg-purple-50 p-4 rounded-b-lg border-2 border-purple-200">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="bg-white p-3 rounded border border-purple-300">
                      <div className="font-semibold text-purple-900 mb-2">EKS / GKE / AKS</div>
                      <div className="text-slate-600">
                        • Managed Kubernetes<br/>
                        • Node groups: 2-20 nodes<br/>
                        • Auto-scaling enabled<br/>
                        • Instance: t3.medium+
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-purple-300">
                      <div className="font-semibold text-purple-900 mb-2">Container Registry</div>
                      <div className="text-slate-600">
                        • ECR / GCR / ACR<br/>
                        • Image scanning<br/>
                        • Lifecycle policies<br/>
                        • RBAC enabled
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Database Layer */}
              <div>
                <div className="bg-gradient-to-r from-orange-600 to-orange-700 text-white p-3 rounded-t-lg font-bold">
                  💾 Database Layer
                </div>
                <div className="bg-orange-50 p-4 rounded-b-lg border-2 border-orange-200">
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div className="bg-white p-3 rounded border border-orange-300">
                      <div className="font-semibold text-orange-900 mb-2">RDS PostgreSQL</div>
                      <div className="text-slate-600">
                        • Multi-AZ deployment<br/>
                        • Automated backups<br/>
                        • Read replicas<br/>
                        • Point-in-time recovery
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-orange-300">
                      <div className="font-semibold text-orange-900 mb-2">ElastiCache Redis</div>
                      <div className="text-slate-600">
                        • Cluster mode<br/>
                        • Auto-failover<br/>
                        • Encryption at rest<br/>
                        • Snapshot backups
                      </div>
                    </div>
                    <div className="bg-white p-3 rounded border border-orange-300">
                      <div className="font-semibold text-orange-900 mb-2">S3 Storage</div>
                      <div className="text-slate-600">
                        • Versioning enabled<br/>
                        • Lifecycle policies<br/>
                        • Cross-region replication<br/>
                        • Bucket encryption
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Security Layer */}
              <div>
                <div className="bg-gradient-to-r from-red-600 to-red-700 text-white p-3 rounded-t-lg font-bold">
                  🔒 Security Layer
                </div>
                <div className="bg-red-50 p-4 rounded-b-lg border-2 border-red-200">
                  <div className="grid grid-cols-4 gap-3 text-sm">
                    <div className="bg-white p-3 rounded border border-red-300 text-center">
                      <div className="font-semibold text-red-900 mb-1">IAM Roles</div>
                      <div className="text-xs text-slate-600">Least privilege</div>
                    </div>
                    <div className="bg-white p-3 rounded border border-red-300 text-center">
                      <div className="font-semibold text-red-900 mb-1">Secrets Manager</div>
                      <div className="text-xs text-slate-600">API keys, passwords</div>
                    </div>
                    <div className="bg-white p-3 rounded border border-red-300 text-center">
                      <div className="font-semibold text-red-900 mb-1">WAF</div>
                      <div className="text-xs text-slate-600">Web firewall</div>
                    </div>
                    <div className="bg-white p-3 rounded border border-red-300 text-center">
                      <div className="font-semibold text-red-900 mb-1">Security Groups</div>
                      <div className="text-xs text-slate-600">Network ACLs</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Terraform Example */}
            <div className="mt-6 bg-slate-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
              <div className="text-slate-400"># infrastructure/main.tf</div>
              <div>resource "aws_eks_cluster" "main" {"{"}</div>
              <div className="ml-4">name = "production-cluster"</div>
              <div className="ml-4">role_arn = aws_iam_role.cluster.arn</div>
              <div className="ml-4">version = "1.28"</div>
              <div className="ml-4">vpc_config {"{"}</div>
              <div className="ml-8">subnet_ids = aws_subnet.private[*].id</div>
              <div className="ml-8">security_group_ids = [aws_security_group.cluster.id]</div>
              <div className="ml-4">{"}"}</div>
              <div>{"}"}</div>
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
          Deployment Architecture
        </h1>
        <p className="text-center text-slate-600 mb-8">
          From Development to Production
        </p>

        {/* Environment Tabs */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {Object.entries(environments).map(([key, env]) => (
            <button
              key={key}
              onClick={() => setSelectedEnv(key)}
              className={`px-6 py-3 rounded-lg font-medium transition-all whitespace-nowrap ${
                selectedEnv === key
                  ? 'bg-gradient-to-r from-teal-600 to-cyan-600 text-white shadow-lg'
                  : 'bg-white text-slate-700 border-2 border-slate-300 hover:border-teal-400'
              }`}
            >
              {env.title}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="bg-gradient-to-br from-teal-50 to-cyan-50 border-2 border-teal-300 rounded-lg p-6 mb-6">
          <h2 className="text-2xl font-bold text-teal-900 mb-2">
            {environments[selectedEnv].title}
          </h2>
          <p className="text-slate-700">{environments[selectedEnv].description}</p>
        </div>

        {environments[selectedEnv].diagram}

        {/* Environment Comparison */}
        <div className="mt-8 bg-white border-2 border-slate-300 rounded-lg p-6 shadow-lg">
          <h2 className="text-xl font-bold text-slate-800 mb-4">🏗️ Environment Comparison</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-100">
                <tr>
                  <th className="px-4 py-2 text-left font-semibold">Aspect</th>
                  <th className="px-4 py-2 text-left font-semibold">Development</th>
                  <th className="px-4 py-2 text-left font-semibold">Staging</th>
                  <th className="px-4 py-2 text-left font-semibold">Production</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-slate-200">
                  <td className="px-4 py-3 font-semibold">Infrastructure</td>
                  <td className="px-4 py-3">Docker Compose</td>
                  <td className="px-4 py-3">Kubernetes (Small)</td>
                  <td className="px-4 py-3">Kubernetes (HA)</td>
                </tr>
                <tr className="border-t border-slate-200 bg-slate-50">
                  <td className="px-4 py-3 font-semibold">Replicas</td>
                  <td className="px-4 py-3">1 per service</td>
                  <td className="px-4 py-3">2 per service</td>
                  <td className="px-4 py-3">3-10 (auto-scale)</td>
                </tr>
                <tr className="border-t border-slate-200">
                  <td className="px-4 py-3 font-semibold">Database</td>
                  <td className="px-4 py-3">Local PostgreSQL</td>
                  <td className="px-4 py-3">RDS (Single-AZ)</td>
                  <td className="px-4 py-3">RDS (Multi-AZ + Replicas)</td>
                </tr>
                <tr className="border-t border-slate-200 bg-slate-50">
                  <td className="px-4 py-3 font-semibold">Deployment</td>
                  <td className="px-4 py-3">Manual / Hot reload</td>
                  <td className="px-4 py-3">CI/CD Auto</td>
                  <td className="px-4 py-3">Blue-Green / Canary</td>
                </tr>
                <tr className="border-t border-slate-200">
                  <td className="px-4 py-3 font-semibold">Monitoring</td>
                  <td className="px-4 py-3">Logs only</td>
                  <td className="px-4 py-3">Basic metrics</td>
                  <td className="px-4 py-3">Full observability stack</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Cost Estimation */}
        <div className="mt-8 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400 rounded-lg p-6">
          <h2 className="text-xl font-bold text-green-900 mb-4">💰 Monthly Cost Estimation (AWS)</h2>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div className="bg-white p-4 rounded border-2 border-green-300">
              <div className="font-bold text-lg text-green-900 mb-2">Development</div>
              <div className="text-slate-600 space-y-1">
                <div>• EC2 (t3.small): $15</div>
                <div>• RDS (db.t3.micro): $15</div>
                <div>• S3: $5</div>
                <div className="border-t pt-2 font-bold">Total: ~$35/mo</div>
              </div>
            </div>
            <div className="bg-white p-4 rounded border-2 border-green-300">
              <div className="font-bold text-lg text-green-900 mb-2">Staging</div>
              <div className="text-slate-600 space-y-1">
                <div>• EKS: $75</div>
                <div>• EC2 (2x t3.medium): $60</div>
                <div>• RDS (db.t3.small): $30</div>
                <div>• ElastiCache: $20</div>
                <div className="border-t pt-2 font-bold">Total: ~$185/mo</div>
              </div>
            </div>
            <div className="bg-white p-4 rounded border-2 border-green-300">
              <div className="font-bold text-lg text-green-900 mb-2">Production</div>
              <div className="text-slate-600 space-y-1">
                <div>• EKS: $75</div>
                <div>• EC2 (6x t3.large): $400</div>
                <div>• RDS (db.r5.xlarge): $350</div>
                <div>• ElastiCache: $100</div>
                <div>• ALB + CloudFront: $50</div>
                <div className="border-t pt-2 font-bold">Total: ~$975/mo</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeploymentArchitecture;