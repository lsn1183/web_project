<template>
    <div class="login-container">
        <header>
            <div class="logo"></div>
            <div class="login-btn">
                <span @click="controlPopupDisplay"><u>{{$t('login.logIn')}}</u></span>
            </div>
        </header>
        <login-popup v-show="showDialog" @closeLoginPopup="showDialog = false"></login-popup>
    </div>
</template>
<script>
import LoginPopup from './LoginPopup'
export default {
    name: 'login',
    components: { LoginPopup },
    data() {
        return {
            showDialog: false
        }
    },
    methods: {
        controlPopupDisplay () {
            this.showDialog = !this.showDialog
        }
    }
}
</script>
<style lang="scss" scoped>
.login-container {
    position: fixed;
    width: 100%;
    height: 100%;
    background: url('../../assets/login_background.jpg') no-repeat;
    background-size: 100% 100%;
    header {
        position: absolute;
        width: 100%;
        height: 60px;
        line-height: 60px;
        .login-btn {
            margin-right: 35px;
            float: right;
            span {
                cursor: pointer;
            }
        }
    }
}
</style>