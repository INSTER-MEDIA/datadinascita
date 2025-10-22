/**
 * API client for DataDiNascita backend.
 */
import axios from 'axios'
import type {
  User,
  Contact,
  Event,
  AuthTokens,
  LoginRequest,
  RegisterRequest,
  PaginatedResponse,
} from '@/types'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/api/v1/auth/token/refresh/`,
            { refresh: refreshToken }
          )

          const { access } = response.data
          localStorage.setItem('access_token', access)

          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed - clear tokens and redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: async (data: LoginRequest): Promise<AuthTokens & { user: User }> => {
    const response = await api.post('/api/v1/auth/login/', data)
    return response.data
  },

  register: async (data: RegisterRequest): Promise<AuthTokens & { user: User }> => {
    const response = await api.post('/api/v1/auth/register/', data)
    return response.data
  },

  logout: async (refreshToken: string): Promise<void> => {
    await api.post('/api/v1/auth/logout/', { refresh: refreshToken })
  },

  getProfile: async (): Promise<User> => {
    const response = await api.get('/api/v1/auth/profile/')
    return response.data
  },

  updateProfile: async (data: Partial<User>): Promise<User> => {
    const response = await api.patch('/api/v1/auth/profile/', data)
    return response.data
  },
}

// Contacts API
export const contactsApi = {
  list: async (params?: {
    page?: number
    search?: string
  }): Promise<PaginatedResponse<Contact>> => {
    const response = await api.get('/api/v1/birthdays/contacts/', { params })
    return response.data
  },

  get: async (id: number): Promise<Contact> => {
    const response = await api.get(`/api/v1/birthdays/contacts/${id}/`)
    return response.data
  },

  create: async (data: Partial<Contact>): Promise<Contact> => {
    const response = await api.post('/api/v1/birthdays/contacts/', data)
    return response.data
  },

  update: async (id: number, data: Partial<Contact>): Promise<Contact> => {
    const response = await api.patch(`/api/v1/birthdays/contacts/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/v1/birthdays/contacts/${id}/`)
  },

  upcomingBirthdays: async (days: number = 30): Promise<Contact[]> => {
    const response = await api.get('/api/v1/birthdays/contacts/upcoming_birthdays/', {
      params: { days },
    })
    return response.data
  },

  importCsv: async (file: File, skipDuplicates: boolean = true) => {
    const formData = new FormData()
    formData.append('csv_file', file)
    formData.append('skip_duplicates', String(skipDuplicates))

    const response = await api.post('/api/v1/birthdays/contacts/import_csv/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  exportCsv: async (): Promise<Blob> => {
    const response = await api.get('/api/v1/birthdays/contacts/export_csv/', {
      responseType: 'blob',
    })
    return response.data
  },

  deleteAll: async (): Promise<void> => {
    await api.delete('/api/v1/birthdays/contacts/delete_all/')
  },
}

// Events API
export const eventsApi = {
  list: async (params?: {
    page?: number
    search?: string
    type?: string
  }): Promise<PaginatedResponse<Event>> => {
    const response = await api.get('/api/v1/birthdays/events/', { params })
    return response.data
  },

  get: async (id: number): Promise<Event> => {
    const response = await api.get(`/api/v1/birthdays/events/${id}/`)
    return response.data
  },

  create: async (data: Partial<Event>): Promise<Event> => {
    const response = await api.post('/api/v1/birthdays/events/', data)
    return response.data
  },

  update: async (id: number, data: Partial<Event>): Promise<Event> => {
    const response = await api.patch(`/api/v1/birthdays/events/${id}/`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/v1/birthdays/events/${id}/`)
  },

  upcomingEvents: async (days: number = 30): Promise<Event[]> => {
    const response = await api.get('/api/v1/birthdays/events/upcoming_events/', {
      params: { days },
    })
    return response.data
  },
}

export default api
