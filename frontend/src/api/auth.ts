import { apiClient } from './client'
import type { LoginCredentials, RegisterData, TokenResponse, User } from '@/types'

export const authApi = {
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const { data } = await apiClient.post<TokenResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return data
  },

  async register(userData: RegisterData): Promise<User> {
    const { data } = await apiClient.post<User>('/auth/register', userData)
    return data
  },

  async getCurrentUser(): Promise<User> {
    const { data } = await apiClient.get<User>('/auth/me')
    return data
  },

  async logout(): Promise<void> {
    await apiClient.post('/auth/logout')
  },
}
