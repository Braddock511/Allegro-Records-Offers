import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import VueCookies from 'vue-cookies'
import { createI18n } from 'vue-i18n'

import 'bootstrap/dist/css/bootstrap.css'

import messages from './messages.js'

const i18n = createI18n({
  locale: 'en', 
  messages,
})

const app = createApp(App)
app.use(router)
app.use(VueCookies)
app.use(i18n)
app.mount('#app')

import 'bootstrap/dist/js/bootstrap.js'
import './assets/main.scss'