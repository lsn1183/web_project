<template>
    <div class="wrapper">
        <div class="operate-header">
            <div class="operate-header-title">
                <h2 class="title">模块管理
                    <!-- <div class="operate-btn-bar">
                        [
                        <span @click="add_module()">{{$t('moduleManage.addModule')}}</span> ]&nbsp;&nbsp; [
                        <span @click="del_batch_country_tips()">批量删除</span> ]&nbsp;&nbsp;
                        <el-upload style="display: inline-block;" class="upload-demo" :action="upload_address" :on-success="import_success" :show-file-list=false>
                            [
                            <span class=""> {{$t('table.import')}} </span>]&nbsp;&nbsp;
                        </el-upload>
                        [
                        <span @click="export_excel()">{{$t('table.export')}}</span> ]
                    </div> -->
                    <div class="operate-btn-bar">
                        <i class="el-icon-more" v-popover:parent_info_pop></i>
                        <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                            <p class="operate-display-icon" @click="add_module()">{{$t('moduleManage.addModule')}}</p>
                            <p class="operate-display-icon" @click="del_batch_country_tips()"> {{$t('projectManage.batch_delete')}}</p>
                            <p class="operate-display-icon" v-show="show_import_flag">
                                <el-upload style="display: inline-block;" class="upload-demo" :action="upload_address" :on-success="import_success" :show-file-list=false>
                                    <span class=""> {{$t('table.import')}} </span>
                                </el-upload>
                            </p>
                            <p class="operate-display-icon" @click="export_excel()">{{$t('table.export')}}</p>
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
                    <div class="add-filter">
                        {{$t('country.addFilter')}}:
                        <el-select size="mini" v-model="fliter_value" @change="add_filter()">
                            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item" :disabled="item.disabled">
                            </el-option>
                        </el-select>
                    </div>

                    <div class="filters-content">
                        <div v-for="(item, index) in filter_condition" :key="index" class="filters-content-field">
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

                <span class="filter-option-bar-btn" @click="search_detial_module()">
                    <i class="el-icon-check"></i> {{$t('table.apply')}}</span>
                <span class="filter-option-bar-btn" @click="empty_search_option()">
                    <i class="el-icon-refresh"></i> {{$t('table.clear')}}</span>
            </div>

            <el-table :data="moduleTable" border style="width: 100%" @selection-change="handle_select_change" size="mini" :max-height="table_max_height">
                <el-table-column type="selection" width="35" align="center">
                </el-table-column>
                <el-table-column prop="parent_proj.name" label="项目名" align="center">
                </el-table-column>
                <el-table-column prop="parent_model.model_name" label="父模块名" align="center">
                </el-table-column>
                <el-table-column prop="model_name" label="模块名" align="center">
                </el-table-column>
                <el-table-column prop="charger" label="负责人" align="center">
                </el-table-column>
                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <span class="btn-operate" @click="add_children_module(scope.row)"> &nbsp;[ {{$t('moduleManage.add_children_module')}} ]</span>
                        <span class="btn-operate" @click="edit_module(scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span>
                        <span class="btn-operate" @click="del_module(scope.row)"> &nbsp;[ {{$t('table.delete')}} ]</span>
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
import { get_module_list, delete_module, del_batch_module, get_detail_module, get_user_permission_list_fun } from '@/api/backstage'
import ip from '@/utils/address'
export default {
    name: 'ModuleShow',
    data () {
        return {
            moduleTable: [],
            upload_address: ip + 'api/1.0/testmanage/ImportExcle',
            isShowDialog: false,
            countryTable: [],
            searchValue: '',
            fliter_value: '',
            countryForm: {
                id: '',
                code: '',
                cn_name: '',
                en_name: ''
            },
            rules: {
                code: [{ required: true, message: this.$t('country.counrtyCodeTips'), trigger: 'change' }],
                cn_name: [{ required: true, message: this.$t('country.countryCnNameTips'), trigger: 'change' }],
                en_name: [{ required: true, message: this.$t('country.countryEnNameTips'), trigger: 'change' }]
            },
            submitType: '',
            filterFlag: false,
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
            options: [
                {
                    value: 'module_name',
                    label: '模块名称'
                },
                {
                    value: 'user_name',
                    label: '负责人名称'
                }
            ],
            filter_condition: [
                {
                    checked: true,
                    type: 'name',
                    label: '模块名称',
                    content: '',
                    option: '包含'
                }
            ],
            optimal_table_height: window.innerHeight - 235,
            batch_del_module: [],
            page: 1,
            page_size: 20,
            count: 0,
            table_max_height: window.innerHeight - 235,
            proj_id: this.$store.getters.proj_id,
            show_import_flag :false
        }
    },
    created () {
        this.req_module()
        this.edit_options_disabled()
    },
    activated () {
        this.proj_id = this.$store.getters.proj_id
        this.req_module()
        this.edit_options_disabled()
        this.req_import_flag_fun()
    },
    mounted () {
        const that = this
        window.onresize = () => {
            return (() => {
                that.table_max_height = window.innerHeight - 235
            })()
        }
        // this.on_resize_get_height()
    },
    methods: {
        req_import_flag_fun (){
            get_user_permission_list_fun(this.$store.getters.name, "模块管理/导入").then(res => {
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
        req_module () {
            const proj_id = this.proj_id
            return new Promise((resolve, reject) => {
                get_module_list(proj_id)
                    .then(res => {
                        this.moduleTable = res.data
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        add_module () {
            get_user_permission_list_fun(this.$store.getters.name, "模块管理/添加").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.submitType = { type: 'add' }
                    let routerValue = {
                        path: '/backstage/moduleManage/add',
                        query: { params: JSON.stringify(this.submitType) }
                    }
                    this.$router.push(routerValue)
                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        edit_module (row) {
            this.submitType = 'edit'
            this.countryForm = row
            this.countryForm.type = 'edit'
            let user_name = sessionStorage.getItem("UserName")
            get_user_permission_list_fun(this.$store.getters.name, "模块管理/编辑").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    let routerValue = {
                        path: '/backstage/moduleManage/edit',
                        query: { params: JSON.stringify(this.countryForm) }
                    }
                    this.$router.push(routerValue)

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        add_children_module (row) {
            // console.log(row, 'row')
            this.submitType = 'add_children'
            // this.countryForm = row
            // this.countryForm.type = 'add_children'

            let add_children_data = {
                charger: row.charger,
                create_datetime: row.create_datetime,
                field_list: row.field_list,
                id: row.id,
                model_intro: '',
                model_name: '',
                parent_model: row.parent_model,
                parent_model_name: row.model_name,
                parent_proj: row.parent_proj,
                type: 'add_children',
                update_datetime: row.update_datetime,
                user_name: row.user_name
            }
            // console.log(add_children_data, 'add_children_data')
            get_user_permission_list_fun(this.$store.getters.name, "模块管理/添加").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    let routerValue = {
                        path: '/backstage/moduleManage/add',
                        query: { params: JSON.stringify(add_children_data) }
                    }
                    this.$router.push(routerValue)
                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        del_module (row) {
            get_user_permission_list_fun(this.$store.getters.name, "模块管理/删除").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.$confirm('此操作将永久删除此条记录, 是否继续?', this.$t('operateTips.tips'), {
                        confirmButtonText: this.$t('table.confirm'),
                        cancelButtonText: this.$t('table.cancel'),
                        type: 'warning'
                    }).then(() => {
                        return new Promise((resolve, reject) => {
                            delete_module(row.id)
                                .then(res => {
                                    this.$message({
                                        message: this.$t('operateTips.delSuccess'),
                                        type: 'success'
                                    })
                                    this.req_module()
                                })
                                .catch(err => {
                                    reject(err)
                                })
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
        confirm_submit (countryForm) {
            this.$nextTick(function () {
                this.$refs[countryForm].validate(valid => {
                    if (valid) {
                        if (this.submitType === 'add') {
                            return new Promise((resolve, reject) => {
                                add_country(this.countryForm)
                                    .then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.addSuccess'),
                                            type: 'success'
                                        })
                                        this.$refs[countryForm].resetFields()
                                        this.req_module()
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        } else if (this.submitType === 'edit') {
                            return new Promise((resolve, reject) => {
                                edit_country(this.countryForm)
                                    .then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.editSuccess'),
                                            type: 'success'
                                        })
                                        this.$refs[countryForm].resetFields()
                                        this.req_module()
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        } else {
                            // do nothing
                        }
                    } else {
                        return false
                    }
                })
            })
        },
        clean_form_content () {
            this.countryForm = {
                id: '',
                code: '',
                cn_name: '',
                en_name: ''
            }
        },
        add_filter () {
            let filter_value_copy = this.fliter_value
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
            this.fliter_value = ''
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
        import_success (res) {
            if (res == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.req_module()
            } else {
                this.$alert('上传失败，请重新导入', '提示')
            }
        },
        export_excel () {
            get_user_permission_list_fun(this.$store.getters.name, "模块管理/导出").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    return new Promise((resolve, reject) => {
                        export_country_excel()
                            .then(res => {
                                let blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
                                // console.log(blob)
                                const downloadElement = document.createElement('a')
                                let href = null
                                //兼容性
                                if ('msSaveOrOpenBlob' in navigator) {
                                    // IE
                                    href = window.navigator.msSaveOrOpenBlob(blob, 'CountryList.xlsx')
                                } else {
                                    // Chrome FireFox Edge
                                    href = window.URL.createObjectURL(blob)
                                    downloadElement.href = href
                                    downloadElement.download = 'CountryList.xlsx'
                                    document.body.appendChild(downloadElement)
                                    downloadElement.click()
                                    document.body.removeChild(downloadElement) // 下载完成移除元素
                                    window.URL.revokeObjectURL(href) // 释放掉blob对象
                                }
                            })
                            .catch(err => {
                                reject(err)
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
        on_resize_get_height () {
            window.onresize = () => {
                return () => {
                    this.set_optimal_table_height()
                }
            }
        },
        set_optimal_table_height () {
            let other_margin_height = 36
            let other_dom_height =
                document.getElementsByClassName('operate-header')[0].offsetHeight +
                document.getElementsByClassName('operate-bar')[0].offsetHeight
            let container_height = document.getElementsByClassName('backstage-manage-container')[0].offsetHeight - 20
            this.optimal_table_height = container_height - other_dom_height - other_margin_height
        },
        fold () {
            this.filterFlag = !this.filterFlag
        },
        search_detial_module () {
            let list_filter_condition = this.filter_condition.filter(item => {
                return item.checked === true
            })
            if (list_filter_condition.length === 0) {
                this.req_module()
            } else {
                let obj_filter_condition = { filter_condition: list_filter_condition }
                return new Promise((resolve, reject) => {
                    // console.log(list_filter_condition)
                    get_detail_module(list_filter_condition)
                        .then(res => {
                            // console.log(res)
                            this.moduleTable = res.data
                        })
                        .catch(err => {
                            reject(err)
                        })
                })
            }
        },
        empty_search_option () {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'name',
                    label: '模块名称',
                    content: '',
                    option: '包含'
                }
            ]
            this.edit_options_disabled()
            this.req_module()
        },
        del_batch_country_tips () {
            get_user_permission_list_fun(this.$store.getters.name, "模块管理/删除").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    if (this.batch_del_module.length !== 0) {
                        this.$confirm('此操作将永久删除已选中数据, 是否继续?', this.$t('operateTips.tips'), {
                            confirmButtonText: this.$t('table.confirm'),
                            cancelButtonText: this.$t('table.cancel'),
                            type: 'warning'
                        }).then(() => {
                            let obj_batch_del_module = { dellist: JSON.parse(JSON.stringify(this.batch_del_module)) }
                            // console.log(obj_batch_del_module)
                            return new Promise((resolve, reject) => {
                                del_batch_module(obj_batch_del_module)
                                    .then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.delSuccess'),
                                            type: 'success'
                                        })
                                        this.req_module()
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
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
        handle_select_change (val) {
            this.batch_del_module = val.map(item => {
                return item.id
            })
        },
        list_page_change (val) { }
    }
}
</script>
<style lang="scss" scoped>
</style>