
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { useTheme } from './composables/useTheme'

import './assets/main.css'

const app = createApp(App)

app.use(router)
useTheme()

app.mount('#app')
