import axios, { AxiosInstance, AxiosError } from 'axios'
import { useAuthStore } from '@/stores/auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: `${API_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const authStore = useAuthStore()
        if (authStore.accessToken) {
          config.headers.Authorization = `Bearer ${authStore.accessToken}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor for error handling and token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError<any>) => {
        const originalRequest = error.config as any

        // Handle 401 - Unauthorized
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          const authStore = useAuthStore()

          // Try to refresh token
          if (authStore.refreshToken) {
            try {
              const { authApi } = await import('./auth')
              const response = await authApi.refreshToken(authStore.refreshToken)

              authStore.accessToken = response.access_token
              authStore.refreshToken = response.refresh_token

              localStorage.setItem('access_token', response.access_token)
              localStorage.setItem('refresh_token', response.refresh_token)

              // Retry original request with new token
              originalRequest.headers.Authorization = `Bearer ${response.access_token}`
              return this.client(originalRequest)
            } catch (refreshError) {
              // Refresh failed, logout user
              authStore.logout()
              window.location.href = '/login'
              return Promise.reject(refreshError)
            }
          } else {
            // No refresh token, logout
            authStore.logout()
            window.location.href = '/login'
          }
        }

        // Extract error message from response
        let errorMessage = 'Произошла ошибка'
        if (error.response?.data) {
          if (typeof error.response.data === 'string') {
            errorMessage = error.response.data
          } else if (error.response.data.detail) {
            if (typeof error.response.data.detail === 'string') {
              errorMessage = error.response.data.detail
            } else if (Array.isArray(error.response.data.detail)) {
              errorMessage = error.response.data.detail.map((e: any) => e.msg || e.message).join(', ')
            }
          } else if (error.response.data.message) {
            errorMessage = error.response.data.message
          }
        } else if (error.message) {
          errorMessage = error.message
        }

        // Create enhanced error object
        const enhancedError = new Error(errorMessage) as any
        enhancedError.status = error.response?.status
        enhancedError.originalError = error
        enhancedError.response = error.response

        return Promise.reject(enhancedError)
      }
    )
  }

  get instance() {
    return this.client
  }
}

export const apiClient = new ApiClient().instance
