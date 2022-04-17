import BootstrapVue from 'bootstrap-vue';
import datePicker from 'vue-bootstrap-datetimepicker';
import VueBus from 'vue-bus';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import store from './store';

Vue.use(VueBus);
Vue.use(datePicker);
Vue.use(BootstrapVue);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
