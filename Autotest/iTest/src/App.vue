<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
    name: 'App',
    created() {
        // 第二种解决F5刷新，vuex丢失数据的方法
        // 在页面加载时读取sessionStorage里的状态信息

        // replaceState 用于替换整个rootState
        // 第一次加载项目是sessionStorage中没有userMsg,所以前面先做判断
        // 在开发阶段如果在vuex中添加新的字段，则新的字段不能被添加到sessionStorage中，所以采用Object.assign
        sessionStorage.getItem('userMsg') &&  this.$store.replaceState(Object.assign(this.$store.state,JSON.parse(sessionStorage.getItem("userMsg"))))
        //在页面刷新时将vuex里的信息保存到sessionStorage里
        window.addEventListener('beforeunload', () => {
            sessionStorage.setItem('userMsg', JSON.stringify(this.$store.state))
        })
    }
}
</script>

<style>
</style>
