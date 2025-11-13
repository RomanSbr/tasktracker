<template>
  <AppLayout>
    <div v-if="tasksStore.loading" class="text-center py-12 text-gray-500">
      Загрузка задачи...
    </div>

    <div v-else-if="tasksStore.currentTask" class="space-y-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2 text-sm">
          <router-link
            :to="`/projects/${tasksStore.currentTask.project_id}/board`"
            class="text-success-600 hover:text-success-700 font-medium"
          >
            Доска проекта
          </router-link>
          <span class="text-gray-400">/</span>
          <router-link
            :to="`/projects/${tasksStore.currentTask.project_id}/backlog`"
            class="text-success-600 hover:text-success-700 font-medium"
          >
            Бэклог
          </router-link>
          <span class="text-gray-400">/</span>
          <span class="text-gray-500">Задача #{{ tasksStore.currentTask.task_number }}</span>
        </div>
        <div class="space-x-2">
          <button class="btn btn-secondary text-xs" @click="toggleDescriptionEdit">
            {{ isEditingDescription ? 'Отмена' : 'Редактировать' }}
          </button>
          <button class="btn btn-primary text-xs" @click="handleQuickDone">
            Отметить как выполнено
          </button>
        </div>
      </div>

      <div class="flex flex-col xl:flex-row gap-6">
        <section class="flex-1 space-y-6">
          <div class="card">
            <div class="card-body space-y-4">
              <div class="flex items-start justify-between">
                <div>
                  <div class="flex items-center space-x-3 mb-3">
                    <span class="text-sm font-semibold text-gray-500">#{tasksStore.currentTask.task_number}</span>
                    <span class="badge capitalize" :class="priorityClass">
                      {{ tasksStore.currentTask.priority }}
                    </span>
                    <span class="badge capitalize">
                      {{ tasksStore.currentTask.type }}
                    </span>
                  </div>
                  <h1 class="text-3xl font-semibold text-gray-900">{{ tasksStore.currentTask.title }}</h1>
                </div>
                <select v-model="localStatus" @change="updateStatus" class="input text-sm max-w-[160px]">
                  <option v-for="status in statusOptions" :key="status.value" :value="status.value">
                    {{ status.label }}
                  </option>
                </select>
              </div>
              <div>
                <div class="flex items-center justify-between mb-2">
                  <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide">Описание</h2>
                  <button class="text-xs text-success-600 hover:text-success-700" @click="toggleDescriptionEdit">
                    {{ isEditingDescription ? 'Отмена' : 'Редактировать' }}
                  </button>
                </div>
                <div v-if="isEditingDescription">
                  <textarea v-model="descriptionDraft" class="input min-h-[150px]" />
                  <div class="flex justify-end space-x-2 mt-3">
                    <button class="btn btn-secondary" @click="toggleDescriptionEdit">Отмена</button>
                    <button class="btn btn-primary" @click="saveDescription" :disabled="descriptionSaving">
                      {{ descriptionSaving ? 'Сохранение...' : 'Сохранить' }}
                    </button>
                  </div>
                </div>
                <p v-else class="text-gray-800 leading-relaxed whitespace-pre-line">
                  {{ tasksStore.currentTask.description || 'Описание отсутствует' }}
                </p>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header flex items-center justify-between">
              <h2 class="text-lg font-semibold text-gray-900">Комментарии</h2>
              <span class="text-sm text-gray-500">{{ commentsStore.comments.length }} комментариев</span>
            </div>
            <div class="card-body space-y-4">
              <div v-if="commentsStore.loading" class="text-gray-500 text-sm">Загрузка комментариев...</div>

              <div v-else>
                <div
                  v-for="comment in commentsStore.comments"
                  :key="comment.id"
                  class="border border-gray-200 rounded-lg p-4 mb-4 bg-white hover:shadow-sm transition-shadow"
                >
                  <div class="flex items-start justify-between mb-3">
                    <div class="flex items-center space-x-3">
                      <div class="w-8 h-8 rounded-full bg-success-100 flex items-center justify-center text-success-700 font-semibold text-sm">
                        {{ getInitials(comment.user_id) }}
                      </div>
                      <div>
                        <p class="text-sm font-semibold text-gray-900">
                          {{ resolveCommentAuthor(comment.user_id) }}
                        </p>
                        <p class="text-xs text-gray-500">
                          {{ formatDate(comment.created_at) }}
                          <span v-if="comment.edited" class="ml-2 italic">(отредактировано)</span>
                        </p>
                      </div>
                    </div>
                    <div class="flex items-center space-x-2">
                      <button
                        v-if="canEditComment(comment.user_id) && !editingComments[comment.id]"
                        class="text-xs text-gray-600 hover:text-gray-900"
                        @click="startEditComment(comment.id, comment.content)"
                      >
                        Редактировать
                      </button>
                      <button
                        v-if="canDeleteComment(comment.user_id)"
                        class="text-xs text-danger-600 hover:text-danger-700"
                        @click="deleteComment(comment.id)"
                      >
                        Удалить
                      </button>
                    </div>
                  </div>
                  
                  <div v-if="editingComments[comment.id]" class="space-y-2">
                    <textarea
                      v-model="editingComments[comment.id]"
                      rows="4"
                      class="input text-sm"
                      @keydown.ctrl.enter="saveComment(comment.id)"
                      @keydown.meta.enter="saveComment(comment.id)"
                    />
                    <div class="flex justify-end space-x-2">
                      <button
                        class="btn btn-secondary text-xs"
                        @click="cancelEditComment(comment.id)"
                      >
                        Отмена
                      </button>
                      <button
                        class="btn btn-primary text-xs"
                        @click="saveComment(comment.id)"
                        :disabled="!editingComments[comment.id]?.trim()"
                      >
                        Сохранить
                      </button>
                    </div>
                  </div>
                  <div v-else class="text-sm text-gray-800">
                    <MarkdownRenderer :content="comment.content" />
                  </div>
                </div>

                <div v-if="!commentsStore.comments.length" class="text-center text-gray-400 text-sm py-6">
                  Комментариев пока нет — будьте первым!
                </div>
              </div>

              <div class="border-t border-gray-200 pt-4">
                <div class="flex items-center space-x-2 mb-3">
                  <div class="w-8 h-8 rounded-full bg-success-100 flex items-center justify-center text-success-700 font-semibold text-sm">
                    {{ getCurrentUserInitials() }}
                  </div>
                  <label class="block text-sm font-medium text-gray-700">Добавить комментарий</label>
                </div>
                <textarea
                  v-model="newComment"
                  rows="4"
                  class="input text-sm"
                  placeholder="Поделитесь обновлением... (поддерживается Markdown, используйте @username для упоминаний)"
                  @keydown.ctrl.enter="submitComment"
                  @keydown.meta.enter="submitComment"
                />
                <div class="flex items-center justify-between mt-2">
                  <p class="text-xs text-gray-500">
                    Поддерживается Markdown. Используйте Ctrl+Enter для отправки
                  </p>
                  <button
                    class="btn btn-primary text-sm"
                    :disabled="!newComment.trim() || submittingComment"
                    @click="submitComment"
                  >
                    {{ submittingComment ? 'Отправка...' : 'Отправить' }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header flex items-center justify-between">
              <h2 class="text-lg font-semibold text-gray-900">История изменений</h2>
            </div>
            <div class="card-body">
              <div v-if="loadingHistory" class="text-gray-500 text-sm">Загрузка истории...</div>
              <div v-else-if="taskHistory.length === 0" class="text-center text-gray-400 text-sm py-6">
                История изменений пуста
              </div>
              <div v-else class="space-y-3">
                <div
                  v-for="entry in taskHistory"
                  :key="entry.id"
                  class="flex items-start space-x-3 pb-3 border-b border-gray-100 last:border-0"
                >
                  <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-600">
                    {{ getActionIcon(entry.action) }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm text-gray-900">
                      <span class="font-medium">{{ formatHistoryAction(entry) }}</span>
                    </p>
                    <p class="text-xs text-gray-500 mt-1">
                      {{ formatDate(entry.created_at) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <aside class="w-full xl:w-80 space-y-4">
          <div class="card">
            <div class="card-header">
              <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide">Детали</h3>
            </div>
            <div class="card-body space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">Статус</span>
                <span class="text-sm font-medium capitalize">{{ localStatusLabel }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">Исполнитель</span>
                <span class="text-sm text-gray-900">Назначение позже</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">Репортёр</span>
                <span class="text-sm text-gray-900">Скоро</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">Создана</span>
                <span class="text-sm text-gray-900">{{ formatDate(tasksStore.currentTask.created_at) }}</span>
              </div>
              <div
                v-if="tasksStore.currentTask.updated_at"
                class="flex items-center justify-between"
              >
                <span class="text-sm text-gray-500">Обновлена</span>
                <span class="text-sm text-gray-900">{{ formatDate(tasksStore.currentTask.updated_at) }}</span>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide">Оценка</h3>
            </div>
            <div class="card-body space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Story Points</span>
                <span class="text-gray-900">{{ tasksStore.currentTask.story_points ?? '—' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Оценка</span>
                <span class="text-gray-900">{{ tasksStore.currentTask.estimated_hours ?? '—' }} ч</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Затрачено</span>
                <span class="text-gray-900">{{ tasksStore.currentTask.logged_hours }} ч</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Дедлайн</span>
                <span class="text-gray-900">
                  {{ tasksStore.currentTask.due_date ? formatDate(tasksStore.currentTask.due_date) : '—' }}
                </span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { format } from 'date-fns'
import AppLayout from '@/components/layout/AppLayout.vue'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'
import { useTasksStore } from '@/stores/tasks'
import { useCommentsStore } from '@/stores/comments'
import { useAuthStore } from '@/stores/auth'
import { tasksApi } from '@/api/tasks'
import { commentsApi } from '@/api/comments'
import type { TaskStatus, TaskHistory } from '@/types'

const route = useRoute()
const tasksStore = useTasksStore()
const commentsStore = useCommentsStore()
const authStore = useAuthStore()

const localStatus = ref<TaskStatus>('backlog')
const statusOptions = [
  { value: 'backlog', label: 'Бэклог' },
  { value: 'todo', label: 'К выполнению' },
  { value: 'in_progress', label: 'В работе' },
  { value: 'review', label: 'На проверке' },
  { value: 'testing', label: 'Тестирование' },
  { value: 'done', label: 'Выполнено' },
]

const isEditingDescription = ref(false)
const descriptionDraft = ref('')
const descriptionSaving = ref(false)
const newComment = ref('')
const submittingComment = ref(false)
const editingComments = ref<Record<string, string>>({})
const taskHistory = ref<TaskHistory[]>([])
const loadingHistory = ref(false)

onMounted(() => {
  const taskId = route.params.id as string
  tasksStore.fetchTask(taskId)
})

const loadHistory = async (taskId: string) => {
  try {
    loadingHistory.value = true
    taskHistory.value = await tasksApi.getTaskHistory(taskId)
  } catch (error) {
    console.error('Failed to load history:', error)
  } finally {
    loadingHistory.value = false
  }
}

watch(
  () => tasksStore.currentTask,
  (task) => {
    if (!task) return
    localStatus.value = task.status
    descriptionDraft.value = task.description || ''
    commentsStore.fetchComments(task.id)
    loadHistory(task.id)
  },
  { immediate: true }
)

const localStatusLabel = computed(() => {
  return statusOptions.find((option) => option.value === localStatus.value)?.label || localStatus.value
})

const priorityClass = computed(() => {
  const priority = tasksStore.currentTask?.priority
  if (priority === 'critical') return 'badge-danger'
  if (priority === 'high') return 'bg-orange-100 text-orange-800'
  if (priority === 'low') return 'bg-blue-100 text-blue-800'
  return 'badge-primary'
})

const updateStatus = async () => {
  if (!tasksStore.currentTask) return
  await tasksStore.updateTaskStatus(tasksStore.currentTask.id, localStatus.value)
}

const toggleDescriptionEdit = () => {
  isEditingDescription.value = !isEditingDescription.value
  descriptionDraft.value = tasksStore.currentTask?.description || ''
}

const saveDescription = async () => {
  if (!tasksStore.currentTask) return
  descriptionSaving.value = true
  try {
    await tasksStore.updateTask(tasksStore.currentTask.id, { description: descriptionDraft.value })
    isEditingDescription.value = false
  } finally {
    descriptionSaving.value = false
  }
}

const handleQuickDone = async () => {
  if (!tasksStore.currentTask) return
  localStatus.value = 'done'
  await tasksStore.updateTaskStatus(tasksStore.currentTask.id, 'done')
}

const submitComment = async () => {
  if (!tasksStore.currentTask || !newComment.value.trim() || submittingComment.value) return
  try {
    submittingComment.value = true
    await commentsStore.addComment(tasksStore.currentTask.id, newComment.value.trim())
    newComment.value = ''
  } finally {
    submittingComment.value = false
  }
}

const startEditComment = (commentId: string, content: string) => {
  editingComments.value[commentId] = content
}

const cancelEditComment = (commentId: string) => {
  delete editingComments.value[commentId]
}

const saveComment = async (commentId: string) => {
  const content = editingComments.value[commentId]
  if (!content?.trim()) return
  
  try {
    await commentsApi.updateComment(commentId, { content: content.trim() })
    await commentsStore.fetchComments(tasksStore.currentTask!.id)
    delete editingComments.value[commentId]
  } catch (error) {
    console.error('Failed to update comment:', error)
  }
}

const deleteComment = async (commentId: string) => {
  if (!confirm('Вы уверены, что хотите удалить этот комментарий?')) return
  await commentsStore.deleteComment(commentId)
}

const canDeleteComment = (userId: string) => {
  return authStore.user?.id === userId
}

const canEditComment = (userId: string) => {
  return authStore.user?.id === userId
}

const resolveCommentAuthor = (userId: string) => {
  if (authStore.user?.id === userId) {
    const first = authStore.user.first_name
    const last = authStore.user.last_name
    if (first || last) {
      return [first, last].filter(Boolean).join(' ')
    }
    return authStore.user.username
  }
  return `Пользователь ${userId.slice(0, 6)}`
}

const getInitials = (userId: string): string => {
  if (authStore.user?.id === userId) {
    const first = authStore.user.first_name
    const last = authStore.user.last_name
    if (first && last) {
      return `${first[0]}${last[0]}`.toUpperCase()
    }
    if (first) {
      return first[0].toUpperCase()
    }
    if (authStore.user.username) {
      return authStore.user.username[0].toUpperCase()
    }
  }
  return 'U'
}

const getCurrentUserInitials = (): string => {
  if (authStore.user) {
    const first = authStore.user.first_name
    const last = authStore.user.last_name
    if (first && last) {
      return `${first[0]}${last[0]}`.toUpperCase()
    }
    if (first) {
      return first[0].toUpperCase()
    }
    if (authStore.user.username) {
      return authStore.user.username[0].toUpperCase()
    }
  }
  return 'U'
}

const formatDate = (date: string) => {
  return format(new Date(date), 'dd MMM yyyy, HH:mm')
}

const getActionIcon = (action: string): string => {
  const icons: Record<string, string> = {
    created: '✨',
    updated: '✏️',
    deleted: '🗑️',
  }
  return icons[action] || '📝'
}

const formatHistoryAction = (entry: TaskHistory): string => {
  if (entry.action === 'created') {
    return 'Задача создана'
  }
  if (entry.action === 'deleted') {
    return 'Задача удалена'
  }
  if (entry.action === 'updated' && entry.field_name) {
    const fieldLabels: Record<string, string> = {
      status: 'Статус',
      priority: 'Приоритет',
      assignee_id: 'Исполнитель',
      title: 'Название',
      description: 'Описание',
      story_points: 'Story Points',
      due_date: 'Дедлайн',
    }
    const fieldLabel = fieldLabels[entry.field_name] || entry.field_name
    if (entry.old_value && entry.new_value) {
      return `${fieldLabel} изменён с "${entry.old_value}" на "${entry.new_value}"`
    } else if (entry.new_value) {
      return `${fieldLabel} установлен в "${entry.new_value}"`
    }
    return `${fieldLabel} обновлён`
  }
  return 'Задача обновлена'
}
</script>
