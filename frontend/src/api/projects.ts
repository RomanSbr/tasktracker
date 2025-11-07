import { apiClient } from './client'
import type { Project } from '@/types'

interface CreateProjectData {
  organization_id: string
  name: string
  key: string
  description?: string
  start_date?: string
  end_date?: string
  budget?: number
}

interface UpdateProjectData extends Partial<Omit<CreateProjectData, 'organization_id'>> {
  status?: string
}

export const projectsApi = {
  async getProjects(organizationId?: string): Promise<Project[]> {
    const { data } = await apiClient.get<Project[]>('/projects', {
      params: organizationId ? { organization_id: organizationId } : undefined,
    })
    return data
  },

  async getProject(id: string): Promise<Project> {
    const { data } = await apiClient.get<Project>(`/projects/${id}`)
    return data
  },

  async createProject(projectData: CreateProjectData): Promise<Project> {
    const { data } = await apiClient.post<Project>('/projects', projectData)
    return data
  },

  async updateProject(id: string, projectData: UpdateProjectData): Promise<Project> {
    const { data } = await apiClient.patch<Project>(`/projects/${id}`, projectData)
    return data
  },

  async deleteProject(id: string): Promise<void> {
    await apiClient.delete(`/projects/${id}`)
  },
}
