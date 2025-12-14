<template>
  <div class="max-w-2xl mx-auto">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <h2 class="text-2xl font-bold">Gerichte verwalten</h2>
      <button @click="openAdd" class="btn-primary min-h-[44px] touch-manipulation">+ Neues Gericht</button>
    </div>
    <input v-model="search" type="text" placeholder="Suchen..." class="input mb-6" />
    <div class="space-y-2">
      <div v-for="meal in filtered" :key="meal.id" class="group bg-white rounded-xl border p-4 flex items-center gap-4">
        <div class="w-3 h-10 rounded-full flex-shrink-0" :style="{ backgroundColor: meal.color }"></div>
        <span class="flex-1 font-medium min-w-0">{{ meal.name }}</span>
        <div class="flex items-center gap-2 flex-shrink-0">
          <button 
            @click.stop="openEdit(meal)" 
            class="p-2.5 min-w-[44px] min-h-[44px] flex items-center justify-center text-gray-400 hover:text-primary-500 
                   active:bg-primary-50 rounded-lg transition-colors touch-manipulation
                   opacity-100 md:opacity-0 md:group-hover:opacity-100"
            aria-label="Gericht bearbeiten"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button 
            @click.stop="confirmDel(meal)" 
            class="p-2.5 min-w-[44px] min-h-[44px] flex items-center justify-center text-gray-400 hover:text-red-500 
                   active:bg-red-50 rounded-lg transition-colors touch-manipulation
                   opacity-100 md:opacity-0 md:group-hover:opacity-100"
            aria-label="Gericht löschen"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    <AddMealModal :show="showModal" :edit-meal="editMeal" @close="showModal = false" @save="handleSave" />
    <ConfirmDialog :show="showDel" title="Loeschen?" message="Gericht wird entfernt." @close="showDel = false" @confirm="handleDel" />
  </div>
</template>
<script setup>
import { ref, computed } from "vue"
import AddMealModal from "../components/AddMealModal.vue"
import ConfirmDialog from "../components/ConfirmDialog.vue"
const props = defineProps({ meals: Array })
const emit = defineEmits(["create", "update", "delete"])
const search = ref("")
const showModal = ref(false)
const editMeal = ref(null)
const showDel = ref(false)
const delTarget = ref(null)
const filtered = computed(() => { if (!search.value) return props.meals; return props.meals.filter(m => m.name.toLowerCase().includes(search.value.toLowerCase())) })
function openAdd() { editMeal.value = null; showModal.value = true }
function openEdit(m) { editMeal.value = m; showModal.value = true }
function confirmDel(m) { delTarget.value = m; showDel.value = true }
function handleSave(d) { if (d.id) emit("update", d.id, d.name, d.color); else emit("create", d.name, d.color) }
function handleDel() { emit("delete", delTarget.value.id); showDel.value = false }
</script>

<style scoped>
.touch-manipulation {
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}
</style>