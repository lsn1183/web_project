<template>
    <div class="login-popup">
        <i class="el-icon-close close-size" @click="close_login_popup"></i>
        <div class="login-popup-form">
            <!-- <div class="login-register-title">
                <p  class="toggle-style">{{$t('login.logIn')}}</p>
                <p >{{$t('login.guest')}}</p>
                <el-tabs v-model="activeName" @tab-click="handleClick">
                    <el-tab-pane :label="$t('login.logIn')" name="first"></el-tab-pane>
                    <el-tab-pane :label="$t('login.guest')" name="second"></el-tab-pane>
                    
                </el-tabs>
            </div> -->
            <el-tabs v-model="activeName" @tab-click="handleClick(activeName)" :stretch='true' >
                <el-tab-pane :label="$t('login.oa_user')" name="first"></el-tab-pane>
                <el-tab-pane :label="$t('login.guest')" name="second"></el-tab-pane>
                
            </el-tabs>
            <form @keyup.enter="handle_login" v-show="user_login_show_flag">
                <el-input name="username" auto-complete="on" type="text" v-model="userData.username" :placeholder="$t('login.username')" @input="check_username"></el-input>
                <div class="login-error-tips">
                    <p v-show="usernameErrorFlag">{{$t('login.usernameErrorTips')}}</p>
                </div>
                <el-input name="password" auto-complete="on" type="password" v-model="userData.password" :placeholder="$t('login.password')" @input="check_password"></el-input>
                <div class="login-error-tips">
                    <P v-show="pwdErrorFlag">{{$t('login.pwdErrorTips')}}</P>
                    <p v-show="loginErrorFlag">{{$t('login.loginErrorTips')}}</p>
                </div>
                <el-button style="letter-spacing: 2px;width: 100%;background: #42b983;color: white;" @click="handle_login">{{$t('login.logIn')}}</el-button>
            </form>
        </div>
    </div>
</template>
<script>
export default {
    name: 'login-popup',
    data() {
        return {
            loginSubmitData: {},
            usernameErrorFlag: false,
            pwdErrorFlag: false,
            loginErrorFlag: false,
            userData:  {
                username: '',
                password: ''
            },
             activeName: 'first',
             user_login_show_flag:true
        }
    },
    methods: {
        close_login_popup () {
            this.$emit('close_login_popup')
        },
        check_username () {
            this.loginErrorFlag = false
            if (this.userData.username === '') {
                this.usernameErrorFlag = true
            } else {
                this.usernameErrorFlag = false
            }
        },
        check_password () {
            this.loginErrorFlag = false
            if (this.userData.password === '') {
                this.pwdErrorFlag = true
            } else {
                this.pwdErrorFlag = false
            }
        },
        check_user_data () {
            this.check_username()
            this.check_password()
            return this.usernameErrorFlag || this.pwdErrorFlag
        },
        handle_login () {
            if (this.check_user_data()) {
                return
            }
            this.$store.dispatch('Login', this.userData)
            .then(() => {
                this.$router.push({ path: '/homepage' })
            }).catch(err => {
                this.pwdErrorFlag = false
                this.usernameErrorFlag = false
                this.loginErrorFlag = true
            });
        },
        handleClick(activeName) {
            if (activeName == 'second') {
                this.user_login_show_flag = false
                this.$store.dispatch('Login', this.userData)
                .then(() => {
                    this.$router.push({ path: '/homepage' })
                }).catch(err => {
                    this.pwdErrorFlag = false
                    this.usernameErrorFlag = false
                    this.loginErrorFlag = true
                });
            }else{
                this.user_login_show_flag = true
            }
        }
    }
}
</script>
<style lang="scss" scoped>
    .login-popup {
        position: absolute;
        left: 50%;
        top: 42%;
        margin: -170px 0 0 -168px;
        width: 336px;
        height: 340px;
        background-color: white;
        border-radius: 4px;
        box-shadow: 2px 1px 9px #ccc;

        .close-size {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 20px;
            font-weight: bold;
            color: #999;
        }

        .login-popup-form {
            margin: 53px auto 0;
            width: 265px;

            .login-register-title {
                margin-bottom: 30px;
                height: 32px;
                border-bottom: 1px solid #eee;
                color: rgb(153, 153, 153);
                p {
                    float: left;
                    margin-left: 0;
                    width: 50%;
                    text-align: center;
                    cursor: pointer;
                    font-weight: 700;
                    font-size: 16px;
                }
                .toggle-style {
                    color: #42b983;
                    border-bottom: 2px solid #42b983;
                }
            }

            .login-error-tips {
                height: 30px;

                p {
                    font-size: 12px;
                    color: red;
                }
            }

            p {
                margin: 0 0 0 12px;
                height: 30px;
                line-height: 30px;
            }
        }
    }
    
</style>