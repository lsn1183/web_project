<template>
    <div id="basic-degign-step-one">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="基本设计"  v-if="dbrfmFlag">1</el-step>
                    <el-step class="jump" title="详细设计"  v-else>1</el-step>
                    <el-step class="jump" title="式样书" icon="el-icon-edit" status="process">2</el-step>
                    <el-step class="jump" title="Usecase">3</el-step>
                </el-steps>
            </div>
        </div>
        <div class="cbody">
               
            <div class="mid">
                <div class="mid-top">
                    <div class="step-one-title">
                        <h2>
                            <span style="line-height:25px;float:left">式样书</span>
                            <i class="el-icon-question" style="font-size:15px; line-height:25px;float:left;margin-left:3px" title="请提供和本设计相关的全体式样书，式样书可以是要求式样书、机能式样书、操作式样书等"></i>
                            <!-- <div style="display:inline-block;" title="选择UseCase实现的式样书章节:例如，实现了机能式样书func_2_01_Map.xlsm第2.1.1章">
                                <img src="../../assets/img/wenhao10.svg" alt="" style="width:17px;height:17px;">
                            </div> -->
                        </h2>
                    </div>

                    <div class="step-one-content">
                        <div class="step-one-content-books">
                            <div class="checked-input-list-title">选择具体的式样书</div>
                            <div class="select-content" style="">
                                <!-- <el-autocomplete class="select-input" clearable v-model="input_spec" value-key="title" :fetch-suggestions="querySearch" 
                                placeholder="请输入内容"  @focus="clear_input" @select="handleSelect">
                                </el-autocomplete> -->
                                <el-input placeholder="可输入搜索具体式样书" class="select-input" clearable v-model="input_spec" @focus="clear_input"   @blur="loose_focus"></el-input>
                                <div v-show="spec_list_flag==true" class="select-option-box" >
                                    <ul v-for="(item,index) in options">
                                        <li v-if="item.select"  :title="item.title" class="select-option-li" style="color: #42b983" @click="handleSelect(item)">
                                            {{item.title}}
                                        </li>
                                        <li v-else :title="item.title" class="select-option-li" @click="handleSelect(item)">
                                            {{item.title}}
                                        </li>
                                    </ul>
                                    
                                </div>
                            </div>
                        </div>
                    </div>
      
                    <div  class="checked-input-list">
                        <el-table :data="stepOneData.FUNC" border style="width: 98%">
                            <!-- <el-table-column fixed prop="spec_type" label="类别" width="100">
                            </el-table-column> -->
                            <el-table-column fixed prop="title" label="已选式样书" header-align='center'>
                                <template slot-scope="scope">
                                    <span :title="scope.row.title" style="white-space: nowrap;text-overflow: ellipsis;cursor: pointer;"@click="LinkURL(scope.row)">{{scope.row.title}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column fixed="right" label="操作" header-align='center' width="60">
                              <template slot-scope="scope">
                                <!-- <el-button @click="look_input(scope.row)" type="text" size="small" style="">[ 查看 ]</el-button> -->
                                <el-button @click="delete_input(scope.row,scope.$index)" type="text" size="small" style="">[ 删除 ]</el-button>
                              </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
                    
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="prev()"><i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button size="mini" type="primary" @click="save()">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>  
                    <!-- <el-button size="mini" type="primary" @click="next">下一步<i class="el-icon-arrow-right"></i></el-button> -->
                    <el-button size="mini" type="primary" @click='next()'>下一步<i class="el-icon-arrow-right"></i></el-button>    
                </div> 
            </div>
            <div class="right">
            </div>
        </div>   
    </div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    name: 'CreateBasicDesignStepOne',
    data() {
        return {
            checkAll: false,
            active: Number(window.sessionStorage.getItem('Step-Asa')),
            tecBookArray: [],
            optBooksArray: [],
            // books: requireBooksOptions,
            // styleBook: '要求式样书',
            stepOneData: {
                doc_id: 0,
                sec_id: 0,
                micro_ver:Number(window.sessionStorage.getItem('ver')),
                commit_user:window.sessionStorage.getItem('Uall'),
                sec_type: 'SPEC',
                FUNC: [] //requireBookArray
            },
            spec_list_flag:false,
            input_spec:"",
            select_list:[],
            options: [{
              value: 'func_2_01_Map.xlsm-2.1.1.地図種類',
              label: 'func_2_01_Map.xlsm-2.1.1.地図種類'
            }, {
              value: 'func_2_01_Map.xlsm-2.1.1.1.通常地図',
              label: 'func_2_01_Map.xlsm-2.1.1.1.通常地図'
            }, {
              value: 'func_2_02_Route.xlsm-2.2.2.探索考慮項目',
              label: 'func_2_02_Route.xlsm-2.2.2.探索考慮項目'
            }, {
              value: 'func_2_02_Route.xlsm-2.2.2.1.ルート探索基準',
              label: 'func_2_02_Route.xlsm-2.2.2.1.ルート探索基準'
            }, {
              value: 'func_2_02_Route.xlsm-2.2.2.1.1.別ルート',
              label: 'func_2_02_Route.xlsm-2.2.2.1.1.別ルート'
            },],
            get_data:"",
            save_data:"",
            dbrfmFlag:false
        }
    },
    destroyed() {
        // window.sessionStorage.remove('Project_id')
    },
    computed: {
        doc_id(val) {
            return this.$store.state.doc_id
        }
    },
    watch:{
        input_spec(val,cb){
            // console.log(val,cb)
            if(this.input_spec!=""){
                // this.SearchSpec(val,cb)
                this.SearchSpec2(val)
            }else{
                this.getSpec2()
            }
        }
    },
    mounted() {
        this.getSpec2()
        this.reqSaveStepOneData();
        var self = this
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
        clear_input(){
            if(this.input_spec!=""){
                this.SearchSpec2(this.input_spec)
            }else{
                this.getSpec2()
            }
            this.spec_list_flag=true
            // this.input_spec = ""
            
        },
        LinkURL(data){
            // console.log(data)
            window.open(data.url)

        },
        loose_focus(){
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
              this.spec_list_flag=false;
            }, 250);
            
        },
        SearchSpec2(val){
            // console.log(111,val,window.sessionStorage.getItem('Project_id'))
            this.$axios.get(this.Ip+"/Specification/"+ window.sessionStorage.getItem('Project_id') +"/"+val).then(res=>{
                // console.log(res,"....")
                if(res.data.result="OK"){
                    // console.log(res,"....")
                    this.options=res.data.content
                    for(var i=0;i<this.stepOneData.FUNC.length;i++){
                        for(var j=0;j<this.options.length;j++){
                            if(this.stepOneData.FUNC[i].spec_id==this.options[j].spec_id){
                                // console.log(this.options[j],"sps")
                                this.options[j].select = true
                            }
                        }
                    }  
                }
            })
            
        },
        getSpec2(){
            this.$axios.get(this.Ip+"/Specification").then(res=>{
                if(res.data.result="OK"){
                    // console.log(res,"sp")
                    this.options=res.data.content
                    for(var i=0;i<this.stepOneData.FUNC.length;i++){
                        for(var j=0;j<this.options.length;j++){
                            if(this.stepOneData.FUNC[i].spec_id==this.options[j].spec_id){
                                // console.log(this.options[j],"sps")
                                this.options[j].select = true
                            }
                        }
                    }
                }
            })
        },
        SearchSpec(val,cb){
            this.$axios.get(this.Ip+"/Specification/"+1+"/"+val).then(res=>{
                // console.log(res,"....")
                if(res.data.result="OK"){
                    // console.log(res,"....")
                    this.options=res.data.content
                    cb(this.options)
                }
            })
            
        },
        getSpec(cb){
            this.$axios.get(this.Ip+"/Specification").then(res=>{
                if(res.data.result="OK"){
                    // console.log(res,"sp")
                    this.options=res.data.content
                    cb(this.options)  
                }
            })
        },
        querySearch(queryString, cb) {
            // console.log(queryString,"cb")
            if(queryString!=""){
                this.SearchSpec(queryString,cb)
            }else{
                this.getSpec(cb)
            }
        },
        handleSelect(item) {
            var double_flag = false;
            for(var i=0;i<this.stepOneData.FUNC.length;i++){
                if(item.spec_id==this.stepOneData.FUNC[i].spec_id){
                    // this.$alert("您已添加过该式样书","提示")
                    double_flag = true;
                }
            }
            if(double_flag){
                this.$alert("您已添加过该式样书","提示")
            }else{
                this.stepOneData.FUNC.unshift(item)
            }
            
            
        },
        reqSaveStepOneData(){
            this.$axios.get(this.Ip + '/ApiDSDocSpec/' + window.sessionStorage.getItem('DocId'))
            .then(res => {
                this.stepOneData.micro_ver = res.data.micro_ver
                if(res.data.result=="OK"){
                    this.stepOneData.FUNC = res.data.content
                    this.get_data = JSON.stringify(res.data.content)
                }else{
                    this.get_data = '[]'
                }
            })
            .catch(err => {console.log('======')})
        },
        look_input(row){
            console.log(row.url)
            console.log(row)
        },
        delete_input(row,index){
            // this.select_list.splice(index,1)
            this.stepOneData.FUNC.splice(index,1)
        },
        prev(){
            if (this.dbrfmFlag == true) {
                this.$router.push({path:'/tagl/edit_summery',query:{params:this.dbrfmFlag}})
            } else {
                this.$router.push({path:'/tagl/edit_detail_summary',query:{params:this.dbrfmFlag}})                                
            }
          },
        JumpAndSave(router){
          this.stepOneData.doc_id = window.sessionStorage.getItem('DocId')
          this.save_data = JSON.stringify(this.stepOneData.FUNC)
          var path={path:router,query:{params:this.dbrfmFlag}}
          if(this.save_data == this.get_data){
               this.$router.push(path)
          }else{
            this.$confirm(this.globalData.hint.jump, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$axios.post(this.Ip + '/ApiDSDocSpec', this.stepOneData).then(res => {
                    if (res.data.result == 'OK') {
                        this.$router.push(router)
                        this.$message({
                            showClose: true,
                            message: '保存成功',
                            type: 'success'
                            }) 
                    }else{
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
        cancel(){
            this.save_data = JSON.stringify(this.stepOneData.FUNC)
            if(this.save_data == this.get_data){
                window.sessionStorage.removeItem('stepTwoSecId')
                window.sessionStorage.removeItem('Step-Asa') 
                this.$router.push('/tagl/File_design/Preview/'+window.sessionStorage.getItem('DocId'))
            }else{
               this.$confirm(this.globalData.hint.quit, '提示', {
                   confirmButtonText: '确定',
                   cancelButtonText: '取消',
                   type: 'warning'
               })
               .then(() => {
                   window.sessionStorage.removeItem('stepTwoSecId')
                   window.sessionStorage.removeItem('Step-Asa')  
                   this.$router.push('/tagl/File_design/Preview/'+window.sessionStorage.getItem('DocId'))
               })
               .catch(() => {}) 
            }
        },
        next () {
            this.stepOneData.doc_id = window.sessionStorage.getItem('DocId')
            this.$axios.post(this.Ip + '/ApiDSDocSpec', this.stepOneData).then(res => {
                if (res.data.result == 'OK') {
                    if (Number(window.sessionStorage.getItem('Step-Asa')) == 1) {
                        window.sessionStorage.setItem("Step-Asa", 2)
                    }
                    this.$router.push({path:"/tagl/edit_usecase",query:{params:this.dbrfmFlag}})
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
        save () {
            // if (this.userPurviewManage('设计书_添加') == true) {
                this.stepOneData.doc_id = window.sessionStorage.getItem('DocId')
                this.$axios.post(this.Ip + '/ApiDSDocSpec', this.stepOneData).then(res => {
                    if (res.data.result == 'OK') {
                        this.reqSaveStepOneData()
                        this.$message({
                            showClose: true,
                            message: '保存成功',
                            type: 'success'
                        })
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
            // } else {
            //     this.$message({
            //         type: "warning",
            //         message: "您没有操作权限！"
            //     })
            // }
        },
        jump_to(index){
            switch(index){
                case "基本设计":
                    this.JumpAndSave('/tagl/edit_summery')
                    break;
                case "Usecase":
                    this.JumpAndSave('/tagl/edit_usecase')
                    break;
              }
        },
    }
}
</script>

<style scoped>
#basic-degign-step-one {
    /* background-color: bisque; */
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
        border-right: 1px solid #c0c4cc;
}
.header-top{
    height: 100px;
}
.header{
    height: 225px;
    padding:10%;
    clear: both;
}
.cbody{
    float: left;
    height: 100%;
    width: 84%;
    padding-left:1%;
}

.step-one-title {
    margin:40px 0 20px 0;
}
.step-one-text{
    margin-left: 80px;
}
.checked-input-list{
    margin-left: 20px;
    margin-top:100px;
    float: left;
    width: 100%;
    height: 400px;
}
.checked-input-list-title{
    margin-bottom: 15px;
    font-size: 16px;
}
.checked-input-list-li{
    list-style: none;
    width: 100%;
    line-height:30px;
    cursor: pointer;
    font-size: 14px;

}
.mid{
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
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
h2{
    font-size: 22px;
    font-weight:bolder;
    background-color: #6bcca0;
    color: white;
    padding-left: 10px;
    line-height: 25px;
    height: 25px;
    width: 100%
}
.footer{
    position: absolute;
    bottom:20px;
    right: 20px;
}
.right{
    width: 20%;
    height: 100%;
    float: left;
}
.step-one-content {
    margin-top:20px;
    margin-left: 20px;  
}
.select-input{
    width: 50%;
}
.select-content{
    position: relative;
    margin-top: 20px;
}
.select-option-box{
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
.select-option-li{
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
.select-option-li:hover{
    cursor: pointer;
    background-color: #f5f7fa;
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
    .checked-input-list{
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
  .cbody{     
    float: left;
    width: 80%;
    height: 100%;
    }
    .step-one-content {
    }
}
@media screen and (max-width: 1024px) {
    #basic-degign-step-one {
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
    .cbody{
        float: left;
        width: 820px;
        height: 100%;
    }
    .mid{
        width: 635px;
    }
    .step-one-content{
        margin-left: 20px;
    }
    .checked-input-list{
        margin-left: 20px;
        float: left;
        height: 400px;
    }
  }
</style>
