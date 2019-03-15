<template>
    <div class="badesign" id="Model_template">
        <div class="header float-header">
            <span style="display:inline-block;width:50%;" @keyup.enter="search_click(searchValue)">
                <el-input clearable @clear="clear_click()" v-on:input="clear_click()" size="small" :placeholder=placeholderTitle v-model="searchValue" class="input-with-select">
                    <el-button slot="append" icon="el-icon-search" @click="search_click(searchValue)"></el-button>
                </el-input>
            </span>
            <span class="append-span" @click="appendModel()"> &nbsp;[ 添加模块 ]</span>
        </div>
        <div class="body">
            <el-table :data="ModelList" style="width: 97%" border :max-height="adaptivePageHeight">
                <el-table-column prop="code" sortable label="模块编号" width='110' align='center' header-align='center'></el-table-column>
                <el-table-column prop="title" sortable label="模块名称" align='left' header-align='center' min-width='150'>
                    <!-- <template slot-scope="scope">
                        <span class="a_group" :title="modelTitleName" type="text" @click="modelAuthor(scope.$index, scope.row)">{{scope.row.title}}</span>
                    </template> -->
                </el-table-column>
                <el-table-column prop="summary" label="概述" align='left' header-align='center' min-width='250'></el-table-column>
                <el-table-column prop="" label="操作" align='center' width=160 header-align='center'>
                    <template slot-scope="scope">
                        <el-button type='text' class="column-span" @click="editModel(scope.$index, scope.row)">
                            [ 编辑 ]</el-button>
                        <el-button type='text' class="column-span" @click="delModel(scope.$index, scope.row)">
                            [ 删除 ]</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="form-page">
                <el-pagination  @current-change="listPageChange" :current-page="page" :page-size="page_size" layout="total, prev, pager, next,jumper" :total="page_count"></el-pagination>
            </div>
        </div>
        <div class="dialog">
            <el-dialog title="组员" :visible.sync="modelAuthorFlag" width="30%" :before-close="closeEditDialog">
                <!-- <span class="dialog-content">{{modelAuthorName}}</span> -->
                <span class="dialog-span">{{modelName}}</span>
                <ul class="dialog-content" v-for="item in modelAuthorList">
                    <li>{{item.username}}</li>
                </ul>
            </el-dialog>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            ModelList: [],
            searchValue: "",
            modelTitleName: "点击查阅模块负责人",
            placeholderTitle: "请输入模块名称",
            page_copy:null,
            page: 1,
            page_size: 50,
            page_count: 0,
            tableType: null,
            adaptivePageHeight: window.innerHeight - 200,
            modelAuthorFlag:false,
            modelAuthorList:null,
            modelName:""
            // Fw_id:this.$store.state.fw_id,
        }
    },
    mounted () {
        if (this.$route.query.page) {
            let page = Number(this.$route.query.page)
            this.$nextTick(()=>{
                this.listPageChange(page)
            })
        }else{
            this.reqModelList()
            this.restoreStatus()
        }
    },
    computed: {
        fpm_id (val) {
            return this.$store.state.fpm_id
        }
    },
    watch: {
        fpm_id (val) {
            this.reqModelList()
        },
    },
    methods: {
        modelAuthor (index, data) {
            // console.log(data)
            var model_id=data.model_id
            var project_id=1
            this.modelName=data.title
            this.$axios.get(this.Ip + "/ApiModelAuthor/" + project_id + "/" + model_id).then(res => {
                if (res.data.result=="OK") {
                    // console.log(res,"------------------")
                    this.modelAuthorList=res.data.content
                    this.modelAuthorFlag = true 
                } else {
                    this.modelAuthorFlag = false
                    this.modelAuthorList=null
                    this.$message({
                        type:"info",
                        message:"暂无数据"
                    })
                }
            }).catch(err=>{
                
            })
        },
        closeEditDialog () {
            this.modelAuthorFlag = false
        },
        restoreStatus () {
            // window.sessionStorage.setItem('model_id', 0)
            window.sessionStorage.setItem('model_step_id', 0)
            // this.$store.state.step_id = 0
        },
        reqModelList () {
            this.tableType = "normal"
            if (this.$store.state.fpm_id == 2) {
                this.$axios.get(this.Ip + '/Model/' + this.page + "/" + this.page_size).then(res => {
                    if (res.data.result == 'OK') {
                        this.ModelList = res.data.content
                        this.page_count = res.data.count
                        window.sessionStorage.removeItem("model_id")
                    } else {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '服务异常'
                        })
                    }
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
                })
            }

        },
        delModel (index, data) {
            if (this.userPurviewManage('模块管理') == true || window.sessionStorage.getItem("Uall")=='Admin'||window.sessionStorage.getItem("Uall")==='Test_PMO'||window.sessionStorage.getItem("Uall")==='Test_GL'||window.sessionStorage.getItem("Uall")==='Test_DEV') {
                this.$confirm(this.globalData.hint.delete, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$axios.delete(this.Ip + '/Model/' + data.model_id)
                        .then(res => {
                            if (res.data.result == 'OK') {
                                this.ModelList.splice(index, 1)
                                this.$message({
                                    type: 'success',
                                    message: '删除成功!'
                                })
                            } else {
                                this.$message({
                                    showClose: true,
                                    type: 'error',
                                    message: res.data.error
                                })
                            }
                        }).catch(err => {
                            this.$message({
                                showClose: true,
                                type: 'error',
                                message: '服务异常'
                            })
                        })
                }).catch(() => { })
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }

        },
        editModel (index, data) {
            if (this.userPurviewManage('模块管理') == true || window.sessionStorage.getItem("Uall")==='Admin'||window.sessionStorage.getItem("Uall")==='Test_PMO'||window.sessionStorage.getItem("Uall")==='Test_GL'||window.sessionStorage.getItem("Uall")==='Test_DEV') {
                window.sessionStorage.setItem('model_id', data.model_id)
                window.sessionStorage.setItem('model_step_id', 5)
                // this.$store.state.step_id = 5
                let routerValue={path:'/tagl/ModuleSummary',query:{page:this.page_copy}}
                this.$router.push(routerValue)
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }

        },
        appendModel () {
            if (this.userPurviewManage('模块管理') == true || window.sessionStorage.getItem("Uall")==='Admin'||window.sessionStorage.getItem("Uall")==='Test_PMO'||window.sessionStorage.getItem("Uall")==='Test_GL'||window.sessionStorage.getItem("Uall")==='Test_DEV') {
                this.$router.push('/tagl/ModuleSummary')
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        search_click () {
            this.tableType = 'search'
            this.page = 1
            this.$axios.get(this.Ip + '/ModelQuery/' + this.page + "/" + this.page_size + "/" + this.searchValue).then(res => {
                if (res.data.result == 'OK') {
                    this.ModelList = res.data.content
                    this.page_count = res.data.count
                    window.sessionStorage.removeItem("model_id")
                } else {
                    this.$message({
                        type: 'error',
                        showClose: true,
                        message: '无数据'
                    })
                    this.ModelList = []
                    this.page_count = 0
                }
            }).catch(err => {
                this.$message({
                    type: 'error',
                    message: '服务异常'
                })
            })

        },
        clear_click () {
            if (this.searchValue === "") {
                this.reqModelList()
                return
            }
        },
        listPageChange (pageNum) {
            // this.page = pageNum
            this.page_copy=Number(pageNum)
            if (this.tableType == "search") {
                this.$axios.get(this.Ip + '/ModelQuery/' + pageNum + "/" + this.page_size + "/" + this.searchValue).then(res => {
                    if (res.data.result == 'OK') {
                        // 默认高亮哪一页
                        this.page = this.page_copy
                        this.ModelList = res.data.content
                        this.page_count = res.data.count
                        window.sessionStorage.removeItem("model_id")
                    } else {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '无数据'
                        })
                    }
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
                })
            } else {
                this.$axios.get(this.Ip + '/Model/' + pageNum + "/" + this.page_size).then(res => {
                    if (res.data.result == 'OK') {
                        // 默认高亮哪一页
                        this.page = this.page_copy
                        this.ModelList = res.data.content
                        this.page_count = res.data.count
                        window.sessionStorage.removeItem("model_id")
                    } else {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '无数据'
                        })
                    }
                }).catch(err => {
                    this.$message({
                        type: 'error',
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
    position: relative;
    width: 100%;
    height: 100%;
    padding-left: 25px;
    color: #606266;
}
.header {
    padding-top: 20px;
}
/* .float-header {
    float: right;
    padding-bottom: 20px;
    padding-right: 47px;
} */
.body {
    margin: 20px 0 0 0;
    /* max-height: 750px;
    overflow-y: scroll; */
}
.body .el-table_1_column_2 .cell {
    margin: 0 0 0 20px;
    /* padding: 0; */
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
.form-page{
    position: absolute;
    bottom: 20px;
}
.a_group {
    cursor: pointer;
}
.a_group:hover {
    color: #42b983;
}
.dialog-span{
    padding-left: 20px
}
.dialog-content{
    padding-left: 65px;
    max-height: 300px;
    overflow: scroll;
}
@media screen and (max-width: 1024px) {
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
    .append-span{
        font-size:12px;
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
    .append-span{
        font-size:12px;
    }
}
</style>
