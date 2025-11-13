<template>
  <AppLayout>
    <div class="space-y-6">
      <header class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p class="text-xs uppercase text-gray-500 tracking-wide">Доска проекта</p>
          <div class="flex items-center space-x-3">
            <h1 class="text-3xl font-semibold text-gray-900">
              {{ projectsStore.currentProject?.name || 'Доска' }}
            </h1>
            <span class="text-sm uppercase text-gray-400">
              {{ projectsStore.currentProject?.key }}
            </span>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <button class="btn btn-secondary text-sm" @click="openFilters">Фильтры</button>
          <button class="btn btn-primary text-sm inline-flex items-center space-x-2" @click="showCreateTaskModal = true">
            <span>Создать задачу</span>
          </button>
        </div>
      </header>

      <section class="bg-white border-b border-gray-200 -mx-8 px-8 py-3 flex flex-wrap items-center gap-4 shadow-sm">
        <div class="flex items-center gap-6">
          <div class="flex items-center space-x-2 text-sm">
            <span class="text-gray-500">Задач:</span>
            <span class="font-semibold text-gray-900">{{ tasksStore.tasks.length }}</span>
          </div>
          <div class="h-4 w-px bg-gray-300"></div>
          <div class="flex items-center space-x-2 text-xs">
            <button class="px-3 py-1.5 rounded hover:bg-gray-100 text-gray-700 border border-gray-300 transition-colors flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span>Мои задачи</span>
            </button>
            <button class="px-3 py-1.5 rounded hover:bg-gray-100 text-gray-700 border border-gray-300 transition-colors flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92z" clip-rule="evenodd" />
              </svg>
              <span>Высокий приоритет</span>
            </button>
            <button class="px-3 py-1.5 rounded hover:bg-gray-100 text-gray-700 border border-gray-300 transition-colors">
              Без исполнителя
            </button>
          </div>
        </div>
        <div class="ml-auto flex items-center gap-2">
          <button class="p-1.5 rounded hover:bg-gray-100 text-gray-600" title="Группировка">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <button class="p-1.5 rounded hover:bg-gray-100 text-gray-600" title="Настройки">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
        </div>
      </section>

      <div v-if="tasksStore.loading || loadingWorkflow" class="text-center py-12 text-gray-500">
        Загрузка доски...
      </div>

      <div
        v-else-if="statuses.length > 0"
        class="grid gap-4 min-h-[60vh]"
        :class="{
          'grid-cols-1': statuses.length === 1,
          'md:grid-cols-2': statuses.length === 2,
          'md:grid-cols-2 xl:grid-cols-3': statuses.length >= 3 && statuses.length <= 6,
          'md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4': statuses.length > 6,
        }"
      >
        <div
          v-for="status in statuses"
          :key="status.value"
          class="bg-gray-50/50 border border-gray-200 rounded-lg flex flex-col min-h-[500px]"
          @drop="handleDrop($event, status.value)"
          @dragover.prevent
          @dragenter.prevent
        >
          <div class="px-3 py-2.5 border-b border-gray-200 bg-white/80 backdrop-blur-sm flex items-center justify-between sticky top-0 z-10">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-gray-700 uppercase tracking-wide">
                {{ status.label }}
              </span>
              <span class="px-1.5 py-0.5 text-xs font-semibold text-gray-600 bg-gray-200 rounded">
                {{ tasksByStatus[status.value]?.length || 0 }}
              </span>
            </div>
            <button class="text-gray-400 hover:text-gray-600 p-1 hover:bg-gray-100 rounded transition-colors" title="Действия">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
              </svg>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto p-3 space-y-3">
            <div
              v-for="task in tasksByStatus[status.value]"
              :key="task.id"
              draggable="true"
              @dragstart="handleDragStart($event, task)"
              @click="viewTask(task.id)"
              class="bg-white rounded-md border border-gray-200 shadow-sm hover:shadow-lg hover:border-blue-300 transition-all cursor-pointer group"
            >
              <div class="p-3 space-y-2.5">
                <div class="flex items-start justify-between gap-2">
                  <h4 class="text-sm font-medium text-gray-900 line-clamp-2 flex-1 group-hover:text-blue-600 transition-colors">
                    {{ task.title }}
                  </h4>
                  <button
                    class="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-gray-600 transition-opacity flex-shrink-0"
                    @click.stop="() => {}"
                    title="Дополнительно"
                  >
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                    </svg>
                  </button>
                </div>

                <div class="flex items-center gap-2 flex-wrap">
                  <span class="text-xs text-gray-500 font-mono">
                    {{ projectsStore.currentProject?.key }}-{{ task.task_number }}
                  </span>
                  <span
                    v-if="task.priority !== 'medium'"
                    class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-xs font-medium"
                    :class="{
                      'bg-red-50 text-red-700 border border-red-200': task.priority === 'critical',
                      'bg-orange-50 text-orange-700 border border-orange-200': task.priority === 'high',
                      'bg-gray-50 text-gray-600 border border-gray-200': task.priority === 'low',
                    }"
                  >
                    <svg v-if="task.priority === 'critical' || task.priority === 'high'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                    </svg>
                    {{ task.priority === 'critical' ? 'Критический' : task.priority === 'high' ? 'Высокий' : 'Низкий' }}
                  </span>
                </div>

                <div class="flex items-center justify-between pt-1">
                  <div class="flex items-center gap-2">
                    <span
                      class="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded"
                      :class="{
                        'bg-purple-50 text-purple-700': task.type === 'feature',
                        'bg-red-50 text-red-700': task.type === 'bug',
                        'bg-blue-50 text-blue-700': task.type === 'task',
                        'bg-green-50 text-green-700': task.type === 'improvement',
                      }"
                    >
                      <svg v-if="task.type === 'bug'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                      <svg v-else-if="task.type === 'feature'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
                      </svg>
                      {{ task.type }}
                    </span>
                    <span v-if="task.story_points" class="text-xs text-gray-500 flex items-center gap-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                      </svg>
                      {{ task.story_points }}
                    </span>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <div v-if="task.assignee_id" class="w-6 h-6 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-xs font-semibold" title="Исполнитель">
                      {{ task.assignee_id.substring(0, 2).toUpperCase() }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div
              v-if="!tasksByStatus[status.value]?.length"
              class="text-center text-gray-400 text-xs py-6 border border-dashed border-gray-200 rounded-lg"
            >
              Нет задач
            </div>
          </div>
        </div>
      </div>

      <Teleport to="body">
        <div
          v-if="showCreateTaskModal"
          class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
        >
          <div class="bg-white rounded-2xl p-6 max-w-2xl w-full shadow-2xl max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between mb-4">
              <div>
                <p class="text-xs uppercase text-gray-500 tracking-wide">Создать задачу</p>
                <h2 class="text-2xl font-semibold text-gray-900">
                  {{ projectsStore.currentProject?.key }} · Новый issue
                </h2>
              </div>
              <button class="text-gray-400 hover:text-gray-600" @click="showCreateTaskModal = false">×</button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
                <input v-model="newTask.title" type="text" class="input" placeholder="например, 'Настроить RBAC'" />
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
                <textarea v-model="newTask.description" class="input min-h-[120px]" placeholder="Расскажите детали" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Приоритет</label>
                <select v-model="newTask.priority" class="input">
                  <option value="low">Низкий</option>
                  <option value="medium">Средний</option>
                  <option value="high">Высокий</option>
                  <option value="critical">Критический</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Тип</label>
                <select v-model="newTask.type" class="input">
                  <option value="task">Задача</option>
                  <option value="bug">Ошибка</option>
                  <option value="feature">Фича</option>
                  <option value="improvement">Улучшение</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Статус</label>
                <select v-model="newTask.status" class="input">
                  <option v-for="status in statuses" :key="status.value" :value="status.value">
                    {{ status.label }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Story Points</label>
                <input v-model.number="newTask.story_points" type="number" min="0" class="input" />
              </div>
            </div>
            <div class="mt-6 flex justify-end space-x-3">
              <button class="btn btn-secondary" @click="showCreateTaskModal = false">Отмена</button>
              <button class="btn btn-primary" @click="createTask">Создать</button>
            </div>
          </div>
        </div>
      </Teleport>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useProjectsStore } from '@/stores/projects'
import { useTasksStore } from '@/stores/tasks'
import { useNotificationsStore } from '@/stores/notifications'
import { projectsApi } from '@/api/projects'
import type { Task, TaskStatus, WorkflowStatus } from '@/types'

const route = useRoute()
const router = useRouter()
const projectsStore = useProjectsStore()
const tasksStore = useTasksStore()
const notificationsStore = useNotificationsStore()

const showCreateTaskModal = ref(false)
const workflowStatuses = ref<WorkflowStatus[]>([])
const loadingWorkflow = ref(false)

const newTask = ref({
  project_id: route.params.id as string,
  title: '',
  description: '',
  priority: 'medium',
  type: 'task',
  status: 'backlog',
  story_points: undefined as number | undefined,
})

// Цвета для категорий статусов
const getStatusColor = (category: string): string => {
  const colors: Record<string, string> = {
    todo: 'bg-blue-400',
    in_progress: 'bg-yellow-400',
    done: 'bg-success-500',
  }
  return colors[category] || 'bg-gray-400'
}

// Преобразуем статусы workflow в формат для отображения
const statuses = computed(() => {
  return workflowStatuses.value.map((status) => ({
    value: status.key as TaskStatus,
    label: status.name,
    color: getStatusColor(status.category),
    order: status.order,
  })).sort((a, b) => a.order - b.order)
})

// Группировка задач по статусам
const tasksByStatus = computed(() => {
  const grouped: Record<string, Task[]> = {}
  
  statuses.value.forEach((status) => {
    grouped[status.value] = []
  })
  
  tasksStore.tasks.forEach((task) => {
    if (grouped[task.status]) {
      grouped[task.status].push(task)
    }
  })
  
  return grouped
})

let draggedTask: Task | null = null

const loadWorkflow = async (projectId: string) => {
  try {
    loadingWorkflow.value = true
    const workflow = await projectsApi.getProjectWorkflow(projectId)
    workflowStatuses.value = workflow.statuses || []

    // Устанавливаем первый статус по умолчанию для новой задачи
    if (workflowStatuses.value.length > 0) {
      newTask.value.status = workflowStatuses.value[0].key as TaskStatus
    }
  } catch (error: any) {
    console.error('Failed to load workflow:', error)
    notificationsStore.warning('Не удалось загрузить workflow, используются стандартные статусы')
    // Fallback к дефолтным статусам
    workflowStatuses.value = [
      { id: '', key: 'backlog', name: 'Бэклог', order: 0, category: 'todo' },
      { id: '', key: 'todo', name: 'К выполнению', order: 1, category: 'todo' },
      { id: '', key: 'in_progress', name: 'В работе', order: 2, category: 'in_progress' },
      { id: '', key: 'done', name: 'Выполнено', order: 3, category: 'done' },
    ]
  } finally {
    loadingWorkflow.value = false
  }
}

onMounted(async () => {
  const projectId = route.params.id as string
  try {
    await Promise.all([
      projectsStore.fetchProject(projectId),
      tasksStore.fetchTasks({ project_id: projectId }),
      loadWorkflow(projectId),
    ])
  } catch (error: any) {
    notificationsStore.error(error.message || 'Не удалось загрузить данные проекта')
  }
})

const createTask = async () => {
  if (!newTask.value.title.trim()) {
    notificationsStore.error('Введите название задачи')
    return
  }
  try {
    await tasksStore.createTask(newTask.value)
    notificationsStore.success('Задача успешно создана')
    showCreateTaskModal.value = false
    newTask.value = {
      project_id: route.params.id as string,
      title: '',
      description: '',
      priority: 'medium',
      type: 'task',
      status: workflowStatuses.value[0]?.key as TaskStatus || 'backlog',
      story_points: undefined,
    }
  } catch (error: any) {
    notificationsStore.error(error.message || 'Не удалось создать задачу')
    console.error('Failed to create task:', error)
  }
}

const handleDragStart = (event: DragEvent, task: Task) => {
  draggedTask = task
  event.dataTransfer?.setData('text/plain', task.id)
  event.dataTransfer!.effectAllowed = 'move'
}

const handleDrop = async (event: DragEvent, status: TaskStatus) => {
  event.preventDefault()
  if (draggedTask && draggedTask.status !== status) {
    try {
      await tasksStore.updateTaskStatus(draggedTask.id, status)
      notificationsStore.success('Статус задачи обновлен')
    } catch (error: any) {
      notificationsStore.error(error.message || 'Не удалось обновить статус задачи')
    }
  }
  draggedTask = null
}

const openFilters = () => {
  notificationsStore.info('Расширенные фильтры появятся в следующем релизе')
}

const viewTask = (taskId: string) => {
  router.push(`/tasks/${taskId}`)
}
</script>
