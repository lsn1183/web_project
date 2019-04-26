<template>
<div class="app-main">
  <transition name="fade" mode="out-in">
    <router-view></router-view>
  </transition>
</div>
</template>
<script>
export default {
  name: "AppMain",
  data () {
    return {
    };
  }
}
</script>
<style scoped>
.app-main {
  box-sizing: border-box;
  height: 100%;
  overflow: hidden;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0;
}

.fade-enter,
.fade-leave-active {
  opacity: 0;
}
</style>