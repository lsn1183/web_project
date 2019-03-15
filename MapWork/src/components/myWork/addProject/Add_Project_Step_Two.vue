<template>
    <div class="add-project-step">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="项目信息">1</el-step>
                    <el-step class="jump" title="平台" icon="el-icon-edit" status="process">2</el-step>
                    <el-step class="jump" title="知识库">3</el-step>
                    <el-step class="jump" title="模块">4</el-step>
                    <el-step class="jump" title="模块负责组">5</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Mode">
            <div class="mid">
                <div class="mid-top">
                    <div class="div-center">
                        <div class="div-title div-title-ex">
                            <h2>平台
                                <!-- <i class="el-icon-question" title="I/F" style="font-size:15px;height:20px;vertical-align:middle"></i> -->
                            </h2>
                        </div>
                    </div>
                    <div class="project-box-wapper">
                        <!-- <div class="project-box" >
                            <el-radio v-model="projectStepTwoData.fw_id" label="1">
                                <div class="project-box_content">iauto1.0
                                </div>
                            </el-radio>
                        </div>
                        <div class="project-box">
                            <el-radio v-model="projectStepTwoData.fw_id" label="2">
                                <div class="project-box_content">iauto2.0
                                </div>
                            </el-radio> 
                        </div> -->
                        <div class="project-box" v-for="item in FwList">
                            <el-radio v-model="projectStepTwoData.fw_id" :label="item.fw_id" @change="changeRadio(item)">
                                <div class="project-box-content">{{item.fw_name}}
                                </div>
                            </el-radio> 
                        </div>
                    </div>
                        
                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="prev()"><i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button @click="save()" type="primary" size='mini'>&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button @click="cancel()" type="primary" size='mini'>&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="next()">下一步<i class="el-icon-arrow-right"></i></el-button>  
                </div>
            </div>
        </div>
        <!-- <div class="two">
            <div style="width:80%;margin:4% 0 0 8%">
                <div style="padding:0 0 0 5%">
                    
                </div>                
                <div class="footer" style="padding:13% 0 0 ;">
                    <el-button @click="prev()" style="margin:0 3% 0 3%;padding:10px 50px 10px 50px">上一步</el-button>
                    <el-button @click="next()" style="margin:0 3% 0 3%;padding:10px 50px 10px 50px">下一步</el-button>
                    <el-button @click="pass()" style="margin:0 3% 0 3%;padding:10px 50px 10px 50px">取消</el-button>      
                </div>
            </div>
        </div> -->    
    </div>
    
</template>
<script>
require('../../../assets/js/jquery-1.8.3.min.js')
export default {
    data() {
        return {
            projectStepTwoData: { 
                proj_id: 0,
                user_name:window.sessionStorage.getItem('Uall'),
                fw_id: 0 
            },
            active:Number(window.sessionStorage.getItem('step_id')),
            FwList:[],
            fw_name:"",
            get_data: '',
            save_data: '',
        }
    },
    mounted() {
        this.getFramework()
        this.reqStepTwoData()
        var self = this
        $('.jump').on('click', function(e) {
          self.jump_to($(this).text())
        });
    },
    methods: {
        reqStepTwoData() {
            this.$axios.get(this.Ip + '/ProjectFW/' + Number(window.sessionStorage.getItem('proj_id')))
            .then(res => {
                // console.log(res)
                if (res.data.result == 'OK') {
                    this.projectStepTwoData.fw_id = res.data.content.fw_id
                    this.fw_name = res.data.content.fw_name
                    window.sessionStorage.setItem('fw_name',res.data.content.fw_name)
                } else {
                    // alert('服务器出错')
                }
                this.get_data = JSON.stringify(this.projectStepTwoData)
            })
            .catch(err => {
                alert(err)
            })
        },
        getFramework(){
            this.$axios.get(this.Ip+"/Framework").then(res=>{
                if(res.data.result=="OK"){
                    // console.log(res)
                    this.FwList = res.data.content
                }else{

                }
            })
            .catch(res=>{
                alert(err)
            })
        },
        prev() {
            this.$router.push('/tagl/Project_Step_One')
        },
        next() {
            if (this.projectStepTwoData.fw_id == 0) {
                this.$message({
                    message: '请选择框架',
                    type: 'error'
                })
                return
            }
            this.projectStepTwoData.proj_id = window.sessionStorage.getItem('proj_id')
            this.$axios.post(this.Ip + '/ProjectFW', this.projectStepTwoData)
            .then(res => {
                // console.log(res,"pfw")
                if (res.data.result == 'OK') {
                    if (window.sessionStorage.getItem('step_id') == 1) {
                        window.sessionStorage.setItem('step_id', 2)
                    }
                    window.sessionStorage.setItem('fw_name',this.fw_name)
                    this.$router.push('/tagl/Project_Step_Three')
                }else{
                    this.$message({
                        showClose: true,
                        message: '保存失败',
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
        },
        save() {
            if (this.projectStepTwoData.fw_id == 0) {
                this.$message({
                    message: '请选择框架',
                    type: 'error'
                })
                return
            }
            this.projectStepTwoData.proj_id = window.sessionStorage.getItem('proj_id')
            this.$axios.post(this.Ip + '/ProjectFW', this.projectStepTwoData)
            .then(res => {
                if (res.data.result == 'OK') {
                    window.sessionStorage.setItem('fw_name',this.fw_name)
                    this.$message({
                        message: '保存成功',
                        type: 'success'
                    })
                    this.reqStepTwoData()
                }else{
                    this.$message({
                        showClose: true,
                        message: '保存失败',
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
        },
        changeRadio(data){
            // console.log("2")
            this.fw_name = data.fw_name
        },
        JumpAndSave() {
            this.projectStepTwoData.proj_id = window.sessionStorage.getItem('proj_id')
            this.$axios.post(this.Ip + '/ProjectFW', this.projectStepTwoData)
            .then(res => {
                if (res.data.result == 'OK') {
                    window.sessionStorage.setItem('fw_name',this.fw_name)
                    // if (window.sessionStorage.getItem('step_id') < 2) {
                    //     window.sessionStorage.setItem('step_id', 2)
                    //     this.$store.state.step_id = 2
                    // }
                    // this.$message({
                    //     message: '保存成功',
                    //     type: 'success'
                    // })
                }else{
                    this.$message({
                        showClose: true,
                        message: '保存失败',
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
        },
        jump_to(index){
            switch(index){
                case "项目信息":
                  // this.JumpAndSave()
                  this.$router.push('/tagl/Project_Step_One')
                  break;
                case "平台":
                  // this.JumpAndSave()
                  this.$router.push('/tagl/Project_Step_Two')
                  break;
                case "知识库":
                  // this.JumpAndSave()
                  this.$router.push('/tagl/Project_Step_Three')
                  break;
                case "模块":
                  // this.JumpAndSave()
                  this.$router.push('/tagl/Project_Step_Four')
                  break;
                case "模块负责组":
                  // this.JumpAndSave()
                  this.$router.push('/tagl/Project_Step_Five')
                  break;
                // case "1输入项目名称":
                //   if(this.active ==0){
                //     this.$router.push('/tagl/step1')
                //   }
                //   break;
                // case "2选择框架":
                //   if(this.active ==1){
                //     this.$router.push('/tagl/step2')
                //   }
                //   break;
                case "3技术文档":
                  if(this.active >1){
                    this.$router.push('/tagl/Project_Step_Three')
                  }
                  break;
                // case "4选择模块":
                //   if(this.active ==3){
                //     this.$router.push('/tagl/step4')
                //   }
                //   break;
                // case "5选择模块负责组":
                //   if(this.active ==4){
                //     this.$router.push('/tagl/step5')
                //   }
                //   break;
              }
        },
        cancel() {
            this.save_data = JSON.stringify(this.projectStepTwoData)
            if (this.save_data == this.get_data) {
                window.sessionStorage.removeItem('proj_id')
                window.sessionStorage.removeItem('step_id')
                this.$store.state.fpm_id = 1
                this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
            }else{
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
                .catch(() => {}) 
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
.header-top{
    height: 100px;
}
.header{
    height: 400px;
    padding:10%;
    clear: both;
}
.mid{
    width: 80%;
    height: 100%;
    float: left;
    padding-top: 40px;
    padding-right: 1%;
    position: relative;
    padding-right: 20px;
    padding-bottom:55px;
    border-right: 1px solid #ccc;
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

/**/

#Add-File-Mode {
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
    margin:40px 0 20px 0;

}
.step-one-title {
    margin:40px 0 20px 0;
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
.project-box-wapper{
    width: 80%;
}
.project-box{
    margin:20px 0 20px 20px;
    float: left;

}
.project-box-content{
    width: 200px;
    height:150px;
    line-height:150px;
    border:1px solid ;
    display:inline-block;
    text-align: center;
}
@media screen and (max-width:1366px) {
    .mid{
        width: 880px;

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
  #Add-File-Mode{     
    float: left;
    width: 80%;
    height: 100%;
    }
    
  }
@media screen and (max-width:1024px) {
    .add-project-step{
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
    #Add-File-Mode{
        float: left;
        width: 820px;
        height: 100%;
    }
    .mid{
        width: 635px;

    }
    .div-input {
        display: inline-block;
        width: 400px;
    }
  }
</style>