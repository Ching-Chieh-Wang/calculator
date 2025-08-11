import { createRouter, createWebHistory } from 'vue-router'
import Calculator from '../views/Calculator.vue'

const routes = [
  { path: '/', name: 'Calculator', component: Calculator },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router