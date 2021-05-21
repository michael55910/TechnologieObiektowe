import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import axios from 'axios'
import VueApexCharts from 'vue-apexcharts'

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

Vue.config.productionTip = false

Vue.use(BootstrapVue, BootstrapVueIcons, axios, VueApexCharts)
Vue.component('apexchart', VueApexCharts)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
