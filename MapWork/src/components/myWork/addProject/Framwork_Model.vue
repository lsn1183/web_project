<template>
    <div class="add-project-step">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="平台信息">1</el-step>
                    <el-step class="jump" title="模块" icon="el-icon-edit" status="process">2</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Mode">
            <div class="mid">
                <div class="mid-top">
                    <div class="step-one-title">
                        <h2 style="font-size: 22px;font-weight:bolder;background-color: #6bcca0; color: white;padding-left: 10px;line-height: 25px;width: 100%">模块关系
                            <i class="el-icon-question" style="font-size: 15px;" title="请提供和Usecase相关的式样书，式样书可以是要求式样书、机能式样书、操作式样书等"></i>
                        </h2>
                    </div>
                    <div style="font-size: 16px;margin-bottom: 10px;">
                    </div>
                    <div class="two-box">
                        <el-tree :data="FW_Model.model_tree" node-key="id" :props="defaultProps" default-expand-all :expand-on-click-node="false">
                            <span class="custom-tree-node" slot-scope="{ node, data }">
                                <span>{{ node.label }}</span>
                                <span>
                                    <el-popover  placement="left" width="300" v-model="data.key">
                                        <p>选择一个模块？</p>
                                        <div class="select-content" style="text-align: center; margin: 0">

                                            <el-input placeholder="请输入内容" class="select-input" clearable v-model="input_spec" @focus="clear_input" @blur="loose_focus">
                                            </el-input>
                                            <div v-show="spec_list_flag==true" class="select-option-box" >
                                                <ul v-for="(item,index) in options">
                                                    <li v-if="item.select"  :title="item.summary" class="select-option-li" style="color: #42b983" @click="handleSelect(node,item,data)">
                                                        {{item.title}}
                                                    </li>
                                                    <li v-else :title="item.summary" class="select-option-li" @click="handleSelect(node,item,data)">
                                                        {{item.title}}
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                        <el-button type="text" size="mini"  slot="reference" @click="append_node(data)">添加</el-button>
                                    </el-popover>
                                    <el-button type="text" size="mini" @click="delete_node(node,data)">删除</el-button>
                                   <!--  <el-button type="text" size="mini" @click="append_node(node,data)" @blur="hidden_box">添加</el-button>
                                    <el-button type="text" size="mini" >删除</el-button> -->
                                </span>
                            </span>
                        </el-tree>
                    </div>
                    <!-- <div v-show="append_box_flag" class="append-box">
                        <p>选择一个模块？</p>
                        <div class="select-content" style="text-align: center; margin: 0">
                            <el-input placeholder="请输入内容" class="select-input" clearable v-model="input_spec" @focus="clear_input" @blur="loose_focus">
                            </el-input>
                            <div v-show="spec_list_flag==true" class="select-option-box" >
                                <ul v-for="(item,index) in options">
                                    <li :title="item.summary" class="select-option-li" @click="handleSelect(node.key,item,data)">
                                        {{item.title}}
                                    </li>
                                </ul>
                                
                            </div>
                        </div>
                    </div> -->
                        
                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="prev()"><i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button @click="save()" type="primary" size='mini'>&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button @click="cancel()" type="primary" size='mini'>&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button @click="next()" type="primary" size='mini'>&nbsp;&nbsp;完&nbsp;&nbsp;&nbsp;成&nbsp;&nbsp;</el-button>
                    <!-- <el-button size="mini" type="info" disabled >下一步<i class="el-icon-arrow-right"></i></el-button>   -->
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
            FW_Model: {
                fw_id: 0,
                fw_name:'',
                type:"FW_MODEL",
                // user_name:window.sessionStorage.getItem('Uall'),
                model_tree: []
            },
            defaultProps: {
                children: 'model_sub',
                label: 'title',
                id:'model_id',
                key:'key',

            },
            append_box_flag:false,
            repeatList:[],

            OptionsTagList: [],
            active:Number(window.sessionStorage.getItem('fw_step_id')),
            spec_list_flag:false,
            input_spec:"",
            select_list:[],
            options: [],
            getData:{},
            saveData:{},
            get_data:"",
            save_data:"",
        }
    },
    // created() {
    //     this.judgeAll()
    // },
    watch:{
        input_spec(val){
            if(this.input_spec!=""){
                // this.SearchSpec(val,cb)
                this.SearchSpec2(val)
            }else{
                this.getSpec2()
            }
            
        }
    },
    mounted(){
        var self = this
        $('.jump').on('click', function(e) {
          self.jump_to($(this).text())
        });
        // this.judgeAll()
        this.getFW_Model()
    },
    methods: {
        getFW_Model(){
            this.$axios.get(this.Ip+"/Framework/FW_MODEL/"+Number(window.sessionStorage.getItem('fw_id'))).then(res=>{
                // console.log(res,"fwm")
                if(res.data.result=="OK"){
                    this.repeatModel(res.data.content.model_tree[0].model_sub)
                    // console.log(res.data.content.model_tree[0].model_sub,"con")
                    this.FW_Model = res.data.content
                    this.FW_Model.type = "FW_MODEL"
                    this.getData = this.FW_Model.model_tree
                    this.get_data = JSON.stringify(this.FW_Model) 
                }else{

                }
            })
        },
        repeatModel(list){
            // console.log(list,"list")
            let sublist = list
            if(sublist.length == 0){
                // console.log(this.repeatList,"lll")
                return 
            }else{
                for(var i=0;i<sublist.length;i++){
                    this.repeatList.push({model_id:sublist[i].model_id})
                    this.repeatModel(sublist[i].model_sub)
                }
                // this.repeatList.push(sublist.model_id)
                // this.repeatModel(sublist.model_sub)
            }
        },
        clear_input(){
            if(this.input_spec!=""){
                this.SearchSpec2(this.input_spec)
            }else{
                this.getSpec2()
            }
            this.spec_list_flag=true
            // this.input_spec = ""
            
        },
        loose_focus(){
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
              this.spec_list_flag=false;
            }, 250);
            
        },
        SearchSpec2(val){
            this.$axios.get(this.Ip+"/ModelQuery/"+val).then(res=>{
                // console.log(res,"....")
                if(res.data.result=="OK"){
                    // console.log(res,"....")
                    this.options=res.data.content
                    if(this.repeatList.length!=0){
                        for(var i=0;i<this.repeatList.length;i++){
                            for(var j=0;j<this.options.length;j++){
                                if(this.repeatList[i].model_id == this.options[j].model_id){
                                    // console.log(this.options[j],"sps")
                                    this.options[j].select = true
                                }
                            }
                        } 
                    }       
                }else{
                    this.options = []
                }
            }).catch(res=>{
                this.$message({
                    showClose: true,
                    message: '服务异常',
                    type: 'error',
                    duration:0,
                })
            })
        },
        getSpec2(){
            this.$axios.get(this.Ip+"/Model").then(res=>{
                if(res.data.result=="OK"){
                    // console.log(res,"sp")
                    this.options=res.data.content
                    for(var i=0;i<this.repeatList.length;i++){
                        for(var j=0;j<this.options.length;j++){
                            if(this.repeatList[i].model_id==this.options[j].model_id){
                                // console.log(this.options[j],"sps")
                                this.options[j].select = true
                            }
                        }
                    }  
                }else{
                    this.options = []
                }
            }).catch(res=>{
                this.$message({
                    showClose: true,
                    message: '服务异常',
                    type: 'error',
                    duration:0,
                })
            });
        },
        handleSelect(node,item,data){
            // console.log(node.key1,"key")
            var double_flag = false;
            for(var i=0;i<this.repeatList.length;i++){
                if(item.model_id==this.repeatList[i].model_id){
                    // this.$alert("您已添加过该式样书","提示")
                    double_flag = true;
                }
            }
            if(double_flag){
                this.$alert("该模块已被添加","提示")
            }else{
                this.append(node,item,data)
                this.repeatList.push({model_id:item.model_id})
            }
            
            data.key = false;
        },
        append(node,item,data){
            const newChild = { model_id: item.model_id, title: item.title, model_sub: [] ,key:false};
            if (!data.model_sub) {
              this.$set(data, 'model_sub', []);
            }
            data.model_sub.push(newChild);
            
        },

        delete_node(node,data){
            // console.log(node,"de")
            const parent = node.parent;
            // console.log(parent,"pde")
            if(parent.parent!=null){
                const model_sub = parent.data.model_sub || parent.data;
                // console.log(model_sub,"me")
                const index = model_sub.findIndex(d => d.model_id === data.model_id);
                model_sub.splice(index, 1);
                var rep_index = this.repeatList.indexOf(data.model_id)
                // console.log(rep_index,"chs")
                this.repeatList.splice(rep_index,1)
                console.log(this.repeatList,"ch")
            }else{
                this.$alert("该模块已是顶级,不能删除","提示")
            }
            
                
        },
        append_node(data){
            var falg =this.repeaKey(this.FW_Model.model_tree)
            if(falg){
                data.key = true
            }
            
        },
        repeaKey(list){
            // console.log(list,"list")
            let sublist = list
            if(sublist.length == 0){
                return true
            }else{
                for(var i=0;i<sublist.length;i++){
                    if(sublist[i].key==true){
                        sublist[i].key=false
                    }
                    this.repeaKey(sublist[i].model_sub)
                }
            }
        },
        change_node_key1(id,node){
            if(node.key1==true){
                node.key1 = false
            }
        },
        JumpAndSave(router){
            this.save_data = this.FW_Model.model_tree
            console.log(this.save_data,"s")
            if(this.save_data == this.get_data){
                this.$router.push(router) 
            }else{
                this.$confirm('页面信息已发生变更, 是否跳转?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.FW_Model.proj_id = window.sessionStorage.getItem('proj_id')
                    this.$axios.post(this.Ip + '/Framework', this.FW_Model)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.$router.push(router) 
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
                }).catch(()=>{})

                    
            }
        },
        // hidden_box(){
        //     this.append_box_flag= false
        // },
        prev() {
            let routerPath={path:'/tagl/FramworkSummary',query:{flag:"false"}}
            this.$router.push(routerPath)
        },
        jump_to(index){
            switch(index){
                case "平台信息":
                  // this.JumpAndSave('/tagl/FramworkSummary')
                  this.$router.push('/tagl/FramworkSummary')
                  break;
                case "模块":
                  // this.JumpAndSave('/tagl/Framwork_Model')
                  this.$router.push('/tagl/Framwork_Model')
                  break;
                // case "1平台信息":
                //   // this.JumpAndSave('/tagl/FramworkSummary')
                //   this.$router.push('/tagl/FramworkSummary')
                //   break;
              }
        },
        save() {
            if (this.FW_Model.model_tree.length == 0) {
                this.$message({
                    message: '请选择模块',
                    type: 'error'
                })
                return
            }
            this.FW_Model.proj_id = window.sessionStorage.getItem('proj_id')
            this.$axios.post(this.Ip + '/Framework', this.FW_Model)
            .then(res => {
                if (res.data.result == 'OK') {
                    this.getFW_Model()
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
            if (this.FW_Model.model_tree.length == 0) {
                this.$message({
                    message: '请选择模块',
                    type: 'error'
                })
                return
            }
            this.FW_Model.proj_id = window.sessionStorage.getItem('proj_id')
            this.$axios.post(this.Ip + '/Framework', this.FW_Model)
            .then(res => {
                if (res.data.result == 'OK') {
                    this.$store.state.fpm_id = 0
                    this.$router.push('/tagl/Add_NewProject/FramworkTemplate')
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
            this.save_data = JSON.stringify(this.FW_Model)
            if (this.save_data == this.get_data) {
                window.sessionStorage.removeItem('fw_id')
                window.sessionStorage.removeItem('fw_step_id')
                this.$store.state.fpm_id = 0
                this.$router.push('/tagl/Add_NewProject/FramworkTemplate')
            }else{
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                .then(() => {
                    window.sessionStorage.removeItem('fw_id')
                    window.sessionStorage.removeItem('fw_step_id')
                    this.$store.state.fpm_id = 0
                    this.$router.push('/tagl/Add_NewProject/FramworkTemplate')
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
    height: 200px;
}
.header{
    height: 225px;
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
    background-color: #42b983;
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
/**/
.step-one-title {
    margin:40px 0 20px 0;
}
.step-one-text{
    margin-left: 80px;
}
.step-one-content {
    margin-top:20px;
    margin-left: 20px;  
}
.select-input{
    width: 100%;
}
.sequence_title_text{
  margin-left: 20px;
  margin-bottom: 20px;
  font-size: 14px;
  color: #5e6d82
}
.select-content{
    position: relative;
    margin-top: 20px;
}
.select-option-box{
    /*position: absolute;*/
    background-color: white;
    z-index: 5;
    margin-top:10px;
    width: 100%;
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
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}
.append-box{
    width: 500px;
    height: 200px;
    float: left;
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
        height: 100px;
    }
    .header{
        height: 225px;
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