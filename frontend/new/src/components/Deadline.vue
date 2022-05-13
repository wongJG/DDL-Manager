<!-- eslint-disable max-len -->
\<template>

  <div class="container">
        <div class="row">
      <div class="col-sm-10">
  <b-navbar toggleable="lg" type="Dark" variant="Primary">

    <!-- Navbar -->
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

        <hr><br>

        <!-- display message (if enabled) -->
        <alert :message=message v-if="showMessage"></alert>

        <!-- Add bottom -->
        <b-button variant="outline-primary" v-b-modal.add-modal>Add</b-button>
        <b style="word-space:2em">&nbsp;&nbsp;</b>

        <!-- Sync bottom -->
        <b-button variant="outline-primary" v-b-modal.sync-modal>Sync</b-button>
  
      <br><br>

      <!-- Calendar -->
      <calendar ref="calendar" :deadline="deadlines"></calendar>
      
      <br><br><br><br>
      </div>
    </div>

    <!-- add deadline form -->
    <b-modal ref="addModal"
            id="add-modal"
            title="Add a new deadline"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addForm.name"
                        required
                        placeholder="Enter Name">
          </b-form-input>
          <br>
            <date-picker v-model='addForm.time' :config='dateOptions'></date-picker>
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

    <!-- sync deadline form -->
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

    <!-- edit deadline form -->
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
    // request all deadline from back-end
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
    // forward add deadline request to back-end
    addDeadline(payload) {
      const path = 'api/add-deadline';
      axios.post(path, payload)
        .then(() => {
          this.getDeadlines();              // re-fetch all deadlines
          this.message = 'Deadline added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getDeadlines();
        });
    },
    // Initialize forms
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
    // Action on deadline adding is submitted
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
      this.initForm();             // clean the form
    },
    // Action on adding deadline is cancel
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addModal.hide();
      this.initForm();
    },
    // Action on deadline sync is submitted
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
    // forward deadline sync request to back-end
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
    // Action on deadline sync is cancel
    onSyncReset(evt) {
      evt.preventDefault();
      this.$refs.syncModal.hide();
      this.initForm();
    },
    // find the deadline to be edited and load into edit form
    editDeadline(id) {
      for (let i = 0; i < this.deadlines.length; i += 1) {
        if (this.deadlines[i].id === Number(id)) {
          this.editForm = this.deadlines[i];
          break;
        }
      }
    },
    // Action on deadline update is submitted
    onSubmitUpdate(evt) {
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
    // forward deadline update request to back-end
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
    // Action on deadline update is cancel
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editModal.hide();
      this.initForm();
      this.getDeadlines();
    },
    // forward deadline delete request to back-end
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
    // Action on deadline delete is submitted
    onDeleteDeadline(evt) {
      evt.preventDefault();
      this.$refs.editModal.hide();
      this.removeDeadline(this.editForm.id);
    },
  },
  // Initialize the page
  created() {
    this.getDeadlines();
  },
};
</script>
