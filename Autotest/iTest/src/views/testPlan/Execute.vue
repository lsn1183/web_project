<template>

    <div class="test-case">
        <div class="side-bar">
            <el-tree :data="test_plan_result_list" ref="test_case_tree" default-expand-all :expand-on-click-node="false" highlight-current :props="default_props" @node-click="handle_node_click" node-key="unique_id">
            </el-tree>
        </div>

        <div class="case-execute-container">
            <div class="test-case-content" v-show="tree_node_level == 1">
                <div class="wrapper">
                    <h2 class="title">{{title}}</h2>
                    <div class="wrapper-content">
                        <fieldset class="wrapper-content-background">
                            <legend class="wrapper-content-filter-title">全部测试用例执行历史</legend>
                            <div class="wrapper-content-table">
                                <el-table :data="case_list" style="width: 100%" align="center" border size="mini" stripe>
                                    <el-table-column type="index" width="50" label="编号" align="center">
                                    </el-table-column>
                                    <el-table-column prop="title" label="标题" width="180" align="center">
                                    </el-table-column>
                                    <el-table-column prop="test_mode" label="测试方式" width="180" align="center">
                                        <template slot-scope="scope">
                                            {{scope.row.test_mode | switch_test_mode}}
                                        </template>
                                    </el-table-column>
                                    <el-table-column prop="charger" label="创建人" align="center">
                                    </el-table-column>
                                    <el-table-column prop="case_version" label="版本" align="center" style="background-color: red;">
                                    </el-table-column>

                                    <el-table-column prop="update_time" label="执行日期" align="center">
                                    </el-table-column>

                                    <el-table-column prop="state" label="状态" align="center" width="50" style="background-color: red;">
                                        <template slot-scope="scope">
                                            <p v-if="scope.row.state == '通过'" style="background-color: #006400; color: white;">{{scope.row.state}}</p>
                                            <p v-if="scope.row.state == '失败'" style="background-color: #B22222; color: white;">{{scope.row.state}}</p>
                                            <p v-if="scope.row.state == '锁定'" style="background-color: #00008B; color: white;">{{scope.row.state}}</p>
                                        </template>
                                    </el-table-column>
                                    <el-table-column v-for="(item, index) in name_list" :key="index" :label="item.name" align="center">
                                        <template slot-scope="scope">
                                            <span>{{scope.row.field_list_two[item.en_name]}}</span>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                        </fieldset>
                    </div>
                    <div class="wrapper-footer-pagination" style="text-align: right;">
                        <el-button @click="cancel()" size="small">返回</el-button>
                    </div>
                </div>
            </div>

            <div class="test-case-content" v-show="tree_node_level != 1">
                <div class="wrapper">
                    <h2 class="title">{{title}}</h2>
                    <div class="wrapper-content">
                        <fieldset class="wrapper-content-background">
                            <legend class="wrapper-content-filter-title">单条测试用例执行历史</legend>
                            <div class="wrapper-content-table">
                                <el-table :data="case_result_history" style="width: 100%" align="center" border size="mini" stripe>
                                    <el-table-column type="index" width="50" label="编号" align="center">
                                    </el-table-column>
                                    <el-table-column prop="title" label="标题" width="180" align="center">
                                    </el-table-column>
                                    <el-table-column prop="test_mode" label="测试方式" width="180" align="center">
                                        <template slot-scope="scope">
                                            {{scope.row.test_mode | switch_test_mode}}
                                        </template>
                                    </el-table-column>
                                    <el-table-column prop="updatetime" label="执行日期" align="center">
                                    </el-table-column>
                                    <el-table-column prop="result_value" label="状态" align="center" width="50" style="background-color: red;">
                                        <template slot-scope="scope">
                                            <p v-if="scope.row.result_value == '通过'" style="background-color: #006400; color: white;">{{scope.row.result_value}}</p>
                                            <p v-if="scope.row.result_value == '失败'" style="background-color: #B22222; color: white;">{{scope.row.result_value}}</p>
                                            <p v-if="scope.row.result_value == '锁定'" style="background-color: #00008B; color: white;">{{scope.row.result_value}}</p>
                                        </template>
                                    </el-table-column>
                                    <el-table-column prop="address" label="操作" align="center" width="180">
                                        <template slot-scope="scope">
                                            <span class="btn-operate" @click="look_one_case_history(scope.row.id, scope.$index)"> &nbsp;[ 详细 ]</span>
                                            <span class="btn-operate" @click="del_one_case_history(scope.row.id, scope.$index)"> &nbsp;[ {{$t('table.delete')}} ]</span>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                        </fieldset>

                        <fieldset class="wrapper-content-background">
                            <legend class="wrapper-content-filter-title">自定义字段</legend>
                            <div class="wrapper-content-filter">
                            </div>
                            <div class="wrapper-content-table">
                                <el-form label-width="110px">
                                    <el-form-item :label="item.name" v-for="(item, index) in case_details.field_list" :key="index">
                                        <div v-if="item.type === 'input'">
                                            <el-input v-model="item.field_value" style="width: 500px;" :disabled="item.field_open_use != 'test_execution'"></el-input>
                                        </div>

                                        <div v-else-if="item.type === 'textarea'">
                                            <el-input v-model="item.field_value" type="textarea" :disabled="item.field_open_use != 'test_execution'"></el-input>
                                        </div>

                                        <div v-else-if="item.type === 'select'">
                                            <el-select v-model="item.field_value" :disabled="item.field_open_use != 'test_execution'">
                                                <el-option v-for="(item_children, indexs) in item.option_list" :key="indexs" :label="item_children.label" 
                                                :value="item_children.value">

                                                </el-option>
                                            </el-select>
                                        </div>

                                        <div v-else-if="item.type === 'checkbox'">
                                            <el-radio-group v-model="item.field_value" style="line-height: 40px; height: 40px;">
                                                <el-radio :label="item_children.label" v-for="(item_children, indexs) in item.option_list"
                                                :key="indexs" :disabled="item.field_open_use != 'test_execution'">{{item_children.label}}</el-radio>
                                            </el-radio-group>
                                        </div>

                                        <div v-else-if="item.type === 'multiSelect'">
                                            <el-checkbox-group v-model="item.field_value">
                                                <el-checkbox :label="item_children.label" v-for="(item_children, indexs) in item.option_list"
                                                :key="indexs" :disabled="item.field_open_use != 'test_execution'">{{item_children.label}}</el-checkbox>
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
                                <el-table :data="case_details.step_list" border style="width: 100%" size="mini">
                                    <el-table-column label="测试顺序" align="center" width="70" type="index">
                                    </el-table-column>
                                    <el-table-column label="测试操作" align="center" prop="operate">
                                    </el-table-column>
                                    <el-table-column label="期望值" align="center" prop="expected_value">
                                    </el-table-column>
                                    <el-table-column label="测试方式" align="center" width="200px;">
                                        <template slot-scope="scope">
                                            <el-select v-model="scope.row.is_automatically" placeholder="请选择" size="mini" disabled>
                                                <el-option :label="item.label" :value="item.value" v-for="(item, index) in test_method" :key="index"></el-option>
                                            </el-select>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="执行状态" width="120" align="center" prop="step_state">
                                        <template slot-scope="scope">
                                            <el-select v-model="scope.row.step_state" size="mini">
                                                <el-option :label="item.label" :value="item.value" v-for="(item, index) in excute_state" :key="index"></el-option>
                                            </el-select>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                            <div style="margin-top: 20px;position:relative;">
                                <div style="float: left;width: 100%;font-size: 14px; color: #606266;vertical-align:top;">
                                    说明/描述
                                    <el-input type="textarea" v-model="case_details.result_remarks"></el-input>
                                </div>
                                <!-- <div style="float: right;width: 25%;vertical-align:top;text-align: center;">
                                    <div style="height: 180px; width: 210px; border: medium solid #808080;margin-top: 20px;padding: 12px;">
                                        <div style="display: flex;">
                                            <el-button title="点击设置为通过" size="mini" type="primary" @click="sub_case_details('通过')">通过</el-button>
                                            <el-button title="点击设置为失败" size="mini" type="primary" @click="sub_case_details('失败')">失败</el-button>
                                            <el-button title="点击设置为锁定" size="mini" type="primary" @click="sub_case_details('锁定')">锁定</el-button>
                                        </div>

                                        <div style="text-align: left;margin-top: 20px;">
                                            <el-button @click="remove_next" size="mini" type="primary">移动到下一个测试用例</el-button>
                                        </div>
                                    </div>
                                </div> -->
                            </div>
                        </fieldset>

                    </div>

                    <div class="wrapper-footer-pagination" style="text-align: right;">
                        <!-- <el-button type="primary" @click="confirm_submit()" size="small">确定</el-button> -->
                        <el-button title="点击设置为通过" size="small" type="primary" @click="sub_case_details('通过')">通过</el-button>
                        <el-button title="点击设置为失败" size="small" type="primary" @click="sub_case_details('失败')">失败</el-button>
                        <el-button title="点击设置为锁定" size="small" type="primary" @click="sub_case_details('锁定')">锁定</el-button>
                        <el-button title="移动到下一个测试用例" size="small" type="primary" @click="remove_next()">下一个</el-button>
                        <el-button @click="cancel()" size="small">返回</el-button>
                    </div>
                </div>
            </div>

        </div>
    </div>

</template>
<script>
import {
    req_test_plan_result_list,
    req_case_result_history,
    req_one_detail_case,
    sub_case_record,
    del_case_history
} from '@/api/testPlan'
import ip from '@/utils/address'
export default {
    name: 'test-plan-edit',
    filters: {
        switch_test_mode(value) {
            if (value == 'automatically') {
                return '自动'
            } else {
                return '手动'
            }
        },
        switch_importance(value) {
            if (value == 'heigh') {
                return '高'
            } else if (value == 'middle') {
                return '中'
            } else {
                return '低'
            }
        }
    },
    data() {
        return {
            name_list: [],
            field_name_list: [],
            test_plan_result_list: [],
            default_props: {
                children: 'case_list',
                label: 'title'
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
            excute_state: [
                {
                    label: '通过',
                    value: '通过'
                },
                {
                    label: '失败',
                    value: '失败'
                },
                {
                    label: '锁定',
                    value: '锁定'
                }
            ],
            case_result_history: [],
            case_details: [],
            original_case_details: [],
            current_unique_id: 0, // 前端自定义的id(用来高亮树节点)
            case_id: 0, // 后台传过来的case id(用来请求数据)
            options: [
                {
                    value: '版本1',
                    label: '版本1'
                },
                {
                    value: '版本2',
                    label: '版本2'
                },
                {
                    value: '版本3',
                    label: '版本3'
                },
                {
                    value: '版本4',
                    label: '版本4'
                },
                {
                    value: '版本5',
                    label: '版本5'
                }
            ],
            value: '',
            tree_node_level: 1,
            case_list: [],
            title: ''
        }
    },
    created() {
        this.get_tree_data()
    },
    destroyed() {},
    computed: {},
    methods: {
        del_one_case_history(value, index) {
            const data = { dellist: [value] }
            del_case_history(data).then(res => {
                this.case_result_history.splice(index, 1)
            })
        },
        look_one_case_history(value, index) {
            let case_details_data = {
                server_ip: ip,
                id: value,
                index: index
            }
            sessionStorage.setItem('case_details_data', JSON.stringify(case_details_data))
            window.open('../../../static/html/ExecuteDetailed.html')
            return
            const data = { dellist: [value] }
            del_case_history(data).then(res => {
                this.case_result_history.splice(index, 1)
            })
        },
        remove_next() {
            const arr_len = this.test_plan_result_list[0].case_list.length
            if (this.current_unique_id == this.test_plan_result_list[0].case_list[arr_len - 1].unique_id) {
                this.$message({
                    message: '此用例为最后一个测试用例',
                    type: 'warning'
                })
                return // 如果是最后一个case，click失效
            }

            const plan_id = this.$store.getters.test_plan_id
            const plan_history_id = this.$store.getters.test_plan_history_id
            const case_arr = this.test_plan_result_list[0].case_list
            const last_case_id = this.case_id
            for (let i = 0; i < case_arr.length; i++) {
                if (case_arr[i].unique_id == this.current_unique_id) {
                    this.case_id = case_arr[i + 1].id // 获得当前节点的下一个节点的id
                    break
                }
            }

            const case_id = this.case_id

            // 请求case执行历史数据promise
            let case_history_promise = new Promise((resolve, reject) => {
                req_case_result_history(plan_history_id, case_id)
                    .then(res => {
                        resolve(res)
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

            // 请求单独一条case的执行数据promise
            let case_execute_promise = new Promise((resolve, reject) => {
                req_one_detail_case(plan_id, case_id)
                    .then(res => {
                        resolve(res)
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

            return new Promise((resolve, reject) => {
                Promise.all([case_history_promise, case_execute_promise])
                    .then(res => {
                        this.case_result_history = res[0].data.result
                        this.original_case_details = JSON.parse(JSON.stringify(res[1].data.result[0]))
                        this.case_details = res[1].data.result[0]
                        this.title = '测试用例：' + res[1].data.result[0].title
                        this.current_unique_id += 1
                        this.$nextTick(() => {
                            this.$refs['test_case_tree'].setCurrentKey(this.current_unique_id) // 高亮下一个节点
                        })
                    })
                    .catch(err => {
                        this.case_id = last_case_id
                        reject(err)
                    })
            })
        },
        get_tree_data() {
            const plan_id = this.$store.getters.test_plan_id
            const plan_history_id = this.$store.getters.test_plan_history_id
            // 请求case执行左边树数据promise
            let plan_result_promise = new Promise((resolve, reject) => {
                req_test_plan_result_list(plan_history_id)
                    .then(res => {
                        // 自定义树的唯一id
                        res.data.result[0].unique_id = 1
                        res.data.result[0].case_list.forEach((item, index) => {
                            item.unique_id = index + 2
                        })
                        this.test_plan_result_list = JSON.parse(JSON.stringify(res.data.result))
                        this.title = '测试计划：' + res.data.result[0].title
                        this.$nextTick(() => {
                            this.$refs['test_case_tree'].setCurrentKey(1) // 高亮树中的第一个case节点
                        })
                        console.log( res.data.result[0], '2222222222')
                        this.case_list = this.test_plan_result_list[0].case_list
                        this.name_list = this.test_plan_result_list[0].name_list
                        const case_id = this.test_plan_result_list[0].case_list[0].id
                        this.case_id = this.test_plan_result_list[0].case_list[0].id
                        this.current_unique_id = this.test_plan_result_list[0].case_list[0].unique_id
                        // this.get_case_history_and_details(plan_id, plan_history_id, case_id)
                        resolve()
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        get_case_history_and_details(plan_id, plan_history_id, case_id) {
            // 请求case执行历史数据promise
            let case_history_promise = new Promise((resolve, reject) => {
                req_case_result_history(plan_history_id, case_id)
                    .then(res => {
                        resolve(res)
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

            // 请求单独一条case的执行数据promise
            let case_execute_promise = new Promise((resolve, reject) => {
                req_one_detail_case(plan_id, case_id)
                    .then(res => {
                        resolve(res)
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

            return new Promise((resolve, reject) => {
                Promise.all([case_history_promise, case_execute_promise])
                    .then(res => {
                        this.case_result_history = res[0].data.result
                        this.case_details = res[1].data.result[0]
                        this.original_case_details = JSON.parse(JSON.stringify(res[1].data.result[0]))
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        handle_node_click(data, node) {
            // if (node.level === 1) {
            //     // 点击第一层，节点高亮不变化，case数据也不变化
            //     this.$nextTick(() => {
            //         this.$refs['test_case_tree'].setCurrentKey(this.current_unique_id) // 高亮下一个节点
            //     })
            // }
            this.tree_node_level = node.level
            if (node.level === 1) {
                this.get_tree_data()
            }

            if (node.level === 2) {
                const plan_id = this.$store.getters.test_plan_id
                const plan_history_id = this.$store.getters.test_plan_history_id
                this.current_unique_id = data.unique_id
                this.case_id = data.id
                this.title = '测试用例：' + data.title
                const case_id = data.id
                this.get_case_history_and_details(plan_id, plan_history_id, case_id)
            }
        },

        cancel() {
            this.$router.push('/testPlan/history')
        },
        sub_case_details(status) {
            this.case_details.result_value = status
            const data = this.case_details
            const plan_id = this.$store.getters.test_plan_id
            const plan_history_id = this.$store.getters.test_plan_history_id

            const case_id = this.case_id
            const sub_case_record_promise = new Promise((resolve, reject) => {
                sub_case_record(plan_history_id, case_id, data)
                    .then(() => {
                        resolve()
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
            sub_case_record_promise.then(res => {
                this.$message({
                    message: this.$t('operateTips.addSuccess'),
                    type: 'success'
                })
                // 请求case执行历史数据promise
                req_case_result_history(plan_history_id, case_id).then(res => {
                    this.case_result_history = res.data.result
                    this.case_details = JSON.parse(JSON.stringify(this.original_case_details))
                })
            })
        },
        confirm_submit() {
            const data = this.case_details
            const plan_id = this.$store.getters.operation_data
            const case_id = this.case_id
            sub_case_record(plan_id, case_id, data).then(res => {
                this.$message({
                    message: this.$t('operateTips.addSuccess'),
                    type: 'success'
                })
                this.$router.push('/testPlan/testPlanShow')
            })
        },
        handle_land_selection_change(val) {
            this.test_case_form.case_list = val
        },
        handle_case_selection_change(val) {
            this.test_case_form.case_list = val
        }
    }
}
</script>
<style lang="scss" scoped>
.case-execute-container {
    float: left;
    width: calc(100% - 250px);
    height: 100%;
    padding: 20px 0 0 20px;
    box-sizing: border-box;
    position: relative;
}
@media screen and (max-width: 1280px) {
    .case-execute-container {
        width: calc(100% - 200px);
    }
}
</style>