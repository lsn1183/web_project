<template>
    <div class="Add-File-Title">
        <div class="Add-File-Title-nav">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="基本设计"  v-if="dbrfmFlag">1</el-step>
                    <el-step class="jump" title="详细设计"  v-else>1</el-step>
                    <el-step class="jump" title="式样书">2</el-step>
                    <el-step class="jump" title="Usecase" icon="el-icon-edit" status="process">3</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Title">
            <div class="mid">
                <div class="mid-top">
                    <div class="div-center-top">
                        <div class="div-title div-title-ex">
                            <h2>
                                <span style="line-height:25px;float:left">Usecase</span>
                                <i class="el-icon-question" style="font-size:15px; line-height:25px;float:left;margin-left:3px" title="请提供所有Usecase以及Usecase的文字说明"></i>
                                <el-button size="mini"  type="text" style='color:#ffffff;margin-left:3px' @click='append_useacase()'> [ 添加 ]</el-button>
                            </h2>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="Asa-title">
                            <span>Usecase共通图</span>
                            <i class="el-icon-question" style="font-size:15px; line-height:25px;" title="所有的Usecase在同一张图中时，请添加共通图"></i>
                        </div>
                        <div class="div-input">
                            <div class="img-box"  v-for='(src,index_img) in append_useacase_list.public_usecase_content[0].fileList'>
                                <img :src="src.url" alt="" @click="show_to_pic(src.url)" class="Sequence_img">
                                <i class="el-icon-close img-icon" style="float:right" @click='delete_img(index,index_img)'></i>
                            </div>
                            <div class="upload-demo-box">
                                <el-upload
                                class="upload-demo"
                                :action='Up_Img_Ip'
                                :on-preview="handle_preview"
                                :on-remove="handleRemove"
                                :on-success='up_success'
                                :before-upload="beforeUpload"
                                :show-file-list='false'>
                                    <button @click='get_index(index)' class="up-data-btn"><i class="el-icon-picture"></i>点击上传</button>
                                </el-upload>
                            </div>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <!-- <div class="Asa-title">
                            Usecase{{index+1}}
                            <el-button size="mini"  type="text" style='color:#000' @click='append_useacase()'> [ 添加 ]</el-button>
                            <el-button size="mini"  type="text" style='marginLeft:5px;color:#000' @click="delete_useacase(index)" v-if="index === 0 ? false : true"> [ 删除 ]</el-button>
                        </div>
                        <div class="div-input">
                            <el-input
                              class='textarea-name'
                              type="textarea"
                              :autosize="{ minRows:2, maxRows:10}"
                              placeholder="请输入usecase的描述说明"
                              v-model='item.content[0].val'>
                            </el-input>
                        </div> -->
                        <el-table class="table" :data="append_useacase_list.usecase_list" border>
                            <el-table-column label="" width="100">
                                <template slot-scope="scope">
                                    UC{{scope.$index+1}}
                                </template>
                            </el-table-column>
                            <el-table-column label="添加名称" width="200">
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.content[0].title" type="textarea" autosize></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="添加描述" >
                                <template slot-scope="scope">
                                    <el-input v-model="scope.row.content[0].val" type="textarea" autosize></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" width="130">
                                <template slot-scope="scope">
                                    <el-button size="mini"  type="text" style='color:#000' @click='append_useacase()'> [ 添加 ]</el-button>
                                    <el-button size="mini"  type="text" style='marginLeft:5px;color:#000' @click="delete_useacase(scope.$index)"> [ 删除 ]</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>

                </div>
                    
                <div class="min-footer">
                    <div class="div-input" style="text-align: right;width:100%">
                        <el-button type="primary" size="mini" @click="prev()"><i class="el-icon-arrow-left"></i>上一步</el-button>
                        <el-button type="primary" size="mini" @click='save_usecase(1)'>&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                        <el-button type="primary" size="mini" @click='cancel()'>&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                        <el-button size="mini" type="primary" @click='save_usecase(2)'>&nbsp;&nbsp;完&nbsp;&nbsp;&nbsp;成&nbsp;&nbsp;</el-button>
                    </div>
                </div>
            </div>
            <div class="footer"></div>
            <div id="img-dialog-box">
                <el-dialog :visible.sync="dialogTableVisible" >
                    <p class="dialog-title">
                        <span><i class="el-icon-circle-plus" @click='big_img()'></i></span>
                        <span>{{show_num}}%</span>
                        <span><i class="el-icon-remove" @click='s_img()'></i></span>
                    </p>
                    <img :src="img_src" alt="" class='dialog-img'>
                </el-dialog>
            </div>

        </div>
    </div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    data() {
        return {
            active: Number(window.sessionStorage.getItem('Step-Asa')),
            append_useacase_list: {
                doc_id: window.sessionStorage.getItem('DocId'),
                commit_user: window.sessionStorage.getItem('Uall'),
                usecase_list: [],
                public_sec_id: null,
                public_usecase_content: [{'fileList': [], 'val': '', 'title' : ''}],
                public_micro_ver: null
            },
            get_data: '',
            save_data: '',
            index: '',
            Up_Img_Ip: this.Ip + '/UploadImage',
            img_num: 0,
            show_num: 100,
            img_src: '',
            dialogTableVisible: false,
            fileList:[],
            dbrfmFlag:false
        }
    },
    mounted() {
        this.get_usecase()
        let self = this
        setTimeout(()=>{
            $('.jump').on('click', function(e) {
                self.jump_to($(this).text())
            })
        },100)
        if (this.$route.query.params) {
            this.dbrfmFlag = this.$route.query.params
        }
    },
    methods: {
        delete_img(index, index_img) {
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.append_useacase_list.public_usecase_content[0].fileList.splice(index_img, 1)
                this.$message({
                    type: 'success',
                    message: '删除成功!'
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
        handleRemove(file, fileList) {
        },
        handle_preview(file) {
            this.dialogTableVisible = true
            this.img_src = file.url
        },
        show_to_pic(data) {
            this.$axios.get(this.Ip + '/ImageSize/' + data).then(res => {
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
                this.append_useacase_list.public_usecase_content[0].fileList.push({
                    name: 'img',
                    url: response.content
                })
            } else {
                this.$alert('图片未上传成功，请重新上传', '提示')
            }
        },
        get_usecase() {
            this.$axios.get(this.Ip + '/ApiDSDocUsecase/' + window.sessionStorage.getItem('DocId')).then(res => {
                if (res.data.result == 'OK') {
                    this.append_useacase_list.public_sec_id = res.data.content.public_sec_id
                    this.append_useacase_list.public_micro_ver = res.data.content.public_micro_ver
                    if (res.data.content.public_usecase_content === null) {
                        this.append_useacase_list.public_usecase_content = [{'fileList': [], 'val': '', 'title' : ''}]
                    } else {
                        res.data.content.public_usecase_content = JSON.parse(res.data.content.public_usecase_content)
                        this.append_useacase_list.public_usecase_content = res.data.content.public_usecase_content
                    }
                    this.append_useacase_list.usecase_list = []
                    if(res.data.content.usecase_list.length != 0 ){
                        for(let i = 0;i<res.data.content.usecase_list.length;i++){
                            let i_content = JSON.parse(res.data.content.usecase_list[i].content)
                            this.append_useacase_list.usecase_list.push({
                                sec_id: res.data.content.usecase_list[i].sec_id,
                                micro_ver: res.data.content.usecase_list[i].micro_ver,
                                content: i_content
                            })
                        }
                    }
                    this.get_data = JSON.stringify(this.append_useacase_list.usecase_list)
                }
            })
        },
        append_useacase() {
            this.append_useacase_list.usecase_list.push({
                sec_id: 0,
                content: [
                    {
                        fileList: [],
                        val: '',
                        title: ''
                    }
                ],
                micro_ver: ''
            })
        },
        delete_useacase(index) {
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                if (this.append_useacase_list.usecase_list[index].sec_id == 0) {
                    this.append_useacase_list.usecase_list.splice(index, 1)
                    this.$message({
                        type: 'success',
                        message: '删除成功!'
                    })
                } else {
                    var commit_user = window.sessionStorage.getItem('Uall')
                    this.$axios
                        .delete(
                            this.Ip +
                                '/DSDoc/' +
                                this.append_useacase_list.usecase_list[index].sec_id +
                                '/usercase/' +
                                commit_user
                        )
                        .then(res => {
                            if (res.data.result == 'OK') {
                                this.append_useacase_list.usecase_list.splice(index, 1)
                                this.$message({
                                    type: 'success',
                                    message: '删除成功!'
                                })
                            } else {
                                this.$message({
                                    message: '删除失败!'
                                })
                            }
                    })
                }
            })
        },
        save_usecase(type) {
            this.$axios.post(this.Ip + '/ApiDSDocUsecase', this.append_useacase_list).then(res => {
                    if (res.data.result == 'OK') {
                        this.get_usecase()
                        this.$message({
                            showClose: true,
                            message: '保存成功',
                            type: 'success'
                        })
                        if (type == 2) {
                            if(this.append_useacase_list.usecase_list.length==0){
                                this.$confirm('您尚未添加Usecase确认离开吗？', '提示', {
                                    confirmButtonText: '确定',
                                    cancelButtonText: '取消',
                                    type: 'warning'
                                })
                                .then(() => {
                                    window.sessionStorage.removeItem('stepTwoSecId')
                                    window.sessionStorage.removeItem('Step-Asa')
                                    this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                                })
                            }else{
                                this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId')) 
                            }
                        }
                    } else {
                        this.$message({
                            showClose: true,
                            message: res.data.error,
                            type: 'error',
                            duration:0,
                        })
                    }
                }).catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration:0,
                    })
                })
        },
        jump_and_save(router) {
            this.save_data = JSON.stringify(this.append_useacase_list.usecase_list)
            var path={path:router,query:{params:this.dbrfmFlag}}
            if (this.save_data == this.get_data) {
                this.$router.push(path)
            } else {
                this.$confirm(this.globalData.hint.jump, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$axios
                        .post(this.Ip + '/ApiDSDocUsecase', this.append_useacase_list)
                        .then(res => {
                            if (res.data.result == 'OK') {
                                this.$message({
                                    showClose: true,
                                    message: '保存成功',
                                    type: 'success'
                                })
                                this.$router.push(router)
                            } else {
                                this.$message({
                                    showClose: true,
                                    message: res.data.error,
                                    type: 'error',
                                    duration:0,
                                })
                            }
                        })
                        .catch(err => {
                            this.$message({
                                showClose: true,
                                message: '服务异常',
                                type: 'error',
                                duration:0,
                            })
                        })
                })
            }
        },
        jump_to(index) {
            switch (index) {
                case '基本设计':
                    this.jump_and_save('/tagl/edit_summery')
                    break
                case '式样书':
                    this.jump_and_save('/tagl/edit_input')
                    break
            }
        },
        prev() {
            // this.$router.push('/tagl/edit_input')
            this.$router.push({path:"/tagl/edit_input",query:{params:this.dbrfmFlag}})
        },
        cancel() {
            if(this.append_useacase_list.usecase_list.length==0){
                this.$confirm('您尚未添加Usecase确认离开吗？', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                .then(() => {
                    window.sessionStorage.removeItem('stepTwoSecId')
                    window.sessionStorage.removeItem('Step-Asa')
                    this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                })
            }else{
                this.save_data = JSON.stringify(this.append_useacase_list.usecase_list)
                if (this.save_data == this.get_data) {
                    window.sessionStorage.removeItem('stepTwoSecId')
                    window.sessionStorage.removeItem('Step-Asa')
                    this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                }else{
                   this.$confirm(this.globalData.hint.quit, '提示', {
                       confirmButtonText: '确定',
                       cancelButtonText: '取消',
                       type: 'warning'
                   })
                   .then(() => {
                       window.sessionStorage.removeItem('stepTwoSecId')
                       window.sessionStorage.removeItem('Step-Asa')
                       this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                   })
                   .catch(() => {}) 
                }
            }
           
        },
        get_index(index) {
            this.index = index
        }
    }
}
</script>

<style scoped>
.upload-demo {
    margin-top: 20px;
}
.upload-demo-box {
    width: 330px;
    height: 350px;
    vertical-align: bottom;
    display: inline-block;
}
.img-icon {
    position: absolute;
    right: 0px;
    top: 0;
    font-size: 24px;
    cursor: pointer;
    /*font-weight: bold;*/
}
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
.div-center-top {
    width: 100%;
    text-align: left;
    margin: 40px 0 0 0;
    padding: 0 0 20px;
}
.div-center {
    width: 100%;
    text-align: left;
    /*margin:40px 0 0 0;*/
    padding: 0 0 20px;
}

.div-center-label:last-child {
    margin: 0;
}
.div-title {
    display: inline-block;
    width: 90px;
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
    font-weight: 600;
    color: white;
    padding-left: 10px;
    line-height: 25px;
    height: 25px;
    background-color: #6bcca0;
}
.summary {
    vertical-align: top;
    height: 66px;
    line-height: 66px;
}
.div-input {
    padding-left: 30px;
    width: 100%;
    padding-top: 10px;
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
    height: 100px;
}
.header {
    height: 225px;
    padding: 10%;
    clear: both;
}

/* Asa-新增样式 */
.Asa-title {
    padding-left: 30px;
    font-size: 18px;
}
.Sequence_img {
    width: 100%;
    height: 100%;
}
.img-box {
    width: 350px;
    height: 330px;
    padding-left: 20px;
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
.up-data-btn {
    width: 330px;
    height: 320px;
    margin-left: 20px;
    display: block;
    background: #fff;
    outline: none;
    border: 1px dashed #ccc;
    color: #ccc;
    font-size: 15px;
    /*display: inline-block;*/
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
    .checked-input-list {
        margin-left: 20px;
        float: left;
        height: 400px;
    }
    .img-box {
        width: 250px;
        height: 250px;
        margin-right: 20px;
        position: relative;
        display: inline-block;
    }
    .up-data-btn {
        width: 230px;
        height: 240px;
        margin-left: 20px;
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
        width: 380px;
    }
    .checked-input-list {
        margin-left: 20px;
        float: left;
        height: 400px;
    }
    .img-box {
        width: 180px;
        height: 170px;
        margin-right: 10px;
        position: relative;
        display: inline-block;
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
}

</style>
