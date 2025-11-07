import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User, LoginCredentials, RegisterData } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

  function initAuth() {
    const storedAccessToken = localStorage.getItem('access_token')
    const storedRefreshToken = localStorage.getItem('refresh_token')

    if (storedAccessToken && storedRefreshToken) {
      accessToken.value = storedAccessToken
      refreshToken.value = storedRefreshToken
      fetchCurrentUser()
    }
  }

  async function login(credentials: LoginCredentials) {
    try {
      loading.value = true
      error.value = null

      const response = await authApi.login(credentials)

      accessToken.value = response.access_token
      refreshToken.value = response.refresh_token

      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)

      await fetchCurrentUser()
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(userData: RegisterData) {
    try {
      loading.value = true
      error.value = null

      await authApi.register(userData)

      // Auto-login after registration
      return await login({
        username: userData.username,
        password: userData.password,
      })
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchCurrentUser() {
    try {
      user.value = await authApi.getCurrentUser()
    } catch (err) {
      logout()
    }
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    user,
    accessToken,
    refreshToken,
    loading,
    error,
    isAuthenticated,
    initAuth,
    login,
    register,
    fetchCurrentUser,
    logout,
  }
})
