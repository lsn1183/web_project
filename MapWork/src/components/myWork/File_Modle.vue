<template>
	<div id="File-Modle-box" >
		<div class="tree-box">
			<div class="acs-side-bar-space-info">
				<div class="avatar">
					<div class="avatar-img-wrapper">
							<img class="model-img" src="../../assets/img/logoM.jpg" alt="Module展示空间">
					</div>
				</div>
        <div class="name">
          <a title="Module展示空间">ModuleA</a>
        </div>
			</div>
			<div class="technicalDoc">
        <!-- 技术文档 -->
        <a href="javascript:void(0);" class="noTextDecoration">
          <h3 class="doc" @click="handleDoc">技术文档</h3>
        </a>
        <!-- 基本设计Tree -->
        <h3 class="doc">基本设计</h3>
				<el-tree
        class ="tree-one"
				:data="treeData[0].children"
        node-key="id"
        :default-expanded-keys="[treeData[0].id]"
        @node-click="handleNodeClick"
				:expand-on-click-node="true">
				<span class="custom-tree-node" slot-scope="{ node, data }">
					<span>{{ node.label }}</span>
				</span>
				</el-tree>
        <!-- 详细设计Tree -->
        <h3 class="doc">详细设计</h3>
        <el-tree
        class ="tree-two"
				:data="treeData[1].children"
        node-key="id"
        :default-expanded-keys="[treeData[1].id]"
        @node-click="handleNodeClick2"
				:expand-on-click-node="true">
				<span class="custom-tree-node" slot-scope="{ node, data }">
					<span>{{ node.label }}</span>
				</span>
				</el-tree>
			</div>
		</div>
		<div class="content-box" >
			<file-modle :treeNodeIndex="nodeKeyID" v-on:getNewNodeName="appendTreeNode" :treeNodeType="nodeKeyType" v-if="this.nodeKeyType == 'ADDBASIC'?true:false"></file-modle>
      <basic-design :treeNodeIndex="nodeKeyID" :treeNodeType="nodeKeyType" v-on:getNewNodeName="appendTreeNode" v-if="this.nodeKeyType == 'BASIC' || this.nodeKeyType == 'DETAIL'?true:false"></basic-design>
      <technical-doc v-if="this.nodeKeyType == 'TechnicalDoc'?true:false" v-on:addBasicFun="editNodeKeyType"></technical-doc>
		</div>
	</div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js');
import technicalDoc from './Technical_Doc';
import filemodle from './File_Detail_template';
import basicDesign from './Basic_design';
export default {
  data() {
    return {
      nodeKeyID: '',
      nodeKeyType: '',
      treeData: [
        {
          id: 1,
          label: '基本设计',
          sub: []
        },
        {
          id: 2,
          label: '详细设计',
          sub: []
        }
      ]
    };
  },
  mounted() {
    // this.reqTreeData();
  },
  components: {
    'file-modle': filemodle,
    'basic-design': basicDesign,
    'technical-doc': technicalDoc
  },
  methods: {
    editNodeKeyType() {
      this.nodeKeyType = 'ADDBASIC'
    },
    reqTreeData() {
      this.$axios
        .get(this.Ip + '/ModelDSDoc/1')
        .then(res => {
          this.treeData = res.data.content;
        })
        .catch(err => {});
    },
    appendTreeNode(val) {
      let that = this;
      (function getNode(data) {
        for (let i = 0; i < data.length; i++) {
          if (data[i].id == that.nodeKeyID) {
            data[i].children.push({ id: 10, label: val, children: [] });
          }
          if (data[i].children.length != 0) {
            getNode(data[i].children);
          }
        }
      })(this.treeData);
    },
    handleDoc() {
      this.nodeKeyType = 'TechnicalDoc';
    },
    handleNodeClick(data, node) {
      if (data.type == 'doc') {
        this.nodeKeyID = data.id;
      } else {
        this.nodeKeyID = node.parent.data.id;
      }
      let parent = node.parent;
      let children = parent.data.children || parent.data;
      let index = children.findIndex(d => d.id === data.id);
      if (data.type == 'section') {
        // this.jump(index);
      }
      this.nodeKeyType = 'BASIC';
    },
    handleNodeClick2(data, node) {
      if (data.type == 'doc') {
        this.nodeKeyID = data.id;
      } else {
        this.nodeKeyID = node.parent.data.id;
      }
      this.nodeKeyType = 'DETAIL';
      let parent = node.parent;
      let children = parent.data.children || parent.data;
      let index = children.findIndex(d => d.id === data.id);
      if (data.type == 'section') {
        // this.jump(index);
      }
      // console.log(data.type)
    },
    jump(index){
			let jump = document.querySelectorAll('.mark')
			// 获取需要滚动的距离
			let total = jump[index].offsetTop
			let distance = $(".content-box").scrollTop()
			let step = total / 50
			if (total > distance) {
			  smoothDown()
			} else {
			  let newTotal = distance - total
			  step = newTotal / 50
			  smoothUp()
			}
			function smoothDown () {
			  if (distance < total) {
			    distance += step
			    $(".content-box").scrollTop(distance)
			    setTimeout(smoothDown, 10)
			  } else {
				$(".content-box").scrollTop(total) 
			  }
			}
			function smoothUp () {
			  if (distance > total) {
			    distance -= step
			    $(".content-box").scrollTop(distance) 
			    setTimeout(smoothUp, 10)
			  } else {
			  	$(".content-box").scrollTop(total) 
			  }
			} 
    	}
  }
};
</script>

<style scoped>
#File-Modle-box {
  width: 100%;
  height: 100%;
  min-width: 1024px;
  overflow: hidden;
}
.tree-box {
  float: left;
  width: 20%;
  max-width: 320px;
  height: 100%;
  padding-left: 18px;
  overflow: scroll;
  /* background: #f5f5f5 */
}
.content-box {
  float: right;
  height: 100%;
  width: 79%;
  overflow-y: auto;
}
@media screen and (max-width: 1024px) {
  .tree-box {
    width: 250px;
  }
  .content-box {
    width: 770px;
  }
}
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

.acs-side-bar-space-info {
  margin-top: 14px;
  margin-bottom: 10px;
  overflow: hidden;
  display: table;
  table-layout: fixed;
  width: 100%;
}
.acs-side-bar-space-info .avatar {
  display: table-cell;
  padding: 0 9px 0 18px;
  width: 65px;
  min-width: 50px;
}

.acs-side-bar-space-info .avatar-img-wrapper {
  border: 0px solid #ccc;
  border-radius: 50%;
  overflow: hidden;
  display: table-cell;
  vertical-align: middle;
}
.model-img {
  max-width: 48px;
  max-height: 48px;
  display: block;
  border: 0;
  margin: auto;
  background-color: white;
}
.technicalDoc {
  margin-left: 15px;
}
.name {
  display: table-cell;
  padding-right: 10px;
  vertical-align: middle;
  -webkit-hyphens: auto;
  -moz-hyphens: auto;
  hyphens: auto;
  text-overflow: ellipsis;
  overflow: hidden;
}
.technicalDoc .doc {
  padding-left: 10px;
  margin-bottom: 8px;
}
.noTextDecoration {
  text-decoration: none;
  color: black;
}
.noTextDecoration:hover {
  text-decoration: underline;
}
</style>

