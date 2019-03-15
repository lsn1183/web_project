<template>
    <div class="wrapper">
        <div class="tree-box" onselectstart="return false">
            <ul class="tree-ul">
                <li v-for="(node,index) in tree" class="tree-li">
                    <!-- 第一层标题 -->
                    <p @click="FirstScrollTop(index)" class="first-title">
                        <i class="el-icon-caret-right"></i> {{node.node_name}}
                    </p>
                    <!-- 第二层结构 -->
                    <ul class="child_ul">
                        <li class="child-tree-li" v-for="(child_node,child_index) in node.child_node">
                            <p @click="SecondScrillTop(index,child_index)" class="second-title" :title="child_node.child_node_name">
                                {{child_node.child_node_name}}
                            </p>
                        </li>
                    </ul>

                </li>
            </ul>
        </div>
        <div class="content-box">
            <h1 class="title_h1">
                {{title}}
                <span class="append-span" @click="showDialog(true)">[ 版本编辑 ]</span>
                <span class="back" @click="back()">[ 返回 ]</span>
            </h1>
            <p class="title-detail">
                <span>{{doc_update_info}}</span>
            </p>

            <!-- Block -->
            <div class="block-box Asa-box">
                <h3 class="title-h3">
                    <span>Block</span>
                    <span class="append-span" @click="block_fun('add','block')" v-if='Block.length==0'> &nbsp;[ 添加 ]</span>
                    <span class="append-span" @click="block_fun('edit','block')" v-else> &nbsp;[ 编辑 ]</span>
                </h3>
                <!-- Block 子元素块 -->
                <div class="msg-box" v-for="(block_item,index) in Block">
                    <h4 class="title-h4">
                        <span>Block {{index+1}}: {{block_item.sec_title}}</span>
                        <span class="append-span" @click="block_fun('add','block')" v-if='Block.length==0'> &nbsp;[ 添加 ]</span>
                        <span class="append-span" @click="block_fun('edit','block')"> &nbsp;[ 编辑 ]</span>
                    </h4>
                    <div class="content-size">
                        <span>Block说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='block_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in block_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='block_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                </div>
                <p class="message" v-if='Block.length==0'>暂无数据</p>
            </div>

            <!-- Class -->
            <div class="Class-box Asa-box">
                <h3 class="title-h3">
                    <span>Class</span>
                    <span class="append-span" @click="block_fun('add','class')" v-if='Class.length==0'> &nbsp;[ 添加 ]</span>
                    <span class="append-span" @click="block_fun('edit','class')" v-else> &nbsp;[ 编辑 ]</span>
                </h3>
                <!-- Class 子元素块 -->
                <div class="msg-box" v-for="(class_item,index) in Class">
                    <h4 class="title-h4">
                        <span>Class{{index+1}}: {{class_item.sec_title}}</span>
                        <span class="append-span" @click="block_fun('add','class')" v-if='Class.length==0'> &nbsp;[ 添加 ]</span>
                        <span class="append-span" @click="block_fun('edit','class')" v-else> &nbsp;[ 编辑 ]</span>
                    </h4>
                    <div class="content-size">
                        <span>Class说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='class_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in class_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='class_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                </div>
                <p class="message" v-if='Class.length==0'>暂无数据</p>
            </div>

            <!-- Usecase -->
            <div class="Usecase-box Asa-box">
                <h3 class="title-h3">
                    <span>Usecase</span>
                    <span class="append-span" v-if='Usecase.length==0' @click='append_usecase("add")'> &nbsp;[ 添加 ]</span>
                    <span class="append-span" v-else @click='append_usecase("edit")'> &nbsp;[ 编辑 ]</span>
                </h3>
                <!-- Usecase 子元素块 -->
                <div class="msg-box" v-for="(usecase_item,index) in Usecase">
                    <h4 class="title-h4">
                        <span>Usecase{{index+1}}: {{usecase_item.sec_title}}</span>
                        <span class="append-span" v-if='Usecase.length==0' @click='append_usecase("add")'> &nbsp;[ 添加 ]</span>
                        <span class="append-span" v-else @click='append_usecase("edit")'> &nbsp;[ 编辑 ]</span>
                    </h4>
                    <div class="content-size">
                        <span>Usecase说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='usecase_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in usecase_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='usecase_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                </div>
                <p class="message" v-if='Usecase.length==0'>暂无数据</p>
                <!-- Usecase列表 -->
                <div class="Usecase-table">
                    <h4 class="title-h4">
                        <span>Usecase列表</span>
                        <span class="append-span" @click='append_usecase("edit")'> &nbsp;[ 编辑 ]</span>
                    </h4>
                    <el-table :data="UsecaseTable" border style="width:95%">
                        <el-table-column prop="number" label="UseCase Name" header-align='center' width="250px">
                            <template slot-scope="scope">
                                <el-button size="mini" type="text" @click="go_seq(scope.$index, scope.row, 'sec_level1')">
                                    <span> &nbsp;{{scope.row.sec_level1}}</span>
                                </el-button>
                            </template>
                        </el-table-column>
                        <el-table-column prop="number" label="SubUseCase" header-align='center' width="250px">
                            <template slot-scope="scope">
                                <el-button size="mini" type="text" @click="go_seq(scope.$index, scope.row, 'sec_level2')">
                                    <span> &nbsp;{{scope.row.sec_level2}}</span>
                                </el-button>
                            </template>
                        </el-table-column>
                        <el-table-column prop="func_id" label="关联式样书" header-align='center'>
                            <template slot-scope="scope">
                                <div v-for="item in scope.row.func_list">
                                    <a :href="item.html_url" target="_blank"> 
                                        {{item.spec_file_name}}{{item.func_name}}{{item.func_id}}
                                    </a>
                                </div>
                            </template>
                        </el-table-column>
                        <el-table-column prop="explain" label="说明（变更点/对应内容等）" header-align='center'></el-table-column>
                    </el-table>
                </div>
            </div>

            <!-- Statemachine -->
            <div class="Std-box Asa-box">
                <h3 class="title-h3">
                    <span>Statemachine</span>
                    <span class="append-span" @click="block_fun('add','statemachine')" v-if='Statemachine.length==0'> &nbsp;[ 添加 ]</span>
                    <span class="append-span" @click="block_fun('edit','statemachine')" v-else> &nbsp;[ 编辑 ]</span>
                </h3>
                <!-- Statemachine 子元素块 -->
                <div class="msg-box" v-for="(statemachine_item,index) in Statemachine">
                    <h4 class="title-h4">
                        <span>Statemachine{{index+1}}: {{statemachine_item.sec_title}}</span>
                        <span class="append-span" @click="block_fun('edit','statemachine')"> &nbsp;[ 编辑 ]</span>
                    </h4>
                    <div class="content-size">
                        <span>Statemachine说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='statemachine_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in statemachine_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='statemachine_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                </div>
                <p class="message" v-if='Statemachine.length==0'>暂无数据</p>
            </div>

        </div>
        <el-dialog title="版本编辑" :visible.sync="editVersionFlag" width="550px">
            <el-form ref="versionForm" :model="versionForm" :rules="rules" label-width="30%">
                <el-form-item label="版本号" prop="version">
                    <el-input v-model="versionForm.version"></el-input>
                </el-form-item>
                <el-form-item>
                    示例：1.001 (多位数字+ '.' + 三位数字)
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" size="mini" @click="editVersion('versionForm')">确 定</el-button>
                <el-button size="mini" @click="showDialog(false)">取 消</el-button>
            </span>
        </el-dialog>
    </div>
</template>
<script>
require('../../assets/js/jquery-1.8.3.min.js')
document.oncontextmenu = function(){
    return false;
}
document.onselectstart = function(){
    return false;
}
document.oncopy = function(){
    return false;
}
export default {
    data() {
        return {
            UsecaseTable: [],
            tree: [
                { node_name: 'Block', child_node: [] },
                { node_name: 'Class', child_node: [] },
                { node_name: 'Usecase', child_node: [] },
                { node_name: 'Statemachine', child_node: [] }
            ],
            title: '',
            Block: [],
            Class: [],
            Usecase: [],
            Statemachine: [],
            type: '',
            doc_update_info: '',
            editVersionFlag: false,
            rules: {
                version: [
                    { required: true, message: '请输入获得版本号', trigger: 'blur' },
                    { pattern: /^\d+\.\d{3}$/, message: '版本号格式不符合规范' }
                ]
            },
            versionForm: {
                version: ''
            },
            version: '',
            model_id:'',
        }
    },
    created() {},
    mounted() {
        this.doc_id = this.$route.params.docId
        this.type = this.$route.params.docType
        this.get_NewDs_Doc()
    },
    watch: {
        $route(to, from) {
            this.doc_id = this.$route.params.docId
            this.type = this.$route.params.docType
            this.get_NewDs_Doc()
        }
    },
    methods: {
        get_NewDs_Doc() {
            this.$axios.get(this.Ip + '/NewDSDoc/' + this.doc_id).then(res => {
                if (res.data.result == 'OK') {
                    this.model_id = res.data.content.model_id
                    this.versionForm.version = res.data.content.ver
                    this.version = res.data.content.ver
                    let update_date_re = new RegExp(/^\d+-\d+-\d+/)
                    this.doc_update_info =
                        '由 ' +
                        res.data.content.creator +
                        ' 创建，最终由 ' +
                        res.data.content.editor +
                        ' 修改于 ' +
                        res.data.content.update_time.match(update_date_re)
                    this.title = res.data.content.title
                    this.UsecaseTable = res.data.content.UsecaseTable
                    this.tree = [
                        { node_name: 'Block', child_node: [] },
                        { node_name: 'Class', child_node: [] },
                        { node_name: 'Usecase', child_node: [] },
                        { node_name: 'Statemachine', child_node: [] }
                    ]
                    this.get_Block(res.data.content.Block)
                    this.get_Class(res.data.content.Class)
                    this.get_Usecase(res.data.content.Usecase)
                    this.get_Statemachine(res.data.content.Statemachine)
                }
            })
        },
        get_Block(data_json) {
            this.push_data(data_json, this.Block, 'Block', 0)
        },
        get_Class(data_json) {
            this.push_data(data_json, this.Class, 'Class', 1)
        },
        get_Usecase(data_json) {
            this.push_data(data_json, this.Usecase, 'Usecase', 2)
        },
        get_Statemachine(data_json) {
            this.push_data(data_json, this.Statemachine, 'Statemachine', 3)
        },
        push_data(data_json, self, name, index) {
            if (data_json.length == 0) {
                return
            }
            for (let item = 0; item < data_json.length; item++) {
                let img_json = JSON.parse(data_json[item].content)
                this.tree[index].child_node.push({
                    child_node_name: name + (item + 1) + ':' + data_json[item].sec_title
                })
                self.push({
                    complement: data_json[item].complement,
                    img_list: img_json,
                    explain: data_json[item].explain,
                    sec_title: data_json[item].sec_title
                })
            }
        },
        go_seq(index, row, type) {
            let datas = {
                "proj_id": sessionStorage.getItem('proj_id'),
                "model_id": this.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                        // to do
                        let sec_id = row.level1_sec_id
                        this.$router.push({ path: '/tagl/File_design/Preview_seq/' + sec_id })
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
        append_usecase(type) {
            let datas = {
                "proj_id": sessionStorage.getItem('proj_id'),
                "model_id": this.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            sessionStorage.setItem('model_id',this.model_id)
            if (this.type == 'basic_design') {
                if (type == 'add') {
                    this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                        if (res.data.result == "OK") {
                            var userPermissionData = res.data.content
                            if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                                // to do
                                this.$router.push({ path: '/tagl/basic_design_usecase_add/' + this.doc_id + '/' + this.title })
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
                } else {
                    this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                        if (res.data.result == "OK") {
                            var userPermissionData = res.data.content
                            if (this.getCatusPurviewManage(userPermissionData, '设计书_编辑') == true) {
                                // to do
                                this.$router.push({ path: '/tagl/basic_design_usecase_edit/' + this.doc_id + '/' + this.title })
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
                }
            } else {
                if (type == 'add') {
                    this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                        if (res.data.result == "OK") {
                            var userPermissionData = res.data.content
                            if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                                // to do
                                this.$router.push({ path: '/tagl/detail_design_usecase_add/' + this.doc_id + '/' + this.title })
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

                } else {
                    this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                        if (res.data.result == "OK") {
                            var userPermissionData = res.data.content
                            if (this.getCatusPurviewManage(userPermissionData, '设计书_编辑') == true) {
                                // to do
                                this.$router.push({ path: '/tagl/detail_design_usecase_edit/' + this.doc_id + '/' + this.title })
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
                }
            }
        },
        back() {
            this.$router.push('/tagl/develop_design')
        },
        FirstScrollTop(index) {
            $('.first-title').css({ color: '#606266' })
            $('.second-title').css({ color: '#606266' })
            $('.first-title')
                .eq(index)
                .css({ color: '#42b983' })
            let sTop = document.getElementsByClassName('Asa-box')[index].offsetTop
            $('.content-box').animate({ scrollTop: sTop }, 500, function() {})
        },
        SecondScrillTop(index, second) {
            $('.first-title').css({ color: '#606266' })
            $('.second-title').css({ color: '#606266' })
            $('.tree-li')
                .eq(index)
                .find('.second-title')
                .eq(second)
                .css({ color: '#42b983' })
            let sTop = $('.Asa-box')
                .eq(index)
                .find('.msg-box')
                .eq(second)[0].offsetTop
            $('.content-box').animate({ scrollTop: sTop }, 500, function() {})
        },
        block_fun(type, click_type) {
            let value = {
                path: '/tagl/step_Block',
                query: {
                    data: JSON.stringify({
                        type: type,
                        doc_id: this.doc_id,
                        title: this.title,
                        click_type: click_type,
                        doc_type: this.type,
                        proj_id: sessionStorage.getItem('proj_id'),
                        model_id:this.model_id
                    })
                }
            }
            let datas = {
                "proj_id": sessionStorage.getItem('proj_id'),
                "model_id": this.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            if (type == 'add') {
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                            // to do
                            this.$router.push(value)
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
            } else {
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_编辑') == true) {
                            // to do
                            this.$router.push(value)
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
            }
        },
        showDialog(value) {
            let datas = {
                "proj_id": sessionStorage.getItem('proj_id'),
                "model_id": this.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_版本编辑') == true) {
                        // to do
                        if (value) {
                            this.versionForm.version = this.version
                        }
                        this.editVersionFlag = value
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
        editVersion(versionForm) {
            this.$refs[versionForm].validate(valid => {
                if (valid) {
                    let data = {
                        doc_id: this.doc_id,
                        commit_user: window.sessionStorage.getItem('Uall'),
                        ver: this.versionForm.version
                    }
                    this.$axios
                        .post(this.Ip + '/UpDocVer', data)
                        .then(res => {
                            if (res.data.result == 'OK') {
                                this.showDialog(false)
                                this.$message({
                                    type: 'success',
                                    showClose: false,
                                    message: '修改成功'
                                })
                                this.doc_id = this.$route.params.docId
                                this.type = this.$route.params.docType
                                this.get_NewDs_Doc()
                            } else {
                                this.$message({
                                    type: 'error',
                                    showClose: true,
                                    message: res.data.error
                                })
                            }
                        })
                        .catch(err => {
                            this.$message({
                                type: 'error',
                                showClose: true,
                                message: '服务异常'
                            })
                        })
                } else {
                    return false
                }
            })
        }
    }
}
</script>

<style scoped>
html,
body {
    font-family: '微软雅黑';
}
.wrapper {
    width: 100%;
    height: 100%;
    min-width: 1024px;
    color: #606266;
    overflow: hidden;
}
.tree-box {
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
.content-box {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 85%;
    overflow-y: auto;
    padding-left: 20px;
}
.title_h1 {
    font-weight: bold;
    font-size: 24px;
    margin-top: 10px;
    width: 95%;
}
.title-detail {
    font-size: 12px;
    color: #5e6d82;
    text-align: left;
    height: 20px;
    line-height: 20px;
    margin-top: 10px;
}
.block-box,
.Class-box,
.Usecase-table,
.Usecase-box,
.Std-box {
    margin-top: 10px;
}
.Std-box {
    margin-bottom: 40px;
}
.title-h3 {
    font-size: 20px;
    font-weight: 500;
    height: 25px;
    line-height: 25px;
    font-weight: bold;
}
.title-h4 {
    font-size: 18px;
    padding-top: 10px;
    /*font-weight: 500*/
}
.append-span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}

.content-size {
    margin-top: 10px;
}

#editor {
    width: 95%;
    margin-top: 10px;
}
.v-note-wrapper {
    min-height: 100px;
}
.msg-box,
.img-box,
.Usecase-table {
    margin-top: 10px;
}
.img-box {
    overflow: auto;
}
.message {
    width: 95%;
    background-color: #edf9f5;
    text-align: center;
    padding: 20px;
    font-size: 14px;
    color: #909399;
    border: 1px solid #ebeef5;
    margin-top: 10px;
}

/*树*/
ul,
li {
    list-style: none;
}
.tree-ul {
    overflow: hidden;
    width: 100%;
    padding-left: 20px;
}
.child_ul {
    overflow: hidden;
    padding-left: 10px;
}
.tree-li {
    margin-top: 10px;
    font-weight: bold;
    cursor: pointer;
}
.tree-li p {
    height: 24px;
    line-height: 24px;
}
.child-tree-li {
    margin-top: 5px;
    margin-left: 20px;
    font-weight: 500;
    font-size: 14px;
}

.back {
    float: right;
    font-size: 16px;
    cursor: pointer;
    margin-top: 10px;
    font-weight: 500;
}
@media screen and (max-width: 1024px) {
    .wrapper {
        width: 1024px;
    }
    .tree-box {
        width: 20%;
    }
    .content-box {
        width: 80%;
    }
}
</style>

