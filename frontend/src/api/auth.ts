import { apiClient } from './client'
import type { LoginCredentials, RegisterData, TokenResponse, User } from '@/types'

export const authApi = {
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const params = new URLSearchParams()
    params.append('username', credentials.username)
    params.append('password', credentials.password)

    const { data } = await apiClient.post<TokenResponse>('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
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

  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    const { data } = await apiClient.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    })
    return data
  },

  async logout(): Promise<void> {
    await apiClient.post('/auth/logout')
  },
}
