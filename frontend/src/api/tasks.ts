import { apiClient } from './client'
import type { Task } from '@/types'

interface CreateTaskData {
  project_id: string
  title: string
  description?: string
  status?: string
  priority?: string
  type?: string
  assignee_id?: string
  due_date?: string
  estimated_hours?: number
  story_points?: number
  tags?: string[]
}

interface UpdateTaskData extends Partial<CreateTaskData> {
  logged_hours?: number
}

interface TaskFilters {
  project_id?: string
  status?: string
  assignee_id?: string
  skip?: number
  limit?: number
}

export const tasksApi = {
  async getTasks(filters?: TaskFilters): Promise<Task[]> {
    const { data } = await apiClient.get<Task[]>('/tasks', { params: filters })
    return data
  },

  async getTask(id: string): Promise<Task> {
    const { data } = await apiClient.get<Task>(`/tasks/${id}`)
    return data
  },

  async createTask(taskData: CreateTaskData): Promise<Task> {
    const { data } = await apiClient.post<Task>('/tasks', taskData)
    return data
  },

  async updateTask(id: string, taskData: UpdateTaskData): Promise<Task> {
    const { data } = await apiClient.patch<Task>(`/tasks/${id}`, taskData)
    return data
  },

  async deleteTask(id: string): Promise<void> {
    await apiClient.delete(`/tasks/${id}`)
  },

  async getTaskHistory(id: string): Promise<any[]> {
    const { data } = await apiClient.get(`/tasks/${id}/history`)
    return data
  },
}
