<template>
  <div class="TheLogin">
  <b-card
      style="max-width: 540px;"
      title="Login"
    >
    <!-- <h1>Login</h1> -->
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
      <b-button variant="outline-primary" @click="logIn">Log in</b-button>
      <b style="word-space:2em">&nbsp;&nbsp;</b>
      <b-button variant="outline-primary" @click="register">Register</b-button>
    </div>
    </b-card>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css';
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
          if (res.data.message === 'Logged in') {
            this.$session.set('userid', res.data.userid);
            sessionStorage.setItem('isLogin', 'true');
            this.$router.push('/Deadline');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    register() {
      this.$router.push('/Register');
    },
  },
};
</script>
