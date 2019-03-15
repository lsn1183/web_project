<template>
  <div class="file-modle-box">
    <!-- nav -->
    <div class="file-nav">
      <!-- 头部导航 -->
      <ul class="file-ul">
        <li class='file-first'>页面 / </li>
      </ul>
      <!-- 详细内容 -->
      <div class="file-content">
        <!-- 添加基本设计 -->
        <div>
          <h4 class="file-content-h4">添加 基本设计</h4>
          <el-button size='small' class='save-btn'>保存</el-button>
          <el-form ref="form" :model="append_msg" label-width="120px" class='title-msg'>
            <el-form-item label="title:">
              <el-input v-model="append_msg.title"></el-input>
            </el-form-item>
            <el-form-item label="version:">
              <el-input v-model="append_msg.ver"></el-input>
            </el-form-item>
            <el-form-item label="文档创建者：">
              <el-input v-model="append_msg.creator"></el-input>
            </el-form-item>
            <el-form-item label="最后更新人：">
              <el-input v-model="append_msg.editor"></el-input>
            </el-form-item>
          </el-form>
          <!-- 模板插入 -->
          <!-- 概述 -->
          <div class="usecase">
            <h4 class="file-content-h4">概述 ( 可选 )</h4>  
            <div class="mgleft-box">
              <el-input type="textarea" :autosize="{ minRows: 2, maxRows:10}"  placeholder="请输入内容"  v-model="append_msg.SUMMARY">
              </el-input>              
            </div>
          </div>
          <!--UseCase模板  -->
          <div class="usecase">
            <h4 class="file-content-h4">
              UseCase ( 必选 )
            </h4>  
            <div class="mgleft-box">
              <div class="append-delete">
                <el-button type='text' style='marginRight:10px' @click='appendmodel("USERCASE")'>添加</el-button>
                <el-button type='text' @click='deletemodel("USERCASE")'>删除</el-button>
                <el-button type='text'>查看Tag</el-button>
                <el-button type='text'>评论</el-button>
              </div>             
            </div>
          </div>
          <!-- Block模板 -->
          <div class="Block">
            <h4 class="file-content-h4">
              Block ( 必选 )
            </h4>
            <div class="mgleft-box">
              <div class="append-delete">
                <el-button type='text' style='marginRight:10px' @click='appendmodel("Block")'>添加</el-button>
                <el-button type='text' @click='deletemodel("Block")'>删除</el-button>
                <el-button type='text'>查看Tag</el-button>
                <el-button type='text'>评论</el-button>
              </div>           
            </div>
          </div>
          <!-- Sequence模板 -->
          <div class="Sequence">
            <h4 class="file-content-h4">
              Sequence ( 必选 )
            </h4> 
            <div class="mgleft-box" v-for='(item,index) in append_msg.SEQUENCE'>
              <div class="append-delete">
                <el-button type='text' style='marginRight:10px' @click='appendmodel("Sequence")'>添加</el-button>
                <el-button type='text' @click='deletemodel("Sequence",index)'>删除</el-button>
                <el-button type='text'>查看Tag</el-button>
                <el-button type='text'>评论</el-button>
              </div>  
              <!-- <Ttp @getSequencedata="setSequencedata"  :countent='item.content'></Ttp>         -->
            </div>
          </div>
          <!-- Resource模板 -->
          <div class="Resource">
            <h4 class="file-content-h4">
              Resource ( 必选 )
            </h4> 
            <div class="mgleft-box">
              <div class="append-delete">
                <el-button type='text' style='marginRight:10px' @click='appendmodel("Resource")'>添加</el-button>
                <el-button type='text' @click='deletemodel("Resource")'>删除</el-button>
                <el-button type='text'>查看Tag</el-button>
                <el-button type='text'>评论</el-button>
              </div>         
            </div> 
          </div>
          <!-- IF模板 -->
          <div class="IF">
            <h4 class="file-content-h4">
              I/F ( 必选 )
            </h4> 
            <div class="mgleft-box">
              <div class="append-delete">
                <el-button type='text' style='marginRight:10px' @click='appendmodel("IF")'>添加</el-button>
                <el-button type='text' @click='deletemodel("IF")'>删除</el-button>
                <el-button type='text'>查看Tag</el-button>
                <el-button type='text'>评论</el-button>
              </div>      
            </div> 
          </div>
          <!-- 状态迁移图模板 -->
          <div class="STD">
            <h4 class="file-content-h4">
              状态迁移图 ( 可选 )
            </h4>
            <div class="mgleft-box">
              <div class="append_delete">
                <el-button type='text' style='marginRight:10px' @click='appendmodel("STD")'>添加</el-button>
                <el-button type='text' @click='deletemodel("STD")'>删除</el-button>
                <el-button type='text'>查看Tag</el-button>
                <el-button type='text'>评论</el-button>
              </div>     
            </div> 
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
// import ttp from './Edit_picture_text_table';
export default {
  name: 'filemodle',
  data() {
    return { 
      content: [
      { name: '概述',content: []},
      { name: 'UseCase',content:[] },
      { name: 'block',content: []},
      { name: 'Sequence',content: []},
      { name: 'Resource',content: []},
      { name: 'I/F',content: []},
      { name: '状态迁移图',content: []}
      ],  
      append_msg:
      {
       doc_type : '',
       title : '',
       ver : '',
       model_id : 1,
       creator : '',
       editor : '',
       locked : '',
       SUMMARY : '',
       USERCASE : [{'tags': '', 'content' : []}],
       SEQUENCE : [{'tags': '', 'content' : []}],
       CLASS : [{'tags': '', 'content' : []}],
       BLOCK : [{'tags': '', 'content' : []}],
       RESOURCE : [{'tags': '', 'content' : []}],
       IF : [{'tags': '', 'content' : []}],
       STD : [{'tags': '', 'content' : []}]
     },
     basic_show_arr:[],
     doc_id:''
   };
 },
 mounted() {},
  // components: {
  //   'Ttp':ttp
  // },
  watch: {
    treeNodeType(val){

    },
    treeNodeIndex(val){
      this.doc_id = val
    }
  },
  methods: {
    //所有添加项
    appendmodel(type){
      if(type == 'USERCASE'){
        this.UseCaseappend()
      }else if(type == 'USERCASE'){

      }else if(type == 'Block'){

      }else if(type == 'Sequence'){
        this.Sequenceappend()
      }else if(type == 'Resource'){

      }else if(type == 'IF'){

      }else if(type == 'STD'){

      }
    },
    //USERCASE添加
    UseCaseappend(){    
      this.append_msg.USERCASE[0].content.push({'name':'Asa'})
    },
    //Sequence添加
    Sequenceappend(){
     this.append_msg.SEQUENCE.push({'tags': '', 'content' : []})
   },
    //Sequence监听
    setSequencedata(val){
      console.log(val,'val------------------------------')
    },
    //所有删除项
    deletemodel(type,index){
      if(type == 'USERCASE'){

      }else if(type == 'USERCASE'){

      }else if(type == 'Block'){

      }else if(type == 'Sequence'){
        this.Sequencedelete(index)
      }else if(type == 'Resource'){

      }else if(type == 'IF'){

      }else if(type == 'STD'){

      }
    },
    Sequencedelete(index){
      this.append_msg.SEQUENCE.splice(index,1)
    }
  }
};
</script>
<style scoped>
.file-modle-box {
  width: 100%;
}
.file-nav {
  width: 100%;
  height: 25px;
  line-height: 25px;
  margin-top: 10px;
}
.file-ul {
  list-style: none;
  height: 25px;
}
.file-ul .file-first {
  float: left;
  font-size: 14px;
  color: #42b983;
}
.file-content {
  height: 90%;
}

.file-content-h4 {
  font-weight:600;
  font-size: 16px; 
  margin-top: 30px;
  color: #333;
}
.title-msg{
  margin-top: 20px;
}
.mgleft-box{
  margin-left: 120px;
}
.save-btn{
  position: fixed;
  top:12%;
  right:8%;
}
.append-delete{
  float: right;
  margin-right: 10%;
}
@media screen and (max-width: 1024px) {
  .file-ul,
  .file-content {
    padding-left: 10px;
  }
}
</style>
