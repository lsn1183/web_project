<template>
    <div class="test-case">
        <div class="side-bar"></div>
        <div class="content">
            <div class="test-case-content">
                <div class="wrapper">
                    <div class="operate-header">
                        <div class="operate-header-title">
                            <h2 class="title">测试计划执行历史
                                <div class="operate-btn-bar">
                                    <i class="el-icon-more" v-popover:parent_info_pop></i>
                                    <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                                        <!-- <p class="operate-display-icon" @click="go_diff_page('add')">添加计划</p> -->
                                        <p class="operate-display-icon" @click="show_bulk_delete_hint()"> 批量删除</p>
                                    </el-popover>
                                </div>
                            </h2>
                            <p class="title-detail">
                                <span>xxxxxxxxxxx</span>
                            </p>
                        </div>
                    </div>
                    <div class="wrapper-content-show-page">
                        <!-- 过滤先隐藏，代码勿删 -->
                        <!-- <fieldset class="collapsible">
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
                        </fieldset> -->

                        <!-- <div class="filter-option-bar">
                            <span class="filter-option-bar-btn" @click="search_detail_testcase()">
                                <i class="el-icon-check"></i> 应用</span>
                            <span class="filter-option-bar-btn" @click="empty_search_option()">
                                <i class="el-icon-refresh"></i> 清除</span>
                        </div> -->

                        <el-table :data="test_case_table" border style="width: 100%" size="mini" @selection-change="handle_select_change" :max-height="table_max_height">
                            <el-table-column type="selection" width="35" align="center">
                            </el-table-column>
                            <el-table-column prop="title" label="名称" align="center">
                            </el-table-column>
                            <el-table-column prop="version" label="版本" align="center">
                            </el-table-column>
                            <el-table-column prop="user_name" label="创建人" align="center">
                            </el-table-column>
                            <el-table-column prop="time" label="执行日期" align="center">
                            </el-table-column>

                            <el-table-column label="操作" align="center" width="200">
                                <template slot-scope="scope">
                                    <span class="btn-operate" @click="go_execute_page(scope.row)"> &nbsp;[ 执行 ]</span>
                                    <!-- <span class="btn-operate" @click="go_diff_page('edit', scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span> -->
                                    <span class="btn-operate" @click="show_del_hint(scope.row, scope.$index)"> &nbsp;[ {{$t('table.delete')}} ]</span>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>

                    <div class="wrapper-footer-pagination">
                        <!-- <div style="display: inline-block;width: 90%;">
                            <el-pagination id="list_page" @current-change="list_page_change" :current-page="page" :page-size="20" layout="total, prev, pager, next,jumper" :total="total"></el-pagination>
                            </el-pagination>
                        </div> -->
                        <el-button @click="cancel()" size="small" style="float: right;">返回</el-button>
                    </div>
                </div>

            </div>

        </div>
    </div>

</template>
<script>
import { get_test_plan, del_test_plan, get_filter_data_about_test_plan, req_test_plan_history, del_tese_plan_history } from '@/api/testPlan'
export default {
    name: 'test-plan-history',
    data() {
        return {
            page: 1,
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
                    label: '名称'
                },
                {
                    value: 'user_name',
                    label: '创建人'
                }
            ],
            filter_condition: [
                {
                    checked: true,
                    type: 'title',
                    label: '名称',
                    content: '',
                    option: '包含'
                }
            ],
            test_case_table: [],
            total: 0,
            bulk_delete_list: [],
            filter_flag: true, // 判断是否点击 ‘应用’按钮（应用为true,取消为false）
            table_max_height: window.innerHeight - 200
        }
    },
    created() {
        // this.list_page_change(1, 20)
        const plan_id = this.$store.getters.test_plan_id
        this.get_plan_history(plan_id)
        this.edit_options_disabled()
    },
    mounted () {
        const that = this
        window.onresize = () => {
            return (() => {
                that.table_max_height = window.innerHeight - 200
            })()
        }
    },
    methods: {
        get_plan_history(plan_id) {
            req_test_plan_history(plan_id).then(res => {
                this.test_case_table = res.data.result
            })
        },
        search_detail_testcase() {
            this.filter_flag = true
            const data = this.filter_condition
            // 全部testcase下
            get_filter_data_about_test_plan(1, 30, data).then(res => {
                this.total = res.data.count
                this.test_case_table = res.data.result
            })
        },
        empty_search_option() {
            this.filter_flag == false
            this.list_page_change(1, 20)
            this.empty_filter_condition()
        },
        empty_filter_condition() {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'title',
                    label: '名称',
                    content: '',
                    option: '包含'
                }
            ]
            this.edit_options_disabled()
        },
        handle_select_change(val) {
            this.bulk_delete_list = val
        },
        go_diff_page(val, row) {
            if (val === 'edit') {
                this.$store.dispatch('setOperationData', row.id)
                this.$router.push('/testPlan/edit')
            } else {
                this.$router.push('/testPlan/add')
            }
        },
        go_execute_page(row) {
            this.$store.dispatch('setTestPlanId', row.plan_id)
            this.$store.dispatch('setTestPlanHistoryId', row.id)
            this.$router.push('/testPlan/execute')
        },
        list_page_change(page, size) {
            get_test_plan(page, size).then(res => {
                this.total = res.data.count
                this.test_case_table = res.data.result
            })
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
            this.$confirm('此操作将永久删除选中记录, 是否继续?', this.$t('operateTips.tips'), {
                confirmButtonText: this.$t('table.confirm'),
                cancelButtonText: this.$t('table.cancel'),
                type: 'warning'
            }).then(() => {
                let data = { dellist: [row.id] }
                del_tese_plan_history(data).then(() => {
                    this.$message({
                        message: this.$t('operateTips.delSuccess'),
                        type: 'success'
                    })
                    this.test_case_table.splice(index, 1)
                })
            })
        },
        cancel() {
            this.$router.push('/testPlan/testPlanShow')
        },
        show_bulk_delete_hint() {
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
                    del_tese_plan_history(data)
                        .then(() => {
                            this.$message({
                                message: this.$t('operateTips.delSuccess'),
                                type: 'success'
                            })
                            // 删除之后，重新请求,根据page,szie
                            // 判断是否在过滤条件下
                            // if (this.filter_flag) {
                            //     // 不过滤case
                            //     console.log('取消')
                            // } else {
                            //     // 过滤case
                            //     console.log('应用')
                            //     this.filter_flag == false
                            //     this.list_page_change(1, 20)
                            //     this.empty_filter_condition()
                            // }

                            // 删除之后，只在页面上删除，不用重新请求

                            for (let j = 0; j < bulk_del_id_list.length; j++) {
                                for (let i = 0; i < this.test_case_table.length; i++) {
                                    if (bulk_del_id_list[j] == this.test_case_table[i].id) {
                                        this.test_case_table.splice(i, 1)
                                    }
                                }
                            }
                        })
                        .catch(err => {
                            reject(err)
                        })
                })
            })
        }
    }
}
</script>
<style lang="scss" scoped>
</style>