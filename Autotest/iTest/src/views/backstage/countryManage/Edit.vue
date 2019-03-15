<template>
    <div class="wrapper">
        <h2 class="title">{{title}}</h2>
        <div class="wrapper-content">
            <div class="wrapper-content-form">
                <div class="wrapper-content-form-content">
                    <el-form :model="countryForm" :rules="rules" ref="countryForm" label-width="110px">
                        <el-form-item :label="$t('country.countryCode')" prop="code">
                            <el-input v-model="countryForm.code"></el-input>
                        </el-form-item>
                        <el-form-item :label="$t('country.countryCnName')" prop="cn_name">
                            <el-input v-model="countryForm.cn_name"></el-input>
                        </el-form-item>
                        <el-form-item :label="$t('country.countryEnName')" prop="en_name">
                            <el-input v-model="countryForm.en_name"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </div>
        </div>

        <div class="wrapper-footer-btn">
            <el-button type="primary" @click="confirm_submit('countryForm')" size="small">{{$t('table.confirm')}}</el-button>
            <el-button @click="cancel('countryForm')" size="small">{{$t('table.cancel')}}</el-button>
        </div>
    </div>
</template>
<script>
import {
    get_country_list,
    add_country,
    submit_del_country,
    edit_country,
    export_country_excel,
    get_detail_country,
    del_batch_country
} from '@/api/backstage'
import { get_user_permission_list_fun, } from '@/api/backstage'
export default {
    data () {
        return {
            countryForm: {
                id: '',
                code: '',
                cn_name: '',
                en_name: ''
            },
            rules: {
                code: [{ required: true, message: this.$t('country.counrtyCodeTips'), trigger: 'change' }],
                cn_name: [{ required: true, message: this.$t('country.countryCnNameTips'), trigger: 'change' }],
                en_name: [{ required: true, message: this.$t('country.countryEnNameTips'), trigger: 'change' }]
            },
            params_data: null,
            title: '国家添加',
            original_data: ''
        }
    },
    // deactivated() {
    //     if (this.prompt_user_before_leave_page()) {
    //         console.log('999999999999')
    //         this.$router.push('/backstage/countryManage')
    //     }else {
    //         this.confirm_submit('countryForm')
    //     }
    // },
    // beforeDestroy () {//用于点左边目录时候，数据变化提示是否保存
    //     var save_data_str = JSON.stringify(this.countryForm)
    //     window.sessionStorage.setItem('save_data_str', save_data_str)
    //     if (this.raw_data_str == save_data_str) {
    //         return
    //     } else {
    //         this.$confirm('是否需要保存已编辑的信息', '提示', {
    //             confirmButtonText: '确定',
    //             cancelButtonText: '取消',
    //             type: 'warning'
    //         }).then(() => {
    //             this.leave_save()
    //         }).catch(() => {
    //         })
    //     }
    // },
    mounted () {
        this.params_data = JSON.parse(this.$route.query.params)
        if (this.params_data.type === 'edit') {
            this.countryForm = this.params_data
            this.original_data = JSON.stringify(this.params_data)
            this.title = '国家编辑'
        } else {
            this.original_data = JSON.stringify(this.countryForm)
            window.sessionStorage.setItem('raw_data_str', this.raw_data_str)
        }
    },
    methods: {
        confirm_submit (countryForm) {
            get_user_permission_list_fun(this.$store.getters.name, "国家管理/编辑").then(res => {
                console.log(res, '----')
                if (res.data.flag == true) {
                    this.$nextTick(function () {
                        this.$refs[countryForm].validate(valid => {
                            if (valid) {
                                if (this.params_data.type === 'add') {
                                    add_country(this.countryForm).then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.addSuccess'),
                                            type: 'success'
                                        })
                                        this.$refs[countryForm].resetFields()
                                        this.$router.push('/backstage/countryManage')
                                    })
                                } else if (this.params_data.type === 'edit') {
                                    edit_country(this.countryForm).then(res => {
                                        this.$message({
                                            message: this.$t('operateTips.editSuccess'),
                                            type: 'success'
                                        })
                                        this.$refs[countryForm].resetFields()
                                        this.$router.push('/backstage/countryManage')
                                    })
                                } else {
                                    // do nothing
                                }
                            } else {
                                return false
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
        cancel (countryForm) {
            this.prompt_user_before_leave_page()
        },
        prompt_user_before_leave_page () {
            if (this.original_data == JSON.stringify(this.countryForm)) {
                this.$router.push('/backstage/countryManage')
            } else {
                this.$confirm('是否需要保存已编辑的信息', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        this.confirm_submit('countryForm')
                    })
                    .catch(() => {
                        this.$router.push('/backstage/countryManage')
                    })
            }
        }
    }
}
</script>
<style scoped lang="scss">
</style>
