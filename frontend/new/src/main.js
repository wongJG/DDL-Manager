import BootstrapVue from 'bootstrap-vue';
import datePicker from 'vue-bootstrap-datetimepicker';
import VueSessionStorage from 'vue-sessionstorage';
// import VueMobileDetection from 'vue-mobile-detection';
import Element from 'element-ui';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import store from './store';

Vue.use(Element);
Vue.use(VueSessionStorage);
Vue.use(datePicker);
Vue.use(BootstrapVue);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
