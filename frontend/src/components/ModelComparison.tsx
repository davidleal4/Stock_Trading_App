'use client'

interface ModelComparisonProps {
  symbol: string
}

export function ModelComparison({ symbol }: ModelComparisonProps) {
  const models = [
    {
      name: 'LightGBM',
      type: 'Gradient Boosting',
      accuracy: 0.85,
      mse: 0.025,
      status: 'trained',
      prediction: 152.45,
    },
    {
      name: 'LSTM',
      type: 'Deep Learning',
      accuracy: 0.82,
      mse: 0.031,
      status: 'training',
      prediction: 151.20,
    },
    {
      name: 'XGBoost',
      type: 'Gradient Boosting',
      accuracy: 0.83,
      mse: 0.028,
      status: 'trained',
      prediction: 153.10,
    },
  ]

  return (
    <div className="space-y-6">
      {/* Model Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {models.map((model, index) => (
          <div key={index} className="bg-gray-50 rounded-lg p-4 border">
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-semibold text-gray-900">{model.name}</h4>
              <span
                className={`px-2 py-1 rounded-full text-xs font-medium ${
                  model.status === 'trained'
                    ? 'bg-success-100 text-success-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}
              >
                {model.status}
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-3">{model.type}</p>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Accuracy:</span>
                <span className="text-sm font-medium">{(model.accuracy * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">MSE:</span>
                <span className="text-sm font-medium">{model.mse.toFixed(3)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Prediction:</span>
                <span className="text-sm font-medium text-primary-600">
                  ${model.prediction.toFixed(2)}
                </span>
              </div>
            </div>
            
            <div className="mt-4 flex space-x-2">
              <button className="flex-1 bg-primary-600 hover:bg-primary-700 text-white px-3 py-1 rounded text-sm transition-colors">
                Retrain
              </button>
              <button className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-1 rounded text-sm transition-colors">
                Details
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Training Controls */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h4 className="font-semibold text-gray-900 mb-4">Train New Model</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Model Type
            </label>
            <select className="input-field w-full">
              <option>LightGBM</option>
              <option>XGBoost</option>
              <option>CatBoost</option>
              <option>LSTM</option>
              <option>Transformer</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Training Period
            </label>
            <select className="input-field w-full">
              <option>Last 30 days</option>
              <option>Last 90 days</option>
              <option>Last 1 year</option>
              <option>Last 2 years</option>
            </select>
          </div>
        </div>
        <div className="mt-4">
          <button className="btn-primary">
            Start Training
          </button>
        </div>
      </div>
    </div>
  )
}