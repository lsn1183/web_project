<template>
    <div class="app-nav">
        <el-menu :default-active="nav_active_index" class="el-menu-demo" mode="horizontal">
            <el-menu-item index="/dashboard" @click="go_test_dashboard('1')">测试结果列表</el-menu-item>
            <el-menu-item index="/testCase" @click="go_test_case('2')">测试用例</el-menu-item>
            <!-- <el-submenu index="2">
                <template slot="title">测试用例</template>
                <el-menu-item index="2-1">我的测试用例</el-menu-item>
                <el-menu-item index="2-2">全体测试用例</el-menu-item>
                <el-menu-item index="2-3">测试用例统计</el-menu-item>
                <el-menu-item index="2-4">管理测试用例</el-menu-item>
            </el-submenu> -->
            <el-menu-item index="/testPlan" @click="go_test_plan_manage('3')">测试计划</el-menu-item>

            <el-menu-item index="/backstage" @click="go_backstage_manage('4')">后台管理</el-menu-item>

            <el-submenu index="10">
                <template slot="title">{{user_name}}</template>
                <el-menu-item index="10-2" @click='logOut'>退出</el-menu-item>
            </el-submenu>
        </el-menu>
    </div>
</template>
<script>
export default {
    name: 'appNav',
    data() {
        return {
            nav_active_index: '',
            user_name : this.$store.getters.name
        }
    },
    created () {
        this.nav_active_index = '/' + this.$route.path.split('/')[1]
    },
    watch: {
        $route() {
            this.nav_active_index = '/' + this.$route.path.split('/')[1]
        }
    },
    methods: {
        logOut() {
            this.$store.dispatch('LogOut').then(() => {
                this.$router.push('/login')
            })
        },
        go_backstage_manage(index) {
            this.$store.dispatch('setNavActiveIndex', index)
            this.$router.push('/backstage')
        },
        go_test_plan_manage(index) {
            this.$store.dispatch('setNavActiveIndex', index)
            this.$router.push('/testPlan')
        },
        go_test_case(index) {
            this.$store.dispatch('setNavActiveIndex', index)
            this.$router.push('/testCase')
        },
        go_test_dashboard(index){
            this.$store.dispatch('setNavActiveIndex', index)
            this.$router.push('/dashboard')
        }
    }
}
</script>
<style lang="scss" scoped>
.app-nav {
    position: absolute;
    right: 40px;
    // top: 10px;
    top: 0;
    // height: 60px;
    height: 40px;
}
</style>
