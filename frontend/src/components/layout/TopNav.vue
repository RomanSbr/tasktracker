<template>
  <header class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-30">
    <div class="px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
      <div class="flex items-center space-x-6 flex-1">
        <router-link to="/dashboard" class="flex items-center space-x-2 shrink-0">
          <span class="text-xl font-bold text-gray-900">Task<span class="text-success-600">Tracker</span></span>
        </router-link>

        <div class="hidden md:flex items-center space-x-3 text-sm text-gray-500">
          <span class="font-medium text-gray-900">Workspace</span>
          <span>·</span>
          <div class="relative">
            <select
              v-model="selectedOrgId"
              class="pl-3 pr-8 py-1.5 bg-gray-100 border border-gray-200 rounded-md text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-success-500"
            >
              <option disabled value="">{{ organizationsStore.organizations.length ? 'Выберите' : 'Нет рабочей области' }}</option>
              <option
                v-for="org in organizationsStore.organizations"
                :key="org.id"
                :value="org.id"
              >
                {{ org.name }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="flex-1 max-w-xl mx-6 hidden lg:flex shrink-0">
        <div class="w-full relative">
          <span class="absolute inset-y-0 left-3 flex items-center text-gray-400">
            <MagnifyingGlassIcon class="w-4 h-4" />
          </span>
          <input
            type="text"
            class="w-full pl-9 pr-4 py-2 text-sm rounded-md border border-gray-200 bg-gray-50 focus:ring-success-500 focus:border-success-500"
            placeholder="Поиск задач, проектов или участников (скоро)"
            disabled
          />
        </div>
      </div>

      <div class="flex items-center space-x-3 shrink-0">
        <button class="btn btn-primary hidden md:inline-flex items-center space-x-2" @click="handleCreateIssue">
          <PlusIcon class="w-4 h-4" />
          <span>Создать</span>
        </button>
        <button class="p-2 rounded-full hover:bg-gray-100 text-gray-500" title="Уведомления в разработке">
          <BellIcon class="w-5 h-5" />
        </button>
        <div class="flex items-center space-x-2">
          <div class="text-right hidden sm:block">
            <div class="text-sm font-semibold text-gray-900">{{ userDisplayName }}</div>
            <div class="text-xs text-gray-500">Онлайн</div>
          </div>
          <div class="w-9 h-9 rounded-full bg-success-100 text-success-700 flex items-center justify-center font-semibold uppercase">
            {{ userInitials }}
          </div>
          <button @click="handleLogout" class="text-xs text-gray-400 hover:text-gray-600">Выход</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useOrganizationsStore } from '@/stores/organizations'
import { useProjectsStore } from '@/stores/projects'
import { PlusIcon, BellIcon, MagnifyingGlassIcon } from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const organizationsStore = useOrganizationsStore()
const projectsStore = useProjectsStore()

const selectedOrgId = computed({
  get: () => organizationsStore.currentOrganization?.id || '',
  set: (value: string) => {
    if (value) {
      organizationsStore.selectOrganization(value)
    }
  },
})

onMounted(async () => {
  await organizationsStore.fetchOrganizations()
  if (organizationsStore.currentOrganization?.id) {
    projectsStore.fetchProjects(organizationsStore.currentOrganization.id)
  }
})

watch(
  () => organizationsStore.currentOrganization?.id,
  (newId) => {
    if (newId) {
      projectsStore.fetchProjects(newId)
    }
  }
)

const userInitials = computed(() => {
  const first = authStore.user?.first_name?.[0]
  const last = authStore.user?.last_name?.[0]
  if (first || last) {
    return `${first || ''}${last || ''}`.toUpperCase()
  }
  return (authStore.user?.username || '?').slice(0, 2).toUpperCase()
})

const userDisplayName = computed(() => {
  const first = authStore.user?.first_name
  const last = authStore.user?.last_name
  if (first || last) {
    return [first, last].filter(Boolean).join(' ')
  }
  return authStore.user?.username || '—'
})

const handleCreateIssue = () => {
  alert('Создание задачи появится в следующем обновлении ✨')
}

const handleLogout = () => {
  authStore.logout()
  window.location.href = '/login'
}
</script>
