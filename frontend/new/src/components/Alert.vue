<template>
  <div>
    <!-- Display message -->
    <b-alert variant="primary" show>{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message'], // Use to display message
};
</script>
