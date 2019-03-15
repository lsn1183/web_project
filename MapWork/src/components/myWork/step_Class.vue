<template>
  <div class='Append-basic-temlate'>
    <div class="Append-basic-temlate-countent">
      <div class="header-top">
      </div>
      <div class="header">
      </div>
    </div>
    <div class="content-box">
      <div class="mid">
        <div class="mid-top">
          <div class="block-title">
            <h2>Class
            <!-- <i class="el-icon-question" style="font-size: 15px;" title="选择block图"></i> -->
            <i class="el-icon-question" title='请提供描述Class图的文字说明以及Class图' style="font-size:15px;height:20px;vertical-align:middle"></i>
          </h2>
          </div>
          <div class="content-box-deep">
            <div class="label-box" v-for='(item,index) in Class.content'>
             <!--  <div class="label-box-text">
                Class名称
              </div>
              <el-input class='textarea-name' placeholder="请输入Class图的名称" v-model="item.content[0].title">
              </el-input> -->
              <div class="label-box-text">
                Class说明
              </div>
              <el-input class='textarea-name' type="textarea" :autosize="{ minRows: 3, maxRows: 16}" placeholder="请输入Class图的描述说明" v-model="item.content[0].val">
              </el-input>
              <p class="label-box-image" style="color:#333;margin:20px 0;fontSize:18px;">Class图片</p>
              <div class="img-box" v-for="(src,index_img) in item.content[0].fileList">
                <img :src="src.url" @click="img_dialog_fun(src.url)" alt="" class="Sequence-img">
                <i class="el-icon-close img_icon" style="float:right" @click='delete_img(index,index_img)'></i>
              </div>
              <div class="upload-demo-box">
                <el-upload class="upload-demo" :action='Up_Img_Ip' :on-preview="handlePreview" :before-upload="beforeUpload" :on-success='up_success' :show-file-list='false'>
                  <button @click='get_index(index)' class="up-data-btn">
                    <i class="el-icon-picture"></i>点击上传</button>
                </el-upload>
              </div>
            </div>
          </div>
        </div>
        <div style="clear: both;"></div>
        <div class="footer">
          <el-button size="mini" type="primary" @click="save()">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
          <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
          <el-button size="mini" type="primary" @click="next_step()">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
        </div>
      </div>
      <div class="right">
      </div>
      <div id="img-dialog-box">
        <el-dialog :visible.sync="dialogimgflag">
          <p class="dialog-title">
            <span><i class="el-icon-circle-plus" @click='big_img()'></i></span>
            <span>{{show_num}}%</span>
            <span><i class="el-icon-remove" @click='s_img()'></i></span>
          </p>
          <img :src="img_src" alt="原图" class="dialogimg">
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
     show_num:100,
     img_num:0,
     dialogimgflag:false,
     fileList2: [],
     append_to_body:true,
     dialogimgflag:false,
     img_src:'',
     textarea_val:"",
     active:Number(window.sessionStorage.getItem('Step')),
     Class :{
       "doc_id":window.sessionStorage.getItem("DocId"),
       "parent_sec_id": 0,
       "micro_ver":0,
       "commit_user":window.sessionStorage.getItem('Uall'),
       'sec_type':'CLASS',
       "content": [
         {
           'sec_id':0,
           'micro_ver':0,
           'title':'',
           'content':[
             {
               'fileList':[],
               'val':'',
               'checklist':{}
             }
           ],
           
         }
       ]
      },
     Up_Img_Ip:this.Ip+'/UploadImage',
     get_data: '',
     save_data: '',
    }
    
  },
  mounted() {
    // this.Class.doc_id = window.sessionStorage.getItem('DocId')
    if(this.$route.query.DocId != null){
        window.sessionStorage.setItem('DocId', this.$route.query.DocId)
        this.Class.doc_id = window.sessionStorage.getItem("DocId")
        this.up_load()
    }else{
        this.get_data =  JSON.stringify(this.Class)
    }
  },
  methods: {
    up_load(){
      this.$axios.get(this.Ip+'/Section/'+this.Class.doc_id+"/"+this.Class.sec_type)
      .then(res=>{
        if (res.data.result == "OK") {
          this.Class.content[0].content=JSON.parse(res.data.content.content[0].content)
          this.Class.content[0].micro_ver = res.data.content.content[0].micro_ver
          this.Class.micro_ver = res.data.micro_ver
          this.get_data =  JSON.stringify(this.Class)
         }else{
          this.Class.micro_ver = res.data.micro_ver
         }
      })
    },
    
    show_to_pic(url){
      this.dialogTableVisible =true
      this.img_src = url
    },
    handlePreview(file) {
      this.dialogTableVisible = true;
      this.img_src = file.url
    },
    cancel(){
      this.save_data = JSON.stringify(this.Class)
      if (this.save_data == this.get_data) {
          this.$router.push('/tagl/File_design/Preview/'+window.sessionStorage.getItem("DocId"))
          window.sessionStorage.removeItem("DocId")
      }else{
        this.$confirm(this.globalData.hint.quit, '提示', {
                  confirmButtonText: '确定',
                  cancelButtonText: '取消',
                  type: 'warning'
        })
        .then(() => {
            this.$router.push('/tagl/File_design/Preview/'+window.sessionStorage.getItem("DocId"))
            window.sessionStorage.removeItem("DocId")
        })
        .catch(() => {})
      }    
    },
    // pass(){
    //   this.$router.push('/tagl/step9')
    // },
    // 上传图片
    up_success(response, file, fileList){
      if(response.result == 'OK'){
        this.$message({
          type: 'success',
          message: '上传成功!'
        })
        console.log(response.content)
        this.Class.content[this.index].content[0].fileList.push({"name":"img","url":response.content})
      }else{
        this.$alert('图片未上传成功，请重新上传','提示')
      } 
    },
    delete_img(index,index_img){
      this.$confirm(this.globalData.hint.delete, '提示', {
         confirmButtonText: '确定',
         cancelButtonText: '取消',
         type: 'warning'
       }).then(() => {
        this.Class.content[index].content[0].fileList.splice(index_img,1)
        this.$message({
           type: 'success',
           message: '删除成功!'
         })
       })
    },
    // 添加
    append_content(){
      this.Class.content.push({'sec_id':0,'content':[{'fileList':[],'val':'',}]})

    },
    delete_content(index){
      if(index == 0){
        this.$alert('已是最后一项','提示')
      }else{
        this.$confirm(this.globalData.hint.delete, '提示', {
           confirmButtonText: '确定',
           cancelButtonText: '取消',
           type: 'warning'
         }).then(() => {

          this.Class.content.splice(index,1)

          this.$message({
             type: 'success',
             message: '删除成功!'
           })
         })
      } 
    },
    get_index(index){
      this.index = index
    },
    // 点下一步上传当前的东西
    next_step(){
    //   this.Class.doc_id = window.sessionStorage.getItem('DocId')
      if(window.sessionStorage.getItem('DocId')==null){
        this.Class.content[0].sec_id = 0 
        this.Class.parent_sec_id = 0
      }else{
        this.Class.parent_sec_id = 0
      }
      this.$axios.post(this.Ip + '/Section', this.Class).then(res => {
          if(res.data.result == 'OK'){
            // window.sessionStorage.setItem('stepTwoSecId', res.data.sec_id)
            // window.sessionStorage.setItem("Step",this.active+1)
            window.sessionStorage.removeItem("DocId")
            this.$router.push('/tagl/File_design/Preview/'+this.Class.doc_id)
          }else{
            this.$message({
                showClose: true,
                message: res.data.error,
                type: 'error',
                duration:0,
            })
          }
       })
      .catch(res=>{
        this.$message({
            showClose: true,
            message: '服务异常',
            type: 'error',
            duration:0,
        })
      })
    },
    img_dialog_fun(data){
      this.$axios.get(this.Ip+"/ImageSize/"+data).then(res=>{
        // console.log(res)
        if(res.data.result =="OK"){
          this.dialogimgflag = true;
          this.img_src = data 
          this.img_num = 0
          this.show_num = 100
          let img_width = res.data.content.long
          $('.dialogimg').width(img_width)
          
        }
      })
    },
    big_img(){
      let width_first_img = $('.dialogimg').width()*0.1
      let mum = this.img_num + 1 
      this.show_num = this.show_num + mum*10
      let img_width = $('.dialogimg').width() + mum*width_first_img
      $('.dialogimg').width(img_width)
    },
    s_img(){
      let mum = this.img_num - 1 
      if(this.show_num > 10){
        let width_first_img = $('.dialogimg').width()*0.1
        if(mum<=0){
          mum = 1
          let img_width = $('.dialogimg').width() - mum*width_first_img
          $('.dialogimg').width(img_width)
          this.show_num = this.show_num - mum*10
        }else{
          let img_width = $('.dialogimg').width() - mum*width_first_img
          $('.dialogimg').width(img_width)
          this.show_num = this.show_num + mum*10
        }
      }else{
        this.$message({
           message: '图片已缩至最小'
         })
      }
      
    },
    save(){
    //   this.Class.doc_id = window.sessionStorage.getItem('DocId')
      if(window.sessionStorage.getItem('DocId')==null){
        this.Class.content[0].sec_id = 0 
        this.Class.parent_sec_id = 0
      }else{
        this.Class.parent_sec_id = 0
      }
      this.$axios.post(this.Ip + '/Section', this.Class).then(res => {
          if(res.data.result == 'OK'){
            // this.Class.content[0].sec_id = window.sessionStorage.getItem("ClassID")
            this.up_load()
            this.$message({
              type: 'success',
              message: '保存成功!'
            })
          }else{
            this.$message({
                showClose: true,
                message: '保存失败'+res.data.error,
                type: 'error',
                duration:0,
            })
          }
       })
      .catch(res=>{
        this.$message({
            showClose: true,
            message: '服务异常',
            type: 'error',
            duration:0,
        })
      })
    }
  }
}
</script>

<style scoped>
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
    height: 100%;
    border-left: 1px solid #c0c4cc;
    overflow-y: scroll;
}
.mid{
  position: relative;
  width: 80%;
  height: 100%;
  float: left;
  padding-right: 20px;
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
.block-title {
    margin: 40px 0 20px 0;
}
h2 {
    font-size: 22px;
    font-weight: bolder;
    background-color: #6bcca0;
    color: white;
    padding-left: 10px;
    line-height: 25px;
}
.content-box-deep {
    padding-left: 20px;
}
.label-box {
    width: 98%;
    margin: 20px 0;
    overflow: hidden;
}
.label-box-text {
    margin-top: 20px;
    margin-bottom: 20px;
    font-size: 18px;
}
.upload-demo {
    margin-top: 10px;
}
.upload-demo-box {
    width: 260px;
    height: 100px;
    /*display: inline-block;*/
  }
  .add-box{
    /*line-height: 100px;*/
    height: 100px;
    width: 100px;
    padding-top: 20px;
    text-align:center;
    border:1px double #ccc;
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
  .upload-demo-box{
    width: 330px;
    height: 350px;
    vertical-align: bottom;
    display: inline-block;

  }
  .Sequence-img{
    width: 100%;
    height: 100%;
  }
  .img-box{
    width: 350px;
    height: 330px;
    margin-top: 10px;
    padding-right: 20px;
    position: relative;
    display: inline-block;
  }
  .img-box:hover{
    cursor: pointer;
    border: 1px solid transparent; 
    -moz-border-top-colors: red blue white white black; 
    -moz-border-right-colors: red blue white white black; 
    -moz-border-bottom-colors: red blue white white black; 
    -moz-border-left-colors: red blue white white black;
  }

  .img_icon{
    position: absolute;
    right:0px;
    top: 0;
    font-size: 24px;
    cursor: pointer;
  }
  .dialog_img{
    display: block;
    margin: 0 auto;
}
.dialog-title span{
  font-size: 20px;
  margin-right: 20px;
  cursor: pointer;
  color: #42b983
}
.dialog-title{
  height: 30px;
  line-height: 30px;
  width: 170px;
  margin: 0 auto;
}
.dialogimg{
  display: block;
  margin: 0 auto;
}
.textarea-name{
  font-size: 12px;
  font-family: '\5FAE\8F6F\96C5\9ED1';
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
  @media screen and (max-width:1334px) {
    .Append-basic-temlate-countent {
      max-width: 300px;
      min-width: 200px;
      width: 15%;
      height: 100%;
      padding: 20px;
      float: left;
      }
    .content-box{     
      float: left;
      width: 80%;
      height: 100%;
      overflow-y: scroll;
      /*border: 1px solid red;*/
      }
    }
  @media screen and (max-width:1024px) {
    .Append-basic-temlate{
      width: 1024px;
    }
    .header-top{
        display: none;
    }
    .Append-basic-temlate-countent {
      width: 180px;
      height: 100%;
      float: left;
      }
    .header{
        height: 100%;
        width: 180px;
        clear: both;
    }
    .content-box{
        float: left;
        width: 820px;
        height: 100%;
        overflow-y: scroll;
        /*border: 1px solid red;*/
    }
    .up-data-btn{
      width: 160px;
      height: 170px;
    }
    .upload-demo-box{
      width: 180px;
      height: 180px;
      vertical-align: bottom;
      display: inline-block;
    }
    .upload-demo{
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
