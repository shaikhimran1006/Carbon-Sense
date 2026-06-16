import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export interface User {
  id: number
  email: string
  name: string
  location?: string
  vehicle_type?: string
  daily_distance_km: number
  weekly_frequency: number
  monthly_electricity_kwh: number
  monthly_gas_m3: number
  diet_type: string
  weekly_meat_days: number
  shopping_frequency: string
  waste_recycling_rate: number
  created_at: string
}

export interface CarbonLog {
  id: number
  transport_co2: number
  energy_co2: number
  food_co2: number
  lifestyle_co2: number
  total_co2: number
  transport_percent: number
  energy_percent: number
  food_percent: number
  lifestyle_percent: number
  carbon_score: number
  created_at: string
}

export interface Recommendation {
  title: string
  description: string
  difficulty: string
  expected_reduction: number
  impact: string
}

export interface SimulationResult {
  before_total: number
  after_total: number
  reduction_kg: number
  reduction_percent: number
  breakdown: { category: string; co2: number; percentage: number }[]
}

export const authAPI = {
  register: (data: { email: string; password: string; name: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
}

export const userAPI = {
  getMe: () => api.get<User>('/users/me'),
  updateMe: (data: Partial<User>) => api.put<User>('/users/me', data),
}

export const carbonAPI = {
  calculate: () => api.post<CarbonLog>('/carbon/calculate'),
  getLatest: () => api.get<CarbonLog>('/carbon/latest'),
  getHistory: () => api.get<CarbonLog[]>('/carbon/history'),
  getRecommendations: () => api.get<Recommendation[]>('/carbon/recommendations'),
  simulate: (data: any) => api.post<SimulationResult>('/carbon/simulate', data),
  chat: (message: string) =>
    api.post('/carbon/assistant', { message }),
}

export default api
