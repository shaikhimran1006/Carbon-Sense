import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { userAPI } from '../services/api'
import { Leaf } from 'lucide-react'

export const Onboarding: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    location: '',
    vehicle_type: 'petrol',
    daily_distance_km: 0,
    weekly_frequency: 5,
    monthly_electricity_kwh: 0,
    monthly_gas_m3: 0,
    diet_type: 'omnivore',
    weekly_meat_days: 5,
    shopping_frequency: 'weekly',
    waste_recycling_rate: 0.3,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await userAPI.updateMe(formData)
    navigate('/dashboard')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100 dark:from-gray-900 dark:to-gray-800 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full mb-4">
            <Leaf className="w-8 h-8 text-green-600 dark:text-green-400" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Tell us about yourself</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">Help us calculate your carbon footprint</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Transport</label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Vehicle Type</label>
                <select
                  value={formData.vehicle_type}
                  onChange={(e) => setFormData({ ...formData, vehicle_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="petrol">Petrol Car</option>
                  <option value="diesel">Diesel Car</option>
                  <option value="hybrid">Hybrid</option>
                  <option value="electric">Electric</option>
                  <option value="public_transport">Public Transport</option>
                  <option value="bike">Bike</option>
                  <option value="walking">Walking</option>
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Daily Distance (km)</label>
                <input
                  type="number"
                  value={formData.daily_distance_km}
                  onChange={(e) => setFormData({ ...formData, daily_distance_km: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Days/Week</label>
                <input
                  type="number"
                  value={formData.weekly_frequency}
                  onChange={(e) => setFormData({ ...formData, weekly_frequency: Number(e.target.value) })}
                  min="0"
                  max="7"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Energy</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Electricity (kWh/month)</label>
                <input
                  type="number"
                  value={formData.monthly_electricity_kwh}
                  onChange={(e) => setFormData({ ...formData, monthly_electricity_kwh: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Gas (m³/month)</label>
                <input
                  type="number"
                  value={formData.monthly_gas_m3}
                  onChange={(e) => setFormData({ ...formData, monthly_gas_m3: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Diet</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Diet Type</label>
                <select
                  value={formData.diet_type}
                  onChange={(e) => setFormData({ ...formData, diet_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="omnivore">Omnivore</option>
                  <option value="vegetarian">Vegetarian</option>
                  <option value="vegan">Vegan</option>
                  <option value="pescatarian">Pescatarian</option>
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Meat Days/Week</label>
                <input
                  type="number"
                  value={formData.weekly_meat_days}
                  onChange={(e) => setFormData({ ...formData, weekly_meat_days: Number(e.target.value) })}
                  min="0"
                  max="7"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Lifestyle</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Shopping Frequency</label>
                <select
                  value={formData.shopping_frequency}
                  onChange={(e) => setFormData({ ...formData, shopping_frequency: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="weekly">Weekly</option>
                  <option value="biweekly">Bi-weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">Recycling Rate (0-1)</label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="1"
                  value={formData.waste_recycling_rate}
                  onChange={(e) => setFormData({ ...formData, waste_recycling_rate: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-lg transition-colors"
          >
            Continue to Dashboard
          </button>
        </form>
      </div>
    </div>
  )
}
