<template>
  <div>
    <b-alert show dismissible> {{ message }}</b-alert>
</div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
