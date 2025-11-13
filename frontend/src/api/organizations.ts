import { apiClient } from './client'
import type { Organization, OrganizationMember } from '@/types'

interface CreateOrganizationPayload {
  name: string
  slug: string
  description?: string
}

interface UpdateOrganizationPayload extends Partial<CreateOrganizationPayload> {
  logo_url?: string
}

interface AddMemberPayload {
  user_id: string
  role?: string
  permissions?: Record<string, string>
}

export const organizationsApi = {
  async getOrganizations(): Promise<Organization[]> {
    const { data } = await apiClient.get<Organization[]>('/organizations')
    return data
  },

  async createOrganization(payload: CreateOrganizationPayload): Promise<Organization> {
    const { data } = await apiClient.post<Organization>('/organizations', payload)
    return data
  },

  async updateOrganization(id: string, payload: UpdateOrganizationPayload): Promise<Organization> {
    const { data } = await apiClient.patch<Organization>(`/organizations/${id}`, payload)
    return data
  },

  async getMembers(id: string): Promise<OrganizationMember[]> {
    const { data } = await apiClient.get<OrganizationMember[]>(`/organizations/${id}/members`)
    return data
  },

  async addMember(id: string, payload: AddMemberPayload): Promise<void> {
    await apiClient.post(`/organizations/${id}/members`, payload)
  },
}
