<template>
  <AppLayout>
    <div class="space-y-6">
      <div v-if="tasksStore.loading" class="text-center py-12">
        <div class="text-gray-500">Загрузка задачи...</div>
      </div>
      <div v-else-if="tasksStore.currentTask" class="max-w-4xl">
        <div class="mb-4">
          <router-link
            :to="`/projects/${tasksStore.currentTask.project_id}/board`"
            class="text-success-600 hover:text-success-700 text-sm"
          >
            ← Вернуться к доске
          </router-link>
        </div>

        <div class="card">
          <div class="card-body">
            <div class="flex items-start justify-between mb-6">
              <div class="flex-1">
                <div class="flex items-center space-x-3 mb-2">
                  <span class="text-sm text-gray-500">#{tasksStore.currentTask.task_number}</span>
                  <span
                    class="badge"
                    :class="{
                      'badge-danger': tasksStore.currentTask.priority === 'critical',
                      'bg-orange-100 text-orange-800': tasksStore.currentTask.priority === 'high',
                      'badge-primary': tasksStore.currentTask.priority === 'medium',
                      'bg-blue-100 text-blue-800': tasksStore.currentTask.priority === 'low',
                    }"
                  >
                    {{ tasksStore.currentTask.priority }}
                  </span>
                  <span
                    class="badge"
                    :class="{
                      'bg-purple-100 text-purple-800': tasksStore.currentTask.type === 'feature',
                      'badge-danger': tasksStore.currentTask.type === 'bug',
                      'badge-primary': tasksStore.currentTask.type === 'task',
                    }"
                  >
                    {{ tasksStore.currentTask.type }}
                  </span>
                </div>
                <h1 class="text-2xl font-bold text-gray-900">{{ tasksStore.currentTask.title }}</h1>
              </div>
              <div>
                <select
                  v-model="localStatus"
                  @change="updateStatus"
                  class="input text-sm"
                >
                  <option value="backlog">Бэклог</option>
                  <option value="todo">К выполнению</option>
                  <option value="in_progress">В работе</option>
                  <option value="review">На проверке</option>
                  <option value="testing">Тестирование</option>
                  <option value="done">Выполнено</option>
                </select>
              </div>
            </div>

            <div class="prose max-w-none">
              <h3 class="text-sm font-medium text-gray-500 mb-2">Описание</h3>
              <p class="text-gray-900">
                {{ tasksStore.currentTask.description || 'Описание отсутствует' }}
              </p>
            </div>

            <div class="mt-6 grid grid-cols-2 gap-6">
              <div>
                <h3 class="text-sm font-medium text-gray-500 mb-2">Детали</h3>
                <dl class="space-y-2">
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-600">Создана</dt>
                    <dd class="text-sm text-gray-900">{{ formatDate(tasksStore.currentTask.created_at) }}</dd>
                  </div>
                  <div v-if="tasksStore.currentTask.updated_at" class="flex justify-between">
                    <dt class="text-sm text-gray-600">Обновлена</dt>
                    <dd class="text-sm text-gray-900">{{ formatDate(tasksStore.currentTask.updated_at) }}</dd>
                  </div>
                  <div v-if="tasksStore.currentTask.due_date" class="flex justify-between">
                    <dt class="text-sm text-gray-600">Срок выполнения</dt>
                    <dd class="text-sm text-gray-900">{{ formatDate(tasksStore.currentTask.due_date) }}</dd>
                  </div>
                </dl>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-500 mb-2">Оценка</h3>
                <dl class="space-y-2">
                  <div v-if="tasksStore.currentTask.estimated_hours" class="flex justify-between">
                    <dt class="text-sm text-gray-600">Оценка</dt>
                    <dd class="text-sm text-gray-900">{{ tasksStore.currentTask.estimated_hours }}ч</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-600">Затрачено</dt>
                    <dd class="text-sm text-gray-900">{{ tasksStore.currentTask.logged_hours }}ч</dd>
                  </div>
                  <div v-if="tasksStore.currentTask.story_points" class="flex justify-between">
                    <dt class="text-sm text-gray-600">Story Points</dt>
                    <dd class="text-sm text-gray-900">{{ tasksStore.currentTask.story_points }}</dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useTasksStore } from '@/stores/tasks'
import { format } from 'date-fns'
import type { TaskStatus } from '@/types'

const route = useRoute()
const tasksStore = useTasksStore()
const localStatus = ref<TaskStatus>('backlog')

onMounted(() => {
  const taskId = route.params.id as string
  tasksStore.fetchTask(taskId)
})

watch(() => tasksStore.currentTask, (task) => {
  if (task) {
    localStatus.value = task.status
  }
})

const updateStatus = async () => {
  if (tasksStore.currentTask) {
    await tasksStore.updateTaskStatus(tasksStore.currentTask.id, localStatus.value)
  }
}

const formatDate = (date: string) => {
  return format(new Date(date), 'MMM dd, yyyy HH:mm')
}
</script>
