<template>
    <div class="wrapper">
        <div class="operate-header">
            <div class="operate-header-title">
                <h2 class="title">国家管理
                    <!-- <div class="operate-btn-bar">
                        [
                        <span @click="show_add_country_dialog()">{{$t('country.addCountry')}}</span> ]&nbsp;&nbsp; [
                        <span @click="show_del_batch_country_tips()">批量删除</span> ]&nbsp;&nbsp;
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
                            <p class="operate-display-icon" @click="show_add_country_dialog()">{{$t('country.addCountry')}}</p>
                            <p class="operate-display-icon" @click="show_del_batch_country_tips()"> 批量删除</p>
                            <p class="operate-display-icon"  v-show="show_import_flag">
                                <el-upload style="display: inline-block;" class="upload-demo" :action="upload_address" :on-success="import_success" :show-file-list=false>
                                    <span class=""> {{$t('table.import')}} </span>
                                </el-upload>
                            </p>
                            <p class="operate-display-icon" @click="export_excel()">{{$t('table.export')}}</p>
                        </el-popover>
                    </div>
                </h2>
                <p class="title-detail">
                    <span>{{$t('country.title_summary')}}</span>
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
                        <el-select size="mini" v-model="filter_value" @change="add_filter()">
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
                <!-- <el-button size="mini" @click="search_detail_country()" type="primary">{{$t('table.apply')}}</el-button>
                <el-button size="mini" @click="empty_search_option()" type="primary">{{$t('table.cancel')}}</el-button> -->
                <span class="filter-option-bar-btn" @click="search_detail_country()">
                    <i class="el-icon-check"></i> {{$t('table.apply')}}</span>
                <span class="filter-option-bar-btn" @click="empty_search_option()">
                    <i class="el-icon-refresh"></i> {{$t('table.clear')}}</span>
            </div>

            <el-table :data="countryTable" border style="width: 100%" @selection-change="handle_select_change" size="mini" :max-height="table_max_height">
                <el-table-column type="selection" width="35" align="center">
                </el-table-column>
                <el-table-column prop="code" label="ISO三位国家代码" align="center" width="200px">
                </el-table-column>
                <el-table-column prop="en_name" :label="$t('country.countryEnName')" align="center">
                </el-table-column>
                <el-table-column prop="cn_name" :label="$t('country.countryCnName')" align="center">
                </el-table-column>

                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <span class="btn-operate" @click="show_edit_country_dialog(scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span>
                        <span class="btn-operate" @click="show_del_country_tips(scope.row)"> &nbsp;[ {{$t('table.delete')}} ]</span>
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
import {
    get_country_list,
    add_country,
    submit_del_country,
    edit_country,
    export_country_excel,
    get_detail_country,
    del_batch_country
} from '@/api/backstage'
import address from '@/utils/address'
import { get_user_permission_list_fun, } from '@/api/backstage'
export default {
    name: 'CountryShow',
    data () {
        return {
            page: 1,
            page_size: 20,
            count: 0,
            upload_address: address + 'api/1.0/testmanage/ImportExcle',
            isShowDialog: false,
            countryTable: [],
            searchValue: '',
            filter_value: '',
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
                    value: 'en_name',
                    label: '国家英文名称'
                },
                {
                    value: 'cn_name',
                    label: '国家中文名称'
                },
                {
                    value: 'code',
                    label: 'ISO三位国家代码'
                }
            ],
            filter_condition: [
                {
                    checked: true,
                    type: 'en_name',
                    label: '国家英文名称',
                    content: '',
                    option: '包含'
                }
            ],
            table_max_height: window.innerHeight - 235,
            batch_del_country: [],
            show_import_flag :false
        }
    },
    created () {
        this.req_country()
        this.edit_options_disabled()
        this.req_import_flag_fun()
    },
    destroyed () {
        window.sessionStorage.removeItem('save_data_str') //清除编辑页面保存的session
    },
    mounted () {
        const that = this
        window.onresize = () => {
            return (() => {
                that.table_max_height = window.innerHeight - 235
            })()
        }
    },
    methods: {
        req_import_flag_fun (){
            get_user_permission_list_fun(this.$store.getters.name, "国家管理/导入").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.show_import_flag = true
                } else {
                    
                    this.show_import_flag = false
                }
            })
        },
        req_country () {
            get_country_list().then(res => {
                this.countryTable = res.data
            })
        },
        show_add_country_dialog () {
            get_user_permission_list_fun(this.$store.getters.name, "国家管理/添加").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.submitType = { type: 'add' }
                    let routerValue = {
                        path: '/backstage/countryManage/add',
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
        show_edit_country_dialog (row) {
            get_user_permission_list_fun(this.$store.getters.name, "国家管理/编辑").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.submitType = 'edit'
                    this.countryForm = row
                    this.countryForm.type = 'edit'
                    let routerValue = {
                        path: '/backstage/countryManage/edit',
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
        show_del_country_tips (row) {
            get_user_permission_list_fun(this.$store.getters.name, "国家管理/删除").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.$confirm('此操作将永久删除此条记录, 是否继续?', this.$t('operateTips.tips'), {
                        confirmButtonText: this.$t('table.confirm'),
                        cancelButtonText: this.$t('table.cancel'),
                        type: 'warning'
                    }).then(() => {
                        submit_del_country(row).then(() => {
                            this.$message({
                                message: this.$t('operateTips.delSuccess'),
                                type: 'success'
                            })
                            this.req_country()
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
                            add_country(this.countryForm).then(() => {
                                this.$message({
                                    message: this.$t('operateTips.addSuccess'),
                                    type: 'success'
                                })
                                this.$refs[countryForm].resetFields()
                                this.req_country()
                            })
                        } else if (this.submitType === 'edit') {
                            edit_country(this.countryForm).then(() => {
                                this.$message({
                                    message: this.$t('operateTips.editSuccess'),
                                    type: 'success'
                                })
                                this.$refs[countryForm].resetFields()
                                this.req_country()
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
                this.req_country()
            } else {
                this.$alert('上传失败，请重新导入', '提示')
            }
        },
        export_excel () {
            get_user_permission_list_fun(this.$store.getters.name, "国家管理/导出").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    export_country_excel().then(res => {
                        let blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
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

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        fold () {
            this.filterFlag = !this.filterFlag
        },
        search_detail_country () {
            let list_filter_condition = this.filter_condition.filter(item => {
                return item.checked === true
            })
            if (list_filter_condition.length === 0) {
                this.req_country()
            } else {
                let obj_filter_condition = { filter_condition: list_filter_condition }
                get_detail_country(list_filter_condition).then(res => {
                    this.countryTable = res.data
                })
            }
        },
        empty_search_option () {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'en_name',
                    label: '国家英文名称',
                    content: '',
                    option: '包含'
                }
            ]
            this.edit_options_disabled()
            this.req_country()
        },
        show_del_batch_country_tips () {
            get_user_permission_list_fun(this.$store.getters.name, "国家管理/删除").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    if (this.batch_del_country.length === 0) {
                        this.$message({
                            message: '请选择数据',
                            type: 'warning'
                        })
                        return
                    }
                    if (this.batch_del_country.length !== 0) {
                        this.$confirm('此操作将永久删除已选中数据, 是否继续?', this.$t('operateTips.tips'), {
                            confirmButtonText: this.$t('table.confirm'),
                            cancelButtonText: this.$t('table.cancel'),
                            type: 'warning'
                        }).then(() => {
                            let batch_del_list = { dellist: JSON.parse(JSON.stringify(this.batch_del_country)) }
                            del_batch_country(batch_del_list).then(() => {
                                this.$message({
                                    message: this.$t('operateTips.delSuccess'),
                                    type: 'success'
                                })
                                this.req_country()
                            })
                        })
                    } else {
                        this.$message({
                            message: this.$t('operateTips.delWarning'),
                            type: 'warning'
                        })
                        return
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
            this.batch_del_country = val.map(item => {
                return item.id
            })
        },
        list_page_change (val) { }
    }
}
</script>
<style lang="scss" scoped>
</style>
