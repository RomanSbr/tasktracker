<template>
  <AppLayout>
    <div class="space-y-6">
      <div v-if="projectsStore.loading" class="text-center py-12">
        <div class="text-gray-500">Загрузка проекта...</div>
      </div>
      <div v-else-if="projectsStore.currentProject">
        <div class="flex justify-between items-start">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">
              {{ projectsStore.currentProject.name }}
            </h1>
            <p class="text-gray-600">{{ projectsStore.currentProject.key }}</p>
          </div>
          <router-link :to="`/projects/${projectsStore.currentProject.id}/board`" class="btn btn-primary">
            Открыть доску
          </router-link>
        </div>

        <div class="mt-6 card">
          <div class="card-body">
            <h2 class="text-lg font-semibold mb-4">Детали проекта</h2>
            <dl class="space-y-4">
              <div>
                <dt class="text-sm font-medium text-gray-500">Описание</dt>
                <dd class="mt-1 text-gray-900">{{ projectsStore.currentProject.description || 'Описание отсутствует' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Статус</dt>
                <dd class="mt-1">
                  <span class="badge badge-success">{{ projectsStore.currentProject.status }}</span>
                </dd>
              </div>
              <div v-if="projectsStore.currentProject.start_date">
                <dt class="text-sm font-medium text-gray-500">Дата начала</dt>
                <dd class="mt-1 text-gray-900">{{ formatDate(projectsStore.currentProject.start_date) }}</dd>
              </div>
              <div v-if="projectsStore.currentProject.end_date">
                <dt class="text-sm font-medium text-gray-500">Дата окончания</dt>
                <dd class="mt-1 text-gray-900">{{ formatDate(projectsStore.currentProject.end_date) }}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useProjectsStore } from '@/stores/projects'
import { format } from 'date-fns'

const route = useRoute()
const projectsStore = useProjectsStore()

onMounted(() => {
  const projectId = route.params.id as string
  projectsStore.fetchProject(projectId)
})

const formatDate = (date: string) => {
  return format(new Date(date), 'MMM dd, yyyy')
}
</script>
