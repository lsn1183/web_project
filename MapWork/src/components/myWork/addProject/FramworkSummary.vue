<template>
    <div class="Add-File-Title">
        <div class="Add-File-Title-nav">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="平台信息" icon="el-icon-edit" status="process">1</el-step>
                    <el-step class="jump" title="模块">2</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Title">
            <div class="mid">
                <div class="mid-top">
                    <div class="div-centers">
                        <div class="div-title div-title-ex">
                            <h2>平台信息
                                <i class="el-icon-question" title="请提供该平台的详细信息以及平台框架图" style="font-size:15px;height:20px;vertical-align:middle"></i>
                            </h2>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">标题:</div>

                        <div class="div-input" v-if="fw_title_flag">
                            <!-- <el-input  v-model="file_form.proj_name"></el-input> -->
                            <el-select v-model="fw_model" placeholder="请选择" clearable @visible-change="reqFwOptions" @clear="clearClick" @change="optionChangeValue()">
                                <el-option v-for="item in fw_options" :key="item.fw_id" :label="item.fw_name" :value="item.fw_id">
                                </el-option>
                            </el-select>
                        </div>
                        <div class="div-input" v-else>
                            <el-input v-model="file_form.fw_name"></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title summary">概述:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.summary" type="textarea" :autosize="{ minRows: 3, maxRows:6}"></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label" style="marginLeft:10px;overflow:hidden">
                        <div class="div-title" style="float:left;marginRight:25px">框架图:</div>
                        <div class="div-input" style="float:left">
                            <div class="upload-demo-box" v-if='img_flag'>
                                <el-upload class="upload-demo" :action='Up_Img_Ip' :on-success='up_success' :show-file-list='false'>
                                    <button class="up-data-btn">
                                        <i class="el-icon-picture"></i>点击上传</button>
                                </el-upload>
                            </div>
                            <div class="upload-demo-box" v-if='!img_flag'>
                                <i class="el-icon-close img_icon" @click='delete_img()'></i>
                                <img :src="file_form.content" alt="" class="img-name" @click="img_dialog_fun(file_form.content)">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="min-footer">
                    <div class="div-input" style="text-align: right;width:100%">
                        <el-button size="mini" type="info" disabled>
                            <i class="el-icon-arrow-left"></i>上一步</el-button>
                        <el-button @click="save()" type="primary" size="mini">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                        <el-button @click="cancle()" type="primary" size="mini">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                        <el-button size="mini" type="primary" @click="next">下一步
                            <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>
                </div>
            </div>
            <div class="footer"></div>
            <!-- 点击打开原图 -->
            <div id="img_dialog_box">
                <el-dialog :visible.sync="dialogimgflag">
                    <p class="dialog-title">
                        <span>
                            <i class="el-icon-circle-plus" @click='big_img()'></i>
                        </span>
                        <span>{{show_num}}%</span>
                        <span>
                            <i class="el-icon-remove" @click='s_img()'></i>
                        </span>
                    </p>
                    <img :src="img_src" alt="原图" class="dialogimg">
                </el-dialog>
            </div>
        </div>
    </div>
</template>

<script>
require('../../../assets/js/jquery-1.8.3.min.js')
export default {
    data () {
        return {
            file_form: {
                fw_id: '',
                fw_name: '',
                summary: '',
                content: '',
                manager: window.sessionStorage.getItem("Uall")
            },
            doc_id: null,
            summary: '',
            active: Number(window.sessionStorage.getItem('fw_step_id')),
            Up_Img_Ip: this.Ip + '/UploadImage',
            img_flag: true,
            show_num: 100,
            img_num: 0,
            dialogimgflag: false,
            img_src: "",
            Data: '',
            saveData: '',
            get_data: '',
            save_data: '',
            fw_model: "",
            fw_title_flag: true,
            fw_options: []
        }
    },
    mounted () {
        var self = this
        $('.jump').on('click', function (e) {
            self.jump_to($(this).text())
        });
        if (this.$route.query.flag == "false") {//编辑项目
            this.fw_title_flag = false
            this.getData()
        } else {
            // nothing to do
            this.get_data = JSON.stringify(this.file_form)
        }
    },
    methods: {
        clearClick () {

        },
        reqFwOptions () {
            let datas = { "accessToken": window.sessionStorage.getItem("accessToken"), "manager": window.sessionStorage.getItem("Uall") }
            if (this.fw_model === "") {
                this.$axios.post(this.Ip + "/GetCactusFw", datas).then(res => {
                    // console.log(res)
                    if (res.data.result == 'OK') {
                        this.fw_options = res.data.content
                        // this.file_form.proj_id = res.data.content[0].proj_id
                        // this.file_form.manager = res.data.content[0].proj_manager
                    } else {
                        this.$message({
                            showClose: true,
                            message: '您无平台可添加',
                            type: 'warning',
                            // duration: 15,
                        })
                    }
                })
            } else {
                return
            }
        },
        optionChangeValue () {
            // 选择平台时候，赋值数据
            if (this.fw_model !== "") {
                for (const item of this.fw_options) {
                    if (item.fw_id == this.fw_model) {
                        this.file_form.fw_id = item.fw_id
                        this.file_form.fw_name = item.fw_name
                        this.file_form.manager = item.manager
                    }
                }
            }
        },
        getData () {
            let fw_id = window.sessionStorage.getItem('fw_id')
            if (fw_id != null) {
                this.$axios.get(this.Ip + '/Framework/FW/' + fw_id).then(res => {
                    if (res.data.result == 'OK') {
                        console.log(this.file_form, "Res")
                        this.file_form = res.data.content[0]
                        this.Data = JSON.stringify(this.file_form)
                        if (this.file_form.content == null || this.file_form.content == "") {
                            this.img_flag = true
                        } else {
                            this.img_flag = false
                        }
                        this.get_data = JSON.stringify(this.file_form)
                    }
                })
            }
        },
        save () {
            if (this.file_form.fw_name == "") {
                this.$message({
                    type: 'error',
                    message: '标题信息不可为空！'
                })
            } else {
                this.file_form.type = 'FW'
                // console.log(this.file_form, "111")
                // return
                this.$axios.post(this.Ip + '/Framework', this.file_form).then(res => {
                    // console.log(res)
                    if (res.data.result == "OK") {
                        window.sessionStorage.setItem('fw_id', res.data.content)
                        this.getData()
                        this.$message({
                            type: 'success',
                            message: '保存成功!'
                        })
                        this.getData()
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败',
                            type: 'error',
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
            }
            // this.file_form.editor = window.sessionStorage.getItem('Uall')
        },
        cancle () {
            this.save_data = JSON.stringify(this.file_form)
            if (this.save_data == this.get_data) {
                window.sessionStorage.removeItem('fw_id')
                window.sessionStorage.removeItem('fw_step_id')
                this.$store.state.fpm_id = 0
                this.$router.push('/tagl/Add_NewProject/FramworkTemplate')
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    window.sessionStorage.removeItem('fw_id')
                    window.sessionStorage.removeItem('fw_step_id')
                    this.$store.state.fpm_id = 0
                    this.$router.push('/tagl/Add_NewProject/FramworkTemplate')
                }).catch(() => { })
            }
        },
        next () {
            this.file_form.type = 'FW'
            this.$axios.post(this.Ip + '/Framework', this.file_form).then(res => {
                // console.log(res)
                if (res.data.result == "OK") {
                    window.sessionStorage.setItem('fw_id', res.data.content)
                    if (Number(window.sessionStorage.getItem('fw_step_id')) == 0) {
                        window.sessionStorage.setItem('fw_step_id', 1)
                    }
                    let routerPath={path:'/tagl/Framwork_Model',query:{flag:"false"}}
                    this.$router.push(routerPath)
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
        up_success (response, file, fileList) {
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.img_flag = false
                this.file_form.content = ''
                this.file_form.content = this.Ip + '/DownFile/' + response.content
            } else {
                this.$alert('图片未上传成功，请重新上传', '提示')
            }
        },
        delete_img () {
            this.$confirm('确定删除该图片吗?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(() => {
                    this.file_form.content = ''
                    this.img_flag = true
                })
                .catch(() => { })

        },
        img_dialog_fun (data) {
            this.$axios.get(this.Ip + "/ImageSize/" + data).then(res => {
                if (res.data.result == "OK") {
                    this.dialogimgflag = true;
                    this.img_src = data
                    this.img_num = 0
                    this.show_num = 100
                    let img_width = res.data.content.long
                    $('.dialogimg').width(img_width)

                }
            })
        },
        big_img () {
            let width_first_img = $('.dialogimg').width() * 0.1
            let mum = this.img_num + 1
            this.show_num = this.show_num + mum * 10
            let img_width = $('.dialogimg').width() + mum * width_first_img
            $('.dialogimg').width(img_width)
        },
        JumpAndSave (router) {
            this.save_data = JSON.stringify(this.file_form)
            if (this.save_data == this.Data) {
                this.$router.push(router)
            } else {
                this.$confirm('页面信息已发生变更, 是否跳转?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.file_form.type = 'FW'
                    this.$axios.post(this.Ip + '/Framework', this.file_form).then(res => {
                        // console.log(res)
                        if (res.data.result == "OK") {
                            window.sessionStorage.setItem('fw_id', res.data.content)
                            this.$router.push(router)
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
                })
            }
        },
        jump_to (index) {
            switch (index) {
                case "平台信息":
                    this.JumpAndSave('/tagl/FramworkSummary')
                    // this.$router.push('/tagl/FramworkSummary')
                    break;
                case "模块":
                    this.JumpAndSave('/tagl/Framwork_Model')
                    // this.$router.push('/tagl/Framwork_Model')
                    break;
                case "2模块":
                    if (window.sessionStorage.getItem('fw_step_id') == 1) {
                        this.JumpAndSave('/tagl/Framwork_Model')
                        // this.$router.push('/tagl/Framwork_Model')
                    }
                    break;
            }
        },
        s_img () {
            let mum = this.img_num - 1

            if (this.show_num > 10) {
                let width_first_img = $('.dialogimg').width() * 0.1
                if (mum <= 0) {
                    mum = 1
                    let img_width = $('.dialogimg').width() - mum * width_first_img
                    $('.dialogimg').width(img_width)
                    this.show_num = this.show_num - mum * 10
                } else {
                    let img_width = $('.dialogimg').width() - mum * width_first_img
                    $('.dialogimg').width(img_width)
                    this.show_num = this.show_num + mum * 10
                }
            } else {
                this.$message({
                    message: '图片已缩至最小'
                })
            }

        }
    }
}
</script>

<style scoped>
.Add-File-Title {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}
.Add-File-Title-nav {
    max-width: 300px;
    min-width: 200px;
    width: 15%;
    height: 100%;
    padding: 20px;
    float: left;
    border-right: 1px solid #c0c4cc;
}
.mid {
    width: 80%;
    height: 100%;
    float: left;
    padding-top: 40px;
    border-right: 1px solid #c0c4cc;
    padding-right: 1%;
    /*overflow-y: scroll;*/
    position: relative;
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
    width: 20%;
    height: 100%;
}
#Add-File-Title {
    float: left;
    margin: 0 auto;
    width: 84%;
    height: 100%;
    padding-left: 1%;
}

.div-centers {
    width: 100%;
    text-align: left;
    margin: 40px 0 0 0;
    padding: 0 0 20px;
}
.div-center {
    width: 100%;
    text-align: left;
    padding: 0 0 20px;
}
.div-center-label {
    margin-left: 10px;
}
.div-center-label:last-child {
    margin: 0;
}
.div-title {
    display: inline-block;
    width: 90px;
    text-align: right;
    margin-right: 20px;
    color: #4d4d4d;
    font-weight: bold;
    font-size: 15px;
}
.div-title-ex {
    margin: 0;
    padding: 0;
    width: 100%;
    text-align: left;
}
h2 {
    font-size: 22px;
    font-weight: 600;
    color: white;
    padding-left: 10px;
    background-color: #6bcca0;
    height: 25px;
    line-height: 25px;
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
.min-footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}
.input-btn {
    text-align: right;
    width: 100%;
}
#Add-File-Title .el-input__inner {
    height: 36px;
    line-height: 36px;
}
.header-top {
    height: 200px;
}
.header {
    height: 225px;
    padding: 10%;
    clear: both;
}
.upload-demo-box {
    /*margin-top: 20px;*/
    position: relative;
    width: 330px;
    height: 350px;
    vertical-align: bottom;
    display: inline-block; /*display: inline-block;*/
}
.upload-demo {
    width: 330px;
    height: 350px;
}
.up-data-btn {
    cursor: pointer;
    width: 330px;
    height: 340px;
    /*margin-left: 20px;*/
    display: block;
    background: #fff;
    outline: none;
    border: 1px dashed #ccc;
    color: #ccc;
    font-size: 15px;
}
.img-name {
    display: block;
    width: 100%;
    height: 100%;
    border: 1px solid #ccc;
}
.img_icon {
    position: absolute;
    right: 3px;
    font-size: 24px;
    cursor: pointer;
}
.dialog-title span {
    font-size: 20px;
    margin-right: 20px;
    cursor: pointer;
    color: #42b983;
}
.dialogimg {
    display: block;
    margin: 0 auto;
}
.dialog-title {
    height: 30px;
    line-height: 30px;
    width: 170px;
    margin: 0 auto;
}
@media screen and (max-width: 1366px) {
    .mid {
        width: 880px;
    }
    .right {
        width: 20%;
        height: 100%;
        float: left;
    }
    .checked_input_list {
        margin-left: 20px;
        float: left;
        height: 400px;
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
    .Add-File-Title {
        width: 1024px;
    }
    .header-top {
        height: 100px;
    }
    .header {
        height: 225px;
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
        width: 380px;
    }
    .checked_input_list {
        margin-left: 20px;
        float: left;
        height: 400px;
    }
}
</style>
