<template>
  <div>
    <notes-list-items v-bind:releaseNotes="notes"></notes-list-items>
    <notes-btn-actions placeholder="Add new note" v-on:new-item-added="addToList"></notes-btn-actions>

    <br />* Click on note number to remove it<br/><br/>
  </div>
</template>

<script>
import NotesListItems from "./NotesListItems";
import AddButtonActions from "./ActionList";

export default {
  components: {
    "notes-list-items": NotesListItems,
    "notes-btn-actions": AddButtonActions
  },
  props: {
        initialNotes: Array
  },
  data() {
    return {
      notes: this.initialNotes
    };
  },
  methods: {
    addToList(new_item) {
      this.notes.push(new_item);
    }
  }
};
</script>

<style>
</style>