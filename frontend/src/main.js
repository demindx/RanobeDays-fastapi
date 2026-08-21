import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { useTheme } from './composables/useTheme'

import './assets/main.css'

const requiredEnvVars = ['VITE_API_BASE_URL']

for (const key of requiredEnvVars) {
  if (!import.meta.env[key]) {
    console.warn(`[RanobeDays] Missing required env variable: ${key}. Using default.`)
  }
}

const app = createApp(App)

app.config.errorHandler = (err, instance, info) => {
  console.error('[RanobeDays]', err, info)
}

app.use(router)
useTheme()

app.mount('#app')
