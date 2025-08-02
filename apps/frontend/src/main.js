import { createSSRApp } from 'vue'
import App from './App.vue'
import pinia from './store'
import uviewPlus from 'uview-plus'

export function createApp() {
  const app = createSSRApp(App)
  
  // 使用Pinia状态管理
  app.use(pinia)
  
  // 使用uView组件库
  app.use(uviewPlus)
  
  return {
    app
  }
}
