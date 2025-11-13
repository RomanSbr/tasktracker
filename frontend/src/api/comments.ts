import { apiClient } from './client'
import type { Comment } from '@/types'

interface CreateCommentPayload {
  task_id: string
  content: string
  parent_comment_id?: string
}

interface UpdateCommentPayload {
  content: string
}

export const commentsApi = {
  async getComments(taskId: string) {
    const { data } = await apiClient.get<Comment[]>('/comments', {
      params: { task_id: taskId, limit: 100 },
    })
    return data
  },

  async createComment(payload: CreateCommentPayload) {
    const { data } = await apiClient.post<Comment>('/comments', payload)
    return data
  },

  async updateComment(id: string, payload: UpdateCommentPayload) {
    const { data } = await apiClient.patch<Comment>(`/comments/${id}`, payload)
    return data
  },

  async deleteComment(id: string) {
    await apiClient.delete(`/comments/${id}`)
  },
}
