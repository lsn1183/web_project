<template>
    <div class="add-project-step" v-loading="loading">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="项目信息">1</el-step>
                    <!-- <el-step class="jump" title="平台">2</el-step> -->
                    <el-step class="jump" title="知识库">3</el-step>
                    <el-step class="jump" title="模块" icon="el-icon-edit" status="process">4</el-step>
                    <el-step class="jump" title="模块负责组">5</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Mode" >
            <div class="mid">
                <div class="mid-top">
                    <div class="step-one-title">
                        <h2>模块
                            <i class="el-icon-question" style="font-size: 15px;" title="请提供和Usecase相关的式样书，式样书可以是要求式样书、机能式样书、操作式样书等"></i>
                        </h2>
                    </div>
                    <div style="font-size: 16px;margin-bottom: 10px;">
                        <div style="margin:20px 0 10px 0">
                            <span style="padding-left:20px">项目：{{proj_name}}</span>

                            <span style="padding-left:40px;cursor:pointer;font-size:14px" @click="Synchronize_module()">[ 同步框架模块信息 ]</span>
                        </div>

                    </div>
                    <div class="two-box"  >
                        <el-tree  :data="subModelList.model_tree" node-key="id" :props="defaultProps" default-expand-all :expand-on-click-node="false">
                            <span class="custom-tree-node" slot-scope="{ node, data }">
                                <span>{{ node.label }}</span>
                            </span>
                        </el-tree>
                    </div>
                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="prev()">
                        <i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button @click="save()" disabled type="primary" size='mini'>&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button @click="cancel()" type="primary" size='mini'>&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="next()">下一步
                        <i class="el-icon-arrow-right"></i>
                    </el-button>
                </div>
            </div>
        </div>
    </div>

</template>
<script>
require('../../../assets/js/jquery-1.8.3.min.js')
export default {
    data () {
        return {
            checkAll: true,
            modelList: [
                { model_name: 'Route', model_id: 1 },
                { model_name: 'Guide', model_id: 2 },
                { model_name: 'RouteView', model_id: 3 },
                { model_name: 'GuideView', model_id: 4 },
                { model_name: 'RouteWeb', model_id: 5 },
                { model_name: 'GuideWeb', model_id: 6 },
                { model_name: 'RouteNive', model_id: 7 },
                { model_name: 'GuideNive', model_id: 8 },
                { model_name: 'RouteVoice', model_id: 9 },
                { model_name: 'GuideVoice', model_id: 10 },
                { model_name: 'DataView', model_id: 11 }
            ],
            defaultProps: {
                children: 'model_sub',
                label: 'title',
                id: 'model_id',
                key: 'key',

            },
            repeatList: [],

            proj_name: window.sessionStorage.getItem('proj_name'),
            fw_name: window.sessionStorage.getItem('fw_name'),
            subModelList: {
                proj_id: 0,
                user_name: window.sessionStorage.getItem('Uall'),
                model_tree: []
            },
            visible2: false,
            tree_add_pop: false,

            OptionsTagList: [],
            active: Number(window.sessionStorage.getItem('step_id')),
            spec_list_flag: false,
            input_spec: "",
            select_list: [],
            options: [],
            get_data: '',
            save_data: '',
            loading: true,
        }
    },
    watch: {
        input_spec (val) {
            if (this.input_spec != "") {
                // this.SearchSpec(val,cb)
                this.SearchSpec2(val)
            } else {
                this.getSpec2()
            }

        }
    },
    mounted () {
        var self = this
        $('.jump').on('click', function (e) {
            self.jump_to($(this).text())
        });
        this.judgeAll()
        this.getFW_Name()
    },
    methods: {
        CheckedAll (val) {
            if (val) {
                for (const mod of this.modelList) {
                    this.subModelList.model_tree.push(mod.model_id)
                }
            } else {
                this.subModelList.model_tree = []
            }

        },
        getFW_Name () {
            this.$axios.get(this.Ip + '/ProjectFW/' + Number(window.sessionStorage.getItem('proj_id')))
                .then(res => {
                    // console.log(res)
                    if (res.data.result == 'OK') {
                        this.fw_name = res.data.content.fw_name
                    } else {
                    }

                })
                .catch(err => {

                })
        },
        repeatModel (list) {
            // console.log(list,"list")
            let sublist = list
            if (sublist.length == 0) {
                return
            } else {
                for (var i = 0; i < sublist.length; i++) {
                    this.repeatList.push({ model_id: sublist[i].model_id })
                    this.repeatModel(sublist[i].model_sub)
                }
                // this.repeatList.push(sublist.model_id)
                // this.repeatModel(sublist.model_sub)
            }
        },
        CheckedChange (value) {
            let checkedCount = value.length
            this.checkAll = checkedCount === this.modelList.length
        },
        judgeAll () {
            this.$axios.get(this.Ip + '/ProjectModel/' + window.sessionStorage.getItem('proj_id'))
                .then(res => {
                    // console.log(res,"md")
                    if (res.data.result == 'OK') {
                        this.repeatModel(res.data.content.model_tree[0].model_sub)
                        this.subModelList.model_tree = res.data.content.model_tree
                        this.get_data = JSON.stringify(this.subModelList)
                        this.loading = false
                    }
                })
                .catch(err => {
                    alert(err)
                })
        },
        clear_input () {
            if (this.input_spec != "") {
                this.SearchSpec2(this.input_spec)
            } else {
                this.getSpec2()
            }
            this.spec_list_flag = true
            // this.input_spec = ""

        },
        loose_focus () {
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                this.spec_list_flag = false;
            }, 250);

        },
        SearchSpec2 (val) {
            this.$axios.get(this.Ip + "/ModelQuery/" + val).then(res => {
                // console.log(res,"....")
                if (res.data.result == "OK") {
                    // console.log(res,"....")
                    this.options = res.data.content
                    if (this.repeatList.length != 0) {
                        for (var i = 0; i < this.repeatList.length; i++) {
                            for (var j = 0; j < this.options.length; j++) {
                                if (this.repeatList[i].model_id == this.options[j].model_id) {
                                    // console.log(this.options[j],"sps")
                                    this.options[j].select = true
                                }
                            }
                        }
                    }
                } else {
                    this.options = []
                }
            }).catch(res => {
                this.$message({
                    showClose: true,
                    message: '服务异常',
                    type: 'error',
                    duration: 0,
                })
            })
        },
        getSpec2 () {
            this.$axios.get(this.Ip + "/Model").then(res => {
                if (res.data.result == "OK") {
                    // console.log(res,"sp")
                    this.options = res.data.content
                    for (var i = 0; i < this.repeatList.length; i++) {
                        for (var j = 0; j < this.options.length; j++) {
                            if (this.repeatList[i].model_id == this.options[j].model_id) {
                                // console.log(this.options[j],"sps")
                                this.options[j].select = true
                            }
                        }
                    }
                } else {
                    this.options = []
                }
            })
                .catch(res => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0,
                    })
                });
        },

        handleSelect (node, item, data) {
            // console.log(item)
            var double_flag = false;
            for (var i = 0; i < this.repeatList.length; i++) {
                if (item.model_id == this.repeatList[i].model_id) {
                    // this.$alert("您已添加过该式样书","提示")
                    double_flag = true;
                }
            }
            if (double_flag) {
                this.$alert("该模块已被添加", "提示")
            } else {
                this.append(node, item, data)
                this.repeatList.push({ model_id: item.model_id })
            }

            data.key = false;
        },
        append (node, item, data) {
            const newChild = { model_id: item.model_id, title: item.title, model_sub: [], key: false };
            if (!data.model_sub) {
                this.$set(data, 'model_sub', []);
            }
            data.model_sub.push(newChild);

        },
        append_node (data) {
            var falg = this.repeaKey(this.subModelList.model_tree)
            if (falg) {
                data.key = true
            }

        },
        repeaKey (list) {
            // console.log(list,"list")
            let sublist = list
            if (sublist.length == 0) {
                return true
            } else {
                for (var i = 0; i < sublist.length; i++) {
                    if (sublist[i].key == true) {
                        sublist[i].key = false
                    }
                    this.repeaKey(sublist[i].model_sub)
                }
            }
        },
        delete_node (node, data) {
            // console.log(node,"de")
            const parent = node.parent;
            const model_sub = parent.data.model_sub || parent.data;
            const index = model_sub.findIndex(d => d.model_id === data.model_id);
            model_sub.splice(index, 1);
            var rep_index = this.repeatList.indexOf(data.model_id)
            // console.log(rep_index,"chs")
            this.repeatList.splice(rep_index, 1)
            // console.log(this.repeatList,"ch")
        },

        prev () {
            // this.$router.push('/tagl/Project_Step_Three')
            let router_flag = this.$route.query.flag
            let routerValue = { path: '/tagl/Project_Step_Three', query: { flag: router_flag } }
            this.$router.push(routerValue)
        },
        jump_to (index) {
            switch (index) {
                case "项目信息":
                    // this.JumpAndSave()
                    var router_flag = this.$route.query.flag
                    if (this.$route.query.flag == "true") {
                        router_flag = "false"
                    }
                    var routerValue = { path: '/tagl/Project_Step_One', query: { flag: router_flag } }
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_One')
                    break;
                case "平台":
                    // this.JumpAndSave()
                    this.$router.push('/tagl/Project_Step_Two')
                    break;
                case "知识库":
                    // this.JumpAndSave()
                    var router_flag = this.$route.query.flag
                    var routerValue = { path: '/tagl/Project_Step_Three', query: { flag: router_flag } }
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_Three')
                    break;
                case "模块":
                    // this.JumpAndSave()
                    var router_flag = this.$route.query.flag
                    var routerValue = { path: '/tagl/Project_Step_Four', query: { flag: router_flag } }
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_Four')
                    break;
                case "模块负责组":
                    // this.JumpAndSave()
                    var router_flag = this.$route.query.flag
                    var routerValue = { path: '/tagl/Project_Step_Five', query: { flag: router_flag } }
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_Five')
                    break;
                case "5模块负责组":
                    if (this.active > 3) {
                        this.$router.push('/tagl/Project_Step_Five')
                    }
                    break;
            }
        },
        save () {
            if (this.subModelList.model_tree.length == 0) {
                this.$message({
                    message: '请选择模块',
                    type: 'error'
                })
                return
            }
            this.subModelList.proj_id = window.sessionStorage.getItem('proj_id')
            this.$axios.post(this.Ip + '/ProjectModel', this.subModelList)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.judgeAll()
                        this.$message({
                            message: '保存成功',
                            type: 'success'
                        })
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败',
                            type: 'error',
                            duration: 0,
                        })
                    }
                })
                .catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0,
                    })
                })
        },
        next () {
            if (window.sessionStorage.getItem('step_id') == 3) {
                window.sessionStorage.setItem('step_id', 4)
            }
            let router_flag = this.$route.query.flag
            let routerValue = { path: '/tagl/Project_Step_Five', query: { flag: router_flag } }
            this.$router.push(routerValue)
            return//只跳转页面
            if (this.subModelList.model_tree.length == 0) {
                this.$message({
                    message: '请选择模块',
                    type: 'error'
                })
                return
            }
            this.subModelList.proj_id = window.sessionStorage.getItem('proj_id')
            this.$axios.post(this.Ip + '/ProjectModel', this.subModelList)
                .then(res => {
                    if (res.data.result == 'OK') {
                        if (window.sessionStorage.getItem('step_id') == 3) {
                            window.sessionStorage.setItem('step_id', 4)
                        }
                        // this.$router.push('/tagl/Project_Step_Five')
                        let router_flag = this.$route.query.flag
                        let routerValue = { path: '/tagl/Project_Step_Five', query: { flag: router_flag } }
                        this.$router.push(routerValue)
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败',
                            type: 'error',
                            duration: 0,
                        })
                    }
                })
                .catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0,
                    })
                })
        },
        cancel () {
            this.save_data = JSON.stringify(this.subModelList)
            if (this.save_data == this.get_data) {
                window.sessionStorage.removeItem('proj_id')
                window.sessionStorage.removeItem('step_id')
                this.$store.state.fpm_id = 1
                this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        window.sessionStorage.removeItem('proj_id')
                        window.sessionStorage.removeItem('step_id')
                        this.$store.state.fpm_id = 1
                        this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
                    })
                    .catch(() => { })
            }

        },
        Synchronize_module () {
            this.loading = true
            this.$axios.get(this.Ip + '/ImportProjectModel' + '/' + this.proj_name).then(res => {
                if (res.data.result == 'OK') {
                    this.judgeAll()
                    setTimeout(() => {
                        this.$message({
                            type: "success",
                            message: '同步' + res.data.msg
                        })
                        this.loading = false
                    }, 50)
                } else {
                    this.$message({
                        type: "error",
                        message: res.data.msg
                    })
                    this.loading = false
                }
            }).catch(err => {
                console.log(err)
            })
        }
    }
}
</script>
<style scoped>
.add-project-step {
    margin: 0 auto;
    width: 100%;
    height: 100%;
}
.countent {
    max-width: 300px;
    min-width: 200px;
    width: 15%;
    height: 100%;
    padding: 20px;
    float: left;
}
.header-top {
    height: 100px;
}
.header {
    height: 400px;
    padding: 10%;
    clear: both;
}
.mid {
    width: 80%;
    height: 100%;
    float: left;
    padding-top: 40px;
    padding-right: 1%;
    position: relative;
    padding-right: 20px;
    padding-bottom: 55px;
    border-right: 1px solid #ccc;
}
.mid-top {
    position: absolute;
    top: 0;
    bottom: 55px;
    width: 100%;
    padding-right: 20px;
    overflow-y: scroll;
}
.step-one-content {
    margin-top: 20px;
    margin-left: 20px;
}
.footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}

/**/

#Add-File-Mode {
    float: left;
    margin: 0 auto;
    width: 84%;
    height: 100%;
    padding-left: 1%;
    border-left: 1px solid #c0c4cc;
}

.div-center {
    width: 100%;
    text-align: left;
    padding: 0 0 20px;
}
.div-center-label {
    margin-left: 10px;
}

.div-title {
    display: inline-block;
    width: 90px;
    text-align: right;
    margin-right: 20px;
    color: #4d4d4d;
    font-weight: bold;
}
.div-title-ex {
    margin: 0;
    padding: 0;
    width: 100%;
    text-align: left;
}
h2 {
    font-size: 22px;
    font-weight: bolder;
    color: white;
    padding-left: 10px;
    line-height: 26px;
    background-color: #6bcca0;
}
.summary {
    vertical-align: top;
    height: 66px;
    line-height: 66px;
}
.div-input {
    display: inline-block;
    width: 500px;
}
.project_box {
    margin: 20px 0 20px 20px;
}
.project_box_content {
    width: 200px;
    height: 150px;
    line-height: 150px;
    border: 1px solid;
    display: inline-block;
    text-align: center;
}
/**/
.step-one-title {
    margin: 40px 0 20px 0;
}
.step-one-text {
    margin-left: 80px;
}
.checked_input_list {
    margin-left: 20px;
    margin-top: 100px;
    float: left;
    width: 100%;
    height: 400px;
}
.checked_input_list_title {
    margin-bottom: 15px;
    font-size: 18px;
}
.checked_input_list_li {
    list-style: none;
    width: 100%;
    line-height: 30px;
    cursor: pointer;
    font-size: 14px;
}
.step-one-content {
    margin-top: 20px;
    margin-left: 20px;
}
.select-input {
    width: 100%;
}
.sequence_title_text {
    margin-left: 20px;
    margin-bottom: 20px;
    font-size: 14px;
    color: #5e6d82;
}
.select-content {
    position: relative;
    margin-top: 20px;
}
.select-option-box {
    /*position: absolute;*/
    background-color: white;
    z-index: 5;
    margin-top: 10px;
    width: 100%;
    max-height: 150px;
    overflow-y: scroll;
    border: 1px solid #ccc;
    border-radius: 5px;
}
.select-option-li {
    font-size: 14px;
    width: 98%;
    white-space: nowrap;
    list-style: none;
    line-height: 30px;
    padding-left: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #606266;
}
.select-option-li:hover {
    cursor: pointer;
    background-color: #f5f7fa;
}
.one_box {
    /*border:1px dashed red;*/
    width: 100%;
    float: left;
}
.two-box {
    margin-left: 20px;
    /*border:1px dashed #c0c4cc;*/
    width: 500px;
    min-height: 80px;
    float: left;
}
.three_box {
    /*margin-left:40px;*/
    /*border:1px dashed green;*/
}

.checked_title {
    font-size: 18px !important;
    margin: 10px 0 10px 20px;
    /*text-align: center;*/
}
.checked_title_two {
    font-size: 16px !important;
    text-align: center;
}
.checked_title_three {
    font-size: 14px !important;
}
.checked_content_box {
    margin-left: 20px;
    line-height: 30px;
    width: 169px;
}
.content_box {
    border: 1px dashed #c0c4cc;
    width: 80%;
    margin-left: 20px;
}
.one_box_all {
    margin: 10px 0 10px 20px;
}
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}
@media screen and (max-width: 1366px) {
    .mid {
        width: 880px;
    }
}
@media screen and (max-width: 1334px) {
    .countent {
        max-width: 300px;
        min-width: 200px;
        width: 15%;
        height: 100%;
        padding: 20px;
        float: left;
    }
    #Add-File-Mode {
        float: left;
        width: 80%;
        height: 100%;
    }
}
@media screen and (max-width: 1024px) {
    .add-project-step {
        width: 1024px;
    }
    .header-top {
        display: none;
    }
    .header {
        height: 100%;
        padding: 10%;
        clear: both;
    }
    #Add-File-Mode {
        float: left;
        width: 820px;
        height: 100%;
    }
    .mid {
        width: 635px;
    }
    .div-input {
        display: inline-block;
        width: 400px;
    }
}
</style>