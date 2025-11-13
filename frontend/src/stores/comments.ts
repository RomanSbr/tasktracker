import { defineStore } from 'pinia'
import { ref } from 'vue'
import { commentsApi } from '@/api/comments'
import type { Comment } from '@/types'

export const useCommentsStore = defineStore('comments', () => {
  const comments = ref<Comment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchComments(taskId: string) {
    try {
      loading.value = true
      error.value = null
      comments.value = []
      comments.value = await commentsApi.getComments(taskId)
    } catch (err: any) {
      error.value = err.message || 'Не удалось загрузить комментарии'
    } finally {
      loading.value = false
    }
  }

  async function addComment(taskId: string, content: string) {
    const newComment = await commentsApi.createComment({ task_id: taskId, content })
    comments.value.push(newComment)
    return newComment
  }

  async function deleteComment(commentId: string) {
    await commentsApi.deleteComment(commentId)
    comments.value = comments.value.filter((c) => c.id !== commentId)
  }

  return {
    comments,
    loading,
    error,
    fetchComments,
    addComment,
    deleteComment,
  }
})
