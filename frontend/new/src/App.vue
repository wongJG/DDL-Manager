<template>
  <div id="app">
    <router-view v-if="this.$store.state.islogin"></router-view>
    <TheLogin v-else @TheLogin::loginResult="handleLoginResult"/>
  </div>
</template>

<script>
import TheLogin from './components/Login.vue';

export default {
  name: 'app',
  components: {
    TheLogin,
  },
  data() {
    return {
      userIsLoggedIn: false,
      userEmail: '',
    };
  },
  computed: {
    isLoggedIn() {
      return this.userIsLoggedIn;
    },
  },
  methods: {
    handleLoginResult({ loginResult, userid }) {
      this.$store.state.islogin = loginResult;
      this.$store.state.userid = userid;
    },
  },
};
</script>

<style>
#app {
  margin-top: 60px;
  margin-left: 40px;
  margin-right: 40px;
}
.fade-enter,
.fade-leave-active {
  opacity: 50;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
</style>
