<template>
    <div class="wrapper">
        <div class="operate-header">
            <div class="operate-header-title">
                <h2 class="title">仕向地管理
                    <!-- <div class="operate-btn-bar">
                        [
                        <span @click="add_land()">添加仕向地</span> ]&nbsp;&nbsp; [
                        <span @click="click_del_batch_land()">批量删除</span> ]
                    </div> -->
                    <div class="operate-btn-bar">
                        <i class="el-icon-more" v-popover:parent_info_pop></i>
                        <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                            <p class="operate-display-icon" @click="add_land()">添加仕向地</p>
                            <p class="operate-display-icon" @click="click_del_batch_land()">批量删除</p>
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
                            <el-select size="mini" v-model="fliter_value" @change="add_filter()">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item" :disabled="item.disabled">
                                </el-option>
                            </el-select>
                        </div>

                        <div v-for="item in filter_condition" class="filters-content-field">
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
                <!-- <el-button size="mini" @click="search_detial_land()" type="primary">{{$t('table.apply')}}</el-button>
                <el-button size="mini" @click="empty_search_option()" type="primary">{{$t('table.cancel')}}</el-button> -->
                <span class="filter-option-bar-btn" @click="search_detial_land()">
                    <i class="el-icon-check"></i> {{$t('table.apply')}}</span>
                <span class="filter-option-bar-btn" @click="empty_search_option()">
                    <i class="el-icon-refresh"></i> {{$t('table.clear')}}</span>
            </div>

            <el-table :data="land_table" border style="width: 100%" @selection-change="handle_select_change" size="mini" :max-height="table_max_height">
                <el-table-column type="selection" width="35" align="center">
                </el-table-column>
                <!-- <el-table-column type="expand">
                    <template slot-scope="scope">
                        <span>国家:</span>
                        <span v-for="(item, index) in scope.row.country_list">{{ item }} </span>
                    </template>
                </el-table-column> -->

                <el-table-column prop="name" label="仕向地名称" align="center">
                </el-table-column>
                <el-table-column prop="provider" label="数据供应商" align="center">
                </el-table-column>
                <el-table-column prop="introduce" label="仕向地简介" align="center">
                </el-table-column>
                <el-table-column label="操作" width="200" align="center">
                    <template slot-scope="scope">
                        <span class="btn-operate" @click="edit_land(scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span>
                        <span class="btn-operate" @click="del_land(scope.row)"> &nbsp;[ {{$t('table.delete')}} ]</span>
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
import { get_land_list, add_land, edit_land, get_country_list, del_batch_land, get_detail_land, del_land_item } from '@/api/backstage'
import ip from '@/utils/address'
import { get_user_permission_list_fun, } from '@/api/backstage'
export default {
    name: 'LandShow',
    data () {
        return {
            page: 1,
            page_size: 20,
            count: 0,
            upload_address: ip + 'api/1.0/testmanage/ImportExcle',
            isShowDialog: false,
            land_table: [],
            searchValue: '',
            fliter_value: '',
            landForm: {
                id: '',
                name: '',
                introduce: '',
                country_list: []
            },
            rules: {
                name: [{ required: true, message: '请输入仕向地名称', trigger: 'change' }],
                abbreviation: [{ required: true, message: '请输入数据供应商', trigger: 'change' }],
                introduce: [{ required: true, message: '请输入仕向地简介', trigger: 'change' }]
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
                    value: 'name',
                    label: '仕向地名称'
                },
                {
                    value: 'provider',
                    label: '数据供应商'
                },
                {
                    value: 'introduce',
                    label: '仕向地简介'
                }
            ],
            filter_condition: [
                {
                    checked: true,
                    type: 'name',
                    label: '仕向地名称',
                    content: '',
                    option: '包含'
                }
            ],
            // optimal_table_height: window.innerHeight - 220,
            country_list: [],
            batch_del_land: [],
            table_max_height: window.innerHeight - 235
        }
    },
    created () {
        this.req_land_list()
        this.edit_options_disabled()
    },
    mounted () {
        const that = this
        window.onresize = () => {
            return (() => {
                that.table_max_height = window.innerHeight - 235
            })()
        }
        // this.on_resize_get_height()
    },
    methods: {
        search_detial_land () {
            let check_checkout_data = this.filter_condition.filter(item => item.checked === true)
            if (check_checkout_data.length != 0) {
                return new Promise((resolve, reject) => {
                    get_detail_land(check_checkout_data).then(res => {
                        this.land_table = res.data
                    }).catch(err => {
                        reject(err)
                    })
                })
            }

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
        req_land_list () {
            return new Promise((resolve, reject) => {
                get_land_list()
                    .then(res => {
                        this.land_table = res.data
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        add_land () {
            get_user_permission_list_fun(this.$store.getters.name, "仕向地管理/添加").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.toggle_dialog_display_status()
                    this.submitType = { type: 'add' }
                    let routerValue = { path: '/backstage/landManage/edit', query: { params: JSON.stringify(this.submitType) } }
                    this.$router.push(routerValue)
                    return
                    this.toggle_dialog_display_status()

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        edit_land (row) {
            get_user_permission_list_fun(this.$store.getters.name, "仕向地管理/编辑").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.toggle_dialog_display_status()
                    this.submitType = 'edit'
                    this.landForm = row
                    this.landForm.type = 'edit'
                    let routerValue = { path: '/backstage/landManage/edit', query: { params: JSON.stringify(this.landForm) } }
                    this.$router.push(routerValue)

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        del_land (row) {
            get_user_permission_list_fun(this.$store.getters.name, "仕向地管理/删除").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.$confirm('此操作将永久删除此条记录, 是否继续?', this.$t('operateTips.tips'), {
                        confirmButtonText: this.$t('table.confirm'),
                        cancelButtonText: this.$t('table.cancel'),
                        type: 'warning'
                    }).then(() => {
                        return new Promise((resolve, reject) => {
                            del_land_item(row.id).then(res => {
                                this.$message({
                                    message: "删除成功",
                                    type: 'success'
                                })
                                this.req_land_list()
                            }).catch(err => {
                                reject(err)
                            })
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
        handle_close () {
            let landForm = 'landForm'
            this.$refs[landForm].resetFields()
            this.toggle_dialog_display_status()
            this.clean_form_content()
        },
        search_click () { },
        toggle_dialog_display_status () {
            this.isShowDialog = !this.isShowDialog
        },
        confirm_submit (landForm) {
            this.$nextTick(function () {
                this.$refs[landForm].validate(valid => {
                    if (valid) {
                        if (this.submitType === 'add') {
                            return new Promise((resolve, reject) => {
                                add_land(this.landForm)
                                    .then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.editSuccess'),
                                            type: 'success'
                                        })
                                        this.$refs[landForm].resetFields()
                                        this.toggle_dialog_display_status()
                                        this.req_land_list()
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        } else if (this.submitType === 'edit') {
                            return new Promise((resolve, reject) => {
                                edit_land(this.landForm)
                                    .then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.editSuccess'),
                                            type: 'success'
                                        })
                                        this.$refs[landForm].resetFields()
                                        this.toggle_dialog_display_status()
                                        this.req_land_list()
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
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
        cancel (landForm) {
            this.$refs[landForm].resetFields()
            this.toggle_dialog_display_status()
            this.clean_form_content()
        },
        clean_form_content () {
            this.landForm = {
                id: '',
                abbreviation: '',
                country_list: [],
                introduce: '',
                name: ''
            }
        },
        add_filter () {
            let filter_value_copy = this.fliter_value
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
            this.fliter_value = ''
        },
        import_success (res) {
            if (res == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.req_land_list()
            } else {
                this.$alert('上传失败，请重新导入', '提示')
            }
        },
        on_resize_get_height () {
            window.onresize = () => {
                return () => {
                    this.set_optimal_table_height()
                }
            }
        },
        set_optimal_table_height () {
            if (!this.isShowDialog) {
                let other_margin_height = 36
                let other_dom_height =
                    document.getElementsByClassName('operate-header')[0].offsetHeight +
                    document.getElementsByClassName('operate-bar')[0].offsetHeight
                let container_height =
                    document.getElementsByClassName('backstage-manage-container')[0].offsetHeight - 20
                this.optimal_table_height = container_height - other_dom_height - other_margin_height
            }
        },
        fold () {
            this.filterFlag = !this.filterFlag
            // ???不加$nextTick为什么，table高度不变(this.optimal_table_height数据变了)
            // this.$nextTick(() => {
            //     this.set_optimal_table_height()
            // })
        },
        empty_search_option () {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'name',
                    label: '仕向地名称',
                    content: '',
                    option: '包含'
                }
            ]
            this.edit_options_disabled()
            this.req_land_list()
        },
        click_del_batch_land () {
            get_user_permission_list_fun(this.$store.getters.name, "仕向地管理/删除").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    if (this.batch_del_land.length === 0) {
                        this.$message({
                            message: '请选择数据',
                            type: 'warning'
                        })
                        return
                    }
                    if (this.batch_del_land.length !== 0) {
                        this.$confirm('此操作将永久删除已选中数据, 是否继续?', this.$t('operateTips.tips'), {
                            confirmButtonText: this.$t('table.confirm'),
                            cancelButtonText: this.$t('table.cancel'),
                            type: 'warning'
                        }).then(() => {
                            let obj_batch_del_land = { dellist: JSON.parse(JSON.stringify(this.batch_del_land)) }
                            return new Promise((resolve, reject) => {
                                del_batch_land(obj_batch_del_land)
                                    .then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.delSuccess'),
                                            type: 'success'
                                        })
                                        this.req_land_list()
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        })
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
            this.batch_del_land = val.map(item => {
                return item.id
            })
        },
        list_page_change (val) {

        }
    }
}
</script>
<style lang="scss" scoped>
.country-manage {
    height: 100%;
    overflow: hidden;

    .operate-header {
        font-size: 14px;

        .search-text {
            vertical-align: middle;
            border-radius: 40px;
            height: 28px;
            outline: none;
            padding: 1px 10px;
            background-color: #fff;
            color: #3d454c;
            border: 1px solid #e0e2e3;
            margin: 0px;
        }

        .fr {
            float: right;
        }
    }

    .operate-bar {
        margin: 0 0 10px 0;
    }
}
</style>