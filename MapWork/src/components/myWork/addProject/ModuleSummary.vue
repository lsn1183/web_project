<template>
    <div class="Add-File-Title">
        <div class="Add-File-Title-nav">
            <!-- <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="基本设计" icon="el-icon-edit" status="process">1</el-step>
                    <el-step class="jump" title="式样书">2</el-step>
                    <el-step class="jump" title="Usecase">3</el-step>
                </el-steps>
            </div> -->
        </div>
        <div id="Add-File-Title">
            <div class="mid">
                <div class="mid-top">
                    <div class="div-centers">
                        <div class="div-title div-title-ex">
                            <h2>模块信息
                                <!-- <i class="el-icon-question" title="I/F" style="font-size:15px;height:20px;vertical-align:middle"></i> -->
                            </h2>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">模块编号:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.code"></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">名称:</div>
                        <div class="div-input">
                            <el-input disabled v-model="file_form.title"></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label" style="margin-left:10px">
                        <div class="div-title summary">概述:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.summary" type="textarea" :autosize="{ minRows:14, maxRows:16}"></el-input>
                        </div>
                    </div>
                    <!-- <div class="div-center div-center-label">
                        <div class="div-title">版本:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.ver" disabled></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">文档创建者:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.creator" disabled></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label" style="margin-left:10px">
                        <div class="div-title">文档更新者:</div>
                        <div class="div-input ">
                            <el-input v-model="file_form.editor" disabled></el-input>
                        </div>
                    </div> -->
                </div>
                <div class="min-footer">
                    <div class="div-input" style="text-align: right;width:100%">
                        <el-button @click="save()" type="primary" size="mini" >&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
                        <el-button @click="cancel()" type="primary" size="mini">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    </div>
                </div>
            </div>
            <div class="footer"></div>

        </div>
    </div>
</template>

<script>
require('../../../assets/js/jquery-1.8.3.min.js')
export default {
    data () {
        return {
            file_form: {
            },
            doc_id: null,
            summary: '',
            // active: Number(window.sessionStorage.getItem('Step-Asa')),
            get_data:"",
            save_data:"",
        }
    },
    mounted() {
        this.getData()
    },
    methods: {
        getData(){
            let model_id = window.sessionStorage.getItem('model_id')
            if(model_id != null){
                this.$axios.get(this.Ip+ '/Model/' + model_id).then(res=>{
                    if(res.data.result == 'OK'){
                        this.file_form = res.data.content[0]
                        this.get_data = JSON.stringify(this.file_form) 
                    }
                }) 
            }else{
                let data = {"title":'',"summary":'',"model_id":'','code':''}
                this.file_form = data
                this.get_data = JSON.stringify(this.file_form) 
            }
            
        },
        save(){
            if(this.file_form.title == ""){
                this.$message({
                  type: 'error',
                  message: '名称信息不可为空！'
                })
            }else{
                this.$axios.post(this.Ip + '/Model',this.file_form).then(res=>{
                    if(res.data.result == 'OK'){
                        this.$message({
                          type: 'success',
                          message: '保存成功!'
                        })
                        this.$store.state.fpm_id = 2
                        let routerValue = { path: '/tagl/Add_NewProject/ModelTemplate', query: { page: this.$route.query.page } }
                        this.$router.push(routerValue)
                    } else {
                        this.$message({
                          type: 'error',
                          showClose: true,
                          message: '保存失败!',
                          duration:0,
                        })
                    }
                })
            }
            
        },
        cancel(){
            this.save_data = JSON.stringify(this.file_form)
            let routerValue = { path: '/tagl/Add_NewProject/ModelTemplate', query: { page: this.$route.query.page } }
            if (this.save_data == this.get_data) {
                this.$store.state.fpm_id = 2
                this.$router.push(routerValue)
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        this.$store.state.fpm_id = 2
                        this.$router.push(routerValue)
                    })
                    .catch(() => { })
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
.mid-top{
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

.div-centers{
    width: 100%;
    text-align: left;
    margin:40px 0 0 0;
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
    line-height: 25px
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
.min-footer{
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
.header-top{
    height: 100px;
}
.header{
    height: 225px;
    padding:10%;
    clear: both;
}

@media screen and (max-width:1366px) {
    .mid{
        width: 880px;

    }
    .right{
        width: 20%;
        height: 100%;
        float: left;
    }
    .checked_input_list{
        margin-left: 20px;
        float: left;
        height: 400px;
    }
}
@media screen and (max-width:1334px) {
    .countent {
        max-width: 300px;
        min-width: 200px;
        width: 15%;
        height: 100%;
        padding: 20px;
        float: left;
    }
    #Add-File-Title{     
        float: left;
        width: 80%;
        height: 100%;
    }
    
  }
@media screen and (max-width:1024px) {
    .Add-File-Title{
        width: 1024px;
    }
    .header-top{
        display: none;
    }
    .header{
        height: 100%;
        padding:10%;
        clear: both;
    }
    #Add-File-Title{
        float: left;
        width: 820px;
        height: 100%;
    }
    .mid{
        width: 635px;
    }
    .div-input {
        display: inline-block;
        width: 380px;
    }
    .checked_input_list{
        margin-left: 20px;
        float: left;
        height: 400px;
    }
  }
</style>
