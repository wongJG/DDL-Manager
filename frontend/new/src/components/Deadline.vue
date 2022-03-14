<!-- eslint-disable max-len -->
\<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1> Deadlines </h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.add-modal>Add</button>
        <b style="word-space:2em">&nbsp;&nbsp;</b>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.sync-modal>Sync</button>
        <br><br>
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
                          @click="editDeadline(deadline)">
                      Update
                  </button>
                  <b style="word-space:2em">&nbsp;&nbsp;</b>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteDeadline(deadline)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addModal"
            id="add-modal"
            title="Add a new deadline"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addForm.name"
                        required
                        placeholder="Enter Name">
          </b-form-input>
          </b-form-group>
          <br>
          <b-form-group id="form-time-group"
                      label="Time:"
                      label-for="form-time-input">
            <b-form-input id="form-time-input"
                          type="text"
                          v-model="addForm.time"
                          required
                          placeholder="Enter Time">
            </b-form-input>
          </b-form-group>
          <br>
        <b-form-group id="form-reminder-group">
          <b-form-checkbox-group v-model="addForm.reminder" id="form-checks">
            <b-form-checkbox value="true"><b style="word-space:1em">&nbsp;&nbsp;</b>Set reminder?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <br>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b style="word-space:2em">&nbsp;&nbsp;</b>
          <b-button type="reset" variant="danger">Reset</b-button>
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
                          type="text"
                          v-model="syncForm.password"
                          required
                          placeholder="Enter Password">
            </b-form-input>
          </b-form-group>
          <br>
        <br>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b style="word-space:2em">&nbsp;&nbsp;</b>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editModal"
            id="update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-name-edit-group"
                    label="Name:"
                    label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter Name">
          </b-form-input>
        </b-form-group>
          <br>
                  <b-form-group id="form-time-edit-group"
                      label="Time:"
                      label-for="form-time-edit-input">
            <b-form-input id="form-time-edit-input"
                          type="text"
                          v-model="editForm.time"
                          required
                          placeholder="Enter Time">
            </b-form-input>
          </b-form-group>
          <br>
        <b-form-group id="form-reminder-edit-group">
          <b-form-checkbox-group v-model="editForm.reminder" id="form-checks">
            <b-form-checkbox value="true"><b style="word-space:1em">&nbsp;&nbsp;</b>Set Reminder?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <br>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b style="word-space:2em">&nbsp;&nbsp;</b>
          <b-button type="reset" variant="danger">Cancel</b-button>
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
      deadlines: [],
      addForm: {
        name: '',
        time: '',
        reminder: [],
      },
      message: '',
      showMessage: false,
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
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getDeadlines() {
      const path = 'api/deadlines';
      axios.get(path)
        .then((res) => {
          this.deadlines = res.data.deadlines;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addDeadline(payload) {
      const path = 'api/deadlines';
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
      this.$refs.syncModal.hide();
      const payload = {
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
          this.getDeadlines();
          this.message = 'Deadline Synced';
          this.showMessage = true;
        })
        .catch((error) => {
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
    editDeadline(deadline) {
      this.editForm = deadline;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editModal.hide();
      let reminder = false;
      if (this.editForm.reminder[0]) reminder = 1;
      const payload = {
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
    onDeleteDeadline(deadline) {
      this.removeDeadline(deadline.id);
    },
  },
  created() {
    this.getDeadlines();
  },
};
</script>
