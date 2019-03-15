<template>
    <div class="add-project-step">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="项目信息" icon="el-icon-edit" status="process">1</el-step>
                    <!-- <el-step class="jump" title="平台" >2</el-step> -->
                    <el-step class="jump" title="知识库">3</el-step>
                    <el-step class="jump" title="模块">4</el-step>
                    <el-step class="jump" title="模块负责组">5</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Title">
            <div class="mid">
                <div class="mid-top">
                    <div class="div-center">
                        <div class="div-title div-title-ex">
                            <h2>项目信息</h2>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">项目名称:</div>
                        <div class="div-input" v-if="project_title_flag">
                            <!-- <el-input  v-model="file_form.proj_name"></el-input> -->
                            <el-select v-model="project_model" placeholder="请选择" clearable @visible-change="reqStepOneData" @clear="clearClick" @change="optionChangeValue()">
                                <el-option v-for="item in project_options" :key="item.proj_id" :label="item.proj_name" :value="item.proj_id">
                                </el-option>
                            </el-select>
                        </div>
                        <div class="div-input" v-else>
                            <el-input v-model="file_form.proj_name"></el-input>
                        </div>
                    </div>
                    <div class="div-radio div-center-label">
                        <div class="div-title summary">项目类型:</div>
                        <el-radio-group v-model="file_form.proj_tag_id">
                            <el-radio :label="item.tag_id" :key="item.tag_id" class="checkradio" v-for="item in radiolist">{{item.tag}}</el-radio>
                        </el-radio-group>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title summary">概述:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.summary" type="textarea" :autosize="{ minRows: 3, maxRows:6}"></el-input>
                        </div>
                    </div>

                    <div class="div-center div-center-label">
                        <div class="div-title">版本:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.ver" disabled></el-input>
                        </div>
                    </div>

                    <div class="div-center div-center-label">
                        <div class="div-title">项目管理者:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.proj_manager" disabled></el-input>
                        </div>
                    </div>
                    <!-- <div class="div-center div-center-label">
                        <div class="div-title">项目更新者:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.editor" disabled></el-input>
                        </div>
                    </div> -->
                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="info" disabled>
                        <i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button @click="save()" type="primary" size='mini' :disabled="disabled_flag">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button @click="cancel()" type="primary" size='mini'>&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="next()" :disabled="disabled_flag">下一步
                        <i class="el-icon-arrow-right"></i>
                    </el-button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
require('../../../assets/js/jquery-1.8.3.min.js')
export default {
    data () {
        return {
            projectStepOndData: { proj_name: '', proj_id: '' },
            active: Number(window.sessionStorage.getItem('step_id')),
            file_form: {
                // proj_name: '',
                // proj_id: Number(window.sessionStorage.getItem('proj_id')),
                // manager: window.sessionStorage.getItem('Uall'),
                // summary: '',
                // proj_tag_id: '',
                // ver: 0.01,
                'fw_id': null,
                'fw_name': null,
                'fw_manager': null,
                'proj_id': "",
                'proj_name': "",
                'proj_manager': "",
                'summary': "",
                'proj_tag_id': "",
                'ver': 0.01,
            },
            radiolist: [],
            get_data: '',
            save_data: '',
            project_options: [],
            project_model: "",
            project_title_flag: true,
            disabled_flag:true
        }
    },
    computed:{
        watchDisabledFun(val){
            return this.project_model
        },
        watchDisabledFunTwo(val){
            return this.file_form.proj_name
        }
    },
    watch:{
        watchDisabledFun(val){
            if(val !=="" ){
                this.disabled_flag=false
            }else{
                this.disabled_flag=true
            }
        },
        watchDisabledFunTwo(val){
            if(val !=="" ){
                this.disabled_flag=false
            }else{
                this.disabled_flag=true
            }
        }
    },
    mounted () {
        this.getTag()
        var self = this
        $('.jump').on('click', function (e) {
            self.jump_to($(this).text())
        });
        if (this.$route.query.flag == "false") {//编辑项目
            this.project_title_flag = false
            this.getStepOneData()
        } else {
            // nothing to do
            this.get_data=JSON.stringify(this.file_form)
        }
    },
    methods: {
        clearClick () {
        },
        optionChangeValue () {
            // 选择项目时候，赋值数据
            if (this.project_model !== "") {
                for (const item of this.project_options) {
                    if (item.proj_id == this.project_model) {
                        this.file_form.fw_id = item.fw_id
                        this.file_form.fw_name = item.fw_name
                        this.file_form.fw_manager = item.fw_manager
                        this.file_form.proj_id = this.project_model
                        this.file_form.proj_name = item.proj_name
                        this.file_form.proj_manager = item.proj_manager
                    }
                }
            }
        },
        getStepOneData () {
            if (window.sessionStorage.getItem('proj_id') != null) {
                this.$axios.get(this.Ip + '/Project/' + window.sessionStorage.getItem('proj_id')).then(res => {
                    // console.log(res, "pg")
                    if (res.data.result == 'OK') {
                        this.file_form.proj_name = res.data.content[0].proj_name
                        this.file_form.proj_id = res.data.content[0].proj_id
                        this.file_form.proj_manager = res.data.content[0].manager
                        this.file_form.summary = res.data.content[0].summary
                        this.file_form.proj_tag_id = res.data.content[0].proj_tag_id
                        this.file_form.ver = res.data.content[0].ver
                        this.file_form.fw_id = res.data.content[0].fw_id
                    } else {
                    }
                    this.get_data = JSON.stringify(this.file_form)
                }).catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0,
                    })
                })
            }
        },
        reqStepOneData () {
            let datas = { "accessToken": window.sessionStorage.getItem("accessToken"), "manager": window.sessionStorage.getItem("Uall") }
            if (this.project_model === "") {
                this.$axios.post(this.Ip + "/GetCactusProject", datas).then(res => {
                    // console.log(res)
                    if (res.data.result == 'OK') {
                        this.project_options = res.data.content
                        // this.file_form.proj_id = res.data.content[0].proj_id
                        // this.file_form.manager = res.data.content[0].proj_manager
                    } else {
                        this.$message({
                            showClose: true,
                            message: '您无项目可添加',
                            type: 'warning',
                            duration: 20,
                        })
                    }
                }).catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 20,
                    })
                })
            } else {
                return
            }
        },
        getTag () {
            this.$axios.get(this.Ip + '/DocTagProject/special').then(res => {
                // console.log(res, "DT")
                if (res.data.result == 'OK') {
                    this.radiolist = res.data.content.proj_tag
                } else {
                }
            }).catch(err => {
                this.$message({
                    showClose: true,
                    message: '服务异常',
                    type: 'error',
                    duration: 0,
                })
            })
        },
        next () {
            if (this.project_title_flag==true) {
                this.file_form.proj_id = this.project_model
            }
            if (this.file_form.proj_name == '') {
                this.$message({
                    message: '项目名不能为空',
                    type: 'error'
                })
                return
            } else if (this.file_form.proj_tag_id == '') {
                this.$message({
                    message: '类型不能为空',
                    type: 'error'
                })
                return
            }
            // console.log(this.file_form)
            this.$axios.post(this.Ip + '/Project', this.file_form)
                .then(res => {
                    // console.log(res, "保存")
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('proj_id', res.data.content)
                        window.sessionStorage.setItem('proj_name', this.file_form.proj_name)
                        if (window.sessionStorage.getItem('step_id') == 0) {
                            window.sessionStorage.setItem('step_id', 1)//直接跳过平台
                        }
                        // this.$router.push('/tagl/Project_Step_Two')
                        let router_flag=this.$route.query.flag
                        let routerValue={path:'/tagl/Project_Step_Three',query:{flag:"false"}}
                        this.$router.push(routerValue)
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败',
                            type: 'error',
                            duration: 20,
                        })
                    }
                })
                .catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0,
                    })
                })
        },
        save () {
            if (this.file_form.proj_name == '') {
                this.$message({
                    message: '项目名不能为空',
                    type: 'error'
                })
                return
            } else if (this.file_form.proj_tag_id == '') {
                this.$message({
                    message: '类型不能为空',
                    type: 'error'
                })
                return
            }
            // return
            this.$axios.post(this.Ip + '/Project', this.file_form).then(res => {
                // console.log(res)
                if (res.data.result == 'OK') {
                    window.sessionStorage.setItem('proj_id', res.data.content)
                    window.sessionStorage.setItem('proj_name', this.file_form.proj_name)
                    this.file_form.proj_id = res.data.content
                    this.project_title_flag = false
                    this.getStepOneData()
                    this.$message({
                        message: '保存成功',
                        type: 'success'
                    })
                } else {
                    this.$message({
                        showClose: true,
                        message: '失败:'+res.data.error,
                        type: 'error',
                        duration: 0,
                    })
                }
            }).catch(err => {
                this.$message({
                    showClose: true,
                    message: '服务异常',
                    type: 'error',
                    duration: 0,
                })
            })

        },
        JumpAndSave () {
            this.$axios.post(this.Ip + '/Project', this.file_form)
                .then(res => {
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('proj_id', res.data.content)
                        // if(window.sessionStorage.getItem('step_id') != 4) {
                        //     window.sessionStorage.setItem('step_id', 1)
                        //     this.$store.state.step_id = 1
                        // }
                        this.$message({
                            message: '保存成功',
                            type: 'success'
                        })
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败',
                            type: 'error',
                            duration: 0,
                        })
                    }
                })
                .catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0,
                    })
                })
        },
        jump_to (index) {
            switch (index) {
                case "项目信息":
                    // this.JumpAndSave()
                    var router_flag=this.$route.query.flag
                    var routerValue={path:'/tagl/Project_Step_One',query:{flag:router_flag}}
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_One')
                    break;
                case "平台":
                    // this.JumpAndSave()
                    this.$router.push('/tagl/Project_Step_Two')
                    break;
                case "知识库":
                    // this.JumpAndSave()
                    var router_flag=this.$route.query.flag
                    var routerValue={path:'/tagl/Project_Step_Three',query:{flag:router_flag}}
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_Three')
                    break;
                case "模块":
                    // this.JumpAndSave()
                    var router_flag=this.$route.query.flag
                    var routerValue={path:'/tagl/Project_Step_Four',query:{flag:router_flag}}
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_Four')
                    break;
                case "模块负责组":
                    // this.JumpAndSave()
                    var router_flag=this.$route.query.flag
                    var routerValue={path:'/tagl/Project_Step_Five',query:{flag:router_flag}}
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_Five')
                    break;
                // case "1输入项目名称":
                //   if(this.active ==0){
                //     this.$router.push('/tagl/step1')
                //   }
                //   break;
                case "2框架":
                    if (this.active > 0) {
                        this.$router.push('/tagl/Project_Step_Two')
                    }
                    break;

            }
        },
        cancel () {
            this.save_data = JSON.stringify(this.file_form)
            if (this.save_data == this.get_data) {
                window.sessionStorage.removeItem('proj_id')
                window.sessionStorage.removeItem('step_id')
                this.$store.state.fpm_id = 1
                this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        window.sessionStorage.removeItem('proj_id')
                        window.sessionStorage.removeItem('step_id')
                        this.$store.state.fpm_id = 1
                        this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
                    })
                    .catch(() => { })
            }
        }
    }
}
</script>
<style scoped>
.add-project-step {
    margin: 0 auto;
    width: 100%;
    height: 100%;
}
.countent {
    max-width: 300px;
    min-width: 200px;
    width: 15%;
    height: 100%;
    padding: 20px;
    float: left;
}
.header-top {
    height: 100px;
}
.header {
    height: 400px;
    padding: 10%;
    clear: both;
}
.mid {
    width: 80%;
    height: 100%;
    float: left;
    padding-top: 40px;
    padding-right: 1%;
    position: relative;
    padding-right: 20px;
    padding-bottom: 55px;
    border-right: 1px solid #ccc;
}
.mid-top {
    position: absolute;
    top: 0;
    bottom: 55px;
    width: 100%;
    padding-right: 20px;
    overflow-y: scroll;
}
.footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}

/**/

#Add-File-Title {
    float: left;
    margin: 0 auto;
    width: 84%;
    height: 100%;
    padding-left: 1%;
    border-left: 1px solid #c0c4cc;
}

.div-center {
    width: 100%;
    text-align: left;
    padding: 0 0 20px;
    margin: 40px 0 20px 0;
}
.div-radio {
    width: 100%;
    text-align: left;
    padding: 0 0 20px;
    margin: 0px 0 -20px 0;
}
.div-center-label {
    margin-left: 10px;
}

.div-title {
    display: inline-block;
    width: 90px;
    text-align: right;
    margin-right: 20px;
    color: #4d4d4d;
    font-weight: bold;
}
.div-title-ex {
    margin: 0;
    padding: 0;
    width: 100%;
    text-align: left;
}
h2 {
    font-size: 22px;
    font-weight: bolder;
    color: white;
    padding-left: 10px;
    line-height: 26px;
    background-color: #6bcca0;
}
.summary {
    vertical-align: top;
    height: 66px;
    line-height: 66px;
}
.div-input {
    display: inline-block;
    width: 500px;
}

.input-btn {
    text-align: right;
    width: 100%;
}
#Add-File-Title .el-input__inner {
    height: 36px;
    line-height: 36px;
}
.checkradio {
    padding-top: 25px;
}

@media screen and (max-width: 1366px) {
    .mid {
        width: 880px;
    }
}
@media screen and (max-width: 1334px) {
    .countent {
        max-width: 300px;
        min-width: 200px;
        width: 15%;
        height: 100%;
        padding: 20px;
        float: left;
    }
    #Add-File-Title {
        float: left;
        width: 80%;
        height: 100%;
    }
}
@media screen and (max-width: 1024px) {
    .add-project-step {
        width: 1024px;
    }
    .header-top {
        display: none;
    }
    .header {
        height: 100%;
        padding: 10%;
        clear: both;
    }
    #Add-File-Title {
        float: left;
        width: 820px;
        height: 100%;
    }
    .mid {
        width: 635px;
    }
    .div-input {
        display: inline-block;
        width: 400px;
    }
}
</style>