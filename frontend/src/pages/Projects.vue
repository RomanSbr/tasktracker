<template>
  <AppLayout>
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">Projects</h1>
        <button @click="showCreateModal = true" class="btn btn-primary">
          Create Project
        </button>
      </div>

      <div v-if="projectsStore.loading" class="text-center py-12">
        <div class="text-gray-500">Loading projects...</div>
      </div>

      <div v-else-if="projectsStore.projects.length === 0" class="text-center py-12">
        <p class="text-gray-500 mb-4">No projects yet</p>
        <button @click="showCreateModal = true" class="btn btn-primary">
          Create Your First Project
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="project in projectsStore.projects"
          :key="project.id"
          class="card hover:shadow-lg transition-shadow cursor-pointer"
          @click="$router.push(`/projects/${project.id}/board`)"
        >
          <div class="card-body">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900">{{ project.name }}</h3>
                <p class="text-sm text-gray-500 mt-1">{{ project.key }}</p>
              </div>
              <span class="badge badge-success">{{ project.status }}</span>
            </div>
            <p v-if="project.description" class="mt-3 text-sm text-gray-600 line-clamp-2">
              {{ project.description }}
            </p>
            <div class="mt-4 flex justify-end">
              <router-link
                :to="`/projects/${project.id}/board`"
                class="text-sm text-success-600 hover:text-success-700 font-medium"
              >
                View Board →
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Project Modal (simplified for now) -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 max-w-md w-full">
          <h2 class="text-xl font-bold mb-4">Create Project</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Project Name</label>
              <input v-model="newProject.name" type="text" class="input" placeholder="My Project" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Project Key</label>
              <input v-model="newProject.key" type="text" class="input" placeholder="MP" maxlength="10" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea v-model="newProject.description" class="input" rows="3"></textarea>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button @click="showCreateModal = false" class="btn btn-secondary">Cancel</button>
            <button @click="createProject" class="btn btn-primary">Create</button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useProjectsStore } from '@/stores/projects'

const projectsStore = useProjectsStore()
const showCreateModal = ref(false)
const newProject = ref({
  name: '',
  key: '',
  description: '',
  organization_id: '00000000-0000-0000-0000-000000000001' // Default org ID for demo
})

onMounted(() => {
  projectsStore.fetchProjects()
})

const createProject = async () => {
  try {
    await projectsStore.createProject(newProject.value)
    showCreateModal.value = false
    newProject.value = {
      name: '',
      key: '',
      description: '',
      organization_id: '00000000-0000-0000-0000-000000000001'
    }
  } catch (error) {
    console.error('Failed to create project:', error)
  }
}
</script>
