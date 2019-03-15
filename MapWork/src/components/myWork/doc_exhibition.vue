<template>
    <div class="doc-exhibition">
        <!-- <div class="doc-exhibition-aside">
            <el-tree :data="leftTreeData" :props="defaultProps2" default-expand-all :expand-on-click-node="false">
                <div slot-scope="{ node, data }">
                    <div @click="handleNodeClick(data)" :class="data.sub.length === 0 ? 'cursor-style' : ''">
                        {{data.title}}
                    </div>
                </div>
            </el-tree>
        </div> -->
        <div class="doc-exhibition-content">
            <div>
                <div style="border: solid 2px #ebeef5;font-weight: bold;height: 41px;padding: 8px 0;color: #909399">
                    <span style="padding-left: 10px;">分级</span>
                    <span style="float: right;padding-right: 18px;">文档编号</span>
                </div>
                <div style="padding: 1px; border: solid 2px #ebeef5; border-top: none;">
                    <el-tree :data="rightTreeData" default-expand-all :indent=30 :expand-on-click-node="false" :props="defaultProps">
                        <div class="custom-tree-node" slot-scope="{ node, data }">
                            <div>
                                {{data.title === '未定1' || data.title === '未定2' ? '' : data.title}}
                            </div>
                            <div style="height: 11px;flex-grow:1;border-bottom: dotted 1px" v-if="data.doc_list.length !== 0 ? true : false"></div>
                            <div v-if="data.doc_list.length !== 0 ? true : false">
                                <i class="el-icon-document" v-if="data.doc_list[0] === -1 ? false : true"></i>
                                <el-button v-if="data.doc_list[0] === -1 ? false : true" v-for="(item, index) in data.doc_list" :key="index" @click="go_doc_text(item)" type="text" size="mini">
                                    {{item}}
                                </el-button>
                                <el-button style="cursor: default" v-if="data.doc_list[0] === -1 ? true : false" type="text" size="mini">
                                    TBD
                                </el-button>
                            </div>
                        </div>
                    </el-tree>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
// require('../../assets/css/iconfont.css')
require('../../assets/js/jquery-1.8.3.min.js')
$(document).ready(function() {
    $('.doc-exhibition-content').on('mouseover', '.el-tree-node__content', function() {
        $(this)
            .parent()
            .css('border', 'solid 2px #42b983')
    })
    $('.doc-exhibition-content').on(' mouseout', '.el-tree-node__content', function() {
        $(this)
            .parent()
            .css('border', 'solid 2px white')
    })
})
export default {
    data() {
        return {
            rightTreeData: [],
            leftTreeData: [],
            defaultProps: {
                children: 'sub',
                label: 'title'
            },
            defaultProps2: {
                children: 'sub',
                label: 'title'
            }
        }
    },
    props: ['tag_name'],
    watch: {
        tag_name(val) {
            this.req_doc_tree()
        }
    },
    created() {
        if (this.tag_name === '') {
            this.req_doc_tree()
        } else {
            window.sessionStorage.setItem('tag_name_save', this.tag_name)
            this.req_doc_tree()
        }
    },
    mounted() {
        $(document).ready(function() {
            $('.doc-exhibition-content').on('mouseover', '.el-tree-node__content', function() {
                $(this)
                    .parent()
                    .css('border', 'solid 2px #42b983')
            })
            $('.doc-exhibition-content').on(' mouseout', '.el-tree-node__content', function() {
                $(this)
                    .parent()
                    .css('border', 'solid 2px white')
            })
        })
    },
    methods: {
        req_doc_tree() {
            // 设置homepage导航条默认高亮
            window.sessionStorage.setItem('activeIndex2', '1')
            // 考虑两种情况：1.点击左边树跳转，2.点击浏览器按钮刷新
            if (this.tag_name) {
                this.$axios
                    .get(this.Ip + '/KnowledgeClassify/right/' + this.tag_name)
                    .then(res => {
                        this.rightTreeData = res.data.content[0].sub
                    })
                    .catch(err => {
                        this.$notify({
                            type: 'error',
                            message: '服务器异常: ' + err.response.status,
                            showClose: true,
                            duration: '0'
                        })
                    })
            } else {
                //浏览器直接刷新时候，无法接收到父传过来的tag_name
                let tagName = window.sessionStorage.getItem('tag_name_save')
                this.$axios
                    .get(this.Ip + '/KnowledgeClassify/right/' + tagName)
                    .then(res => {
                        this.rightTreeData = res.data.content[0].sub
                    })
                    .catch(err => {
                        this.$notify({
                            type: 'error',
                            message: '服务器异常: ' + err.response.status,
                            showClose: true,
                            duration: '0'
                        })
                    })
            }
        },
        toogle_table_row_class_name({ row, rowIndex }) {
            if (rowIndex === 1) {
                return 'warning-row'
            } else if (rowIndex === 3) {
                return 'success-row'
            }
            return ''
        },
        go_doc_text(val) {
            let objData = { doc_id: val }
            let data = {
                'data':objData,
                'server_ip':this.Ip
            }
            window.sessionStorage.setItem('listDocID', JSON.stringify(data))
            window.open('../../../static/DocList-item.html')
        },
        handle_node_click(data) {
            if (data.sub.length === 0) {
                this.$axios
                    .get(this.Ip + '/KnowledgeClassify/right/' + data.title)
                    .then(res => {
                        this.rightTreeData = res.data.content[0].sub
                    })
                    .catch(err => {
                        this.$notify({
                            type: 'error',
                            message: '服务器异常: ' + err.response.status,
                            showClose: true,
                            duration: '0'
                        })
                    })
            }
        }
    }
}
</script>
<style scoped>
.doc-exhibition {
    width: 100%;
    height: 100%;
}
.doc-exhibition-aside {
    float: left;
    width: 15%;
    height: 100%;
    padding: 20px 0 0 30px;
    border-right: 2px solid rgba(216, 231, 223, 0.5);
    /* background: salmon; */
}
.doc-exhibition-content {
    /* margin-left: 15%; */
    height: 100%;
    padding: 20px 25px;
    overflow: scroll;
    /* background: saddlebrown; */
}
.el-table .warning-row {
    background: oldlace;
}

.el-table .success-row {
    background: #f0f9eb;
}
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}
.cursor-style {
    cursor: pointer;
}
</style>
