<template>
  <div align='center'>

    <!-- Card view -->
    <b-card style="max-width: 540px;" title="Register">
    <br>

    <!-- Display message (when enabled) -->
    <alert :message=message v-if="showMessage"></alert>
    
    <!-- Input form -->
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
      <b-button variant="outline-primary" @click="register">Sign Up</b-button>
      <b style="word-space:2em">&nbsp;&nbsp;</b>
      <b-button variant="outline-primary" @click="sentCode">Get Verification Code</b-button>
    </div>


    </b-card>
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
    // forward register request to back-end
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
          console.log(error);
        });
    },
    // forward sent verification code request to back-end
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
          console.log(error);
        });
    },
  },
};
</script>
