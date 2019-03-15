<template>
  <div>
    <div class="leftCheck">
      <div>
          <h4 class="leftCheck-title" @click="hidden_and_show(1)">■ 式样书：</h4>
          <ul class="leftCheck-content">
            <li v-for="item in showTreeData.one" @click="LinkURL(item)" :key="item.spec_id" :title='item.title'>
              {{item.title}}
            </li>
          </ul>
      </div>
      <div>
          <h4 class="leftCheck-title" @click="hidden_and_show(2)">■ 场景：</h4>
          <ul style="cursor:default" class="leftCheck-title-ex leftCheck-content" >
            <li v-for="item in showTreeData.scene" :key="item.key" :title='item' style="cursor:default">
              {{item}}
            </li>
          </ul>
      </div>
      <div v-show="show_flag">
          <h4 class="leftCheck-title" @click="hidden_and_show(3)">■ 关联技术文档：</h4>
          <ul class="leftCheck-content" >
            <li v-for="item in docListData" :key="item.doc_id">
              <span @click="go_doc_text(item.doc_id)" :title="item.doc_title">{{item.doc_title}}</span>
            </li>
            <!-- <li>
              <span @click="go_doc_text(338)">资源泄露防止对策</span>
            </li>
            <li>
              <span @click="go_doc_text(382)">BackupMemory使用说明</span>
            </li> -->
          </ul>
      </div>
      <div>
            <h4 class="leftCheck-title" @click="hidden_and_show(4)">■ BugList：</h4>
            <ul class="leftCheck-content" >
                <li v-for="item in bugListData" :key="item.doc_id">
                    <span @click="go_doc_text(item.doc_id)" :title="item.doc_title">{{item.doc_title}}</span>
                </li>
            </ul>
      </div>
    </div>
    <!-- <div class="left-box">
      <i class="el-icon-d-arrow-left" @click='left_leftCheck()'></i>
    </div> -->
  </div>
    
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
  data() {
    return {
     showTreeData:{
       one:[],
       scene:[]
     },
     show_flag:false,
     docListData:[],
     bugListData:[]   
    };
  },
  mounted(){
    this.showTree()
  },
  methods: {
    hidden_and_show(index){
      switch (index){
        case 1:
          if($('.leftCheck-content').eq(0).css("display")=="none"){
            $('.leftCheck-content').eq(0).css({display:"block"})
          }else{
            $('.leftCheck-content').eq(0).css({display:"none"})
          }
          break;
        case 2:
          if($('.leftCheck-content').eq(1).css("display")=="none"){
            $('.leftCheck-content').eq(1).css({display:"block"})
          }else{
            $('.leftCheck-content').eq(1).css({display:"none"})
          }
          break;
        case 3:
          if($('.leftCheck-content').eq(2).css("display")=="none"){
            $('.leftCheck-content').eq(2).css({display:"block"})
          }else{
            $('.leftCheck-content').eq(2).css({display:"none"})
          }
          break;
        case 4:
          if($('.leftCheck-content').eq(3).css("display")=="none"){
            $('.leftCheck-content').eq(3).css({display:"block"})
          }else{
            $('.leftCheck-content').eq(3).css({display:"none"})
          }
          break;  
      }
    },
    LinkURL(data){
        // console.log(data)
        window.open(data.url)
    },
    getBuglist(){
        let sec_id = window.sessionStorage.getItem('stepTwoSecId')
        this.$axios.get(this.Ip + "/KnowledgeDoc/" + sec_id).then(res=>{
            // console.log(res,"res")
            if (res.data.result == "OK") {
                this.bugListData=res.data.content.bug_list
                this.docListData=res.data.content.knowledge_docs
            } else {
                this.bugListData = []
                this.docListData = []
            }
        })
    },
    showTree(){
      this.showTreeData.scene = []
      this.showTreeData.one = []
      this.show_flag = false
      this.$axios.get(this.Ip + '/Section/' + window.sessionStorage.getItem('stepTwoSecId') + '/SCENES')
          .then(res => {
              if (res.data.result == 'OK') {
                  for (let i_data of res.data.content) {
                      this.showTreeData.scene.push(i_data.scene)
                      this.show_flag = true
                      this.getBuglist()
                  }
              }
          })
      this.$axios.get(this.Ip + '/Section/' + window.sessionStorage.getItem('stepTwoSecId') + '/SPEC')
      .then(res => {
          if (res.data.result == 'OK') {
              for (let i_data of res.data.content) {
                  this.showTreeData.one.push(i_data)

              }
          }
      })
    },
    go_doc_text(val){
        var datas = {};
        datas.doc_id = val;
        let data = {
                'data':datas,
                'server_ip':this.Ip
            }
        window.sessionStorage.setItem("listDocID",JSON.stringify(data));
        window.open("../../../static/DocList-item.html") ;
    },
    right_amt(){
      $('.leftCheck').animate({right:-400},500,function(){
        $('.leftCheck').hide()
        $('.left-box').show()
      })
    },
    left_leftCheck(){
       $('.leftCheck').show()
        $('.left-box').hide()
      $('.leftCheck').animate({right:0},500,function(){
       
      })
    }
  }
};
</script>

<style scoped>
.leftCheck{
  position: relative;
  background-color: white;
  font-size: 14px;
  padding: 10px;
  width: 280px;
  top: 20px;
  overflow-y: scroll;
}

  .leftCheck ul li{
    list-style: none;
    margin-top: 5px;
    margin-left: 20px;
    color: #000;
    width: 200px;
    font-size: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear;
    padding-left: 5px;
    padding-bottom: 5px;
    cursor: pointer;
  }
  .leftCheck ul li:hover{
    background: #6bcca0
  }
  .leftCheck-title:hover{
      background: #6bcca0
  }
  .leftCheck .leftCheck-title-ex li:hover{
    background:white
  }
  .leftCheck-title{
    font-weight: 500;
    margin-top: 5px;
    font-size: 14px;
  }
  .leftCheck-title:hover{
    cursor: pointer;
  }
  .left-box{
    display: none;
    font-size: 28px;
    line-height: 50px;
    text-align: center;
    width: 50px;
    height: 50px;
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear; 
    cursor: pointer;
    border-radius: 50%;
  }
  .left-box:hover{
    color: #67c23a ;
    box-shadow:2px 9px 16px 0px rgba(242, 239, 255, 1); 
  }
</style>
