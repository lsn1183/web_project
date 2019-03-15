<template>
    <div class="wrapper">
        <div class="operate-header">
            <div class="operate-header-title">
                <h2 class="title">自定义字段管理
                    <!-- <div class="operate-btn-bar">
                        [
                        <span @click="show_diff_field_dialog('add')">添加自定义字段</span> ]&nbsp;&nbsp; [
                        <span @click="show_bulk_delete_hint()">批量删除</span> ] 
                    </div> -->
                    <div class="operate-btn-bar">
                        <i class="el-icon-more" v-popover:parent_info_pop></i>
                        <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                            <p class="operate-display-icon" @click="show_diff_field_dialog('add')">添加自定义字段</p>
                            <p class="operate-display-icon" @click="show_bulk_delete_hint()"> 批量删除</p>
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

                            <div class="filter-select" v-if="item.type === 'is_show' && item.checked">
                                <input type="checkbox" v-model="item.content" class="input-checkbox">
                            </div>

                            <div class="filter-select" v-if="!(item.type === 'is_show') && item.checked ">
                                <el-select size="mini" v-model="item.option">
                                    <el-option v-for="(item, index) in fliter_options" :key="index" :label="item.label" :value="item.value">
                                    </el-option>
                                </el-select>
                            </div>
                            <input v-model="item.content" class="input-text" v-if="!(item.type === 'is_show') && item.checked">
                        </div>
                    </div>
                </div>
            </fieldset>

            <div class="filter-option-bar">
                <!-- <el-button size="mini" @click="search_detial_field()" type="primary">{{$t('table.apply')}}</el-button>
                <el-button size="mini" @click="empty_search_option()" type="primary">{{$t('table.cancel')}}</el-button> -->
                <span class="filter-option-bar-btn" @click="search_detial_field()">
                    <i class="el-icon-check"></i> {{$t('table.apply')}}</span>
                <span class="filter-option-bar-btn" @click="empty_search_option()">
                    <i class="el-icon-refresh"></i> {{$t('table.clear')}}</span>
            </div>

            <el-table :data="custom_field_list" border style="width: 100%" size="mini" @selection-change="handle_select_change" :max-height="table_max_height">
                <el-table-column type="selection" width="35" align="center">
                </el-table-column>
                <el-table-column prop="sort_num" label="显示次序" align="center">
                </el-table-column>
                <el-table-column prop="name" label="名称" align="center">
                </el-table-column>
                <el-table-column prop="type" label="类型" align="center">
                </el-table-column>
                <el-table-column label="选项" align="center">
                    <template slot-scope="scope">
                        <span v-for="(item, index) in scope.row.option_list" :key="index">
                            {{item.value}}
                        </span>
                    </template>
                </el-table-column>
                <el-table-column prop="is_show" label="显示" align="center">
                    <template slot-scope="scope">
                        <el-checkbox v-model="scope.row.is_show" disabled></el-checkbox>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="200" align="center">
                    <template slot-scope="scope">
                        <span class="btn-operate" @click="show_diff_field_dialog('edit', scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span>
                        <span class="btn-operate" @click="show_del_confirm(scope.row)"> &nbsp;[ {{$t('table.delete')}} ]</span>
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
    get_custom_field_list,
    edit_custom_field,
    add_custom_field,
    del_custom_field,
    get_detail_field,
    del_batch_field
} from '@/api/backstage'
import { get_user_permission_list_fun, } from '@/api/backstage'
export default {
    name: 'CustomShow',
    data () {
        return {
            page: 1,
            page_size: 20,
            count: 0,
            custom_field_list: [],
            show_dialog_type: '',
            field_form: {
                id: null,
                is_show: false,
                name: '',
                type: '',
                option_list: []
            },
            rules: {
                name: [{ required: true, message: '请输入名称', trigger: 'change' }],
                type: [{ required: true, message: '请输入类型', trigger: 'change' }]
            },
            add_options: '',
            filter_value: '',
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
                    value: 'name',
                    label: '名称'
                },
                {
                    value: 'type',
                    label: '类型'
                },
                {
                    value: 'is_show',
                    label: '是否在执行时显示'
                }
            ],
            filter_condition: [
                {
                    checked: true,
                    type: 'name',
                    label: '名称',
                    content: '',
                    option: '包含'
                }
            ],
            batch_del_list: [],
            table_max_height: window.innerHeight - 235
        }
    },
    created () {
        this.get_custom_field()
        this.edit_options_disabled()
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
        show_bulk_delete_hint () {
            let perm_data = {
                "user_name": this.$store.getters.name,
                "per_name": "自定义字段管理"
            }
            get_user_permission_list_fun(perm_data).then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {

                    if (this.batch_del_list.length === 0) {
                        this.$message({
                            message: '请选择数据',
                            type: 'warning'
                        })
                        return
                    }
                    if (this.batch_del_list.length !== 0) {
                        this.$confirm('此操作将永久删除已选中数据, 是否继续?', this.$t('operateTips.tips'), {
                            confirmButtonText: this.$t('table.confirm'),
                            cancelButtonText: this.$t('table.cancel'),
                            type: 'warning'
                        }).then(() => {
                            let batch_del_list = { dellist: JSON.parse(JSON.stringify(this.batch_del_list)) }
                            del_batch_field(batch_del_list).then(() => {
                                this.$message({
                                    message: this.$t('operateTips.delSuccess'),
                                    type: 'success'
                                })
                                this.get_custom_field()
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
            this.batch_del_list = val.map(item => {
                return item.id
            })
        },
        search_detial_field () {
            var list_filter_condition = this.filter_condition.filter(item => {
                if (item.type === 'is_show') {
                    item.option = '等于'
                    if (item.content === '') {
                        item.content = false
                    }
                }

                return item.checked === true
            })
            if (list_filter_condition.length === 0) {
                this.req_country()
            } else {
                // let list_filter_condition1 = { filter_condition: list_filter_condition }
                get_detail_field(list_filter_condition).then(res => {
                    this.custom_field_list = res.data
                })
            }
        },
        empty_search_option () {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'name',
                    label: '名称',
                    content: '',
                    option: '包含'
                }
            ]
            this.get_custom_field()
            this.edit_options_disabled()
        },
        fold () {
            this.filterFlag = !this.filterFlag
        },
        get_custom_field () {
            get_custom_field_list().then(res => {
                this.custom_field_list = res.data
            })
        },
        handle_close () {
            let filed_form_name = 'filedForm'
            this.$refs[filed_form_name].resetFields()
            this.clean_form_content()
        },
        clean_form_content () {
            this.field_form = {
                id: '',
                name: '',
                type: '',
                is_show: '',
                option_list: []
            }
        },
        show_diff_field_dialog (val, row) {
            let perm_data = {
                "user_name": this.$store.getters.name,
                "per_name": "自定义字段管理"
            }
            get_user_permission_list_fun(perm_data).then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {

                    this.$store.dispatch('setOperationType', val)
                    if (val === 'edit') {
                        this.$store.dispatch('setOperationData', row)
                        this.$router.push('/backstage/customManage/edit')
                    } else {
                        this.$router.push('/backstage/customManage/add')
                    }

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        add_field_options () {
            if (this.add_options !== '') {
                let add_options = { id: null, value: this.add_options }
                this.add_options = ''
                this.field_form.option_list.push(add_options)
            }
        },
        del_tag (index) {
            this.field_form.option_list.splice(index, 1)
        },
        empty_dialog_req_table (fieldForm) {
            this.$refs[fieldForm].resetFields()
            this.get_custom_field()
        },
        cancel (fieldForm) {
            this.$refs[fieldForm].resetFields()
            this.clean_form_content()
        },
        confirm_submit (fieldForm) {
            let dialog_type = this.show_dialog_type
            let data = this.field_form
            this.$nextTick(() => {
                this.$refs[fieldForm].validate(valid => {
                    if (valid) {
                        if (dialog_type === 'add') {
                            add_custom_field(data).then(() => {
                                this.$message({
                                    message: this.$t('operateTips.editSuccess'),
                                    type: 'success'
                                })
                                this.empty_dialog_req_table(fieldForm)
                            })
                        } else if (dialog_type === 'edit') {
                            edit_custom_field(data).then(() => {
                                this.$message({
                                    message: this.$t('operateTips.editSuccess'),
                                    type: 'success'
                                })
                                this.empty_dialog_req_table(fieldForm)
                            })
                        } else {
                            // do nothing
                        }
                    }
                })
            })
        },
        show_del_confirm (data) {
            let perm_data = {
                "user_name": this.$store.getters.name,
                "per_name": "自定义字段管理"
            }
            get_user_permission_list_fun(perm_data).then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {

                    this.$confirm('此操作将永久删除已选中数据, 是否继续?', this.$t('operateTips.tips'), {
                        confirmButtonText: this.$t('table.confirm'),
                        cancelButtonText: this.$t('table.cancel'),
                        type: 'warning'
                    }).then(() => {
                        del_custom_field(data).then(() => {
                            this.$message({
                                message: this.$t('operateTips.delSuccess'),
                                type: 'success'
                            })
                            this.get_custom_field()
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
        list_page_change () { }
    }
}
</script>
<style lang="scss" scoped>
</style>