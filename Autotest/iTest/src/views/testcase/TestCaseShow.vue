<template>
    <div class="test-case-content">
        <div class="wrapper">
            <div class="operate-header">
                <div class="operate-header-title">
                    <h2 class="title">测试用例
                        <!-- <div class="operate-btn-bar">
                            <span @click="go_diff_page('add')" v-if="add_case_flag">[ 添加Case ]</span>&nbsp;&nbsp;
                            <span @click="show_bulk_delete_hint()">[ 批量删除 ]</span>&nbsp;&nbsp; -->
                        <!-- <el-upload style="display: inline-block;" class="upload-demo" :action="upload_address" :on-success="import_success" :show-file-list=false>
                                    [
                                    <span class=""> {{$t('table.import')}} </span>]&nbsp;&nbsp;
                                </el-upload> -->

                        <!-- <span>[ {{$t('table.import')}} ]</span>&nbsp;&nbsp;
                            <span v-if="tree_node_level > 1 ? true : false">[ {{$t('table.export')}} ]</span>
                        </div> -->

                        <div class="operate-btn-bar">
                            <i class="el-icon-more" v-popover:parent_info_pop></i>
                            <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                                <p class="operate-display-icon" @click="go_diff_page('add')" v-if="add_case_flag">添加测试用例</p>
                                <p class="operate-display-icon" @click="show_bulk_delete_hint()"> 批量删除</p>
                                <p class="operate-display-icon">{{$t('table.import')}}</p>
                                <!-- <p class="operate-display-icon">
                                    <el-upload style="display: inline-block;" class="upload-demo" :action="upload_address" :on-success="import_success" :show-file-list=false>
                                        <span class=""> {{$t('table.import')}} </span>
                                    </el-upload>
                                </p> -->
                                <p class="operate-display-icon" v-if="tree_node_level > 1 ? true : false" @click="export_excel">{{$t('table.export')}}</p>
                            </el-popover>
                        </div>
                    </h2>
                    <p class="title-detail">
                        <span>xxxxxxxxxxx</span>
                    </p>
                </div>
            </div>
            <div class="wrapper-content-show-page">
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
                                <div class="filter-label" style="width:130px;">
                                    <input type="checkbox" v-model="item.checked" class="input-checkbox">
                                    <label>{{item.label}}</label>
                                </div>

                                <div class="filter-select" v-if="item.checked">
                                    <el-select size="mini" v-model="item.option">
                                        <el-option v-for="(item, index) in fliter_options" :key="index" :label="item.label" :value="item.value">
                                        </el-option>
                                    </el-select>
                                </div>
                                <input v-model="item.content" class="input-text" v-if="item.checked"></input>
                            </div>
                        </div>
                    </div>
                </fieldset>

                <div class="filter-option-bar">
                    <span class="filter-option-bar-btn" @click="search_detail_testcase()">
                        <i class="el-icon-check"></i> 应用</span>
                    <span class="filter-option-bar-btn" @click="empty_search_option()">
                        <i class="el-icon-refresh"></i> 清除</span>
                </div>

                <el-table :data="test_case_list" border style="width: 100%" size="mini" @selection-change="handle_select_change" :max-height="table_max_height">
                    <el-table-column type="selection" width="35" align="center">
                    </el-table-column>
                    <el-table-column prop="title" label="标题" align="center">
                    </el-table-column>
                    <!-- <el-table-column prop="abstract" label="摘要" align="center">
                    </el-table-column>
                    <el-table-column prop="premise" label="前提" align="center">
                    </el-table-column> -->
                    <el-table-column prop="test_mode" label="测试方式" align="center">
                        <template slot-scope="scope">
                            <span v-if="scope.row.test_mode === 'automatically'">自动</span>
                            <span v-else>手动</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="charger" label="负责人" align="center">
                    </el-table-column>

                    <el-table-column label="操作" align="center">
                        <template slot-scope="scope">
                            <span class="btn-operate" @click="go_preview(scope.row)"> &nbsp;[ 预览 ]</span>
                            <span class="btn-operate" @click="go_diff_page('edit', scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span>
                            <span class="btn-operate" @click="show_del_hint(scope.row, scope.$index)"> &nbsp;[ {{$t('table.delete')}} ]</span>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div class="wrapper-footer-pagination">
                <el-pagination id="list_page" @current-change="list_page_change" :current-page="page" :page-size="20" layout="total, prev, pager, next,jumper" :total="total"></el-pagination>
                </el-pagination>
            </div>
        </div>

    </div>
</template>
<script>
import {
    get_all_case,
    get_proj_test_case,
    get_module_test_case,
    del_test_case,
    get_filter_data_about_all_case,
    get_filter_data_about_project,
    get_filter_data_about_module
} from '@/api/testcase'
import { get_user_permission_list_fun } from '@/api/backstage'

export default {
    name: 'testCaseShow',
    data() {
        return {
            page: this.$store.getters.test_case_page,
            filterFlag: false,
            filter_value: '',
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
                    value: 'title',
                    label: '标题'
                },
                // {
                //     value: 'abstract',
                //     label: '摘要'
                // },
                // {
                //     value: 'premise',
                //     label: '前提'
                // },
                {
                    value: 'test_mode',
                    label: '测试方式'
                },
                {
                    value: 'charge',
                    label: '负责人'
                }
            ],
            filter_condition: [
                {
                    checked: true,
                    type: 'title',
                    label: '标题',
                    content: '',
                    option: '包含'
                }
            ],
            test_case_list: [],
            total: 0,
            add_case_flag: false,
            bulk_delete_list: [],
            filter_flag: true, // 判断是否点击 ‘应用’按钮（应用为true,取消为false）
            table_max_height: window.innerHeight - 310,
            proj_id: this.$store.getters.proj_id
        }
    },
    computed: {
        tree_node_level() {
            return this.$store.getters.tree_node_level
        },
        tree_node_unique_id() {
            return this.$store.getters.tree_node_unique_id
        },
        tree_node_data_id() {
            return this.$store.getters.tree_node_data_id
        }
    },
    watch: {
        tree_node_level(val) {
            if (val > 1) {
                this.add_case_flag = true
            } else {
                this.add_case_flag = false
            }
        },
        tree_node_unique_id(value) {
            if(this.tree_node_data_id == 0) {
                this.total = 0
                this.page = 1
                 this.test_case_list = []
                return 
            }
            this.proj_id = this.tree_node_data_id
            if (this.tree_node_level === 1) {
                get_proj_test_case(this.proj_id, 1, 20).then(res => {
                    this.total = res.data.count
                    this.page = 1
                    this.test_case_list = res.data.result
                })
            } else if (this.tree_node_level > 1) {
                get_module_test_case(this.proj_id, 1, 20).then(res => {
                    this.total = res.data.count
                    this.page = 1
                    this.test_case_list = res.data.result
                })
            } else {
                // do nothing
            }
        },
        monitor_change() {}
    },
    created() {
        if (this.$store.getters.tree_node_level > 0) {
            this.add_case_flag = true
        }
        this.proj_id = this.$store.getters.tree_node_data_id
        this.edit_options_disabled()
    },
    activated() {
        if (this.$store.getters.nav_active_index == '2') {
            this.$store.dispatch('setTestCasePage', 1) // 在切换页面时，去除case page页码的记录
            this.proj_id = this.$store.getters.proj_id
            this.list_page_change(1)
            this.edit_options_disabled()
        }
    },
    mounted() {
        // this.$nextTick(() => {
        this.list_page_change(1)
        // })
        const that = this
        window.onresize = () => {
            return (() => {
                that.table_max_height = window.innerHeight - 310
            })()
        }
    },
    destroyed() {
        this.$store.dispatch('setTestCasePage', this.page)
    },
    methods: {
        search_detail_testcase() {
            this.filter_flag = true
            const data = this.filter_condition
            if (this.tree_node_level == 0) {
                // 全部testcase下
                get_filter_data_about_project(this.proj_id, 1, 30, data).then(res => {
                    this.total = res.data.count
                    this.test_case_list = res.data.result
                })
            } else if (this.tree_node_level == 1) {
                // 项目下
                get_filter_data_about_project(this.proj_id, 1, 30, data).then(res => {
                    this.total = res.data.count
                    this.test_case_list = res.data.result
                })
            } else {
                // 模块下
                get_filter_data_about_module(this.proj_id, 1, 30, data).then(res => {
                    this.total = res.data.count
                    this.test_case_list = res.data.result
                })
            }
        },
        empty_search_option() {
            if (this.filter_flag == false) {
                // 已经在取消状态下 无动作
            } else {
                // 在应用状态下， 恢复过滤前状态
                this.filter_flag == false
                this.empty_filter_condition()
            }
        },
        empty_filter_condition() {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'title',
                    label: '标题',
                    content: '',
                    option: '包含'
                }
            ]
            this.edit_options_disabled()
            this.search_detail_testcase()
        },
        handle_select_change(val) {
            this.bulk_delete_list = val
        },
        req_test_case_list() {
            // 条件1 : 项目下 、 模块下
            // 条件2 ： 项目id 、模块id
            // 条件3 ： 搜索完total变化 页数变1
            if (this.tree_node_level == 0) {
                // 所有case
            } else if (this.tree_node_level == 1) {
                // 项目下case
            } else {
                // 模块下case
            }
        },
        go_diff_page(val, row) {
            get_user_permission_list_fun(this.$store.getters.name, '测试计划创建/编辑').then(res => {
                if (res.data.flag == true) {
                    this.$store.dispatch('setOperationType', val)
                    if (val === 'edit') {
                        this.$store.dispatch('setTestCaseId', row.id)
                        this.$router.push('/testCase/edit')
                    } else {
                        this.$router.push('/testCase/add')
                    }
                } else {
                    return this.$message({
                        type: 'warning',
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })
        },
        go_preview(row) {
            get_user_permission_list_fun(this.$store.getters.name, '测试用例查看(只读)').then(res => {
                if (res.data.flag == true) {
                    this.$store.dispatch('setTestCaseId', row.id)
                    this.$router.push('/testCase/preview')
                } else {
                    return this.$message({
                        type: 'warning',
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })
        },
        list_page_change(page) {
            this.$store.dispatch('setTestCasePage', page)
            if (this.tree_node_level == 0) {
                // get_all_case(page, 20).then(res => {
                //     this.page = page
                //     this.total = res.data.count
                //     this.test_case_list = res.data.result
                // })
                get_proj_test_case(this.proj_id, page, 20).then(res => {
                    this.page = page
                    this.total = res.data.count
                    this.test_case_list = res.data.result
                })
            } else if (this.tree_node_level == 1) {
                get_proj_test_case(this.proj_id, page, 20).then(res => {
                    this.page = page
                    this.total = res.data.count
                    this.test_case_list = res.data.result
                })
            } else if (this.tree_node_level > 1) {
                get_module_test_case(this.proj_id, page, 20).then(res => {
                    this.page = page
                    this.total = res.data.count
                    this.test_case_list = res.data.result
                })
            } else {
                // do nothing
            }
        },
        fold() {
            this.filterFlag = !this.filterFlag
        },
        add_filter() {
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
        edit_options_disabled() {
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
        show_del_hint(row, index) {
            get_user_permission_list_fun(this.$store.getters.name, '删除执行的测试用例').then(res => {
                if (res.data.flag == true) {
                    this.$confirm('此操作将永久删除选中记录, 是否继续?', this.$t('operateTips.tips'), {
                        confirmButtonText: this.$t('table.confirm'),
                        cancelButtonText: this.$t('table.cancel'),
                        type: 'warning'
                    }).then(() => {
                        let data = { dellist: [row.id] }
                        del_test_case(data).then(() => {
                            this.$message({
                                message: this.$t('operateTips.delSuccess'),
                                type: 'success'
                            })
                            this.test_case_list.splice(index, 1)
                        })
                    })
                } else {
                    return this.$message({
                        type: 'warning',
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })
        },
        show_bulk_delete_hint() {
            get_user_permission_list_fun(this.$store.getters.name, '测试用例创建/编辑').then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    if (this.bulk_delete_list.length === 0) {
                        this.$message({
                            message: '请选择数据',
                            type: 'warning'
                        })
                        return
                    }
                    this.$confirm('此操作将永久删除选中记录, 是否继续?', this.$t('operateTips.tips'), {
                        confirmButtonText: this.$t('table.confirm'),
                        cancelButtonText: this.$t('table.cancel'),
                        type: 'warning'
                    }).then(() => {
                        let bulk_del_id_list = this.bulk_delete_list.map(item => item.id)
                        let data = { dellist: bulk_del_id_list }
                        return new Promise((resolve, reject) => {
                            del_test_case(data)
                                .then(() => {
                                    this.$message({
                                        message: this.$t('operateTips.delSuccess'),
                                        type: 'success'
                                    })

                                    for (let j = 0; j < bulk_del_id_list.length; j++) {
                                        for (let i = 0; i < this.test_case_list.length; i++) {
                                            if (bulk_del_id_list[j] == this.test_case_list[i].id) {
                                                this.test_case_list.splice(i, 1)
                                            }
                                        }
                                    }
                                })
                                .catch(err => {
                                    reject(err)
                                })
                        })
                    })
                } else {
                    return this.$message({
                        type: 'warning',
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })
        },
        export_excel() {
            get_user_permission_list_fun(this.$store.getters.name, '测试用例/导出').then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                } else {
                    return this.$message({
                        type: 'warning',
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })
        }
    }
}
</script>
<style lang="scss" scoped>
</style>