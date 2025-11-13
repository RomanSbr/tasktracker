<template>
  <AppLayout>
    <div class="space-y-6">
      <div class="flex justify-between items-center flex-wrap gap-3">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Проекты</h1>
          <p class="text-gray-500" v-if="organizationsStore.currentOrganization">
            {{ organizationsStore.currentOrganization.name }}
          </p>
        </div>
        <div class="flex items-center space-x-3">
          <button @click="showCreateOrgModal = true" class="btn btn-secondary">
            Новый workspace
          </button>
          <button @click="openProjectModal" class="btn btn-primary" :disabled="!organizationsStore.currentOrganization">
            Создать проект
          </button>
        </div>
      </div>

      <div v-if="organizationsStore.loading" class="text-center py-12 text-gray-500">
        Загрузка рабочих областей...
      </div>

      <div
        v-else-if="!organizationsStore.organizations.length"
        class="text-center py-16 border border-dashed border-gray-300 rounded-xl bg-white"
      >
        <h2 class="text-xl font-semibold text-gray-900 mb-2">Рабочие области отсутствуют</h2>
        <p class="text-gray-500 mb-6 max-w-xl mx-auto">
          Создайте организацию, чтобы начать вести проекты и задачи. Каждый workspace хранит свои проекты, участников и настройки.
        </p>
        <button class="btn btn-primary" @click="showCreateOrgModal = true">
          Создать workspace
        </button>
      </div>

      <div v-else-if="projectsStore.loading" class="text-center py-12">
        <div class="text-gray-500">Загрузка проектов...</div>
      </div>

      <div v-else-if="projectsStore.projects.length === 0" class="text-center py-12">
        <p class="text-gray-500 mb-4">Проектов пока нет</p>
        <button @click="showCreateModal = true" class="btn btn-primary">
          Создать первый проект
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
                Открыть доску →
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Project Modal -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 max-w-md w-full">
          <h2 class="text-xl font-bold mb-4">Создать проект</h2>
          <div class="space-y-4">
            <div v-if="organizationsStore.currentOrganization">
              <label class="block text-sm font-medium text-gray-700 mb-1">Рабочая область</label>
              <p class="text-sm text-gray-600">{{ organizationsStore.currentOrganization.name }}</p>
            </div>
            <div v-else class="text-sm text-danger-600">
              Нет выбранной рабочей области
            </div>
            <div class="mt-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Название проекта</label>
              <input v-model="newProject.name" type="text" class="input" placeholder="Мой проект" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Ключ проекта</label>
              <input v-model="newProject.key" type="text" class="input" placeholder="МП" maxlength="10" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
              <textarea v-model="newProject.description" class="input" rows="3"></textarea>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button @click="showCreateModal = false" class="btn btn-secondary">Отмена</button>
            <button @click="createProject" class="btn btn-primary">Создать</button>
          </div>
        </div>
      </div>

      <!-- Create Organization Modal -->
      <div v-if="showCreateOrgModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-6 max-w-md w-full">
          <h2 class="text-xl font-bold mb-4">Новая рабочая область</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
              <input v-model="newOrganization.name" type="text" class="input" placeholder="Product Team" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Slug</label>
              <input v-model="newOrganization.slug" type="text" class="input" placeholder="product-team" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
              <textarea v-model="newOrganization.description" class="input" rows="3"></textarea>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button @click="showCreateOrgModal = false" class="btn btn-secondary">Отмена</button>
            <button @click="createOrganization" class="btn btn-primary">Создать</button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useProjectsStore } from '@/stores/projects'
import { useOrganizationsStore } from '@/stores/organizations'
import { useNotificationsStore } from '@/stores/notifications'

const projectsStore = useProjectsStore()
const organizationsStore = useOrganizationsStore()
const notificationsStore = useNotificationsStore()
const showCreateModal = ref(false)
const showCreateOrgModal = ref(false)
const newProject = ref({
  name: '',
  key: '',
  description: '',
  organization_id: ''
})
const newOrganization = ref({
  name: '',
  slug: '',
  description: ''
})

const initData = async () => {
  await organizationsStore.fetchOrganizations()
  if (organizationsStore.currentOrganization?.id) {
    newProject.value.organization_id = organizationsStore.currentOrganization.id
    projectsStore.fetchProjects(organizationsStore.currentOrganization.id)
  }
}

onMounted(() => {
  initData()
})

watch(
  () => organizationsStore.currentOrganization?.id,
  (newId) => {
    if (newId) {
      newProject.value.organization_id = newId
      projectsStore.fetchProjects(newId)
    }
  }
)

const openProjectModal = () => {
  if (!organizationsStore.currentOrganization) {
    showCreateOrgModal.value = true
    return
  }
  showCreateModal.value = true
}

const createProject = async () => {
  try {
    if (!newProject.value.name.trim()) {
      notificationsStore.error('Введите название проекта')
      return
    }
    if (!newProject.value.key.trim()) {
      notificationsStore.error('Введите ключ проекта')
      return
    }
    if (!newProject.value.organization_id) {
      notificationsStore.error('Выберите рабочую область')
      return
    }

    await projectsStore.createProject(newProject.value)
    notificationsStore.success('Проект успешно создан')
    showCreateModal.value = false
    newProject.value = {
      name: '',
      key: '',
      description: '',
      organization_id: organizationsStore.currentOrganization?.id || ''
    }
  } catch (error: any) {
    notificationsStore.error(error.message || 'Не удалось создать проект')
    console.error('Failed to create project:', error)
  }
}

const createOrganization = async () => {
  try {
    if (!newOrganization.value.name.trim()) {
      notificationsStore.error('Введите название организации')
      return
    }
    if (!newOrganization.value.slug.trim()) {
      notificationsStore.error('Введите slug организации')
      return
    }

    await organizationsStore.createOrganization(newOrganization.value)
    notificationsStore.success('Организация успешно создана')
    showCreateOrgModal.value = false
    newOrganization.value = {
      name: '',
      slug: '',
      description: ''
    }
  } catch (error: any) {
    notificationsStore.error(error.message || 'Не удалось создать организацию')
    console.error('Failed to create organization:', error)
  }
}
</script>
