<template>
    <div class="wrapper">
        <div class="operate-header">
            <div class="operate-header-title">
                <h2 class="title">权限管理
                    <div class="operate-btn-bar">
                        <i class="el-icon-more" v-popover:parent_info_pop></i>
                        <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                            <!-- <p class="operate-display-icon" @click="add_module()">{{$t('moduleManage.addModule')}}</p> -->
                            <!-- <p class="operate-display-icon" @click="del_batch_country_tips()"> {{$t('projectManage.batch_delete')}}</p> -->
                            <!-- <p class="operate-display-icon">
                                <el-upload style="display: inline-block;" class="upload-demo" :action="upload_address" :on-success="import_success" :show-file-list=false>
                                    <span class=""> {{$t('table.import')}} </span>
                                </el-upload>
                            </p> -->
                            <!-- <p class="operate-display-icon" @click="export_excel()">{{$t('table.export')}}</p> -->
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
                    <i :class="filterFlag? 'el-icon-caret-right':'el-icon-caret-bottom'"></i>{{$t('title_text.role_name')}}
                </legend>
                <el-select v-model="role_name_value" placeholder="请选择" class="select-box" style="width:31%;" @change='select_user_role_fun' @visible-change="get_role_list_fun">
                    <el-option v-for="item in role_list" :key="item.id" :label="item.role_name" :value="item.id">
                    </el-option>
                </el-select>
            </fieldset>

            <fieldset class="collapsible">
                <legend>
                    <i :class="filterFlag? 'el-icon-caret-right':'el-icon-caret-bottom'"></i>{{$t('title_text.role_permission')}}
                </legend>
            </fieldset>
            <div class="wrapper-content-middle">
                <el-checkbox-group v-model="checked_array" @change='change_checkbox_value_fun'>
                    <el-table :data="user_permission_arr" border style="width: 100%;">
                        <el-table-column prop="perm_type" label="分类" width="180" align="left" header-align="center" >
                            <template slot-scope="scope">
                                <span class="item-children">{{scope.row.perm_type}}</span>
                            </template>
                            <!-- style="white-space: nowrap;text-overflow: ellipsis;cursor: pointer;" -->
                        </el-table-column>
                        <el-table-column prop="perm_name" label="权限" align="left" header-align="center">
                            <template slot-scope="scope">
                                <div class="wrapper-content-middle-children">
                                    <span v-for='item in scope.row.perm_list' :key="item.id" class="item-children">
                                        <el-checkbox :label="item.id">
                                            <span class="item-children">{{item.perm_name}}</span>
                                        </el-checkbox>
                                    </span>
                                </div>

                            </template>
                        </el-table-column>

                    </el-table>
                </el-checkbox-group>
            </div>

        </div>
        <div class="wrapper-footer-btn">
            <el-button type="primary" @click="confirm_submit('projForm')" size="small">{{$t('table.confirm')}}</el-button>
            <el-button @click="cancel('countryForm')" size="small">{{$t('table.cancel')}}</el-button>
        </div>
    </div>
</template>
<script>
import { get_permission_list, edit_permission, get_permission_role, get_role_list } from '@/api/backstage'
import { get_user_permission_list_fun, } from '@/api/backstage'
import ip from '@/utils/address'
export default {
    name: 'PersonnelShow',
    data () {
        return {
            upload_address: ip + 'api/1.0/testmanage/ImportExcle',
            table_max_height: window.innerHeight - 235,
            optimal_table_height: window.innerHeight - 235,
            filterFlag: false,
            role_name_value: '',
            role_list: [],
            checked_array: [],
            user_permission_arr: []
        }
    },
    created () {
        this.get_permission_fun()
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
        get_role_list_fun (val) {
            if (val === true) {
                if (this.role_list.length == 0) {
                    get_role_list().then(res => {
                        this.role_list = res.data.result
                    })
                }

            }
        },
        change_checkbox_value_fun (val) {
            // console.log(this.checked_array)
        },
        select_user_role_fun () {
            this.checked_array = []
            let role = this.role_name_value
            get_permission_role(role).then(res => {
                this.checked_array = res.data.result
            })
        },
        get_permission_fun () {
            // all-user
            get_permission_list().then(res => {
                console.log(res,'==========')
                this.user_permission_arr = res.data.reverse()
            })

        },
        confirm_submit (form_ame) {
            const data = {
                'role_name': this.role_name_value,
                'perm_list': this.checked_array
            }
            if (this.role_name_value == '') {
                this.$message({
                    type: "warning",
                    message: this.$t('title_text.select_role')
                })
                return
            }
            get_user_permission_list_fun(this.$store.getters.name,"权限管理").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    edit_permission(data).then(() => {
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
            this.checked_array = []
            this.role_name_value = ''
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
        },
        on_resize_get_height () {
            window.onresize = () => {
                return () => {
                    this.set_optimal_table_height()
                }
            }
        },

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
        width: 33%;
        font-size: 12px;
    }
}
</style>