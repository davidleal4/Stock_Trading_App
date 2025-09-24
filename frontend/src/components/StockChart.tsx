'use client'

import React from 'react'
import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'

// Dynamically import Plotly to avoid SSR issues and cast to a flexible component type
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false }) as unknown as React.ComponentType<any>

interface StockChartProps {
  symbol: string
}

interface OHLCData {
  x: string
  open: number
  high: number
  low: number
  close: number
}

export function StockChart({ symbol }: StockChartProps) {
  const [chartData, setChartData] = useState<OHLCData[] | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    generateSampleData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [symbol])

  const generateSampleData = () => {
    setLoading(true)

    const data: OHLCData[] = []
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
        open: parseFloat(open.toFixed(2)),
        high: parseFloat(high.toFixed(2)),
        low: parseFloat(low.toFixed(2)),
        close: parseFloat(close.toFixed(2)),
      })

      currentPrice = close
    }

    setChartData(data)
    setLoading(false)
  }

  if (loading || !chartData) {
    return (
      <div className="h-96 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600" />
      </div>
    )
  }

  const plotData: any[] = [
    {
      x: chartData.map((d) => d.x),
      open: chartData.map((d) => d.open),
      high: chartData.map((d) => d.high),
      low: chartData.map((d) => d.low),
      close: chartData.map((d) => d.close),
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
      <Plot data={plotData} layout={layout} config={config} style={{ width: '100%', height: '400px' }} />
    </div>
  )
}

