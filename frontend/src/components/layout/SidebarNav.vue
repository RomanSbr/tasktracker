<template>
  <aside class="hidden lg:flex lg:flex-col lg:w-64 bg-gray-50 border-r border-gray-200">
    <div class="px-4 py-3 border-b border-gray-200">
      <p class="text-xs uppercase text-gray-500 tracking-wide">Навигация</p>
    </div>
    <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-6">
      <div>
        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Работа</p>
        <SidebarLink
          v-for="item in mainNav"
          :key="item.name"
          :to="item.to"
          :icon="item.icon"
          :label="item.label"
          :disabled="item.disabled"
        />
      </div>
      <div>
        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Проект</p>
        <SidebarLink
          v-for="item in projectNav"
          :key="item.name"
          :to="item.to"
          :icon="item.icon"
          :label="item.label"
          :disabled="item.disabled"
        />
      </div>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { computed, onMounted, type Component } from 'vue'
import { useRoute } from 'vue-router'
import { useProjectsStore } from '@/stores/projects'
import SidebarLink from './SidebarNavLink.vue'
import {
  HomeIcon,
  Squares2X2Icon,
  ListBulletIcon,
  ViewColumnsIcon,
  BookmarkSquareIcon,
} from '@heroicons/vue/24/outline'

const projectsStore = useProjectsStore()
const route = useRoute()

type NavItem = {
  name: string
  label: string
  to: string
  icon: Component
  disabled?: boolean
}

onMounted(() => {
  if (!projectsStore.projects.length) {
    projectsStore.fetchProjects()
  }
})

const activeProjectId = computed(() => {
  return (
    route.params.id ||
    projectsStore.currentProject?.id ||
    projectsStore.projects[0]?.id ||
    null
  )
})

const mainNav = computed<NavItem[]>(() => [
  {
    name: 'dashboard',
    label: 'Главная',
    to: '/dashboard',
    icon: HomeIcon,
  },
  {
    name: 'projects',
    label: 'Проекты',
    to: '/projects',
    icon: Squares2X2Icon,
  },
])

const projectNav = computed<NavItem[]>(() => {
  const pid = activeProjectId.value
  return [
    {
      name: 'backlog',
      label: 'Бэклог',
      to: pid ? `/projects/${pid}/backlog` : '/projects',
      icon: ListBulletIcon,
      disabled: !pid,
    },
    {
      name: 'board',
      label: 'Доска',
      to: pid ? `/projects/${pid}/board` : '/projects',
      icon: ViewColumnsIcon,
      disabled: !pid,
    },
    {
      name: 'issues',
      label: 'Задачи',
      to: '/tasks', // зарезервировано под будущий список задач
      icon: BookmarkSquareIcon,
      disabled: true,
    },
  ]
})
</script>
