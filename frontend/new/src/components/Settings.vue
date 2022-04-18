<template>
  <div align='center'>
      <b-navbar toggleable="lg" type="Dark" variant="Primary">
    <!-- <b style="word-space:4em">&nbsp;&nbsp;</b> -->
    <!-- <b-navbar-brand href="#">DDL Manager</b-navbar-brand> -->
    <!-- <b-navbar-toggle target="nav-collapse"></b-navbar-toggle> -->
    <!-- <b-collapse id="nav-collapse" is-nav> -->
      <b-navbar-nav>
        <b-nav-item href="/project">Project</b-nav-item>
        <b-nav-item href="/deadline">Deadline</b-nav-item>
      <!-- </b-navbar-nav> -->

      <!-- Right aligned nav items -->
      <!-- <b-navbar-nav class="ml-auto"> -->
        <b-nav-item-dropdown>
          <!-- Using 'button-content' slot -->
          <template #button-content>
            <em>User</em>
          </template>
          <b-dropdown-item href="/settings">Profile</b-dropdown-item>
          <b-dropdown-item href="/signout">Sign Out</b-dropdown-item>
          <b-dropdown-item href="/admin">Admin</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    <!-- </b-collapse> -->
  </b-navbar>
  <hr><br>
    <!-- <h1>Settings</h1> -->
    <br>
     <b-card
      style="max-width: 540px;"
    >
    <alert :message=message v-if="showMessage"></alert>
    <!-- <UploadImg v-model="photolink" /> -->
    <upload></upload>
    <div>
      <b-form-input id="form-name-input"
                        type="password"
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
      <b-button variant="outline-primary" @click="update">Update</b-button>
    </div>
    </b-card>
    <br><br><br>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import upload from './upload.vue';

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
    upload,
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
