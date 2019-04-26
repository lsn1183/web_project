<template>
<div class="image-view-container">
  <img src="../../../static/img/logo.png" alt="logo">
</div>
</template>
<script>
export default {
  name: "ImageView",
  data () {
    return {
    };
  }
}
</script>
<style scoped>
.image-view-container {
  position: fixed;
  top: 20px;
  right: 121px;
  /* width: 400px; */
  /* height: 400px; */
  overflow: auto;
  background: red;
}
</style>