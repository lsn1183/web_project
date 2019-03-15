<template>
    <div class="wrapper">
        <div class="tree-box">
            <ul class="tree-ul">
                <li v-for="(node,index) in treeArr" class="tree-li">
                    <p @click="firstScrollTop(index)" class="first-title">
                        <i class="el-icon-caret-right"></i> {{node.node_name}}
                    </p>
                    <ul class="child_ul">
                        <li class="child-tree-li" v-for="(child_node, child_index) in node.child_node">
                            <p @click="secondScrillTop(index, child_index)" class="second-title">
                                {{child_node.node_name}}
                            </p>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
        <div class="content-box">
            <h1 class="title_h1">{{content_box_data.title_name}}</h1>
            <p class="title-detail">
                <span>{{content_box_data.title_detail}}</span>
            </p>

            <!-- Block -->
            <div class="Usecase-box Asa-box">
                <h3 class="title-h3">
                    <span>{{content_box_data.title_content_name}}</span>
                    <span class="append-span" style="margin-left: 20px;" @click="add()">[ 添加 ]</span>
                </h3>
                <!-- Block 子元素块 -->
                <div class="msg-box" v-for="(item, index) in block_data.section_list">
                    <h4 class="title-h4">
                        <span>{{content_box_data.title_content_name}}{{ index + 1 }}</span>
                        <div style="display: inline-block; margin-left: 20px; width: 300px;height: 24px;">
                            <el-input :placeholder="placeholder_value" size="mini" clearable v-model="item.sec_title"></el-input>
                        </div>
                        <span class="append-span" @click="delBlock(index)">&nbsp;[ 删除 ]</span>
                    </h4>
                    <div class="content-size">
                        <span>{{content_box_data.title_content_name}}说明 : </span>
                        <div class="editor">
                            <mavon-editor v-model="item.explain" :editable='true' :subfield='true' defaultOpen='edit' :toolbarsFlag='true' :scrollStyle='true' :toolbars="toolbars"></mavon-editor>
                        </div>
                    </div>
                    <div class="content-size">
                        <span>{{content_box_data.title_content_name}}图 : </span>
                        <div class="editor">
                            <div class="img-box-ex" v-for='(image_item, index_img) in item.content' :key="index_img">
                                <img :src="image_item.url" alt="" @click="showImgDialog(image_item.url)" class="Sequence-img">
                                <i class="el-icon-close img_icon" style="float:right" @click='deleteImg(item.content, index_img)'></i>
                            </div>
                            <div class="upload-demo-box">
                                <el-upload class="upload-demo" :action='upImagIp' :on-preview="handlePreview" :before-upload="beforeUpload" :on-success='up_success' :show-file-list='false'>
                                    <button @click='get_index(index)' class="up-data-btn">
                                        <i class="el-icon-picture"></i>点击上传</button>
                                </el-upload>
                            </div>
                        </div>
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div class="editor">
                            <mavon-editor v-model="item.complement" :editable='true' :subfield='true' defaultOpen='edit' :toolbarsFlag='true' :scrollStyle='true' :toolbars="toolbars"></mavon-editor>
                        </div>
                    </div>
                </div>
            </div>
 
        </div>
        <div id="img-dialog-box">
            <el-dialog :visible.sync="dialogTableVisible">
                <p class="dialog-title">
                    <span>
                        <i class="el-icon-circle-plus" @click='enlargeImg()'></i>
                    </span>
                    <span>{{show_num}}%</span>
                    <span>
                        <i class="el-icon-remove" @click='shrinkImg()'></i>
                    </span>
                </p>
                <img :src="imgSrc" alt="" class='dialog-img'>
            </el-dialog>
        </div>
        <div class="footer">
            <el-button size="mini" type="primary" @click="confirm()">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
            <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
        </div>
    </div>
</template>
<script>
  require('../../assets/js/jquery-1.8.3.min.js')
export default {
  data() {
    return {
        toolbars: {
            bold: true, // 粗体
            italic: true, // 斜体
            header: true, // 标题
            underline: true, // 下划线
            mark: true, // 标记
            superscript: true, // 上角标
            quote: true, // 引用
            ol: true, // 有序列表
            table: true,
            ishljs: true,
            code: true, // code
            subfield: true, // 是否需要分栏
            fullscreen: true, // 全屏编辑
            undo: true, // 上一步
            trash: true // 清空
        },
        content_box_data:{
            title_name:'IF式样或基本设计(模块名称)',
            title_detail:'',
            title_content_name:'Block',
        },
        title:"IF式样或基本设计(模块名称)",
        title_detail:'',
        upImagIp: this.Ip + '/UploadImage',
        block_data:{
            doc_id: 0,
            sec_type: 'BLOCK',
            commit_user: window.sessionStorage.getItem('Uall'),
            section_list: [
                {
                    sec_id: 0,
                    sec_title: '',
                    content: [],
                    explain: '',
                    complement: '',
                    micro_ver: 0
                }
            ]
        },
        section_list_index:0,
        doc_id:0,
        dialogTableVisible: false,
        imgSrc: '',
        show_num: 100,
        treeArr: [
            {
                node_name: 'Usecase',
                child_node: []
            },
            
        ],
        placeholder_value:''

    }    
  },
  mounted() {
      this.mounted_fun()
  },
  methods: {
        mounted_fun(){
            let data = JSON.parse(this.$route.query.data)
            // console.log(data,'路由传参')
            this.doc_id = Number(data.doc_id)
            this.content_box_data.title_name = data.title
            this.content_box_data.title_content_name = data.click_type.substring(0,1).toUpperCase()+data.click_type.substring(1)
            this.placeholder_value = '请输入' + this.content_box_data.title_content_name + '名称'
            if (data.click_type == 'statemachine') {
                this.block_data.sec_type = 'STD'
            }else{
                this.block_data.sec_type = data.click_type.toUpperCase()
            }
            if (data.type == 'add') {//添加模式
                this.treeArr =[
                    {
                        node_name: this.content_box_data.title_content_name,
                        child_node: []
                    },
                ]
            }else if(data.type == 'edit'){
                this.treeArr =[
                    {
                        node_name: this.content_box_data.title_content_name,
                        child_node: []
                    },
                ]
                if (data.doc_id) {//需要传doc_id的
                    this.get_edit_data_fun(data.doc_id)
                }else{//sec_id
                    this.get_edit_data_sec_fun(data.sec_id)
                    
                }
            }

        },
        get_edit_data_sec_fun(sec_id){
            this.$axios.get(this.Ip + '/DsUcSub/' + sec_id + "/"  + this.block_data.sec_type).then(res=>{
                // console.log(res.data,'res-data')
                let index = 0
                for (let item of res.data.content.section_list) {
                    // console.log(item,'-====')
                    item.content = JSON.parse(item.content)//解构图片list
                    index++
                    this.treeArr[0].child_node.push({//左边锚点树结构
                        'node_name': this.content_box_data.title_content_name + index
                    })
                }
                this.block_data = res.data.content
            }).catch(err=>{

            })
        },
        get_edit_data_fun(doc_id){
            // console.log(this.block_data.sec_type,'this.block_data.sec_type')
            this.$axios.get(this.Ip + '/NewDsSection/' + doc_id + "/"  + this.block_data.sec_type).then(res=>{
                // console.log(res.data,'res-data')
                let index = 0
                for (let item of res.data.content.section_list) {
                    // console.log(item,'-====')
                    item.content = JSON.parse(item.content)//解构图片list
                    index++
                    this.treeArr[0].child_node.push({//左边锚点树结构
                        'node_name': this.content_box_data.title_content_name + index
                    })
                }
                this.block_data = res.data.content
                // console.log(this.block_data,'----------')
            }).catch(err=>{

            })
        },
        up_success(response, file, fileList){
            if(response.result == 'OK'){
                this.$message({
                type: 'success',
                message: '上传成功!'
                })
                this.block_data.section_list[this.section_list_index].content.push({
                    name: 'img',
                    url: response.content
                })
                // console.log(this.block_data.section_list)
                
            }else{
                this.$alert('图片未上传成功，请重新上传','提示')
            } 
        },
        get_index(index) {
            this.section_list_index = index
        },
        cancel() {
            let data = JSON.parse(this.$route.query.data)
            if (data.doc_type == 'IF_stylebook') {
                this.$router.push({
                    path: '/tagl/Edit_IF/' + this.doc_id + '/' + window.sessionStorage.getItem('docType')
                })
            } else {
                if (data.doc_id) {
                    this.$router.push({
                        path: '/tagl/File_design/Preview/' + this.doc_id + '/' + window.sessionStorage.getItem('docType')
                    })
                }else{//sec_id
                    this.block_data.sec_id = data.sec_id
                    this.$router.push({
                        path: '/tagl/File_design/Preview_seq/' + this.block_data.sec_id
                    })
                }
            }
        },
        confirm() {
            this.block_data.doc_id = this.doc_id
            this.block_data.commit_user=window.sessionStorage.getItem('Uall')
            const data = this.block_data
            let router_data = JSON.parse(this.$route.query.data)
            let datas = {
                "proj_id": router_data.proj_id,
                "model_id": router_data.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            // console.log(router_data,'点击确认按钮======router_data')
            // console.log(data,'点击确认按钮======data')
            if (router_data.type == 'add') {
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                            // console.log(res.data)
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                            if (data.doc_id) {
                                this.post_NewDsSection_fun(data)
                            }else{
                                data.sec_id = router_data.sec_id
                                this.post_DsUcSub_fun(data)
                            }
                        } else {
                            this.$message({
                                type: "warning",
                                message: "您没有权限操作"
                            })
                        }
                    } else {
                        // nothing to do
                        this.$message({
                            type: "warning",
                            message: res.data.error
                        })
                    }
                })
                
            } else {
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_编辑') == true) {
                            if (data.doc_id) {
                                this.post_NewDsSection_fun(data)
                            } else {
                                data.sec_id = router_data.sec_id
                                this.post_DsUcSub_fun(data)
                            }
                        } else {
                            this.$message({
                                type: "warning",
                                message: "您没有权限操作"
                            })
                        }
                    } else {
                        // nothing to do
                        this.$message({
                            type: "warning",
                            message: res.data.error
                        })
                    }
                })
            }
        },
        post_NewDsSection_fun(data){
            this.$axios.post(this.Ip + '/NewDsSection', data).then(res => {
                if(res.data.result == 'OK') {
                    // 成功，跳转页面
                    this.$message({
                        showClose: true,
                        message: '添加成功',
                        type: 'success',
                        duration: 0
                    })
                    this.$router.push({
                            path:
                                '/tagl/File_design/Preview/' +
                                this.doc_id +
                                '/' +
                                window.sessionStorage.getItem('docType')
                        })
                } else {
                    // 异常报错
                    this.$message({
                        showClose: true,
                        message: res.data.result,
                        type: 'error',
                        duration: 0
                    })
                }
            }).catch(err => {
                this.$message({
                    showClose: true,
                    message: '服务异常',
                    type: 'error',
                    duration: 0
                })
            })
        },
        post_DsUcSub_fun(data){
            // console.log(data,'上传了')
            this.$axios.post(this.Ip + '/DsUcSub', data).then(res => {
                if(res.data.result == 'OK') {
                    // 成功，跳转页面
                    this.$message({
                        showClose: true,
                        message: '添加成功',
                        type: 'success',
                        duration: 0
                    })
                    this.$router.push({
                            path:
                                '/tagl/File_design/Preview_seq' +
                                this.block_data.usecase_id
                        })
                } else {
                    // 异常报错
                    this.$message({
                        showClose: true,
                        message: res.data.result,
                        type: 'error',
                        duration: 0
                    })
                }
            }).catch(err => {
                this.$message({
                    showClose: true,
                    message: '服务异常',
                    type: 'error',
                    duration: 0
                })
            })
        },
        add(){
            // console.log(this.block_data.section_list)
            let new_block_data = {
                complement: "",
                content: [],
                explain: "",
                micro_ver: 0,
                sec_id: 0,
                sec_title: ""
            }
            let router_data = JSON.parse(this.$route.query.data)
            let datas = {
                "proj_id": router_data.proj_id,
                "model_id": router_data.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                        // to do
                        this.block_data.section_list.push(new_block_data)
                        let index = this.block_data.section_list.length 
                        this.treeArr[0].child_node.push({//左边锚点树结构
                            'node_name': this.content_box_data.title_content_name + index
                        })

                    } else {
                        this.$message({
                            type: "warning",
                            message: "您没有权限操作"
                        })
                    }
                } else {
                    // nothing to do
                    this.$message({
                        type: "warning",
                        message: res.data.error
                    })
                }
            })
            
        },
        delBlock(index){
            // console.log(index)
            let router_data = JSON.parse(this.$route.query.data)
            let datas = {
                "proj_id": router_data.proj_id,
                "model_id": router_data.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_删除') == true) {
                        // to do
                        if (index ==0) {
                            this.$message({
                                type:"warning",
                                message:"已是最后一个！"
                            })
                            return
                        }
                        this.block_data.section_list.splice(index,1)

                    } else {
                        this.$message({
                            type: "warning",
                            message: "您没有权限操作"
                        })
                    }
                } else {
                    // nothing to do
                    this.$message({
                        type: "warning",
                        message: res.data.error
                    })
                }
            })
        },
        showImgDialog(data) {
            this.$axios.get(this.Ip + '/ImageSize/' + data).then(res => {
                if (res.data.result == 'OK') {
                    this.dialogTableVisible = true
                    this.imgSrc = data
                    this.img_num = 0
                    this.show_num = 100
                    let img_width = res.data.content.long
                    $('.dialogimg').width(img_width)
                }
            })
        },
        handlePreview(file) {
            this.dialogTableVisible = true
            this.imgSrc = file.url
        },
        enlargeImg() {
            let width_first_img = $('.dialog-img').width() * 0.1
            let mum = this.img_num + 1
            this.show_num = this.show_num + mum * 10
            let img_width = $('.dialog-img').width() + mum * width_first_img
            $('.dialog-img').width(img_width)
        },
        shrinkImg() {
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
        deleteImg(img_list, img_index) {
            let router_data = JSON.parse(this.$route.query.data)
            let datas = {
                "proj_id": router_data.proj_id,
                "model_id": router_data.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_删除') == true) {
                        // to do
                        this.$confirm(this.globalData.hint.delete, '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(() => {
                            img_list.splice(img_index, 1)
                        })

                    } else {
                        this.$message({
                            type: "warning",
                            message: "您没有权限操作"
                        })
                    }
                } else {
                    // nothing to do
                    this.$message({
                        type: "warning",
                        message: res.data.error
                    })
                }
            })
            
        },
        firstScrollTop(index) {
            $('.first-title').css({ color: '#606266' })
            $('.second-title').css({ color: '#606266' })
            $('.first-title')
                .eq(index)
                .css({ color: '#42b983' })
            let sTop = document.getElementsByClassName('Asa-box')[index].offsetTop
            $('.content-box').animate({ scrollTop: sTop }, 500, function() {})
        },
        secondScrillTop(index, second) {
            $('.first-title').css({ color: '#606266' })
            $('.second-title').css({ color: '#606266' })
            $('.tree-li')
                .eq(index)
                .find('.second-title')
                .eq(second)
                .css({ color: '#42b983' })
            let sTop = $('.Asa-box')
                .eq(index)
                .find('.msg-box')
                .eq(second)[0].offsetTop
            $('.content-box').animate({ scrollTop: sTop }, 500, function() {})
        },    
  }
}
</script>

<style scoped>
html,
body {
    font-family: '微软雅黑';
}
.wrapper {
    width: 100%;
    height: 100%;
    min-width: 1024px;
    color: #606266;
    overflow: hidden;
}
.tree-box {
    position: relative;
    top: 1px;
    left: 0;
    z-index: 999;
    margin: 0;
    padding: 0;
    width: 15%;
    height: 98%;
    background-color: white;
    border-right: 2px solid rgba(216, 231, 223, 0.5);
    overflow-y: auto;
    padding-left: 20px;
}
.content-box {
    position: absolute;
    top: 0;
    right: 0;
    left: 15%;
    bottom: 80px;
    width: 85%;
    overflow-y: auto;
    padding-left: 20px;
    padding-bottom: 20px;
}
.title_h1 {
    font-weight: bold;
    font-size: 24px;
    margin-top: 10px;
}
.title-detail {
    font-size: 12px;
    color: #5e6d82;
    text-align: left;
    height: 20px;
    line-height: 20px;
    margin-top: 10px;
}
.block-box,
.Class-box,
.Usecase-table,
.Usecase-box,
.Std-box,
.IF-box {
    margin-top: 10px;
}
.IF-box {
    margin-bottom: 40px;
}
.title-h3 {
    font-size: 22px;
    font-weight: 500;
    height: 25px;
    line-height: 25px;
    font-weight: bold;
}
.title-h4 {
    font-size: 18px;
    padding-top: 10px;
    /*font-weight: 500*/
}
.append-span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}

.content-size {
    margin-top: 10px;
}

.editor {
    width: 95%;
    margin-top: 10px;
}
.v-note-wrapper {
    min-height: 100px;
}
.msg-box,
.img-box {
    margin-top: 10px;
}
.img-box {
    overflow: auto;
}
.bottom-box {
    position: absolute;
    left: 0;
    height: 50px;
    width: 100%;
    bottom: 0;
    background-color: rgb(237, 249, 245);
}
.right-btn {
    width: 50px;
    height: 50px;
    float: right;
    background-color: rgb(225, 237, 233);
    cursor: pointer;
}
/*树*/
ul,
li {
    list-style: none;
}
.tree-ul {
    overflow: hidden;
    width: 100%;
    padding-left: 20px;
}
.child_ul {
    overflow: hidden;
    padding-left: 10px;
}
.tree-li {
    margin-top: 10px;
    font-weight: bold;
    cursor: pointer;
}
.tree-li p {
    height: 24px;
    line-height: 24px;
}
.child-tree-li {
    margin-top: 5px;
    margin-left: 20px;
    font-weight: 500;
    font-size: 14px;
}
.img-box-ex {
    width: 330px;
    height: 330px;
    margin-right: 20px;
    padding-left: 20px;
    position: relative;
    display: inline-block;
    box-sizing: border-box;
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
.dialog-img {
    display: block;
    margin: 0 auto;
}
.upload-demo-box {
    width: 330px;
    height: 330px;
    vertical-align: top;
    display: inline-block;
}
.upload-demo {
    /* margin-top: 20px; */
}
.up-data-btn {
    width: 330px;
    height: 330px;
    /* margin-left: 20px; */
    display: block;
    background: #fff;
    outline: none;
    border: 1px dashed #ccc;
    color: #ccc;
    font-size: 15px;
    /*display: inline-block;*/
}
.Sequence-img {
    width: 100%;
    height: 100%;
}
.img_icon {
    position: absolute;
    right: 0px;
    top: 0;
    font-size: 24px;
    cursor: pointer;
    /*font-weight: bold;*/
}
.img-box-ex:hover {
    cursor: pointer;
    /* border: 1px solid transparent; */
}
.append-span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}
.append-span:hover {
    color: #42b983;
}
.footer {
    position: absolute;
    bottom: 20px;
    right: 29px;
}
@media screen and (max-width: 1024px) {
    .wrapper {
        width: 1024px;
    }
    .tree-box {
        width: 20%;
    }
    .content-box {
        left: 20%;
    }
    .up-data-btn {
        width: 160px;
        height: 170px;
    }
    .upload-demo-box {
        width: 180px;
        height: 180px;
        vertical-align: top;
        display: inline-block;
    }
    .img-box-ex {
        width: 180px;
        height: 170px;
        margin-right: 10px;
        position: relative;
        display: inline-block;
    }
}
@media screen and (max-width: 1366px) {
    .up-data-btn {
        width: 230px;
        height: 230px;
        /* margin-left: 20px; */
        display: block;
        background: #fff;
        outline: none;
        border: 1px dashed #ccc;
        color: #ccc;
        font-size: 15px;
    }
    .upload-demo-box {
        width: 230px;
        height: 230px;
        vertical-align: top;
        display: inline-block;
    }
    .upload-demo {
        margin-top: 0;
    }
    .img-box-ex {
        width: 230px;
        height: 230px;
        margin-right: 20px;
        position: relative;
        display: inline-block;
    }
}
</style>