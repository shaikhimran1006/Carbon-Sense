import React, { useState } from 'react'
import { Layout } from '../components/Layout'
import { carbonAPI, SimulationResult } from '../services/api'
import { TrendingUp, ArrowDown } from 'lucide-react'

export const Simulator: React.FC = () => {
  const [simParams, setSimParams] = useState({
    vehicle_type: '',
    daily_distance_km: '',
    weekly_frequency: '',
    monthly_electricity_kwh: '',
    monthly_gas_m3: '',
    diet_type: '',
    weekly_meat_days: '',
  })
  const [result, setResult] = useState<SimulationResult | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSimulate = async () => {
    setLoading(true)
    try {
      const params = Object.fromEntries(
        Object.entries(simParams).filter(([_, v]) => v !== '')
      )
      const response = await carbonAPI.simulate(params)
      setResult(response.data)
    } catch (error) {
      console.error('Simulation failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="space-y-6 mb-20 md:mb-0">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Carbon Twin Simulator</h1>
          <p className="text-gray-600 dark:text-gray-400">See how lifestyle changes impact your footprint</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Change Parameters</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Vehicle Type
                </label>
                <select
                  value={simParams.vehicle_type}
                  onChange={(e) => setSimParams({ ...simParams, vehicle_type: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="">No change</option>
                  <option value="petrol">Petrol Car</option>
                  <option value="diesel">Diesel Car</option>
                  <option value="hybrid">Hybrid</option>
                  <option value="electric">Electric</option>
                  <option value="public_transport">Public Transport</option>
                  <option value="bike">Bike</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Daily Distance (km)
                </label>
                <input
                  type="number"
                  value={simParams.daily_distance_km}
                  onChange={(e) => setSimParams({ ...simParams, daily_distance_km: e.target.value })}
                  placeholder="No change"
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Diet Type
                </label>
                <select
                  value={simParams.diet_type}
                  onChange={(e) => setSimParams({ ...simParams, diet_type: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="">No change</option>
                  <option value="omnivore">Omnivore</option>
                  <option value="vegetarian">Vegetarian</option>
                  <option value="vegan">Vegan</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Meat Days/Week
                </label>
                <input
                  type="number"
                  value={simParams.weekly_meat_days}
                  onChange={(e) => setSimParams({ ...simParams, weekly_meat_days: e.target.value })}
                  placeholder="No change"
                  min="0"
                  max="7"
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>

              <button
                onClick={handleSimulate}
                disabled={loading}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-lg transition-colors disabled:opacity-50"
              >
                {loading ? 'Simulating...' : 'Simulate Changes'}
              </button>
            </div>
          </div>

          {result && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Results</h3>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-xl">
                  <p className="text-sm text-gray-600 dark:text-gray-400">Before</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {result.before_total.toFixed(1)} kg
                  </p>
                </div>
                <div className="p-4 bg-green-50 dark:bg-green-900/30 rounded-xl">
                  <p className="text-sm text-green-600 dark:text-green-400">After</p>
                  <p className="text-2xl font-bold text-green-700 dark:text-green-300">
                    {result.after_total.toFixed(1)} kg
                  </p>
                </div>
              </div>

              {result.reduction_kg > 0 && (
                <div className="flex items-center gap-3 p-4 bg-green-100 dark:bg-green-900/30 rounded-xl mb-6">
                  <div className="w-10 h-10 bg-green-600 rounded-full flex items-center justify-center">
                    <ArrowDown className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="font-semibold text-green-800 dark:text-green-200">
                      {result.reduction_kg.toFixed(1)} kg CO2 saved!
                    </p>
                    <p className="text-sm text-green-700 dark:text-green-300">
                      {result.reduction_percent.toFixed(1)}% reduction
                    </p>
                  </div>
                </div>
              )}

              <div className="space-y-3">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300">New Breakdown:</p>
                {result.breakdown.map((item, i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <span className="text-gray-700 dark:text-gray-300">{item.category}</span>
                    <span className="font-semibold text-gray-900 dark:text-white">
                      {item.co2.toFixed(1)} kg ({item.percentage.toFixed(1)}%)
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}
