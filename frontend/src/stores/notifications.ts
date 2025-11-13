import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  duration?: number
}

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref<Notification[]>([])
  let idCounter = 0

  function addNotification(
    type: Notification['type'],
    message: string,
    duration: number = 4000
  ) {
    const id = `notification-${++idCounter}-${Date.now()}`
    const notification: Notification = { id, type, message, duration }

    notifications.value.push(notification)

    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, duration)
    }

    return id
  }

  function removeNotification(id: string) {
    const index = notifications.value.findIndex((n) => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }

  function success(message: string, duration?: number) {
    return addNotification('success', message, duration)
  }

  function error(message: string, duration?: number) {
    return addNotification('error', message, duration || 6000)
  }

  function warning(message: string, duration?: number) {
    return addNotification('warning', message, duration)
  }

  function info(message: string, duration?: number) {
    return addNotification('info', message, duration)
  }

  function clear() {
    notifications.value = []
  }

  return {
    notifications,
    addNotification,
    removeNotification,
    success,
    error,
    warning,
    info,
    clear,
  }
})
