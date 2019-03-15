<template>
    <div class="wrapper">
        <div class="operate-header">
            <div class="operate-header-title">
                <h2 class="title">关键字管理
                    <!-- <div class="operate-btn-bar">
                        [
                        <span @click="add_keyword()">添加关键字</span> ]&nbsp;&nbsp; [
                        <span @click="del_keyword_list()">批量删除</span> ]
                    </div> -->
                    <div class="operate-btn-bar">
                        <i class="el-icon-more" v-popover:parent_info_pop></i>
                        <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                            <p class="operate-display-icon" @click="add_keyword()">添加关键字</p>
                            <p class="operate-display-icon" @click="del_keyword_list()"> 批量删除</p>
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
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item" disabled="disabled">
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
                <!-- <el-button size="mini" @click="search_detial_keyword()" type="primary">{{$t('table.apply')}}</el-button>
            <el-button size="mini" @click="empty_search_option()" type="primary">{{$t('table.cancel')}}</el-button> -->
                <span class="filter-option-bar-btn" @click="search_detial_keyword()">
                    <i class="el-icon-check"></i> {{$t('table.apply')}}</span>
                <span class="filter-option-bar-btn" @click="empty_search_option()">
                    <i class="el-icon-refresh"></i> {{$t('table.clear')}}</span>
            </div>

            <el-table :data="keyword_table_list" border style="width: 100%" @selection-change="handle_select_change" size="mini" :max-height="table_max_height">
                <el-table-column type="selection" width="35" align="center">
                </el-table-column>
                <el-table-column prop="name" label="关键字" align="center">
                </el-table-column>
                <el-table-column label="操作" width="200" align="center">
                    <template slot-scope="scope">
                        <span class="btn-operate" @click="edit_keyword('edit', scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span>
                        <span class="btn-operate" @click="del_keyword(scope.row)"> &nbsp;[ {{$t('table.delete')}} ]</span>
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
import { get_keyword_list, del_keyword, add_keyword, edit_keyword, search_keyword, del_keyword_list } from '@/api/backstage'
import { get_user_permission_list_fun, } from '@/api/backstage'
export default {
    name: 'component_name',
    created () {
        this.edit_options_disabled()
        this.get_keyword_list()
    },
    mounted () {
        const that = this
        window.onresize = () => {
            return (() => {
                that.table_max_height = window.innerHeight - 235
            })()
        }
    },
    data () {
        return {
            page: 1,
            page_size: 20,
            count: 0,
            keyword_table_list: [],
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
            ],
            options: [
                {
                    value: 'keyword',
                    label: '关键字名称'
                }],
            filter_condition: [
                {
                    checked: true,
                    type: 'keyword',
                    label: '关键字名称',
                    content: '',
                    option: '包含'
                }
            ],
            filter_value: "",
            batch_del_keyword: [],
            table_max_height: window.innerHeight - 235
        }
    },
    methods: {
        add_keyword () {
            let perm_data = {
                "user_name": this.$store.getters.name,
                "per_name": "关键字管理"
            }
            get_user_permission_list_fun(perm_data).then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.$router.push("/backstage/keywordManage/add")
                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })
        },
        edit_keyword (type, data) {
            let perm_data = {
                "user_name": this.$store.getters.name,
                "per_name": "关键字管理"
            }
            get_user_permission_list_fun(perm_data).then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    let routerValue = { path: "/backstage/keywordManage/edit", query: { params: JSON.stringify(data) } }
                    this.$router.push(routerValue)

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })

        },
        get_keyword_list () {
            const get_tabel_list = new Promise((resolve, reject) => {
                get_keyword_list().then(res => {
                    if (res != undefined) {
                        this.keyword_table_list = res.data
                    }
                }).catch(err => {
                    reject(err)
                })
            })
            return get_tabel_list
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
                    option: '关键字名称'
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
        search_detial_keyword () {
            let check_checkout_data = this.filter_condition.filter(item => item.checked === true)

            if (check_checkout_data.length != 0) {
                return new Promise((resolve, reject) => {
                    // return
                    search_keyword(check_checkout_data).then(res => {
                        this.keyword_table_list = res.data
                    }).catch(err => {
                        reject(err)
                    })
                })
            }

        },
        empty_search_option () {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'keyword',
                    label: '关键字名称',
                    content: '',
                    option: '包含'
                }
            ];
            this.edit_options_disabled()
            this.get_keyword_list()
        },
        handle_select_change (val) {
            this.batch_del_keyword = val.map(item => {
                return item.id
            })
        },
        del_keyword_list () {
            let perm_data = {
                "user_name": this.$store.getters.name,
                "per_name": "关键字管理"
            }
            get_user_permission_list_fun(perm_data).then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    if (this.batch_del_keyword.length !== 0) {
                        this.$confirm('此操作将永久删除已选中数据, 是否继续?', this.$t('operateTips.tips'), {
                            confirmButtonText: this.$t('table.confirm'),
                            cancelButtonText: this.$t('table.cancel'),
                            type: 'warning'
                        }).then(() => {
                            let obj_batch_del_keyword = { dellist: JSON.parse(JSON.stringify(this.batch_del_keyword)) }
                            return new Promise((resolve, reject) => {
                                del_keyword_list(obj_batch_del_keyword)
                                    .then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.delSuccess'),
                                            type: 'success'
                                        })
                                        this.get_keyword_list()
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
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
        del_keyword (data) {
            let perm_data = {
                "user_name": this.$store.getters.name,
                "per_name": "关键字管理"
            }
            get_user_permission_list_fun(perm_data).then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    del_keyword(data.id)
                        .then(res => {
                            this.$message({
                                message: this.$t('operateTips.delSuccess'),
                                type: 'success'
                            })
                            this.get_keyword_list()
                        }).catch(err => {
                            reject(err)
                        })

                } else {
                    return this.$message({
                        type: "warning",
                        message: this.$t('title_text.permission_alert_text')
                    })
                }
            })


        },
        list_page_change (val) {

        }
    }
}
</script>
<style lang="scss" scoped>
</style>