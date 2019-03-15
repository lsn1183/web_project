<template>
    <div class='Append-basic-temlate'>
        <div class="Append-basic-temlate-countent">
            <div class="header-top">
            </div>
            <div class="header">
            </div>
        </div>

        <div class="content-box">
            <div class="middle">
                <div class="middle-top">
                    <div class="sequence-title">
                        <h2 style="fontSize: 22px;fontWeight:bolder;backgroundColor:#6bcca0; color: white;lineHeight: 25px;height:25px">
                            <span style="lineHeight:25px;float:left;paddingLeft: 10px;">Statemachine</span>
                            <i class="el-icon-question" style="fontSize:15px; lineHeight:25px;float:left;marginLeft:5px" title="请提供描述Statemachine图的文字说明以及Statemachine图"></i>
                            <!-- <div style="display:inline-block;" title="如果Usecase中的机能有复杂的状态变化，可以上传状态图。状态图可以省略。">
                    <img src="../../assets/img/wenhao10.svg" alt="" style="width:17px;height:17px;">
                </div> -->
                        </h2>
                    </div>
                    <div class="lable-box">
                        <div v-for='(item,index) in STD.content' style="width:100%;margin:20px 20px;padding-right: 20px;padding-bottom: 50px;" :key="index">

                            <div style="margin:20px auto;font-size: 18px;">
                                Statemachine说明
                                <!-- <el-button size="mini"  type="text" @click='delete_content(index)' style='marginLeft:5px;color:#000'> [ 删除 ]</el-button> -->
                            </div>
                            <el-input class='textarea-name' type="textarea" :autosize="{ minRows: 2, maxRows: 16}" placeholder="请输入Statemachine的描述说明" v-model="item.content[0].val">
                            </el-input>

                            <!-- <div style="margin:20px auto;font-size: 18px;">
                                关联UseCase
                            </div>
                            <div class="squence-usecase">
                                <el-checkbox-group v-model="item.rel_id_list">
                                    <span v-for='(item_usecase, index) in doc_usecase_list' class="check-span" :key="index">
                                        <el-checkbox :label="item_usecase.sec_id">
                                            {{item_usecase.number}}
                                        </el-checkbox>
                                    </span>
                                </el-checkbox-group>
                            </div> -->

                            <p style="color:#333;margin:20px auto;fontSize:18px;">Statemachine图片</p>
                            <div class="img-box" v-for='(src,index_img) in item.content[0].fileList' :key="index_img">
                                <img :src="src.url" alt="" @click="show_to_pic(src.url)" class="Sequence-img">
                                <i class="el-icon-close img_icon" style="float:right" @click='delete_img(index, index_img)'></i>
                            </div>
                            <div class="upload-demo-box">
                                <el-upload class="upload-demo" :action='Up_Img_Ip' :on-preview="handlePreview" :on-success='up_success' :show-file-list='false' :before-upload="beforeUpload">
                                    <button @click='get_index(index)' class="up-data-btn">
                                        <i class="el-icon-picture"></i>点击上传</button>
                                </el-upload>
                            </div>

                            <div class="btn_box">
                                <!-- <el-button size="mini"  type="primary" @click='delete_content(index)' style='float:right'><i class="el-icon-delete"></i> 删除</el-button> -->
                                <!-- <el-button size="mini"  type="primary" @click='append_content(index)' class='append-btn'><i class="el-icon-plus"></i>添加</el-button> -->
                            </div>
                        </div>
                        <!-- <div class="add-box" @click='append_content(index)'>
                  <i class="el-icon-plus"></i>
                  <br>
                  <span>
                    点击添加<br>Statemachine
                  </span>
              </div> -->
                    </div>
                </div>

                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="save()">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="success()">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>

                </div>
            </div>
            <div class="right">
                <!-- <showLeftCheck></showLeftCheck> -->
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
                    <!-- <i class="el-icon-close img_icon" style="float:right" @click='close_img()'></i> -->
                </el-dialog>
            </div>

        </div>
    </div>
</template>

<script>
import showLeftCheck from './step_showLeftCheck'
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    components: {
        showLeftCheck: showLeftCheck
    },
    data() {
        return {
            img_num: 0,
            show_num: 100,
            index: 0,
            append_to_body: true,
            dialogTableVisible: false,
            img_src: '',
            fileList2: [],
            textarea_val: '',
            STD: {
                doc_id: window.sessionStorage.getItem('DocId'),
                micro_ver: Number(window.sessionStorage.getItem('ver')),
                commit_user: window.sessionStorage.getItem('Uall'),
                sec_type: 'STD',
                content: [
                    {
                        sec_id: 0,
                        content: [
                            {
                                fileList: [],
                                val: ''
                            }
                        ],
                        checklist: {},
                        rel_id_list: []
                    }
                ]
            },

            Up_Img_Ip: this.Ip + '/UploadImage',
            get_data: '',
            save_data: '',
            dbrfmFlag: false,
            doc_usecase_list: []
        }
    },
    mounted() {
        var self = this
        if (this.$route.query.params) {
            this.dbrfmFlag = this.$route.query.params
        }
        console.log(window.sessionStorage.getItem('DocId'))
    },
    created() {
        this.get_doc_all_usecase()
        this.reqStdData()
    },
    methods: {
        get_doc_all_usecase() {
            this.$axios
                .get(this.Ip + '/AllUsecase/' + window.sessionStorage.getItem('DocId'))
                .then(res => {
                    this.doc_usecase_list = res.data.content
                    this.sec_id_list = res.data.content.map(item => item.sec_id)
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
        reqStdData() {
            this.$axios
                .get(this.Ip + '/Section/' + window.sessionStorage.getItem('DocId') + '/STD')
                .then(res => {
                    if (res.data.result == 'OK') {
                        for (let i = 0; i < res.data.content.content.length; i++) {
                            res.data.content.content[i].content = JSON.parse(res.data.content.content[i].content)
                        }
                        this.STD.content = res.data.content.content
                        this.STD.micro_ver = res.data.micro_ver
                    } else {
                        this.STD.micro_ver = res.data.micro_ver
                    }
                    this.get_data = JSON.stringify(this.STD)
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
        get_index(index) {
            this.index = index
        },
        handlePreview(file) {
            this.dialogTableVisible = true
            this.img_src = file.url
        },
        cancel() {
            this.save_data = JSON.stringify(this.STD)
            if (this.save_data == this.get_data) {
                this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                    })
                    .catch(() => {})
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
        // 上传图片
        up_success(response, file, fileList) {
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.STD.content[this.index].content[0].fileList.push({
                    name: 'img',
                    url: response.content
                })
            } else {
                this.$alert('图片未上传成功，请重新上传', '提示')
            }
        },
        delete_img(index, index_img) {
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.STD.content[index].content[0].fileList.splice(index_img, 1)
                this.$message({
                    type: 'success',
                    message: '删除成功!'
                })
            })
        },
        // 添加
        append_content() {
            this.STD.content.push({ sec_id: 0, content: [{ fileList: [], val: '' }] })
        },
        delete_content(index) {
            if (index == 0) {
                this.$alert('已是最后一项', '提示')
            } else {
                this.$confirm(this.globalData.hint.delete, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.STD.content.splice(index, 1)
                })
            }
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
        save() {
            this.STD.doc_id = window.sessionStorage.getItem('DocId')
            if (window.sessionStorage.getItem('DocId') == null) {
                this.STD.content[0].sec_id = 0
            } else {
            }
            this.$axios
                .post(this.Ip + '/Section', this.STD)
                .then(res => {
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                        this.reqStdData()
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
                        message: '服务异常',
                        type: 'error',
                        duration: 0
                    })
                })
        },
        success() {
            this.STD.doc_id = window.sessionStorage.getItem('DocId')
            if (window.sessionStorage.getItem('DocId') == null) {
                this.STD.content[0].sec_id = 0
            } else {
            }
            this.$axios
                .post(this.Ip + '/Section', this.STD)
                .then(res => {
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                        this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
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
                        message: '服务异常',
                        type: 'error',
                        duration: 0
                    })
                })
            
        }
    }
}
</script>

<style scoped>
.check-span {
    display: block;
    margin: 5px 0;
    min-width: 20%;
    width: 25%;
    float: left;
}
.squence-usecase {
    border-radius: 4px;
    border: 1px solid #dcdfe6;
    margin: 20px 0;
    overflow-y: scroll;
    overflow-x: hidden;
    padding: 10px;
    max-height: 300px;
}
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
    border-left: 1px solid #c0c4cc;
    height: 100%;
    /*overflow-y: scroll;*/
}
.sequence-title {
    margin: 40px 0 0 0;
}
.upload-demo {
    margin-top: 20px;
}
.title,
.textarea-name {
    display: block;

    padding: 10px 0;
    /*margin: 0 auto;*/
}

.middle {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
    padding-right: 20px;
    border-right: 1px solid #ccc;
}
.middle-top {
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
    overflow-y: scroll;
    overflow-x: hidden;
}
.lable-box {
    overflow: hidden;
}
.add-box {
    /*line-height: 100px;*/
    height: 100px;
    width: 100px;
    padding-top: 20px;
    text-align: center;
    border: 1px dashed #ccc;
    cursor: pointer;
    font-size: 14px;
    /*margin:20px auto;*/
    margin-left: 20px;
}
.add-box:hover {
    /*line-height: 100px;*/
    height: 100px;
    width: 100px;
    padding-top: 20px;
    text-align: center;
    border: 1px dashed #67c23a;
    color: #67c23a;
    cursor: pointer;
}
.title {
    width: 80%;
    margin: 20px 0;
}
.up-data-btn {
    width: 330px;
    height: 320px;
    /*margin-left: 20px;*/
    /*margin-top:20px;*/
    display: block;
    background: #fff;
    outline: none;
    border: 1px dashed #ccc;
    color: #ccc;
    font-size: 15px;
}
.upload-demo-box {
    width: 330px;
    height: 350px;
    vertical-align: bottom;
    display: inline-block;
}
.Sequence-img {
    width: 100%;
    height: 100%;
}
.img-box {
    width: 330px;
    height: 330px;
    /*padding-right: 20px;*/
    margin-right: 20px;
    position: relative;
    display: inline-block;
}
.img-box:hover {
    cursor: pointer;
    border: 1px solid transparent;
    -moz-border-top-colors: red blue white white black;
    -moz-border-right-colors: red blue white white black;
    -moz-border-bottom-colors: red blue white white black;
    -moz-border-left-colors: red blue white white black;
}

.img_icon {
    position: absolute;
    right: 0px;
    top: 0;
    font-size: 24px;
    cursor: pointer;
    /*font-weight: bold;*/
}
.dialog-img {
    display: block;
    margin: 0 auto;
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
        width: 230px;
        height: 240px;
        /*margin-left: 20px;*/
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
        margin-top: 0;
    }
    .img-box {
        width: 250px;
        height: 250px;
        margin-right: 20px;
        position: relative;
        display: inline-block;
    }
    .check-span {
        display: block;
        margin: 5px 0;
        min-width: 20%;
        width: 30%;
        float: left;
    }
}
@media screen and (max-width: 1334px) {
    .Append-basic-temlate-countent {
        max-width: 300px;
        min-width: 200px;
        width: 15%;
        height: 100%;
        padding: 20px;
        float: left;
    }
    .content_box {
        float: left;
        width: 80%;
        height: 100%;
        /*overflow-y: scroll;*/
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
        /*overflow-y: scroll;*/
        /*border: 1px solid red;*/
    }
    .up-data-btn {
        width: 160px;
        height: 170px;
    }
    .upload-demo-box {
        width: 180px;
        height: 180px;
        vertical-align: bottom;
        display: inline-block;
    }
    .upload-demo {
        margin-top: 0;
    }
    .img-box {
        width: 180px;
        height: 170px;
        margin-right: 10px;
        position: relative;
        display: inline-block;
    }
    .check-span {
        display: block;
        margin: 5px 0;
        min-width: 20%;
        width: 50%;
        float: left;
    }
}
</style>
