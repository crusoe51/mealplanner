import axios from 'axios'

// API URL: Immer relative URL verwenden (Nginx-Proxy)
// Nginx leitet /api automatisch an backend:5000 weiter
const getApiUrl = () => {
  // Wenn VITE_API_URL explizit gesetzt ist (zur Build-Zeit), verwende diese
  // Aber nur wenn es NICHT der Standard localhost ist
  if (import.meta.env.VITE_API_URL && 
      import.meta.env.VITE_API_URL !== 'http://localhost:5000/api' &&
      !import.meta.env.VITE_API_URL.startsWith('/')) {
    console.log('📦 Using build-time API URL:', import.meta.env.VITE_API_URL)
    return import.meta.env.VITE_API_URL
  }
  
  const hostname = window.location.hostname
  const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1'
  
  // Für lokale Entwicklung (nicht Docker): direkte Verbindung
  if (isLocalhost && window.location.port === '5173') {
    // Vite Dev Server - direkte Verbindung
    const apiUrl = 'http://localhost:5000/api'
    console.log('🏠 Using localhost API URL (Dev):', apiUrl)
    return apiUrl
  }
  
  // Für Docker/Production: Immer relative URL verwenden (Nginx-Proxy)
  // Nginx leitet /api an backend:5000 weiter
  const apiUrl = '/api'
  console.log('🔄 Using Nginx proxy API URL:', apiUrl, '(hostname:', hostname, ')')
  return apiUrl
}

const API_URL = getApiUrl()

// Debug: API URL in Console ausgeben (immer, für Troubleshooting)
console.log('🔗 API URL:', API_URL)

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
})

export const mealsApi = {
  getAll: () => api.get('/meals'),
  create: (name, color) => api.post('/meals', { name, color }),
  update: (id, name, color) => api.put(`/meals/${id}`, { name, color }),
  delete: (id) => api.delete(`/meals/${id}`)
}

export const planApi = {
  getWeeks: (year, start, count) => 
    api.get(`/plan/weeks?year=${year}&start=${start}&count=${count}`),
  
  setMeal: (year, week, day, mealId) => 
    api.put(`/plan/${year}/${week}/${day}`, { meal_id: mealId }),
  
  clearMeal: (year, week, day) => 
    api.delete(`/plan/${year}/${week}/${day}`),
  
  clearWeeks: (year, start, count) =>
    api.delete(`/plan/weeks?year=${year}&start=${start}&count=${count}`)
}

export const utilsApi = {
  getCurrentWeek: () => api.get('/current-week'),
  health: () => api.get('/health')
}

