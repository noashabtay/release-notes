<template>
  <div class="form-wrapper">
      <form ref='form'>
        <input v-model="new_item" v-bind:placeholder="placeholder" />
        <button type="submit" @click='addToList'>Add</button>
      </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      new_item: "",
      placeholder: "Add new note"
    };
  },
  methods: {
    addToList() {
      this.$refs.form.addEventListener('submit', event => {
        event.preventDefault()
      })
      this.$emit("new-item-added", this.new_item);
      this.new_item = "";
    }
  }
};
</script>

<style>
</style>