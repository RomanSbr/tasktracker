import { defineStore } from 'pinia'
import { ref } from 'vue'
import { organizationsApi } from '@/api/organizations'
import type { Organization, OrganizationMember } from '@/types'

export const useOrganizationsStore = defineStore('organizations', () => {
  const organizations = ref<Organization[]>([])
  const currentOrganization = ref<Organization | null>(null)
  const members = ref<OrganizationMember[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchOrganizations(reload = false) {
    if (organizations.value.length && !reload) {
      return
    }
    try {
      loading.value = true
      error.value = null
      organizations.value = await organizationsApi.getOrganizations()
      if (!currentOrganization.value && organizations.value.length) {
        currentOrganization.value = organizations.value[0]
      } else if (
        currentOrganization.value &&
        !organizations.value.find((org) => org.id === currentOrganization.value?.id)
      ) {
        currentOrganization.value = organizations.value[0] || null
      }
    } catch (err: any) {
      error.value = err.message || 'Не удалось загрузить организации'
    } finally {
      loading.value = false
    }
  }

  async function selectOrganization(id: string) {
    const target = organizations.value.find((org) => org.id === id)
    if (target) {
      currentOrganization.value = target
      members.value = []
    }
  }

  async function createOrganization(payload: { name: string; slug: string; description?: string }) {
    loading.value = true
    try {
      const org = await organizationsApi.createOrganization(payload)
      organizations.value.unshift(org)
      currentOrganization.value = org
      return org
    } finally {
      loading.value = false
    }
  }

  async function fetchMembers() {
    if (!currentOrganization.value) return
    members.value = await organizationsApi.getMembers(currentOrganization.value.id)
  }

  return {
    organizations,
    currentOrganization,
    members,
    loading,
    error,
    fetchOrganizations,
    selectOrganization,
    createOrganization,
    fetchMembers,
  }
})
