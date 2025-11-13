<template>
  <AppLayout>
    <div class="space-y-8">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-gray-500 uppercase tracking-wide">Проект</p>
          <h1 class="text-3xl font-semibold text-gray-900">
            {{ projectsStore.currentProject?.name || 'Бэклог' }}
          </h1>
          <p class="text-gray-500">
            Управляйте спринтами и приоритетами. Здесь появятся списки задач по спринтам и бэклогу.
          </p>
        </div>
        <button class="btn btn-primary" @click="openCreateTask">
          Создать задачу
        </button>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <section class="card">
          <div class="card-header flex items-center justify-between">
            <div>
              <h2 class="text-lg font-semibold text-gray-900">Активный спринт</h2>
              <p class="text-sm text-gray-500">Скоро здесь появится планирование спринтов</p>
            </div>
            <span class="badge badge-primary">В разработке</span>
          </div>
          <div class="card-body">
            <p class="text-sm text-gray-500">
              Мы работаем над полноценным списком задач спринта с оценками, доской планирования и burndown диаграммами.
            </p>
            <ul class="mt-4 space-y-3">
              <li
                v-for="task in sprintMock"
                :key="task.id"
                class="p-3 rounded-md border border-dashed border-gray-200 flex justify-between text-sm"
              >
                <div>
                  <p class="font-medium text-gray-900">{{ task.title }}</p>
                  <p class="text-gray-500 text-xs">{{ task.status }}</p>
                </div>
                <span class="text-gray-400">{{ task.story_points }} SP</span>
              </li>
            </ul>
          </div>
        </section>

        <section class="card">
          <div class="card-header flex items-center justify-between">
            <div>
              <h2 class="text-lg font-semibold text-gray-900">Бэклог</h2>
              <p class="text-sm text-gray-500">Задачи сортируются по приоритету</p>
            </div>
            <button class="text-sm text-gray-500 hover:text-success-600" @click="refreshTasks">
              Обновить
            </button>
          </div>
          <div class="card-body">
            <div v-if="tasksStore.loading" class="text-gray-400 text-sm">Загрузка...</div>
            <ul v-else class="divide-y divide-gray-100">
              <li
                v-for="task in backlogTasks"
                :key="task.id"
                class="py-3 flex items-center justify-between hover:bg-white rounded-md px-2 transition"
              >
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ task.title }}</p>
                  <p class="text-xs text-gray-500">
                    #{{ task.task_number }} • {{ task.status }} • {{ task.priority }}
                  </p>
                </div>
                <router-link :to="`/tasks/${task.id}`" class="text-success-600 text-xs font-semibold">
                  Открыть
                </router-link>
              </li>
              <li v-if="!backlogTasks.length" class="py-6 text-center text-gray-400 text-sm">
                Задачи отсутствуют. Создайте первую задачу.
              </li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useProjectsStore } from '@/stores/projects'
import { useTasksStore } from '@/stores/tasks'
import type { Task } from '@/types'

const route = useRoute()
const projectsStore = useProjectsStore()
const tasksStore = useTasksStore()

const sprintMock = [
  { id: 'mock-1', title: 'Планирование RBAC', status: 'Запланировано', story_points: 5 },
  { id: 'mock-2', title: 'Редизайн карточки задачи', status: 'В процессе', story_points: 8 },
]

const priorityOrder: Record<Task['priority'], number> = {
  critical: 0,
  high: 1,
  medium: 2,
  low: 3,
}

const backlogTasks = computed(() =>
  tasksStore.tasks
    .filter((task) => task.status === 'backlog' || task.status === 'todo')
    .sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority])
)

const refreshTasks = () => {
  const projectId = route.params.id as string | undefined
  tasksStore.fetchTasks(projectId ? { project_id: projectId } : undefined)
}

const openCreateTask = () => {
  alert('Новый опыт создания задачи появится позже. Пока используйте доску проекта.')
}

onMounted(() => {
  const projectId = route.params.id as string | undefined
  if (projectId) {
    projectsStore.fetchProject(projectId)
    tasksStore.fetchTasks({ project_id: projectId })
  } else {
    tasksStore.fetchTasks()
  }
})
</script>
