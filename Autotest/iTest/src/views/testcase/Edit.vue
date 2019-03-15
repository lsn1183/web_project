<template>
    <div class="test-case-content test-case-content-ex">
        <div class="wrapper">
            <h2 class="title">{{title}}</h2>
            <div class="wrapper-content">
                <div class="wrapper-content-form">
                    <div class="wrapper-content-form-content wrapper-content-form-content-ex">
                        <el-form :model="test_case_form" ref="test_case_form" :rules="rules" label-width="110px" label-position="right">
                            <el-form-item label="版本" prop="case_version">
                                <el-input v-model="test_case_form.case_version" class="input-wid" disabled></el-input>
                            </el-form-item>
                            <el-form-item label="负责人" prop="charger">
                                <el-select v-model="test_case_form.charger" filterable remote placeholder="请输入搜索负责人名称" :remote-method="query_search_async" :loading="loading">
                                <el-option v-for="item in user_list" :key="item.id" :label="item.value" :value="item.value">
                                </el-option>
                            </el-select>
                            </el-form-item>
                            <el-form-item label="标题" prop="title">
                                <el-input v-model="test_case_form.title" class="input-wid"></el-input>
                            </el-form-item>
                            <el-form-item label="摘要" prop="abstract">
                                
                                <tinymce :height="400" v-model="test_case_form.abstract"></tinymce>
                            </el-form-item>
                            <el-form-item label="前提" prop="premise">
                                <tinymce :height="400" v-model="test_case_form.premise"></tinymce>
                            </el-form-item>

                            <el-form-item label="仕向地">
                                <el-table ref="landTable" :data="three_list.dest_list" border style="width: 100%" @selection-change="handle_land_selection_change" size="mini">
                                    <el-table-column type="selection" width="35" align="center">
                                    </el-table-column>
                                    <el-table-column label="仕向地名称" align="center" prop="name">
                                    </el-table-column>
                                </el-table>
                            </el-form-item>

                            <el-form-item label="重要性" prop="importance">
                                <el-select v-model="test_case_form.importance" placeholder="请选择">
                                    <el-option label="低" value="low"></el-option>
                                    <el-option label="中" value="middle"></el-option>
                                    <el-option label="高" value="high"></el-option>
                                </el-select>
                            </el-form-item>

                            <el-form-item label="测试方式" prop="test_mode">
                                <el-select v-model="test_case_form.test_mode" placeholder="请选择">
                                    <el-option label="自动" value="automatically"></el-option>
                                    <el-option label="手动" value="manually"></el-option>
                                </el-select>
                            </el-form-item>

                            <el-form-item label="关键字">
                                <el-table ref="keywordTable" :data="three_list.keyword_list" border style="width: 100%" @selection-change="handle_keyword_selection_change" size="mini">
                                    <el-table-column type="selection" width="35" align="center">
                                    </el-table-column>
                                    <el-table-column label="关键字名称" align="center" prop="name">
                                    </el-table-column>
                                </el-table>
                            </el-form-item>

                        </el-form>
                    </div>
                </div>

                <fieldset class="wrapper-content-background">
                    <legend class="wrapper-content-filter-title">自定义字段</legend>
                    <div class="wrapper-content-filter">
                    </div>
                    <div class="wrapper-content-table">
                        <el-form label-width="110px">
                            <el-form-item :label="item.name" v-for="(item, index) in three_list.field_list" :key="index">
                                <div v-if="item.type === 'input'">
                                    <el-input v-model="item.field_value" style="width: 500px;"></el-input>
                                </div>

                                <div v-else-if="item.type === 'textarea'">
                                    <el-input v-model="item.field_value" type="textarea"></el-input>
                                </div>

                                <div v-else-if="item.type === 'select'">
                                    <el-select v-model="item.field_value">
                                        <el-option v-for="(item_children, indexs) in item.option_list" :key="indexs" :label="item_children.label" :value="item_children.value">

                                        </el-option>
                                    </el-select>
                                </div>

                                <div v-else-if="item.type === 'checkbox'">
                                    <el-radio-group v-model="item.field_value" style="line-height: 40px; height: 40px;">
                                        <el-radio :label="item_children.label" v-for="(item_children, indexs) in item.option_list" :key="indexs">{{item_children.label}}</el-radio>
                                    </el-radio-group>
                                </div>

                                <div v-else-if="item.type === 'multiSelect'">
                                    <el-checkbox-group v-model="item.field_value">
                                        <el-checkbox :label="item_children.label" v-for="(item_children, indexs) in item.option_list" :key="indexs">{{item_children.label}}</el-checkbox>
                                    </el-checkbox-group>
                                </div>
                            </el-form-item>
                        </el-form>
                    </div>
                </fieldset>

                <fieldset class="wrapper-content-background">
                    <legend class="wrapper-content-filter-title">测试步骤</legend>
                    <div class="wrapper-content-filter">
                    </div>
                    <div class="wrapper-content-table">
                        <!-- <div class="filter-option-bar" style="margin-bottom: 15px;margin-top: 0px;">
                            <span class="filter-option-bar-btn" @click="add_test_step()">
                                <i class="el-icon-plus"></i> 添加</span>
                        </div> -->
                        <el-table :data="test_case_form.step_list" ref="caseStepTable" border style="width: 100%" @selection-change="handle_select_change" size="mini">
                            <el-table-column label="测试顺序" align="center" width="80" type="index">
                            </el-table-column>
                            <el-table-column label="测试操作" align="center">
                                <template slot-scope="scope">
                                    <el-input type="textarea" v-model="scope.row.operate" :rows="1"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="期望值" align="center">
                                <template slot-scope="scope">
                                    <el-input type="textarea" v-model="scope.row.expected_value" :rows="1"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="测试方式" align="center" width="200px;">
                                <template slot-scope="scope">
                                    <el-select v-model="scope.row.is_automatically" placeholder="请选择" size="small">
                                        <el-option :label="item.label" :value="item.value" v-for="(item, index) in test_method" :key="index"></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" width="120" align="center">
                                <template slot-scope="scope">
                                    <span class="btn-operate" @click="add_test_step(scope.$index, scope.row)">[ {{$t('table.add')}} ]</span>
                                    <span class="btn-operate" @click="del_test_step(scope.$index, scope.row)" v-if="test_case_form.step_list.length !== 1">[ {{$t('table.delete')}} ]</span>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>

                </fieldset>
            </div>

            <div class="wrapper-footer-btn">
                <el-button type="primary" @click="confirm_submit('test_case_form')" size="small">{{$t('table.confirm')}}</el-button>
                <el-button @click="cancel()" size="small">{{$t('table.cancel')}}</el-button>
            </div>
        </div>
    </div>
</template>
<script>
import Tinymce from '@/views/editor/tinymce'
import { get_all_user } from '@/api/login'
import { get_three_list, add_test_case, edit_test_case, get_one_test_case } from '@/api/testcase'
import { get_user_permission_list_fun, } from '@/api/backstage'
export default {
    name: 'testCaseEdit',
    components: {
        tinymce: Tinymce
    },
    data() {
        return {
            rules: {
                // case_version: [{ required: true, message: '版本不能为空', trigger: 'change' }],
                charger: [{ required: true, message: '负责人不能为空', trigger: 'change' }],
                title: [{ required: true, message: '标题不能为空', trigger: 'change' }]
            },
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
            filter_condition: [
                {
                    checked: true,
                    type: 'test_method',
                    label: '测试方法',
                    content: '',
                    option: '包含'
                }
            ],
            options: [
                {
                    value: 'test_method',
                    label: '测试方法'
                },
                {
                    value: 'test_result',
                    label: '测试结果'
                },
                {
                    value: 'is_automatically',
                    label: '测试方式'
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
            test_case_form: {
                id: 0,
                title: '',
                case_version: '1',
                commit_user: this.$store.getters.name,
                charger: '',
                abstract: '',
                premise: '',
                importance: '',
                test_mode: '',
                dest_list: [],
                keyword_list: [],
                field_value_list: [],
                step_list: [
                    {
                        order: '',
                        operate: '',
                        expected_value: '',
                        is_automatically: true
                    }
                ]
            },
            selected_step_list: [],
            three_list: {},
            user_list: [],
            loading: false
        }
    },
    created() {
        if (this.$store.getters.tree_node_data_id !== 0) {
            this.edit_options_disabled()

            if (this.$store.getters.operation_type === 'edit') {
                this.title = '测试用例编辑'
                this.transfer_req_data_to_display_data()
            } else {
                this.req_three_list()
            }
        }
    },
    computed: {
        module_id() {
            return this.$store.getters.tree_node_data_id
        },
        test_case_id() {
            return this.$store.getters.test_case_id
        }
    },
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
        // testcae
        get_select_data(data, allData, sel_data) {
            // 将请求的数据与请求回来的全部数据对比，获得一个新数组
            for (let item of data) {
                for (let items of allData) {
                    if (item.id === items.id) {
                        sel_data.push(items)
                        break
                    }
                }
            }
        },

        transfer_req_data_to_display_data() {
            let id = this.test_case_id
            const one_test_case_promise = new Promise((resolve, reject) => {
                get_one_test_case(id)
                    .then(res => {
                        this.test_case_form = res.data.result
                        resolve()
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

            const three_list_promise = new Promise((resolve, reject) => {
                get_three_list(this.module_id)
                    .then(res => {
                        this.three_list = res.data
                        resolve()
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

            Promise.all([one_test_case_promise, three_list_promise])
                .then(() => {
                    for (let item of this.test_case_form.field_value_list) {
                        for (let field_item of this.three_list.field_list) {
                            if (item.field_id == field_item.id) {
                                if (field_item.type === 'multiSelect') {
                                    const str_len = item.field_value.length
                                    // 截取第二位到倒数第二位 去除空格 去除单双引号
                                    const spl_arr = item.field_value
                                        .slice(2, str_len - 1)
                                        .replace(/\s+/g, '')
                                        .replace(/['"]+/g, '')
                                        .split(',')
                                    field_item.field_value = spl_arr
                                } else {
                                    field_item.field_value = JSON.parse(JSON.stringify(item.field_value))
                                }
                            }
                        }
                    }
                    let checked_dest_list = []
                    let checked_keyword_list = []
                    this.get_select_data(this.test_case_form.dest_list, this.three_list.dest_list, checked_dest_list)
                    this.get_select_data(
                        this.test_case_form.keyword_list,
                        this.three_list.keyword_list,
                        checked_keyword_list
                    )
                    this.$nextTick(() => {
                        checked_dest_list.forEach(row => {
                            this.$refs.landTable.toggleRowSelection(row)
                        })

                        checked_keyword_list.forEach(row => {
                            this.$refs.keywordTable.toggleRowSelection(row)
                        })
                    })
                })
                .catch(err => {
                    console.log(err, 'Promise.all失败的原因')
                })
        },
        req_three_list() {
            // let module_id = this.$store.getters.tree_node_data.id
            get_three_list(this.module_id).then(res => {
                this.three_list = res.data
            })
        },
        fold() {
            this.filter_flag = !this.filter_flag
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
        empty_search_option() {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'test_method',
                    label: '测试方法',
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
            this.edit_options_disabled()
            // this.req_project()
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
        handle_select_change(val) {
            this.selected_step_list = val
        },
        add_test_step(index) {
            let add_item = {
                order: '',
                method_method: '',
                expected_value: '',
                is_automatically: true
            }
            this.test_case_form.step_list.splice(index + 1, 0, add_item)
        },
        del_test_step(index) {
            if (this.test_case_form.step_list.length === 1) {
                return
            }
            this.$confirm('是否删除数据?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.test_case_form.step_list.splice(index, 1)
            })
        },
        cancel() {
            this.$router.push('/testCase/testCaseShow')
        },
        confirm_submit(formName) {
           
            get_user_permission_list_fun(this.$store.getters.name,"编辑执行的测试用例").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.$nextTick(function() {
                        this.$refs[formName].validate(valid => {
                            if (valid) {
                                // 将测试步骤中的测试顺序index 赋值到 字段order中
                                this.test_case_form.step_list.forEach((item, index) => (item.order = index + 1))
                                // this.test_case_form.step_list = this.test_case_form.step_list.map((item, index) => item.order = index + 1)
                                if (this.$store.getters.operation_type === 'add') {
                                    let field_list_data = this.three_list.field_list.map(item => {
                                        return { field_id: item.id, field_value: item.field_value }
                                    })
                                    this.test_case_form.field_value_list = field_list_data
                                    
                                    add_test_case(this.module_id, this.test_case_form).then(() => {
                                        this.$message({
                                            message: this.$t('operateTips.addSuccess'),
                                            type: 'success'
                                        })
                                        this.$router.push('/testCase/testCaseShow')
                                    })
                                } else if (this.$store.getters.operation_type === 'edit') {
                                    this.test_case_form.commit_user = this.$store.getters.name
                                    let field_list_data = this.three_list.field_list.map(item => {
                                        return { field_id: item.id, field_value: item.field_value }
                                    })
                                    this.test_case_form.field_value_list = field_list_data
                                   
                                    edit_test_case(this.test_case_id, this.test_case_form).then(() => {
                                        this.$message({
                                            message: this.$t('operateTips.editSuccess'),
                                            type: 'success'
                                        })
                                        this.$router.push('/testCase/testCaseShow')
                                    })
                                }
                            } else {
                                return
                            }
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
        handle_land_selection_change(val) {
            this.test_case_form.dest_list = val
        },
        handle_keyword_selection_change(val) {
            this.test_case_form.keyword_list = val
        }
    }
}
</script>
<style lang="scss" scoped>
.input-wid {
    width: 500px;
}
</style>