<template>
<!-- Show loading signal -->
<div class="loading"></div>
</template>

<script>
export default {
  name: 'Loading', // use to show loading signal
};
</script>

<style scoped>
.loading {
  position: fixed;
  left: 0;
  top: 0;
  background: url('~@/assets/loading.svg') center center no-repeat #fff;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
}
</style>
