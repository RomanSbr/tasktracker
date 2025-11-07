<template>
  <AppLayout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">
            {{ projectsStore.currentProject?.name || 'Board' }}
          </h1>
          <p class="text-gray-600">{{ projectsStore.currentProject?.key }}</p>
        </div>
        <button @click="showCreateTaskModal = true" class="btn btn-primary">
          Create Task
        </button>
      </div>

      <!-- Kanban Board -->
      <div v-if="tasksStore.loading" class="text-center py-12">
        <div class="text-gray-500">Loading tasks...</div>
      </div>

      <div v-else class="flex space-x-4 overflow-x-auto pb-4">
        <!-- Column for each status -->
        <div
          v-for="status in statuses"
          :key="status.value"
          class="flex-shrink-0 w-80"
        >
          <div class="bg-gray-100 rounded-lg p-4">
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-semibold text-gray-900 flex items-center">
                <span
                  class="w-3 h-3 rounded-full mr-2"
                  :class="status.color"
                ></span>
                {{ status.label }}
                <span class="ml-2 text-sm text-gray-500">
                  ({{ tasksStore.tasksByStatus[status.value]?.length || 0 }})
                </span>
              </h3>
            </div>

            <!-- Tasks -->
            <div
              class="space-y-3 min-h-[200px]"
              @drop="handleDrop($event, status.value)"
              @dragover.prevent
              @dragenter.prevent
            >
              <div
                v-for="task in tasksStore.tasksByStatus[status.value]"
                :key="task.id"
                draggable="true"
                @dragstart="handleDragStart($event, task)"
                class="bg-white rounded-lg p-4 shadow border border-gray-200 cursor-move hover:shadow-md transition-shadow"
              >
                <div class="flex items-start justify-between mb-2">
                  <span class="text-xs text-gray-500">{{ task.task_number }}</span>
                  <span
                    class="badge"
                    :class="{
                      'badge-danger': task.priority === 'critical',
                      'bg-orange-100 text-orange-800': task.priority === 'high',
                      'badge-primary': task.priority === 'medium',
                      'bg-blue-100 text-blue-800': task.priority === 'low',
                    }"
                  >
                    {{ task.priority }}
                  </span>
                </div>
                <h4 class="font-medium text-gray-900 text-sm mb-2">{{ task.title }}</h4>
                <p v-if="task.description" class="text-xs text-gray-600 line-clamp-2 mb-3">
                  {{ task.description }}
                </p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span
                      class="badge"
                      :class="{
                        'bg-purple-100 text-purple-800': task.type === 'feature',
                        'badge-danger': task.type === 'bug',
                        'badge-primary': task.type === 'task',
                        'bg-blue-100 text-blue-800': task.type === 'improvement',
                      }"
                    >
                      {{ task.type }}
                    </span>
                  </div>
                  <button
                    @click="viewTask(task.id)"
                    class="text-xs text-success-600 hover:text-success-700"
                  >
                    View
                  </button>
                </div>
              </div>

              <div
                v-if="!tasksStore.tasksByStatus[status.value]?.length"
                class="text-center py-8 text-gray-400 text-sm"
              >
                Drop tasks here
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Task Modal -->
      <div v-if="showCreateTaskModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <h2 class="text-xl font-bold mb-4">Create Task</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
              <input v-model="newTask.title" type="text" class="input" placeholder="Task title" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea v-model="newTask.description" class="input" rows="4"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                <select v-model="newTask.priority" class="input">
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
                <select v-model="newTask.type" class="input">
                  <option value="task">Task</option>
                  <option value="bug">Bug</option>
                  <option value="feature">Feature</option>
                  <option value="improvement">Improvement</option>
                </select>
              </div>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button @click="showCreateTaskModal = false" class="btn btn-secondary">Cancel</button>
            <button @click="createTask" class="btn btn-primary">Create</button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useProjectsStore } from '@/stores/projects'
import { useTasksStore } from '@/stores/tasks'
import type { Task, TaskStatus } from '@/types'

const route = useRoute()
const router = useRouter()
const projectsStore = useProjectsStore()
const tasksStore = useTasksStore()

const showCreateTaskModal = ref(false)
const newTask = ref({
  project_id: route.params.id as string,
  title: '',
  description: '',
  priority: 'medium',
  type: 'task',
  status: 'backlog',
})

const statuses = [
  { value: 'backlog', label: 'Backlog', color: 'bg-gray-400' },
  { value: 'todo', label: 'To Do', color: 'bg-blue-400' },
  { value: 'in_progress', label: 'In Progress', color: 'bg-yellow-400' },
  { value: 'review', label: 'Review', color: 'bg-purple-400' },
  { value: 'testing', label: 'Testing', color: 'bg-orange-400' },
  { value: 'done', label: 'Done', color: 'bg-success-500' },
]

let draggedTask: Task | null = null

onMounted(() => {
  const projectId = route.params.id as string
  projectsStore.fetchProject(projectId)
  tasksStore.fetchTasks({ project_id: projectId })
})

const createTask = async () => {
  try {
    await tasksStore.createTask(newTask.value)
    showCreateTaskModal.value = false
    newTask.value = {
      project_id: route.params.id as string,
      title: '',
      description: '',
      priority: 'medium',
      type: 'task',
      status: 'backlog',
    }
  } catch (error) {
    console.error('Failed to create task:', error)
  }
}

const handleDragStart = (event: DragEvent, task: Task) => {
  draggedTask = task
  event.dataTransfer!.effectAllowed = 'move'
}

const handleDrop = async (event: DragEvent, status: string) => {
  event.preventDefault()
  if (draggedTask && draggedTask.status !== status) {
    await tasksStore.updateTaskStatus(draggedTask.id, status as TaskStatus)
  }
  draggedTask = null
}

const viewTask = (taskId: string) => {
  router.push(`/tasks/${taskId}`)
}
</script>
