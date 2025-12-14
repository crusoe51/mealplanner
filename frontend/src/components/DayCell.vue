<template>
  <div 
    class="day-cell rounded-lg border-2 overflow-hidden transition-all"
    :class="isToday ? 'border-primary-500 shadow-md' : 'border-gray-200'"
  >
    <!-- Header -->
    <div 
      class="text-center py-1.5"
      :class="isToday ? 'bg-primary-500 text-white' : isWeekend ? 'bg-gray-100 text-gray-400' : 'bg-gray-50 text-gray-600'"
    >
      <div class="text-xs font-medium">{{ dayName }}</div>
      <div class="text-lg font-bold leading-none">{{ dayNumber }}</div>
    </div>
    
    <!-- Drop Zone -->
    <div 
      class="p-2 min-h-[70px] transition-colors"
      :class="isDragOver ? 'bg-primary-50' : meal ? 'bg-white' : 'bg-gray-50'"
      @dragover.prevent="isDragOver = true"
      @dragleave="isDragOver = false"
      @drop="onDrop"
    >
      <!-- Meal -->
      <div 
        v-if="meal"
        class="group relative p-2 rounded-lg border-l-4 bg-white shadow-sm cursor-grab active:cursor-grabbing"
        :style="{ borderColor: meal.color }"
        draggable="true"
        @dragstart="onDragStart"
      >
        <span class="text-sm font-medium text-gray-800 line-clamp-2">{{ meal.name }}</span>
        
        <button
          @click="$emit('clear')"
          class="absolute -top-1.5 -right-1.5 w-5 h-5 bg-red-500 text-white rounded-full 
                 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- Empty -->
      <div v-else class="h-full flex items-center justify-center text-gray-300">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  day: Number,
  meal: Object,
  weekStart: Date,
  year: Number,
  week: Number
})

const emit = defineEmits(['set', 'clear', 'move'])

const isDragOver = ref(false)
const days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

const date = computed(() => {
  const d = new Date(props.weekStart)
  d.setDate(d.getDate() + props.day)
  return d
})

const dayName = computed(() => days[props.day])
const dayNumber = computed(() => date.value.getDate())
const isWeekend = computed(() => props.day >= 5)
const isToday = computed(() => date.value.toDateString() === new Date().toDateString())

function onDragStart(e) {
  e.dataTransfer.setData('application/json', JSON.stringify({
    type: 'move',
    year: props.year,
    week: props.week,
    day: props.day,
    mealId: props.meal.id
  }))
}

function onDrop(e) {
  isDragOver.value = false
  const data = JSON.parse(e.dataTransfer.getData('application/json'))
  
  if (data.type === 'new') {
    emit('set', data.mealId)
  } else if (data.type === 'move') {
    emit('move', data)
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

