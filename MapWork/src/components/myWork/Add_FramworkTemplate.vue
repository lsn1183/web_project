<template>
    <div class="badesign" id="Framework_template">
        <div class="header float-header">
            <!-- <span style="display:inline-block;width:50%;" @keyup.enter="search_click(searchValue)">
                <el-input clearable @clear="clear_click()" v-on:input="clear_click()" size="small" :placeholder=placeholderTitle v-model="searchValue" class="input-with-select">
                    <el-button slot="append" icon="el-icon-search" @click="search_click(searchValue)"></el-button>
                </el-input>
            </span> -->
            <span class="append-span"  @click="add_name()"> &nbsp;[ 添加平台 ]</span>
        </div>
        <div class="body">
            <el-table :data="FrameworkList" style="width: 97%" border :max-height="adaptivePageHeight" :empty-text="empty_text">
                <el-table-column prop="fw_id" sortable label="平台编号" width='110' align='center' header-align='center'></el-table-column>
                <el-table-column prop="fw_name" sortable label="平台名称" align='left' header-align='center' min-width='200'></el-table-column>
                <el-table-column prop="summary" label="概述" align='left' header-align='center' min-width='300'></el-table-column>
                <el-table-column prop="" label="操作" align='center' width=160 header-align='center'>
                    <template slot-scope="scope">
                        <!-- <el-button size="mini" type="primary" @click="_show_list(scope.$index, scope.row)">编辑</el-button> -->
                        <el-button type='text' class="column-span" @click="editFramwork(scope.$index, scope.row)">
                            [ 编辑 ]</el-button>
                        <el-button type='text' class="column-span" @click="delFramwork(scope.$index, scope.row)">
                            [ 删除 ]</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!-- <div class="form_page">
                <el-pagination id="list_page" @current-change="listPageChange" :current-page="page" :page-size="page_size" layout="total, prev, pager, next,jumper" :total="page_count"></el-pagination>
            </div> -->
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            FrameworkList: [],
            searchValue: "",
            placeholderTitle: "请输入搜索的标题或概述",
            page: 1,
            page_size: 20,
            page_count: 0,
            tableType: null,
            adaptivePageHeight: window.innerHeight - 200,
            empty_text:"暂无平台"
            // Fw_id:this.$store.state.fw_id,
        }
    },
    mounted () {
        this.reqFramworkList()
        this.restoreStatus()
    },
    computed: {
        fpm_id (val) {
            return this.$store.state.fpm_id
        }
    },
    watch: {
        fpm_id (val) {
            this.reqFramworkList()
        },
    },
    methods: {
        restoreStatus () {
            // window.sessionStorage.setItem('fw_id', 0)
            window.sessionStorage.setItem('fw_step_id', 0)
            this.$store.state.step_id = 0
        },
        reqFramworkList () {
            // console.log(this.$store.state.fpm_id,"FFF")
            if (this.$store.state.fpm_id == 0) {
                this.$axios.get(this.Ip + "/Framework").then(res => {
                    if (res.data.result == "OK") {
                        // console.log(res,"f")
                        this.FrameworkList = res.data.content
                        window.sessionStorage.removeItem("fw_id")
                    } else {
                        // this.$message({
                        //     type: 'info',
                        //     showClose: true,
                        //     message: '暂无数据'
                        // })
                    }
                })
                    .catch(err => {
                        this.$message({
                            type: 'error',
                            message: '服务异常'
                        })
                    })
            }
        },
        add_name () {
            // if (data.manager == window.sessionStorage.getItem("Uall") || window.sessionStorage.getItem("Uall") == 'Admin'||window.sessionStorage.getItem("Uall") =='Test_PMO') {
            let routerValue={path:'/tagl/FramworkSummary',query:{flag:"true"}}
            this.$router.push(routerValue)
            // } else {
            //     this.$message({
            //         type: "warning",
            //         message: "您没有操作权限！"
            //     })
            // }
        },
        editFramwork (index, data) {
            if (data.manager == window.sessionStorage.getItem("Uall") || window.sessionStorage.getItem("Uall") == 'Admin'||window.sessionStorage.getItem("Uall") =='Test_PMO' ) {
                window.sessionStorage.setItem('fw_id', data.fw_id)
                window.sessionStorage.setItem('fw_step_id', 2)
                // this.$store.state.step_id = 5
                let routerValue={path:'/tagl/FramworkSummary',query:{flag:"false"}}
                this.$router.push(routerValue)
                // this.$router.push('/tagl/FramworkSummary')
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        delFramwork (index, data) {
            if (data.manager == window.sessionStorage.getItem("Uall") || window.sessionStorage.getItem("Uall") == 'Admin'||window.sessionStorage.getItem("Uall") =='Test_PMO') {
                this.$confirm(this.globalData.hint.delete, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$axios.delete(this.Ip + '/Framework/' + data.fw_id +"/"+window.sessionStorage.getItem("Uall"))
                        .then(res => {
                            if (res.data.result == 'OK') {
                                this.FrameworkList.splice(index, 1)
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
                        })
                        .catch(err => {
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
        
        search_click () {
            // this.tableType = 'search'

        },
        clear_click () {
            if (this.searchValue === "") {

                return
            }

        },
        listPageChange (pageNum) {

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
.float-header {
    float: right;
    padding-bottom: 20px;
    padding-right: 47px;
}
.body {
    margin: 20px 0 0 0;
}
.body .btn_delete > span {
    color: red;
}
.body .el-table_1_column_2 .cell {
    margin: 0 0 0 20px;
}
.append-span {
    /* float: right; */
    /* margin-right: 47px; */
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
</style>
