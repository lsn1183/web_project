<template>
    <div id="my-tree" class="wrapper">
        <div class="tree-box" onselectstart="return false">
            <div class="tree-box-content">
                <el-input size="mini" placeholder="输入子节点进行过滤" v-model="filterText">
                </el-input>
                <el-tree :data="tree_data" ref="tree" :default-expanded-keys='expandedKeys' :props="defaultProps" :expand-on-click-node='false' 
                @node-click="node_click" highlight-current :indent='14' node-key="num_id" v-loading="loading" :filter-node-method="filterNode">
                </el-tree>
            </div>
            <div class="nav-bar" title="左右拖动">
                <i class="el-icon-arrow-right"></i>
            </div>
        </div>
        <div class="content-box">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    data () {
        return {
            show_title: '折叠菜单',
            isActive: false,
            hasError: false,
            tree_data: [],
            tree_data_backup: [],
            nodeKeyID: '',
            nodeKeyType: '',
            treeData: [],
            page: 1,
            page_size: 20,
            defaultProps: { label: "title", children: "sub" },
            expandedKeys: [],
            loading: true,
            filterText: ''
        }
    },
    computed: {
        watchPreviewDoc () {
            return this.$store.state.previewDocId
        },
        getTreeData () {
            return this.$store.state.user_data
        }
    },
    watch: {
        watchPreviewDoc (val) {
            // 递归修改树结构高亮显示：
            this.recursionFun(val)
        },
        getTreeData (val) {
            // this.watchPreviewHeightFun();
            if (this.$route.query.params) {
                let value = JSON.parse(this.$route.query.params)
                if (value.type == "model" || value.type == "project" || value.type == "framework") {
                    this.defaultGetTreeFuntwo(value)
                } else {
                    this.defaultGetTreeFun()
                }
            } else {
                this.watchPreviewHeightFun()
            }
        },
        filterText (val) {
            this.$refs.tree.filter(val);
            // this.filter_tree_node(val)
        }
    },
    mounted () {
        // 拖动左边框
        this.move_left_box()
        /*
        分两种情况判断：1，路由不传参，2，路由传参；路由传参又细分：a,高亮具体文档，b,文档的父级，c,模块OR项目OR平台
        */
        if (this.$route.query.params) {//路由传对象时
            let val = JSON.parse(this.$route.query.params)
            if (val.type == "model" || val.type == "project" || val.type == "framework") {
                this.defaultGetTreeFuntwo(val)
            } else {
                this.defaultGetTreeFun()
            }
        } else {//路由传参无对象
            this.watchPreviewHeightFun()
        }
    },
    methods: {
        filterNode (value, data,node) {
            if (!value) return true;
            let regexp = RegExp(value,'i')
            return data.title.search(regexp) !== -1;
            // return data.title.toLowerCase().indexOf(value.toLowerCase()) !== -1;
        },
        filter_tree_node(val){
            // console.log(val)
            if (!val) return;
            window.sessionStorage.setItem("tree_data_storage",JSON.stringify(this.tree_data))
            let regexp = RegExp(val,'i')
            let data = this.tree_data
            console.log(this.tree_data,'tree-all-data')
            function recursionTree (data) {
                for (let i = 0, len = data.length; i < len; i++) {
                    if (data[i].title.search(regexp) !== -1 ) {
                        console.log(data[i],'node')
                    } else {
                        recursionTree(data[i].sub)
                    }
                }
            }
            recursionTree(this.tree_data_backup)
        },
        defaultGetTreeFuntwo (type) {
            this.$axios.get(this.Ip + "/ModelTree").then(res => {
                let data = res.data.content
                this.expandedKeys = []
                var index = 0
                for (const item of data) {
                    for (const iterator of item.sub) {
                        // num_id用于默认树展开的节点id
                        iterator.num_id = index++
                        if (iterator.type == "project") {
                            this.expandedKeys.push(iterator.num_id)
                        }
                    }
                }
                if (type.type == "framework" || type.type == "project") {
                    this.tree_data = data
                    this.loading = false
                    this.tree_data_backup = data
                    return
                }
                // 用于二次修改树节点的高亮和展开
                this.tree_data_backup = data
                // 高亮判断
                let val = JSON.parse(this.$route.query.params)
                var previewData = val
                this.expandedKeys = []
                this.tree_data = []
                var index = 0
                var lightKeys = null
                var self = this
                function recursionTree (data) {
                    for (let i = 0, len = data.length; i < len; i++) {
                        data[i].num_id = index++
                        if (data[i].proj_id == previewData.proj_id && data[i].type == previewData.type && data[i].id == previewData.model_id) {
                            self.expandedKeys.push(data[i].num_id)
                            lightKeys = data[i].num_id
                            window.sessionStorage.setItem("lightKeys", lightKeys)
                            break
                        } else {
                            recursionTree(data[i].sub)
                        }
                    }
                }
                recursionTree(this.tree_data_backup)
                this.$nextTick(() => {
                    this.tree_data = this.tree_data_backup
                    this.loading = false
                    let _this = this
                    setTimeout(() => {
                        _this.$refs.tree.setCurrentKey(lightKeys);
                    }, 0)
                })
            })
        },
        defaultGetTreeFun () {
            this.$axios.get(this.Ip + "/ModelTree").then(res => {
                let data = res.data.content
                this.expandedKeys = []
                var index = 0
                for (const item of data) {
                    for (const iterator of item.sub) {
                        // num_id用于默认树展开的节点id
                        iterator.num_id = index++
                        if (iterator.type == "project") {
                            this.expandedKeys.push(iterator.num_id)
                        }
                    }
                }
                // this.tree_data = data
                // 用于二次修改树节点的高亮和展开
                this.tree_data_backup = data
                // 高亮判断
                if (this.$route.query.params) {//添加基本设计or详细设计页面返回
                    let val = JSON.parse(this.$route.query.params)
                    if (val) {
                        if (val.type == "DETAIL") {
                            val.type = "详细设计"
                        } else if (val.type == "BASIC") {
                            val.type = "基本设计"
                        }
                    } else {
                        this.$router.path("/tagl/File_design/basic_design_template")
                        return
                    }
                    var previewData = val
                    this.expandedKeys = []
                    this.tree_data = []
                    var index = 0
                    var lightKeys = null
                    var self = this
                    function recursionTree (data) {
                        for (let i = 0, len = data.length; i < len; i++) {
                            data[i].num_id = index++
                            if (data[i].proj_id == previewData.proj_id && data[i].title == previewData.type && data[i].parent_model_id == previewData.model_id) {
                                self.expandedKeys.push(data[i].num_id)
                                lightKeys = data[i].num_id
                                window.sessionStorage.setItem("lightKeys", lightKeys)
                                break
                            } else {
                                recursionTree(data[i].sub)
                            }
                        }
                    }
                    recursionTree(this.tree_data_backup)
                    this.$nextTick(() => {
                        this.tree_data = this.tree_data_backup
                        this.loading = false
                        let _this = this
                        setTimeout(() => {
                            _this.$refs.tree.setCurrentKey(lightKeys);
                        }, 0)
                    })
                }
            })
        },
        watchPreviewHeightFun () {
            this.$axios.get(this.Ip + "/ModelTree").then(res => {
                let data = res.data.content
                this.expandedKeys = []
                var index = 0
                for (const item of data) {
                    for (const iterator of item.sub) {
                        // num_id用于默认树展开的节点id
                        iterator.num_id = index++
                        if (iterator.type == "project") {
                            this.expandedKeys.push(iterator.num_id)
                        }
                    }
                }
                // 用于二次修改树节点的高亮和展开
                this.tree_data_backup = data
                // 高亮判断
                if (this.$route.params.docid) {//preview页面跳转后点击刷新，继续显示高亮
                    let val = {}
                    val.doc_id = this.$route.params.docid
                    // 调用递归方法修改树结构高亮显示：
                    this.recursionFun(val)
                    window.sessionStorage.removeItem("lightKeys")
                } else {
                    this.tree_data = data
                    this.loading = false
                }
            })
        },
        recursionFun (val) {
            var previewData = val
            // console.log(val, "高亮")
            this.expandedKeys = []
            this.tree_data = []
            var index = 0
            var lightKeys = null
            var self = this
            function recursionTree (data) {
                for (let i = 0, len = data.length; i < len; i++) {
                    if (data[i].sub.length === 0) {
                        data[i].num_id = index++
                        if (data[i].id == previewData.doc_id) {
                            self.expandedKeys.push(data[i].num_id)
                            lightKeys = data[i].num_id
                        }
                    } else {
                        recursionTree(data[i].sub)
                    }
                }
            }
            recursionTree(this.tree_data_backup)
            this.$nextTick(() => {
                this.tree_data = this.tree_data_backup
                this.loading = false
                let _this = this
                setTimeout(() => {
                    _this.$refs.tree.setCurrentKey(lightKeys);
                }, 0)
            })
        },
        move_right_tree () {
            var e21 = event.clientX
        },
        node_click (data) {
            // console.log(data,"data")
            var clickNodeData = data
            window.sessionStorage.setItem('scrollTop', 0)
            if (clickNodeData.type && clickNodeData.type == "model") {// 判断点击的是模块
                this.go_to_module_list_fun(clickNodeData)
            } else if (clickNodeData.type && clickNodeData.id == "BASIC") {//判断点击的是基本设计
                this.go_to_basic_list_fun(clickNodeData)
            } else if (clickNodeData.type && clickNodeData.id == "DETAIL") {//判断点击的是详细设计
                this.go_to_detail_list_fun(clickNodeData)
            } else if (clickNodeData.type && clickNodeData.type == "doc") {//具体文档跳转详细页面
                this.go_to_doc_preview_fun(clickNodeData)
            } else if (clickNodeData && clickNodeData.type == "framework") {//判断点击的是平台
                this.go_to_framework_lsit_fun(clickNodeData)
            } else if (clickNodeData && clickNodeData.type == 'project') {//判断点击的是项目 
                this.go_to_project_list_fun(clickNodeData)
            }
        },
        go_to_doc_preview_fun (clickNodeData) {
            var doc_id = clickNodeData.id
            let datas = {
                "proj_id": clickNodeData.proj_id,
                "model_id": clickNodeData.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_查看') == true) {//权限
                        this.$store.state.desk_id = 0
                        let routerValue = { id: clickNodeData.id, model_id: clickNodeData.model_id, proj_id: clickNodeData.proj_id, type: clickNodeData.type }
                        window.sessionStorage.setItem("previewPurviewManageData", JSON.stringify(routerValue))
                        this.$router.push({ path: '/tagl/File_design/Preview/' + doc_id, query: { preview: JSON.stringify(routerValue) } })
                        window.sessionStorage.removeItem("treeNodeId")
                    } else {
                        this.$message({
                            type: "warning",
                            message: "您没有权限操作"
                        })
                    }
                } else {
                    // nothing to do
                    this.$message({
                        type: "warning",
                        message: res.data.error
                    })
                }
            })
        },
        go_to_module_list_fun (clickNodeData) {
            let id_Obj = { 'model_id': clickNodeData.id, 'proj_id': clickNodeData.proj_id, 'type': 'model' }
            window.sessionStorage.setItem("treeNodeId", JSON.stringify(id_Obj))
            this.$store.state.desk_id = id_Obj
            this.$router.push({ path: '/tagl/File_design/basic_design_template', query: { params: JSON.stringify(id_Obj) } })
        },
        go_to_basic_list_fun (clickNodeData) {
            var id_Obj = { 'model_id': clickNodeData.parent_model_id, 'proj_id': clickNodeData.proj_id, 'type': "BASIC" }
            window.sessionStorage.setItem("treeNodeId", JSON.stringify(id_Obj))
            this.$store.state.desk_id = id_Obj
            // 用来解决路由切换后vuex监听不执行（preview页面和list页面来回切换，vuex执行问题）
            this.$router.push({ path: '/tagl/File_design/basic_design_template', query: { params: JSON.stringify(id_Obj) } })
        },
        go_to_detail_list_fun (clickNodeData) {
            var id_Obj = { 'model_id': clickNodeData.parent_model_id, 'proj_id': clickNodeData.proj_id, 'type': "DETAIL" }
            window.sessionStorage.setItem("treeNodeId", JSON.stringify(id_Obj))
            this.$store.state.desk_id = id_Obj
            // 用来解决路由切换后vuex监听不执行
            this.$router.push({ path: '/tagl/File_design/basic_design_template', query: { params: JSON.stringify(id_Obj) } })
        },
        go_to_project_list_fun (clickNodeData) {
            // 项目ID
            var id_Obj = { "project_id": clickNodeData.id, "type": "project" }
            this.$store.state.desk_id = id_Obj
            this.$router.push({ path: '/tagl/File_design/basic_design_template', query: { params: JSON.stringify(id_Obj) } })
            // 点击不在设置session范围的时候默认清除
            window.sessionStorage.removeItem("treeNodeId")
        },
        go_to_framework_lsit_fun (clickNodeData) {
            // 平台ID
            var id_Obj = { "framework_id": clickNodeData.id, "type": "framework" }
            this.$store.state.desk_id = id_Obj
            this.$router.push({ path: '/tagl/File_design/basic_design_template', query: { params: JSON.stringify(id_Obj) } })
            // 点击不在设置session范围的时候默认清除
            window.sessionStorage.removeItem("treeNodeId")
        },
        move_left_box () {
            var self = this
            $('.nav-bar').mousedown(function (e) {
                $('#my-tree').mousemove(function (e) {
                    if (document.body.clientWidth <= 1138) {
                        if ($('.tree-box').width() <= 178) {
                            $('.tree-box').css({ "width": 190 + "px" })
                            $('.nav-bar').css({ left: 190 + 'px' })
                            $('#my-tree').unbind('mousemove')
                        } else if ($('.tree-box').width() > document.body.clientWidth * 0.85) {
                            $('.tree-box').css({ "width": document.body.clientWidth * 0.84 + "px" })
                            $('.nav-bar').css({ left: document.body.clientWidth * 0.84 + 'px' })
                            $('#my-tree').unbind('mousemove')
                        } else {
                            $('.tree-box').css({ "width": e.clientX + "px" })
                            $('.nav-bar').css({ left: e.clientX + 'px' })
                        }
                    } else if (document.body.clientWidth > 1138 && document.body.clientWidth <= 1498) {
                        if ($('.tree-box').width() <= 200) {
                            $('.tree-box').css({ "width": 210 + "px" })
                            $('.nav-bar').css({ left: 210 + 'px' })
                            $('#my-tree').unbind('mousemove')
                        } else if ($('.tree-box').width() > document.body.clientWidth * 0.85) {
                            $('.tree-box').css({ "width": document.body.clientWidth * 0.84 + "px" })
                            $('.nav-bar').css({ left: document.body.clientWidth * 0.84 + 'px' })
                            $('#my-tree').unbind('mousemove')
                        } else {
                            $('.tree-box').css({ "width": e.clientX + "px" })
                            $('.nav-bar').css({ left: e.clientX + 'px' })
                        }
                    } else if (document.body.clientWidth <= 2133) {
                        if ($('.tree-box').width() <= 235) {
                            $('.tree-box').css({ "width": 245 + "px" })
                            $('.nav-bar').css({ left: 245 + 'px' })
                            $('#my-tree').unbind('mousemove')
                        } else if ($('.tree-box').width() > document.body.clientWidth * 0.85) {
                            $('.tree-box').css({ "width": document.body.clientWidth * 0.84 + "px" })
                            $('.nav-bar').css({ left: document.body.clientWidth * 0.84 + 'px' })
                            $('#my-tree').unbind('mousemove')
                        } else {
                            $('.tree-box').css({ "width": e.clientX + "px" })
                            $('.nav-bar').css({ left: e.clientX + 'px' })
                        }
                    }
                })
            })
            $('#my-tree').mouseup(function (e) {
                $('#my-tree').unbind('mousemove')
            })
        }
    }
}
</script>

<style scoped>
.wrapper {
    width: 100%;
    height: 100%;
    min-width: 1024px;
    color: #606266;
    overflow: hidden;
}
.tree-box {
    /*float: left;*/
    position: relative;
    top: 0;
    left: 0;
    z-index: 9;
    margin: 0;
    padding: 0;
    width: 15%;
    height: 98%;
    background-color: white;
    border-right: 2px solid rgba(216, 231, 223, 0.5);
    overflow: scroll;
    overflow-x: hidden;
}

.tree-box-content {
    margin-left: 0;
    padding-left: 10px;
    height: 100%;
    margin-right: 0;
    padding-right: 0;
    padding-top: 20px;
}

.content-box {
    /*float: right;*/
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 85%;
    overflow-y: auto;
}
.nav-bar {
    position: fixed;
    top: 50%;
    margin-top: -15px;
    /*z-index: 11;*/
    /*right: 0;*/
    left: 15%;
    width: 14px;
    height: 30px;
    border-radius: 10px;
    line-height: 30px;
    background-color: #42b983;
    cursor: e-resize;
    color: white;
}
@media screen and (max-width: 1024px) {
    .wrapper {
        width: 1024px;
    }
    .tree-box {
        width: 20%;
    }
    .nav-bar {
        position: fixed;
        left: 20%;
    }
    .content-box {
        width: 80%;
    }
}
@media screen and (max-width: 1366px) {
    .tree-box {
        width: 20%;
    }
    .nav-bar {
        position: fixed;
        left: 20%;
    }
    .content-box {
        width: 80%;
    }
}
</style>

