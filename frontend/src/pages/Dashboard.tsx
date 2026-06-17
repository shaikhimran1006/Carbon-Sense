import React, { useState, useEffect } from 'react'
import { Layout } from '../components/Layout'
import { carbonAPI, CarbonLog, Recommendation } from '../services/api'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import { Leaf, Award, CheckCircle2, RefreshCw } from 'lucide-react'

const COLORS = ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444']

export const Dashboard: React.FC = () => {
  const [carbonData, setCarbonData] = useState<CarbonLog | null>(null)
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setError(null)
      const [carbonRes, recRes] = await Promise.all([
        carbonAPI.getLatest(),
        carbonAPI.getRecommendations(),
      ])
      setCarbonData(carbonRes.data)
      setRecommendations(recRes.data)
    } catch (error) {
      setError('Failed to load your carbon data. Please try again.')
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const chartData = carbonData
    ? [
        { name: 'Transport', value: carbonData.transport_co2 },
        { name: 'Energy', value: carbonData.energy_co2 },
        { name: 'Food', value: carbonData.food_co2 },
        { name: 'Lifestyle', value: carbonData.lifestyle_co2 },
      ]
    : []

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100 dark:bg-green-900/30'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30'
    if (score >= 40) return 'text-orange-600 bg-orange-100 dark:bg-orange-900/30'
    return 'text-red-600 bg-red-100 dark:bg-red-900/30'
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex flex-col items-center justify-center h-64 gap-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
          <p className="text-gray-500 dark:text-gray-400">Loading your carbon data...</p>
        </div>
      </Layout>
    )
  }

  if (error) {
    return (
      <Layout>
        <div className="flex flex-col items-center justify-center h-64 gap-4">
          <div className="bg-red-100 dark:bg-red-900/30 p-4 rounded-xl text-center max-w-md">
            <p className="text-red-700 dark:text-red-400 mb-2">{error}</p>
            <button
              onClick={fetchData}
              className="flex items-center gap-2 mx-auto px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
              aria-label="Retry loading data"
            >
              <RefreshCw className="w-4 h-4" aria-hidden="true" />
              Retry
            </button>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="space-y-6 mb-20 md:mb-0">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
            <p className="text-gray-600 dark:text-gray-400">Your carbon footprint overview</p>
          </div>
          <button
            onClick={fetchData}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            aria-label="Refresh data"
          >
            <RefreshCw className="w-5 h-5 text-gray-600 dark:text-gray-400" aria-hidden="true" />
          </button>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" role="region" aria-label="Carbon summary statistics">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6 transition-transform hover:scale-[1.02]">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total CO2</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">
                  {carbonData?.total_co2.toFixed(1) || 0}
                  <span className="text-lg font-normal text-gray-500">kg</span>
                </p>
              </div>
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center">
                <Leaf className="w-6 h-6 text-green-600 dark:text-green-400" aria-hidden="true" />
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6 transition-transform hover:scale-[1.02]">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Carbon Score</p>
                <p className={`text-3xl font-bold ${getScoreColor(carbonData?.carbon_score || 0)}`}>
                  {carbonData?.carbon_score || 0}
                  <span className="text-lg font-normal">/100</span>
                </p>
              </div>
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center">
                <Award className="w-6 h-6 text-blue-600 dark:text-blue-400" aria-hidden="true" />
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <section className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6" aria-label="Emission breakdown chart">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Emission Breakdown</h2>
            <div className="h-64" role="img" aria-label="Pie chart showing carbon emission breakdown">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {chartData.map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip aria-label="Chart details" />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="grid grid-cols-2 gap-4 mt-4">
              {chartData.map((item, index) => (
                <div key={item.name} className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }} aria-hidden="true" />
                  <span className="text-sm text-gray-600 dark:text-gray-400">{item.name}</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white ml-auto">
                    {item.value.toFixed(1)}kg
                  </span>
                </div>
              ))}
            </div>
          </section>

          <section className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6" aria-label="Personalized recommendations">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Personalized Actions</h2>
            <div className="space-y-4">
              {recommendations.map((rec, index) => (
                <article key={index} className="p-4 border border-gray-200 dark:border-gray-700 rounded-xl transition-transform hover:scale-[1.01]">
                  <div className="flex items-start gap-3">
                    <div className="mt-1">
                      <CheckCircle2 className="w-5 h-5 text-green-600" aria-hidden="true" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900 dark:text-white">{rec.title}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{rec.description}</p>
                      <div className="flex items-center gap-4 mt-2">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          rec.difficulty === 'easy' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                          rec.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                          'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
                        }`}>
                          {rec.difficulty}
                        </span>
                        <span className="text-xs text-green-600 dark:text-green-400 font-medium">{rec.impact}</span>
                      </div>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>
        </div>
      </div>
    </Layout>
  )
}
