<template>
    <div class="wrapper">
        <h2 class="title">{{title}}</h2>
        <div class="wrapper-content">
            <div class="wrapper-content-form wrapper-content-select">
                <div class="wrapper-content-form-content ">
                    <span class="wrapper-content-select-span">{{title_two}}</span>
                    <el-select size="small" v-model="project_model" @change="select_project()" :disabled="select_project_flag" disabled>
                        <el-option v-for="(item, index) in select_project_options" :key="index" :label="item.name" :value="item.id">
                        </el-option>
                    </el-select>
                    <!-- <el-input v-model="title_two"></el-input> -->
                </div>
            </div>
            <div class="wrapper-content-form">
                <div class="wrapper-content-form-conten wrapper-content-form-custom">
                    <el-form ref="moduleForm" :model="moduleForm" :rules="rules" label-width="100px">
                        <el-form-item label="父模块名称" prop="parent_model_name">
                            <el-input class="wrapper-content-form-content-item" v-model="moduleForm.parent_model_name" :disabled="select_parent_module_flag"></el-input>
                        </el-form-item>
                        <el-form-item label="模块名称" prop="model_name">
                            <el-input class="wrapper-content-form-content-item" v-model="moduleForm.model_name"></el-input>
                        </el-form-item>
                        <el-form-item label="负责人" prop="charger">
                            <el-select v-model="moduleForm.charger" filterable remote placeholder="请输入搜索负责人名称" :remote-method="query_search_async" :loading="loading">
                                <el-option v-for="item in user_list" :key="item.id" :label="item.value" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <!-- <el-form-item label="模块描述" >
                        </el-form-item> -->
                        <!-- <div> -->
                        <div class="local-form-div">模块描述</div>
                        <el-input class="local-form-input" type="textarea" :autosize="{ minRows: 4, maxRows: 100}" v-model="moduleForm.model_intro"></el-input>
                        <!-- </div> -->
                        <!-- <el-form-item label="" prop="provider">
                            <el-input type="textarea" v-model="moduleForm.model_intro"></el-input>
                        </el-form-item> -->
                        <!-- <el-transfer v-model="landForm.country_list" :data="country_list" size="mini"></el-transfer> -->
                    </el-form>
                </div>
            </div>
            <fieldset class="wrapper-content-background">
                <legend class="wrapper-content-filter-title">选择自定义字段</legend>
                <div class="wrapper-content-filter">
                    <fieldset class="collapsible">
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
                    <fieldset class="collapsible">
                        <legend>
                            <i :class="filter_Flag? 'el-icon-caret-right':'el-icon-caret-bottom'" @click="fold_2()"></i>筛选器
                        </legend>
                        <div v-show="!filter_Flag">

                            <div class="filters-content">
                                <div v-for="(item, index) in filter_custom" :key="index" class="filters-content-field">
                                    <div class="filter-label">
                                        <!-- <el-checkbox v-model="item.checked" @change="checkbox_click">{{item.label}}</el-checkbox> -->
                                        <input type="checkbox" v-model="item.checked" class="input-checkbox">
                                        <label>{{item.label}}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </fieldset>
                    <div class="filter-option-bar">
                        <!-- <el-button type="text" size="mini" @click="search_detial_country()" >{{$t('table.apply')}}</el-button> -->
                        <!-- <el-button type="text" size="mini" @click="empty_search_option()" >{{$t('table.cancel')}}</el-button> -->
                        <span class="filter-option-bar-btn" @click="search_detial_country()">
                            <i class="el-icon-success"></i> 应用</span>
                        <span class="filter-option-bar-btn" @click="empty_search_option()">
                            <i class="el-icon-error"></i> 清除</span>
                    </div>
                </div>
                <div class="wrapper-content-table">
                    <el-table :data="module_field_list" border style="width: 100%" size="small" @selection-change="handle_select_change" ref="multipleTable">
                        <el-table-column type="selection" width="35" align="center">
                        </el-table-column>
                        <el-table-column prop="name" label="名称" align="center">
                        </el-table-column>
                        <el-table-column prop="type" label="类型" align="center">
                        </el-table-column>
                        <el-table-column label="选项" align="center">
                            <template slot-scope="scope">
                                <span v-for="(item, index) in scope.row.option_list" :key="index">
                                    {{item.value}}
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="is_show" label="显示" align="center">
                            <template slot-scope="scope">
                                <el-checkbox v-model="scope.row.is_show" disabled></el-checkbox>
                            </template>
                        </el-table-column>
                        <!-- <el-table-column label="操作" width="200" align="center">
                            <template slot-scope="scope">
                                <span class="btn-operate" @click="show_diff_field_dialog('edit', scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span>
                                <span class="btn-operate" @click="show_del_confirm(scope.row)"> &nbsp;[ {{$t('table.delete')}} ]</span>
                            </template>
                        </el-table-column> -->
                    </el-table>
                </div>
            </fieldset>
        </div>
        <div class="wrapper-footer-btn">
            <el-button type="primary" @click="confirm_submit('moduleForm')" size="small">{{$t('table.confirm')}}</el-button>
            <el-button @click="cancel('moduleForm')" size="small">{{$t('table.cancel')}}</el-button>
        </div>
    </div>
</template>
<script>
import { get_all_user } from '@/api/login'
import { add_module, get_project_list, edit_module, get_edit_module,get_project_fields_list } from '@/api/backstage'
export default {
    data() {
        return {
            moduleForm: {
                parent_model_name: '',
                parent_proj_id: '',
                parent_model_id: '',
                model_name: '',
                model_intro: '',
                charger: '',
                user_name: '',
                field_option_list: [],
                type: null
            },
            rules: {
                model_name: [{ required: true, message: '请输入模块名称', trigger: 'change' }],
                model_intro: [{ required: true, message: '请输入模块描述', trigger: 'change' }],
                charger: [{ required: true, message: '请输入模块负责人', trigger: 'change' }]
            },
            filter_value: '',
            filter_custom: [
                {
                    checked: false,
                    type: 'en_name',
                    label: '已选择自定义字段'
                }
            ],
            title: '模块添加',
            title_two: '项目选择',
            params_data: null,
            module_field_list: [],
            project_model: this.$store.getters.proj_id,
            filter_condition: [
                {
                    checked: true,
                    type: 'en_name',
                    label: '名称',
                    content: '',
                    option: '包含'
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
            options: [
                {
                    value: 'name',
                    label: '名称'
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
            filterFlag: false,
            filter_Flag: false,
            optimal_table_height: window.innerHeight - 220,
            select_project_options: [],
            select_project_flag: false,
            select_parent_module_flag: true,
            user_list: [],
            loading: false
        }
    },
    created() {
        this.params_data = JSON.parse(this.$route.query.params)
        if (this.params_data.type === 'edit') {
            this.edit_module_fun()
            this.title_two = '已选项目'
        } else {
            this.req_project()
            this.get_new_add_fields()//获取自定义字段
        }
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
        get_edit_module_fun() {
            let id = this.params_data.id
            return new Promise((resolve, reject) => {
                get_edit_module(id)
                    .then(res => {
                        this.module_field_list = res.data.field_list
                        this.$nextTick(() => {
                            for (let items of res.data.field_list) {
                                for (let id of res.data.check_field_list) {
                                    if (items.id == id) {
                                        // this.countryTable.push(item)
                                        // this.countryTableAfter = this.countryTable;//用于后面判断是否有筛选
                                        this.$refs.multipleTable.toggleRowSelection(items, true)
                                    }
                                }
                            }
                        })
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        edit_module_fun() {
            this.title = '模块编辑'
            // form表单赋值：
            this.filter_custom[0].checked = true
            this.select_project_flag = true
            this.moduleForm = this.params_data
            this.project_model = this.moduleForm.parent_proj.name
            this.moduleForm.parent_model_name = this.moduleForm.parent_model.model_name
            this.get_edit_module_fun() //获取自定义字段表格数据

            // console.log(this.moduleForm,'this.moduleForm')
        },
        req_project() {
            if (this.params_data.type == 'add_children') {
                this.select_project_flag = true
                this.title_two = '已选项目'
                this.project_model = this.params_data.parent_proj.name
                // this.moduleForm.parent_model_name = this.params_data.parent_model_name
                ;(this.moduleForm = {
                    parent_model_name: this.params_data.parent_model_name,
                    parent_proj_id: this.params_data.parent_proj.proj_id,
                    parent_model_id: this.params_data.id,
                    model_name: '',
                    model_intro: '',
                    charger: '',
                    user_name: '',
                    field_option_list: [],
                    type: null
                }),
                    (this.module_field_list = this.params_data.field_list)
            }
            return new Promise((resolve, reject) => {
                get_project_list()
                    .then(res => {
                        console.log(res,'请求项目')
                        this.select_project_options = res.data
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

        },
        confirm_submit(moduleForm) {
            this.$nextTick(function() {
                this.$refs[moduleForm].validate(valid => {
                    if (valid) {
                        if (this.params_data.type == 'add') {
                            //添加
                            if (this.project_model == '') {
                                this.$message({
                                    type: 'warning',
                                    message: '请选择项目'
                                })
                                return false
                            }
                            // console.log(this.project_model,'++++++++++++')
                            this.moduleForm.parent_proj_id = this.project_model
                            // console.log(this.moduleForm,'---------------------')
                            return new Promise((resolve, reject) => {
                                add_module(this.moduleForm)
                                    .then(res => {
                                        // console.log(res, "res")
                                        this.$message({
                                            type: 'success',
                                            message: '添加成功'
                                        })
                                        this.$router.push('/backstage/moduleManage')
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        } else if (this.params_data.type == 'edit') {
                            //编辑
                            // console.log(this.project_model)
                            // console.log(this.moduleForm, "编辑")
                            return new Promise((resolve, reject) => {
                                edit_module(this.moduleForm)
                                    .then(res => {
                                        // console.log(res, "res")
                                        this.$message({
                                            type: 'success',
                                            message: '添加成功'
                                        })
                                        this.$router.push('/backstage/moduleManage')
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        } else {
                            //子模块添加
                            // console.log(this.moduleForm,'children')
                            // return
                            return new Promise((resolve, reject) => {
                                add_module(this.moduleForm)
                                    .then(res => {
                                        // console.log(res, "res")
                                        this.$message({
                                            type: 'success',
                                            message: '添加成功'
                                        })
                                        this.$router.push('/backstage/moduleManage')
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        }
                    } else {
                        return false
                    }
                })
            })
        },
        fold() {
            this.filterFlag = !this.filterFlag
            // ???不加$nextTick为什么，table高度不变(this.optimal_table_height数据变了)
            this.$nextTick(() => {
                this.set_optimal_table_height()
            })
        },
        fold_2() {
            this.filter_Flag = !this.filter_Flag
            // ???不加$nextTick为什么，table高度不变(this.optimal_table_height数据变了)
            this.$nextTick(() => {
                this.set_optimal_table_height()
            })
        },
        set_optimal_table_height() {
            if (!this.isShowDialog) {
                let other_margin_height = 36
                let other_dom_height =
                    document.getElementsByClassName('wrapper')[0].offsetHeight +
                    document.getElementsByClassName('wrapper')[0].offsetHeight
                let container_height = document.getElementsByClassName('wrapper')[0].offsetHeight - 20
                this.optimal_table_height = container_height - other_dom_height - other_margin_height
            }
        },
        cancel(moduleForm) {
            this.$refs[moduleForm].resetFields()
            this.clean_form_content()
            this.$router.push('/backstage/moduleManage')
        },
        clean_form_content() {
            this.moduleForm = {
                parent_proj_id: '',
                parent_model_id: '',
                model_name: '',
                model_intro: '',
                charger: '',
                user_name: '',
                field_option_list: [],
                type: null
            }
        },
        select_project() {
            if (this.project_model !== '') {
                let project_id = Number(this.project_model),
                    module_field_table_list = this.select_project_options
                for (const item of module_field_table_list) {
                    if (project_id == item.id) {
                        this.module_field_list = item.field_list
                        break
                    }
                }
            }
        },
        handle_select_change(val) {
            // console.log(this.moduleForm, 'this.moduleForm选择')
            // console.log(val, 'val')
            this.moduleForm.field_option_list = val.map(item => {
                return item.id
            })
        },
        get_new_add_fields(){
            let proj_id = this.project_model
            console.log(proj_id,'proj_id')
            return new Promise((resolve, reject) => {
                get_project_fields_list(proj_id)
                    .then(res => {
                        this.module_field_list = res.data.field_list
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        }
    }
}
</script>
<style scoped lang="scss">
.wrapper-content-select {
    height: 65px;
    color: #606266;
    margin: 0 0 20px;
    font-size: 14px;
}
.wrapper-content-select-span {
    padding: 0 10px 0 33px;
}

// margin-left: 30px;
/* display: inherit; */
/* position: absolute; */
/* top: 325px; */
// width: 178%;
</style>
