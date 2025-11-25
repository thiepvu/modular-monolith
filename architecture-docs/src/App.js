import React, { useState } from 'react';

// Import all diagram components (defined below)
import ApplicationArchitecture from './components/ApplicationArchitecture';
import DatabaseSchema from './components/DatabaseSchema';
import ModuleInteractionFlows from './components/ModuleInteractionFlows';
import DeploymentArchitecture from './components/DeploymentArchitecture';
import UseCaseFlows from './components/UseCaseFlows';
import ModuleDependencyFlows from './components/ModuleDependencyFlows';
import MigrationSeedPractices from './components/MigrationSeedPractices';

function App() {
  const [activeTab, setActiveTab] = useState('app-arch');

  const tabs = [
    { id: 'app-arch', label: 'Application Architecture', component: ApplicationArchitecture },
    { id: 'db-schema', label: 'Database Schema', component: DatabaseSchema },
    { id: 'module-interaction', label: 'Module Interactions', component: ModuleInteractionFlows },
    { id: 'deployment', label: 'Deployment', component: DeploymentArchitecture },
    { id: 'use-cases', label: 'Use Case Flows', component: UseCaseFlows },
    { id: 'dependencies', label: 'Module Dependencies', component: ModuleDependencyFlows },
    { id: 'migrations', label: 'Migrations & Seeds', component: MigrationSeedPractices },
  ];

  const ActiveComponent = tabs.find(tab => tab.id === activeTab)?.component;

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-slate-800 to-slate-900 text-white shadow-lg sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold mb-2">Complete Architecture Documentation</h1>
          <p className="text-slate-300 text-sm">Modular Monolith with Clean Architecture</p>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-slate-200 sticky top-[88px] z-40 shadow-sm">
        <div className="container mx-auto px-4">
          <div className="flex overflow-x-auto space-x-2 py-3">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-all ${
                  activeTab === tab.id
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {ActiveComponent && <ActiveComponent />}
      </main>

      {/* Footer */}
      <footer className="bg-slate-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-slate-300">
            Complete Architecture Documentation • FastAPI/NestJS • PostgreSQL • Clean Architecture
          </p>
          <p className="text-slate-400 text-sm mt-2">
            Built with React • All diagrams are interactive • Production-ready patterns
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;