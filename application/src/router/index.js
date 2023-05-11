import { createRouter, createWebHashHistory } from 'vue-router'
import WelcomeView from '../views/WelcomeView.vue'
import AllegroCredntialsView from '../views/AllegroCredntialsView.vue'


const routes = [
    {
      path: '/',
      name: 'home',
      component: WelcomeView
    },
    {
      path: '/allegro-credentials',
      name: 'allegro-credentials',
      component: AllegroCredntialsView
    }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router