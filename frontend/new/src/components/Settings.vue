<template>
  <div>
    <h1>Settings</h1>
    <br>
    <alert :message=message v-if="showMessage"></alert>
    <!-- <UploadImg v-model="photolink" /> -->
    <div>
      <b-form-input id="form-name-input"
                        type="text"
                        v-model="oldPassword"
                        required
                        placeholder="Enter Old Password">
      </b-form-input>
      <br>
      <b-form-input id="form-name-input"
                        type="password"
                        v-model="newPassword"
                        required
                        placeholder="Enter New Password">
      </b-form-input>
      <br><br>
      <b-button type='info' @click="update">Update</b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
// import upload from './Upload.vue';

export default {
  name: 'TheLogin',
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      showMessage: false,
      message: '',
    //   photolink: '',
    };
  },
  components: {
    alert: Alert,
    // uploading
  },
  methods: {
    update() {
      const path = 'api/changePass';
      const payload = {
        id: this.$store.state.userid,
        oldPass: this.oldPassword,
        newPass: this.newPassword,
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
