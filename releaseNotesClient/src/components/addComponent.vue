<template>
  <b-form ref="editReleaseModal" @submit="onSubmit($event,releaseToAdd)" @reset="onReset" class="w-100">
        
        <b-form-group id="form-releaseId-group"
                    label="releaseId:"
                    label-for="form-releaseId-input">
            <b-form-input id="form-releaseId-input"
                        type="text"
                        v-model="releaseToAdd.id"
                        required
                        placeholder="Enter release ID">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-notes-group"
                    label="notes:"
                    label-for="form-notes-input">
                <notes-list v-bind:initialNotes="releaseToAdd.releaseNotes"></notes-list>
        </b-form-group>
        
        <b-form-group id="form-releaseDate-group"
                        label="releaseDate:"
                        label-for="form-releaseDate-input">
                <b-form-input id="form-releaseDate-input"
                            type="date"
                            v-model="releaseToAdd.releaseDate"
                            required
                            placeholder="Enter Release Date">
                </b-form-input>
        </b-form-group>


        <b-form-group id="form-author-group"
                        label="Author:"
                        label-for="form-author-input">
            <b-form-input id="form-author-input"
                        type="text"
                        v-model="releaseToAdd.author"
                        required
                        placeholder="Enter author">
            </b-form-input>
        </b-form-group>
        <b-button-group> 
          <b-button type="submit" variant="primary">Submit</b-button>   
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
</template>

<script>
import axios from 'axios';
import NotesList from './notesList';
export default {
    data(){
        return {
            releaseToAdd : {
                id: '',
                releaseNotes: [],
                author: '',
                releaseDate: ''
            },
        }
    },

    components: {
        "notes-list": NotesList,
    },

    methods:{
        onReset(evt, releaseToAdd) {
            evt.preventDefault();
            this.$emit("hide-add-model");
        },
        onSubmit(evt,releaseToAdd) {
            evt.preventDefault();
            const payload = {
                id: this.releaseToAdd.id,
                releaseNotes: this.releaseToAdd.releaseNotes,
                releaseDate: this.releaseToAdd.releaseDate,
                author: this.releaseToAdd.author,
            };
            this.releaseToAdd = payload;
            this.addRelease(payload);
        },
        addRelease(payload) {
            const path = 'http://localhost:5000/releases';
            axios.post(path, payload)
                .then(() => {
                    const msg = 'Release added!';
                    this.$emit("hide-add-model");
                    this.$emit("show-message", msg);
                })
                .catch((error) => {
                    const msg = 'Failed to add release';
                    this.$emit("hide-add-model");
                    this.$emit("show-message", msg);
                    console.log(error);
                });
            },
    }
}
</script>
