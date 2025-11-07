import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { tasksApi } from '@/api/tasks'
import type { Task, TaskStatus } from '@/types'

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([])
  const currentTask = ref<Task | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const tasksByStatus = computed(() => {
    const grouped: Record<TaskStatus, Task[]> = {
      backlog: [],
      todo: [],
      in_progress: [],
      review: [],
      testing: [],
      done: [],
      cancelled: [],
    }

    tasks.value.forEach((task) => {
      grouped[task.status]?.push(task)
    })

    return grouped
  })

  async function fetchTasks(filters?: any) {
    try {
      loading.value = true
      error.value = null
      tasks.value = await tasksApi.getTasks(filters)
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function fetchTask(id: string) {
    try {
      loading.value = true
      error.value = null
      currentTask.value = await tasksApi.getTask(id)
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function createTask(taskData: any) {
    try {
      loading.value = true
      error.value = null
      const newTask = await tasksApi.createTask(taskData)
      tasks.value.push(newTask)
      return newTask
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateTask(id: string, taskData: any) {
    try {
      loading.value = true
      error.value = null
      const updatedTask = await tasksApi.updateTask(id, taskData)

      const index = tasks.value.findIndex((t) => t.id === id)
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }

      if (currentTask.value?.id === id) {
        currentTask.value = updatedTask
      }

      return updatedTask
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateTaskStatus(id: string, status: TaskStatus) {
    return updateTask(id, { status })
  }

  async function deleteTask(id: string) {
    try {
      loading.value = true
      error.value = null
      await tasksApi.deleteTask(id)

      const index = tasks.value.findIndex((t) => t.id === id)
      if (index !== -1) {
        tasks.value.splice(index, 1)
      }
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    tasks,
    currentTask,
    loading,
    error,
    tasksByStatus,
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    updateTaskStatus,
    deleteTask,
  }
})
