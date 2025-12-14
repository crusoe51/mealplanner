<template>
  <div class="bg-white rounded-xl shadow-sm p-4 mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
    <div class="flex items-center gap-2">
      <button @click="$emit('navigate', -weeksToShow)" class="btn-icon">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      
      <button @click="$emit('today')" class="btn-secondary text-sm px-3 py-1.5 min-h-[44px]">
        Heute
      </button>
      
      <button @click="$emit('navigate', weeksToShow)" class="btn-icon">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
    
    <div class="text-center">
      <div class="text-lg font-bold text-gray-900">KW {{ startWeek }} – KW {{ endWeek }}</div>
      <div class="text-sm text-gray-500">{{ dateRange }}</div>
    </div>
    
    <div class="flex items-center gap-2">
      <span class="text-sm text-gray-500">Wochen:</span>
      <div class="flex rounded-lg border border-gray-300 overflow-hidden">
        <button
          v-for="n in [2, 3]"
          :key="n"
          @click="$emit('update:weeksToShow', n)"
          class="px-3 py-1.5 min-h-[44px] text-sm font-medium transition-colors touch-manipulation"
          :class="weeksToShow === n 
            ? 'bg-primary-500 text-white active:bg-primary-600' 
            : 'bg-white text-gray-600 hover:bg-gray-50 active:bg-gray-100'"
        >
          {{ n }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  year: Number,
  startWeek: Number,
  weeksToShow: Number
})

defineEmits(['navigate', 'today', 'update:weeksToShow'])

const endWeek = computed(() => {
  let w = props.startWeek + props.weeksToShow - 1
  return w > 52 ? w - 52 : w
})

const dateRange = computed(() => {
  const getMonday = (y, w) => {
    const jan4 = new Date(y, 0, 4)
    const dow = jan4.getDay() || 7
    const mon = new Date(jan4)
    mon.setDate(jan4.getDate() - dow + 1 + (w - 1) * 7)
    return mon
  }
  
  const start = getMonday(props.year, props.startWeek)
  const end = getMonday(props.year, props.startWeek + props.weeksToShow - 1)
  end.setDate(end.getDate() + 6)
  
  const fmt = d => d.toLocaleDateString('de-DE', { day: '2-digit', month: 'short' })
  return `${fmt(start)} – ${fmt(end)} ${end.getFullYear()}`
})
</script>

