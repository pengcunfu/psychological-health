import App from './App'

// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
  ...App
})
app.$mount()
// #endif
import uviewPlus from 'uview-plus'
// #ifdef VUE3
import { createSSRApp } from 'vue'
import * as Pinia from 'pinia'
export function createApp() {
  const app = createSSRApp(App)
  app.use(uviewPlus)
  app.use(Pinia.createPinia())
  return {
    app,
    Pinia
  }
}
// #endif