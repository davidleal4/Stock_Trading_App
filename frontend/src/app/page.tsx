"use client"

import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { TrendingUp, TrendingDown, DollarSign, BarChart3, Users, Activity } from "lucide-react"
import { motion } from "framer-motion"
import { useEffect, useState } from "react"
import axios from "axios"

interface TrendingStock {
  symbol: string
  price: number
  change: number
}

interface PortfolioData {
  cash: number
  stocks: Record<string, { quantity: number; avgPrice: number }>
}

export default function Dashboard() {
  const [trendingStocks, setTrendingStocks] = useState<TrendingStock[]>([])
  const [portfolio, setPortfolio] = useState<PortfolioData>({ cash: 10000, stocks: {} })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch trending stocks
        const trendingResponse = await axios.get('http://localhost:5000/api/trending')
        setTrendingStocks(trendingResponse.data.slice(0, 4))

        // Fetch portfolio
        const portfolioResponse = await axios.get('http://localhost:5000/api/portfolio')
        setPortfolio(portfolioResponse.data)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const portfolioValue = Object.entries(portfolio.stocks).reduce((total, [symbol, data]) => {
    return total + (data.quantity * data.avgPrice)
  }, portfolio.cash)

  const stats = [
    {
      title: "Portfolio Value",
      value: `$${portfolioValue.toLocaleString()}`,
      change: "+12.5%",
      icon: DollarSign,
      positive: true
    },
    {
      title: "Total Profit/Loss",
      value: `$${(portfolioValue - 10000).toLocaleString()}`,
      change: "+8.2%", 
      icon: TrendingUp,
      positive: portfolioValue > 10000
    },
    {
      title: "Active Positions",
      value: Object.keys(portfolio.stocks).length.toString(),
      change: "+2",
      icon: BarChart3,
      positive: true
    },
    {
      title: "Win Rate",
      value: "78%",
      change: "+5.1%",
      icon: Activity,
      positive: true
    }
  ]

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between"
        >
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
            <p className="text-muted-foreground">
              Welcome back! Here's your trading overview.
            </p>
          </div>
          <Button className="bg-blue-600 hover:bg-blue-700">
            Start Trading
          </Button>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {stat.title}
                  </CardTitle>
                  <stat.icon className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <p className={`text-xs flex items-center ${
                    stat.positive ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {stat.positive ? (
                      <TrendingUp className="h-3 w-3 mr-1" />
                    ) : (
                      <TrendingDown className="h-3 w-3 mr-1" />
                    )}
                    {stat.change} from last month
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Trending Stocks */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="lg:col-span-2"
          >
            <Card>
              <CardHeader>
                <CardTitle>Trending Stocks</CardTitle>
                <CardDescription>
                  Top performing stocks today
                </CardDescription>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="space-y-4">
                    {[...Array(4)].map((_, i) => (
                      <div key={i} className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div className="w-10 h-10 bg-muted rounded animate-pulse" />
                          <div className="space-y-2">
                            <div className="w-16 h-4 bg-muted rounded animate-pulse" />
                            <div className="w-12 h-3 bg-muted rounded animate-pulse" />
                          </div>
                        </div>
                        <div className="text-right space-y-2">
                          <div className="w-20 h-4 bg-muted rounded animate-pulse" />
                          <div className="w-16 h-3 bg-muted rounded animate-pulse" />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="space-y-4">
                    {trendingStocks.map((stock, index) => (
                      <motion.div
                        key={stock.symbol}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex items-center justify-between hover:bg-muted/50 p-2 rounded-lg transition-colors"
                      >
                        <div className="flex items-center space-x-4">
                          <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                            <span className="font-semibold text-blue-600 dark:text-blue-400">
                              {stock.symbol.slice(0, 2)}
                            </span>
                          </div>
                          <div>
                            <p className="font-medium">{stock.symbol}</p>
                            <p className="text-sm text-muted-foreground">Stock</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-medium">${stock.price.toFixed(2)}</p>
                          <p className={`text-sm flex items-center justify-end ${
                            stock.change >= 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {stock.change >= 0 ? (
                              <TrendingUp className="h-3 w-3 mr-1" />
                            ) : (
                              <TrendingDown className="h-3 w-3 mr-1" />
                            )}
                            {stock.change.toFixed(2)}%
                          </p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
                <CardDescription>
                  Manage your portfolio
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button className="w-full border border-input bg-background hover:bg-muted">
                  <TrendingUp className="h-4 w-4 mr-2" />
                  View All Stocks
                </Button>
                <Button className="w-full border border-input bg-background hover:bg-muted">
                  <BarChart3 className="h-4 w-4 mr-2" />
                  Trading Dashboard
                </Button>
                <Button className="w-full border border-input bg-background hover:bg-muted">
                  <Activity className="h-4 w-4 mr-2" />
                  Portfolio Analysis
                </Button>
                <Button className="w-full bg-blue-600 hover:bg-blue-700">
                  <DollarSign className="h-4 w-4 mr-2" />
                  Make Trade
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </DashboardLayout>
  )
}
