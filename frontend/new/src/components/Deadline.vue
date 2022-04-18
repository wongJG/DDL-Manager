<!-- eslint-disable max-len -->
\<template>

  <div class="container">
        <div class="row">
      <div class="col-sm-10">
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
        <!-- <h1> Deadlines </h1> -->
        <hr><br>
        <alert :message=message v-if="showMessage"></alert>
        <b-button variant="outline-primary" v-b-modal.add-modal>Add</b-button>
        <b style="word-space:2em">&nbsp;&nbsp;</b>
        <b-button variant="outline-primary" v-b-modal.sync-modal>Sync</b-button>
        <!-- <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Time</th>
              <th scope="col">Reminder?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(deadline, index) in deadlines" :key="index">
              <td>{{ deadline.name }}</td>
              <td>{{ deadline.time }}</td>
              <td>
                <span v-if="deadline.reminder">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.update-modal
                          @click="editDeadline(deadline.id)">
                      Update
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table> -->
      <br>
      <br>
      <calendar ref="calendar" :deadline="deadlines"></calendar>
      <br>
      <br>
      <br>
      <br>
      </div>
    </div>
    <b-modal ref="addModal"
            id="add-modal"
            title="Add a new deadline"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <!-- <b-form-group id="form-name-group" -->
                    <!-- label="Name:" -->
                    <!-- label-for="form-name-input"> -->
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addForm.name"
                        required
                        placeholder="Enter Name">
          </b-form-input>
          <!-- </b-form-group> -->
          <br>
          <!-- <b-form-group id="form-time-group"
                      label="Time:"
                      label-for="form-time-input"> -->
            <!-- <b-form-input id="form-time-input"
                          type="text"
                          v-model="addForm.time"
                          required
                          placeholder="Enter Time">
            </b-form-input> -->
            <date-picker v-model='addForm.time' :config='dateOptions'></date-picker>
          <!-- </b-form-group> -->
          <br>
        <b-form-group id="form-reminder-group">
          <b-form-checkbox-group v-model="addForm.reminder" id="form-checks">
            <b-form-checkbox value="true"><b style="word-space:1em">&nbsp;&nbsp;</b>Set reminder?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <br>
        <b-button-group>
          <b-button type="submit" variant="outline-primary">Submit</b-button>
          <b style="word-space:2em">&nbsp;&nbsp;</b>
          <b-button type="reset" variant="outline-danger">Reset</b-button>
        </b-button-group>
      </b-form>
      </b-modal>
    <b-modal ref="syncModal"
            id="sync-modal"
            title="Sync with Blackboard"
            hide-footer>
      <b-form @submit="onSyncSubmit" @reset="onSyncReset" class="w-100">
      <b-form-group id="form-username-group"
                    label="Username:"
                    label-for="form-username-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="syncForm.username"
                        required
                        placeholder="Enter Username">
          </b-form-input>
          <br>
        </b-form-group>
        <b-form-group id="form-passwd-group"
                      label="Password:"
                      label-for="form-passwd-input">
            <b-form-input id="form-passwd-input"
                          type="password"
                          v-model="syncForm.password"
                          required
                          placeholder="Enter Password">
            </b-form-input>
          </b-form-group>
          <br>
        <br>
        <b-button-group>
          <b-button type="submit" variant="outline-primary">Submit</b-button>
          <b style="word-space:2em">&nbsp;&nbsp;</b>
          <b-button type="reset" variant="outline-danger">Reset</b-button>
          <b style="word-space:2em">&nbsp;&nbsp;</b>
          <loading v-if="show_waiting_sign"> </loading>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editModal"
            id="update-modal"
            title="Update"
            hide-footer
            hide-header>
      <b-form @submit="onSubmitUpdate" @reset="onDeleteDeadline" class="w-100">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter Name">
          </b-form-input>
          <br>
          <date-picker v-model='editForm.time' :config='dateOptions'></date-picker>
          <!-- <CustomDateTimePicker /> -->
          <br>
        <b-form-group id="form-reminder-edit-group">
          <b-form-checkbox-group v-model="editForm.reminder" id="form-checks">
            <b-form-checkbox value="true"><b style="word-space:1em">&nbsp;&nbsp;</b>Set Reminder?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
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
import 'bootstrap/dist/css/bootstrap.css';
import '@fortawesome/fontawesome-free/css/all.css';
import 'pc-bootstrap4-datetimepicker/build/css/bootstrap-datetimepicker.css';
import datePicker from 'vue-bootstrap-datetimepicker';
import axios from 'axios';
import Alert from './Alert.vue';
import Calendar from './Calendar.vue';
import Loading from './loading.vue';
// import CustomDateTimePicker from './date-timepicker.vue';

export default {
  data() {
    return {
      deadlines: [],
      user: '',
      addForm: {
        name: '',
        time: '',
        reminder: [],
      },
      message: '',
      showMessage: false,
      show_waiting_sign: false,
      editForm: {
        id: '',
        name: '',
        time: '',
        reminder: [],
      },
      syncForm: {
        username: '',
        password: '',
      },
      dateOptions: {
        format: 'YYYY-MM-DD hh:mm:ss',
        useCurrent: false,
        icons: {
          time: 'far fa-clock',
          date: 'far fa-calendar',
          up: 'fas fa-arrow-up',
          down: 'fas fa-arrow-down',
          previous: 'fas fa-chevron-left',
          next: 'fas fa-chevron-right',
          today: 'fas fa-calendar-check',
          clear: 'far fa-trash-alt',
          close: 'far fa-times-circle',
        },
      },
    };
  },
  components: {
    alert: Alert,
    Calendar,
    loading: Loading,
    datePicker,
  },
  methods: {
    getDeadlines() {
      // eslint-disable-next-line
      const path = 'api/deadlines';
      // console.log(this.$store.state.userid);
      const payload = { id: this.$session.get('userid') };
      axios.post(path, payload)
        .then((res) => {
          this.deadlines = res.data.deadlines;
          this.$refs.calendar.refresh(res.data.deadlines);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addDeadline(payload) {
      const path = 'api/add-deadline';
      axios.post(path, payload)
        .then(() => {
          this.getDeadlines();
          this.message = 'Deadline added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getDeadlines();
        });
    },
    initForm() {
      this.addForm.name = '';
      this.addForm.time = '';
      this.addForm.reminder = [];
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.time = '';
      this.editForm.reminder = [];
      this.syncForm.username = '';
      this.syncForm.password = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addModal.hide();
      let reminder = false;
      if (this.addForm.reminder[0]) reminder = 1;
      const payload = {
        id: this.$session.get('userid'),
        name: this.addForm.name,
        time: this.addForm.time,
        reminder,
      };
      this.addDeadline(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addModal.hide();
      this.initForm();
    },
    onSyncSubmit(evt) {
      evt.preventDefault();
      this.show_waiting_sign = true;
      const payload = {
        id: this.$session.get('userid'),
        username: this.syncForm.username,
        password: this.syncForm.password,
      };
      this.syncDeadline(payload);
      this.initForm();
    },
    syncDeadline(payload) {
      const path = 'api/deadlines/sync';
      axios.put(path, payload)
        .then(() => {
          this.$refs.syncModal.hide();
          this.getDeadlines();
          this.message = 'Deadline Synced';
          this.showMessage = true;
        })
        .catch((error) => {
          this.$refs.syncModal.hide();
          // eslint-disable-next-line
          console.error(error);
          this.getDeadlines();
        });
    },
    onSyncReset(evt) {
      evt.preventDefault();
      this.$refs.syncModal.hide();
      this.initForm();
    },
    editDeadline(id) {
      for (let i = 0; i < this.deadlines.length; i += 1) {
        if (this.deadlines[i].id === Number(id)) {
          this.editForm = this.deadlines[i];
          break;
        }
      }
    },
    onSubmitUpdate(evt) {
      // console.log(this.editForm.time);
      evt.preventDefault();
      this.$refs.editModal.hide();
      let reminder = false;
      if (this.editForm.reminder[0]) reminder = 1;
      const payload = {
        id: this.$session.get('userid'),
        name: this.editForm.name,
        time: this.editForm.time,
        reminder,
      };
      this.updateDeadline(payload, this.editForm.id);
    },
    updateDeadline(payload, ID) {
      const path = `api/deadlines/${ID}`;
      axios.put(path, payload)
        .then(() => {
          this.getDeadlines();
          this.message = 'Deadline updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getDeadlines();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editModal.hide();
      this.initForm();
      this.getDeadlines();
    },
    removeDeadline(ID) {
      const path = `api/deadlines/${ID}`;
      axios.delete(path)
        .then(() => {
          this.getDeadlines();
          this.message = 'Deadline removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getDeadlines();
        });
    },
    onDeleteDeadline(evt) {
      evt.preventDefault();
      this.$refs.editModal.hide();
      this.removeDeadline(this.editForm.id);
    },
  },
  created() {
    this.getDeadlines();
  },
};
</script>
