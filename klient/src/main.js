import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import VueApexCharts from 'vue-apexcharts'

Vue.config.productionTip = false

Vue.use(BootstrapVue, BootstrapVueIcons, VueApexCharts)
Vue.component('apexchart', VueApexCharts)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
