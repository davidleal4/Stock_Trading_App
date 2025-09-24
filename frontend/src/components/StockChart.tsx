'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false })

interface StockChartProps {
  symbol: string
}

export function StockChart({ symbol }: StockChartProps) {
  const [chartData, setChartData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    generateSampleData()
  }, [symbol])

  const generateSampleData = () => {
    setLoading(true)
    
    // Generate sample OHLC data
    const data = []
    const basePrice = Math.random() * 200 + 100
    let currentPrice = basePrice
    
    for (let i = 0; i < 30; i++) {
      const date = new Date()
      date.setDate(date.getDate() - (29 - i))
      
      const open = currentPrice
      const changePercent = (Math.random() - 0.5) * 0.1 // ±5% daily change
      const close = open * (1 + changePercent)
      const high = Math.max(open, close) * (1 + Math.random() * 0.02)
      const low = Math.min(open, close) * (1 - Math.random() * 0.02)
      
      data.push({
        x: date.toISOString().split('T')[0],
        open: open.toFixed(2),
        high: high.toFixed(2),
        low: low.toFixed(2),
        close: close.toFixed(2),
      })
      
      currentPrice = close
    }
    
    setChartData(data)
    setLoading(false)
  }

  if (loading) {
    return (
      <div className="h-96 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const plotData = [
    {
      x: chartData.map((d: any) => d.x),
      open: chartData.map((d: any) => parseFloat(d.open)),
      high: chartData.map((d: any) => parseFloat(d.high)),
      low: chartData.map((d: any) => parseFloat(d.low)),
      close: chartData.map((d: any) => parseFloat(d.close)),
      type: 'candlestick',
      name: symbol,
      increasing: { line: { color: '#10b981' } },
      decreasing: { line: { color: '#ef4444' } },
    },
  ]

  const layout = {
    title: `${symbol} Stock Price`,
    xaxis: {
      title: 'Date',
      rangeslider: { visible: false },
    },
    yaxis: {
      title: 'Price ($)',
    },
    paper_bgcolor: 'white',
    plot_bgcolor: 'white',
    font: {
      family: 'Inter, sans-serif',
    },
    margin: {
      l: 50,
      r: 50,
      t: 50,
      b: 50,
    },
  }

  const config = {
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
    responsive: true,
  }

  return (
    <div className="w-full">
      <Plot
        data={plotData}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '400px' }}
      />
    </div>
  )
}