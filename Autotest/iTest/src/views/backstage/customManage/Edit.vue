<template>
    <div class="wrapper">
        <h2 class="title line-height">{{title}}
            <i class="el-icon-question icon-question" title='未有内容'></i>
        </h2>
        <div class="wrapper-content">
            <div class="wrapper-content-form">
                <div class="wrapper-content-form-content">
                    <el-form :model="field_form" :rules="rules" ref="filedForm" label-width="150px">
                        <el-form-item label="标签名称" prop="name">
                            <el-input v-model="field_form.name"></el-input>
                        </el-form-item>
                        <el-form-item label="字段名称" prop="en_name">
                            <el-input v-model="field_form.en_name"></el-input>
                        </el-form-item>
                        <el-form-item label="填写类型" prop="type">
                            <el-select v-model="field_form.type" placeholder="" style="display: block;">
                                <el-option v-for="item in type_select_options" :key="item.label" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="启用" prop="field_open_use">
                            <el-select v-model="field_form.field_open_use" placeholder="" style="display: block;">
                                <el-option v-for="item in enable_select_options" :key="item.label" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="显示在测试执行中" prop="is_show">
                            <!-- <el-checkbox v-model="field_form.is_show"></el-checkbox> -->
                            <el-select v-model="field_form.is_show" placeholder="是或否" style="display: block;">

                                <el-option v-for="item in show_select_options" :key="item.label" :label="item.label" :value="item.value"></el-option>

                                <!-- <el-option label="是" value="true"></el-option>
                                <el-option label="否" value="false"></el-option> -->

                            </el-select>
                        </el-form-item>
                        <el-form-item label="字段选项" prop="option_list" v-show="this.field_form.type == 'multiSelect' ||
                            this.field_form.type == 'checkbox' ||
                            this.field_form.type == 'select'">
                            <div v-if="field_form.option_list.length === 0">
                                <div>
                                    <el-input v-model="add_options">
                                        <el-button slot="append" icon="el-icon-plus" @click="add_field_options()" size="small"></el-button>
                                    </el-input>
                                    <span style="font-size: 12px; color: #f56c6c;">请新增字段选项</span>
                                </div>
                                <!-- <span style="font-size: 12px; color: #f56c6c;line-height: 12px;height: 12px;">请新增字段选项</span> -->
                            </div>
                            <div>
                                <el-tag type="success" v-for="(tag, index) in field_form.option_list" :key="index" closable @close="del_tag(index)" v-if="field_form.option_list.length !== 0" style="margin-bottom: 5px;">
                                    {{tag.value}}
                                </el-tag>
                            </div>
                        </el-form-item>
                        <el-form-item label="" v-if="field_form.option_list.length !== 0">
                            <el-input v-model="add_options" placeholder="新增字段添加框">
                                <el-button slot="append" icon="el-icon-plus" @click="add_field_options()" size="small"></el-button>
                            </el-input>
                        </el-form-item>
                        <el-form-item label="显示次序" prop="sort_num">
                            <el-input v-model="field_form.sort_num"></el-input>

                        </el-form-item>
                    </el-form>
                </div>
            </div>
        </div>

        <div class="wrapper-footer-btn">
            <el-button type="primary" @click="confirm_submit('filedForm')" size="small">{{$t('table.confirm')}}</el-button>
            <el-button @click="cancel('filedForm')" size="small">{{$t('table.cancel')}}</el-button>
        </div>
    </div>

</template>
<script>
import { edit_custom_field, add_custom_field } from '@/api/backstage'
export default {
    data() {
        return {
            field_form: {
                id: null,
                is_show: '',
                name: '',
                type: '',
                option_list: [],
                field_open_use: '',
                sort_num: null
            },
            rules: {
                name: [{ required: true, message: '请输入标签名称', trigger: 'change' }],
                en_name: [{ required: true, message: '请输入字段名称', trigger: 'change' }],
                type: [{ required: true, message: '请输入类型', trigger: 'change' }],
                field_open_use: [{ required: true, message: '请选择启用', trigger: 'change' }],
                is_show: [{ required: true, message: '请选择', trigger: 'change' }],
                sort_num: [{ required: true, message: '请输入排序', trigger: 'change' }]
            },
            add_options: '',
            title: '自定义字段添加',
            type_select_options: [
                { label: '单选', value: 'checkbox' },
                { label: '多选', value: 'multiSelect' },
                { label: '下拉框', value: 'select' },
                { label: '单行文本', value: 'input' },
                { label: '多行文本', value: 'textarea' }
            ],
            enable_select_options: [
                { label: '测试用例', value: 'test_example' },
                { label: '测试执行', value: 'test_execution' }
            ],
            show_select_options: [{ label: '是', value: true }, { label: '否', value: false }]
        }
    },
    created() {
        if (this.$store.getters.operation_type === 'edit') {
            this.field_form = this.$store.getters.operation_data
            this.title = '自定义字段编辑'
        }
    },
    methods: {
        add_field_options() {
            if (this.add_options !== '') {
                let add_options = { id: null, value: this.add_options }
                this.add_options = ''
                this.field_form.option_list.push(add_options)
            }
        },
        confirm_submit(fieldForm) {
            let submit_type = this.$store.getters.operation_type
            let data = this.field_form
            this.$nextTick(() => {
                this.$refs[fieldForm].validate(valid => {
                    if (valid) {
                        if (submit_type === 'add') {
                            if (this.field_form.sort_num == '') {
                                return false
                            }
                            return new Promise((resolve, reject) => {
                                add_custom_field(data)
                                    .then(() => {
                                        this.$message({
                                            message: this.$t('operateTips.addSuccess'),
                                            type: 'success'
                                        })
                                        // this.empty_dialog_req_table(fieldForm)
                                        this.$router.push('/backstage/customManage')
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        } else if (submit_type === 'edit') {
                            return new Promise((resolve, reject) => {
                                edit_custom_field(data)
                                    .then(() => {
                                        this.$message({
                                            message: this.$t('operateTips.editSuccess'),
                                            type: 'success'
                                        })
                                        // this.empty_dialog_req_table(fieldForm)
                                        this.$router.push('/backstage/customManage')
                                    })
                                    .catch(err => {
                                        reject(err)
                                    })
                            })
                        } else {
                            // do nothing
                        }
                    }
                })
            })
        },
        del_tag(index) {
            this.field_form.option_list.splice(index, 1)
        },
        cancel() {
            this.$router.push('/backstage/customManage')
        }
    }
}
</script>
<style scoped lang="scss">
.line-height {
    line-height: 23px;
    .icon-question {
        font-size: 15px;
        // float: left;
        line-height: 23px;
        margin: 0 5px;
        color: #606266;
    }
}
</style>

