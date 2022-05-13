<template>
  <div align='center'>
      <b-navbar toggleable="lg" type="Dark" variant="Primary">
      

      <b-navbar-nav>

        <!-- navbar item -->
        <b-nav-item href="/project">Project</b-nav-item>
        <b-nav-item href="/deadline">Deadline</b-nav-item>

        <!-- Dropdown item -->
        <b-nav-item-dropdown>
          <template #button-content>
            <em>User</em>
          </template>
          <b-dropdown-item href="/settings">Profile</b-dropdown-item>
          <b-dropdown-item href="/signout">Sign Out</b-dropdown-item>
          <b-dropdown-item href="/admin">Admin</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
  </b-navbar>
  
  <hr><br><br>

  <!-- Card view -->
     <b-card style="max-width: 540px;">
    <!-- Message display -->
    <alert :message=message v-if="showMessage"></alert>

    <!-- Upload avatar module -->
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
    };
  },
  components: {
    alert: Alert,
    upload,
  },
  methods: {
    // Forward changing password to backend
    update() {
      const path = 'api/changePass';
      const payload = {
        id: this.$store.state.userid,
        oldPass: this.oldPassword,
        newPass: this.newPassword,
      };
      axios.post(path, payload)
        .then((res) => {
          this.showMessage = true;           // Display message if success
          this.message = res.data.message;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
