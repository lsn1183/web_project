<template>
    <div class='Append-basic-temlate'>
        <div class="Append-basic-temlate-countent">
            <div class="header-top">
            </div>
            <div class="header">
            </div>
        </div>
        <div class="content-box">

            <div class="mid">
                <div class="mid-top">
                    <div class="usecase-title">
                        <h2 style="fontSize: 22px;fontWeight:bolder;backgroundColor:#6bcca0; color: white;lineHeight: 25px;height:25px">
                            <span style="lineHeight:25px;float:left;paddingLeft: 10px;">Usecase</span>
                            <i class="el-icon-question" style="fontSize:15px; lineHeight:25px;float:left;marginLeft:5px" title="请提供描述Usecase图的文字说明以及Usecase图"></i>
                            <!-- <div style="display:inline-block;" title="选择Usecase涉及的场景，主要从以下两方面考虑:1.Usecase用到场景中哪些资源.2.Usecase会影响场景中哪些方面">
                    <img src="../../assets/img/wenhao10.svg" alt="" style="width:17px;height:17px;">
                </div> -->
                        </h2>
                    </div>
                    <div class="content-box-deep">
                        <div class="lable-box">
                            <div style="margin-bottom: 10px;fontSize:18px;">
                                Usecase名称
                            </div>
                            <el-input class='textarea-name' placeholder="请输入usecase的名称" v-model="USERCASE.content[0].content[0].title">
                            </el-input>
                            <div style="margin-bottom: 10px;fontSize:18px;">
                                Usecase说明
                            </div>
                            <el-input class='textarea-name' type="textarea" :autosize="{ minRows: 3, maxRows: 16}" placeholder="请输入usecase的描述说明" v-model="USERCASE.content[0].content[0].val">
                            </el-input>
                            <p style="color:#333;margin:20px 0;fontSize:18px;">Usecase图片</p>
                            <div class="img-box" v-for='(src,index) in USERCASE.content[0].content[0].fileList' :key="index">
                                <img :src="src.url" alt="" @click="show_to_pic(src.url)" class="Sequence-img">
                                <i class="el-icon-close img-icon" style="float:right;" @click='delete_img(index)'></i>
                            </div>

                            <div class="upload-demo-box">
                                <el-upload class="upload-demo" :action='Up_Img_Ip' :on-preview="handlePreview" :before-upload="beforeUpload" :on-success='up_success' :show-file-list='false'>
                                    <button class="up-data-btn">
                                        <i class="el-icon-picture"></i>点击上传</button>
                                </el-upload>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="info" disabled>
                        <i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button size="mini" type="primary" @click="save()">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="next_step()">下一步
                        <i class="el-icon-arrow-right"></i>
                    </el-button>
                </div>
            </div>
            <div class="right">

            </div>
            <div id="img-dialog-box">
                <el-dialog :visible.sync="dialogTableVisible">
                    <p class="dialog-title">
                        <span>
                            <i class="el-icon-circle-plus" @click='big_img()'></i>
                        </span>
                        <span>{{show_num}}%</span>
                        <span>
                            <i class="el-icon-remove" @click='s_img()'></i>
                        </span>
                    </p>
                    <img :src="img_src" alt="" class='dialog-img'>
                    <!-- <i class="el-icon-close img-icon" style="float:right" @click='close_img()'></i> -->
                </el-dialog>
            </div>
        </div>
    </div>
</template>

<script>
// import showLeftCheck from './step_showLeftCheck'
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    //  components: {
    // 		"showLeftCheck": showLeftCheck,
    // },
    data() {
        return {
            img_num: 0,
            show_num: 100,
            fileList2: [],
            append_to_body: true,
            dialogTableVisible: false,
            img_src: '',
            dialogTableVisible: false,
            textarea_val: '',
            active: Number(window.sessionStorage.getItem('Step')),
            USERCASE: {
                doc_id: 0,
                parent_sec_id: 0,
                micro_ver: 0,
                commit_user: window.sessionStorage.getItem('Uall'),
                sec_type: 'USERCASE',
                content: [
                    {
                        sec_id: 0,
                        micro_ver: 0,
                        content: [
                            {
                                fileList: [],
                                val: '',
                                title: ''
                            }
                        ],
                        checklist: {}
                    }
                ]
            },
            Up_Img_Ip: this.Ip + '/UploadImage',
            get_data: '',
            save_data: '',
            dbrfmFlag: false
        }
    },
    mounted() {
        this.USERCASE.doc_id = window.sessionStorage.getItem('DocId')
        this.load_up()
        var self = this
        setTimeout(() => {
            $('.jump').on('click', function(e) {
                self.jump_to($(this).text())
            })
        }, 10)
        if (this.$route.query.params) {
            this.dbrfmFlag = this.$route.query.params
        }
    },
    methods: {
        handlePreview(file) {},
        load_up() {
            if (window.sessionStorage.getItem('stepTwoSecId') == null) {
                this.USERCASE.content[0].sec_id = 0
                this.USERCASE.parent_sec_id = 0
            } else {
                this.USERCASE.content[0].sec_id = window.sessionStorage.getItem('stepTwoSecId')
            }
            this.$axios
                .get(this.Ip + '/Section/' + this.USERCASE.content[0].sec_id + '/USERCASE')
                .then(res => {
                    if (res.data.result == 'OK') {
                        let data = JSON.parse(res.data.content.content[0].content)
                        this.USERCASE.content[0].content[0].val = data[0].val
                        this.USERCASE.content[0].content[0].title = data[0].title
                        this.USERCASE.content[0].sec_id = res.data.content.content[0].sec_id
                        this.USERCASE.content[0].content[0].fileList = data[0].fileList
                        this.USERCASE.content[0].micro_ver = res.data.content.content[0].micro_ver
                        this.USERCASE.micro_ver = res.data.micro_ver
                    } else {
                        this.USERCASE.micro_ver = res.data.micro_ver
                    }
                    this.get_data = JSON.stringify(this.USERCASE)
                })
                .catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0
                    })
                })
        },
        cancel() {
            this.save_data = JSON.stringify(this.USERCASE)
            if (this.save_data == this.get_data) {
                window.sessionStorage.removeItem('stepTwoSecId')
                window.sessionStorage.removeItem('Step')
                this.$router.push('/tagl/File_design/Preview/' + this.USERCASE.doc_id)
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        window.sessionStorage.removeItem('stepTwoSecId')
                        window.sessionStorage.removeItem('Step')
                        this.$router.push('/tagl/File_design/Preview/' + this.USERCASE.doc_id)
                    })
                    .catch(() => {})
            }
        },
        jump_to(index) {
            switch (index) {
                // case 'Usecase(必填)':
                //     this.$router.push({path:'/tagl/step1',query:{params:this.dbrfmFlag}})
                //     break
                case '式样书(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
                    break
                case '场景(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step3', query: { params: this.dbrfmFlag } })
                    break
                case '变更变化点(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step4', query: { params: this.dbrfmFlag } })
                    break
                case 'Sequence(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step5', query: { params: this.dbrfmFlag } })
                    break
                case 'Statemachine(选填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step6', query: { params: this.dbrfmFlag } })
                    break
                case 'DRBFM(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step7', query: { params: this.dbrfmFlag } })
                    break
                case '1Usecase(必填)':
                    if (this.active == 0) {
                        this.$router.push('/tagl/step1')
                    }
                    break
                case '2式样书(必填)':
                    if (this.active < 2) {
                        this.next_step()
                        // this.$router.push('/tagl/step2')
                    }
                    break
                case '3场景(必填)':
                    if (this.active == 2) {
                        this.$router.push('/tagl/step3')
                    }
                    break
                case '4Sequence(必填)':
                    if (this.active == 3) {
                        this.$router.push('/tagl/step4')
                    }
                    break
                case '5Statemachine(选填)':
                    if (this.active == 4) {
                        this.$router.push('/tagl/step5')
                    }
                    break
                case '6DRBFM(必填)':
                    if (this.active == 5) {
                        this.$router.push('/tagl/step6')
                    }
                    break
            }
        },
        // 上传图片
        up_success(response, file, fileList) {
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })

                this.USERCASE.content[0].content[0].fileList.push({
                    name: 'img',
                    url: this.Ip + '/DownFile/' + response.content
                })
            } else {
                this.$alert('图片未上传成功，请重新上传', '提示')
            }
        },
        // 点下一步上传当前的东西
        next_step() {
            this.USERCASE.doc_id = window.sessionStorage.getItem('DocId')
            if (window.sessionStorage.getItem('stepTwoSecId') == null) {
                this.USERCASE.content[0].sec_id = 0
                this.USERCASE.parent_sec_id = 0
            } else {
                this.USERCASE.parent_sec_id = 0
            }
            this.$axios.post(this.Ip + '/Section', this.USERCASE).then(res => {
                // console.log(res, '--------------------')
                if (res.data.result == 'OK') {
                    // console.log(res, '001')
                    window.sessionStorage.setItem('stepTwoSecId', res.data.sec_id)
                    window.sessionStorage.setItem('ver', res.data.micro_ver)
                    if (window.sessionStorage.getItem('Step') > '6') {
                        window.sessionStorage.setItem('Step', 7)
                    } else if (window.sessionStorage.getItem('Step') == '0') {
                        window.sessionStorage.setItem('Step', 1)
                    }
                    this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
                } else {
                    this.$message({
                        showClose: true,
                        type: 'error',
                        message: res.data.error,
                        duration: 0
                    })
                }
            })
        },
        save() {
            this.USERCASE.doc_id = window.sessionStorage.getItem('DocId')
            if (window.sessionStorage.getItem('stepTwoSecId') == null) {
                this.USERCASE.content[0].sec_id = 0
                this.USERCASE.parent_sec_id = 0
            } else {
                this.USERCASE.parent_sec_id = 0
            }
            this.$axios
                .post(this.Ip + '/Section', this.USERCASE)
                .then(res => {
                    if (res.data.result == 'OK') {
                        // console.log(res, 'mv')
                        window.sessionStorage.setItem('stepTwoSecId', res.data.sec_id)
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                        this.load_up()
                        this.$message({
                            type: 'success',
                            message: '保存成功!'
                        })
                    } else {
                        this.$message({
                            showClose: true,
                            type: 'error',
                            message: res.data.error,
                            duration: 0
                        })
                    }
                })
                .catch(err => {
                    this.$message({
                        showClose: true,
                        type: 'error',
                        message: '服务异常',
                        duration: 0
                    })
                })
        },
        JumpAndSave() {
            this.USERCASE.doc_id = window.sessionStorage.getItem('DocId')
            if (window.sessionStorage.getItem('stepTwoSecId') == null) {
                this.USERCASE.content[0].sec_id = 0
                this.USERCASE.parent_sec_id = 0
            } else {
                this.USERCASE.parent_sec_id = 0
            }
            this.$axios
                .post(this.Ip + '/Section', this.USERCASE)
                .then(res => {
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('stepTwoSecId', res.data.sec_id)
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                    }
                })
                .catch(err => {
                    this.$message({
                        showClose: true,
                        type: 'error',
                        message: '服务异常',
                        duration: 0
                    })
                })
        },
        big_img() {
            let width_first_img = $('.dialog-img').width() * 0.1
            let mum = this.img_num + 1
            this.show_num = this.show_num + mum * 10
            let img_width = $('.dialog-img').width() + mum * width_first_img
            $('.dialog-img').width(img_width)
        },
        s_img() {
            let mum = this.img_num - 1

            if (this.show_num > 10) {
                let width_first_img = $('.dialog-img').width() * 0.1
                if (mum <= 0) {
                    mum = 1
                    let img_width = $('.dialog-img').width() - mum * width_first_img
                    $('.dialog-img').width(img_width)
                    this.show_num = this.show_num - mum * 10
                } else {
                    let img_width = $('.dialog-img').width() - mum * width_first_img
                    $('.dialog-img').width(img_width)
                    this.show_num = this.show_num + mum * 10
                }
            } else {
                this.$message({
                    message: '图片已缩至最小'
                })
            }
        },
        show_to_pic(data) {
            this.$axios.get(this.Ip + '/ImageSize/' + data).then(res => {
                // console.log(res)
                if (res.data.result == 'OK') {
                    this.dialogTableVisible = true
                    this.img_src = data
                    this.img_num = 0
                    this.show_num = 100
                    let img_width = res.data.content.long
                    $('.dialogimg').width(img_width)
                }
            })
        },
        delete_img(index) {
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.USERCASE.content[0].content[0].fileList.splice(index, 1)
            })
        }
    }
}
</script>

<style scoped>
.Append-basic-temlate {
    margin: 0 auto;
    width: 100%;
    height: 100%;
}
.Append-basic-temlate-countent {
    max-width: 300px;
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

.active {
    background: #fff;
}
.content-box {
    float: left;
    width: 84%;
    padding-left: 1%;
    height: 100%;
    border-left: 1px solid #c0c4cc;
    /*overflow-y: scroll;*/
}
.usecase-title {
    margin: 40px 0 20px 0;
}
.upload-demo {
    width: 340px;
    /*min-width: 500px;*/
    margin: 0 auto;
}
.title {
    display: block;
    /*width: 60%;*/
    padding: 10px 0;
    /*margin: 0 auto;*/
}
.textarea-name {
    display: block;
    width: 90%;
    padding: 10px 0;
    /*margin: 0 auto;*/
}
.lable-box {
    width: 100%;
    padding: 0 0 0 20px;
}
.lable-box {
    overflow: hidden;
}

.dialog-img {
    display: block;
    margin: 0 auto;
    /*width: 100%;*/
}
.up-data-btn {
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
.upload-demo-box {
    /*margin-top: 20px;*/
    width: 330px;
    height: 350px;
    vertical-align: bottom;
    display: inline-block; /*display: inline-block;*/
}
.Sequence-img {
    width: 100%;
    height: 100%;
    /*display: inline-block;*/
}
.img-box {
    width: 330px;
    height: 350px;
    position: relative;
    display: inline-block;
    margin-right: 20px;
}
.img-box:hover {
    cursor: pointer;
    border: 1px solid transparent;
    -moz-border-top-colors: red blue white white black;
    -moz-border-right-colors: red blue white white black;
    -moz-border-bottom-colors: red blue white white black;
    -moz-border-left-colors: red blue white white black;
}
.img-icon {
    position: absolute;
    right: 0px;
    top: 0;
    font-size: 24px;
    cursor: pointer;
    /*font-weight: bold;*/
}

.mid {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
    padding-right: 20px;
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
.right {
    width: 20%;
    height: 100%;
    float: left;
}
.dialog-title span {
    font-size: 20px;
    margin-right: 20px;
    cursor: pointer;
    color: #42b983;
}
.dialog-title {
    height: 30px;
    line-height: 30px;
    width: 170px;
    margin: 0 auto;
}
@media screen and (max-width: 1366px) {
    .up-data-btn {
        width: 250px;
        height: 240px;
        margin-right: 20px;
        display: block;
        background: #fff;
        outline: none;
        border: 1px dashed #ccc;
        color: #ccc;
        font-size: 15px;
    }
    .upload-demo-box {
        width: 250px;
        height: 250px;
        vertical-align: bottom;
        display: inline-block;
    }
    .upload-demo {
        width: 250px;
        /*min-width: 500px;*/
        margin-top: 0;
    }
    .img-box {
        width: 250px;
        height: 250px;
        margin-right: 20px;
        position: relative;
        display: inline-block;
    }
}
@media screen and (max-width: 1334px) {
    .Append-basic-temlate_countent {
        max-width: 300px;
        min-width: 200px;
        width: 15%;
        height: 100%;
        padding: 20px;
        float: left;
    }
    .content-box {
        float: left;
        width: 80%;
        height: 100%;
        overflow-y: scroll;
        /*border: 1px solid red;*/
    }
}
@media screen and (max-width: 1024px) {
    .Append-basic-temlate {
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
    .content-box {
        float: left;
        width: 820px;
        height: 100%;
        overflow-y: scroll;
        /*border: 1px solid red;*/
    }
    .up-data-btn {
        width: 180px;
        height: 170px;
    }
    .upload-demo {
        width: 180px;
        /*min-width: 500px;*/
        margin-top: 0;
    }
    .upload-demo-box {
        width: 180px;
        height: 180px;
        vertical-align: bottom;
        display: inline-block;
    }
    .img-box {
        width: 180px;
        height: 180px;
        margin-right: 10px;
        position: relative;
        display: inline-block;
    }
}
</style>
