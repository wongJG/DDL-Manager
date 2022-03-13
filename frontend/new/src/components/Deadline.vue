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
        <button type="button" class="btn btn-success btn-sm" v-b-modal.add-modal>Sync</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Date</th>
              <th scope="col">Time</th>
              <th scope="col">Reminder?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(deadline, index) in deadlines" :key="index">
              <td>{{ deadline.name }}</td>
              <td>{{ deadline.date }}</td>
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
          <br>
        </b-form-group>
        <b-form-group id="form-date-group"
                      label="Date:"
                      label-for="form-date-input">
            <b-form-input id="form-date-input"
                          type="text"
                          v-model="addForm.author"
                          required
                          placeholder="Enter Date">
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
        <b-form-group id="form-date-edit-group"
                      label="Date:"
                      label-for="form-date-edit-input">
            <b-form-input id="form-date-edit-input"
                          type="text"
                          v-model="editForm.date"
                          required
                          placeholder="Enter Date">
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
        date: '',
        time: '',
        reminder: [],
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        name: '',
        date: '',
        time: '',
        reminder: [],
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getDeadlines() {
      const path = 'http://127.0.0.1:5000/deadlines';
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
      const path = 'http://127.0.0.1:5000/deadlines';
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
      this.addBookForm.name = '';
      this.addBookForm.date = '';
      this.addBookForm.time = '';
      this.addBookForm.reminder = [];
      this.editForm.id = '';
      this.editBookForm.name = '';
      this.editBookForm.date = '';
      this.editBookForm.time = '';
      this.editBookForm.reminder = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addModal.hide();
      let reminder = false;
      if (this.addForm.reminder[0]) reminder = true;
      const payload = {
        name: this.addForm.name,
        date: this.addForm.date,
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
    editDeadline(deadline) {
      this.editForm = deadline;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editModal.hide();
      let reminder = false;
      if (this.editForm.reminder[0]) reminder = true;
      const payload = {
        name: this.editForm.name,
        date: this.editForm.date,
        time: this.editForm.time,
        reminder,
      };
      this.updateDeadline(payload, this.editForm.id);
    },
    updateDeadline(payload, ID) {
      const path = `http://127.0.0.1:5000/deadlines/${ID}`;
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
      const path = `http://127.0.0.1:5000/deadlines/${ID}`;
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
