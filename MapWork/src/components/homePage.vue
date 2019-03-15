<template>
    <div id="homepage" class="wrapper">
        <!--头部组件-->
        <div id="header" class="header">
            <div id="brand">
                <!-- <span class="hmi-size" ></span> -->
                <img src="../assets/img/tab_log.png" class="left-hmi-img" alt="商标" title="设计辅助系统首页" @click='OnSpider'>
                <span style="margin-top: 2px;">· {{titleName}}</span>
            </div>

            <div id="nav">
                <el-menu :default-active="activeIndex2" class="el-menu-demo header_li" mode="horizontal">
                    <el-menu-item index="5" @click='go_bug_fun()'>Bug搜索</el-menu-item>
                    <el-menu-item index="4" @click='go_development_book()'>式样书</el-menu-item>      
                    <el-menu-item index="2" @click='go_basic_design_template()'>开发设计</el-menu-item>
                    <el-menu-item index="1" @click='go_KnowHow_DB_AllDoc()'>知识库</el-menu-item>
                    <el-submenu index="3">
                        <template slot="title">管理</template>
                        <el-menu-item index="3-4-1" @click='OnPlatformManagement()'>平台管理</el-menu-item>
                        <el-menu-item index="3-4-2" @click='OnProjectManagement()'>项目管理</el-menu-item>
                        <el-menu-item index="3-4-3" @click='OnModuleManagement()'>模块信息管理</el-menu-item>
                        <el-menu-item index="3-4-6" @click='OnModuleRelationshipManagement()'>模块关系管理</el-menu-item>
                        <el-menu-item index="3-4-4" @click='OnAuthorManagement(1)' v-if="this.userPurviewManage('用户管理') == true">用户管理</el-menu-item>
                        <el-menu-item index="3-4-5" @click='OnAuthorManagement(2)' v-if="this.userPurviewManage('角色/权限管理') == true">角色/权限管理</el-menu-item>
                        <!-- <el-menu-item index="3-4-7" @click='go_book_management()'>式样书管理</el-menu-item> -->
                    </el-submenu>
                    <el-submenu index="10">
                        <template slot="title">{{user_name}}</template>
                        <el-menu-item index="10-2" @click='OnLogout'>退出</el-menu-item>
                    </el-submenu>
                </el-menu>
            </div>

        </div>
        <div class="homepage-view">
            <router-view v-bind:work="workType"></router-view>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            szPointer: 'MyARL',
            user_name: '',
            fullscreenLoading: false,
            activeIndex2: '2',
            workType: 'my',
            u_man: false,
            p_list: [],

            admin_flag: false,
            pl_flag: false,
            leader_flag: false,
            member_flag: false,
            translation_flag: false,

            Admin: false,
            PL: false,
            Leader: false,
            leadGp: [],

            group_flag: false,
            titleName: '开发设计'
        }
    },
    created() {
        // 获取用户权限:
        // this.getUserPurview()
    },
    computed: {
        highLinght(val) {
            return this.$store.state.high_type
        }
    },
    watch: {
        highLinght(val) {
            // 点击联动title,menu高亮
            this.activeIndex2 = window.sessionStorage.getItem('activeIndex2')
            this.changeTitle(window.sessionStorage.getItem('diffTitleType'))
        }
    },
    mounted() {
        this.changeTitle(window.sessionStorage.getItem('diffTitleType'))
        this.user_name = window.sessionStorage.getItem('Uall')
        this.activeIndex2 = window.sessionStorage.getItem('activeIndex2')
    },
    methods: {
        backHomePage() {
            this.$router.push('/tab')
        },
        changeTitle(val) {
            switch (val) {
                case 'bugList':
                    this.titleName = 'Bug搜索'
                    break
                case 'developmentBook':
                    this.titleName = '式样书'
                    break
                case 'knowhowDB':
                    this.titleName = '知识库'
                    break
                case 'developmentDesign':
                    this.titleName = '开发设计'
                    break

                case 'platformManagement':
                    this.titleName = '平台管理'
                    break
                case 'projectManagement':
                    this.titleName = '项目管理'
                    break
                case 'moduleManagement':
                    this.titleName = '模块信息管理'
                    break
                case 'userManagement':
                    this.titleName = '用户管理'
                    break
                case 'roleManagement':
                    this.titleName = '角色/权限管理'
                    break
                case 'teamManagement':
                    this.titleName = '组管理'
                    break
                case 'ModuleRelationship':
                    this.titleName = '模块关系管理'
                    break
                case 'bookManagement':
                    this.titleName = '式样书管理'
                    break
                default:
                    break
            }
        },
        handleSelect(key, keyPath) {
            event.preventDefault()
        },
        OnSpider() {
            this.szPointer = 'MyARL'
            this.$router.push('/tab')
        },
        OnLogout() {
            window.sessionStorage.removeItem('admin')
            window.sessionStorage.removeItem('Uall')
            window.sessionStorage.removeItem('workType')
            window.localStorage.removeItem('WorkTypeStatus')
            window.sessionStorage.clear()
            window.localStorage.clear()
            this.$router.push('/login')
        },
        Map_manage() {
            this.szPointer = 'Map'
            window.localStorage.setItem('WorkTypeStatus', 'Map')
            this.$router.push('/tagl/Map_Modle')
        },
        TAG_manage() {
            this.szPointer = 'TAG'
            window.localStorage.setItem('WorkTypeStatus', 'TAG')
            this.$router.push('/tagl/TAGLStauts')
        },
        authorManage() {
            this.szPointer = 'Author'
            window.localStorage.setItem('WorkTypeStatus', 'Author')
            this.$router.push('/tagl/authorManage')
        },
        
        go_KnowHow_DB_AllDoc() {
            this.titleName = '知识库'
            window.sessionStorage.setItem('activeIndex2', '1')
            window.sessionStorage.setItem('diffTitleType', 'knowhowDB')
            this.$router.push('/tagl/Form_Modle')
        },
        goKnowledgePoint() {
            this.titleName = '知识库'
            this.$store.state.basic_type = 'KnowledgePoint'
            this.$router.push('/tagl/Doc_Exhibition')
        },
        go_KnowHow_DB_MyDoc() {
            this.titleName = '知识库'
            this.$store.state.basic_type = 'MyDoc'
            this.$router.push('/tagl/Form_Modle/' + 'MyDoc')
        },
        go_KnowHow_DB_Count() {
            // 暂用超级管理员权限
            if (this.userPurviewManage('用户管理') == true) {
                this.titleName = '知识库'
                this.$store.state.basic_type = 'Count'
                this.$router.push('/tagl/Form_Modle/' + 'Count')
            } else {
                this.$message({
                    type: 'warning',
                    message: '您没有操作权限！'
                })
            }
        },
        go_KnowHow_TAG_Count() {
            // 暂用Knowledge条目_删除权限
            if (this.userPurviewManage('Knowledge条目_删除') == true) {
                this.titleName = '知识库'
                this.$store.state.basic_type = 'Tag'
                this.$router.push('/tagl/TAGLStauts')
            } else {
                this.$message({
                    type: 'warning',
                    message: '您没有操作权限！'
                })
            }
        },
        go_basic_design_template() {
            this.titleName = '开发设计'
            window.sessionStorage.setItem('activeIndex2', '2')
            window.sessionStorage.setItem('diffTitleType', 'developmentDesign')
            this.$router.push('/tagl/develop_design')
        },
        OnAuthorManagement(value) {
            switch (value) {
                case 1:
                    if (this.userPurviewManage('用户管理') == true) {
                        this.titleName = '用户管理'
                        window.sessionStorage.setItem('activeIndex2', '3-4-4')
                        this.$store.state.workType = '3-4-4'
                        this.$router.push('/tagl/authorManage')
                    } else {
                        this.$message({
                            type: 'warning',
                            message: '您没有操作权限！'
                        })
                    }

                    break
                case 2:
                    if (this.userPurviewManage('角色/权限管理') == true) {
                        this.titleName = '角色/权限管理'
                        window.sessionStorage.setItem('activeIndex2', '3-4-5')
                        this.$store.state.workType = '3-4-5'
                        this.$router.push('/tagl/authorManage')
                    } else {
                        this.$message({
                            type: 'warning',
                            message: '您没有操作权限！'
                        })
                    }

                    break
                case 3:
                    if (this.userPurviewManage('组管理') == true) {
                        this.titleName = '组管理'
                        window.sessionStorage.setItem('activeIndex2', '3-4-6')
                        this.$store.state.workType = '3-4-6'
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
        OnPlatformManagement() {
            // if (this.userPurviewManage('平台管理') == true) {
            this.titleName = '平台管理'
            window.sessionStorage.setItem('activeIndex2', '3-4-1')
            this.$store.state.fpm_id = 0
            this.$router.push('/tagl/Add_NewProject/FramworkTemplate')
            // } else {
            //     this.$message({
            //         type: 'warning',
            //         message: '您没有操作权限！'
            //     })
            // }
        },
        OnProjectManagement() {
            // if (this.userPurviewManage('项目管理') == true) {
            this.titleName = '项目管理'
            this.$store.state.fpm_id = 1
            window.sessionStorage.setItem('activeIndex2', '3-4-2')
            this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
            // } else {
            //     this.$message({
            //         type: 'warning',
            //         message: '您没有操作权限！'
            //     })
            // }
        },
        OnModuleRelationshipManagement() {
            //  if (this.userPurviewManage('项目管理') == true) {
            this.titleName = '模块关系管理'
            this.$store.state.fpm_id = 3
            window.sessionStorage.setItem('activeIndex2', '3-4-6')
            this.$router.push('/tagl/Add_NewProject/ModuleRelationship')
            // } else {
            //     this.$message({
            //         type: 'warning',
            //         message: '您没有操作权限！'
            //     })
            // }
        },
        OnModuleManagement() {
            this.titleName = '模块管理'
            window.sessionStorage.setItem('activeIndex2', '3-4-3')
            this.$store.state.fpm_id = 2
            this.$router.push('/tagl/Add_NewProject/ModelTemplate')
         
        },
        go_book_management() {
            this.titleName = '式样书管理'
            window.sessionStorage.setItem('activeIndex2', '3-4-7')
            this.$store.state.workType = '3-4-7'
            // this.$store.state.fpm_id = 2

            this.$router.push('/tagl/BookManagement')
        },
        go_development_book(){
            this.titleName = '式样书'
            window.sessionStorage.setItem('activeIndex2', '4')
            window.sessionStorage.setItem('diffTitleType', 'developmentBook')
            this.$router.push('/tagl/BookList')
        },
        go_bug_fun(){
            this.titleName = 'Bug搜索'
            window.sessionStorage.setItem('activeIndex2', '5')
            window.sessionStorage.setItem('diffTitleType', 'bugList')
            this.$router.push('/tagl/BugList')
        }
    }
}
</script>

<style scoped>
.bbb {
    border-bottom: 5px solid #42b983;
}
.wrapper {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow: hidden;
}
.header {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    width: 100%;
    height: 60px;
    background-color: white;
    z-index: 1000;
    box-shadow: 0 0 1px rgba(0, 0, 0, 0.25);
}
.homepage-view {
    position: absolute;
    left: 0;
    right: 0;
    top: 60px;
    bottom: 0px;
    overflow: hidden;
    width: 100%;
    background: white;
}
#footer {
    position: absolute;
    z-index: 700;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 22px;
    background-color: white;
    text-align: right;
    line-height: 22px;
}
#brand {
    position: absolute;
    left: 20px;
    top: 8px;
    width: 40%;
    height: 54px;
    font-size: 30px;
    color: #2c3e50;
    line-height: 40px;
    font-weight: bold;
    font-family: 'Dosis', 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
}
#brand img {
    vertical-align: middle;
    margin-right: 0px;
    cursor: pointer;
    width: 106px;
    height: 23px;
}
#brand span {
    text-shadow: 0 0 6px green;
    color: white;
    font-size: 22px;
}
#logout {
    position: absolute;
    right: 90px;
}
#nav {
    position: absolute;
    right: 24px;
    top: 10px;
    height: 60px;
}
.liqq {
    float: right;
    right: 70px;
}
.header .el-menu {
    border-radius: 2px;
    list-style: none;
    position: relative;
    margin: 0;
    padding-left: 0;
    background-color: white;
}

.header .el-menu--horizontal.el-menu--dark .el-submenu .el-menu-item.is-active,
.el-menu-item.is-active {
    border-bottom: 2px solid #42b983;
}
.left-hmi-img {
    /* border-radius: 50%; */
    width: 106px;
    height: 23px;
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
</style>
