<template>
  <div id="technical-doc">
      <div style="padding-top:20px;padding-right:20px;">
        <i class="el-icon-more" style="float:right;fontSize:24px" v-popover:parent_info_pop></i>
          <el-popover placement="bottom" width="200" ref='parent_info_pop' trigger="hover">
              <p class="nav-select-size" @click="addBasic">添加基本设计</p>
          </el-popover>
      </div>
      <div class="technical-doc-aside">
       <h3 class="doc">模块技术文档</h3>
       <el-tree
            :data="treeDataTwo"
            :props="defaultProps"
            node-key="id"
            default-expand-all
            @node-click="handleNodeClick"
            :expand-on-click-node="false">
        </el-tree>
       <h3 class="doc">基本设计技术文档</h3>
       <el-tree
            :data="treeDataOne"
            :props="defaultProps"
            node-key="id"
            default-expand-all
            @node-click="handleNodeClick"
            :expand-on-click-node="false">
        </el-tree>
      </div>
      <div class="technical-doc-content">
        
      </div>      
  </div>
</template>

<script>
export default {
    name: 'TechnicalDoc',
    data() {
        return {
            treeDataOne: [],
            treeDataTwo: [],
            defaultProps: {
                children: 'sub_tags',
                label: 'tag'
            }
        }
    },
    methods: {
        reqTechnicalDocTreeData() {
            this.$axios
                .get(this.Ip + '/ModelTag/1')
                .then(res => {
                    this.treeDataOne = res.data.content
                })
                .catch(err => {})
            this.$axios
                .get(this.Ip + '/ModelDSDocTag/1/BASIC')
                .then(res => {
                    this.treeDataTwo = res.data.content
                })
                .catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error'
                    })
                })
        },
        handleNodeClick(node, data) {
            console.log(node.tag)
        },
        addBasic() {
            this.$emit('addBasicFun')
        }
    },
    created() {
        this.reqTechnicalDocTreeData()
    }
}
</script>

<style scoped>
#technical-doc {
    height: 100%;
}
.technical-doc-aside {
    float: left;
    width: 250px;
    height: 100%;
    padding-left: 10px;
    padding-top: 20px;
    overflow: scroll;
}
.technical-doc-content {
    overflow-y: scroll;
    height: 100%;
    padding-top: 20px;
    /* background-color: silver; */
}
.doc {
    margin-bottom: 8px;
}
.nav-select-size:hover {
    background: #2ee08f;
}
/* .el-tree>.el-tree-node>.el-tree-node__content>span {
    color:black;
    font-family:"微软雅黑", "宋体", "黑体", Arial;
    font-size: 16px;
    font-weight: bold;
}
.el-tree>.el-tree-node>.el-tree-node__content>span:before{
    content: none
}
.el-tree>.el-tree-node:focus>.el-tree-node__content{
   background-color: white!important;
} */
</style>
