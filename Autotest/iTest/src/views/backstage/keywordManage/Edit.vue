<template>
    <div class="wrapper">
        <h2 class="title" v-if="title_show_flag">关键字添加</h2>
        <h2 class="title" v-else>关键字编辑</h2>
        <div class="wrapper-content">
            <div class="wrapper-content-form">
                <el-form :model="keyForm" :rules="rules" ref="keyform" label-width="100px" class="wrapper-content-block">
                    <el-form-item :label="form_label" prop="name">
                        <el-input v-model="keyForm.name"></el-input>
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <div class="wrapper-footer-btn">
            <el-button type="primary" @click="confirm_submit('keyform')" size="small">{{$t('table.confirm')}}</el-button>
            <el-button @click="cancel('keyform')" size="small">{{$t('table.cancel')}}</el-button>
        </div>
    </div>
</template>
<script>
import { add_keyword, edit_keyword } from '@/api/backstage'
import { get_user_permission_list_fun, } from '@/api/backstage'
export default {
    name: 'component_name',
    data () {
        return {
            keyForm: {
                name: '',
                id: null,
                type: 'add'
            },
            rules: {
                name: [{ required: true, message: '请输入关键字', trigger: 'change' }]
            },
            title_show_flag: true,
            form_label: '添加关键字'
        }
    },
    created () {
        if (this.$route.query.params) {
            this.title_show_flag = false
            this.form_label = '编辑关键字'
            let value = JSON.parse(this.$route.query.params)
            this.keyForm.name = value.name
            this.keyForm.id = value.id
            this.keyForm.type = 'edit'
        } else {
        }
    },
    mounted () { },
    methods: {
        confirm_submit (keyform) {
            let perm_data = {
                "user_name": this.$store.getters.name,
                "per_name": "关键字管理"
            }
            get_user_permission_list_fun(perm_data).then(res => {
                // console.log(res, '----')
                if (res.data.flag == true) {
                    this.$refs[keyform].validate(valid => {
                        if (valid) {
                            return new Promise((resolve, reject) => {
                                if (this.keyForm.type == 'add') {
                                    add_keyword(this.keyForm)
                                        .then(res => {
                                            if (res != undefined) {
                                                this.$message({
                                                    message: '添加成功',
                                                    type: 'success'
                                                })
                                                this.$refs[keyform].resetFields()
                                                this.$router.push('/backstage/keywordManage/keywordShow')
                                            }
                                        })
                                        .catch(err => {
                                            reject(err)
                                        })
                                } else if (this.keyForm.type == 'edit') {
                                    edit_keyword(this.keyForm, this.keyForm.id)
                                        .then(res => {
                                            if (res != undefined) {
                                                this.$message({
                                                    message: '编辑成功',
                                                    type: 'success'
                                                })
                                                this.$refs[keyform].resetFields()
                                                this.$router.push('/backstage/keywordManage/keywordShow')
                                            }
                                        })
                                        .catch(err => {
                                            reject(err)
                                        })
                                }
                            })
                        } else {
                            return
                        }
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
            this.$router.push('/backstage/keywordManage/keywordShow')
        }
    }
}
</script>
<style lang="scss" scoped>
.wrapper-content-block {
    width: 60%;
}
</style>