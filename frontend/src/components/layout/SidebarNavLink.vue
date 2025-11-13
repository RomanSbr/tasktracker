<template>
  <router-link
    :to="to"
    class="flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors"
    :class="[
      isActive ? 'bg-white text-success-700 shadow-sm border border-success-100' : 'text-gray-600 hover:bg-white hover:text-gray-900',
      disabled ? 'pointer-events-none opacity-50' : '',
    ]"
  >
    <component :is="icon" class="w-4 h-4" />
    <span>{{ label }}</span>
  </router-link>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

interface Props {
  to: string
  label: string
  icon: any
  disabled?: boolean
}

const props = defineProps<Props>()
const route = useRoute()

const isActive = computed(() => route.path === props.to)
</script>
