<template>
  <div class="TheLogin">
    <h1>Login</h1>
    <br>
    <alert :message=message v-if="showMessage"></alert>
    <div>
      <b-form-input id="form-name-input"
                        type="text"
                        v-model="userEmail"
                        required
                        placeholder="Enter Username">
      </b-form-input>
      <br>
      <b-form-input id="form-name-input"
                        type="password"
                        v-model="userPassword"
                        required
                        placeholder="Enter Password">
      </b-form-input>
      <br><br>
      <b-button type='info' @click="logIn">Log in</b-button>
      <b style="word-space:2em">&nbsp;&nbsp;</b>
      <b-button type='info' @click="register">Register</b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  name: 'TheLogin',
  data() {
    return {
      userEmail: '',
      userPassword: '',
      showMessage: false,
      message: '',
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    logIn() {
      const path = 'api/login';
      const payload = {
        username: this.userEmail,
        password: this.userPassword,
      };
      axios.post(path, payload)
        .then((res) => {
          this.showMessage = true;
          this.message = res.data.message;
          this.$store.state.userid = res.data.userid;
          if (res.data.message === 'Logged in') this.$emit('TheLogin::loginResult', { loginResult: true });
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
      // this.$emit('TheLogin::loginResult', { loginResult: true, email: this.userEmail });
    },
    register() {
      this.$emit('TheLogin::loginResult', { loginResult: true, email: this.userEmail });
      this.$router.push('/Register');
    },
  },
};
</script>
