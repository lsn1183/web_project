<template>

    <div class="wrapper">
        <h2 class="title">{{title}}</h2>
        <div class="wrapper-content">
            <div class="wrapper-content-form">
                <div class="wrapper-content-form-content">
                    <el-form :model="projForm" :rules="rules" ref="projForm" label-width="100px" label-position="left">
                        <el-form-item label="项目名称" prop="name">
                            <el-input v-model="projForm.name" :disabled="edit_flag"></el-input>
                            <!-- <el-select v-model="projForm.id" placeholder="请选择" @change='chang_project_fun' v-else>
                                <el-option v-for="item in proj_options" :key="item.proj_id" :label="item.proj_name" :value="item.proj_id">
                                </el-option>
                            </el-select> -->
                        </el-form-item>
                        <el-form-item label="项目描述" prop="intro">
                            <el-input type="textarea" v-model="projForm.intro" placeholder="请填写项目描述"></el-input>
                        </el-form-item>
                        <el-form-item label="负责人" prop="charger">
                            <el-select v-model="projForm.charger" filterable remote placeholder="请输入搜索负责人名称" :remote-method="query_search_async" :loading="loading">
                                <el-option v-for="item in user_list" :key="item.id" :label="item.value" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="项目时间">
                            <el-date-picker v-model="project_time" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd">
                            </el-date-picker>
                            <!-- <el-col :span="11">
                                <el-form-item prop="create_time">
                                    {{project_time}}
                                    <el-date-picker type="date" placeholder="选择日期" v-model="projForm.create_time" style="width: 100%;" value-format="yyyy-MM-dd"></el-date-picker>
                                </el-form-item>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                            <el-col :span="11">
                                <el-form-item prop="finish_time">
                                    <el-date-picker type="date" placeholder="选择日期" v-model="projForm.finish_time" style="width: 100%;" value-format="yyyy-MM-dd"></el-date-picker>
                                </el-form-item>
                            </el-col> -->
                        </el-form-item>
                    </el-form>
                </div>
            </div>

            <fieldset class="wrapper-content-background">
                <legend class="wrapper-content-filter-title">选择仕向地</legend>
                <div class="wrapper-content-filter">
                    <fieldset class="collapsible">
                        <legend>
                            <i :class="filterLandFlag? 'el-icon-caret-right':'el-icon-caret-bottom'" @click="foldLand()"></i>{{$t('country.filter')}}
                        </legend>
                        <div v-show="!filterLandFlag">
                            <div class="add-filter">
                                {{$t('country.addFilter')}}:
                                <el-select size="mini" v-model="filter_value" @change="add_filter('dest')">
                                    <el-option v-for="item in dest_filter_options" :key="item.value" :label="item.label" :value="item" :disabled="item.disabled">
                                    </el-option>
                                </el-select>
                            </div>

                            <div class="filters-content">
                                <div v-for="(item, index) in dest_filter_condition" :key="index" class="filters-content-field">
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
                    <fieldset class="collapsible">
                        <legend>
                            <i class="el-icon-caret-bottom"></i>筛选器
                        </legend>
                        <div>

                            <div class="filters-content">
                                <div v-for="(item, index) in selected_dest" :key="index" class="filters-content-field">
                                    <div class="filter-label">
                                        <input type="checkbox" v-model="item.checked" class="input-checkbox">
                                        <label>{{item.label}}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </fieldset>
                    <div class="filter-option-bar">
                        <span class="filter-option-bar-btn" @click="search_detail('dest')">
                            <i class="el-icon-success"></i> {{$t('table.apply')}}</span>
                        <span class="filter-option-bar-btn" @click="empty_search_option('dest')" type="primary">
                            <i class="el-icon-error"></i> {{$t('table.clear')}}</span>
                    </div>
                </div>
                <div class="wrapper-content-table">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 35px; padding: 8px 0;">
                                    <el-checkbox v-model="is_select_all_dest" @change="click_select_all_checkbox('dest', is_select_all_dest)"></el-checkbox>
                                </th>
                                <th>仕向地名称</th>
                                <th>数据供应商</th>
                                <th>仕向地简介</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in dest_show_list" :key="item.id">
                                <td style="width: 35px; padding: 8px 0;">
                                    <el-checkbox v-model="item.is_selected" @change="click_select_checkbox('dest')"></el-checkbox>
                                </td>
                                <td>{{item.name}}</td>
                                <td>{{item.provider}}</td>
                                <td>{{item.introduce}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </fieldset>

            <fieldset class="wrapper-content-background">
                <legend class="wrapper-content-filter-title">选择自定义字段</legend>
                <div class="wrapper-content-filter">
                    <fieldset class="collapsible">
                        <legend>
                            <i :class="filterLandFlag? 'el-icon-caret-right':'el-icon-caret-bottom'" @click="foldField()"></i>{{$t('country.filter')}}
                        </legend>
                        <div v-show="!filterLandFlag">
                            <div class="add-filter">
                                {{$t('country.addFilter')}}:
                                <el-select size="mini" v-model="filter_value" @change="add_filter('field')">
                                    <el-option v-for="item in field_filter_options" :key="item.value" :label="item.label" :value="item" :disabled="item.disabled">
                                    </el-option>
                                </el-select>
                            </div>

                            <div class="filters-content">
                                <div v-for="(item, index) in field_filter_condition" :key="index" class="filters-content-field">
                                    <div class="filter-label">
                                        <input type="checkbox" v-model="item.checked" class="input-checkbox">
                                        <label>{{item.label}}</label>
                                    </div>

                                    <div class="filter-select" v-if="item.type === 'is_show' && item.checked">
                                        <input type="checkbox" v-model="item.content" class="input-checkbox">
                                    </div>

                                    <div class="filter-select" v-if="!(item.type === 'is_show') && item.checked ">
                                        <el-select size="mini" v-model="item.option">
                                            <el-option v-for="(item, index) in fliter_options" :key="index" :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </div>
                                    <input v-model="item.content" class="input-text" v-if="!(item.type === 'is_show') && item.checked">
                                </div>
                            </div>
                        </div>
                    </fieldset>
                    <fieldset class="collapsible">
                        <legend>
                            <i class="el-icon-caret-bottom"></i>筛选器
                        </legend>
                        <div>

                            <div class="filters-content">
                                <div v-for="(item, index) in selected_field" :key="index" class="filters-content-field">
                                    <div class="filter-label">
                                        <input type="checkbox" v-model="item.checked" class="input-checkbox">
                                        <label>{{item.label}}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </fieldset>
                    <div class="filter-option-bar">
                        <span class="filter-option-bar-btn" @click="search_detail('field')">
                            <i class="el-icon-success"></i> {{$t('table.apply')}}</span>
                        <span class="filter-option-bar-btn" @click="empty_search_option('field')" type="primary">
                            <i class="el-icon-error"></i> {{$t('table.clear')}}</span>
                    </div>
                </div>
                <div class="wrapper-content-table">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 35px; padding: 8px 0;">
                                    <el-checkbox v-model="is_select_all_field" @change="click_select_all_checkbox('field', is_select_all_field)"></el-checkbox>
                                </th>
                                <th>名称</th>
                                <th>类型</th>
                                <th>选项</th>
                                <th>显示</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in field_show_list" :key="item.id">
                                <td style="width: 35px; padding: 8px 0;">
                                    <el-checkbox v-model="item.is_selected" @change="click_select_checkbox('field')"></el-checkbox>
                                </td>
                                <td>{{item.name}}</td>
                                <td>{{item.type}}</td>
                                <td>
                                    <template slot-scope="scope">
                                        <span v-for="(item_son, index_son) in scope.row.option_list">
                                            {{item_son.value}}
                                        </span>
                                    </template>
                                </td>
                                <td>
                                    <el-checkbox v-model="item.is_show" disabled></el-checkbox>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </fieldset>

            <fieldset class="wrapper-content-background">
                <legend class="wrapper-content-filter-title">选择关键字</legend>
                <div class="wrapper-content-filter">
                    <fieldset class="collapsible">
                        <legend>
                            <i :class="filterLandFlag? 'el-icon-caret-right':'el-icon-caret-bottom'" @click="foldKeyword()"></i>{{$t('country.filter')}}
                        </legend>
                        <div v-show="!filterLandFlag">
                            <div class="add-filter">
                                {{$t('country.addFilter')}}:
                                <el-select size="mini" v-model="filter_value" @change="add_filter('keyword')">
                                    <el-option v-for="item in keyword_filter_options" :key="item.value" :label="item.label" :value="item" :disabled="item.disabled">
                                    </el-option>
                                </el-select>
                            </div>

                            <div class="filters-content">
                                <div v-for="(item, index) in keyword_filter_condition" :key="index" class="filters-content-field">
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
                    <fieldset class="collapsible">
                        <legend>
                            <i class="el-icon-caret-bottom"></i>筛选器
                        </legend>
                        <div>

                            <div class="filters-content">
                                <div v-for="(item, index) in selected_keyword" :key="index" class="filters-content-field">
                                    <div class="filter-label">
                                        <input type="checkbox" v-model="item.checked" class="input-checkbox">
                                        <label>{{item.label}}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </fieldset>
                    <div class="filter-option-bar">
                        <span class="filter-option-bar-btn" @click="search_detail('keyword')">
                            <i class="el-icon-success"></i> {{$t('table.apply')}}</span>
                        <span class="filter-option-bar-btn" @click="empty_search_option('keyword')" type="primary">
                            <i class="el-icon-error"></i> {{$t('table.clear')}}</span>
                    </div>
                </div>
                <div class="wrapper-content-table">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 35px; padding: 8px 0;">
                                    <el-checkbox v-model="is_select_all_keyword" @change="click_select_all_checkbox('keyword', is_select_all_keyword)"></el-checkbox>
                                </th>
                                <th>关键字名称</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in keyword_show_list" :key="item.id">
                                <td style="width: 35px; padding: 8px 0;">
                                    <el-checkbox v-model="item.is_selected" @change="click_select_checkbox('keyword')"></el-checkbox>
                                </td>
                                <td>{{item.name}}</td>
                            </tr>
                        </tbody>
                    </table>

                </div>
            </fieldset>
        </div>

        <div class="wrapper-footer-btn">
            <el-button type="primary" @click="confirm_submit('projForm')" size="small">{{$t('table.confirm')}}</el-button>
            <el-button @click="cancel('countryForm')" size="small">{{$t('table.cancel')}}</el-button>
        </div>
    </div>
</template>
<script>
import {
    add_project,
    edit_project,
    get_land_list,
    get_custom_field_list,
    get_keyword_list,
    search_keyword,
    get_detail_land,
    get_detail_field
} from '@/api/backstage'
import { get_all_user } from '@/api/login'
import { get_user_permission_list_fun, } from '@/api/backstage'
export default {
    name: 'ProjectEdit',
    components: {},
    data() {
        return {
            project_time: [],
            timeout: null,
            restaurants: [],
            projForm: {
                id: '',
                name: '',
                intro: '',
                charger: '',
                create_time: '',
                update_time: '',
                finish_time: '',
                dest_list: [],
                field_list: [],
                keyword_list: []
            },
            checked_dest_list: [],
            checked_field_list: [],
            checked_keyword_list: [],
            filterLandFlag: false,
            filterFieldFlag: false,
            filterKeywordFlag: false,
            rules: {
                name: [{ required: true, message: '请输入活动名称', trigger: 'blur' }],
                intro: [{ required: true, message: '请填写项目描述', trigger: 'change' }],
                charger: [{ required: true, message: '请填写负责人', trigger: 'change' }]
            },
            searchLand: '',
            searchField: '',
            searchKeyword: '',
            title: '项目添加',
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
            dest_filter_options: [
                {
                    value: 'name',
                    label: '仕向地名称',
                    disabled: true
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
            dest_filter_condition: [
                {
                    checked: true,
                    type: 'name',
                    label: '仕向地名称',
                    content: '',
                    option: '包含'
                }
            ],
            field_filter_options: [
                {
                    value: 'name',
                    label: '自定义字段名称',
                    disabled: true
                },
                {
                    value: 'type',
                    label: '类型'
                },
                {
                    value: 'is_show',
                    label: '是否在执行时显示'
                }
            ],
            field_filter_condition: [
                {
                    checked: true,
                    type: 'name',
                    label: '自定义字段名称',
                    content: '',
                    option: '包含'
                }
            ],
            keyword_filter_options: [
                {
                    value: 'keyword',
                    label: '关键字名称',
                    disabled: true
                }
            ],
            keyword_filter_condition: [
                {
                    checked: true,
                    type: 'keyword',
                    label: '关键字名称',
                    content: '',
                    option: '等于'
                }
            ],
            dest_all_list: [],
            field_all_list: [],
            keyword_all_list: [],
            temp_dest_all_list: [],
            temp_field_all_list: [],
            temp_keyword_all_list: [],
            dest_select_flag: false,
            field_select_flag: false,
            keyword_select_flag: false,
            is_select_all_dest: false,
            is_select_all_field: false,
            is_select_all_keyword: false,
            dest_show_list: [],
            field_show_list: [],
            keyword_show_list: [],
            proj_options: [],
            selected_dest: [
                {
                    checked: true,
                    type: 'en_name',
                    label: '已选择仕向地'
                }
            ],
            selected_field: [
                {
                    checked: true,
                    type: 'en_name',
                    label: '已选择自定义字段'
                }
            ],
            selected_keyword: [
                {
                    checked: true,
                    type: 'en_name',
                    label: '已选择关键字'
                }
            ],
            user_list: [],
            loading: false,
            edit_flag: false
        }
    },
    created() {
        if (this.$store.getters.operation_type === 'edit') {
            this.projForm = this.$store.getters.operation_data
            this.project_time[0] = this.projForm.create_time
            this.project_time[1] = this.projForm.finish_time
            this.title = '项目编辑'
            this.edit_flag = true
        }
        // else{
        //     this.get_project_list_fun()
        // }
        this.req_all_dest_field_keyworld()
    },
    mounted() {},
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
        chang_project_fun() {
            for (let item of this.proj_options) {
                if (item.proj_id == this.projForm.id) {
                    this.projForm.name = item.proj_name
                    this.projForm.intro = item.intro
                    this.projForm.charger = item.charger
                }
            }
        },
        // get_project_list_fun () {
        //     let data = {
        //         'manager': sessionStorage.getItem('username'),
        //         'accessToken': sessionStorage.getItem('Token')
        //     }
        //     return new Promise((resolve, reject) => {
        //         get_project_list_fun(data).then(res => {
        //             this.proj_options = res.data
        //         }).catch(() => {
        //             reject()
        //         })
        //     })

        // },
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
        click_select_checkbox(table_name) {
            this.check_full_box(table_name)

            // 在勾选的时候就将勾选的数据，保存到projForm中，这样不用在点击'确定'按钮时候在判断
            // 分两种情况
            let select_flag_name = table_name + '_select_flag'
            let list_name = table_name + '_list'
            let show_list_name = table_name + '_show_list'
            if (this[select_flag_name]) {
                // 过滤情况下
                let sub_dest_list = JSON.parse(JSON.stringify(this.projForm[list_name]))
                for (let itemss of this[show_list_name]) {
                    let is_exit = false
                    let same_id = null
                    for (let itemsss of sub_dest_list) {
                        // 判断dest_show_list里的数据是否在projForm.dest_list中存在
                        if (itemss.id == itemsss.id) {
                            is_exit = true // 如果存在 is_exit 为 true
                            same_id = itemss.id
                            break
                        }
                    }

                    if (is_exit === true) {
                        // 存在相同数据的清空
                        if (itemss.is_selected == true) {
                            // 相同数据且is_selected为true情况下，就不用添加
                        } else {
                            // 相同数据且is_selected为false情况下，去除这个数据

                            for (let i = 0; i < this.projForm[list_name].length; i++) {
                                if (this.projForm[list_name][i].id == same_id) {
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
        get_selected_list(partial_data, all_data) {
            for (let item_partial of partial_data) {
                for (let item_all of all_data) {
                    if (item_partial.id == item_all.id) {
                        item_all.is_selected = true
                        break
                    }
                }
            }
        },
        show_selected_data() {
            let dest_selected_list = JSON.parse(JSON.stringify(this.projForm.dest_list))
            let field_selected_list = JSON.parse(JSON.stringify(this.projForm.field_list))
            let keyword_selected_list = JSON.parse(JSON.stringify(this.projForm.keyword_list))

            this.get_selected_list(dest_selected_list, this.dest_show_list)
            this.get_selected_list(field_selected_list, this.field_show_list)
            this.get_selected_list(keyword_selected_list, this.keyword_show_list)

            if (this.selected_dest[0].checked == true) {
                // 过滤条件下的 已选择
                this.dest_show_list = this.dest_show_list.filter(item => item.is_selected == true)
            }

            if (this.selected_field[0].checked == true) {
                // 过滤条件下的 已选择
                this.field_show_list = this.field_show_list.filter(item => item.is_selected == true)
            }

            if (this.selected_keyword[0].checked == true) {
                // 过滤条件下的 已选择
                this.keyword_show_list = this.keyword_show_list.filter(item => item.is_selected == true)
            }

            this.check_full_box('dest')
            this.check_full_box('field')
            this.check_full_box('keyword')
        },
        req_all_dest_field_keyworld() {
            const dest_promise = new Promise((resolve, reject) => {
                get_land_list()
                    .then(res => {
                        for (let item of res.data) {
                            item.is_selected = false
                        }

                        this.dest_show_list = JSON.parse(JSON.stringify(res.data))
                        this.dest_all_list = JSON.parse(JSON.stringify(res.data))
                        this.temp_dest_all_list = JSON.parse(JSON.stringify(res.data))
                        resolve()
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

            const keyword_promise = new Promise((resolve, reject) => {
                get_keyword_list()
                    .then(res => {
                        for (let item of res.data) {
                            item.is_selected = false
                        }

                        this.keyword_show_list = JSON.parse(JSON.stringify(res.data))
                        this.keyword_all_list = JSON.parse(JSON.stringify(res.data))
                        this.temp_keyword_all_list = JSON.parse(JSON.stringify(res.data))
                        resolve()
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

            const field_promise = new Promise((resolve, reject) => {
                get_custom_field_list()
                    .then(res => {
                        for (let item of res.data) {
                            item.is_selected = false
                        }
                        this.field_show_list = JSON.parse(JSON.stringify(res.data))
                        this.field_all_list = JSON.parse(JSON.stringify(res.data))
                        this.temp_field_all_list = JSON.parse(JSON.stringify(res.data))
                        resolve()
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
            // 只有3个实例的状态都变为fulfilled,才会调用Promise.all方法的回调函数
            return new Promise((resolve, reject) => {
                Promise.all([dest_promise, keyword_promise, field_promise])
                    .then(() => {
                        this.show_selected_data()
                    })
                    .catch(() => {
                        reject()
                    })
            })
        },
        req_detail_dest(data) {
            get_detail_land(data)
                .then(res => {
                    let detail_dest_data = res.data
                    for (let item of detail_dest_data) {
                        item.is_selected = false
                    }
                    for (let item of this.projForm.dest_list) {
                        for (let items of detail_dest_data) {
                            if (item.id == items.id) {
                                items.is_selected = true
                                break
                            }
                        }
                    }
                    if (this.selected_dest[0].checked == true) {
                        // 过滤条件下的 已选择
                        this.dest_show_list = detail_dest_data.filter(item => item.is_selected == true)
                    } else {
                        this.dest_show_list = detail_dest_data
                    }
                    this.check_full_box('dest') // 用来判断是否要勾选 全选checkbox
                    this.dest_select_flag = true
                })
                .catch(err => {
                    this.dest_select_flag = false
                })
        },
        req_detail_field(data) {
            // if (!this.field_select_flag) {
            get_detail_field(data)
                .then(res => {
                    let detail_field_data = res.data
                    for (let item of detail_field_data) {
                        item.is_selected = false
                    }
                    for (let item of this.projForm.field_list) {
                        for (let items of detail_field_data) {
                            if (item.id == items.id) {
                                items.is_selected = true
                                break
                            }
                        }
                    }
                    if (this.selected_field[0].checked == true) {
                        // 过滤条件下的 已选择
                        this.field_show_list = detail_field_data.filter(item => item.is_selected == true)
                    } else {
                        this.field_show_list = detail_field_data
                    }
                    this.check_full_box('field') // 用来判断是否要勾选 全选checkbox
                    this.field_select_flag = true
                })
                .catch(err => {
                    this.field_select_flag = false
                })
            // }
        },
        req_detail_keyword(data) {
            // if (!this.keyword_select_flag) {
            return new Promise((resolve, reject) => {
                search_keyword(data)
                    .then(res => {
                        let detail_keyword_data = res.data
                        for (let item of detail_keyword_data) {
                            item.is_selected = false
                        }

                        for (let item of this.projForm.keyword_list) {
                            for (let items of detail_keyword_data) {
                                if (item.id == items.id) {
                                    items.is_selected = true
                                    break
                                }
                            }
                        }
                        if (this.selected_keyword[0].checked == true) {
                            // 过滤条件下的 已选择
                            this.keyword_show_list = detail_keyword_data.filter(item => item.is_selected == true)
                        } else {
                            this.keyword_show_list = detail_keyword_data
                        }

                        this.check_full_box('keyword') // 用来判断是否要勾选 全选checkbox
                        this.keyword_select_flag = true
                    })
                    .catch(err => {
                        this.keyword_select_flag = false
                        reject(err)
                    })
            })
        },
        foldLand() {
            this.filterLandFlag = !this.filterLandFlag
        },
        foldField() {
            this.filterFieldFlag = !this.filterFieldFlag
        },
        foldKeyword() {
            this.filterKeywordFlag = !this.filterKeywordFlag
        },
        add_filter(val) {
            let filter_condition = val + '_filter_condition'
            let filter_value_copy = this.filter_value
            let set = new Set(this[filter_condition])
            let hasTheSame = false
            for (let item of set.keys()) {
                hasTheSame = hasTheSame || item.type === filter_value_copy.value
            }
            if (!hasTheSame) {
                this[filter_condition].push({
                    checked: true,
                    type: filter_value_copy.value,
                    label: filter_value_copy.label,
                    content: '',
                    option: '包含'
                })
            }
            this.edit_options_disabled(val)
            this.filter_value = ''
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
        handle_select_change_dest(val) {
            if (this.dest_select_flag === true) {
                // 点击'应用'按钮的情况
                for (let item of val) {
                    for (let items of this.dest_all_list) {
                        if (item.id == items.id) {
                            items.is_selected = true
                        }
                    }
                }
                let sub_dest_list = JSON.parse(JSON.stringify(this.projForm.dest_list))
                for (let itemss of this.dest_all_list) {
                    let is_exit = false
                    let same_id = null
                    for (let itemsss of sub_dest_list) {
                        // 判断dest_all_list里的数据是否在projForm.dest_list中存在
                        if (itemss.id == itemsss.id) {
                            is_exit = true // 如果存在 is_exit 为 true
                            same_id = itemss.id
                            break
                        }
                    }

                    if (is_exit === true) {
                        // 存在相同数据的清空
                        if (itemss.is_selected == true) {
                            // 相同数据且is_selected为true情况下，就不用添加
                        } else {
                            // 相同数据且is_selected为false情况下，去除projForm.dest_list 中的这个数据
                            for (let i = 0, len = this.projForm.dest_list.length; i < len; i++) {
                                if (this.projForm.dest_list[i].id == same_id) {
                                    this.projForm.dest_list.splice(i, 1)
                                }
                            }
                        }
                    } else {
                        // 不存在相同数据的清空
                        if (itemss.is_selected == true) {
                            this.projForm.dest_list.push(itemss)
                        }
                    }
                }
            } else {
                // 点击'取消'按钮的情况
                this.projForm.dest_list = val
            }
        },
        transfer_filter_condition(table_name) {
            // 整合过滤条件
            let list_filter_condition = []
            let filter_condition_name = table_name + '_filter_condition'
            if (table_name == 'field') {
                return (list_filter_condition = this[filter_condition_name].filter(item => {
                    if (item.type === 'is_show') {
                        item.option = '等于'
                        if (item.content === '') {
                            item.content = false
                        }
                    }

                    return item.checked === true
                }))
            } else {
                return (list_filter_condition = this[filter_condition_name].filter(item => {
                    return item.checked === true
                }))
            }
        },
        search_detail(table_name) {
            const table_data_name = table_name + '_show_list'
            const proj_list = table_name + '_list'
            // this.projForm[proj_list] = this[table_data_name].filter(item => item.is_selected === true)
            const transfer_filter_condition_data = this.transfer_filter_condition(table_name)
            switch (table_name) {
                case 'dest':
                    this.req_detail_dest(transfer_filter_condition_data)
                    break
                case 'field':
                    this.req_detail_field(transfer_filter_condition_data)
                    break
                case 'keyword':
                    this.req_detail_keyword(transfer_filter_condition_data)
                    break
                default:
                    break
            }
        },
        empty_search_option(val) {
            switch (val) {
                case 'dest':
                    // if (this.dest_select_flag == true) {
                    this.selected_dest[0].checked = false  
                    this.dest_filter_condition = [
                        {
                            checked: true,
                            type: 'name',
                            label: '仕向地名称',
                            content: '',
                            option: '包含'
                        }
                    ]

                    this.edit_options_disabled(val) // 清空过滤条件

                    // 下面3行代码用来显示field table 勾选
                    this.dest_show_list = JSON.parse(JSON.stringify(this.temp_dest_all_list))
                    let dest_selected_list = JSON.parse(JSON.stringify(this.projForm.dest_list))
                    this.get_selected_list(dest_selected_list, this.dest_show_list)
                    this.check_full_box('dest')
                    this.dest_select_flag = false
                    // }

                    break
                case 'field':
                    // if (this.field_select_flag == true) {
                    this.selected_field[0].checked = false
                    this.field_filter_condition = [
                        {
                            checked: true,
                            type: 'name',
                            label: '自定义字段名称',
                            content: '',
                            option: '包含'
                        }
                    ]

                    this.edit_options_disabled(val) // 清空过滤条件

                    // 下面3行代码用来显示field table 勾选
                    this.field_show_list = JSON.parse(JSON.stringify(this.temp_field_all_list))
                    let field_selected_list = JSON.parse(JSON.stringify(this.projForm.field_list))
                    this.get_selected_list(field_selected_list, this.field_show_list)
                    this.check_full_box('field')
                    this.field_select_flag = false
                    // }

                    break
                case 'keyword':
                    // if (this.keyword_select_flag == true) {
                    this.selected_keyword[0].checked = false
                    this.keyword_filter_condition = [
                        {
                            checked: true,
                            type: 'keyword',
                            label: '关键字名称',
                            content: '',
                            option: '等于'
                        }
                    ]

                    this.edit_options_disabled(val) // 清空过滤条件

                    // 下面3行代码用来显示keyword table 勾选
                    this.keyword_show_list = JSON.parse(JSON.stringify(this.temp_keyword_all_list))
                    let keyword_selected_list = JSON.parse(JSON.stringify(this.projForm.keyword_list))
                    this.get_selected_list(keyword_selected_list, this.keyword_show_list)
                    this.check_full_box('keyword')

                    this.keyword_select_flag = false
                    // }

                    break
                default:
                    break
            }
        },
        confirm_submit(form_ame) {
            get_user_permission_list_fun(this.$store.getters.name,"项目管理/编辑").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.$nextTick(function() {
                        this.$refs[form_ame].validate(valid => {
                            if (valid) {

                                if(this.project_time == null) {
                                    
                                } else {
                                    this.projForm.create_time = this.project_time[0]
                                    this.projForm.finish_time = this.project_time[1]
                                }

                                this.projForm.user_name = this.$store.getters.name
                                const data = this.projForm
                                if (this.$store.getters.operation_type === 'edit') {
                                    edit_project(data).then(() => {
                                        this.$message({
                                            message: this.$t('operateTips.editSuccess'),
                                            type: 'success'
                                        })
                                        this.$router.push('/backstage/projectManage')
                                    })
                                } else {
                                    add_project(data).then(() => {
                                        this.$message({
                                            message: this.$t('operateTips.addSuccess'),
                                            type: 'success'
                                        })
                                        this.$router.push('/backstage/projectManage')
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
        cancel() {
            this.$router.push('/backstage/projectManage')
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
    max-height: 500px;
}
table th,
tr,
td {
    border: 1px solid #ebeef5;
}
thead {
    background: #ecf9f5;
    color: #909399;
}
tbody {
    color: #606266;
}
th {
    padding: 3px 0;
}

.project-form {
    width: 500px;

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

    input::-webkit-input-placeholder,
    textarea::-webkit-input-placeholder {
        /* WebKit browsers */
        color: #dcdfe6;
    }
    input:-moz-placeholder,
    textarea:-moz-placeholder {
        /* Mozilla Firefox 4 to 18 */
        color: #dcdfe6;
    }
    input::-moz-placeholder,
    textarea::-moz-placeholder {
        /* Mozilla Firefox 19+ */
        color: #dcdfe6;
    }
    input:-ms-input-placeholder,
    textarea:-ms-input-placeholder {
        /* Internet Explorer 10+ */
        color: #dcdfe6;
    }

    .line {
        text-align: center;
    }
}
.line {
    text-align: center;
}
</style>

