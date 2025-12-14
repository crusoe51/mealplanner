<template>
  <header class="bg-white shadow-sm sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 bg-primary-500 rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <h1 class="text-lg font-bold text-gray-900">Essensplan</h1>
      </div>
      
      <nav class="flex items-center gap-1">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="$emit('navigate', tab.id)"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          :class="current === tab.id 
            ? 'bg-primary-100 text-primary-700' 
            : 'text-gray-600 hover:bg-gray-100'"
        >
          {{ tab.label }}
        </button>
      </nav>
      
      <div class="flex items-center gap-2 text-sm text-gray-500">
        <span class="w-2 h-2 rounded-full" :class="connected ? 'bg-green-500' : 'bg-red-500'"></span>
        <span class="hidden sm:inline">{{ connected ? 'Online' : 'Offline' }}</span>
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  current: String,
  connected: Boolean
})

defineEmits(['navigate'])

const tabs = [
  { id: 'planner', label: 'Wochenplan' },
  { id: 'meals', label: 'Gerichte' }
]
</script>

