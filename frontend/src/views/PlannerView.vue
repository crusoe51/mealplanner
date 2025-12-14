<template>
  <div>
    <WeekSelector :year="year" :start-week="startWeek" :weeks-to-show="weeksToShow"
      @navigate="$emit('navigate', $event)" @today="$emit('today')" @update:weeks-to-show="$emit('update:weeksToShow', $event)" />
    <div class="grid grid-cols-1 xl:grid-cols-[1fr_280px] gap-6">
      <div>
        <WeekRow v-for="w in weeks" :key="w.year+'-'+w.week" :year="w.year" :week="w.week" :plan="plans[w.year+'-'+w.week] || {}"
          @set="$emit('set', $event)" @clear="$emit('clear', $event)" @move="$emit('move', $event)" />
        <button @click="$emit('clearAll')" class="btn-secondary text-sm">Alle Wochen leeren</button>
      </div>
      <MealPool :meals="meals" @add="$emit('addMeal')" />
    </div>
  </div>
</template>
<script setup>
import { computed } from "vue"
import WeekSelector from "../components/WeekSelector.vue"
import WeekRow from "../components/WeekRow.vue"
import MealPool from "../components/MealPool.vue"
const props = defineProps({ year: Number, startWeek: Number, weeksToShow: Number, plans: Object, meals: Array })
defineEmits(["navigate", "today", "update:weeksToShow", "set", "clear", "move", "clearAll", "addMeal"])
const weeks = computed(() => { const r = []; let y = props.year, w = props.startWeek; for (let i = 0; i < props.weeksToShow; i++) { r.push({ year: y, week: w }); w++; if (w > 52) { w = 1; y++ } } return r })
</script>