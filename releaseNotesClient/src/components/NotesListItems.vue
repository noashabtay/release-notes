<template>
    <ol>
        <span v-for="(note,index) in my_release_notes" :key="index">
            <li @click="removeNote(index)">{{ note }}</li>
        </span>
    </ol>
</template>

<script>
export default {
    props: {
        releaseNotes: Array
    },
    data() {
        return {
            header: "Notes",
            placeholder: "add new note",
            new_note: "",
            my_release_notes: this.releaseNotes
        };
    },
    methods: {
        addNewNote() {
            console.log("addNewNote in NotesList releaseNotes = ",this.releaseNotes);
            this.releaseNotes.push(this.new_note);
            this.new_note = "";
        },
        removeNote(index){
            this.releaseNotes.splice(index,1);
        }
    }
}
</script>