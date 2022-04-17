<template>
  <div>
    <h1>Register</h1>
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
      <br>
      <b-form-input id="form-name-input"
                        type="password"
                        v-model="verifyCode"
                        required
                        placeholder="Enter Verification Code">
      </b-form-input>
      <br><br>
      <b-button type='info' @click="register">Sign Up</b-button>
      <b style="word-space:2em">&nbsp;&nbsp;</b>
      <b-button type='info' @click="sentCode">Get Verification Code</b-button>
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
      verifyCode: '',
      showMessage: false,
      message: '',
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    register() {
      const path = 'api/register';
      const payload = {
        username: this.userEmail,
        password: this.userPassword,
        verifyCode: this.verifyCode,
      };
      axios.post(path, payload)
        .then((res) => {
          this.showMessage = true;
          this.message = res.data.message;
          if (res.data.message === 'Registration Success') {
            this.$store.state.userid = res.data.id;
            this.$router.push('/');
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    sentCode() {
      const path = 'api/sentCode';
      const payload = {
        username: this.userEmail,
      };
      axios.post(path, payload)
        .then((res) => {
          this.showMessage = true;
          this.message = res.data.message;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
  },
};
</script>
