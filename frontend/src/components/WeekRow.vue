<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
    <!-- Header -->
    <div 
      class="flex items-center gap-3 px-4 py-2 border-b"
      :class="isCurrent ? 'bg-primary-50 border-primary-200' : 'bg-gray-50 border-gray-200'"
    >
      <span 
        class="px-2.5 py-1 rounded-lg text-sm font-bold"
        :class="isCurrent ? 'bg-primary-500 text-white' : 'bg-gray-200 text-gray-600'"
      >
        KW {{ week }}
      </span>
      <span class="text-sm text-gray-500">{{ dateRange }}</span>
      <span v-if="isCurrent" class="text-xs bg-primary-100 text-primary-700 px-2 py-0.5 rounded-full ml-auto">
        Aktuell
      </span>
    </div>
    
    <!-- Days -->
    <div class="grid grid-cols-7 gap-2 p-3">
      <DayCell
        v-for="d in 7"
        :key="d"
        :day="d - 1"
        :meal="plan[d - 1]"
        :week-start="weekStart"
        :year="year"
        :week="week"
        @set="mealId => $emit('set', { year, week, day: d - 1, mealId })"
        @clear="$emit('clear', { year, week, day: d - 1 })"
        @move="data => $emit('move', { ...data, toYear: year, toWeek: week, toDay: d - 1 })"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import DayCell from './DayCell.vue'

const props = defineProps({
  year: Number,
  week: Number,
  plan: Object
})

defineEmits(['set', 'clear', 'move'])

const weekStart = computed(() => {
  const jan4 = new Date(props.year, 0, 4)
  const dow = jan4.getDay() || 7
  const mon = new Date(jan4)
  mon.setDate(jan4.getDate() - dow + 1 + (props.week - 1) * 7)
  return mon
})

const isCurrent = computed(() => {
  const now = new Date()
  const y = now.getFullYear()
  const jan1 = new Date(y, 0, 1)
  const days = Math.floor((now - jan1) / 86400000)
  const w = Math.ceil((days + jan1.getDay() + 1) / 7)
  return props.year === y && props.week === w
})

const dateRange = computed(() => {
  const end = new Date(weekStart.value)
  end.setDate(end.getDate() + 6)
  const fmt = d => d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit' })
  return `${fmt(weekStart.value)} – ${fmt(end)}`
})
</script>

