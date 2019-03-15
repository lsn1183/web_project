<template>
    <div class="badesign" id="badesign_design" v-loading="loading_flag" :element-loading-text="loading_text">
        <div class="header">
            <span class="header-span" @keyup.enter="search_click(searchValue)">
                <el-input clearable @clear="clear_click()" v-on:input="clear_click()" size="small" :placeholder=placeholderTitle v-model="searchValue" class="input-with-select">
                    <el-button slot="append" icon="el-icon-search" @click="search_click(searchValue)"></el-button>
                </el-input>
            </span>
            <!-- <span class="append-span margin-right" @click="export_doc()" v-show="show_export_btn">[ 导出文档 ]</span>
                <span class="append-span" @click="check_module_personnel()" v-show="show_module_personnel_flag">[ 模块人员信息 ]</span>
                <span class="append-span" @click="add_basic()" v-show="show_add_titleFlag">[ 添加基本设计 ]</span>
                <span class="append-span" @click="add_detail()" v-show="show_detail_titleFlag">[ 添加详细设计 ]</span> -->
            <span class="margin-right">
                <i class="el-icon-more" v-popover:parent_info_pop v-show="show_module_personnel_flag"></i>
                <el-popover placement="bottom" ref='parent_info_pop' trigger="hover">
                    <span class="append-span" @click="add_basic()" v-show="show_add_titleFlag">[ 添加基本设计 ]</span>
                    <span class="append-span" @click="add_detail()" v-show="show_detail_titleFlag">[ 添加详细设计 ]</span>

                    <el-upload v-show="show_improt_Flag" :disabled='import_flag' ref="up_file" :show-file-list="show_file_flag" :data="import_data" :action="import_ip" :on-success='import_success' :before-upload="before_upload" :auto-upload='false' :on-change='on_change'>
                        <span @click="import_doc()" class="append-span" style="color:#606266">[ 导入文档 ]</span>
                    </el-upload>

                    <span class="append-span" @click="export_doc()" v-show="show_export_btn">[ 导出文档 ]</span>
                    <span class="append-span" @click="check_module_personnel()" v-show="show_module_personnel_flag">[ 模块人员信息 ]</span>
                </el-popover>
            </span>

        </div>
        <div class="main">
            <el-table :data="basicDesignList" style="width: 97%" border :max-height="adaptivePageHeight" :empty-text="emptyText">
                <el-table-column prop="doc_id" sortable label="文档编号" width='110' align='center' header-align='center'>
                </el-table-column>
                <el-table-column prop="model" sortable label="模块名称" align='center' header-align='center' min-width='50'>
                </el-table-column>
                <el-table-column prop="title" sortable label="标题" align='left' header-align='center' min-width='100'>
                    <template slot-scope="scope">
                        <span @click="Preview(scope.$index, scope.row)" class="go-doc-text">
                            {{scope.row.title}}
                        </span>
                    </template>
                </el-table-column>
                <el-table-column prop="summary" label="概述" align='left' header-align='center' min-width='200'></el-table-column>
                <el-table-column prop="doc_type" label="设计书类型" align='left' header-align='center' min-width='50'></el-table-column>
                <el-table-column prop="" label="操作" align='center' width=160 header-align='center'>
                    <template slot-scope="scope">
                        <span @click="Preview(scope.$index, scope.row)" class="column-span mg10">[ 详细 ]</span>
                        <span @click="delete_item(scope.$index, scope.row)" class="column-span">[ 删除 ]</span>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="form-page">
            <el-pagination id="list_page" @current-change="listPageChange" :current-page="page" :page-size="page_size" layout="total, prev, pager, next,jumper" :total="page_count"></el-pagination>
        </div>
        <el-dialog :title=dialog_title :visible.sync="dialogVisible" width="30%" :before-close="handleClose" :height=adaptivePageHeight>
            <el-table :data="dialog_list_data" style="width: 100%" border :max-height="adaptivePageHeight">
                <el-table-column prop="group_name" label="组">
                </el-table-column>
                <el-table-column prop="username" label="姓名">
                </el-table-column>
                <el-table-column prop="user_role" label="角色">
                </el-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="dialogVisible = false" size="mini">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
                <el-button type="primary" @click="dialogVisible = false" size="mini">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
            </span>
        </el-dialog>
    </div>
    <!-- <div class="badesign">
            <router-view></router-view>
        </div> -->
    <!-- </div> -->

</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    data () {
        return {
            basicDesignList: [],
            basic_deep_flag: false,
            deep_list: [{}],
            searchValue: "",
            page: 1,
            page_size: 50,
            page_count: 0,
            tableType: null,
            placeholderTitle: "请输入搜索的标题或概述",
            adaptivePageHeight: window.innerHeight - 200,
            getTreeId: "",
            show_add_titleFlag: false,
            show_detail_titleFlag: false,
            detailData: {},
            emptyText: "暂无点击",
            loading_flag: false,
            show_export_btn: false,
            show_module_personnel_flag: false,
            dialogVisible: false,
            dialog_title: '暂无数据',
            dialog_list_data: [],
            import_data: {},
            import_ip: this.Ip + "/WebImportDsDoc",
            import_flag: true,
            show_file_flag: false,
            show_improt_Flag: false,
            loading_text: '拼命加载中...'
        }
    },
    computed: {
        watchDevelopTree () {
            return this.$store.state.desk_id
        },
    },
    watch: {
        watchDevelopTree (val) {
            if (val) {
                if (val.type == "framework" || val.type == 'project') {
                    this.reqBasic_Fra_Pro_Data(val)
                    this.show_add_titleFlag = false
                    this.show_detail_titleFlag = false
                    this.show_export_btn = false
                    this.show_module_personnel_flag = false
                } else {
                    this.reqBasicDesignData()
                    this.detailData = val
                    this.show_export_btn = true
                    this.show_module_personnel_flag = true
                    if (val.type == 'BASIC' || val.type == 'DETAIL') {
                        this.show_improt_Flag = true
                        this.import_manage_fun()//当点击的是基本设计or详细设计时候请求用户的权限
                    } else {
                        this.show_improt_Flag = false
                    }
                }

            }
        },
    },
    mounted () {
        this.mounted_fun()
    },
    methods: {
        mounted_fun () {
            // 控制表格高度自适应：
            this.windowOnresize()
            // 用来解决路由切换后vuex监听不执行
            if (this.$route.query.params) {
                this.detailData = JSON.parse(this.$route.query.params)
                if (this.detailData.type == "framework" || this.detailData.type == "project") {
                    this.reqBasic_Fra_Pro_Data(this.detailData)
                    this.show_add_titleFlag = false
                    this.show_detail_titleFlag = false
                    this.show_export_btn = false
                    this.show_module_personnel_flag = false
                } else {
                    this.reqBasicDesignData()
                    this.show_export_btn = true
                    this.show_module_personnel_flag = true
                    if (this.detailData.type == 'BASIC' || this.detailData.type == 'DETAIL') {
                        this.show_improt_Flag = true
                        this.import_manage_fun()
                    } else {
                        this.show_improt_Flag = false
                    }
                }
            } else {
                window.sessionStorage.removeItem("treeNodeId")
                this.show_export_btn = false
                this.show_improt_Flag = false
            }
        },
        import_manage_fun () {
            let export_data = JSON.parse(this.$route.query.params)
            let datas = {
                "proj_id": export_data.proj_id,
                "model_id": export_data.model_id,
                'accessToken': window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_编辑') == true) {
                        this.import_flag = false//导入控制flag
                    } else {
                        this.import_flag = true
                        // this.$message({
                        //     type: "warning",
                        //     message: "您没有权限操作"
                        // })
                    }
                } else {
                    // this.$message({
                    //     type: "warning",
                    //     message: res.data.error
                    // })
                    this.loading_flag = false
                    this.import_flag = true

                }
            })
        },
        import_doc () {
            let export_data = JSON.parse(this.$route.query.params)
            this.import_data = {
                'proj_id': export_data.proj_id,
                'model_id': export_data.model_id,
                'creator': window.sessionStorage.getItem('Uall'),
                'doc_type': export_data.type
            };//上传携带的参数
            if (this.import_flag == true) {
                this.$message({
                    type: "warning",
                    message: "您没有权限操作"
                })
            }
        },
        on_change (file, fileList) {
            if (file) {
                if (this.import_flag == false) {
                    this.$refs.up_file.submit()//文件上传控制开关方法
                }
            }
        },
        before_upload (file) {
            // 检查文件是否符合：
            let file_type = file.type,
                regexp_sheet = RegExp(/.sheet/i),
                regexp_pdf = RegExp(/pdf/i),
                regexp_sheet_xlsm = RegExp(/.ms-excel/i);
            if (file_type.search(regexp_sheet) !== -1) {
                // open loading
                this.loading_text = '拼命导入中...'
                this.loading_flag = true
                return true
            } else if (file_type.search(regexp_pdf) !== - 1) {
                // open loading
                this.loading_text = '拼命导入中...'
                this.loading_flag = true
                return true
            } else if (file_type.search(regexp_sheet_xlsm) !== - 1) {
                // open loading
                this.loading_text = '拼命导入中...'
                this.loading_flag = true
                return true
            } else {
                this.$alert("您上传的文件格式不支持", '提示')
                return false
            }

        },
        import_success (response, file, fileList) {
            this.loading_flag = false
            if (response.result == 'OK') {
                this.$store.state.user_data = file.uid;//通知左边树刷新dom
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.mounted_fun()
            } else {
                this.$alert(response.error, '错误提示')
            }
        },
        export_doc () {
            if (this.$route.query.params) {
                let export_data = JSON.parse(this.$route.query.params)
                let datas = {
                    "proj_id": export_data.proj_id,
                    "model_id": export_data.model_id,
                    accessToken: window.sessionStorage.getItem('accessToken'),
                    "username": window.sessionStorage.getItem('Uall')
                };
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_编辑') == true) {
                            // open loading
                            this.loading_text = '拼命导出中...'
                            this.loading_flag = true
                            let routerPath = JSON.parse(this.$route.query.params)
                            switch (routerPath.type) {
                                case "DETAIL":
                                    this.export_Fun(1, routerPath)
                                    break;
                                case "BASIC":
                                    this.export_Fun(1, routerPath)
                                    break;
                                case "project":
                                    this.export_Fun(2, routerPath)
                                    break;
                                case "model":
                                    this.export_Fun(3, routerPath)
                                    break;
                                default:
                                    break;
                            }
                        } else {
                            this.$message({
                                type: "warning",
                                message: "您没有权限操作"
                            })
                        }
                    } else {
                        this.$message({
                            type: "warning",
                            message: res.data.error
                        })
                    }

                })
            }
        },
        export_Fun (val, data) {
            if (val == 1) {
                this.$axios.get(this.Ip + "/ExportDoc/" + data.proj_id + "/" + data.model_id + "/" + data.type).then(res => {
                    if (res.data.result == "OK") {
                        window.location.href = this.Ip + "/DownFile/" + res.data.file_path
                        var self = this
                        setTimeout(() => {
                            self.loading_flag = false
                        }, 500)
                    } else {
                        // do nothing
                        this.loading_flag = false
                        this.$message({
                            type: "error",
                            message: res.data.msg
                        })
                    }
                })
            } else if (val == 2) {
                this.$axios.get(this.Ip + "/ExportDoc/" + data.proj_id).then(res => {
                    if (res.data.result == "OK") {
                        window.location.href = this.Ip + "/DownFile/" + res.data.file_path
                        var self = this
                        setTimeout(() => {
                            self.loading_flag = false
                        }, 500)
                    } else {
                        // do nothing
                        this.loading_flag = false
                        this.$message({
                            type: "error",
                            message: res.data.msg
                        })
                    }
                })
            } else if (val == 3) {
                this.$axios.get(this.Ip + "/ExportDoc/" + data.proj_id + "/" + data.model_id).then(res => {
                    if (res.data.result == "OK") {
                        window.location.href = this.Ip + "/DownFile/" + res.data.file_path
                        var self = this
                        setTimeout(() => {
                            self.loading_flag = false
                        }, 500)
                    } else {
                        // do nothing
                        this.loading_flag = false
                        this.$message({
                            type: "error",
                            message: res.data.msg
                        })
                    }
                })
            }
        },
        reqBasic_Fra_Pro_Data (data) {
            this.tableType = 'normal'
            if (data.type == "framework") {
                // 点击平台的请求
                this.page_count = 0
                this.$axios.get(this.Ip + '/ModelDSDocByFw/' + this.page + "/" + this.page_size + "/" + data.framework_id).then(res => {
                    this.basicDesignList = res.data.content
                    this.page_count = res.data.count
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
                })
            } else {
                // 点击项目的请求
                this.page_count = 0
                this.$axios.get(this.Ip + '/ModelDSDocByPro/' + this.page + "/" + this.page_size + "/" + data.project_id).then(res => {
                    this.basicDesignList = res.data.content
                    this.page_count = res.data.count
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
                })
            }
        },
        reqBasicDesignData () {
            this.tableType = 'normal'
            if (window.sessionStorage.getItem("treeNodeId")) {
                this.getTreeId = JSON.parse(window.sessionStorage.getItem("treeNodeId"))
            } else {
                return
            }
            var docType = null
            this.show_add_titleFlag = false
            this.show_detail_titleFlag = false
            if (this.getTreeId) {
                if (this.getTreeId.type == "BASIC") {
                    this.show_add_titleFlag = true
                    this.show_detail_titleFlag = false
                    docType = "BASIC"
                } else if (this.getTreeId.type == "DETAIL") {
                    this.show_add_titleFlag = false
                    this.show_detail_titleFlag = true
                    docType = "DETAIL"
                }
                this.page_count = 0
                this.page = 1
                if (docType == null) {
                    this.$axios.get(this.Ip + '/ModelDSDoc/' + this.page + "/" + this.page_size + '/' + this.getTreeId.proj_id + '/' + this.getTreeId.model_id).then(res => {
                        if (res.data.result == "OK") {
                            this.basicDesignList = res.data.content
                            this.page_count = res.data.count
                        } else {
                            this.basicDesignList = []
                        }
                    }).catch(res => {
                        this.$message({
                            type: 'error',
                            message: '服务异常'
                        })
                    })
                } else {
                    this.$axios.get(this.Ip + '/ModelDSDoc/' + this.page + "/" + this.page_size + '/' + this.getTreeId.proj_id + '/' + this.getTreeId.model_id + "/" + docType).then(res => {
                        if (res.data.result == "OK") {
                            this.basicDesignList = res.data.content
                            this.page_count = res.data.count
                        } else {
                            this.basicDesignList = []
                        }
                    }).catch(res => {
                        this.$message({
                            type: 'error',
                            message: '服务异常'
                        })
                    })
                }
            } else {
                //默认在没有点击树时候，为空
                this.show_add_titleFlag = false
                this.basicDesignList = []
                this.page_count = 0
            }
        },
        add_basic () {
            if (this.$route.query.params) {
                let add_basic_data = JSON.parse(this.$route.query.params)
                let datas = {
                    "proj_id": add_basic_data.proj_id,
                    "model_id": add_basic_data.model_id,
                    accessToken: window.sessionStorage.getItem('accessToken'),
                    "username": window.sessionStorage.getItem('Uall')
                };
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                            // 基本设计传true
                            this.detailData.dbrfmFlag = true
                            this.$router.push({ path: '/tagl/add_basic_design', query: { params: JSON.stringify(this.detailData) } })
                        } else {
                            this.$message({
                                type: "warning",
                                message: "您没有权限操作"
                            })
                        }

                    } else {
                        // nothing to do
                        this.$message({
                            type: "warning",
                            message: res.data.error
                        })
                    }
                })

            }
        },
        add_detail () {
            if (this.$route.query.params) {
                let add_detail_data = JSON.parse(this.$route.query.params)
                let datas = {
                    "proj_id": add_detail_data.proj_id,
                    "model_id": add_detail_data.model_id,
                    accessToken: window.sessionStorage.getItem('accessToken'),
                    "username": window.sessionStorage.getItem('Uall')
                };
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                            // 详细设计传false
                            this.detailData.dbrfmFlag = false
                            this.$router.push({ path: '/tagl/add_detail_design', query: { params: JSON.stringify(this.detailData) } })
                        } else {
                            this.$message({
                                type: "warning",
                                message: "您没有权限操作"
                            })
                        }

                    } else {
                        // nothing to do
                        this.$message({
                            type: "warning",
                            message: res.data.error
                        })
                    }
                })
            }
        },
        delete_item (index, row) {
            // console.log(row, "row")
            let datas = {
                "proj_id": row.proj_id,
                "model_id": row.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_删除') == true) {
                        this.$confirm(this.globalData.hint.delete, '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(() => {
                            var commit_user = window.sessionStorage.getItem("Uall");
                            this.$axios.delete(this.Ip + '/DSDoc/' + row.doc_id + '/doc/' + commit_user).then(res => {
                                if (res.data.result == 'OK') {
                                    this.basicDesignList.splice(index, 1)
                                    this.$store.state.user_data = row.doc_id;
                                    this.$message({
                                        type: 'success',
                                        message: '删除成功!'
                                    })
                                } else {
                                    this.$message({
                                        showClose: true,
                                        type: 'error',
                                        message: '删除失败,' + res.data.error
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
                            message: "您没有权限操作"
                        })
                    }
                } else {
                    // nothing to do
                    this.$message({
                        type: "warning",
                        message: res.data.error
                    })
                }
            })

        },
        Preview (index, data) {
            var previewData = data
            let datas = {
                "proj_id": data.proj_id,
                "model_id": data.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_查看') == true) {
                        this.$store.state.previewDocId = data
                        // preview权限需要用的数据
                        window.sessionStorage.setItem("previewPurviewManageData", JSON.stringify(data))
                        this.$router.push({ path: '/tagl/File_design/Preview/' + data.doc_id, query: { preview: JSON.stringify(previewData) } })
                    } else {
                        this.$message({
                            type: "warning",
                            message: "您没有权限操作"
                        })
                    }
                } else {
                    // nothing to do
                    this.$message({
                        type: "warning",
                        message: res.data.error
                    })
                }
            })
        },
        search_click () {
            this.tableType = 'search'
            this.$axios.get(this.Ip + '/ModelDSDocQuery/' + this.page + "/" + this.page_size + "/" + this.searchValue).then(res => {
                if (res.data.result == 'OK') {
                    this.basicDesignList = res.data.content
                    this.page_count = res.data.count
                } else {
                    this.$message({
                        type: 'error',
                        showClose: true,
                        message: '无数据'
                    })
                    this.basicDesignList = []
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
            var val = this.$store.state.desk_id
            if (this.searchValue == "") {
                if (val.type == "framework" || val.type == 'project') {
                    this.reqBasic_Fra_Pro_Data(val)
                } else {
                    this.reqBasicDesignData()

                }
                return
            }
            this.reqBasicDesignData()
        },
        listPageChange (pageNum) {
            this.page = pageNum
            // 判断当前表格内容是搜索还是全体
            if (this.tableType == 'search') {
                this.$axios.get(this.Ip + '/ModelDSDocQuery/' + this.page + "/" + this.page_size + "/" + this.searchValue).then(res => {
                    this.basicDesignList = res.data.content
                    this.page_count = res.data.count
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
                })
            } else {
                this.$axios.get(this.Ip + '/ModelDSDoc/' + this.page + "/" + this.page_size).then(res => {
                    this.basicDesignList = res.data.content
                    this.page_count = res.data.count
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
                })
            }
        },
        windowOnresize () {
            this.adaptivePageHeight = window.innerHeight - 200
            const that = this
            window.onresize = () => {
                return (() => {
                    that.adaptivePageHeight = window.innerHeight - 200
                })()
            }
        },
        check_module_personnel () {
            let export_data = JSON.parse(this.$route.query.params)
            let datas = {
                "proj_id": export_data.proj_id,
                "model_id": export_data.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            // this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
            //     if (res.data.result == "OK") {
            //         var userPermissionData = res.data.content
            //         // console.log(datas,'ads')
            //         if (this.getCatusPurviewManage(userPermissionData, '设计书_查看') == true) {
            this.$axios.post(this.Ip + '/ModelGroupMessage', datas).then(res => {
                // console.log(res)
                if (res.data.result == 'OK') {
                    this.dialogVisible = true
                    this.dialog_title = "模块名：" + res.data.model_name
                    this.dialog_list_data = res.data.content
                } else {
                    this.$message({
                        type: "error",
                        message: "暂无信息"
                    })
                    this.dialog_list_data = []
                }
            })
            //         } else {
            //             this.$message({
            //                 type: "warning",
            //                 message: "您没有权限操作"
            //             })
            //         }
            //     } else {
            //         if (res.data.result == 'NG') {
            //             this.$message({
            //                 type: "error",
            //                 message: res.data.error,
            //             })
            //         }
            //     }
            // })
        },
        handleClose (done) {
            this.dialogVisible = false
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
}
.header {
    padding-top: 20px;
}
.main {
    margin: 20px 0 0 0;
}

.append-span {
    /* float: right; */
    /* margin-right: 20px; */
    display: block;
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
    color: #606266;
}

.margin-right {
    float: right;
    margin-right: 40px;
}
.mg10 {
    margin-left: 10px;
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
}
.column-span:hover {
    color: #6bcca0;
}

.form-page {
    position: absolute;
    bottom: 20px;
}
.header-span {
    display: inline-block;
    width: 50%;
}
.go-doc-text {
    cursor: pointer;
}
.go-doc-text:hover {
    color: #42b983;
}
li {
    list-style: none;
    margin: 10px 0 10px 0;
}
.el-dialog__body {
    padding: 20px;
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
        overflow-y: auto;
        width: 100%;
        height: 100%;
    }
}
</style>
