<template>
  <AppLayout>
    <div class="space-y-6">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Главная</h1>
        <p class="mt-2 text-gray-600">Добро пожаловать, {{ authStore.user?.username }}!</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div class="card">
          <div class="card-body">
            <div class="flex items-center">
              <div class="flex-1">
                <div class="text-sm font-medium text-gray-500">Всего проектов</div>
                <div class="mt-1 text-3xl font-semibold text-gray-900">
                  {{ projectsStore.projects.length }}
                </div>
              </div>
              <div class="w-12 h-12 bg-success-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
            <div class="flex items-center">
              <div class="flex-1">
                <div class="text-sm font-medium text-gray-500">Всего задач</div>
                <div class="mt-1 text-3xl font-semibold text-gray-900">
                  {{ tasksStore.tasks.length }}
                </div>
              </div>
              <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
            <div class="flex items-center">
              <div class="flex-1">
                <div class="text-sm font-medium text-gray-500">В работе</div>
                <div class="mt-1 text-3xl font-semibold text-gray-900">
                  {{ tasksStore.tasksByStatus.in_progress.length }}
                </div>
              </div>
              <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
            <div class="flex items-center">
              <div class="flex-1">
                <div class="text-sm font-medium text-gray-500">Завершено</div>
                <div class="mt-1 text-3xl font-semibold text-gray-900">
                  {{ tasksStore.tasksByStatus.done.length }}
                </div>
              </div>
              <div class="w-12 h-12 bg-success-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Projects -->
      <div class="card">
        <div class="card-header">
          <h2 class="text-lg font-semibold text-gray-900">Недавние проекты</h2>
        </div>
        <div class="card-body">
          <div v-if="projectsStore.loading" class="text-center py-8">
            <div class="text-gray-500">Загрузка...</div>
          </div>
          <div v-else-if="projectsStore.projects.length === 0" class="text-center py-8">
            <p class="text-gray-500">Проектов пока нет</p>
            <router-link to="/projects" class="mt-4 btn btn-primary inline-block">
              Создать проект
            </router-link>
          </div>
          <div v-else class="space-y-4">
            <div
              v-for="project in projectsStore.projects.slice(0, 5)"
              :key="project.id"
              class="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg border border-gray-200"
            >
              <div>
                <h3 class="font-medium text-gray-900">{{ project.name }}</h3>
                <p class="text-sm text-gray-500">{{ project.key }}</p>
              </div>
              <router-link
                :to="`/projects/${project.id}/board`"
                class="btn btn-secondary btn-sm"
              >
                Открыть доску
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import { useProjectsStore } from '@/stores/projects'
import { useTasksStore } from '@/stores/tasks'

const authStore = useAuthStore()
const projectsStore = useProjectsStore()
const tasksStore = useTasksStore()

onMounted(() => {
  projectsStore.fetchProjects()
  tasksStore.fetchTasks()
})
</script>
