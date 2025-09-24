'use client'

import { Menu, Bot, TrendingUp } from 'lucide-react'

interface HeaderProps {
  onMenuClick: () => void
  onAgentClick: () => void
  selectedSymbol: string
}

export function Header({ onMenuClick, onAgentClick, selectedSymbol }: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="flex items-center justify-between">
        {/* Left side */}
        <div className="flex items-center space-x-4">
          <button
            onClick={onMenuClick}
            className="p-2 hover:bg-gray-100 rounded-md lg:hidden"
          >
            <Menu className="h-5 w-5" />
          </button>
          
          <div className="flex items-center space-x-2">
            <TrendingUp className="h-6 w-6 text-primary-600" />
            <h1 className="text-xl font-bold text-gray-900">Stock Trading App</h1>
          </div>
        </div>

        {/* Center - Current Symbol */}
        <div className="hidden md:block">
          <div className="bg-primary-50 px-4 py-2 rounded-lg">
            <span className="text-sm text-primary-600 font-medium">Current Symbol:</span>
            <span className="ml-2 text-lg font-bold text-primary-900">{selectedSymbol}</span>
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center space-x-4">
          <button
            onClick={onAgentClick}
            className="flex items-center space-x-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md transition-colors"
          >
            <Bot className="h-4 w-4" />
            <span className="hidden sm:inline">AI Assistant</span>
          </button>
        </div>
      </div>
    </header>
  )
}