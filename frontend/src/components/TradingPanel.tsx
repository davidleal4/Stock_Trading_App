'use client'

import { useState } from 'react'

interface TradingPanelProps {
  symbol: string
  currentPrice?: number
}

export function TradingPanel({ symbol, currentPrice }: TradingPanelProps) {
  const [orderType, setOrderType] = useState<'market' | 'limit'>('market')
  const [side, setSide] = useState<'buy' | 'sell'>('buy')
  const [quantity, setQuantity] = useState('')
  const [limitPrice, setLimitPrice] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle order submission
    console.log('Order submitted:', { symbol, orderType, side, quantity, limitPrice })
  }

  const totalValue = currentPrice && quantity ? parseFloat(quantity) * currentPrice : 0

  return (
    <div className="space-y-6">
      {/* Order Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Buy/Sell Toggle */}
        <div className="flex rounded-lg bg-gray-100 p-1">
          <button
            type="button"
            onClick={() => setSide('buy')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              side === 'buy'
                ? 'bg-success-600 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Buy
          </button>
          <button
            type="button"
            onClick={() => setSide('sell')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              side === 'sell'
                ? 'bg-danger-600 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Sell
          </button>
        </div>

        {/* Order Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Order Type
          </label>
          <select
            value={orderType}
            onChange={(e) => setOrderType(e.target.value as 'market' | 'limit')}
            className="input-field w-full"
          >
            <option value="market">Market Order</option>
            <option value="limit">Limit Order</option>
          </select>
        </div>

        {/* Quantity */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Quantity
          </label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            placeholder="Enter quantity"
            className="input-field w-full"
            min="1"
            step="1"
          />
        </div>

        {/* Limit Price (if limit order) */}
        {orderType === 'limit' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Limit Price
            </label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                $
              </span>
              <input
                type="number"
                value={limitPrice}
                onChange={(e) => setLimitPrice(e.target.value)}
                placeholder="0.00"
                className="input-field w-full pl-8"
                step="0.01"
              />
            </div>
          </div>
        )}

        {/* Order Summary */}
        {currentPrice && quantity && (
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-medium text-gray-900 mb-2">Order Summary</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Symbol:</span>
                <span className="font-medium">{symbol}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Side:</span>
                <span className={`font-medium ${side === 'buy' ? 'text-success-600' : 'text-danger-600'}`}>
                  {side.toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Quantity:</span>
                <span className="font-medium">{quantity}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Price:</span>
                <span className="font-medium">
                  {orderType === 'market' ? `~$${currentPrice.toFixed(2)}` : `$${limitPrice || '0.00'}`}
                </span>
              </div>
              <div className="flex justify-between border-t border-gray-200 pt-2">
                <span className="text-gray-600">Total:</span>
                <span className="font-medium">
                  ~${(orderType === 'market' ? totalValue : parseFloat(limitPrice || '0') * parseFloat(quantity)).toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          className={`w-full py-3 px-4 rounded-md font-medium text-white transition-colors ${
            side === 'buy'
              ? 'bg-success-600 hover:bg-success-700'
              : 'bg-danger-600 hover:bg-danger-700'
          }`}
          disabled={!quantity || (orderType === 'limit' && !limitPrice)}
        >
          Place {side.toUpperCase()} Order
        </button>
      </form>

      {/* Recent Orders */}
      <div className="border-t border-gray-200 pt-6">
        <h4 className="font-medium text-gray-900 mb-4">Recent Orders</h4>
        <div className="space-y-2">
          {[
            { id: 'ORDER_001', symbol: 'AAPL', side: 'BUY', quantity: 10, price: 150.25, status: 'Filled' },
            { id: 'ORDER_002', symbol: 'MSFT', side: 'SELL', quantity: 5, price: 300.50, status: 'Pending' },
          ].map((order) => (
            <div key={order.id} className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded">
              <div className="flex items-center space-x-3">
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  order.side === 'BUY' ? 'bg-success-100 text-success-800' : 'bg-danger-100 text-danger-800'
                }`}>
                  {order.side}
                </span>
                <span className="text-sm font-medium">{order.symbol}</span>
                <span className="text-sm text-gray-600">{order.quantity} @ ${order.price}</span>
              </div>
              <span className={`text-xs font-medium ${
                order.status === 'Filled' ? 'text-success-600' : 'text-yellow-600'
              }`}>
                {order.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}