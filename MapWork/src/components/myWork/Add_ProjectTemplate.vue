<template>
    <div class="badesign" id="badesign_design">
        <div class="header">
            <span style="display:inline-block;width:50%;" @keyup.enter="search_click(searchValue)">
                <el-input clearable @clear="clear_click()" v-on:input="clear_click()" size="small" :placeholder=placeholderTitle v-model="searchValue" class="input-with-select">
                    <el-button slot="append" icon="el-icon-search" @click="search_click(searchValue)"></el-button>
                </el-input>
            </span>
            <span class="append-span"  @click="add_name()"> &nbsp;[ 添加项目 ]</span>
        </div>
        <div class="body">
            <el-table :data="projectList" style="width: 97%" border :max-height="adaptivePageHeight" :empty-text="empty_text">
                <el-table-column prop="proj_id" sortable label="项目编号" width='110' align='center' header-align='center'></el-table-column>
                <el-table-column prop="proj_name" sortable label="项目标题" align='left' header-align='center' min-width='120'></el-table-column>
                <el-table-column prop="summary" label="概述" align='left' header-align='center' min-width='150'></el-table-column>
                <el-table-column prop="fw_name" sortable label="所属平台" align='left' header-align='center' min-width='80'></el-table-column>
                <el-table-column prop="" label="操作" align='center' width=160 header-align='center'>
                    <template slot-scope="scope">
                        <!-- <el-button size="mini" type="primary" @click="_show_list(scope.$index, scope.row)">编辑</el-button> -->
                        <el-button type='text' class="column-span" @click="editProject(scope.$index, scope.row)">
                            [ 编辑 ]</el-button>
                        <el-button type='text' class="column-span" @click="delProject(scope.$index, scope.row)">
                            [ 删除 ]</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="form-page">
                <el-pagination id="list_page" @current-change="listPageChange" :current-page="page" :page-size="page_size" layout="total, prev, pager, next,jumper" :total="page_count"></el-pagination>
            </div>
        </div>
    </div>

</template>

<script>
export default {
    data () {
        return {
            projectList: [],
            manegePurviewEdit_Flag: null,
            searchValue: null,
            placeholderTitle: "请输入搜索的标题或概述",
            page: 1,
            page_size: 20,
            page_count: 0,
            tableType: null,
            adaptivePageHeight: window.innerHeight - 200,
            token: window.sessionStorage.getItem("accessToken"),
            user: window.sessionStorage.getItem("Uall"),
            empty_text:"暂无项目"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        }
    },
    created () {
        // 用户权限请求
        // this.getUserPermission()
        // 设置用户权限:
        // if (this.userPurviewManage("项目管理") == true) {
        //     this.manegePurviewEdit_Flag = true
        // } else {
        //     this.manegePurviewEdit_Flag = false
        // }
    },
    mounted () {
        this.reqProjectList()
        this.restoreStatus()
    },
    computed: {
        fpm_id (val) {
            return this.$store.state.fpm_id
        }
    },
    watch: {
        fpm_id (val) {
            this.reqProjectList()
        },
    },
    methods: {
        restoreStatus () {
            window.sessionStorage.setItem('proj_id', 0)
            window.sessionStorage.setItem('step_id', 0)
            this.$store.state.step_id = 0
        },
        reqProjectList () {
            if (this.$store.state.fpm_id == 1) {
                // let datas = {
                //     "accessToken": this.token,
                //     "page": this.page,
                //     "size": this.page_size,
                //     "manager": this.user
                // }
                this.$axios.get(this.Ip + '/Project/'+ this.page + "/" +this.page_size).then(res => {
                    if (res.data.result == 'OK') {
                        this.projectList = res.data.content
                        this.page_count = res.data.count
                        window.sessionStorage.removeItem('proj_id')
                        window.sessionStorage.removeItem('proj_name')
                    } else {
                        if (res.data.error == "") {
                            this.$message({
                                type: 'error',
                                showClose: true,
                                message: '您暂无项目。'
                            })
                        } else {
                            // this.$message({
                            //     type: 'error',
                            //     showClose: true,
                            //     message: "暂无数据"
                            // })
                        }
                    }
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        showClose: true,
                        message: '服务异常'
                    })
                })
            }

        },
        add_name () {
            // if (this.manegePurviewEdit_Flag == true || this.user==='Admin'||this.user==='Test_PL') {
                let routerValue={path:'/tagl/Project_Step_One',query:{flag:"true"}}
                this.$router.push(routerValue)
            // } else {
            //     this.$message({
            //         type: "warning",
            //         message: "您没有操作权限！"
            //     })
            // }
        },
        delProject (index, data) {
            if (data.manager == this.user || this.user==='Admin'||this.user==='Test_PL') {
                this.$confirm(this.globalData.hint.delete, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    let datas = {
                        "accessToken": this.token,
                        "proj_id": data.proj_id,
                    }
                    // console.log(this.token,window.sessionStorage.getItem("Uall"))
                    this.$axios.delete(this.Ip + '/Project/' + data.proj_id +"/" + window.sessionStorage.getItem("Uall")).then(res => {
                        if (res.data.result == 'OK') {
                            this.projectList.splice(index, 1)
                            this.$message({
                                type: 'success',
                                message: '删除成功!'
                            })
                        } else {
                            this.$message({
                                showClose: true,
                                type: 'error',
                                message: '删除失败!'
                            })
                        }
                    }).catch(err => {
                        this.$message({
                            showClose: true,
                            type: 'error',
                            message: '服务异常'
                        })
                    })
                })
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        editProject (index, data) {
            if (data.manager == this.user || this.user==='Admin'||this.user==='Test_PL') {
                window.sessionStorage.setItem('proj_id', data.proj_id)
                window.sessionStorage.setItem('step_id', 5)
                window.sessionStorage.setItem('proj_name', data.proj_name)
                this.$store.state.step_id = 5
                let routerValue={path:'/tagl/Project_Step_One',query:{flag:"false"}}
                this.$router.push(routerValue)
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        search_click () {
            this.tableType = 'search'
            let datas = {
                "accessToken": this.token,
                "page": this.page,
                "size": this.page_size,
                "manager": this.user,
                "condition": this.searchValue
            }
            this.$axios.post(this.Ip + '/CactusProject', datas).then(res => {
                if (res.data.result == 'OK') {
                    this.projectList = res.data.content
                    this.page_count = res.data.count
                    window.sessionStorage.removeItem('proj_id')
                    window.sessionStorage.removeItem('proj_name')
                } else {
                    if (res.data.error == "") {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '您暂无项目。'
                        })
                    } else {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: res.data.error
                        })
                    }
                    this.projectList = []
                    this.page_count = 0
                }
            }).catch(err => {
                this.$message({
                    type: 'error',
                    showClose: true,
                    message: '服务异常'
                })
            })
        },
        clear_click () {
            this.tableType = null
            if (this.searchValue === null) {
                this.reqProjectList()
                return
            }
        },
        listPageChange (pageNum) {
            this.page = pageNum
            if (this.tableType == "search") {
                let datas = {
                    "accessToken": this.token,
                    "page": this.page,
                    "size": this.page_size,
                    "manager": this.user,
                    "condition": this.searchValue
                }
                this.$axios.post(this.Ip + '/CactusProject', datas).then(res => {
                    if (res.data.result == 'OK') {
                        this.projectList = res.data.content
                        window.sessionStorage.removeItem('proj_id')
                        window.sessionStorage.removeItem('proj_name')
                    } else {
                        if (res.data.error == "") {
                            this.$message({
                                type: 'error',
                                showClose: true,
                                message: '您暂无项目。'
                            })
                        } else {
                            this.$message({
                                type: 'error',
                                showClose: true,
                                message: res.data.error
                            })
                        }
                    }
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        showClose: true,
                        message: '服务异常'
                    })
                })
            } else {
                let datas = {
                    "accessToken": this.token,
                    "page": this.page,
                    "size": this.page_size,
                    "manager": this.user,
                }
                this.$axios.post(this.Ip + '/CactusProject', datas).then(res => {
                    if (res.data.result == 'OK') {
                        this.projectList = res.data.content
                        window.sessionStorage.removeItem('proj_id')
                        window.sessionStorage.removeItem('proj_name')
                    } else {
                        if (res.data.error == "") {
                            this.$message({
                                type: 'error',
                                showClose: true,
                                message: '您暂无项目。'
                            })
                        } else {
                            this.$message({
                                type: 'error',
                                showClose: true,
                                message: res.data.error
                            })
                        }
                    }
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        showClose: true,
                        message: '服务异常'
                    })
                })
            }
        }
    }
}
</script>

<style scoped>
.badesign {
    width: 100%;
    height: 100%;
    position: relative;
    padding-left: 25px;
    color: #606266;
}
.header {
    padding-top: 20px;
}
.body {
    margin: 20px 0 0 0;
}
.body .el-table_1_column_2 .cell {
    margin: 0 0 0 20px;
}
.append-span {
    float: right;
    margin-right: 47px;
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}
.column-span {
    cursor: pointer;
    padding: 5px;
    display: block;
    float: left;
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear;
    color: #606266;
}
.column-span:hover {
    color: #6bcca0;
}
.form-page {
    position: absolute;
    bottom: 20px;
}
@media screen and (max-width: 1024px) {
    .badesign {
        width: 100%;
        height: 100%;
        min-width: 240px;
        font-size: 12px;
    }
    .body .docTable {
        max-height: 360px;
        width: 100%;
        height: 100%;
    }
    .append-span {
        font-size: 12px;
    }
}
@media screen and (max-width: 1366px) {
    .badesign {
        width: 100%;
        height: 100%;
        min-width: 240px;
        font-size: 10px;
    }
    .body .docTable {
        max-height: 360px;
        width: 100%;
        height: 100%;
    }
    .append-span {
        font-size: 12px;
    }
}
</style>
