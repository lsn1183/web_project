<template>
    <div class="wrapper">
        <div class="operate-header">
            <div class="operate-header-title">
                <h2 class="title">项目管理
                    <!-- <div class="operate-btn-bar">
                        [ <span @click="go_project_modify_page('add')">添加项目</span> ]&nbsp;&nbsp;
                        [ <span @click="show_del_batch_country_tips()">批量删除</span> ]
                        <el-upload style="display: inline-block;" class="upload-demo" :action="upload_address" :on-success="import_success" :show-file-list=false>
                            [ <span class=""> {{$t('table.import')}} </span >]&nbsp;&nbsp;
                        </el-upload>
                    </div> -->
                    <div class="operate-btn-bar">
                        <i class="el-icon-more" v-popover:parent_info_pop></i>
                        <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                            <p class="operate-display-icon" @click="go_project_modify_page('add')">添加项目</p>
                            <p class="operate-display-icon" @click="show_del_batch_country_tips()"> 批量删除</p>
                            <p class="operate-display-icon" v-show="show_import_flag">
                                <el-upload style="display: inline-block;" class="upload-demo" :action="upload_address" :on-success="import_success" 
                                :show-file-list=false  :auto-upload=false ref="import_excel">
                                    <span class=""> {{$t('table.import')}} </span>
                                </el-upload>
                            </p>
                        </el-popover>
                    </div>

                </h2>
                <p class="title-detail">
                    <span>xxxxxxxxxxx</span>
                </p>
            </div>
        </div>
        <div class="wrapper-content-show-page wrapper-content-show-page-ex">
            <fieldset class="collapsible">
                <legend>
                    <i :class="filterFlag? 'el-icon-caret-right':'el-icon-caret-bottom'" @click="fold()"></i>{{$t('country.filter')}}
                </legend>
                <div v-show="!filterFlag">
                    <div class="filters-content">
                        <div class="add-filter">
                            {{$t('country.addFilter')}}:
                            <el-select size="mini" v-model="filter_value" @change="add_filter()">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item" :disabled="item.disabled">
                                </el-option>
                            </el-select>
                        </div>

                        <div v-for="item in filter_condition" class="filters-content-field">
                            <div class="filter-label">
                                <input type="checkbox" v-model="item.checked" class="input-checkbox">
                                <label>{{item.label}}</label>
                            </div>

                            <div class="filter-select" v-if="item.checked">
                                <el-select size="mini" v-model="item.option">
                                    <el-option v-for="(item, index) in fliter_options" :key="index" :label="item.label" :value="item.value">
                                    </el-option>
                                </el-select>
                            </div>
                            <input v-model="item.content" class="input-text" v-if="item.checked">
                        </div>
                    </div>
                </div>
            </fieldset>

            <div class="filter-option-bar">
                <!-- <el-button size="mini" type="primary" @click="search_detail_project()">{{$t('table.apply')}}</el-button>
                <el-button size="mini" type="primary" @click="empty_search_option()">{{$t('table.cancel')}}</el-button> -->
                <span class="filter-option-bar-btn" @click="search_detail_project()">
                    <i class="el-icon-check"></i> {{$t('table.apply')}}</span>
                <span class="filter-option-bar-btn" @click="empty_search_option()">
                    <i class="el-icon-refresh"></i> {{$t('table.clear')}}</span>
            </div>

            <el-table :data="proj_list" border style="width: 100%" @selection-change="handle_select_change" size="mini" :max-height="table_max_height">
                <el-table-column type="selection" width="35" align="center">
                </el-table-column>
                <el-table-column prop="name" label="项目名" align="center">
                </el-table-column>
                <el-table-column prop="intro" label="项目描述" align="center">
                </el-table-column>
                <el-table-column prop="charger" label="负责人" align="center">
                </el-table-column>
                <el-table-column label="操作" width="200" align="center">
                    <template slot-scope="scope">
                        <span class="btn-operate" @click="go_project_modify_page('edit', scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span>
                        <span class="btn-operate" @click="show_del_proj_tips(scope.row)"> &nbsp;[ {{$t('table.delete')}} ]</span>
                        <span class="btn-operate" @click="export_proj(scope.row)"> &nbsp;[ 导出 ]</span>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        
        <!-- <div class="wrapper-footer-pagination">
            <el-pagination @current-change="list_page_change" :current-page="page" :page-size="page_size" layout="total, prev, pager, next,jumper" :total="count"></el-pagination>
        </div> -->
    </div>
</template>
<script>
import { get_project_list, del_project, del_batch_project, get_detail_project, export_project } from '@/api/backstage'
import address from '@/utils/address'
import { get_user_permission_list_fun, } from '@/api/backstage'
export default {
    name: 'ProjectShow',
    data () {
        return {
            page: 1,
            page_size: 20,
            count: 0,
            upload_address: address + 'ImportYaml',
            proj_list: [],
            send_data: {
                type: '',
                proj_data: {}
            },
            filter_condition: [
                {
                    checked: true,
                    type: 'name',
                    label: '项目名称',
                    content: '',
                    option: '包含'
                }
            ],
            options: [
                {
                    value: 'name',
                    label: '项目名称'
                },
                {
                    value: 'user_name',
                    label: '负责人'
                }
            ],
            fliter_options: [
                {
                    value: '包含',
                    label: '包含'
                },
                {
                    value: '不包含',
                    label: '不包含'
                },
                {
                    value: '等于',
                    label: '等于'
                },
                {
                    value: '不等于',
                    label: '不等于'
                }
            ],
            filterFlag: false,
            filter_value: '',
            select_porj: [],
            table_max_height: window.innerHeight - 310,
            show_import_flag:false
        }
    },
    created () {
        this.edit_options_disabled()
        this.req_project()
        this.req_import_flag_fun()
    },
    mounted () {
        const that = this
        window.onresize = () => {
            return (() => {
                that.table_max_height = window.innerHeight - 310
            })()
        }
    },
    methods: {
        req_import_flag_fun (){
            get_user_permission_list_fun(this.$store.getters.name, "项目管理/导入").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.show_import_flag = true
                } else {
                    // this.$message({
                    //     type: "warning",
                    //     message: this.$t('title_text.permission_alert_text')
                    // })
                    this.show_import_flag = false
                }
            })
        },
        submitUpload () {
            this.$refs.upload.submit();
        },
        handleRemove (file, fileList) {
            console.log(file, fileList);
        },
        handlePreview (file) {
            console.log(file);
        },

       
        import_success (res) {
            if (res !== 'NG') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.req_project()
            } else {
                this.$alert('上传失败，请重新导入', '提示')
            }
        },
        req_project () {
            get_project_list().then(res => {
                this.proj_list = res.data
            })
        },
        export_excel () { },
        go_project_modify_page (val, row) {
            let permission_string = "项目管理/编辑"
            if (val == "add") {
                permission_string = "项目管理/添加"
            }
            console.log(permission_string, 'permission_string')
            get_user_permission_list_fun(this.$store.getters.name, permission_string).then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.$store.dispatch('setOperationType', val)
                    if (val === 'edit') {
                        this.$store.dispatch('setOperationData', row)
                        this.$router.push('/backstage/projectManage/edit')
                    } else {
                        this.$router.push('/backstage/projectManage/add')
                    }
                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        search_detail_project () {
            let check_checkout_data = this.filter_condition.filter(item => item.checked === true)
            get_detail_project(check_checkout_data).then(res => {
                this.proj_list = res.data
            })
        },
        edit_options_disabled () {
            this.options = this.options.map(item => {
                item.disabled = false
                return item
            })

            for (let item of this.filter_condition) {
                for (let item_options of this.options) {
                    if (item.type === item_options.value) {
                        item_options.disabled = true
                        break
                    }
                }
            }
        },
        fold () {
            this.filterFlag = !this.filterFlag
        },
        add_filter () {
            let filter_value_copy = this.filter_value
            let set = new Set(this.filter_condition)
            let hasTheSame = false
            for (let item of set.keys()) {
                hasTheSame = hasTheSame || item.type === filter_value_copy.value
            }
            if (!hasTheSame) {
                this.filter_condition.push({
                    checked: true,
                    type: filter_value_copy.value,
                    label: filter_value_copy.label,
                    content: '',
                    option: '包含'
                })
            }
            this.edit_options_disabled()
            this.filter_value = ''
        },
        empty_search_option () {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'name',
                    label: '项目名称',
                    content: '',
                    option: '包含'
                }
            ]
            this.edit_options_disabled()
            this.req_project()
        },
        show_del_proj_tips (row) {
            get_user_permission_list_fun(this.$store.getters.name, "项目管理/删除").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.$confirm('此操作将永久删除此条记录, 是否继续?', this.$t('operateTips.tips'), {
                        confirmButtonText: this.$t('table.confirm'),
                        cancelButtonText: this.$t('table.cancel'),
                        type: 'warning'
                    }).then(() => {
                        del_project(row).then(() => {
                            this.$message({
                                message: this.$t('operateTips.delSuccess'),
                                type: 'success'
                            })
                            this.req_project()
                        })
                    })

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        handle_select_change (val) {
            this.select_porj = val
        },
        show_del_batch_country_tips () {
            get_user_permission_list_fun(this.$store.getters.name, "项目管理/删除").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    if (this.select_porj.length === 0) {
                        this.$message({
                            message: '请选择数据',
                            type: 'warning'
                        })
                        return
                    }
                    if (this.select_porj.length !== 0) {
                        const data = {
                            dellist: this.select_porj.map(item => {
                                return item.id
                            })
                        }
                        this.$confirm('此操作将永久删除选中记录, 是否继续?', this.$t('operateTips.tips'), {
                            confirmButtonText: this.$t('table.confirm'),
                            cancelButtonText: this.$t('table.cancel'),
                            type: 'warning'
                        }).then(() => {
                            del_batch_project(data).then(() => {
                                this.$message({
                                    message: this.$t('operateTips.delSuccess'),
                                    type: 'success'
                                })
                                this.req_project()
                            })
                        })
                    }

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        export_proj (row) {
            get_user_permission_list_fun(this.$store.getters.name, "项目管理/导出").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    export_project(row).then(res => {
                        let blob = new Blob([res.data], { type: 'application/octet-stream' })
                        const downloadElement = document.createElement('a')
                        let href = null
                        //兼容性
                        if ('msSaveOrOpenBlob' in navigator) {
                            // IE
                            href = window.navigator.msSaveOrOpenBlob(blob, 'Project.yaml')
                        } else {
                            // Chrome FireFox Edge
                            href = window.URL.createObjectURL(blob)
                            downloadElement.href = href
                            downloadElement.download = 'Project.yaml'
                            document.body.appendChild(downloadElement)
                            downloadElement.click()
                            document.body.removeChild(downloadElement) // 下载完成移除元素
                            window.URL.revokeObjectURL(href) // 释放掉blob对象
                        }
                    })

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        list_page_change () { }
    }
}
</script>
<style lang="scss" scoped>
</style>