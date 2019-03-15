<template>
    <div class="add-project-step" v-loading="loading">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="项目信息">1</el-step>
                    <!-- <el-step class="jump" title="平台">2</el-step> -->
                    <el-step class="jump" title="知识库">3</el-step>
                    <el-step class="jump" title="模块" >4</el-step>
                    <el-step class="jump" title="模块负责组" icon="el-icon-edit" status="process">5</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Mode">
            <div class="mid">
                <div class="mid-top">
                    <div class="step-one-title">
                        <h2 >模块负责组
                            <i class="el-icon-question" style="font-size: 15px;" title="模块负责组"></i>
                        </h2>
                    </div>
                    <el-table  :data="StepData.model_list" style="width: 97%" border>
                        <el-table-column prop="parent_title" sortable label="父模块" align='center' header-align='center'></el-table-column>
                        <el-table-column prop="title" sortable label="模块" align='left' header-align='center' ></el-table-column>
                        <el-table-column  label="分组" header-align='center'>
                            <template slot-scope="scope">
                                <el-select v-model="scope.row.group_list" multiple class="StepData-SelectBox" placeholder="请选择">
                                    <el-option
                                      v-for="item in group_list"
                                      :key="item"
                                      :label="item"
                                      :value="item">
                                    </el-option>
                                  </el-select>
                            </template>
                        </el-table-column>
                    </el-table>    
                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="prev()"><i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button @click="save()" type="primary" size='mini'>&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button @click="cancel()" type="primary" size='mini'>&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="next()">&nbsp;&nbsp;完&nbsp;&nbsp;&nbsp;成&nbsp;&nbsp;</el-button>  
                </div>
            </div>
        </div>
    </div>
</template>
<script>
require('../../../assets/js/jquery-1.8.3.min.js')
export default {
    data() {
        return {
            checkAll: false,
            active:Number(window.sessionStorage.getItem('step_id')),
            spec_list_flag:false,
            value5:"",
            group_list: [],
            modelOptions: [
                { model_name: 'Route', model_id: 1 },
                { model_name: 'Guide', model_id: 2 },
                { model_name: 'RouteView', model_id: 3 },
                { model_name: 'GuideView', model_id: 4 },
                { model_name: 'RouteWeb', model_id: 5 },
                { model_name: 'GuideWeb', model_id: 6 },
                { model_name: 'RouteNive', model_id: 7 },
                { model_name: 'GuideNive', model_id: 8 },
                { model_name: 'RouteVoice', model_id: 9 },
                { model_name: 'GuideVoice', model_id: 10 },
                { model_name: 'DataView', model_id: 11 }
            ],
            StepData:{
                proj_id: 0,
                user_name:window.sessionStorage.getItem('Uall'),
                model_list: []
            },
            get_data: '',
            save_data: '',
            proj_id:window.sessionStorage.getItem('proj_id'),
            accessToken:window.sessionStorage.getItem("accessToken"),
            loading:true,
        }
    },
    created() {
    },
    mounted(){
        this.getGroupList()
        this.getData()
        var self = this
        $('.jump').on('click', function(e) {
          self.jump_to($(this).text())
        });
    },
    methods: {
        getGroupList(){
            let datas={
                "accessToken":this.accessToken,
                "proj_id":this.proj_id
            }
            this.$axios.post(this.Ip+"/CactusGroups",datas).then(res=>{
                // console.log(res,"group")
                if(res.data.result=="OK"){
                    this.group_list=res.data.content
                }
            })
        },
        getData(){
            this.$axios.get(this.Ip+"/ApiProjectGroup/"+ this.proj_id).then(res=>{
                // console.log(res,"table")
                if(res.data.result=="OK"){
                    this.StepData=res.data.content
                    // for(var mod of res.data.content.model_list){
                    //     for(var opt of this.modelOptions){
                    //         if(mod.model_id ==opt.model_id)
                    //             this.StepData.model_list.push({"group_list":mod.group_list,"model_id":mod.model_id,"model_name":opt.model_name,})
                    //     }
                    // }
                    this.get_data = JSON.stringify(this.StepData)
                    this.loading = false
                }else{
                    this.loading = false
                    this.$message({
                        type:"error",
                        message:res.data.result
                    })
                }
            })
        },
        prev() {
            // this.$router.push('/tagl/Project_Step_Four')
            let router_flag=this.$route.query.flag
            let routerValue={path:'/tagl/Project_Step_Four',query:{flag:router_flag}}
            this.$router.push(routerValue)
        },
        jump_to(index){
            switch(index){
                case "项目信息":
                    // this.JumpAndSave()
                    var router_flag=this.$route.query.flag
                    if (this.$route.query.flag=="true") {
                        router_flag="false"
                    }
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
                case "5模块负责组":
                  if(this.active ==4){
                    this.$router.push('/tagl/Project_Step_Five')
                  }
                  break;
              }
        },
        save() {
            this.StepData.proj_id = this.proj_id
            this.StepData.user_name = window.sessionStorage.getItem("Uall")
            this.$axios.post(this.Ip + '/ApiProjectGroup', this.StepData)
            .then(res => {
                // console.log(res,"save")
                // console.log(this.StepData,"save2")
                if (res.data.result == 'OK') {
                    // window.sessionStorage.setItem('step_id', 4)
                    // this.$router.push('/tagl/Add_NewProject')
                    this.getData()
                    this.$message({
                        message: '保存成功',
                        type: 'success'
                    })
                } else {
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
        next() {
            this.StepData.proj_id = this.proj_id
            this.StepData.user_name = window.sessionStorage.getItem("Uall")
            this.$axios.post(this.Ip + '/ApiProjectGroup', this.StepData)
            .then(res => {
                if (res.data.result == 'OK') {
                    if (window.sessionStorage.getItem('step_id') ==4) {
                        window.sessionStorage.setItem('step_id', 5)
                    }
                    this.$store.state.fpm_id = 1
                    this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
                } else {
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
        cancel() {
            this.save_data = JSON.stringify(this.StepData)
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
.step-one-content {
    margin-top:20px;
    margin-left: 20px;  
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
.project_box{
    margin:20px 0 20px 20px;
}
.project_box_content{
    width: 200px;
    height:150px;
    line-height:150px;
    border:1px solid ;
    display:inline-block;
    text-align: center;
}
/**/
.step-one-title {
    margin:40px 0 20px 0;
}
.step-one-text{
    margin-left: 80px;
}
.checked_input_list{
    margin-left: 20px;
    margin-top:100px;
    float: left;
    width: 100%;
    height: 400px;
}
.checked_input_list_title{
    margin-bottom: 15px;
    font-size: 18px;
}
.checked_input_list_li{
    list-style: none;
    width: 100%;
    line-height:30px;
    cursor: pointer;
    font-size: 14px;

}
.step-one-content {
    margin-top:20px;
    margin-left: 20px;  
}
.select_input{
    width: 50%;
}
.sequence_title_text{
  margin-left: 20px;
  margin-bottom: 20px;
  font-size: 14px;
  color: #5e6d82
}
.select_content{
    position: relative;
    margin-top: 20px;
}
.select_option_box{
    position: absolute;
    background-color: white;
    z-index: 5;
    margin-top:10px;
    width: 50%;
    max-height: 150px;
    overflow-y: scroll;
    border:1px solid #ccc;
    border-radius: 5px;
}
.select_option_li{
    font-size: 14px;
    width: 98%;
    white-space: nowrap;
    list-style: none;
    line-height: 30px;
    padding-left: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #606266;
}
.select_option_li:hover{
    cursor: pointer;
    background-color: #f5f7fa;
}
.StepData-SelectBox{
    width: 80%;
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