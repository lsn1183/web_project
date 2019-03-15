<template>
    <!-- new test -->
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
                    <span>正文</span>
                    <el-form-item label="URL" style="width: 98%;">
                        <el-input type="url" v-model="formData.path" :autosize="{minRows:1,maxRows:2}" @focus="url_input_focus" :disabled="url_flag" placeholder='请输入地址，示例：http://' @change="url_changeVal" clearable>
                            <!-- <template slot="prepend">http://</template> -->
                        </el-input>
                    </el-form-item>
                    <el-form-item label="文件" style="width: 98%">
						<el-upload :data="formData" :limit='2' :on-success="up_success" ref="upload" :action="up_ip" :on-remove="up_Remove" :auto-upload="auto_up_flag" 
            :disabled="up_disable_flag" :drag='true' :on-change="up_change">
							<div class="el-upload__text" id="select-btn" @click="uploadFile_click" ><i class="el-icon-upload"></i>将文件拖到此处，或<em>点击上传</em></div>
                            <span @click="on_upload"></span>
                        </el-upload>
                    </el-form-item>
                    <el-form-item label="文本" style="width: 98%">
                        <el-input type="textarea" v-model="formData.content" size="small" @focus="text_input_focus" @change="text_changeVal" :autosize="{ minRows: 6, maxRows: 20}" :disabled="textarea_flag"></el-input>
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

                <el-form-item label="关键字" style='padding-top: 7px'>
                    <el-input type="text" v-model="formData.keywords" size="small" placeholder="用逗号隔开"></el-input>
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
                <p style="display: block;margin:0px 0 0 0px">Tag选项:</p>
                <el-tree class="filter-tree" :data="datas" ref="tree" show-checkbox :props="defaultProps" :expand-on-click-node="false" node-key="tag_id" :default-expand-all="true" :check-strictly="true">
                    <span class="custom-tree-node" slot-scope="{node,data}" :title="data.remark">
                        <span>{{data.tag}}</span>
                    </span>
                </el-tree>
            </div>
        </div>
        <div class="submit">
            <el-button type="primary" @click="on_submit('form_ref')" size="mini">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
            <el-button type="primary" @click="on_cancel()" size="mini">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
        </div>
    </div>

</template>

<script>
export default {
    components: {},
    created () { },
    watch: {},
    data () {
        return {
            defaultProps: {
                children: "sub_tags",
                label: "tag"
            },
            formData: {
                doc_type: "",
                doc_title: "",
                path: "",
                tags: [],
                summary: "",
                content: "",
                keywords: "",
                sub_cat:'',
                considers: [{ "consider_id": 0, "consider_name": null }],
                failure_mode: [{ "failure_id": 0, "failure_mode_name": null }],
                ver: 1,
                committer: window.sessionStorage.getItem("Uall")
            },
            url_flag: false,
            textarea_flag: false,
            up_ip: this.Ip + "/Doc",
            auto_up_flag: false,
            up_disable_flag: false,
            datas: [],
            data1: [],
            data2: [],
            file_flag: false,
            getData_flag: false,
        };
    },
    mounted () {
        // 右边树:
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
        });
        // 左边树：
        this.$axios.get(this.Ip + "/TagTree/" + "often").then(res => {
            let often_data = res.data.content;
            for (let i = 0; i < often_data.length; i++) {
                if (i <= 1) {
                    this.data1.push(often_data[i]);
                } else {
                    this.data2.push(often_data[i]);
                }
            }
        });
    },
    methods: {
        // 递归方法：
        setTgaFun (val) {
            for (let i = 0; i < val.length; i++) {
                if (val[i].required == true) {
                    val[i].tag += "[必填]"
                } else {
                    self.setTgaFun(val[i].required);
                }
            }
        },
        url_input_focus () {
            // this.$notify({
            //   type: "info",
            //   message: "若添加URL内容，请确认文本内容为空"
            // });
        },
        text_input_focus () {
            // this.$notify({
            //   type: "info",
            //   message: "若添加URL内容，请确认文本内容为空"
            // });
        },
        url_changeVal () {
            let btn = document.getElementById("select-btn");
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
            let btn = document.getElementById("select-btn");
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
        up_success (response) {
            if (response.result == "OK") {
                this.$message({
                    type: "success",
                    message: "成功!"
                });
                this.$store.state.basic_type = new Date().getTime();
                this.$destroy();
                this.$router.back(-1);
            } else {
                this.$message({
                    type: "error",
                    message: "上传失败，文件可能已经存在!!"
                });
            }
        },
        up_change (file,fileList) {
            if (fileList.length == 2) {//自动替换上一个选择文件
                fileList.shift()
            }  
            if (file.uid != "") {
                this.formData.doc_type = "file";
            } else {
                // nothing to do
                return
            }
        },
        up_Remove (file, fileList) {
            this.url_flag = false;
            this.textarea_flag = false;
        },
        // 上传文件函数
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
            if (this.formData.tags != "") {
                // 调用check检查是否勾选
                const tag = this.formData.tags;
                this.check_NodeKey(tag);
                if (this.getData_flag == true) {
                    this.$refs.upload.submit();
                }
            } else {
                this.$alert("请选择tag");
            }
        },
        // 上传文本函数
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
            if (this.formData.tags != "") {
                // 调用check检查是否勾选
                const tag = this.formData.tags;
                this.check_NodeKey(tag);
                if (this.getData_flag == true) {
                    this.$axios.post(this.Ip + "/Doc", this.formData).then(res => {
                        if (res.data.result == "OK") {
                            this.$message({
                                type: "success",
                                message: "添加成功"
                            });
                            this.$store.state.basic_type = new Date().getTime();
                            this.$destroy();
                            this.$router.back(-1);
                        } else {
                            this.$message({
                                type: "error",
                                message: "添加失败"
                            });
                        }
                    })
                }
            } else {
                this.$alert("请选择tag");
            }
        },
        // 确认按钮
        on_submit () {
            if (this.formData.doc_type == "text" || this.formData.doc_type == "url") {
                this.on_upload_doc();
            } else if (this.formData.doc_type == "file") {
                this.url_flag = true;
                this.textarea_flag = true;
                this.on_upload();
            } else {
                this.$message({
                    type: "warning",
                    message: "新增文档没有填写完整，请检查"
                });
            }
        },
        on_cancel () {
            this.formData.doc_type = "";
            this.$destroy();
            this.$router.back(-1);
        },
        uploadFile_click () {
            if (this.up_disable_flag == true) {
                return;
            } else {
                if (this.formData.content == "" && this.formData.path == "") {
                    this.url_flag = true;
                    this.textarea_flag = true;
                } else if (
                    this.formData.content == null &&
                    this.formData.path == null
                ) {
                    this.url_flag = true;
                    this.textarea_flag = true;
                } else {
                    this.url_flag = false;
                    this.textarea_flag = false;
                    this.$notify({
                        type: "warning",
                        message: this.globalData.hint.warning_editForm_uploadFile
                    });
                }
            }
        },
        // check是否勾选了必填tag项：
        check_NodeKey (tag) {
            let check = tag;
            let tagData = JSON.parse(window.sessionStorage.getItem("tagData"));//在form页面存储
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
        // 考虑点：
        addConsider () {
            this.formData.considers.push({ "consider_id": 0, "consider_name": null })
        },
        deleteConsider (item, index) {
            if (this.formData.considers.length == 1) {
                this.$notify({
                    type: 'warning',
                    message: "已是最后一个无法删除"
                })
            } else {
        this.formData.considers.splice(index,1);
            }
        },
        addFailureMode () {
            this.formData.failure_mode.push({ "failure_id": 0, "failure_mode_name": null })
        },
        delete_failure_mode (item, index) {
            if (this.formData.failure_mode.length == 1) {
                this.$notify({
                    type: 'warning',
                    message: "已是最后一个无法删除"
                })
            } else {
                this.formData.failure_mode.splice(index, 1);
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
