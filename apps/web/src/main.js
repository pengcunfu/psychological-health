import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

// 创建Vue应用实例
const app = createApp(App)

// 使用插件
app.use(router)
app.use(Antd)

// 挂载应用
app.mount('#app')
