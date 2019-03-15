<template>
    <div id="login">
        <header>
            <div class="fl">
                <span class="hmi-size"></span>
            </div>
            <span class="fr" style="margin-right: 35px;cursor: pointer" @click='logout()'>
                <u>退出</u>
            </span>
        </header>
        <div class="tab-content-first">

            <ul class="tab-content-first-ul">
                <li class="asa-li" v-for="item in tab_list_data" :key="item.name" @click="tab_box_click_fun(item)">
                    <div class="content-size-box">
                        <p class="tab-content-size tab-content-size-ex">{{item.name}}</p>
                    </div>
                    <div class="Asa-box">
                        <ul class="tab-content-first-ul tab-content-ul-column" v-for="children in item.list" :key="children.name">
                            <li @click='tab_box_children_click_fun(children)'>
                                <div class="content-size-box content-size-box-ex">
                                    <p class="tab-content-size tab-content-size-ex tab-content-ex">{{children.children_name}}</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </li>
            </ul>
        </div>

        <footer>Copyright&nbsp;&copy;&nbsp;2018 iAUTO</footer>
    </div>
</template>

<script>
export default {
    name: 'tab',
    data() {
        return {
            user_name: '',
            page: 1,
            page_size: 20,
            tab_list_data: [
                { name: 'Bug搜索' },
                { name: '式样书' },
                { name: '开发设计' },
                { name: '知识库' },
                {
                    name: '管理',
                    list: [
                        { children_name: '平台管理' },
                        { children_name: '项目管理' },
                        { children_name: '模块信息管理' },
                        { children_name: '模块关系管理' },
                        // {children_name:'式样书管理'},
                        { children_name: '用户管理' },
                        { children_name: '角色/权限管理' }
                    ]
                }
            ]
        }
    },
    mounted() {
        this.user_name = window.sessionStorage.getItem('Uall')
        // console.log(this.userPurviewManage("平台管理"))
    },
    methods: {
        logout() {
            // 清除
            window.sessionStorage.removeItem('UserPermission')
            window.sessionStorage.removeItem('Uall')
            window.sessionStorage.clear()
            this.$router.push('/login')
        },
        go_KnowHow_DB_AllDoc() {
            window.sessionStorage.setItem('diffTitleType', 'knowhowDB')
            window.sessionStorage.setItem('activeIndex2', '1')
            this.$router.push('/tagl/Form_Modle')
        },
        go_KnowHow_DB_Count() {
            // 暂用超级管理员权限：
            if (this.userPurviewManage('用户管理') == true) {
                window.sessionStorage.setItem('diffTitleType', 'knowhowDB')
                window.sessionStorage.setItem('activeIndex2', '1-2-3')
                this.$router.push('/tagl/Form_Modle/' + 'Count')
            } else {
                this.$message({
                    type: 'warning',
                    message: '您没有操作权限！'
                })
            }
        },
        go_development_book() {
            window.sessionStorage.setItem('activeIndex2', '4')
            window.sessionStorage.setItem('diffTitleType', 'developmentBook')
            this.$router.push('/tagl/BookList')
        },
        go_bug_fun() {
            window.sessionStorage.setItem('activeIndex2', '5')
            window.sessionStorage.setItem('diffTitleType', 'bugList')
            this.$router.push('/tagl/BugList')
        },
        go_development_design() {
            window.sessionStorage.setItem('activeIndex2', '2')
            window.sessionStorage.setItem('diffTitleType', 'developmentDesign')
            // this.$router.push('/tagl/File_design/basic_design_template')
            this.$router.push('/tagl/develop_design')
        },

        go_platform_management() {
            // if (this.userPurviewManage('平台管理') == true) {
            window.sessionStorage.setItem('activeIndex2', '3-4-1')
            window.sessionStorage.setItem('diffTitleType', 'platformManagement')
            this.$store.state.fpm_id = 0
            this.$router.push('/tagl/Add_NewProject/FramworkTemplate')
            // } else {
            //     this.$message({
            //         type: 'warning',
            //         message: '您没有操作权限！'
            //     })
            // }
        },
        go_project_management() {
            // if (this.userPurviewManage('项目管理') == true) {
            window.sessionStorage.setItem('activeIndex2', '3-4-2')
            window.sessionStorage.setItem('diffTitleType', 'projectManagement')
            this.$store.state.fpm_id = 1
            this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
            // } else {
            //     this.$message({
            //         type: 'warning',
            //         message: '您没有操作权限！'
            //     })
            // }
        },
        go_module_management() {
            // if (this.userPurviewManage('模块管理') == true) {
            window.sessionStorage.setItem('activeIndex2', '3-4-3')
            window.sessionStorage.setItem('diffTitleType', 'moduleManagement')
            this.$store.state.fpm_id = 2
            this.$router.push('/tagl/Add_NewProject/ModelTemplate')
            // } else {
            //     this.$message({
            //         type: 'warning',
            //         message: '您没有操作权限！'
            //     })
            // }
        },
        go_module_relationship_manage() {
            window.sessionStorage.setItem('activeIndex2', '3-4-6')
            window.sessionStorage.setItem('diffTitleType', 'ModuleRelationship')
            this.$store.state.fpm_id = 3
            this.$router.push('/tagl/Add_NewProject/ModuleRelationship')
        },
        go_author_management(value) {
            switch (value) {
                case '1':
                    if (this.userPurviewManage('用户管理') == true) {
                        window.sessionStorage.setItem('activeIndex2', '3-4-4')
                        window.sessionStorage.setItem('diffTitleType', 'userManagement')
                        this.$router.push('/tagl/authorManage')
                    } else {
                        this.$message({
                            type: 'warning',
                            message: '您没有操作权限！'
                        })
                    }
                    break
                case '2':
                    if (this.userPurviewManage('角色/权限管理') == true) {
                        window.sessionStorage.setItem('activeIndex2', '3-4-5')
                        window.sessionStorage.setItem('diffTitleType', 'roleManagement')
                        this.$router.push('/tagl/authorManage')
                    } else {
                        this.$message({
                            type: 'warning',
                            message: '您没有操作权限！'
                        })
                    }
                    break
                default:
                    break
            }
        },
        go_book_management() {
            window.sessionStorage.setItem('activeIndex2', '3-4-7')
            window.sessionStorage.setItem('diffTitleType', 'bookManagement')
            this.$router.push('/tagl/BookManagement')
        },
        tab_box_click_fun(val) {
            switch (val.name) {
                case 'Bug搜索':
                    this.go_bug_fun()
                    break
                case '式样书':
                    this.go_development_book()
                    break
                case '开发设计':
                    this.go_development_design()
                    break
                case '知识库':
                    this.go_KnowHow_DB_AllDoc()
                    break
                default:
                    break
            }
        },
        tab_box_children_click_fun(val) {
            switch (val.children_name) {
                case '平台管理':
                    this.go_platform_management()
                    break
                case '项目管理':
                    this.go_project_management()
                    break
                case '模块信息管理':
                    this.go_module_management()
                    break
                case '模块关系管理':
                    this.go_module_relationship_manage()
                    break
                case '式样书管理':
                    this.go_book_management()
                    break
                case '用户管理':
                    this.go_author_management('1')
                    break
                case '角色/权限管理':
                    this.go_author_management('2')
                    break
                default:
                    break
            }
        }
    }
}
</script>

<style scoped>
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
.hmi-size {
    display: block;
    margin: 19px 0 0 20px;
    font-weight: 600;
    font-size: 24px;
    color: #42b983;
    background: url('../assets/img/tab_log.png') no-repeat;
    background-size: 100% 100%;
    width: 106px;
    height: 23px;
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

.fl {
    float: left;
}
.fr {
    float: right;
}

.bg {
    position: absolute;
    /*z-index: -1;*/
    width: 100%;
    margin-top: 60px;
    background: url('../assets/img/index_background.jpg') no-repeat;
    background-size: 100% 100%;
}
.tab_title_index {
    width: 100%;
    height: 60px;
    padding-top: 40px;
}
.index_ul_nav {
    width: 100%;
    height: 60px;
}
.index_ul_nav li {
    width: 200px;
    text-align: center;
    height: 60px;
    line-height: 60px;
    cursor: pointer;
    color: black;
    background: #f8fafc;
    font-size: 14px;
}
.index_ul_first {
    font-weight: 700;
    margin-left: 30px;
}
.index_ul_nav .index_ul_two {
    font-weight: 700;
    margin-right: 30px;
    color: black;
}
.tab-content-first {
    position: absolute;
    width: 100%;
    height: 114px;
    top: 40%;
    margin-top: -57px;
    left: 0;
    z-index: 10;
}
.tab-content-first-ul {
    width: 90%;
    min-width: 1024px;
    margin: 0 auto;
    /*background: #fff;*/
    display: flex;
    justify-content: space-around;
}
.tab-content-ul-column {
    width: 234px;
    min-width: 234px;
    flex-direction: column;
}
.tab-content-first-ul li {
    width: 234px;
    height: 114px;
    cursor: pointer;
    border-radius: 5px;
    position: relative;
    background: hsla(0, 0%, 100%, 0.3);
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear;
    background: url('../assets/img/tab_small_show.png') no-repeat;
    background-size: 100% 100%;
}
.tab-content-first-ul li:hover {
    box-shadow: 0 0 0 1px hsla(0, 0%, 100%, 0.3) inset, 0 0.5em 1em rgba(0, 0, 0, 0.6);
    text-shadow: 0 1px 1px hsla(0, 0%, 100%, 0.3);
    background: url('../assets/img/tab_small_hidden.png') no-repeat;
    background-size: 100% 100%;
    /* background: hsla(0, 0%, 100%, 0.3); */
}
.Asa-box .tab-content-first-ul li:hover {
    box-shadow: none;
}
.Asa-box .tab-content-first-ul li:hover .content-size-box .tab-content-ex {
    color: white;
}
.tab-content-first-ul li:hover .content-size-box .tab-content-ex {
    color: #42b983;
}

.tab-content-first-ul li:hover .content-size-box p {
    color: white;
}
.tab-content-first-ul li .content-size-box p {
    width: 160px;
    padding-left: 50px;
    height: 20px;
    line-height: 20px;
    color: #42b983;
    font-size: 21px;
}
.Asa-box .tab-content-first-ul li .content-size-box p {
    font-size: 11px;
}
.tab-content-size {
    font-weight: 500;
}
.content-size-box {
    margin-top: 36px;
}
.content-size-box-ex {
    margin-top: 0;
}
.tab-content-first-ul li .content-size-box .tab-content-size-ex {
    height: 47px;
    line-height: 47px;
}
.website-name {
    position: absolute;
    top: 32px;
    left: 55px;
    width: 150px;
    color: #42b983;
    font-size: 23px;
}
.user-logout {
    position: absolute;
    right: 4.35%;
    top: 5%;
    height: 33px;
    width: 268px;
    background: url('../assets/img/user_name_bg.png');
    background-size: 100% 100%;
}
.user-logout:hover .selli {
    display: block;
}
.selli {
    display: none;
    background-color: #42b983;
    border-radius: 6px;
    height: 29px;
    line-height: 29px;
    padding-left: 16px;
    font-size: 14px;
    margin: 0px 16px 0 14px;
    color: white;
    cursor: pointer;
}
.asa-li {
    position: relative;
}
.asa-li:hover .Asa-box {
    display: inline-block;
}
.Asa-box {
    position: absolute;
    left: 10px;
    top: 114px;
    width: 210px;
    display: none;
}

@media only screen and (max-width: 1440px) {
    .Asa-box .tab-content-first-ul li .content-size-box p {
        font-size: 13px;
    }
    .tab-content-first-ul {
        width: 100%;
        min-width: 936px;
        margin: 0 auto;
        /*background: #fff;*/
        display: flex;
        justify-content: space-around;
    }
    .tab-content-first-ul li {
        width: 205px;
        height: 100px;
        cursor: pointer;
        border-radius: 5px;
        position: relative;
        background: hsla(0, 0%, 100%, 0.3);
        transition: all 0.5s linear;
        -moz-transition: all 0.5s linear; /* Firefox 4 */
        -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
        -o-transition: all 0.5s linear;
        background: url('../assets/img/tab_small_show.png') no-repeat;
        background-size: 100% 100%;
    }
    .tab-content-first-ul li .content-size-box p {
        width: 150px;
        padding-left: 30px;
        height: 20px;
        line-height: 20px;
        color: #42b983;
        font-size: 17px;
    }
    .content-size-box {
        margin-top: 28px;
    }
    .Asa-box {
        position: absolute;
        left: 10px;
        top: 100px;
        display: none;
    }
    .asa-li .Asa-box .tab-content-first-ul li {
        margin-top: 11px;
        height: 40px;
        width: 180px;
    }
    .content-size-box-ex {
        margin-top: 0;
    }
    .tab-content-ul-column {
        width: 164px;
        min-width: 164px;
        flex-direction: column;
        margin: 0;
    }
    .tab-content-first-ul li .content-size-box .tab-content-size-ex {
        height: 42px;
        line-height: 42px;
    }
}

@media only screen and (max-width: 1280px) {
    .Asa-box .tab-content-first-ul li .content-size-box p {
        font-size: 13px;
    }
    .tab-content-first-ul {
        width: 100%;
        min-width: 936px;
        margin: 0 auto;
        /*background: #fff;*/
        display: flex;
        justify-content: space-around;
    }
    .tab-content-first-ul li {
        width: 164px;
        height: 80px;
        cursor: pointer;
        border-radius: 5px;
        position: relative;
        background: hsla(0, 0%, 100%, 0.3);
        transition: all 0.5s linear;
        -moz-transition: all 0.5s linear; /* Firefox 4 */
        -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
        -o-transition: all 0.5s linear;
        background: url('../assets/img/tab_small_show.png') no-repeat;
        background-size: 100% 100%;
    }
    .tab-content-first-ul li .content-size-box p {
        width: 150px;
        padding-left: 30px;
        height: 20px;
        line-height: 20px;
        color: #42b983;
        font-size: 17px;
    }
    .content-size-box {
        margin-top: 17px;
    }
    .Asa-box {
        position: absolute;
        left: 10px;
        top: 80px;
        display: none;
    }
    .asa-li .Asa-box .tab-content-first-ul li {
        margin-top: 11px;
        height: 40px;
        width: 150px;
    }
    .content-size-box-ex {
        margin-top: 0;
    }
    .tab-content-ul-column {
        width: 164px;
        min-width: 164px;
        flex-direction: column;
        margin: 0;
    }
    .tab-content-first-ul li .content-size-box .tab-content-size-ex {
        height: 42px;
        line-height: 42px;
    }
}

.Asa-box .tab-content-first-ul li {
    margin-top: 11px;
    height: 50px;
    width: 217px;
    background: url('../assets/img/tab_hidden_small.png') no-repeat;
    background-size: 100% 100%;
}

.Asa-box .tab-content-first-ul li:hover {
    background: url('../assets/img/tab_show_small.png') no-repeat;
    background-size: 100% 100%;
}
.Asa-box .tab-content-first-ul li:hover p {
    color: white;
}
/* .Asa-box .tab-content-first-ul li:hover {
    box-shadow: 0 0 0 1px hsla(0, 0%, 100%, 0.3) inset, 0 0.5em 1em rgba(0, 0, 0, 0.6);
    text-shadow: 0 1px 1px hsla(0, 0%, 100%, 0.3);
    background: hsla(0, 0%, 100%, 0.3);
} */
/* .Asa-box .tab-content-first-ul li:hover .content-size-box p {
    color: black;
} */
</style>
