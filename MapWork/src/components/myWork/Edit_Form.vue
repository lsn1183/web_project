<template>
    <div id="add-form" class="wrapper">
        <div class="form-item">
            <el-form :model="formData" label-width="85px" ref='form_ref'>
                <el-form-item label="标题">
                    <el-input type="text" v-model="formData.doc_title" size="small" clearable></el-input>
                </el-form-item>
                <el-form-item label="子分类">
                    <el-input type="text" v-model="formData.sub_cat" size="small" clearable></el-input>
                </el-form-item>
                <el-form-item label="摘要">
                    <el-input type="textarea" v-model="formData.summary" size="small" :autosize="{ minRows: 6, maxRows: 20}"></el-input>
                </el-form-item>
                <el-form-item label="">
                    <el-tree class="filter-tree" :data="data1" node-key="tag_id" ref="tree1" show-checkbox :props="defaultProps" :expand-on-click-node="false" :default-expand-all="true" :check-strictly="true"></el-tree>
                </el-form-item>
                <div class="form-border">
                    <span>正文:</span>
                    <el-form-item label="URL" style="width: 98%;">
                        <el-input type="" v-model="formData.path" :autosize="{minRows:1,maxRows:2}" :disabled="url_flag" @focus="url_input_focus" placeholder='请输入地址，示例：http://' @change="url_changeVal" clearable>
                        </el-input>
                    </el-form-item>
                    <el-form-item label="文件" style="width: 98%">
                        <el-upload :data="formData" :limit='2' :on-success="up_success" ref="upload" :on-remove="up_remove" :action="up_ip" :on-change="up_change" :auto-upload="auto_up_flag" :disabled="up_disable_flag" :drag='true' :before-remove='before_remove'>
                            <div class="el-upload-text" id="select_btn" @click="uploadFile_click"><i class="el-icon-upload "></i>修改文件拖到此处，或<em>点击上传</em></div>
                            <!-- <span @click="on_upload"></span><span style="font-size:12px">{{fileName_show}}</span> -->
                        </el-upload>
                        <div >
                            <span @click="on_upload"></span><span style="font-size:12px">{{fileName_show}} </span>
                            <i class="el-icon-close margin-left" @click="delete_file()" v-if="fileName_show"></i>
                        </div>
                    </el-form-item>
                    <el-form-item label="文本" style="width: 98%">
                        <el-input type="textarea" v-model="formData.content" @focus="text_input_focus" size="small" :autosize="{ minRows: 8, maxRows: 20}" :disabled="textarea_flag" @change="text_changeVal"></el-input>
                    </el-form-item>
                    <el-form-item label="">
                        <el-tree class="filter-tree" :data="data2" node-key="tag_id" ref="tree2" show-checkbox :props="defaultProps" :expand-on-click-node="false" :default-expand-all="true" :check-strictly="true"></el-tree>
                    </el-form-item>
                </div>
                <!-- 新增failure mode -->
                <div class="form-border">
                    <span>failure mode</span>&nbsp;&nbsp;
                    <span style="font-size:12px;cursor: pointer;" @click="addFailureMode">[&nbsp;添&nbsp;加&nbsp;]</span>
                    <el-form-item label="" style="width: 98%;">
                        <li v-for="(item,index) in formData.failure_mode" :key="index">
                            {{index+1}}&nbsp;
                            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 6}" v-model="item.failure_mode_name"></el-input>
                            <i style="font-style: normal;font-size: 12px;font-weight: 300;cursor: pointer;" @click="delete_failure_mode(item,index)">[&nbsp;删&nbsp;除&nbsp;]</i>
                        </li>
                    </el-form-item>
                </div>
                <!-- 新增考虑点 -->
                <div class="form-border">
                    <span>考虑点</span>&nbsp;&nbsp;
                    <span style="font-size:12px;cursor: pointer;" @click="addConsider">[&nbsp;添&nbsp;加&nbsp;]</span>
                    <el-form-item label="" style="width: 98%;">
                        <li v-for="(item,index) in formData.considers" :key="index">
                            {{index+1}}&nbsp;
                            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 6}" v-model="item.consider_name"></el-input>
                            <i style="font-style: normal;font-size: 12px;font-weight: 300;cursor: pointer;" @click="deleteConsider(item,index)">[&nbsp;删&nbsp;除&nbsp;]</i>
                        </li>

                    </el-form-item>
                </div>
                <el-form-item label="关键字：" style='padding-top: 7px'>
                    <el-input type="text" v-model="formData.keywords" size="small" placeholder="用逗号隔开"></el-input>
                </el-form-item>
                <el-form-item label="作者">
                    <el-input type="text" v-model="formData.author" size="small" :disabled="true"></el-input>
                </el-form-item>

                <el-form-item label="创建时间" style='padding-top: 7px'>
                    <el-input type="text" v-model="formData.create_time" :disabled="true" size="small"></el-input>
                </el-form-item>
                <el-form-item label="版本" style='padding-top: 7px'>
                    <el-input type="text" v-model="formData.ver" :disabled="true" size="small"></el-input>
                </el-form-item>
                <el-form-item label="提交人">
                    <el-input type="text" v-model="formData.committer" :disabled="true" size="small"></el-input>
                </el-form-item>
            </el-form>
        </div>
        <!-- Tag树 -->
        <div class="tree">
            <div style="display: inline-block;height:auto;margin-left:10px">
                <p style="display: block;">Tag选项</p>
                <el-tree class="filter-tree" :data="datas" node-key="tag_id" :default-checked-keys="this.tree_checked_keys" ref="tree" show-checkbox :props="defaultProps" :expand-on-click-node="false" :default-expand-all="true" :check-strictly="true">
                    <span class="custom-tree-node" slot-scope="{node,data}" :title="data.remark">
                        <span>{{data.tag}}</span>
                    </span>
                </el-tree>
            </div>

        </div>
        <div class="submit">
            <el-button type="primary" @click="on_submit()" size="mini">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
            <el-button type="primary" @click="on_cancel()" size="mini">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
        </div>
    </div>
</template>
<script>
export default {
    components: {},
    created () { },
    computed: {
        getUserIcon () {
            return this.$store.state.form_item_id
        }
    },
    watch: {
        getUserIcon (val) {
            this.ListItem_Fun(val);
        }
    },
    data () {
        return {
            defaultProps: {
                children: "sub_tags",
                label: "tag"
            },
            formData: {},
            up_ip: this.Ip + "/UpdateDoc",
            url_flag: false,
            auto_up_flag: false,
            up_disable_flag: false,
            textarea_flag: false,
            datas: [],
            data1: [],
            data2: [],
            file_flag: false,
            tree_checked_keys: [],
            Tags: [],
            getData_flag: false,
            up_fileName: "",
            fileName_show: ''
        };
    },
    mounted () {
        let doc_id = JSON.parse(window.sessionStorage.getItem("doc_id"));
        this.ListItem_Fun(doc_id);
    },
    methods: {
        // 编辑页面主函数
        ListItem_Fun (val) {
            let doc_id = val;
            this.$axios.get(this.Ip + "/Doc/" + doc_id).then(res => {
                const val = res.data.content
                this.defaulte(val);
            }),
                // 右边树：
                this.$axios.get(this.Ip + "/TagTree/" + "normal").then(res => {
                    let data = res.data.content;
                    for (let i = 0; i < data.length; i++) {
                        if (data[i].required == true) {
                            data[i].tag += "[必填]"
                        } else {
                            break
                        }
                    }
                    this.datas = data;
                }),
                // 左边树：
                this.$axios.get(this.Ip + "/TagTree/" + "often").then(res => {
                    let often_data = res.data.content;
                    let array1 = [];
                    let array2 = [];
                    for (let i = 0; i < often_data.length; i++) {
                        if (i <= 1) {
                            array1.push(often_data[i]);
                        } else {
                            array2.push(often_data[i]);
                        }
                    }
                    this.data1 = Array.from(new Set((array1)));
                    this.data2 = Array.from(new Set((array2)));
                });
        },
        //   默认加载页面时候调用函数：
        defaulte (val) {
            let form_item = val;
            let btn = document.getElementById("select_btn");
            if (form_item.file != "" && form_item.file != '') {
                this.fileName_show = form_item.file_name
                // 存在已上传文件关闭url/text框
                this.textarea_flag = true
                this.url_flag = true
            }else if(form_item.content != ''){
                this.url_flag = true
                this.up_disable_flag = true
                btn.style.color = "#c0c4cc";
                btn.style.backgroundColor = "#f5f7fa";
                btn.style.borderColor = "#e4e7ed";
            }else if(form_item.path != ''){
                this.textarea_flag = true
                this.up_disable_flag = true
                btn.style.color = "#c0c4cc";
                btn.style.backgroundColor = "#f5f7fa";
                btn.style.borderColor = "#e4e7ed";
            }
            this.formData = form_item
            this.tags = form_item.tags
            this.tree_checked_keys = [];
            let usedKeys = [];
            for (let i = 0; i < form_item.tags.length; i++) {
                if (
                    form_item.tags[i].tag_id == 94 ||
                    form_item.tags[i].tag_id == 95 ||
                    form_item.tags[i].tag_id == 96 ||
                    form_item.tags[i].tag_id == 97
                ) {
                    usedKeys.push(form_item.tags[i].tag_id);
                } else {
                    this.tree_checked_keys.push(form_item.tags[i].tag_id);
                }
            }
            this.$refs.tree1.setCheckedKeys(usedKeys);
            this.$refs.tree2.setCheckedKeys(usedKeys);
        },
        url_input_focus () {
            // this.$notify({
            //   type: "info",
            //   message: "若想上传URL内容，请确认已清空文本内容"
            // });
        },
        text_input_focus () {
            // this.$notify({
            //   type: "info",
            //   message: "若想上传文本内容，请确认已清空URL内容"
            // });
        },
        url_changeVal () {
            let btn = document.getElementById("select_btn");
            if (this.formData.path != "") {
                this.up_disable_flag = true;
                this.textarea_flag = true;
                this.formData.doc_type = "url";
                btn.style.color = "#c0c4cc";
                btn.style.backgroundColor = "#f5f7fa";
                btn.style.borderColor = "#e4e7ed";
                // DOM的em元素：
                btn.lastChild.style.color = "#c0c4cc";
            } else {
                this.up_disable_flag = false;
                this.textarea_flag = false;
                btn.style.backgroundColor = "#FFFFFF";
                btn.style.color = "#42b983";
                btn.style.borderColor = "#42b983";
                btn.lastChild.style.color = "#409eff";
            }
        },
        text_changeVal () {
            let btn = document.getElementById("select_btn");
            if (this.formData.content != "") {
                this.url_flag = true;
                this.up_disable_flag = true;
                this.formData.doc_type = "text";
                btn.style.color = "#c0c4cc";
                btn.style.backgroundColor = "#f5f7fa";
                btn.style.borderColor = "#e4e7ed";
                btn.lastChild.style.color = "#c0c4cc";
            } else {
                this.up_disable_flag = false;
                this.url_flag = false;
                btn.style.backgroundColor = "#FFFFFF";
                btn.style.color = "#42b983";
                btn.style.borderColor = "#42b983";
                btn.lastChild.style.color = "#409eff";
            }
        },
        // 文件上传函数
        on_upload (item) {
            let node = this.$refs.tree.getCheckedNodes();
            let node1 = this.$refs.tree1.getCheckedNodes();
            let node2 = this.$refs.tree2.getCheckedNodes();
            this.Tags = [];
            if (node.length != 0 || node1.length != 0 || node2.length != 0) {
                for (let i = 0; i < node.length; i++) {
                    const element = node[i].tag_id;
                    this.Tags.push(element);
                }
                for (let i = 0; i < node1.length; i++) {
                    const element = node1[i].tag_id;
                    this.Tags.push(element);
                }
                for (let i = 0; i < node2.length; i++) {
                    const element = node2[i].tag_id;
                    this.Tags.push(element);
                }
            }
            this.formData.tags = this.Tags;
            // console.log(this.formData, "this.formData111111");
            if (this.formData.tags.length != 0) {
                // 调用check检查是否勾选
                const tag = this.formData.tags;
                this.check_NodeKey(tag);
                if (this.getData_flag == true) {
                    if (this.up_fileName != '') {
                        this.$refs.upload.submit();
                    } else {
                        this.$axios.put(this.Ip + "/Doc", this.formData).then(res => {
                            this.$message({
                                type: "success",
                                message: "修改成功"
                            });
                            this.$destroy();
                            this.$router.back(-1);
                        }).catch(err => {
                            this.$message({
                                type: "error",
                                message: "失败"
                            });
                        });
                    }
                }
            } else {
                this.$message({
                    type: "error",
                    message: "tag没选，请查看"
                })
            }
        },
        // 文本内容上传函数
        on_upload_doc () {
            let node = this.$refs.tree.getCheckedNodes();
            let node1 = this.$refs.tree1.getCheckedNodes();
            let node2 = this.$refs.tree2.getCheckedNodes();
            this.Tags = [];
            if (node.length != 0 || node1.length != 0 || node2.length != 0) {
                for (let i = 0; i < node.length; i++) {
                    const element = node[i].tag_id;
                    this.Tags.push(element);
                }
                for (let i = 0; i < node1.length; i++) {
                    const element = node1[i].tag_id;
                    this.Tags.push(element);
                }
                for (let i = 0; i < node2.length; i++) {
                    const element = node2[i].tag_id;
                    this.Tags.push(element);
                }
            }
            this.formData.tags = this.Tags;
            if (this.formData.tags.length != 0) {
                // 调用check检查是否勾选
                const tag = this.formData.tags;
                this.check_NodeKey(tag);
                if (this.getData_flag == true) {
                    this.$axios.put(this.Ip + "/Doc", this.formData).then(res => {
                        this.$message({
                            type: "success",
                            message: "修改成功"
                        });
                        let routerValue = { path: '/tagl/Form_Modle', query: { page: this.$route.query.page } }
                        this.$router.push(routerValue);
                    }).catch(err => {
                        this.$message({
                            type: "error",
                            message: "失败"
                        });
                    });
                }
            } else {
                this.$message({
                    type: "error",
                    message: "tag没选，请查看"
                })
            }

        },
        // 确认按钮
        on_submit () {
            if (this.formData.path == "" && this.formData.content == "" && this.up_disable_flag == false && this.textarea_flag == false && this.url_flag == false) {
                if(this.fileName_show ==''){
                    this.$alert("正文内容不能全部为空，警告！");
                    return
                }
            }//限定url/文本/文件都为空禁止上传
            if (this.formData.doc_type == "text") {//文本判断
                if (this.formData.path == "") {
                    this.on_upload_doc();
                } else {
                    this.$alert("上传文本，请清空URL地址栏");
                    this.url_flag = false;
                }
            } else if (this.formData.doc_type == "url") {//url地址判断
                if (this.formData.content == "") {
                    this.on_upload_doc();
                } else {
                    this.$alert("上传url，请清空文本框");
                    this.textarea_flag = false;
                }
            } else if (this.formData.doc_type == "file") {//文件判断
                if (this.url_flag == true && this.textarea_flag == true) {//url和文本框是否已disabled
                    this.on_upload();
                } else {
                    if (this.fileName_show != '') {
                        this.on_upload();
                    } else {
                        if (this.formData.path != '' && this.formData.content != '') {
                            this.$confirm('此操作上传文件需清空url和文本框，是否继续?', '提示', {
                                confirmButtonText: "确定",
                                cancelButtonText: "取消",
                                type: 'warning'
                            }).then(() => {
                                this.url_flag = true;
                                this.textarea_flag = true;
                                this.formData.path = null;
                                this.formData.content = null;
                            }).catch(() => {
                                this.url_flag = false;
                                this.textarea_flag = false;
                            })
                        } else {
                            this.url_flag = true;
                            this.textarea_flag = true;
                            this.formData.path = null;
                            this.formData.content = null;
                        }

                    }
                }
            } else {
                this.$message({
                    type: "error",
                    message: "该条编辑内容没有添加完整，请确认"
                });
            }
        },
        delete_file () {
            this.fileName_show = ''
            this.textarea_flag = false
            this.url_flag = false
        },
        on_cancel () {
            this.formData.doc_type = "";
            let routerValue = { path: '/tagl/Form_Modle', query: { page: this.$route.query.page } }
            this.$router.push(routerValue);
        },
        //文件上传成功回调函数
        up_success (response) {
            if (response.result == "OK") {
                this.$message({
                    type: "success",
                    message: "成功!"
                });
                this.$destroy();
                this.$router.back(-1);
            } else {
                this.$message({
                    type: "error",
                    message: "上传失败，文件可能已经存在!!"
                });
            }
        },
        up_change (file, fileList) {
            if (fileList.length == 2) {//自动替换上一个选择文件
                fileList.shift()
            }  
            if (file.uid != "") {
                this.formData.doc_type = "file";
                this.formData.path = '';
                this.formData.content = '';
                this.url_flag = true;
                this.textarea_flag = true;
                this.up_fileName = file.name;
                if (this.formData.content == "" && this.formData.path == '') {//检测是否已选择文件，关闭url/text文本框输入
                    this.url_flag = true;
                    this.textarea_flag = true;
                } 
            } else {
                this.up_fileName = ""
            }
        },
        before_remove (file, fileList){
        },
        up_remove (file) {
            this.url_flag = false;
            this.textarea_flag = false;
        },
        uploadFile_click () {
            if (this.up_disable_flag == true) {
                return;
            }
            //  else {
            //     if (this.formData.content == "" && this.formData.path == '') {
            //         this.url_flag = true;
            //         this.textarea_flag = true;
            //     } else if (this.formData.content == '' && this.formData.path == "") {
            //         this.url_flag = true;
            //         this.textarea_flag = true;
            //     } else {
            //         // console.log(this.formData.content,this.formData.path)
            //         return
            //         this.$notify({
            //             type: "warning",
            //             message: this.globalData.hint.warning_editForm_uploadFile
            //         })
            //     }
            // }
        },
        // check是否勾选了必填tag项：
        check_NodeKey (tag) {
            let check = tag;
            let tagData = JSON.parse(window.sessionStorage.getItem("tagData"));
            var sortFun = function (a, b) {
                return a - b;
            };
            for (let i = 0; i < tagData.length; i++) {
                var check_result = check.filter(v => tagData[i].includes(v));
                if (check_result.length != 0) {
                    this.getData_flag = true;
                } else {
                    this.$notify({
                        type: "warning",
                        message: this.globalData.hint.warning_editForm_tag
                    });
                    this.getData_flag = false;
                    break;
                }
            };
        },
        // ：
        addFailureMode () {
            if (this.formData.failure_mode) {
                this.formData.failure_mode.push({ "failure_id": 0, "failure_mode_name": null })
            }
        },
        delete_failure_mode (item, index) {
            if (item) {
                if (this.formData.failure_mode.length == 0) {
                    this.$notify({
                        type: 'warning',
                        message: "已无法删除"
                    })
                } else {
                    this.formData.failure_mode.splice(index, 1)
                }
            }
        },
        // 考虑点：
        addConsider () {
            if (this.formData.considers) {
                this.formData.considers.push({ "consider_id": 0, "consider_name": null })
            }
        },
        deleteConsider (item, index) {
            if (item) {
                if (this.formData.considers.length == 0) {
                    this.$notify({
                        type: 'warning',
                        message: "已无法删除"
                    })
                } else {
                    this.formData.considers.splice(index, 1)
                }
            }

        }
    }
};
</script>

<style scoped>
.wrapper {
    height: 100%;
    width: 100%;
    min-width: 360px;
    text-align: left;
    margin-top: 10px;
    padding-left: 1%;
    position: relative;
    font-size: 14px;
    color: #606266;
}
.margin-left {
    margin-left: 10%;
    cursor: pointer;
}
.form-item {
    display: block;
    width: 100%;
    max-height: 85%;
    overflow: auto;
}
.el-form {
    width: 80%;
    height: 80%;
}
.tree {
    display: block;
    position: absolute;
    top: 0;
    right: 0;
    width: 25%;
    max-height: 80%;
    overflow: auto;
    padding-left: 1%;
    padding-top: 1%;
}

#select_btn {
    color: #42b983;
    border-color: #42b983;
    background-color: #ffffff;
}

.form-item p {
    display: inline-block;
    margin-bottom: 10px;
}

.submit {
    position: absolute;
    bottom: 20px;
    right: 20px;
}
.submit :after {
    content: "";
    display: block;
    height: 0;
    clear: both;
    visibility: hidden;
}
.form-border {
    border: 1px solid rgba(231, 228, 228, 0.959);
    border-radius: 10px;
    width: 78%;
    padding-top: 2px;
    margin-left: 25px;
    background: #f3f7f8;
    margin-bottom: 5px;
}
li {
    display: inline-flex;
    width: 100%;
    list-style: none;
    vertical-align: middle;
}

.filter-tree {
    margin-left: 10px;
}
@media screen and (max-width: 1024px) {
    .wrapper {
        height: 100%;
        width: 100%;
        min-width: 240px;
        font-size: 12px;
    }
    .form-item {
        width: 70%;
        overflow: auto;
        max-height: 80%;
    }

    .tree {
        width: 30%;
        max-height: 80%;
    }
}
@media screen and (max-width: 1366px) {
    .wrapper {
        min-width: 280px;
        font-size: 12px;
    }
    .form-item {
        width: 100%;
    }
    .tree {
        width: 30%;
        max-height: 80%;
    }
}
</style>
