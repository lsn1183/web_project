<template>
  <div id="my-work" class="wrapper">
    <div id="my-tree" class="main-left" onselectstart="return false">
      <el-tree v-loading="loading"  :data="tree_data" :expand-on-click-node="false" :default-expanded-keys='expandedKeys' :props="defaultProps" ref="tree2" @node-click="node_click" :highlight-current='true' node-key="openNumId" :indent='14'>
        <span class="custom-tree-node" slot-scope="{node,data}" :title="data.tag+'('+data.num+')'">
          <span class="tree_label">{{data.tag}}</span>
          <span v-if="data.num">({{data.num}})</span>
        </span>
      </el-tree>
      <div class="nav-bar" title="左右拖动">
        <i class="el-icon-arrow-right"></i>
    </div>
    </div>
    <div class="my-work-view">
      <router-view :tag_name = 'work_tag_name' @receiveAction="responseAction"></router-view>
    </div>
  </div>
</template>
<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    data() {
        return {
            data: [],
            defaultProps: { label: 'tag', children: 'sub_tags' },
            workType: '',
            filterText: '',
            tableData_countAll: '',
            tableData_countMy: '',
            tree_data: [],
            showAll_flag: false,
            showMy_flag: false,
            page: 1,
            page_size: 20,
            user_name: window.sessionStorage.getItem('Uall'),
            work_tag_name: '',
            expandedKeys: [],
            loading:true,
        }
    },
    mounted() {
        // main left tree:
        this.Get_TAG_data()
        // 拖动左边box
        this.move_left_box()
    },
    methods: {
        //相应右边树改变的刷新函数
        responseAction() {
            this.Get_TAG_data()
        },
        // 点击左边那棵树事件：
        node_click(data) {
            // console.log(data)
            if (!data.type) {
                return
            }
            if (data.type == "knowledge" || data.type == "技术文档" ) {//线程
                //点击线程
                this.work_tag_name = '线程'
                this.$router.push('/tagl/Doc_Exhibition')
            } else if (data.type == "failure_mode") {
                this.$store.state.text_type = data
                this.$router.push({path:'/tagl/Form_Modle',query:{type:data.type}})
            } else if(data.type === "manage"){
                //点击知识库管理跳转管理页面
                this.$router.push('/tagl/TAGLStauts')
            }else if(data.type === "all" || data.type === "tag"){//知识点列表
                window.sessionStorage.setItem('tag_id', JSON.stringify(data.tag_id));
                this.$store.state.text_type = data.tag_id
                this.$router.push({path:'/tagl/Form_Modle',query:{params:data.tag_id}})
            }
        },
        Get_TAG_data() {
            this.$axios.get(this.Ip + '/TagTreeIncludeNumber/' + sessionStorage.getItem('user_id')).then(res => {
                if (res.data.result == 'OK') {
                    let data = res.data.content
                    let index = 0
                    for (const getItem of data) {
                        for (const iterator of getItem.sub_tags) {
                            // 赋值一个id用于默认展开
                            iterator.openNumId = index++
                            // 树展开节点的数组
                            this.expandedKeys.push(iterator.openNumId)
                            for (const item of iterator.sub_tags) {
                                if (item.tag == '知识点分类') {
                                    item.openNumId = iterator.openNumId * 10
                                    this.expandedKeys.push(item.openNumId)
                                }
                            }
                        }
                    }
                    this.tree_data = data
                    this.loading=false
                } else {
                    this.this.tree_data = []
                }
            })
        },
        count_click() {
            this.$router.push('/tagl/Form_Modle/' + 'Count')
        },
        // 拖动左边框
        move_left_box(){
            var self = this
            $('.nav-bar').mousedown(function(event) {
                $('#my-work').mousemove(function(event) {
                    if (document.body.clientWidth <= 1138) {
                        if ($('#my-tree').width() <= 178) {
                            $('#my-tree').css({ width: 195 + 'px' })
                            $('.nav-bar').css({left: 195 +'px'})
                            $('#my-work').unbind('mousemove')
                        }else if($('#my-tree').width() > document.body.clientWidth*0.85){
                            $('#my-tree').css({ "width": document.body.clientWidth*0.85 + "px" })
                            $('.nav-bar').css({left: document.body.clientWidth*0.85 +'px'})
                            $('#my-work').unbind('mousemove')
                        }  else {
                            $('#my-tree').css({ width: event.clientX  + 'px' })
                            // $('#nav-bar').position().left = event.clientX + 23 +'px'
                            $('.nav-bar').css({left: event.clientX +'px'})
                        }
                    } else if (document.body.clientWidth > 1138 && document.body.clientWidth <= 1498) {
                        // var mid_width =
                        if ($('#my-tree').width() <= 200) {
                            $('#my-tree').css({ width: 215 + 'px' })
                            $('.nav-bar').css({left: 215 +'px'})
                            $('#my-work').unbind('mousemove')
                        }else if($('#my-tree').width() > document.body.clientWidth*0.85){
                            $('#my-tree').css({ "width": document.body.clientWidth*0.85 + "px" })
                            $('.nav-bar').css({left: document.body.clientWidth*0.85 +'px'})
                            $('#my-work').unbind('mousemove')
                        } else {
                            $('#my-tree').css({ width: event.clientX  + 'px' })
                            // $('.nav-bar').position().left = event.clientX + 23 +'px'
                            // console.log()
                            $('.nav-bar').css({left: event.clientX +'px'})
                            
                        }
                    } else if (document.body.clientWidth <= 2133) {
                        if ($('#my-tree').width() <= 235) {
                            $('#my-tree').css({ width: 249 + 'px' })
                            $('.nav-bar').css({left: 249 +'px'})
                            $('#my-work').unbind('mousemove')
                        }else if($('#my-tree').width() > document.body.clientWidth*0.85){
                            $('#my-tree').css({ "width": document.body.clientWidth*0.85 + "px" })
                            $('.nav-bar').css({left: document.body.clientWidth*0.85 +'px'})
                            $('#my-work').unbind('mousemove')
                        } else {
                            $('#my-tree').css({ width: event.clientX  + 'px' })
                            // $('#nav-bar').position().left = event.clientX + 23 +'px'
                            $('.nav-bar').css({left: event.clientX +'px'})
                        }
                    }
                })
            })
            $('#my-work').mouseup(function(event) {  
                $('#my-work').unbind('mousemove')
            })
        }
    }
}
</script>

<style scoped>
*{
    margin: 0;
    padding: 0
  }
.wrapper {
    position: relative;
    width: 100%;
    height: 100%;
    max-width: 1920px;
    min-width: 1024px;
    background: white;
    overflow: hidden;
    font-family: Dosis, Source Sans Pro, Helvetica Neue, Arial, sans-serif;
    color: #606266;
}
.main-left {
    position: relative;
    top: 0;
    left: 0;
    z-index: 9;
    width: 15%;
    padding: 20px 0 0 10px;
    height: 100%;
    background-color: white;
    border-right: 2px solid rgba(216, 231, 223, 0.5);
    overflow: scroll;
    overflow-x: hidden;
}
.my-work-view {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 85%;
}

.jindu {
    padding-left: 25px;
    line-height: 26px;
}
.jindu span {
    color: #606266;
    font-size: 14px;
}

.el-tree {
    border: 0 none;
}
.main-left-tag {
    margin-top: 5px;
    font-size: 14px;
    font-weight: 400;
}

.nav-bar{
  position: fixed;
  margin-top:-15px;
  top:50%;
  /*right: 0;*/
  left: 15%;
  width: 14px;
  height: 30px;
  line-height: 30px;
  border-radius: 10px;
  background-color: #42b983;
  cursor: e-resize;
  color: white;

}
@media screen and (max-width: 1366px) {
    .wrapper {
        width: 100%;
        height: 100%;
        font-size: 12px;
    }
    .main-left {
        width: 20%;
    }
    .nav-bar{
        position: fixed;
        left: 20%;
    }
    .my-work-view {
        width: 80%;
    }
}
@media screen and (max-width: 1024px) {
    .wrapper {
        width: 100%;
        height: 100%;
        font-size: 10px;
        /* overflow-y: scroll; */
    }
    .main-left {
        float: left;
        width: 20%;
        padding: 20px 0 0 10px;
        height: 100%;
        overflow: scroll;
    }
    .nav-bar{
        position: fixed;
        left: 20%;
    }
    .my-work-view {
        float: left;
        width: 80%;
        height: 100%;
        border-left: 2px solid rgba(216, 231, 223, 0.5);
        background-color: white;
    }
}
</style>
