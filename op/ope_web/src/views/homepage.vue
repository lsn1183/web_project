<template>
    <div :class="hiddenClass" class="homepage-container">
        <div class="login-out-nav">
            <div class="img">
                <img @click="show_login_bar()" alt="user" src="../../static/img/user.png">
                <!-- <i class="el-icon-arrow-down"></i> -->
            </div>
            <div class="login-out-bar" v-show="show_login_flag">
                <el-button @click="login_out" type="text">退出</el-button>
            </div>
        </div>
        <div class="main-container">
            <app-main></app-main>
        </div>
        <navbar v-show="isVisible"></navbar>
    </div>
</template>
<script>
import AppMain from './AppMain'
import Navbar from './Navbar'
export default {
    name: "homepage",
    components: {
        AppMain,
        Navbar
    },
    data() {
        return {
            clientHeight: 0,
            clientWidth: 0,
            isVisible: true,
            show_login_flag:false
        };
    },
    methods: {
        // showNavbar(event) {
        //   this.clientWidth =   `${document.documentElement.clientWidth}`
        //   const clientX = event.clientX
        //   if(!this.isVisible && clientX + 20 >= this.clientWidth) {
        //     this.isVisible = true
        //   }

        //   if(this.isVisible && clientX + 101 < this.clientWidth) {
        //     this.isVisible = false
        //   }
        // }
        show_login_bar(){
            this.show_login_flag = !this.show_login_flag
        },
        login_out(){
            this.$router.push("/")
        }
    },
    computed: {
        sidebar() {
            return this.$store.state.app.sidebar
        },
        hiddenClass(aa) {
            return {
                hiddenSidebar: !this.sidebar.opened
            }
        }
    }
}
</script>
<style scoped>
.homepage-container {
    position: relative;
    height: 100%;
}
.main-container {
    height: calc(100% - 40px);
    transition: margin-right 0.28s;
    margin-right: 101px;
}
.hiddenSidebar .main-container {
    margin-right: 0;
}
.hiddenSidebar .navbar-container {
    right: -101px;
}
</style>

<style scoped lang="less">
@position_absolute: absolute;
@position_relative: relative;
@right: 120px;
@background_color: #ffffff;
.login-out-nav {
    width: 100%;
    height: 40px;
    position: @position_relative;
    padding-top: 3px;
    z-index: 10;
    cursor: pointer;
    background: #f0f0f0;
    .img:hover,.img:hover+.login-out-bar {
        img {
            border-radius: 3px;
            background-color: @background_color;
        }
        .el-icon-arrow-down {
            display: inline-block;
        }
        // display: block;
    }
    img {
        width: 32px;
        position: @position_absolute;
        right: @right;
        z-index: 101;
    }
    .el-icon-arrow-down {
        position: @position_absolute;
        right: 102px;
        width: 16px;
        display: none;
    }
    .login-out-bar {
        width: 80px;
        height: 50px;
        position: @position_absolute;
        right: @right;
        top: 35px;
        background: @background_color;

    }
}

</style>