import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

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

