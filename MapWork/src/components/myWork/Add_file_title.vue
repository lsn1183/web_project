<template>
    <div class="Add-File-Title">
        <div class="Add-File-Title-nav">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="基本设计" icon="el-icon-edit" status="process">1</el-step>
                    <el-step class="jump" title="式样书">2</el-step>
                    <el-step class="jump" title="Usecase">3</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Title">
            <div class="mid">
                <div class="mid-top">
                    <div class="div-centers">
                        <div class="div-title div-title-ex">
                            <h2>基本设计
                                <!-- <i class="el-icon-question" title="I/F" style="font-size:15px;height:20px;vertical-align:middle"></i> -->
                            </h2>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">标题:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.title"></el-input>
                        </div>
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
                        <div class="div-title">文档创建者:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.creator" disabled></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label" style="margin-left:10px">
                        <div class="div-title">文档更新者:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.editor" disabled></el-input>
                        </div>
                    </div>
                </div>
                    
                <div class="min-footer">
                    <div class="div-input input-btn">
                        <el-button size="mini" type="info" disabled ><i class="el-icon-arrow-left"></i>上一步</el-button>
                        <el-button @click="save()" type="primary" size='mini'>&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                        <el-button @click="cancel()" type="primary" size='mini'>&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                        <el-button size="mini" type="primary" @click="next">下一步<i class="el-icon-arrow-right"></i></el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            file_form: {
                doc_type: 'BASIC',
                title: '',
                ver: 0.01,
                creator: window.sessionStorage.getItem('Uall'),
                editor: window.sessionStorage.getItem('Uall'),
                summary: '',
                model_id:JSON.parse(window.sessionStorage.getItem('treeNodeId')).model_id,
                proj_id:JSON.parse(window.sessionStorage.getItem('treeNodeId')).proj_id,
            },
            doc_id: null,
            active:0,
            detailData:{},
            height_light_data:null,
            dbrfmFlag:false
        }
    },
    mounted(){
        if (this.$route.query.params) {
            // 用于点击退出按钮树节点高亮
            this.detailData = JSON.parse(this.$route.query.params)
            // 用于控制基本设计和详细设计谁显示
            this.dbrfmFlag = this.detailData.dbrfmFlag
        }
    },
    methods: {
        get_save_data(doc_id){
            this.$axios.get(this.Ip + '/DSDoc/' + doc_id).then(res => {
                if (res.data.result == 'OK') {
                    this.file_form = res.data.content
                } else {
                    this.$message({
                        showClose: true,
                        message: '请求失败',
                        type: 'error'
                    })
                }
            })
            .catch(err => {
                this.$message({
                    showClose: true,
                    message: '服务异常',
                    type: 'error'
                })
            })
        },
        save (type) {
            if (this.userPurviewManage('设计书_添加') == true) {
                if (this.file_form.title != "") {
                    this.$axios.post(this.Ip + '/DSDoc', this.file_form).then(res => {
                        if (res.data.result == 'OK') {
                            window.sessionStorage.setItem('DocId', res.data.doc_id)
                            this.doc_id = res.data.doc_id
                            this.$store.commit('amendDocId', res.data.doc_id)
                            this.$message({
                                message: '添加成功',
                                type: 'success'
                            })
                            this.height_light_data = this.detailData
                            window.sessionStorage.setItem("Step-Asa", 1)
                            window.sessionStorage.setItem("DocId", res.data.doc_id)
                            this.get_save_data(res.data.doc_id)
                            if (type == 'next') {
                                this.$router.push('/tagl/edit_input')
                            }
                        } else {
                            this.$message({
                                showClose: true,
                                message: '添加失败',
                                type: 'error'
                            })
                        }
                    }).catch(err => {
                    })
                } else {
                    this.$alert("标题不可为空 !", { title: '提示' })
                }
            } else {
                this.$message({
                    type:"warning",
                    message:"您没有操作权限！"
                })
            }
        },
        cancel () {
            if (this.height_light_data === null) {
            // 当什么都没操作时候，清空session，解决返回list页面还默认显示添加按钮
                this.$router.push({path:"/tagl/File_design/basic_design_template",query:{params:JSON.stringify(this.detailData)}})
                // window.sessionStorage.removeItem("treeNodeId")
            }else{
                this.$router.push({path:"/tagl/File_design/basic_design_template",query:{params:JSON.stringify(this.height_light_data)}})
            }
        },
        next(){
            this.save('next')
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
.footer{
    position: absolute;
    bottom:20px;
    right: 20px;

}
.min-footer{
    position: absolute;
    bottom: 20px;
    right: 20px;
}
#Add-File-Title {
    float: left;
    margin: 0 auto;
    width: 84%;
    height: 100%;
    padding-left: 1%;
}

.div-center {
    width: 100%;
    text-align: left;
    padding: 0 0 20px;
}
.div-centers{
    width: 100%;
    text-align: left;
    margin:40px 0 0 0;
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
    font-size: 15px
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
  }
</style>
