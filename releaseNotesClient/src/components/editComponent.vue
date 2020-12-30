<template>
  <b-form ref="editReleaseModal" @submit="onSubmitUpdate($event)" @reset="onResetUpdate" class="w-100">
        
        <b-form-group id="form-releaseId-edit-group"
                    label="releaseId:"
                    label-for="form-releaseId-edit-input">
            <b-form-input id="form-releaseId-edit-input"
                        type="text"
                        v-model="id"
                        required
                        placeholder="Enter release ID">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-notes-edit-group"
                    label="notes:"
                    label-for="form-notes-edit-input">
                <notes-list v-bind:initialNotes="notes"></notes-list>
        </b-form-group>
        
        <b-form-group id="form-releaseDate-edit-group"
                        label="releaseDate:"
                        label-for="form-releaseDate-edit-input">
                <b-form-input id="form-releaseDate-edit-input"
                            type="date"
                            v-model="date"
                            required
                            placeholder="Enter Release Date">
                </b-form-input>
        </b-form-group>


        <b-form-group id="form-author-edit-group"
                        label="Author:"
                        label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                        type="text"
                        v-model="author"
                        required
                        placeholder="Enter author">
            </b-form-input>
        </b-form-group>
        <b-button-group> 
          <b-button type="submit" variant="primary">Update</b-button>   
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
</template>

<script>
import axios from 'axios';
import NotesList from './notesList';
export default {
    props: {
        originReleaseNotes: Object
    },
    data(){
        return {
            releaseToEdit : this.originReleaseNotes,
            id : '',
            date : '',
            notes : [],
            author : '',
            originReleaseNotesID : '',
        }
    },
    created(){
        this.id = this.releaseToEdit.ID;
        this.date = this.releaseToEdit["Release Date"];
        this.notes = this.releaseToEdit["Release notes"];
        this.originReleaseNotesID = this.releaseToEdit.ID;
        this.author = this.releaseToEdit.Author;
    },
    components: {
        "notes-list": NotesList,
    },

    methods:{
        onResetUpdate(evt) {
            evt.preventDefault();
            this.$emit("hide-update-model");
        },
        onSubmitUpdate(evt) {
            evt.preventDefault();
            const payload = {
                id: this.id,
                releaseNotes: this.notes,
                releaseDate: this.date,
                author: this.author,
            };
            this.updateBook(payload, this.originReleaseNotesID);
        },
        updateBook(payload, releaseID) {
            const path = `http://localhost:5000/releases/${releaseID}`;
            axios.put(path, payload)
                .then(() => {
                    const msg = 'Release updated!';
                    this.$emit("hide-update-model");
                    this.$emit("show-message", msg);
                })
                .catch((error) => {
                    console.error(error);
                    const msg = 'Failed to update release';
                    this.$emit("hide-update-model");
                    this.$emit("show-message", msg);
                });
        },
    }
}
</script>
