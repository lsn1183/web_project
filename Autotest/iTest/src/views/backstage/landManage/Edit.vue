<template>
    <div class="wrapper">
        <h2 class="title">{{title}}</h2>

        <div class="wrapper-content">
            <div class="wrapper-content-form">
                <div class="wrapper-content-form-conten">
                    <el-form ref="landForm" :model="landForm" :rules="rules" label-width="100px">
                        <el-form-item label="仕向地名称" prop="name">
                            <el-input class="wrapper-content-form-content-item" v-model="landForm.name"></el-input>
                        </el-form-item>
                        <el-form-item label="数据供应商" prop="provider">
                            <el-input class="wrapper-content-form-content-item" v-model="landForm.provider"></el-input>
                        </el-form-item>
                        <!-- <el-form-item label="仕向地简介" prop="introduce">
                            <el-input type="textarea" autosize v-model="landForm.introduce"></el-input>
                        </el-form-item> -->
                        <div class="local-form-div">仕向地简介</div>
                        <el-input type="textarea" class="local-form-input" :autosize="{ minRows: 4, maxRows: 100}" v-model="landForm.introduce"></el-input>
                        <!-- <el-transfer v-model="landForm.country_list" :data="country_list" size="mini"></el-transfer> -->
                    </el-form>
                </div>
            </div>
            <fieldset class="wrapper-content-background">
                <legend class="wrapper-content-filter-title">选择国家</legend>
                <div class="wrapper-content-filter">
                    <fieldset class="collapsible">
                        <legend>
                            <i :class="filterFlag? 'el-icon-caret-right':'el-icon-caret-bottom'" @click="fold()"></i>{{$t('country.filter')}}
                        </legend>
                        <div v-show="!filterFlag">
                            <div class="add-filter">
                                {{$t('country.addFilter')}}:
                                <el-select size="mini" v-model="fliter_value" @change="add_filter()">
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
                                <div v-for="(item, index) in filter_country" :key="index" class="filters-content-field">
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
                        <span class="filter-option-bar-btn" @click="search_detial_country()">
                            <i class="el-icon-success"></i> 应用</span>
                        <span class="filter-option-bar-btn" @click="clear_search_option()">
                            <i class="el-icon-error"></i> 清除</span>
                    </div>
                </div>
                <div class="wrapper-content-table">
                    <el-table :data="countryTable" ref="multipleTable" border style="width: 100%" @select-all="select_all" size="small" @select='select'>
                        <el-table-column type="selection" width="35" align="center">
                        </el-table-column>
                        <el-table-column prop="code" label="ISO三位国家代码" align="center" width="200px">
                        </el-table-column>
                        <el-table-column prop="en_name" :label="$t('country.countryEnName')" align="center">
                        </el-table-column>
                        <el-table-column prop="cn_name" :label="$t('country.countryCnName')" align="center">
                        </el-table-column>

                        <!-- <el-table-column label="操作" align="center">
                            <template slot-scope="scope">
                                <span class="btn-operate" size="small" @click="show_edit_country_dialog(scope.row)"> &nbsp;[ {{$t('table.edit')}} ]</span>
                                <span class="btn-operate" size="small" @click="show_del_country_tips(scope.row)"> &nbsp;[ {{$t('table.delete')}} ]</span>
                            </template>
                        </el-table-column> -->
                    </el-table>
                </div>
            </fieldset>
        </div>
        <div class="wrapper-footer-btn">
            <el-button type="primary" @click="confirm_submit('landForm')" size="small">{{$t('table.confirm')}}</el-button>
            <el-button @click="cancel('landForm')" size="small">{{$t('table.cancel')}}</el-button>
        </div>
    </div>
</template>
<script>
import {
    get_land_list,
    add_land,
    edit_land,
    get_country_list,
    del_batch_land,
    get_detail_country,
} from '@/api/backstage'
export default {
    data () {
        return {
            landForm: {
                id: '',
                name: '',
                provider: "",
                introduce: '',
                country_list: [],
                type: null
            },
            rules: {
                name: [{ required: true, message: '请输入仕向地名称', trigger: 'change' }],
                provider: [{ required: true, message: '请输入数据供应商名称', trigger: 'change' }],
                introduce: [{ required: true, message: '请输入仕向地简介', trigger: 'change' }]
            },
            country_list: [],
            params_data: null,
            filterFlag: false,
            filter_Flag: false,
            fliter_value: '',
            filter_condition: [
                {
                    checked: true,
                    type: 'en_name',
                    label: '国家英文名称',
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
            filter_country: [
                {
                    checked: false,
                    type: 'en_name',
                    label: '已选择国家',
                }
            ],
            options: [
                {
                    value: 'en_name',
                    label: '国家英文名称'
                },
                {
                    value: 'cn_name',
                    label: '国家中文名称'
                },
                {
                    value: 'code',
                    label: 'ISO三位国家代码'
                }

            ],
            countryTable: [],
            countryTableBegin: [],
            countryTableAfter: [],
            optimal_table_height: window.innerHeight - 220,
            select_country_list: [],
            title: "仕向地添加",
            select_country_list_save: []


        }
    },
    created () {
        this.params_data = JSON.parse(this.$route.query.params)
        if (this.params_data.type === 'edit') {
            this.landForm = this.params_data
            this.title = "仕向地编辑"
            this.filter_country[0].checked = true
        }
        this.req_country()
    },
    computed: {

    },
    methods: {
        show_edit () {
            this.$emit('showEdit')
        },
        req_country () {
            return new Promise((resolve, reject) => {
                get_country_list()
                    .then(res => {
                        if (this.params_data.type === 'edit') {//编辑时候默认勾选
                            this.countryTableBegin = res.data
                            this.countryTable = []
                            this.$nextTick(() => {
                                for (const item of this.countryTableBegin) {//this.filter_country[0].checked === true
                                    for (const id of this.params_data.country_list) {
                                        if (item.id == id) {
                                            this.countryTable.push(item)
                                            this.select_country_list.push(item.id)//初始化已勾选的数组
                                            this.select_country_list = Array.from(new Set(this.select_country_list))
                                            this.$refs.multipleTable.toggleRowSelection(item, true)
                                        }
                                    }
                                }
                            })
                        } else {
                            this.countryTableBegin = res.data
                            this.countryTable = this.countryTableBegin
                        }
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        confirm_submit (landForm) {
            this.$nextTick(function () {
                this.$refs[landForm].validate(valid => {
                    if (valid) {
                        if (this.params_data.type === 'add') {
                            return new Promise((resolve, reject) => {
                                this.landForm.country_list = this.select_country_list
                                add_land(this.landForm)
                                    .then(res => {
                                        this.$message({
                                            message: '添加成功',
                                            type: 'success'
                                        })
                                        this.$refs[landForm].resetFields()
                                        this.show_edit()
                                        this.$router.push("/backstage/landManage")
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        } else if (this.params_data.type === 'edit') {
                            return new Promise((resolve, reject) => {
                                this.landForm.country_list = this.select_country_list
                                edit_land(this.landForm)
                                    .then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.editSuccess'),
                                            type: 'success'
                                        })
                                        this.$refs[landForm].resetFields()
                                        this.show_edit()
                                        this.$router.push("/backstage/landManage")

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
        clean_form_content () {
            this.landForm = {
                id: '',
                abbreviation: '',
                country_list: [],
                introduce: '',
                name: ''
            }
        },
        cancel (landForm) {
            this.$refs[landForm].resetFields()
            this.clean_form_content()
            this.show_edit()
            this.$router.push("/backstage/landManage")
        },
        select (select_all_data, select_item) {
            if (this.select_country_list.indexOf(select_item.id) !== -1) {//执行删除
                let index = this.select_country_list.indexOf(select_item.id)
                this.select_country_list.splice(index, 1)
            }
            select_all_data.map(item => {
                this.select_country_list.push(item.id)
            })
            this.select_country_list = Array.from(new Set(this.select_country_list))
        },
        select_all (select_all_data) {//全选触发
            this.select_country_list = select_all_data.map(item => {
                return item.id
            })
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
        add_filter_option (index) {
            this.edit_options_disabled()
            let new_filter_option = {
                type: '',
                label: '',
                content: '',
                option: '等于'
            }
            this.filter_condition.splice(index + 1, 0, new_filter_option)
        },
        del_filter_option (index) {
            this.filter_condition.splice(index, 1)
            this.edit_options_disabled()
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
                    option: '等于'
                })
            }
            this.edit_options_disabled()
            this.fliter_value = ''
        },
        fold () {
            this.filterFlag = !this.filterFlag
            // ???不加$nextTick为什么，table高度不变(this.optimal_table_height数据变了)
            this.$nextTick(() => {
                this.set_optimal_table_height()
            })
        },
        fold_2 () {
            this.filter_Flag = !this.filter_Flag
            // ???不加$nextTick为什么，table高度不变(this.optimal_table_height数据变了)
            this.$nextTick(() => {
                this.set_optimal_table_height()
            })
        },
        set_optimal_table_height () {
            if (!this.isShowDialog) {
                let other_margin_height = 36
                let other_dom_height =
                    document.getElementsByClassName('wrapper')[0].offsetHeight +
                    document.getElementsByClassName('wrapper')[0].offsetHeight
                let container_height =
                    document.getElementsByClassName('wrapper')[0].offsetHeight - 20
                this.optimal_table_height = container_height - other_dom_height - other_margin_height
            }
        },
        search_detial_country () {
            let list_filter_condition = this.filter_condition.filter(item => {
                return item.checked === true
            })
            if (list_filter_condition.length === 0) {//去掉国家勾选
                this.filter_country_list_fun()
            } else {
                let obj_filter_condition = { filter_condition: list_filter_condition }
                return new Promise((resolve, reject) => {
                    get_detail_country(list_filter_condition)
                        .then(res => {
                            let req_country = res.data
                            // 用于判断筛选器是否有勾选
                            if (this.params_data.type === 'edit') {//编辑模式
                                if (this.filter_country[0].checked == true) {//筛选打钩，
                                    this.countryTable = []
                                    for (const req_country_item of req_country) {
                                        for (const select_id of this.select_country_list) {
                                            if (req_country_item.id == select_id) {
                                                this.countryTable.push(req_country_item)
                                                this.$nextTick(() => {
                                                    this.$refs.multipleTable.toggleRowSelection(req_country_item, true)
                                                })
                                                break
                                            }
                                        }
                                    }
                                } else {//筛选不打勾
                                    this.countryTable = req_country
                                    this.$nextTick(() => {
                                        for (const item of req_country) {
                                            for (const id of this.select_country_list) {
                                                if (id == item.id) {
                                                    this.$refs.multipleTable.toggleRowSelection(item, true)
                                                    break
                                                }
                                            }
                                        }
                                    })
                                }
                            } else {//添加模式
                                if (this.filter_country[0].checked == true) {//筛选打钩，
                                    this.countryTable = []
                                    for (const req_country_item of req_country) {
                                        for (const select_id of this.select_country_list) {
                                            if (req_country_item.id == select_id) {
                                                this.countryTable.push(req_country_item)
                                                this.$nextTick(() => {
                                                    this.$refs.multipleTable.toggleRowSelection(req_country_item, true)
                                                })
                                                break
                                            }
                                        }
                                    }
                                } else {//筛选不打勾
                                    this.countryTable = req_country
                                    this.$nextTick(() => {
                                        for (const item of req_country) {
                                            for (const id of this.select_country_list) {
                                                if (id == item.id) {
                                                    this.$refs.multipleTable.toggleRowSelection(item, true)
                                                    break
                                                }
                                            }
                                        }
                                    })
                                }
                            }
                        })
                        .catch(err => {
                            reject(err)
                        })
                })
            }
        },
        clear_search_option () {
            this.filter_condition = [
                {
                    checked: true,
                    type: 'en_name',
                    label: '国家英文名称',
                    content: '',
                    option: '包含'
                }
            ],
                this.edit_options_disabled()
            this.filter_country[0].checked = false
            this.countryTable = this.countryTableBegin
            for (const item of this.countryTableBegin) {
                for (const id of this.select_country_list) {
                    if (id == item.id) {
                        this.$nextTick(() => {
                            this.$refs.multipleTable.toggleRowSelection(item, true)
                        })
                    }
                }
            }
        },
        filter_country_list_fun () {
            return new Promise((resolve, reject) => {
                get_country_list()
                    .then(res => {
                        if (this.params_data.type === 'edit') {//编辑时候默认勾选
                            this.countryTableBegin = res.data
                            this.countryTable = []
                            if (this.filter_country[0].checked === false) {//当去掉勾选国家/筛选国家后，点击搜索表格应该是全部数据及勾选过的
                                this.countryTable = this.countryTableBegin //所有国家
                                for (const item of this.countryTableBegin) {
                                    for (const id of this.select_country_list) {
                                        if (id == item.id) {
                                            this.$nextTick(() => {
                                                this.$refs.multipleTable.toggleRowSelection(item, true)
                                            })

                                        }
                                    }
                                }
                            } else {
                                for (const item of this.countryTableBegin) {//this.filter_country[0].checked === true
                                    for (const id of this.select_country_list) {
                                        if (item.id == id) {
                                            this.countryTable.push(item)
                                            this.$nextTick(() => {
                                            this.$refs.multipleTable.toggleRowSelection(item, true)
                                            })
                                        }
                                    }
                                }
                            }

                        } else {
                            this.countryTableBegin = res.data
                            this.countryTable = this.countryTableBegin
                        }
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },

    }
}

</script>
<style scoped lang="scss">
.filter-option-bar-btn {
    color: #42b983;
    padding: 0 10px 0;
    cursor: pointer;
}
</style>
