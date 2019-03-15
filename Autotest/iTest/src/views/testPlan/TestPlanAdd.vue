<template>

    <div class="test-case">
        <div class="side-bar"></div>

        <div class="content">
            <div class="test-case-content">
                <div class="wrapper">
                    <h2 class="title">测试计划添加</h2>
                    <div class="wrapper-content">
                        <div class="wrapper-content-form">
                            <div class="wrapper-content-form-content wrapper-content-form-content-ex">
                                <el-form :model="projForm" :rules="rules" ref="test_plan_form" label-width="110px">
                                    <el-form-item label="测试计划名称" prop="title">
                                        <el-input v-model="projForm.title" class="input-wid"></el-input>
                                    </el-form-item>
                                    <el-form-item label="负责人" prop="charger">
                                        <el-select v-model="projForm.charger" filterable remote placeholder="请输入搜索负责人名称" :remote-method="query_search_async" :loading="loading">
                                            <el-option v-for="item in user_list" :key="item.id" :label="item.value" :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                </el-form>
                            </div>
                        </div>

                        <fieldset class="wrapper-content-background">
                            <legend class="wrapper-content-filter-title">jenkins配置</legend>
                            <div class="wrapper-content-table">
                                <el-form :model="projForm" :rules="rules" ref="test_plan_form" label-width="110px">
                                    <el-form-item label="名称" prop="title">
                                        <el-input v-model="node_name" class="input-wid"></el-input>
                                    </el-form-item>
                                    <el-form-item label="节点名称" prop="charger">
                                        <el-select v-model="node" placeholder="请选择节点">
                                            <el-option v-for="item in jenkins_node_list" :key="item.node" :label="item.node" :value="item.node">
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                </el-form>
                            </div>
                        </fieldset>

                        <fieldset class="wrapper-content-background">
                            <legend class="wrapper-content-filter-title">测试用例</legend>
                            <div class="wrapper-content-filter">
                                <fieldset class="collapsible">
                                    <legend>
                                        <i :class="filterLandFlag? 'el-icon-caret-right':'el-icon-caret-bottom'" @click="foldcase()"></i>{{$t('country.filter')}}
                                    </legend>
                                    <div v-show="!filterLandFlag">
                                        <div class="add-filter">
                                            {{$t('country.addFilter')}}:
                                            <el-select size="mini" v-model="filter_value" @change="add_filter('case')">
                                                <el-option v-for="item in case_filter_options" :key="item.value" :label="item.label" :value="item" :disabled="item.disabled">
                                                </el-option>
                                            </el-select>
                                        </div>

                                        <div class="filters-content">
                                            <div v-for="(item, index) in case_filter_condition" :key="index" class="filters-content-field">
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
                                                <input v-model="item.content" class="input-text" v-if="item.checked"></input>
                                            </div>
                                        </div>
                                    </div>
                                </fieldset>
                                <div class="filter-option-bar">
                                    <span class="filter-option-bar-btn" @click="search_detail('case')">
                                        <i class="el-icon-success"></i> {{$t('table.apply')}}</span>
                                    <span class="filter-option-bar-btn" @click="empty_search_option('case')" type="primary">
                                        <i class="el-icon-error"></i> {{$t('table.clear')}}</span>
                                </div>
                            </div>
                            <div class="wrapper-content-table">
                                <table>
                                    <thead>
                                        <tr>
                                            <th style="width: 35px; padding: 8px 0;">
                                                <el-checkbox v-model="is_select_all_case" @change="click_select_all_checkbox('case', is_select_all_case)"></el-checkbox>
                                            </th>
                                            <th>标题</th>
                                            <th>测试方式</th>
                                            <th>版本</th>
                                            <th>负责人</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(item, index) in case_show_list" :key="item.id">
                                            <td style="width: 35px; padding: 8px 0;">
                                                <el-checkbox v-model="item.is_selected" @change="click_select_checkbox('case')"></el-checkbox>
                                            </td>
                                            <td>{{item.title}}</td>
                                            <td>{{item.test_mode | translate}}</td>
                                            <td style="width: 100px;text-align: center;">
                                                <template>
                                                    <div style="display: inline-block;width: 80px;">
                                                        <el-select v-model="item.version" placeholder="请选择" @change="replace_id(item)" :disabled="item.version_list.length == 1">
                                                            <el-option v-for="items in item.version_list" :key="items.id" :label="items.version" :value="items.version">
                                                            </el-option>
                                                        </el-select>
                                                    </div>

                                                </template>
                                            </td>
                                            <td>{{item.charger}}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </fieldset>
                    </div>

                    <div class="wrapper-footer-btn">
                        <el-button type="primary" @click="confirm_submit('test_plan_form')" size="small">{{$t('table.confirm')}}</el-button>
                        <el-button @click="cancel()" size="small">{{$t('table.cancel')}}</el-button>
                    </div>
                </div>
            </div>

        </div>
    </div>

</template>
<script>
import { get_all_case_no_paging, get_filter_data_about_all_case_no_paging } from '@/api/testcase'
import { add_test_plan, get_jenkins_node } from '@/api/testPlan'
import { get_all_user } from '@/api/login'
export default {
    name: 'test-plan-add',
    filters: {
        translate(value) {
            if (value == 'automatically') {
                return '自动'
            } else {
                return '手动'
            }
        }
    },
    data() {
        return {
            test_method: [
                {
                    label: '自动',
                    value: true
                },
                {
                    label: '手动',
                    value: false
                }
            ],
            title: '测试用例添加',
            filter_flag: false,
            filter_value: '',
            filter_step: [
                {
                    checked: false,
                    type: 'test_step',
                    label: '已选择步骤'
                }
            ],
            case_filter_condition: [
                {
                    checked: true,
                    type: 'title',
                    label: '标题',
                    content: '',
                    option: '包含'
                }
            ],
            case_filter_options: [
                {
                    value: 'title',
                    label: '标题'
                },
                {
                    value: 'test_mode',
                    label: '测试方式'
                },
                {
                    value: 'charge',
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
            test_plan_form: {
                id: 0,
                title: '',
                case_version: '',
                charger: '',
                abstract: '',
                premise: '',
                importance: '',
                test_mode: '',
                case_list: [],
                field_value_list: [],
                step_list: [
                    {
                        order: '',
                        operate: '',
                        expected_value: '',
                        is_automatically: ''
                    }
                ]
            },
            selected_step_list: [],
            three_list: {},

            case_all_list: [],
            temp_case_all_list: [],
            case_show_list: [],
            is_select_all_case: [],
            case_select_flag: false,
            projForm: {
                id: 0,
                title: '',
                charger: '',
                user_name: '',
                case_list: []
            },
            filterLandFlag: false,
            rules: {
                title: [{ required: true, message: '计划名称不能为空', trigger: 'change' }],
                charger: [{ required: true, message: '负责人不能为空', trigger: 'change' }]
            },
            user_list: [],
            jenkins_node_list: [],
            node_name: '',
            node: '',
            loading: false,
            proj_id: null
        }
    },
    created() {
        this.proj_id = this.$store.getters.proj_id
        this.req_jenkins_node_list()
        this.get_all_test_case_data()
        this.edit_options_disabled('case')
    },
    activated() {
        // console.log('22222222')
        // this.get_all_test_case_data()
        // this.edit_options_disabled('case')
    },
    computed: {},
    methods: {
        query_search_async(query_string) {
            if (query_string == '') {
                this.user_list = []
            } else {
                this.loading = true
                get_all_user(query_string)
                    .then(res => {
                        this.user_list = res.data.result.data_list
                        this.loading = false
                    })
                    .catch(() => {
                        this.loading = false
                    })
            }
        },
        replace_id(item) {
            let arr = item.version_list.filter(items => items.version == item.version)
            item.id = arr[0].id
            this.click_select_checkbox('case')
        },
        req_jenkins_node_list() {
            get_jenkins_node().then(res => {
                this.jenkins_node_list = res.data
            })
        },
        get_all_test_case_data() {
            get_all_case_no_paging(this.proj_id).then(res => {
                for (let item of res.data.result) {
                    item.is_selected = false
                }
                this.case_show_list = JSON.parse(JSON.stringify(res.data.result))
                this.case_all_list = JSON.parse(JSON.stringify(res.data.result))
                this.temp_case_all_list = JSON.parse(JSON.stringify(res.data.result))
                this.show_selected_data()
            })
        },
        show_selected_data() {
            let case_selected_list = JSON.parse(JSON.stringify(this.projForm.case_list))
            this.get_selected_list(case_selected_list, this.case_show_list)
            this.check_full_box('case')
        },
        get_selected_list(partial_data, all_data) {
            for (let item_partial of partial_data) {
                for (let item_all of all_data) {
                    if (item_partial.source_id == item_all.source_id) {
                        item_all.is_selected = true
                        item_all.version = item_partial.version
                        item_all.id = item_partial.id
                        break
                    }
                }
            }
        },
        check_full_box(table_name) {
            // 判断table数据,来判断table表上全选是否勾选
            const table_data_name = table_name + '_show_list'

            if (this[table_data_name].length != 0) {
                const is_select_all = 'is_select_all_' + table_name
                const unselected_data = this[table_data_name].filter(item => item.is_selected === false)
                if (unselected_data.length === 0) {
                    this[is_select_all] = true
                } else {
                    this[is_select_all] = false
                }
            }
        },
        click_select_all_checkbox(table_name, select_all_flag) {
            // 点击全选checkbox
            const data_name = table_name + '_show_list'
            this.select_all_data(select_all_flag, this[data_name]) // 根据select_all_flag, 全选/不全选

            this.click_select_checkbox(table_name)
        },
        select_all_data(select_all_flag, data) {
            // 根据select_all_flag, 全选/不全选
            if (select_all_flag) {
                for (let item of data) {
                    item.is_selected = true
                }
            } else {
                for (let item of data) {
                    item.is_selected = false
                }
            }
        },
        click_select_checkbox(table_name) {
            this.check_full_box(table_name)

            // 在勾选的时候就将勾选的数据，保存到projForm中，这样不用在点击'确定'按钮时候在判断
            // 分两种情况
            let select_flag_name = table_name + '_select_flag'
            let list_name = table_name + '_list'
            let show_list_name = table_name + '_show_list'
            if (this[select_flag_name]) {
                // 过滤情况下
                let sub_case_list = JSON.parse(JSON.stringify(this.projForm[list_name]))
                for (let itemss of this[show_list_name]) {
                    let is_exit = false
                    let same_id = null
                    for (let itemsss of sub_case_list) {
                        // 判断case_show_list里的数据是否在projForm.case_list中存在
                        if (itemss.source_id == itemsss.source_id) {
                            is_exit = true // 如果存在 is_exit 为 true
                            same_id = itemss.source_id
                            break
                        }
                    }

                    if (is_exit === true) {
                        // 存在相同数据的清空
                        if (itemss.is_selected == true) {
                            // 相同数据且is_selected为true情况下，就不用添加
                            for (let i = 0; i < this.projForm[list_name].length; i++) {
                                if (this.projForm[list_name][i].source_id == same_id) {
                                    this.projForm[list_name].splice(i, 1, itemss)
                                }
                            }
                        } else {
                            // 相同数据且is_selected为false情况下，去除这个数据

                            for (let i = 0; i < this.projForm[list_name].length; i++) {
                                if (this.projForm[list_name][i].source_id == same_id) {
                                    this.projForm[list_name].splice(i, 1)
                                }
                            }
                        }
                    } else {
                        // 不存在相同数据的清空
                        if (itemss.is_selected == true) {
                            this.projForm[list_name].push(itemss)
                        }
                    }
                }
            } else {
                // 未过滤情况下
                let sub_data_name = table_name + '_list'
                this.projForm[sub_data_name] = this[show_list_name].filter(item => item.is_selected === true)
            }
        },
        fold() {
            this.filter_flag = !this.filter_flag
        },
        add_filter() {
            let filter_value_copy = this.filter_value
            let set = new Set(this.case_filter_condition)
            let hasTheSame = false
            for (let item of set.keys()) {
                hasTheSame = hasTheSame || item.type === filter_value_copy.value
            }
            if (!hasTheSame) {
                this.case_filter_condition.push({
                    checked: true,
                    type: filter_value_copy.value,
                    label: filter_value_copy.label,
                    content: '',
                    option: '包含'
                })
            }
            this.edit_options_disabled('case')
            this.filter_value = ''
        },
        empty_search_option(val) {
            if (this.case_select_flag) {
                const filter_condition_name = val + '_filter_condition'
                this[filter_condition_name] = [
                    {
                        checked: true,
                        type: 'title',
                        label: '标题',
                        content: '',
                        option: '包含'
                    }
                ]
                this.filter_step = [
                    {
                        checked: false,
                        type: 'test_step',
                        label: '已选择步骤'
                    }
                ]
                this.edit_options_disabled(val)
                this.case_show_list = JSON.parse(JSON.stringify(this.temp_case_all_list))
                let case_selected_list = JSON.parse(JSON.stringify(this.projForm.case_list))
                this.get_selected_list(case_selected_list, this.case_show_list)
                this.check_full_box('case')
                this.case_select_flag = false
            }
        },
        edit_options_disabled(val) {
            let filter_options = val + '_filter_options'
            let filter_condition = val + '_filter_condition'
            this[filter_options] = this[filter_options].map(item => {
                item.disabled = false
                return item
            })

            for (let item of this[filter_condition]) {
                for (let item_options of this[filter_options]) {
                    if (item.type === item_options.value) {
                        item_options.disabled = true
                        break
                    }
                }
            }
        },
        search_detail(table_name) {
            const table_data_name = table_name + '_show_list'
            const proj_list = table_name + '_list'
            if ((this.case_select_flag = true)) {
                // 在 过滤情况下 this.projForm.case_list 不变化
            } else {
                // 在 没有过滤情况下 this.projForm.case_list 不变化
                this.projForm[proj_list] = this[table_data_name].filter(item => item.is_selected === true)
            }
            const transfer_filter_condition_data = this.transfer_filter_condition(table_name)
            this.req_detail_case(transfer_filter_condition_data)
        },
        transfer_filter_condition(table_name) {
            // 整合过滤条件
            let list_filter_condition = []
            let filter_condition_name = table_name + '_filter_condition'
            if (table_name == 'field') {
                list_filter_condition = this[filter_condition_name].filter(item => {
                    if (item.type === 'is_show') {
                        item.option = '等于'
                        if (item.content === '') {
                            item.content = false
                        }
                    }

                    return item.checked === true
                })
                return list_filter_condition
            } else {
                return (list_filter_condition = this[filter_condition_name].filter(item => {
                    return item.checked === true
                }))
            }
        },
        req_detail_case(data) {
            return new Promise((resolve, reject) => {
                get_filter_data_about_all_case_no_paging(data)
                    .then(res => {
                        let detail_case_data = res.data.result
                        for (let item of detail_case_data) {
                            item.is_selected = false
                        }
                        for (let item of this.projForm.case_list) {
                            for (let items of detail_case_data) {
                                if (item.source_id == items.source_id) {
                                    items.is_selected = true
                                    items.version = item.version
                                    items.id = item.id
                                    break
                                }
                            }
                        }

                        this.case_show_list = detail_case_data
                        this.check_full_box('case') // 用来判断是否要勾选 全选checkbox
                        this.case_select_flag = true
                    })
                    .catch(err => {
                        this.case_select_flag = false
                        reject(err)
                    })
            })
        },
        cancel() {
            this.$router.push('/testPlan/testPlanShow')
        },
        confirm_submit(form_name) {
            if (this.projForm.case_list.length === 0) {
                this.$message({
                    message: '请添加测试用例',
                    type: 'warning'
                })
                return
            }
            this.$nextTick(function() {
                this.$refs[form_name].validate(valid => {
                    if (valid) {
                        this.projForm.proj_id = this.proj_id
                        const data = this.projForm
                        add_test_plan(data).then(() => {
                            this.$message({
                                message: this.$t('operateTips.addSuccess'),
                                type: 'success'
                            })
                            this.$router.push('/testPlan/testPlanShow')
                        })
                    } else {
                        return
                    }
                })
            })
        },
        handle_land_selection_change(val) {
            this.test_plan_form.case_list = val
        },
        handle_case_selection_change(val) {
            this.test_plan_form.case_list = val
        }
    }
}
</script>
<style lang="scss" scoped>
table {
    width: 100%;
    border-collapse: collapse;
    text-align: center;
    font-size: 14px;
    background-color: #fff;
}
table th,
tr,
td {
    border: 1px solid #ebeef5;
}
thead {
    color: #909399;
}
tbody {
    color: #606266;
}
th {
    padding: 3px 0;
}

.input-wid {
    width: 500px;
}
</style>