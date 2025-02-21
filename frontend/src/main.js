import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // 确保正确引入了 router/index.js

const app = createApp(App)
app.use(router)
app.mount('#app')