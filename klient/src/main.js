import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
//import 'zingchart/es6'; //https://www.zingchart.com/hello/create-interactive-charts-in-vue-with-zingchart
//import zingchartVue from 'zingchart-vue';
import VueFusionCharts from 'vue-fusioncharts'; //https://fusioncharts.github.io/vue-fusioncharts
import FusionCharts from 'fusioncharts';
import Charts from 'fusioncharts/fusioncharts.charts'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

//Vue.component('zingchart', zingchartVue);

Vue.use(VueFusionCharts, FusionCharts, Charts);

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
