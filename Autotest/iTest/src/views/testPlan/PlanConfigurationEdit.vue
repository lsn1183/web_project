<template>
    <div class="test-case">
        <div class="side-bar"></div>
        <div class="content">
            <div class="test-case-content">
                <div class="wrapper">
                    <div class="operate-header">
                        <div class="operate-header-title">
                            <h2 class="title">测试计划配置
                                <div class="operate-btn-bar">
                                    <!-- <i class="el-icon-more" v-popover:parent_info_pop></i>
                                    <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                                        <p class="operate-display-icon" @click="go_diff_page('add')">添加计划</p>
                                        <p class="operate-display-icon" @click="show_bulk_delete_hint()"> 批量删除</p>
                                    </el-popover> -->
                                </div>
                            </h2>
                            <p class="title-detail">
                                <span>xxxxxxxxxxx</span>
                            </p>
                        </div>
                    </div>
                    <div class="wrapper-content-show-page">
                        <el-table :data="configuration_list" border style="width: 100%" size="mini" @selection-change="handle_select_change" :max-height="table_max_height">
                            <el-table-column type="selection" width="35" align="center">
                            </el-table-column>
                            <el-table-column prop="field_name" label="自定义标签名称" align="center">
                            </el-table-column>
                            <el-table-column prop="field_en_name" label="自定义字段名称" align="center">
                            </el-table-column>
                        </el-table>
                    </div>

                    <div class="wrapper-footer-pagination" style="text-align: right">
                        <el-button type="primary" @click="submit()" size="small">{{$t('table.confirm')}}</el-button>
                        <el-button @click="cancel()" size="small">{{$t('table.cancel')}}</el-button>
                    </div>
                </div>

            </div>

        </div>
    </div>

</template>
<script>
import { get_plan_configuration_list, set_plan_configuration, get_selected_plan_configuration } from '@/api/testPlan'
export default {
    name: 'test-plan-history',
    data() {
        return {
            configuration_list: [],
            sub_configuration_list: [],
            table_max_height: window.innerHeight - 200
        }
    },
    created() {
        const plan_id = this.$store.getters.test_plan_id
        this.req_all_configuration(plan_id)
    },
    mounted() {
        const that = this
        window.onresize = () => {
            return (() => {
                that.table_max_height = window.innerHeight - 200
            })()
        }
    },
    methods: {
        req_selected_configuration(plan_id) {
            get_selected_plan_configuration(plan_id).then(res => {
                console.log(res, 'res')
                // this.$nextTick(() => {
                //     for (let items of res.data.field_list) {

                //         this.$refs.multipleTable.toggleRowSelection(items, true)
                //     }
                // })
            })
        },
        req_all_configuration(plan_id) {
            get_plan_configuration_list(plan_id).then(res => {
                this.configuration_list = res.data.result
            })
        },
        handle_select_change(val) {
            this.sub_configuration_list = val
        },
        cancel() {
            this.$router.push('/testPlan/testPlanShow')
        },
        submit() {
            const plan_id = this.$store.getters.test_plan_id
            const data = this.sub_configuration_list
            set_plan_configuration(plan_id, data).then(res => {
                this.$router.push('/testPlan/testPlanShow')
            })
        }
    }
}
</script>
<style lang="scss" scoped>
</style>