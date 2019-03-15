<template>
  <div id="basic-design">
        <div>
            <h2 style="font-weight:normal;">{{treeNodeType == 'BASIC'?'基本设计':'详细设计'}}
                <i class="el-icon-more" style="float:right;" v-popover:parent_info_pop></i>
                <el-popover placement="bottom" width="200" ref='parent_info_pop' trigger="hover">
                    <p class="nav-select-size">添加概述</p>
                    <p class="nav-select-size"> 添加UserCase</p>
                    <p class="nav-select-size">添加block</p>
                    <p class="nav-select-size"> 添加Sequence</p>
                    <p class="nav-select-size">添加I/F</p>
                    <p class="nav-select-size"> 添加状态迁移图</p>
                </el-popover>
            </h2>
        </div>
        
        <!-- 基本设计内容 -->
        <div class="basic-design-content">
            <!-- 概述 -->
            <div class ="basic-design-content-section">
                <h3 class="title-font-style">概述</h3>
                <div class="basic-design-content-section-content">
                    <p>概述内容</p>
                </div>
            </div>
            <!-- UserCase -->
            <div class ="basic-design-content-section">
                <h3 class="title-font-style">UserCase</h3>
                <div class="basic-design-content-section-content basic-design-content-section-content-ex">
                    <div style="margin-top:20px">
                        <el-table
                            :data="tableData"
                            border
                            style="width: 100%">
                            <el-table-column
                                prop="date"
                                label="日期"
                                width="180">
                            </el-table-column>
                            <el-table-column
                                prop="name"
                                label="姓名"
                                width="180">
                            </el-table-column>
                            <el-table-column
                                prop="address"
                                label="地址">
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </div>
            <!-- block -->
            <div class ="basic-design-content-section">
                <h3 class="title-font-style">block</h3>
                <div class="basic-design-content-section-content">
                    <p>block内容</p>
                </div>
            </div>
            <!-- Sequence -->
            <div class ="basic-design-content-section">
                <h3 class="title-font-style">Sequence</h3>
                <div class="basic-design-content-section-content basic-design-content-section-content-ex">
                    <div style="margin-top:20px">
                        <el-table
                            :data="tableData"
                            border
                            style="width: 100%">
                            <el-table-column
                                prop="date"
                                label="日期"
                                width="180">
                            </el-table-column>
                            <el-table-column
                                prop="name"
                                label="姓名"
                                width="180">
                            </el-table-column>
                            <el-table-column
                                prop="address"
                                label="地址">
                            </el-table-column>
                        </el-table>
                    </div>
                    
                </div>
            </div>
            <!-- Resource -->
            <div class ="basic-design-content-section">
                <h3 class="title-font-style">Resource</h3>
                <div class="basic-design-content-section-content">
                    <p>Resource内容</p>
                </div>
            </div>
            <!-- Resource -->
            <div class ="basic-design-content-section">
                <h3 class="title-font-style">I/F</h3>
                <div class="basic-design-content-section-content">
                    <p>I/F内容</p>
                </div>
            </div>
            <!-- 状态迁移图 -->
            <div class ="basic-design-content-section">
                <h3 class="title-font-style">状态迁移图</h3>
                <div class="basic-design-content-section-content">
                    <img src="https://img-blog.csdn.net/20141020191900984" alt="状态迁移图片">
                </div>
            </div>
        </div>
  </div>
</template>

<script>
export default {
  name: 'basic-design',
  props: ['treeNodeIndex', 'treeNodeType'],
  data() {
    return {
      content: [
        { name: '概述', content: [] },
        { name: 'UseCase', content: [] },
        { name: 'block', content: [] },
        { name: 'Sequence', content: [] },
        { name: 'Resource', content: [] },
        { name: 'I/F', content: [] },
        { name: '状态迁移图', content: [] }
      ],
       tableData: [{
          date: '2016-05-02',
          name: 'Admin',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-04',
          name: 'User',
          address: '上海市普陀区金沙江路 1517 弄'
        }, {
          date: '2016-05-01',
          name: 'Boss',
          address: '上海市普陀区金沙江路 1519 弄'
        }, {
          date: '2016-05-03',
          name: 'Permission',
          address: '上海市普陀区金沙江路 1516 弄'
        }]
    };
  },
  watch: {
    treeNodeIndex(val) {
        this.reqBasicDesignData();
    },
    // treeNodeType(val) {
    //     this.reqBasicDesignData();
    // }
  },
  created() {
    this.reqBasicDesignData();
  },
  methods: {
    reqBasicDesignData() {
      this.$axios
        .get(this.Ip + '/DSDoc/1')
        .then(res => {
          console.log(res.data.content);
        })
        .catch(err => {});
    }
  }
};
</script>

<style scoped>
#basic-design {
  /* padding: 20px; */
  padding: 20px 20px 20px 0;
}
.basic-design-content {
  padding: 20px;
}
.basic-design-content-section {
  margin-bottom: 20px;
}
.basic-design-content-section-content {
  font-size: 14px;
  padding-left: 30px;
  padding-top: 15px;
}
.basic-design-content-section-content-ex {
    padding-top: 5px;
}
img {
  max-width: 100%;
  height: auto;
}
.nav-select-size {
  width: 180px;
  padding: 0 10px;
  height: 26px;
  line-height: 26px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.5s linear;
  -moz-transition: all 0.5s linear; /* Firefox 4 */
  -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
  -o-transition: all 0.5s linear;
}
.nav-select-size:hover {
  background: #2ee08f;
}
.title-font-style {
    font-weight: normal;
}
</style>
