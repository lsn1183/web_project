<template>
    <div id="login">
        <header>
            <div class="fl">
                <span class="hmi-size"></span>
            </div>
            <span class="fr" style="margin-right: 35px;cursor: pointer;" @click="show_login_popup">
                <u>登录</u>
            </span>
        </header>

        <div class="content">
            <section class="section">
                <div><img src="../assets/img/Icon/IDESIGN.gif" class="log-img" alt="iDesign Logo" /></div>
                <br><br>
                <p>
                    <font color="#42b983">iDesign 〓 设计辅助系统</font>
                </p><br><br>
                <p>
                    <font color="#42b983">欢迎您</font>
                </p>
            </section>
        </div>

        <div id="popup" v-if="popupIsShow == true">
            <div id="popup-close" @click="close_popup">
                ×
            </div>
            <div class="login-content" v-if="Login_flag">
                <div class="login-fr">
                    <div class="big-re">
                        <p class="Regist fl" @click="to_login" style="border-bottom: 2px solid #42b983;">登录</p>
                        <p class="Regist fr" style="color: #999;">注册</p>
                    </div>
                    <div @keyup.enter="login()">
                        <div class="value-content">
                            <el-input v-model="user" placeholder="工号" @blur="check_username(registerName2)" @change="check_username(registerName2)"></el-input>
                            <p class="login-admin" v-show="admin_flag4 == true">工号不能为空</p>
                        </div>
                        <div class="value-content">
                            <el-input type="password" v-model="pwd" placeholder="密码" @blur="check_password(registerPwd2)" @change="check_password(registerPwd2)"></el-input>
                            <p class="login-key2" v-show="pwd_flag5 == true">密码不能为空</p>
                            <p class="login-key2" v-show="flag == true">工号或密码错误</p>
                        </div>
                    </div>
                    <el-button type="primary" @click="login" @keyup.enter="login()" size="midium" style="position: absolute;letter-spacing: 2px;width: 78%;margin-left: 42px;">立即登录</el-button>
                    <!-- <el-button type="primary" @click="sub2()" size="midium" style="letter-spacing: 2px;width: 35%;margin-left: 116px;position: absolute;top: 46.5%;">登录</el-button> -->
                    <!--</div>-->

                </div>
            </div>
            <!-- 注册页面 -->
            <div class="login-content" v-if="Regist_flag">
                <p class="bitian">*</p>
                <p class="bitian2">*</p>
                <p class="bitian3">*</p>
                <div class="login-fr">
                    <div class="big-re">
                        <p class="Regist fl" @click="to_login" style="color: #999;">登录</p>
                        <p class="Regist fr" style="border-bottom: 2px solid #42b983;">注册</p>
                    </div>
                    <div @keyup.enter="register()">
                        <div class="value-content">
                            <el-input v-model="registerName" placeholder="用户名" @blur="check_register_name(registerName)" @change="check_register_name(registerName)"></el-input>
                            <p class="login-admin" v-show="admin_flag == true">用户名重复</p>
                            <p class="login-admin" v-show="admin_flag2 == true">用户名不能为空</p>
                            <div class="correct-img2" v-show="correct_img2 == true">
                                <img src="../assets/img/reg_icons.png" />
                            </div>
                        </div>
                        <div class="value-content">
                            <el-input v-model="registerPwd" type="password" placeholder="输入密码" @blur="check_register_pwd(registerPwd)" @focus="check_register_pwd(registerPwd)" @change="check_register_pwd(registerPwd)"></el-input>
                            <p class="login-key2" v-show="pwd_flag4 == true">密码不能为空</p>
                            <p class="login-key2" v-show="pwd_flag == true">长度为6-15个字符</p>
                            <div class="correct-img" v-show="correct_img == true">
                                <img src="../assets/img/reg_icons.png" />
                            </div>
                        </div>
                        <div class="value-content">
                            <el-input v-model="REpwd" type="password" placeholder="确认密码" @blur="confirm_register_pwd(REpwd)" @change="confirm_register_pwd(REpwd)" @focus="confirm_register_pwd(REpwd)"></el-input>
                            <span class="re-key" v-show="repwd_flag2 == true">密码不能为空</span>
                            <span class="re-key" v-show="repwd_flag == true">两次密码不一致</span>
                            <div class="correct-img3" v-show="correct_img3 == true">
                                <img src="../assets/img/reg_icons.png" />
                            </div>
                        </div>
                        <p class="value-content">
                            <el-input v-model="RMail" placeholder="邮箱名">
                                <template slot="append">@security.suntec.net</template>
                            </el-input>
                        </p>
                    </div>
                    <p class="zhushi" v-show="zhushi_flag == true">*&nbsp;&nbsp;为必填项</p>
                    <el-button type="primary" @click="register()" size="midium" style="letter-spacing: 2px;width: 35%;margin-left: 116px;position: absolute;top: 76.5%;">立即注册</el-button>
                </div>
            </div>
        </div>
        <footer>Copyright&nbsp;&copy;&nbsp;2018 iAUTO</footer>
    </div>

</template>

<script>
export default {
    name: 'login',
    data() {
        return {
            correct_img: false,
            correct_img2: false,
            correct_img3: false,
            correct_flag: false,
            popupIsShow: false,
            repwd_flag: false,
            repwd_flag2: false,
            admin_flag: false,
            admin_flag2: false,
            pwd_flag: false,
            pwd_flag2: false,
            pwd_flag3: false,
            pwd_flag4: false,
            zhushi_flag: true,
            user: '',
            pwd: '',
            msg: '',
            valueup: {
                pwd: '',
                user: ''
            },
            flag: false,
            admin_flag4: false,
            pwd_flag5: false,
            Login_flag: true,
            Regist_flag: false,
            registerName: '',
            registerName2: '',
            registerPwd: '',
            registerPwd2: '',
            Ggroups: [],
            REpwd: '',
            RMail: '',
            usermember: '',
            testCheckData: '1111'
        }
    },
    mounted() {
        // this.get_groups();
        // this.get_members();
        // this.$Check.doCheck('HUDef', 'option', this.testCheckData)
    },
    methods: {
        check_register_name(name) {
            this.$axios.get(this.Ip + '/AllUsers').then(res => {
                for (var i = 0; i < res.data.content.length; i++) {
                    if (this.registerName == '') {
                        this.admin_flag = false
                        this.admin_flag2 = true
                        this.correct_img2 = false
                    } else {
                        if (name == res.data.content[i].user_name) {
                            this.admin_flag = true
                            this.admin_flag2 = false
                            this.correct_img2 = false
                            return
                        } else {
                            this.admin_flag = false
                            this.admin_flag2 = false
                            this.correct_img2 = true
                        }
                        if (this.registerName != '' && this.registerPwd != '' && this.REpwd != '') {
                            this.zhushi_flag = false
                        } else {
                            this.zhushi_flag = true
                        }
                    }
                }
            })
        },
        check_username(registerName2) {
            if (this.user == '') {
                this.admin_flag4 = true
                this.flag = false
            } else {
                this.admin_flag4 = false
                this.flag = false
            }
        },
        check_register_pwd(registerPwd) {
            if (registerPwd == '') {
                //如何密码为空时 ，focus和blur时提示出现
                this.pwd_flag = false
                this.pwd_flag4 = true
                this.correct_img = false
                //				this.correct_flag = false
            } else {
                //密码不为空时，进行判断，以此显示不同的响应状态
                var P_pwd = new RegExp(/^[\s\w]{6,15}$/)
                if (P_pwd.test(registerPwd) == true) {
                    this.pwd_flag = false
                    this.pwd_flag4 = false
                    //	 				this.correct_flag = true
                    this.correct_img = true
                } else {
                    this.pwd_flag = true
                    this.pwd_flag4 = false
                    //	 				this.correct_flag = false
                    this.correct_img = false
                }
            }
            if (this.registerPwd != '' && this.REpwd != '') {
                if (this.registerPwd == this.REpwd) {
                    this.correct_img3 = true
                    this.repwd_flag2 = false
                    this.repwd_flag = false
                } else {
                    this.correct_img3 = false
                    this.repwd_flag2 = false
                    this.repwd_flag = true
                }
            }

            if (this.registerName != '' && this.registerPwd != '' && this.REpwd != '') {
                this.zhushi_flag = false
            } else {
                this.zhushi_flag = true
            }
        },
        check_password(registerPwd2) {
            if (this.pwd == '') {
                this.pwd_flag5 = true
                this.flag = false
            } else {
                this.pwd_flag5 = false
                this.flag = false
            }
        },
        confirm_register_pwd(REpwd) {
            if (this.REpwd == '') {
                this.repwd_flag2 = true
                this.repwd_flag = false
                this.correct_img3 = false
            } else {
                if (REpwd == this.registerPwd) {
                    this.correct_img3 = true
                    this.repwd_flag2 = false
                    this.repwd_flag = false
                } else {
                    this.correct_img3 = false
                    this.repwd_flag2 = false
                    this.repwd_flag = true
                }
            }

            if (this.registerName != '' && this.registerPwd != '' && this.REpwd != '') {
                this.zhushi_flag = false
            } else {
                this.zhushi_flag = true
            }
        },
        close_popup() {
            this.popupIsShow = false
        },
        show_login_popup() {
            this.popupIsShow = true
        },
        login() {
            if (this.user && this.pwd != '') {
                this.valueup.pwd = this.pwd
                this.valueup.user = this.user
                window.sessionStorage.removeItem('accessToken')
                this.$axios
                    .post(this.Ip + '/login', { username: this.valueup.user, password: this.valueup.pwd })
                    .then(res => {
                        if (res.data.result == true) {
                            // 获取用户权限，提示用户目前是否有角色权限:
                            this.getUserPermission(res.data.user_id)
                            window.sessionStorage.setItem('workType', 'my')
                            window.sessionStorage.setItem('Uall', res.data.username)
                            window.sessionStorage.setItem('accessToken', res.data.accessToken)
                            window.sessionStorage.setItem('token', res.data.idesignToken)
                            sessionStorage.setItem('user_id',res.data.user_id)
                            this.flag = false
                            let self = this
                            setTimeout(() => {
                                //延迟路由跳转tab页面加载权限函数，解决权限未请求完成赋值，dom就调用函数了
                                self.$router.push('/tab')
                            }, 200)
                        } else {
                            this.flag = true
                            sessionStorage.clear()
                        }
                    })
            }
        },
        // login2() {
        //     this.flag = false
        //     window.localStorage.setItem('WorkTypeStatus', 'MyARL')
        //     window.sessionStorage.setItem('admin', '001')
        //     window.sessionStorage.setItem('Uall', 'admin')
        //     window.sessionStorage.setItem('workType', 'my')
        //     this.$router.push('/tagl/Form_Modle')
        // },
        //  ToRegist(){
        //    this.Login_flag = false;
        //    this.Regist_flag = true;
        //  },
        to_login() {
            this.Login_flag = true
            this.Regist_flag = false
        },
        get_groups() {
            this.$axios.get(this.Ip + '/GroupAllGroups').then(res => {
                this.Ggroups = res.data.content
            })
        },
        get_members() {
            this.$axios.get(this.Ip + '/AllUsers').then(res => {
                this.usermember = res.data.content
            })
        },
        register() {
            var user = this.registerName
            var pwd = this.registerPwd
            var Rpwd = this.REpwd
            var email = this.RMail + '@security.suntec.net'
            var P_pwd = new RegExp(/^[\s\w]{6,15}$/)
            if (P_pwd.test(pwd) == true) {
                if (pwd == Rpwd) {
                    this.$axios
                        .get(this.Ip + '/register/' + user + '/' + pwd + '/' + email)
                        .then(res => {
                            if (res.data.result == true) {
                                this.$notify({
                                    type: 'success',
                                    message: '注册成功'
                                })
                                //										this.$message.closeAll()
                                this.to_login()
                            } else {
                                this.$notify({
                                    type: 'error',
                                    message: '注册失败',
                                    showClose: true,
                                    duration: '0'
                                })
                            }
                        })
                        .catch(res => {
                            this.$notify({
                                type: 'error',
                                message: '注册失败',
                                showClose: true,
                                duration: '0'
                            })
                        })
                }
            } else {
                this.$notify({
                    type: 'error',
                    message: '注册失败',
                    showClose: true,
                    duration: '0'
                })
            }
        }
    }
}
</script>

<style>
* {
    margin: 0;
    padding: 0;
}

html,
body {
    font-family: '微软雅黑';
    /*font-size: 14px;*/
}

a {
    text-decoration: none;
}
ul,
ol,
li {
    list-style: none;
}
header span u {
    font-size: 14px;
}
.fl {
    float: left;
}
.fr {
    float: right;
}
#login {
    position: absolute;
    width: 100%;
    height: 100%;
    background: url('../assets/img/index_background.jpg') no-repeat;
    background-size: 100% 100%;
}
header {
    width: 100%;
    height: 60px;
    position: fixed;
    top: 0;
    left: 0;
    /*	background: #f8fafc;*/
    box-shadow: 3px 0 5px #dedede;
    -webkit-box-shadow: 3px 0 5px #dedede;
    line-height: 60px;
}
header img {
    width: 20%;
    height: 20%;
    vertical-align: middle;
    margin-left: 35px;
}
header span {
    color: #4d555d;
}
footer {
    width: 100%;
    height: 60px;
    position: fixed;
    bottom: 0;
    left: 0;
    /*	background: #f8fafc;*/
    line-height: 60px;
    color: #93999f;
    font-size: 12px;
    text-align: center;
    box-shadow: -3px 0 5px #dedede;
    -webkit-box-shadow: -3px 0 5px #dedede;
}
.content {
    width: 100%;
    height: 100%;
    /*	background: #fff;	*/
    position: fixed;
    top: 60px;
    bottom: 0;
    left: 0;
}
.section {
    width: 100%;
    height: 250px;
    position: relative;
    top: 22%;
}
.section div img {
    /* width: 210px; */
    /* height: 210px;	 */
    position: absolute;
    top: 10px;
    left: 47%;
    margin-left: -250px;
}
.section p {
    width: 100%;
    height: 24px;
    line-height: 24px;
    text-align: center;
    position: relative;
    top: 200px;
    color: #2c3e50;
    font-size: 24px;
}

#popup {
    position: fixed;
    width: 336px;
    min-height: 360px;
    left: 50%;
    top: 46%;
    margin-left: -168px;
    margin-top: -190px;
    /* z-index: 100; */
    background-color: #fff;
    border-radius: 4px;
    -webkit-box-shadow: 2px 1px 9px #ccc;
    box-shadow: 2px 1px 9px #ccc;
}

#popup-close {
    position: absolute;
    width: 30px;
    height: 30px;
    right: 5px;
    top: 5px;
    color: #999;
    cursor: pointer;
    text-align: center;
    line-height: 30px;
    font-size: 30px;
}

.login-content {
    width: 340px;
    margin: 0 auto;
}
.logo {
    width: 25%;
}

.size {
    font-size: 22px;
    color: #20a0ff;
}

.login-fr {
    margin-right: 35px;
}

.correct-img {
    position: absolute;
    left: 309px;
    top: 170px;
    width: 13px;
    height: 13px;
}

.correct-img img {
    width: 13px;
    height: 13px;
}

.correct-img2 {
    position: absolute;
    left: 309px;
    top: 104px;
    width: 13px;
    height: 13px;
}

.correct-img2 img {
    width: 13px;
    height: 13px;
}

.correct-img3 {
    position: absolute;
    left: 309px;
    top: 236px;
    width: 13px;
    height: 13px;
}

.correct-img3 img {
    width: 13px;
    height: 13px;
}

.re-key {
    width: 218px;
    height: 5px;
    position: absolute;
    top: 63%;
    left: 15%;
    color: #fc4343;
    font-size: 0.8em;
}

.login-admin {
    width: 218px;
    height: 5px;
    position: absolute;
    top: 44.5%;
    left: 15%;
    color: #fc4343;
    color: #fc4343\0;
    font-size: 0.8em;
}

.login-admin2 {
    display: block;
    width: 218px;
    height: 5px;
    position: absolute;
    top: 31%;
    left: 15%;
    color: #fc4343;
    font-size: 0.8em;
}

.login-admin3 {
    display: block;
    width: 218px;
    height: 5px;
    position: absolute;
    top: 46%;
    left: 15%;
    color: #fc4343;
    font-size: 0.8em;
}

.login-key2 {
    width: 218px;
    height: 5px;
    position: absolute;
    top: 63.5%;
    left: 15%;
    color: #fc4343;
    font-size: 0.8em;
}

.value-content {
    margin-top: 35px;
    margin-left: 40px;
}

.value_img > img {
    max-width: 100%;
    height: 42px;
}
input::-webkit-input-placeholder,
textarea::-webkit-input-placeholder {
    font-size: 14px;
}
input:-moz-placeholder,
textarea:-moz-placeholder {
    font-size: 14px;
}
input::-moz-placeholder,
textarea::-moz-placeholder {
    font-size: 14px;
}
input:-ms-input-placeholder,
textarea:-ms-input-placeholder {
    font-size: 14px;
}

.Regist {
    font-size: 16px;
    width: 50%;
    cursor: pointer;
    color: #42b983;
    padding-bottom: 6px;
    font-weight: bold;
    display: inline-block;
    text-align: center;
}

.Rselect {
    width: 88%;
    margin: 20px 0 0px 39px;
}
select::-webkit-input-placeholder,
option::-webkit-input-placeholder {
    color: rgb(140, 138, 133);
    font-size: 18px;
}
select:-moz-placeholder,
option:-moz-placeholder {
    color: rgb(140, 138, 133);
    font-size: 18px;
}
select::-moz-placeholder,
option::-moz-placeholder {
    color: rgb(140, 138, 133);
    font-size: 18px;
}
select:-ms-input-placeholder,
option:-ms-input-placeholder {
    color: rgb(140, 138, 133);
    font-size: 18px;
}

.value-content .el-input__inner {
    border: 1px solid #bfcbd9;
}

.login-fr .el-button {
    width: 35%;
    margin-top: 50px;
    margin-left: 116px;
}

.big-re {
    width: 80%;
    margin-left: 15%;
    margin-top: 53px;
    height: 30px;
    border-bottom: 1px solid #eee;
}

.bitian {
    /*color: #999;*/
    color: #fc4343;
    position: absolute;
    top: 25%;
    left: 93%;
}

.bitian2 {
    /*color: #999;*/
    color: #fc4343;
    position: absolute;
    top: 39.5%;
    left: 93%;
}

.bitian3 {
    /*color: #999;*/
    color: #fc4343;
    position: absolute;
    top: 55%;
    left: 93%;
}

.correct {
    color: #42b983;
}

.error {
    color: #fc4343;
}

.zhushi {
    width: 80%;
    height: 20px;
    text-indent: 1rem;
    line-height: 20px;
    color: #fc4343;
    font-size: 0.8em;
    position: absolute;
    top: 78%;
    left: 35px;
}
.hmi-size {
    display: block;
    margin: 20px 0 0 30px;
    font-weight: 600;
    font-size: 24px;
    color: #42b983;
    background: url('../assets/img/tab_log.png') no-repeat;
    background-size: 100% 100%;
    width: 106px;
    height: 23px;
}
.log-img {
    display: block;
    /* border-radius: 50%; */
    width: 600px;
    height: 200px;
    opacity: 0.92;
    margin-bottom: 10px;
    /* 1200
    400 */
}
</style>
