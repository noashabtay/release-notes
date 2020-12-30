<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Releases</h1>
        <hr><br><br>
        <alert :message=message :key="reRender" v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.release-modal>Add Release</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Date</th>
              <th scope="col">Author</th>
              <th scope="col">releaseNotes</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(release, index) in releases" :key="index">
                <td>{{ release.ID }}</td>
                <td>{{ release['Release Date'] }}</td>
                <td>{{ release.Author }}</td>
                <td>
                   <ol>
                      <span v-for="(note,index) in release['Release notes']" :key="index">
                          <li>{{ note }}</li>
                      </span>
                  </ol>
                </td>
                <td>
                    <div class="btn-group" role="group">
                    <button
                            type="button"
                            class="btn btn-warning btn-sm"
                            v-b-modal.release-update-modal
                            @click="editRelease(release)">
                        Update
                    </button>
                    <button
                            type="button"
                            class="btn btn-danger btn-sm"
                            @click="onDeleteRelease(release)">
                        Delete
                    </button>
                    </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="addReleaseModal"
            id="release-modal"
            title="Add a new release"
            hide-footer>
            <add-component v-on:show-message="alertMessage"
                            v-on:hide-add-model="hideAdd"
                            ref="editComponent">
            </add-component>
    </b-modal>
    
    <b-modal ref="editReleaseModal"
            id="release-update-modal"
            title="Update"
            hide-footer>
             <div class="form-wrapper" @hide-update-model='hideUpdate'>
              <edit-component v-bind:originReleaseNotes="releaseToEdit"
                              v-on:show-message="alertMessage"
                              v-on:hide-update-model="hideUpdate"
                              ref="editComponent">
              </edit-component>
             </div>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import NotesList from './notesList';
import EditComponent from './editComponent.vue';
import AddComponent from './addComponent.vue';

export default {
  data() {
    return {
      releases: [],
      reRender: 0,
      releaseToAdd: {
          id: '',
          releaseNotes: [],
          author: '',
          releaseDate: ''
       },
      releaseToEdit: {
          id: '',
          releaseNotes: [],
          author: '',
          releaseDate: ''
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
    "notes-list": NotesList,
    "edit-component": EditComponent,
    "add-component" : AddComponent,
  },
  methods: {
     getReleases() {
        const path = 'http://localhost:5000/releases';
        axios.get(path)
            .then((res) => {
              this.releases = res.data.releases;
            })
            .catch((error) => {
              console.error(error);
            });
    },
    addRelease(payload) {
    const path = 'http://localhost:5000/releases';
    axios.post(path, payload)
        .then(() => {
          this.getReleases();
          this.initForm();
          this.message = 'Release added!';
          this.showMessage = true;
        })
        .catch((error) => {
          this.message = 'Failed to add release';
          this.showMessage = true;
          this.forceRerender();
          console.log(error);
          this.getReleases();
        });
    },
    initForm() {
        this.releaseToAdd.id = '';
        this.releaseToAdd.releaseNotes = [];
        this.releaseToAdd.releaseDate = '';
        this.releaseToAdd.author = '';
    },
    forceRerender() {
      this.reRender += 1;
    },
    onSubmit(evt,releaseToAdd) {
      evt.preventDefault();
      this.$refs.addReleaseModal.hide();
      const payload = {
          id: releaseToAdd.id,
          releaseNotes: releaseToAdd.releaseNotes,
          releaseDate: releaseToAdd.releaseDate,
          author: releaseToAdd.author,
      };
      this.releaseToAdd = payload;
      this.addRelease(payload);
    //   this.initForm();
    },

    onReset(evt) {
      evt.preventDefault();
      this.$refs.addReleaseModal.hide();
      this.initForm();
    },

    editRelease(release) {
      this.releaseToEdit = release;
    },

    hideUpdate() {
      this.$refs.editReleaseModal.hide();
      this.initForm();
      this.getReleases(); 
    },
     hideAdd() {
      this.$refs.addReleaseModal.hide();
      this.initForm();
      this.getReleases(); 
    },
    removeRelease(releaseID) {
      const path = `http://localhost:5000/releases/${releaseID}`;
      axios.delete(path)
        .then(() => {
          this.getReleases();
          this.message = 'release removed!';
          this.showMessage = true;
          this.forceRerender();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getReleases();
        });
    },
    onDeleteRelease(release) {
      this.removeRelease(release.ID);
    },
    alertMessage(msg){
      this.forceRerender();
      this.message = msg;
      this.showMessage = true;
    }
  },
  created() {
    this.getReleases();
  },
};
</script>
