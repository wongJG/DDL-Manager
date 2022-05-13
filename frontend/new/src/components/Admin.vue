<!-- eslint-disable max-len -->
\<template>
    <div>
    <!-- navbar -->
    <b-navbar toggleable="lg" type="Dark" variant="Primary">
      <b-navbar-nav>
        <b-nav-item href="/project">Project</b-nav-item>
        <b-nav-item href="/deadline">Deadline</b-nav-item>
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

      <div class="col-sm-10">
        <hr><br>
        <!-- Display message (if enabled) -->
        <alert :message=message v-if="showMessage"></alert>

        <!-- Table display all user -->
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Name</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>
                <div class="btn-group" role="group">
                  <!-- Edit button -->
                  <b-button
                          variant="outline-primary"
                          v-b-modal.update-modal
                          @click="editUser(user.id)">   
                      Update
                  </b-button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    <!-- Edit user model -->
    <b-modal ref="editModal"
            id="update-modal"
            title="Update"
            hide-footer
            hide-header>
      <b-form @submit="onSubmitUpdate" @reset="onDelete" class="w-100">
          <b-form-input id="form-name-edit-input"
                        type="password"
                        v-model="editForm.newPassword"
                        required
                        placeholder="Enter New Password">
          </b-form-input>
        <br>
        <b-button-group>
          <b-button type="submit" variant="outline-primary">Update</b-button>
          <b style="word-space:2em">&nbsp;&nbsp;</b>
          <b-button type="reset" variant="outline-danger">Delete</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      users: [],
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        newPassword: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    // Find the user to be edited and load its information
    editUser(id) {
      for (let i = 0; i < this.users.length; i += 1) {
        if (this.users[i].id === Number(id)) {
          this.editForm = this.users[i];
          break;
        }
      }
    },
    // request back-end to list all users
    getUsers() {
      const path = 'api/users';
      axios.get(path)
        .then((res) => {
          this.users = res.data.users;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    // Initialize update form
    initForm() {
      this.editForm.id = '';
      this.editForm.newPassword = '';
    },
    // Action on user update is submitted
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editModal.hide();
      const payload = {
        newPassword: this.editForm.newPassword,
      };
      this.updateUser(payload, this.editForm.id);
    },
    // forward user update request to back-end
    updateUser(payload, ID) {
      const path = `api/users/${ID}`;
      axios.post(path, payload)
        .then(() => {
          this.getUsers();
          this.message = 'User updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
    // If update is cancel
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editModal.hide();
      this.initForm();
      this.getUsers();
    },
    // forward user delete request to back-end
    removeUser(ID) {
      const path = `api/users/${ID}`;
      axios.delete(path)
        .then(() => {
          this.getUsers();
          this.message = 'User removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
    // Action on user delete is submitted
    onDelete(evt) {
      evt.preventDefault();
      this.$refs.editModal.hide();
      this.removeUser(this.editForm.id);
    },
  },

  // Verified admin privilege
  created() {
    const path = '/api/admin';
    const payload = { id: this.$session.get('userid') };
    axios.post(path, payload)
      .then((res) => {
        if (res.data.isAdmin === 1) this.getUsers();
        else this.$router.back();                      // Bounce back if not admin user
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
  },
};
</script>
