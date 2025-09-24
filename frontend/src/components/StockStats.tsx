'use client'

import { TrendingUp, TrendingDown, Activity, DollarSign } from 'lucide-react'

interface StockStatsProps {
  symbol: string
  data: any
  loading: boolean
}

export function StockStats({ symbol, data, loading }: StockStatsProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="card animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    )
  }

  if (!data) {
    return (
      <div className="card">
        <p className="text-gray-500">No data available for {symbol}</p>
      </div>
    )
  }

  const isPositive = data.change >= 0

  const stats = [
    {
      label: 'Current Price',
      value: `$${data.currentPrice?.toFixed(2) || '0.00'}`,
      icon: DollarSign,
      color: 'text-gray-600',
    },
    {
      label: 'Change',
      value: `${isPositive ? '+' : ''}${data.change?.toFixed(2) || '0.00'}`,
      icon: isPositive ? TrendingUp : TrendingDown,
      color: isPositive ? 'text-success-600' : 'text-danger-600',
    },
    {
      label: 'Change %',
      value: `${isPositive ? '+' : ''}${data.changePercent?.toFixed(2) || '0.00'}%`,
      icon: isPositive ? TrendingUp : TrendingDown,
      color: isPositive ? 'text-success-600' : 'text-danger-600',
    },
    {
      label: 'Volume',
      value: data.volume?.toLocaleString() || '0',
      icon: Activity,
      color: 'text-gray-600',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => {
        const Icon = stat.icon
        return (
          <div key={index} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">{stat.label}</p>
                <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
              </div>
              <Icon className={`h-8 w-8 ${stat.color}`} />
            </div>
          </div>
        )
      })}
    </div>
  )
}