'use client'

import { useState, useEffect } from 'react'
import { StockChart } from './StockChart'
import { StockStats } from './StockStats'
import { ModelComparison } from './ModelComparison'
import { TradingPanel } from './TradingPanel'

interface DashboardProps {
  symbol: string
}

export function Dashboard({ symbol }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'models' | 'trading'>('overview')
  const [stockData, setStockData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchStockData()
  }, [symbol])

  const fetchStockData = async () => {
    setLoading(true)
    try {
      // Placeholder for API call
      await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API delay
      setStockData({
        symbol,
        currentPrice: Math.random() * 200 + 100,
        change: (Math.random() - 0.5) * 10,
        changePercent: (Math.random() - 0.5) * 5,
        volume: Math.floor(Math.random() * 1000000) + 500000,
      })
    } catch (error) {
      console.error('Error fetching stock data:', error)
    } finally {
      setLoading(false)
    }
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'models', label: 'ML Models' },
    { id: 'trading', label: 'Trading' },
  ] as const

  return (
    <div className="flex-1 p-6">
      {/* Tab Navigation */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="space-y-6">
        {activeTab === 'overview' && (
          <>
            {/* Stock Stats */}
            <StockStats symbol={symbol} data={stockData} loading={loading} />
            
            {/* Chart */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Price Chart</h3>
              <StockChart symbol={symbol} />
            </div>
          </>
        )}

        {activeTab === 'models' && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">ML Model Comparison</h3>
            <ModelComparison symbol={symbol} />
          </div>
        )}

        {activeTab === 'trading' && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Trading Panel</h3>
            <TradingPanel symbol={symbol} currentPrice={stockData?.currentPrice} />
          </div>
        )}
      </div>
    </div>
  )
}