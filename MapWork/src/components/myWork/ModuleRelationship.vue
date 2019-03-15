<template>
    <div class="badesign" id="badesign_design">
        <div class="header">
            <span style="width:50%;" @keyup.enter="search_click(searchValue)">
                <el-select v-model="proj_id" filterable placeholder="请选择项目">
                    <el-option v-for="item in projectList" :key="item.proj_id" :label="item.proj_name" :value="item.proj_id">
                    </el-option>
                </el-select>
            </span>
        </div>
        <div class="body">
            <el-table :data="ModuleList" border :max-height="adaptivePageHeight" v-loading="loading">
                <el-table-column prop="model_id" sortable label="模块编号" width='110' align='center' header-align='center'></el-table-column>
                <el-table-column prop="title" sortable label="模块名称" align='center' header-align='center' min-width='150'>
                    <template slot-scope="scope">
                        <span class="a_group" :title="scope.row.titletitle" type="text">{{scope.row.title}}</span>
                    </template>
                </el-table-column>

                <el-table-column prop="model_ref" label="关联模块" align='left' header-align='center' min-width='250'>
                    <template slot-scope="scope">
                        <el-tag v-for="(itemss, itemss_index) in scope.row.model_ref" :key="itemss.model_id" closable type="success" @close="handleClose(scope.row.model_ref, itemss_index, scope.row)">
                            {{itemss.title}}
                        </el-tag>
                    </template>

                </el-table-column>

                <el-table-column prop="model_ref" label="关联模块" align='center' header-align='center' min-width='250'>
                    <template slot-scope="scope">
                        <el-select @focus="get_sub_module_list(scope.row)" filterable v-model="select_value" placeholder="请输入模块名称" style="display:block;">
                            <el-option v-for="(item, index) in scope.row.model_list" :key="index" :label="item.title" :value="item.model_id" @click.native="add_module_ref(scope.row.model_ref, item, scope.row)">

                            </el-option>
                        </el-select>
                    </template>
                </el-table-column>
            </el-table>
            <div class="form-page">
                <!-- <el-pagination id="list_page" @current-change="listPageChange" :current-page="page" :page-size="page_size" layout="total, prev, pager, next,jumper" :total="page_count"></el-pagination> -->
                <div class="div-input" style="text-align: right;width:100%">
                    <el-button @click="save()" type="primary" size="mini" v-if="proj_id !== '' && ModuleList.length !== 0">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
export default {
    data() {
        return {
            projectList: [],
            manegePurviewEdit_Flag: null,
            searchValue: null,
            placeholderTitle: '请输入搜索的标题或概述',
            page: 1,
            page_size: 20,
            page_count: 0,
            tableType: null,
            adaptivePageHeight: window.innerHeight - 200,
            token: window.sessionStorage.getItem('accessToken'),
            user: window.sessionStorage.getItem('Uall'),
            empty_text: '暂无项目',
            proj_id: '',
            ModuleList: [
                {
                    model_id: '',
                    model_list: [],
                    model_ref: [],
                    title: ''
                }
            ],
            subModuleList: [],
            proj_id: '',
            last_proj_id: 0,
            last_proj_data: [],
            loading: false,
            select_value: ''
        }
    },
    created() {
        // 用户权限请求
        // this.getUserPermission()
        // 设置用户权限:
        // if (this.userPurviewManage("项目管理") == true) {
        //     this.manegePurviewEdit_Flag = true
        // } else {
        //     this.manegePurviewEdit_Flag = false
        // }
    },
    mounted() {
        this.adaptivePageHeight = window.innerHeight - 216
        const that = this
        window.onresize = () => {
            return (() => {
                that.adaptivePageHeight = window.innerHeight - 216
            })()
        }
        this.req_proj_list()
        // this.req_module_list()
        // this.restoreStatus()
    },
    computed: {
        fpm_id(val) {
            return this.$store.state.fpm_id
        }
    },
    watch: {
        fpm_id(val) {
            this.req_proj_list()
        },
        proj_id(val) {
            if (this.last_proj_id === 0) {
                // do nothing
                // 第一次变化proj_id 不保存
                this.loading = true
                this.$axios
                    .get(this.Ip + '/SubModel/' + this.proj_id)
                    .then(res => {
                        this.subModuleList = res.data
                        let data = {
                            proj_id: val,
                            accessToken: window.sessionStorage.getItem('accessToken'),
                            username: window.sessionStorage.getItem('Uall')
                        }
                        this.$axios
                            .post(this.Ip + '/ModelRefGet', data)
                            .then(response => {
                                if (response.data.result == 'OK') {
                                    this.ModuleList = response.data.content
                                    for (let item of this.ModuleList) {
                                        item.model_list = []
                                        item.focus = 0
                                        // JSON.parse(JSON.stringify(this.subModuleList))
                                    }
                                    this.loading = false
                                    this.last_proj_id = this.proj_id
                                } else {
                                    this.loading = false
                                    this.$message({
                                        type: 'error',
                                        message: response.data.error
                                    })
                                }
                            })
                            .catch(error => {
                                this.loading = false
                                this.$message({
                                    type: 'error',
                                    message: '服务异常'
                                })
                            })
                    })
                    .catch(err => {
                        this.loading = false
                        this.$message({
                            type: 'error',
                            message: '服务异常'
                        })
                    })
            } else {
                if (this.proj_id == this.last_proj_id) {
                    // 如果上次proj_id 和last_proj_id 相同，说明不用请求心得项目数据
                } else {
                    // 如果上次proj_id 和last_proj_id 不相同相同，请求新的项目数据
                    let data = {
                        commit_user: window.sessionStorage.getItem('Uall'),
                        proj_id: this.last_proj_id,
                        model_list: this.ModuleList
                    }

                    this.$axios
                        .post(this.Ip + '/ModelRefPost', data)
                        .then(res => {
                            if (res.data.result == 'OK') {
                                this.$message({
                                    type: 'success',
                                    showClose: true,
                                    message: '保存成功'
                                })
                                this.loading = true
                                this.last_proj_id = this.proj_id
                                this.$axios
                                    .get(this.Ip + '/SubModel/' + this.proj_id)
                                    .then(res => {
                                        this.subModuleList = res.data
                                        let data = {
                                            proj_id: val,
                                            accessToken: window.sessionStorage.getItem('accessToken'),
                                            username: window.sessionStorage.getItem('Uall')
                                        }
                                        this.$axios
                                            .post(this.Ip + '/ModelRefGet', data)
                                            .then(response => {
                                                if (response.data.result == 'OK') {
                                                    this.ModuleList = response.data.content
                                                    for (let item of this.ModuleList) {
                                                        item.model_list = res.data
                                                    }
                                                    this.loading = false
                                                } else {
                                                    this.loading = false
                                                    this.$message({
                                                        type: 'error',
                                                        message: response.data.error
                                                    })
                                                }
                                            })
                                            .catch(error => {
                                                this.loading = false
                                                this.$message({
                                                    type: 'error',
                                                    message: '服务异常'
                                                })
                                            })
                                    })
                                    .catch(err => {
                                        this.loading = false
                                        this.$message({
                                            type: 'error',
                                            message: '服务异常'
                                        })
                                    })
                            } else {
                                this.proj_id = this.last_proj_id
                                this.$message({
                                    type: 'error',
                                    showClose: true,
                                    message: '服务异常'
                                })
                            }
                        })
                        .catch(err => {
                            this.proj_id = this.last_proj_id
                            this.$message({
                                type: 'error',
                                showClose: true,
                                message: res.data.error
                            })
                        })
                }
            }
        }
    },
    methods: {
        add_module_ref(model_ref, item, row) {
            model_ref.push(item)
            let arr_module_ref = row.model_ref.map(item => item.model_id)
            let arr_sub_module = this.subModuleList.map(item => item.model_id)
            let arr_diff = arr_module_ref
                .concat(arr_sub_module)
                .filter(item => !arr_module_ref.includes(item) || !arr_sub_module.includes(item))
            row.model_list = []
            for (let item of arr_diff) {
                for (let sub_module_item of this.subModuleList) {
                    if (item == sub_module_item.model_id) {
                        row.model_list.push(sub_module_item)
                    }
                }
            }
            this.select_value = ''
        },
        handleClose(model_ref, index, row) {
            model_ref.splice(index, 1)
            let arr_module_ref = row.model_ref.map(item => item.model_id)
            let arr_sub_module = this.subModuleList.map(item => item.model_id)
            let arr_diff = arr_module_ref
                .concat(arr_sub_module)
                .filter(item => !arr_module_ref.includes(item) || !arr_sub_module.includes(item))
            row.model_list = []
            for (let item of arr_diff) {
                for (let sub_module_item of this.subModuleList) {
                    if (item == sub_module_item.model_id) {
                        row.model_list.push(sub_module_item)
                    }
                }
            }
        },
        get_sub_module_list(row) {
            // 根据已选择选项，显示剩下选项
            if (row.focus == 0) {
                let arr_module_ref = row.model_ref.map(item => item.model_id)
                let arr_sub_module = this.subModuleList.map(item => item.model_id)
                let arr_diff = arr_module_ref
                    .concat(arr_sub_module)
                    .filter(item => !arr_module_ref.includes(item) || !arr_sub_module.includes(item))
                row.model_list = []
                for (let item of arr_diff) {
                    for (let sub_module_item of this.subModuleList) {
                        if (item == sub_module_item.model_id) {
                            row.model_list.push(sub_module_item)
                        }
                    }
                }
                row.focus += 1
            }
            
        },
        optionClick(val) {
            this.last_proj_id = val
            this.$axios
                .get(this.Ip + '/SubModel/' + val)
                .then(res => {
                    this.subModuleList = res.data
                    let data = {
                        proj_id: val,
                        accessToken: window.sessionStorage.getItem('accessToken'),
                        username: window.sessionStorage.getItem('Uall')
                    }
                    this.$axios
                        .post(this.Ip + '/ModelRefGet', data)
                        .then(response => {
                            if (response.data.result == 'OK') {
                                this.ModuleList = response.data.content
                                for (let item of this.ModuleList) {
                                    item.model_list = res.data
                                    item.focus = 0
                                }
                            } else {
                                this.$message({
                                    type: 'error',
                                    message: response.data.error
                                })
                            }
                        })
                        .catch(error => {
                            this.$message({
                                type: 'error',
                                message: '服务异常'
                            })
                        })
                })
                .catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
                })
        },
        restoreStatus() {
            window.sessionStorage.setItem('proj_id', 0)
            window.sessionStorage.setItem('step_id', 0)
            this.$store.state.step_id = 0
        },
        req_proj_list() {
            if (this.$store.state.fpm_id == 3) {
                // let datas = {
                //     "accessToken": this.token,
                //     "page": this.page,
                //     "size": this.page_size,
                //     "manager": this.user
                // }
                this.$axios
                    .get(this.Ip + '/Project')
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.projectList = res.data.content
                            this.page_count = res.data.count
                            window.sessionStorage.removeItem('proj_id')
                            window.sessionStorage.removeItem('proj_name')
                        } else {
                            if (res.data.error == '') {
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
                    })
                    .catch(err => {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '服务异常'
                        })
                    })
            }
        },
        editProject(index, data) {
            if (data.manager == this.user || this.user === 'Admin' || this.user === 'Test_PL') {
                window.sessionStorage.setItem('proj_id', data.proj_id)
                window.sessionStorage.setItem('proj_name', data.proj_name)
                this.$router.push('/tagl/ModuleRelationshipEdit')
            } else {
                this.$message({
                    type: 'warning',
                    message: '您没有操作权限！'
                })
            }
        },
        search_click() {
            this.tableType = 'search'
            let datas = {
                accessToken: this.token,
                page: this.page,
                size: this.page_size,
                manager: this.user,
                condition: this.searchValue
            }
            this.$axios
                .post(this.Ip + '/CactusProject', datas)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.projectList = res.data.content
                        this.page_count = res.data.count
                        window.sessionStorage.removeItem('proj_id')
                        window.sessionStorage.removeItem('proj_name')
                    } else {
                        if (res.data.error == '') {
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
                })
                .catch(err => {
                    this.$message({
                        type: 'error',
                        showClose: true,
                        message: '服务异常'
                    })
                })
        },
        clear_click() {
            this.tableType = null
            if (this.searchValue === null) {
                this.req_proj_list()
                return
            }
        },
        save() {
            let data = {
                commit_user: window.sessionStorage.getItem('Uall'),
                proj_id: this.proj_id,
                model_list: this.ModuleList
            }
            this.$axios
                .post(this.Ip + '/ModelRefPost', data)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.$message({
                            type: 'success',
                            showClose: true,
                            message: '保存成功'
                        })
                    } else {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '服务异常'
                        })
                    }
                })
                .catch(err => {
                    this.$message({
                        type: 'error',
                        showClose: true,
                        message: res.data.error
                    })
                })
        },
        listPageChange(pageNum) {
            this.page = pageNum
            if (this.tableType == 'search') {
                let datas = {
                    accessToken: this.token,
                    page: this.page,
                    size: this.page_size,
                    manager: this.user,
                    condition: this.searchValue
                }
                this.$axios
                    .post(this.Ip + '/CactusProject', datas)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.projectList = res.data.content
                            window.sessionStorage.removeItem('proj_id')
                            window.sessionStorage.removeItem('proj_name')
                        } else {
                            if (res.data.error == '') {
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
                    })
                    .catch(err => {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '服务异常'
                        })
                    })
            } else {
                let datas = {
                    accessToken: this.token,
                    page: this.page,
                    size: this.page_size,
                    manager: this.user
                }
                this.$axios
                    .post(this.Ip + '/CactusProject', datas)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.projectList = res.data.content
                            window.sessionStorage.removeItem('proj_id')
                            window.sessionStorage.removeItem('proj_name')
                        } else {
                            if (res.data.error == '') {
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
                    })
                    .catch(err => {
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
.badesign .el-tag {
    margin-right: 10px;
    margin-top: 5px;
}
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
    padding-right: 47px;
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
    right: 47px;
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
