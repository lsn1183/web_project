<template>
    <div class="wrapper">
        <div class="operate-header">
            <div class="operate-header-title">
                <h2 class="title">用户管理
                    <div class="operate-btn-bar">
                        <i class="el-icon-more" v-popover:parent_info_pop></i>
                        <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                            <!-- <p class="operate-display-icon" @click="add_module()">{{$t('moduleManage.addModule')}}</p> -->
                            <!-- <p class="operate-display-icon" @click="del_batch_country_tips()"> {{$t('projectManage.batch_delete')}}</p> -->
                            <p class="operate-display-icon">
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
                    <i :class="filterFlag? 'el-icon-caret-right':'el-icon-caret-bottom'"></i>{{$t('title_text.user_name_search')}}
                </legend>
                <el-select style="width:31%;" v-model="search_user_name" filterable  remote clearable  placeholder="请输入搜索人员名称" :remote-method="query_search_async" 
                :loading="loading" @change="change_user_name_fun" @clear="clear_user_name_fun">
                    <el-option v-for="item in search_user_list" :key="item.id" :label="item.name" :value="item.name">
                    </el-option>
                </el-select>
                
            </fieldset>

            <fieldset class="collapsible">
                <legend>
                    <i :class="filterFlag? 'el-icon-caret-right':'el-icon-caret-bottom'"></i>{{$t('title_text.role_assign')}}
                </legend>
            </fieldset>
            <div class="wrapper-content-middle">
                <el-table :data="all_user_data" border style="width: 100%;">
                    <el-table-column prop="perm_type" label="人员" width="180" align="center">
                        <template slot-scope="scope">
                            <span class="item-children">{{scope.row.name}}</span>
                        </template>
                        <!-- style="white-space: nowrap;text-overflow: ellipsis;cursor: pointer;" -->
                    </el-table-column>
                    <el-table-column prop="perm_name" label="角色分配" align="center">
                        <template slot-scope="scope">
                            <div class="wrapper-content-middle-children">
                                <span v-for='item in scope.row.role_all_list' :key="item.id" class="item-children">
                                    <el-checkbox-group v-model="scope.row.select_role_list" @change='change_checkbox_value_fun'>
                                        <el-checkbox :label="item.id">
                                            <span class="item-children">{{item.role_name}}</span>
                                        </el-checkbox>
                                    </el-checkbox-group>
                                </span>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <div class="wrapper-footer-btn">
            <el-button type="primary" @click="confirm_submit('projForm')" size="small">{{$t('table.confirm')}}</el-button>
            <el-button @click="cancel('countryForm')" size="small">{{$t('table.cancel')}}</el-button>
        </div>
    </div>
</template>
<script>
import { edit_personnel_role, get_all_user_role, get_role_list, get_search_user_list_fun } from '@/api/backstage'
import ip from '@/utils/address'
// import permission from '@/api/permission'
import { get_user_permission_list_fun,permission_judgment } from '@/api/backstage'
export default {
    name: 'PersonnelShow',
    data () {
        return {
            upload_address: ip + 'api/1.0/testmanage/ImportExcle',
            table_max_height: window.innerHeight - 235,
            filterFlag: false,
            all_user_data: [],
            confirm_submit_data: [],
            search_user_name: '',
            search_user_list: [],
            loading: false
        }
    },
    created () {
        this.get_all_user_role_fun()
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
        get_all_user_role_fun () {
            get_all_user_role().then(res => {
                let all_user_data = res.data.result.data_list
                for (let item of all_user_data) {
                    item.role_all_list = res.data.result.role_list_all
                    let new_select_role_list = []
                    if (item.select_role_list.length !== 0) {
                        for (let iterator of item.select_role_list) {
                            new_select_role_list.push(iterator.role_id)
                            iterator = new_select_role_list
                        }
                    }
                    item.select_role_list = new_select_role_list
                }
                this.all_user_data = all_user_data
            })

        },
        change_checkbox_value_fun (val) {
            let new_data = []
            for (let item of this.all_user_data) {
                new_data.push(
                    {
                        'user_id': item.id,
                        'role_list': item.select_role_list
                    }
                )
            }
            this.confirm_submit_data = new_data
        },
        confirm_submit (form_ame) {
            if (this.role_name_value == '') {
                return
            }
            get_user_permission_list_fun(this.$store.getters.name,"用户管理").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    if (this.confirm_submit_data.length == 0) {
                        this.change_checkbox_value_fun()
                    }
                    // console.log(this.confirm_submit_data,'提交的数据')
                    edit_personnel_role(this.confirm_submit_data).then(() => {
                        this.$message({
                            message: this.$t('operateTips.editSuccess'),
                            type: 'success'
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
        cancel () {
            this.get_all_user_role_fun()//回调
        },
        import_success (res) {

        },
        export_excel () {


        },
        on_resize_get_height () {
            window.onresize = () => {
                return () => {
                    this.set_optimal_table_height()
                }
            }
        },
        query_search_async (query_string,cb) {
            if (query_string == '') {
                this.search_user_list = []
            } else {
                this.loading = true
                get_search_user_list_fun(query_string)
                    .then(res => {
                        this.search_user_list = res.data.result.data_list
                        this.loading = false
                        let all_user_data = res.data.result.data_list
                        for (let item of all_user_data) {
                            item.role_all_list = res.data.result.role_list_all
                            let new_select_role_list = []
                            if (item.select_role_list.length !== 0) {
                                for (let iterator of item.select_role_list) {
                                    new_select_role_list.push(iterator.role_id)
                                    iterator = new_select_role_list
                                }
                            }
                            item.select_role_list = new_select_role_list
                        }
                        this.all_user_data = all_user_data

                    })
                    .catch(() => {
                        this.loading = false
                    })
            }
        },
        change_user_name_fun (val) {
            this.query_search_async(val)
        },
        clear_user_name_fun(){
            this.get_all_user_role_fun()
        }

    },

}
</script>
<style lang="scss" scoped>
.wrapper-content-middle {
    // display: flex;
    // flex-wrap: wrap;
    width: 100%;
    .select-box {
        width: 30%;
        margin-left: 0px;
    }
    .wrapper-content-middle-children {
        display: flex;
        flex-wrap: wrap;
        margin: 0 10px 0 10px;
    }
    .item-children {
        width: 20%;
        // text-align: left;
        font-size: 12px;
    }
}
</style>