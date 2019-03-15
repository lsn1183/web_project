<template>
    <div class='Append-basic-temlate' id="book-manage">
        <div class="Append-basic-temlate-countent">
           
        </div>
        <div class="content-box">
            <div class="mid">
                <div class="mid-top">
                    <div class="block-title">
                        <span style="padding-right:10px">项目</span>
                                <el-select v-model="proj_id" placeholder="请选择" @change="select_input" size="small" style="width:100px">
                                    <el-option v-for="item in project_list" :key="item.fw_id" :label="item.proj_name" :value="item.proj_id">
                                    </el-option>
                                </el-select>
                                <span class="header-span" @keyup.enter="search_click(searchValue)">
                                    <el-input clearable @clear="clear_click()" placeholder='搜索式样书内容' size="small"  v-model="searchValue" class="input-with-select">
                                        <el-button slot="append" icon="el-icon-search" @click="search_click(searchValue)"></el-button>
                                    </el-input>
                                </span>
                        <!-- <span style="float:right;margin-top:6px;fontSize:14px;cursor: pointer; " @click="add_new_book_fun('new',null)">[ 添加式样书 ]</span> -->
                        <span style="float:right;margin-top:6px;fontSize:14px; " >
                            <el-dropdown @command="handleCommand">
                            <span class="el-dropdown-link">
                                [ 添加 ]<i class="el-icon-arrow-down el-icon--right"></i>
                            </span>
                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item command="add_input">单本添加</el-dropdown-item>
                                <el-dropdown-item command="add_input_list">批量添加</el-dropdown-item>
                            </el-dropdown-menu>
                            </el-dropdown>
                        </span>
                    </div>
                    <div class="content-box-deep" v-if="!tableflag">
                        <div class="label-box">
                            <div class="label-box-text" >
                                <span v-for="(book,index) in book_data_list" :key="index" :class="{'active':index === inActive}" 
                                 @click="click_book_fun(book,index)" class="book-name-color-active" >[ {{book.book_name}} ]</span>
                            </div>
                            <el-table :data="tableData" border  v-loading="loading">
                                <el-table-column prop="spec_num" label="式样书章节号" width="150" align="left" header-align="center">
                                </el-table-column>
                                <el-table-column prop="spec_name" label="式样书名称" align="left" header-align="center">
                                </el-table-column>
                                <el-table-column prop="ver_list" label="版本"  align="left" header-align="center">
                                    <template slot-scope="scope">
                                        <span class="go-doc-text" v-for="item in scope.row.ver_list" :key="item"> 
                                            <span @click="go_to_html(item,item.spec_ver)">{{item.spec_ver}}</span> 
                                        </span>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="name" label="操作" width="200" align="left" header-align="center">
                                    <template slot-scope="scope">
                                        <el-button size="mini" type="text" @click="add_new_book_fun('children',scope.row)">
                                            <span class="append-span" style="color:#606266;fontSize:14px;font-weight: none;"> &nbsp;[ 添加 ]</span>
                                        </el-button>
                                        <el-popover placement="right" trigger="click" width="200" >
                                            <el-table :data="gridData.ver_list" v-if="delete_input_flag">
                                                <el-table-column  property="spec_ver" label="版本号"></el-table-column>
                                                <el-table-column  property="spec_id" label="操作">
                                                    <template slot-scope="scope">
                                                        <span @click="delete_input_ver(scope.$index,scope.row,'delete_ver')" style="fontSize:12px;cursor:pointer;"> &nbsp;[ 删除 ]</span>
                                                    </template>
                                                </el-table-column>
                                            </el-table>
                                           
                                            <el-button slot="reference" size="mini" type="text"  @click="delete_input(scope.$index,scope.row)">
                                                <span class="append-span" style="color:#606266;fontSize:14px;font-weight: none;"> &nbsp;[ 删除 ]</span>
                                            </el-button>
                                        </el-popover>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </div>
                    <!--  式样书搜索内容 -->
                    <div class="tcontent-box-deep" style="margin-top:20px" v-if="tableflag">
                        <div class="label-box-text" >
                            <span v-for="(book,index) in book_data_list" :key="index" :class="{'active':index == inActive}" 
                             @click="click_book_fun(book,index)" class="book-name-color-active" >[ {{book.book_name}} ]</span>
                        </div>
                        <div class=" warpper">
                            <el-table :data="tableData" border style="width: 100%" class='table-msg'>
                                <el-table-column prop="file_name" label="式样书" min-width = "15%">
                                    <template slot-scope="scope">
                                        <a :href="scope.row.url" target="frSheet" v-html="showDate(scope.row.file_name)"> &nbsp;{{scope.row.file_name}}</a>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="title" label="章节名" min-width= "15%">
                                    <template slot-scope="scope">
                                          <span v-html="showDate(scope.row.title)"></span>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="Outline" label="概要" min-width= "45%">
                                    <template slot-scope="scope">
                                        <span :class="showTotal ? 'total-introduce' : 'detailed-introduce'" v-if="searchValue===''" v-html="scope.row.Outline"></span>
                                        <span :class="showTotal ? 'total-introduce' : 'detailed-introduce'" v-else v-html="showDate(scope.row.Outline)"></span>
                                        <!-- <el-button class="unfold" type="text" @click="showTotalIntro" v-if="showExchangeButton"><u>{{exchangeButton ? '展开' : '收起'}}</u></el-button> -->
                                        <div class="unfold" @click="showTotalIntro" v-if="showExchangeButton">
                                        <p><u>{{exchangeButton ? '展开' : '收起'}}</u></p>
                                        </div>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </div>
                </div>
                <div style="clear: both;"></div>
            </div>
            <div class="right">
            </div>
            <div id="img-dialog-box">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            book_data_list:[
                {'book_name':"机能式样书",id:0},
                {'book_name':"操作式样书",id:1},
                {'book_name':"要求式样书",id:2},
            ],
            inActive:-1,
            searchValue:"",
            tableData:[],
            adaptivePageHeight: window.innerHeight - 300,
            project_list:[],
            proj_id:'',
            book_type:'FUNC',
            gridData:[],
            delete_input_flag:true,
            visible:false,
            loading:true,
            tableData:[],
            tableflag:false,

            // 是否展示所有文本内容
            showTotal:false,
            // 显示展开还是收起
            exchangeButton:true,
            // 是否显示展开收起按钮
            showExchangeButton:true,
            title: '演示展开收起'
        }

    },
    mounted () {
        this.get_project_list()
    },
    methods: {
        showTotalIntro () {
            this.showTotal = !this.showTotal;
            this.exchangeButton = !this.exchangeButton;
        },
        showDate(val) {
            var searchVal = this.trim(this.searchValue)
            return val.replace(new RegExp(searchVal,'ig'), '<font color="red">' + searchVal + '</font>')
        },
        trim(str){  
          return str.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
        },
        handleCommand(command) {
            let datas = {
                "proj_id": this.proj_id,
                "model_id": '',
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
                // console.log(datas,'222222222')
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                // console.log(res.data,'aaaassssssssss')
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '式样书添加') == true) {
                        // to do
                        if (command == 'add_input') {
                            this.add_new_book_fun('new',null)
                        }else{
                            let router_val = {'proj_id':this.proj_id,'input_type':this.book_type};
                            
                            this.$router.push({path:'/tagl/BookManagementList',query:{data:JSON.stringify(router_val)} })
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
        },
        get_project_list () {
            this.$axios.get(this.Ip + '/Project').then(res => {
                if (res.data.result == 'OK') {
                    this.project_list = res.data.content
                    this.proj_id = res.data.content[0].proj_id
                    this.click_book_fun(null,this.inActive)
                } else {
                    //do nothing
                    this.$message({
                        type: 'error',
                        message: res.data.error
                    })
                }
            })
        },
        click_book_fun(val,num){
            this.inActive = num
            this.tableflag = false
            this.book_type ='FUNC'
            if (val!=null && val.id == 1) {
                this.book_type = 'OPE'
            } else if(val!=null && val.id == 2){
                this.book_type ='REQ'
            }
            this.$axios.get(this.Ip + "/DSDocInput/" + this.proj_id +'/' + this.book_type ).then(res=>{
                // console.log(this.inActive,'aaaaaa')
                if (res.data.result == 'OK') {
                    // console.log(res.data.content,'res.data.content')
                    this.tableData = res.data.content
                    this.loading=false
                } else {
                    //do nothing
                    this.$message({
                        type: 'error',
                        message: res.data.error
                    })
                    this.loading=false
                }
            })
        },
        search_click(val){
            let pro_name = ""
            for(let i = 0;i<this.project_list.length;i++){
                if(this.proj_id == this.project_list[i].proj_id){
                    pro_name = this.project_list[i].proj_name 
                }   
            }
            this.inActive = -1//清除式样书类型按钮绑定的class            
            if (this.searchValue) {
                this.$axios.get(this.Ip + '/FunSearch/'+ pro_name + "/" +this.searchValue).then(res => {
                    // console.log(res.data,'==========')
                    if(res.data.result == 'OK'){
                        this.tableData = res.data.content
                        this.tableflag = true
                    }
                })
            }
        },
        go_to_html(val,index){
            window.open(val.url)
        },
        clear_click () {
            this.searchValue = ''
        },
        select_input () {
            this.$axios.get(this.Ip + "/DSDocInput/" + this.proj_id +'/' + this.book_type ).then(res=>{
                this.tableData = res.data.content
            })
        },
        add_new_book_fun(val,data){
            let datas = {
                "proj_id": this.proj_id,
                "model_id": '',
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '式样书添加') == true) {
                        // to do   
                        let router_val = {'proj_id':this.proj_id,'input_type':this.book_type,'type':val}
                        if (val == 'children') {
                            router_val = data
                        }
                        // console.log(router_val,'aaaa')
                        this.$router.push( {path:'/tagl/BookManagement',query:{data:JSON.stringify(router_val)} })
                        
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
        delete_input(index,data){
            // console.log(this.userPurviewManage('设计书_删除'),'data')
            let datas = {
                "proj_id": this.proj_id,
                "model_id": '',
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '式样书删除') == true) {
                        // to do
                        if (data.ver_list.length == 0) {//删除整本式样书
                            this.delete_input_flag = false
                            this.delete_input_ver(index,data,'delete')
                        }else{//删除某版本式样书
                            this.gridData = data
                            this.delete_input_flag = true
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
            
        },
        delete_input_ver(index,data,submit){
            // console.log(index,data,submit)
            let self = this
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                const commitUserID = window.sessionStorage.getItem('Uall')
                if(submit == 'delete'){//删除整本
                    data.ver_id = 0
                }
                this.$axios.delete(this.Ip + '/DSDocInput/' + commitUserID + '/' + data.spec_id + "/" + data.ver_id).then(res => {
                    if (res.data.result == 'OK') {
                        // console.log(res,'res')
                        if (submit == 'delete') {
                            this.tableData.splice(index, 1)                            
                        } else {
                            this.gridData.ver_list.splice(index, 1)
                        }
                        this.$message({
                            type: 'success',
                            message: '删除成功!'
                        })
                    } else {
                        this.$message({
                            type: 'error',
                            message: res.data.error
                        })
                    }
                })
            })
        }
    }
}
</script>

<!-- <style type="text/css">
pre {
    white-space: pre-line;
}
</style> -->

<style scoped>
.total-introduce {
    white-space: pre-line;
}
.detailed-introduce {
    white-space: pre-line;
    display: -webkit-box !important;
    overflow: hidden;
    text-overflow: ellipsis;
    word-break: break-all;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
}
.unfold{
    color: blue;
    text-align: right;
}
.el-dropdown-link {
    cursor: pointer;
    /* color: #409EFF; */
}
.input-with-select{
    width: 50%
}
.active{
    color: #42b983
}
.book-name-color-active:nth-last-of-type(2){
    margin: 0 20px 0 20px;
}
.label-box-warp-border{
    margin-right: 20px;
    border: 1px solid rgb(239, 239, 239);
    background-color: #fff;
    outline-offset: -1px;
    outline: 1px solid rgb(239, 239, 239);
    border-radius: 4px;
}
.inline-black {
    display: inline-block;
}
.margin-left {
    margin-left: 42px;
}
.margin-right {
    margin-right: 40px;
}
.margin-right-input {
    margin-right: 21px;
}
.go-doc-text {
    padding-right: 10px;
}
.go-doc-text:hover {
    color: #42b983;
    cursor: pointer;
}
.Append-basic-temlate {
    margin: 0 auto;
    width: 100%;
    height: 100%;
    /*overflow-y: scroll;*/
}
.Append-basic-temlate-countent {
    max-width: 300px;
    width: 15%;
    height: 100%;
    padding: 20px;
    float: left;
}
.header {
    height: 400px;
    padding: 10%;
    clear: both;
}
.content-box {
    float: left;
    width: 84%;
    padding-left: 1%;
    height: 98%;
    color: #606266;
    background-color: #fff;
    border-left: 2px solid rgba(216,231,223,.5);
    overflow: scroll;
    overflow-x: hidden;

}
.mid {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
    padding-right: 20px;
    background-color: #fff;
    border-right: 2px solid rgba(216,231,223,.5);
    overflow: scroll;
    overflow-x: hidden;
}
.mid-top {
    position: absolute;
    top: 0;
    bottom: 55px;
    width: 100%;
    padding-right: 20px;
    /* overflow-y: scroll; */
}
.footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}
.block-title {
    margin: 20px 0 0px 0;
}
h2 {
    font-size: 22px;
    font-weight: bolder;
    background-color: #6bcca0;
    color: white;
    padding-left: 10px;
    line-height: 25px;
}

.label-box {
    width: 100%;
    overflow: hidden;
}
.label-box-text {
    margin-top: 20px;
    margin-bottom: 20px;
    font-size: 14px;
}
.label-box-text span{
    cursor: pointer;
}

.upload-demo {
    margin-top: 10px;
}
.upload-demo-box {  
    width: 260px;
    height: 100px;
    /*display: inline-block;*/
}
.add-box {
    /*line-height: 100px;*/
    height: 100px;
    width: 100px;
    padding-top: 20px;
    text-align: center;
    border: 1px double #ccc;
    cursor: pointer;
    font-size: 14px;
    /*margin:20px auto;*/
    margin-top: 20px;
}
.active {
    background: #fff;
}
.up-data-btn {
    width: 330px;
    height: 320px;
    /* margin-left: 20px; */
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
    width: 350px;
    height: 330px;
    margin-top: 10px;
    padding-right: 20px;
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
}
.dialog_img {
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
.dialogimg {
    display: block;
    margin: 0 auto;
}
.textarea-name {
    font-size: 12px;
    font-family: "\5FAE\8F6F\96C5\9ED1";
}
@media screen and (max-width: 1366px) {
    .up-data-btn {
        width: 230px;
        height: 240px;
        /* margin-left: 20px; */
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
        margin-top: 10px;
    }
    .img-box {
        width: 250px;
        height: 250px;
        margin-top: 10px;
        margin-right: 20px;
        position: relative;
        display: inline-block;
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
    .Append-basic-temlate-countent {
        width: 180px;
        height: 100%;
        float: left;
    }
    .header {
        height: 100%;
        width: 180px;
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
        margin-top: 10px;
        margin-right: 10px;
        position: relative;
        display: inline-block;
    }
}
</style>
