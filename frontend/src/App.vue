<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar :current="view" :connected="connected" @navigate="view = $event" />
    
    <main class="max-w-[1400px] mx-auto px-4 py-6">
      <div v-if="loading" class="flex flex-col items-center justify-center py-20">
        <div class="w-10 h-10 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p class="text-gray-500">Lade Daten...</p>
      </div>
      
      <template v-else>
        <div v-if="!connected" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <div class="flex items-center gap-2">
            <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <p class="text-yellow-800">
              <strong>Backend nicht erreichbar.</strong> Stelle sicher, dass der Backend-Server auf Port 5000 läuft.
            </p>
          </div>
        </div>
        
        <PlannerView
          v-if="view === 'planner'"
          :year="year"
          :start-week="startWeek"
          :weeks-to-show="weeksToShow"
          :plans="plans"
          :meals="meals"
          @navigate="navigate"
          @today="goToday"
          @update:weeks-to-show="changeWeeks"
          @set="setMeal"
          @clear="clearMeal"
          @move="moveMeal"
          @clear-all="confirmClearAll"
          @add-meal="showModal = true"
        />
        
        <MealsView
          v-else
          :meals="meals"
          @create="createMeal"
          @update="updateMeal"
          @delete="deleteMeal"
        />
      </template>
    </main>
    
    <AddMealModal :show="showModal" @close="showModal = false" @save="handleNewMeal" />
    
    <ConfirmDialog
      :show="showClear"
      title="Alle Wochen leeren?"
      message="Alle Einträge werden entfernt."
      confirm-text="Leeren"
      @close="showClear = false"
      @confirm="clearAll"
    />
    
    <!-- Toast -->
    <div class="fixed bottom-4 right-4 z-50">
      <div v-if="toast" class="px-4 py-3 rounded-lg shadow-lg text-white text-sm"
           :class="toast.type === 'error' ? 'bg-red-500' : 'bg-green-500'">
        {{ toast.message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from './components/NavBar.vue'
import PlannerView from './views/PlannerView.vue'
import MealsView from './views/MealsView.vue'
import AddMealModal from './components/AddMealModal.vue'
import ConfirmDialog from './components/ConfirmDialog.vue'
import { mealsApi, planApi, utilsApi } from './api'

const view = ref('planner')
const loading = ref(true)
const connected = ref(false)

const meals = ref([])
const plans = ref({})
const year = ref(2025)
const startWeek = ref(1)
const weeksToShow = ref(3)

const showModal = ref(false)
const showClear = ref(false)
const toast = ref(null)

function showToast(message, type = 'success') {
  toast.value = { message, type }
  setTimeout(() => toast.value = null, 3000)
}

async function loadMeals() {
  try {
    const res = await mealsApi.getAll()
    meals.value = res.data
  } catch (error) {
    console.error('Fehler beim Laden der Gerichte:', error)
    showToast('Fehler beim Laden der Gerichte', 'error')
    meals.value = []
  }
}

async function loadPlans() {
  try {
    const res = await planApi.getWeeks(year.value, startWeek.value, weeksToShow.value)
    plans.value = res.data
  } catch (error) {
    console.error('Fehler beim Laden der Pläne:', error)
    showToast('Fehler beim Laden der Pläne', 'error')
    plans.value = {}
  }
}

function navigate(delta) {
  let w = startWeek.value + delta
  let y = year.value
  while (w > 52) { w -= 52; y++ }
  while (w < 1) { w += 52; y-- }
  startWeek.value = w
  year.value = y
  loadPlans()
}

function goToday() {
  const now = new Date()
  year.value = now.getFullYear()
  const jan1 = new Date(year.value, 0, 1)
  startWeek.value = Math.ceil((((now - jan1) / 86400000) + jan1.getDay() + 1) / 7)
  loadPlans()
}

function changeWeeks(n) {
  weeksToShow.value = n
  loadPlans()
}

async function setMeal({ year: y, week: w, day, mealId }) {
  try {
    await planApi.setMeal(y, w, day, mealId)
    await loadPlans()
  } catch (error) {
    console.error('Fehler beim Setzen des Gerichts:', error)
    showToast('Fehler beim Setzen des Gerichts', 'error')
  }
}

async function clearMeal({ year: y, week: w, day }) {
  try {
    await planApi.clearMeal(y, w, day)
    await loadPlans()
  } catch (error) {
    console.error('Fehler beim Löschen des Gerichts:', error)
    showToast('Fehler beim Löschen', 'error')
  }
}

async function moveMeal({ year: fromY, week: fromW, day: fromD, mealId, toYear, toWeek, toDay }) {
  try {
    await planApi.setMeal(toYear, toWeek, toDay, mealId)
    await planApi.clearMeal(fromY, fromW, fromD)
    await loadPlans()
  } catch (error) {
    console.error('Fehler beim Verschieben des Gerichts:', error)
    showToast('Fehler beim Verschieben', 'error')
  }
}

function confirmClearAll() {
  showClear.value = true
}

async function clearAll() {
  try {
    await planApi.clearWeeks(year.value, startWeek.value, weeksToShow.value)
    showClear.value = false
    await loadPlans()
    showToast('Alle Wochen geleert')
  } catch (error) {
    console.error('Fehler beim Leeren der Wochen:', error)
    showToast('Fehler beim Leeren', 'error')
    showClear.value = false
  }
}

async function createMeal(name, color) {
  try {
    await mealsApi.create(name, color)
    await loadMeals()
    showToast(`"${name}" erstellt`)
  } catch (error) {
    console.error('Fehler beim Erstellen des Gerichts:', error)
    const errorMsg = error.response?.data?.error || 'Fehler beim Erstellen des Gerichts'
    showToast(errorMsg, 'error')
  }
}

async function updateMeal(id, name, color) {
  try {
    await mealsApi.update(id, name, color)
    await loadMeals()
    showToast('Gespeichert')
  } catch (error) {
    console.error('Fehler beim Aktualisieren des Gerichts:', error)
    const errorMsg = error.response?.data?.error || 'Fehler beim Speichern'
    showToast(errorMsg, 'error')
  }
}

async function deleteMeal(id) {
  try {
    await mealsApi.delete(id)
    await loadMeals()
    await loadPlans()
    showToast('Gelöscht')
  } catch (error) {
    console.error('Fehler beim Löschen des Gerichts:', error)
    showToast('Fehler beim Löschen', 'error')
  }
}

async function handleNewMeal(data) {
  await createMeal(data.name, data.color)
}

onMounted(async () => {
  try {
    await utilsApi.health()
    connected.value = true
  } catch (error) {
    console.error('Backend nicht erreichbar:', error)
    connected.value = false
  }
  
  try {
    const res = await utilsApi.getCurrentWeek()
    year.value = res.data.year
    startWeek.value = res.data.week
  } catch (error) {
    console.warn('Aktuelle Woche konnte nicht geladen werden:', error)
    // Verwende Standardwerte
  }
  
  try {
    await Promise.all([loadMeals(), loadPlans()])
  } catch (error) {
    console.error('Fehler beim Laden der Daten:', error)
  } finally {
    loading.value = false
  }
})
</script>