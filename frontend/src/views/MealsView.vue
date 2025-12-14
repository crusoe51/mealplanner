<template>
  <div class="max-w-2xl mx-auto">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold">Gerichte verwalten</h2>
      <button @click="openAdd" class="btn-primary">+ Neues Gericht</button>
    </div>
    <input v-model="search" type="text" placeholder="Suchen..." class="input mb-6" />
    <div class="space-y-2">
      <div v-for="meal in filtered" :key="meal.id" class="group bg-white rounded-xl border p-4 flex items-center gap-4">
        <div class="w-3 h-10 rounded-full" :style="{ backgroundColor: meal.color }"></div>
        <span class="flex-1 font-medium">{{ meal.name }}</span>
        <button @click="openEdit(meal)" class="p-2 text-gray-400 hover:text-primary-500 opacity-0 group-hover:opacity-100">Edit</button>
        <button @click="confirmDel(meal)" class="p-2 text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100">Del</button>
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