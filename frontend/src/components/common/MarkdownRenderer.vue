<template>
  <div class="markdown-content prose prose-sm max-w-none" v-html="renderedContent"></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps<{
  content: string
}>()

const renderedContent = computed(() => {
  if (!props.content) return ''
  
  // Обработка упоминаний @username
  let processed = props.content.replace(/@(\w+)/g, '<span class="mention">@$1</span>')
  
  // Рендеринг markdown
  return marked(processed, {
    breaks: true,
    gfm: true,
  })
})
</script>

<style scoped>
.markdown-content :deep(p) {
  margin: 0.5em 0;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.markdown-content :deep(code) {
  background-color: #f3f4f6;
  padding: 0.125em 0.25em;
  border-radius: 0.25em;
  font-size: 0.9em;
}

.markdown-content :deep(pre) {
  background-color: #f3f4f6;
  padding: 0.75em;
  border-radius: 0.5em;
  overflow-x: auto;
  margin: 0.5em 0;
}

.markdown-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
}

.markdown-content :deep(blockquote) {
  border-left: 3px solid #e5e7eb;
  padding-left: 1em;
  margin: 0.5em 0;
  color: #6b7280;
}

.markdown-content :deep(a) {
  color: #10b981;
  text-decoration: underline;
}

.markdown-content :deep(.mention) {
  background-color: #dbeafe;
  color: #1e40af;
  padding: 0.125em 0.25em;
  border-radius: 0.25em;
  font-weight: 500;
}
</style>

