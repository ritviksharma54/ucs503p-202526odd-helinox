import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/candidate',
      name: 'candidate',
      component: () => import('../views/CandidateView.vue')
    },
    {
      path: '/hr',
      name: 'hr',
      component: () => import('../views/HRView.vue')
    }
  ]
})

export default router
