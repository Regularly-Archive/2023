import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import './mock'
import router from './route'

Vue.config.productionTip = false

Vue.prototype.$http = axios

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
