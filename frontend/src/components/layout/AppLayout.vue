<template>
  <div class="min-h-screen bg-neutral-50 text-gray-900 flex flex-col">
    <TopNav />
    <div class="flex flex-1 overflow-hidden">
      <SidebarNav />
      <main class="flex-1 overflow-y-auto bg-white/60 backdrop-blur px-4 sm:px-8 py-8">
        <div class="max-w-6xl mx-auto">
          <slot />
        </div>
      </main>
    </div>
    <Notifications />
  </div>
</template>

<script setup lang="ts">
import TopNav from './TopNav.vue'
import SidebarNav from './SidebarNav.vue'
import Notifications from '@/components/common/Notifications.vue'
</script>
