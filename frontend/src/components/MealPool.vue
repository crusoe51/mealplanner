<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 sticky top-20">
    <!-- Header -->
    <div class="p-4 border-b border-gray-100">
      <div class="flex items-center justify-between mb-3">
        <h3 class="font-semibold text-gray-900">Gerichte</h3>
        <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
          {{ meals.length }}
        </span>
      </div>
      
      <!-- Search -->
      <div class="relative">
        <input
          v-model="search"
          type="text"
          placeholder="Suchen..."
          class="input text-sm pl-9 py-2"
        />
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
    </div>
    
    <!-- List -->
    <div class="p-2 max-h-[calc(100vh-300px)] overflow-y-auto">
      <div class="space-y-1.5">
        <div
          v-for="meal in filtered"
          :key="meal.id"
          class="p-2.5 bg-white border border-gray-200 rounded-lg cursor-grab 
                 hover:border-primary-300 hover:shadow-sm transition-all
                 active:cursor-grabbing active:shadow-md"
          :style="{ borderLeftColor: meal.color, borderLeftWidth: '4px' }"
          draggable="true"
          @dragstart="e => onDrag(e, meal)"
        >
          <span class="text-sm font-medium text-gray-800">{{ meal.name }}</span>
        </div>
      </div>
      
      <div v-if="filtered.length === 0" class="py-8 text-center text-gray-400 text-sm">
        Keine Gerichte gefunden
      </div>
    </div>
    
    <!-- Add Button -->
    <div class="p-3 border-t border-gray-100">
      <button @click="$emit('add')" class="w-full btn-primary text-sm py-2">
        + Neues Gericht
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  meals: Array
})

defineEmits(['add'])

const search = ref('')

const filtered = computed(() => {
  if (!search.value) return props.meals
  const q = search.value.toLowerCase()
  return props.meals.filter(m => m.name.toLowerCase().includes(q))
})

function onDrag(e, meal) {
  e.dataTransfer.setData('application/json', JSON.stringify({
    type: 'new',
    mealId: meal.id
  }))
}
</script>

