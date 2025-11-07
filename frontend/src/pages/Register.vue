<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Task<span class="text-success-600">Tracker</span>
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Создайте свой аккаунт
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="email" class="sr-only">Email</label>
            <input
              id="email"
              v-model="userData.email"
              name="email"
              type="email"
              required
              class="input"
              placeholder="Email"
            />
          </div>
          <div>
            <label for="username" class="sr-only">Имя пользователя</label>
            <input
              id="username"
              v-model="userData.username"
              name="username"
              type="text"
              required
              class="input"
              placeholder="Имя пользователя"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Пароль</label>
            <input
              id="password"
              v-model="userData.password"
              name="password"
              type="password"
              required
              class="input"
              placeholder="Пароль (мин. 8 символов, 1 заглавная, 1 цифра)"
            />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="first_name" class="sr-only">Имя</label>
              <input
                id="first_name"
                v-model="userData.first_name"
                name="first_name"
                type="text"
                class="input"
                placeholder="Имя (необязательно)"
              />
            </div>
            <div>
              <label for="last_name" class="sr-only">Фамилия</label>
              <input
                id="last_name"
                v-model="userData.last_name"
                name="last_name"
                type="text"
                class="input"
                placeholder="Фамилия (необязательно)"
              />
            </div>
          </div>
        </div>

        <div v-if="authStore.error" class="text-danger-600 text-sm text-center">
          {{ authStore.error }}
        </div>

        <div>
          <button
            type="submit"
            :disabled="authStore.loading"
            class="btn btn-primary w-full"
          >
            {{ authStore.loading ? 'Создание аккаунта...' : 'Зарегистрироваться' }}
          </button>
        </div>

        <div class="text-center text-sm">
          <span class="text-gray-600">Уже есть аккаунт? </span>
          <router-link to="/login" class="text-success-600 hover:text-success-500">
            Войти
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const userData = ref({
  email: '',
  username: '',
  password: '',
  first_name: '',
  last_name: '',
})

const handleRegister = async () => {
  const success = await authStore.register(userData.value)
  if (success) {
    router.push('/dashboard')
  }
}
</script>
