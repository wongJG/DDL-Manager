import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);
export default new Vuex.Store({     // Store the login info in session storage
  state: {
    islogin: false,
    userid: '',
  },
});
