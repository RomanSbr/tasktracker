import { defineStore } from 'pinia'
import { ref } from 'vue'
import { projectsApi } from '@/api/projects'
import type { Project } from '@/types'

export const useProjectsStore = defineStore('projects', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchProjects(organizationId?: string) {
    try {
      loading.value = true
      error.value = null
      projects.value = await projectsApi.getProjects(organizationId)
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function fetchProject(id: string) {
    try {
      loading.value = true
      error.value = null
      currentProject.value = await projectsApi.getProject(id)
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function createProject(projectData: any) {
    try {
      loading.value = true
      error.value = null
      const newProject = await projectsApi.createProject(projectData)
      projects.value.push(newProject)
      return newProject
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateProject(id: string, projectData: any) {
    try {
      loading.value = true
      error.value = null
      const updatedProject = await projectsApi.updateProject(id, projectData)

      const index = projects.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        projects.value[index] = updatedProject
      }

      if (currentProject.value?.id === id) {
        currentProject.value = updatedProject
      }

      return updatedProject
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteProject(id: string) {
    try {
      loading.value = true
      error.value = null
      await projectsApi.deleteProject(id)

      const index = projects.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        projects.value.splice(index, 1)
      }
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    projects,
    currentProject,
    loading,
    error,
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
  }
})
