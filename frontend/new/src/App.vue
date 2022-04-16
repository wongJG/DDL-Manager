<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>
#app {
  margin-top: 60px;
  margin-left: 40px;
  margin-right: 40px;
}
.fade-enter,
.fade-leave-active {
  opacity: 50;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
</style>
