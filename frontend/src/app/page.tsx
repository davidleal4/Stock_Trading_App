'use client'

import { useState, useEffect } from 'react'
import { Dashboard } from '@/components/Dashboard'
import { Sidebar } from '@/components/Sidebar'
import { AIAgent } from '@/components/AIAgent'
import { Header } from '@/components/Header'

export default function Home() {
  const [selectedSymbol, setSelectedSymbol] = useState<string>('AAPL')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [agentOpen, setAgentOpen] = useState(false)

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar 
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        selectedSymbol={selectedSymbol}
        onSymbolSelect={setSelectedSymbol}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header 
          onMenuClick={() => setSidebarOpen(true)}
          onAgentClick={() => setAgentOpen(true)}
          selectedSymbol={selectedSymbol}
        />

        {/* Dashboard */}
        <main className="flex-1 overflow-auto">
          <Dashboard symbol={selectedSymbol} />
        </main>
      </div>

      {/* AI Agent */}
      <AIAgent 
        isOpen={agentOpen}
        onClose={() => setAgentOpen(false)}
      />
    </div>
  )
}