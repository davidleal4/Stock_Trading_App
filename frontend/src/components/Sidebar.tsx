'use client'

import { X, TrendingUp, BarChart3, Settings, User } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
  selectedSymbol: string
  onSymbolSelect: (symbol: string) => void
}

const DEFAULT_SYMBOLS = ['AAPL', 'MSFT', 'NVDA', 'GOOG', 'AMZN', 'META', 'TSLA', 'BRK.B', 'JPM', 'V']

export function Sidebar({ isOpen, onClose, selectedSymbol, onSymbolSelect }: SidebarProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
            onClick={onClose}
          />

          {/* Sidebar */}
          <motion.div
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            className="fixed left-0 top-0 h-full w-64 bg-white shadow-lg z-50 lg:relative lg:translate-x-0"
          >
            <div className="flex flex-col h-full">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Navigation</h2>
                <button
                  onClick={onClose}
                  className="p-1 hover:bg-gray-100 rounded-md lg:hidden"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              {/* Stock Symbols */}
              <div className="flex-1 overflow-y-auto p-4">
                <div className="mb-6">
                  <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">
                    Stock Symbols
                  </h3>
                  <div className="space-y-1">
                    {DEFAULT_SYMBOLS.map((symbol) => (
                      <button
                        key={symbol}
                        onClick={() => {
                          onSymbolSelect(symbol)
                          onClose()
                        }}
                        className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                          selectedSymbol === symbol
                            ? 'bg-primary-100 text-primary-700'
                            : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                        }`}
                      >
                        {symbol}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Navigation Items */}
                <div className="mb-6">
                  <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">
                    Features
                  </h3>
                  <nav className="space-y-1">
                    <a
                      href="#"
                      className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-100 hover:text-gray-900"
                    >
                      <TrendingUp className="mr-3 h-4 w-4" />
                      Real-time Data
                    </a>
                    <a
                      href="#"
                      className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-100 hover:text-gray-900"
                    >
                      <BarChart3 className="mr-3 h-4 w-4" />
                      ML Models
                    </a>
                    <a
                      href="#"
                      className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-100 hover:text-gray-900"
                    >
                      <User className="mr-3 h-4 w-4" />
                      Portfolio
                    </a>
                    <a
                      href="#"
                      className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-100 hover:text-gray-900"
                    >
                      <Settings className="mr-3 h-4 w-4" />
                      Settings
                    </a>
                  </nav>
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}