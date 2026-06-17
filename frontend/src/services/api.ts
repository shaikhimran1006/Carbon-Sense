import axios, { AxiosInstance } from 'axios'

// ==================== CONFIGURATION ====================
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ==================== CACHING UTILITY ====================
class SimpleCache<T> {
  private cache: Map<string, { data: T; timestamp: number }> = new Map()
  private readonly TTL: number = 60000 // 1 minute TTL

  get(key: string): T | null {
    const entry = this.cache.get(key)
    if (!entry) return null
    if (Date.now() - entry.timestamp > this.TTL) {
      this.cache.delete(key)
      return null
    }
    return entry.data
  }

  set(key: string, data: T): void {
    this.cache.set(key, { data, timestamp: Date.now() })
  }

  clear(): void {
    this.cache.clear()
  }
}

const carbonCache = new SimpleCache<any>()

// ==================== AXIOS INSTANCE ====================
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor: add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Response interceptor: handle 401s and errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      // Use window.location for navigation in SPA fallback
      if (!window.location.pathname.startsWith('/login')) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// ==================== TYPES & INTERFACES ====================
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
  difficulty: 'easy' | 'medium' | 'hard'
  expected_reduction: number
  impact: string
}

export interface SimulationResult {
  before_total: number
  after_total: number
  reduction_kg: number
  reduction_percent: number
  breakdown: Array<{ category: string; co2: number; percentage: number }>
}

export interface AssistantRequest {
  message: string
}

export interface AssistantResponse {
  response: string
  recommendations: Recommendation[]
}

// ==================== API METHODS ====================
export const authAPI = {
  register: (data: { email: string; password: string; name: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
}

export const userAPI = {
  getMe: () => api.get<User>('/users/me'),
  updateMe: (data: Partial<User>) => {
    carbonCache.clear() // Invalidate carbon cache after profile update
    return api.put<User>('/users/me', data)
  },
}

export const carbonAPI = {
  calculate: () => {
    carbonCache.clear() // Invalidate cache on recalculate
    return api.post<CarbonLog>('/carbon/calculate')
  },
  getLatest: async () => {
    const cached = carbonCache.get('latest')
    if (cached) return cached
    const response = await api.get<CarbonLog>('/carbon/latest')
    carbonCache.set('latest', response)
    return response
  },
  getHistory: () => api.get<CarbonLog[]>('/carbon/history'),
  getRecommendations: async () => {
    const cached = carbonCache.get('recommendations')
    if (cached) return cached
    const response = await api.get<Recommendation[]>('/carbon/recommendations')
    carbonCache.set('recommendations', response)
    return response
  },
  simulate: (data: Partial<User>) =>
    api.post<SimulationResult>('/carbon/simulate', data),
  chat: (message: string) =>
    api.post<AssistantResponse>('/carbon/assistant', { message }),
}

export default api
