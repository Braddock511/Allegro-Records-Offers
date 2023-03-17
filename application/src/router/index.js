import { createRouter, createWebHashHistory } from 'vue-router'
import WelcomeView from '../views/WelcomeView.vue'
import ListingView from '../views/ListingView.vue'
import EditView from '../views/EditView.vue'
import StatsView from '../views/StatsView.vue'
import AllegroCredntialsView from '../views/AllegroCredntialsView.vue'


const routes = [
    {
      path: '/',
      name: 'home',
      component: WelcomeView
    },
    {
      path: '/listing',
      name: 'listing',
      component: ListingView
    },
    {
      path: '/edit',
      name: 'edit',
      component: EditView
    },
    {
      path: '/stats',
      name: 'stats',
      component: StatsView
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