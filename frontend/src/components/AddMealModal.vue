<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
      
      <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-6">
          {{ editMeal ? 'Gericht bearbeiten' : 'Neues Gericht' }}
        </h2>
        
        <form @submit.prevent="save">
          <!-- Name -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input
              ref="nameInput"
              v-model="name"
              type="text"
              required
              class="input"
              placeholder="z.B. Spaghetti Bolognese"
            />
          </div>
          
          <!-- Color -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Farbe</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="c in colors"
                :key="c"
                type="button"
                @click="color = c"
                class="w-11 h-11 min-w-[44px] min-h-[44px] rounded-lg border-2 transition-all 
                       hover:scale-110 active:scale-95 touch-manipulation"
                :class="color === c ? 'border-gray-900 scale-110 ring-2 ring-offset-2 ring-gray-400' : 'border-transparent'"
                :style="{ backgroundColor: c }"
                :aria-label="`Farbe ${c} auswählen`"
              ></button>
            </div>
          </div>
          
          <!-- Actions -->
          <div class="flex flex-col sm:flex-row justify-end gap-3">
            <button type="button" @click="$emit('close')" class="btn-secondary min-h-[44px]">
              Abbrechen
            </button>
            <button type="submit" class="btn-primary min-h-[44px]" :disabled="!name.trim()">
              {{ editMeal ? 'Speichern' : 'Erstellen' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  show: Boolean,
  editMeal: Object
})

const emit = defineEmits(['close', 'save'])

const colors = ['#EF4444', '#F97316', '#F59E0B', '#22C55E', '#14B8A6', '#3B82F6', '#8B5CF6', '#EC4899']

const name = ref('')
const color = ref('#3B82F6')
const nameInput = ref(null)

watch(() => props.show, async (val) => {
  if (val) {
    if (props.editMeal) {
      name.value = props.editMeal.name
      color.value = props.editMeal.color
    } else {
      name.value = ''
      color.value = '#3B82F6'
    }
    await nextTick()
    nameInput.value?.focus()
  }
})

function save() {
  if (!name.value.trim()) return
  emit('save', { 
    id: props.editMeal?.id, 
    name: name.value.trim(), 
    color: color.value 
  })
  emit('close')
}
</script>

