<template>
    <div class="Add-File-Title">
        <div class="Add-File-Title-nav">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="详细设计" icon="el-icon-edit" status="process">1</el-step>
                    <el-step class="jump" title="式样书">2</el-step>
                    <el-step class="jump" title="Usecase">3</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Title">
            <div class="mid">
                <div class="mid-top">
                    <div class="div-centers">
                        <div class="div-title div-title-ex">
                            <h2>详细设计</h2>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">选择基本设计:</div>
                        <div class="div-input">
                            <el-select v-model="basic_model" placeholder="请选择" clearable @change="optionChangeValue(A)" @visible-change="getBasicOptions" :disabled="select_option_flag" @clear="clearClick">
                                <el-option v-for="item in basic_options" :key="item.doc_id" :label="item.title" :value="JSON.stringify(item)">
                                </el-option>
                            </el-select>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">拷贝基本设计:</div>
                        <div class="div-input">
                            <el-checkbox v-model="checked_copy" @change="checkboxChangeValue" label="拷贝已选择的基本设计" :disabled="checked_basic_flag"></el-checkbox>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">标题:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.title"></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title summary">概述:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.summary" type="textarea" :autosize="{ minRows: 3, maxRows:6}"></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">版本:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.ver" disabled></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label">
                        <div class="div-title">文档创建者:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.creator" disabled></el-input>
                        </div>
                    </div>
                    <div class="div-center div-center-label" style="margin-left:10px">
                        <div class="div-title">文档更新者:</div>
                        <div class="div-input">
                            <el-input v-model="file_form.editor" disabled></el-input>
                        </div>
                    </div>
                </div>
                <div class="min-footer">
                    <div class="div-input input-btn">
                        <el-button size="mini" type="info" disabled>
                            <i class="el-icon-arrow-left"></i>上一步</el-button>
                        <el-button @click="save()" type="primary" size='mini'>&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                        <el-button @click="cancel()" type="primary" size='mini'>&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                        <el-button size="mini" type="primary" @click="next">下一步
                            <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            file_form: {
                doc_type: 'DETAIL',
                title: '',
                ver: 0.01,
                creator: window.sessionStorage.getItem('Uall'),
                editor: window.sessionStorage.getItem('Uall'),
                summary: '',
                model_id: JSON.parse(window.sessionStorage.getItem('treeNodeId')).model_id,
                proj_id: JSON.parse(window.sessionStorage.getItem('treeNodeId')).proj_id,
                basic_doc_id: null,
                copy_on: false
            },
            doc_id: null,
            active: 0,
            basic_model: "",
            basic_options: [],
            select_option_flag: false,
            checked_basic_flag: true,
            checked_copy: false,
            detailData: {},
            height_light_data: null,
            A: false,
            dbrfmFlag: false,
            doc_id: null
        }
    },
    mounted () {
        if (this.$route.query.params) {
            this.detailData = JSON.parse(this.$route.query.params)
            this.dbrfmFlag = this.detailData.dbrfmFlag
        }
    },
    methods: {
        getBasicOptions (A) {
            // 判断条件，防止多次请求数据
            if (A == true && this.basic_options.length == 0) {
                this.$axios.get(this.Ip + "/CopyBasicToDetail/" + this.detailData.proj_id + "/" + this.detailData.model_id).then(res => {
                    if (res.data.result == "OK") {
                        // console.log(res,"选项框")
                        this.basic_options = res.data.content
                    } else {
                        this.$message({
                            type: "error",
                            message: "无数据"
                        })
                    }
                })
            } else {
                return
            }
        },
        clearClick () {
            // 点清除按钮时候，
            this.basic_model = ''
            this.file_form.title = ''
            this.file_form.summary = ''
            this.checked_copy = false
            this.file_form.copy_on = false
        },
        optionChangeValue () {
            if (this.checked_copy == true) {
                if (this.basic_model != "") {
                    let model = JSON.parse(this.basic_model)
                    if (model.title.search("基本设计") != -1) {
                        this.file_form.title = model.title.replace("基本设计", "详细设计")
                    } else if (model.title.toLowerCase().search("basic") != -1) {
                        this.file_form.title = model.title.replace(/basic/i, "Detail")
                    } else {
                        this.file_form.title = model.title + "_详细设计"
                    }
                    this.file_form.summary = model.summary
                    this.file_form.copy_on = true
                    this.file_form.basic_doc_id = model.doc_id
                }
            } else {
                if (this.basic_model) {
                    this.checked_basic_flag = false
                } else {
                    // 控制拷贝开关
                    this.checked_basic_flag = true
                    // 拷贝打钩清除
                    this.checked_copy = false
                }
            }
        },
        checkboxChangeValue () {
            // console.log(this.file_form,"ssss")
            if (this.checked_copy == true) {
                if (this.basic_model != "") {
                    let model = JSON.parse(this.basic_model)
                    if (model.title.search("基本设计") != -1) {
                        this.file_form.title = model.title.replace("基本设计", "详细设计")
                    } else if (model.title.toLowerCase().search("basic") != -1) {
                        this.file_form.title = model.title.replace(/basic/i, "Detail")
                    } else {
                        this.file_form.title = model.title + "_详细设计"
                    }
                    this.file_form.summary = model.summary
                    this.file_form.copy_on = true
                    this.file_form.basic_doc_id = model.doc_id
                } else {
                    this.file_form.title = ""
                    this.file_form.summary = ""
                    this.file_form.copy_on = false
                    this.file_form.basic_doc_id = null
                }
            } else {
                this.file_form.title = ""
                this.file_form.summary = ""
                this.file_form.copy_on = false
            }
            return
        },
        save (type) {
            if (this.file_form.title != "") {
                this.$axios.post(this.Ip + '/DSDoc', this.file_form).then(res => {
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('DocId', res.data.doc_id)
                        this.$store.commit('amendDocId', res.data.doc_id)
                        this.$message({
                            message: '保存成功',
                            type: 'success'
                        })
                        this.doc_id = res.data.doc_id
                        window.sessionStorage.setItem("Step-Asa", 1)
                        window.sessionStorage.setItem("DocId", res.data.doc_id)
                        this.call_back_get_data_fun(res.data.doc_id)
                        if (type == 'next') {
                            this.$router.push({ path: "/tagl/edit_input", query: { pamams: this.dbrfmFlag } })
                        }
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败:' + res.data.error,
                            type: 'error'
                        })
                    }
                }).catch(err => {
                    this.$message({
                        showClose: true,
                        message: '保存失败',
                        type: 'error'
                    })
                })
            } else {
                this.$alert("标题不可为空 !", { title: '提示' })
            }
        },
        call_back_get_data_fun (doc_id) {
            this.$axios.get(this.Ip + "/DSDoc/" + doc_id).then(res => {
                if (res.data.result == "OK") {
                    this.file_form = res.data.content
                    this.height_light_data = this.detailData
                    if (res.data.content.copy_on == true) {
                        this.select_option_flag = true
                        this.checked_basic_flag = true
                    }
                } else {
                    this.$message({
                        message: '请求数据失败',
                        type: 'error'
                    })
                }
            })
        },
        cancel () {
            if (this.doc_id === null) {
                this.$router.push({ path: "/tagl/File_design/basic_design_template", query: { params: JSON.stringify(this.detailData) } })
                if (window.sessionStorage.removeItem("previewPurviewManageData")) {
                    window.sessionStorage.removeItem("previewPurviewManageData")
                }
                window.sessionStorage.removeItem("Step-Asa")
                window.sessionStorage.removeItem("DocId")
            } else {
                window.sessionStorage.setItem("previewPurviewManageData", JSON.stringify(this.detailData))
                window.sessionStorage.removeItem("Step-Asa")
                this.$router.push({ path: '/tagl/File_design/Preview/' + this.doc_id, query: { preview: JSON.stringify(this.detailData) } })
            }
        },
        next () {
            this.save('next')
        }
    }
}
</script>

<style scoped>
.Add-File-Title {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}
.Add-File-Title-nav {
    max-width: 300px;
    min-width: 200px;
    width: 15%;
    height: 100%;
    padding: 20px;
    float: left;
    border-right: 1px solid #c0c4cc;
}
.mid {
    width: 80%;
    height: 100%;
    float: left;
    padding-top: 40px;
    border-right: 1px solid #c0c4cc;
    padding-right: 1%;
    /*overflow-y: scroll;*/
    position: relative;
}
.mid-top {
    position: absolute;
    top: 0;
    bottom: 55px;
    width: 100%;
    padding-right: 20px;
    overflow-y: scroll;
}
.footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}
.min-footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}
#Add-File-Title {
    float: left;
    margin: 0 auto;
    width: 84%;
    height: 100%;
    padding-left: 1%;
}

.div-center {
    width: 100%;
    text-align: left;
    padding: 0 0 20px;
}
.div-centers {
    width: 100%;
    text-align: left;
    margin: 40px 0 0 0;
    padding: 0 0 20px;
}
.div-center-label {
    margin-left: 10px;
}
.div-center-label:last-child {
    margin: 0;
}
.div-title {
    display: inline-block;
    width: 100px;
    text-align: right;
    margin-right: 20px;
    color: #4d4d4d;
    font-weight: bold;
    font-size: 15px;
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

.input-btn {
    text-align: right;
    width: 100%;
}
#Add-File-Title .el-input__inner {
    height: 36px;
    line-height: 36px;
}
.header-top {
    height: 100px;
}
.header {
    height: 225px;
    padding: 10%;
    clear: both;
}
@media screen and (max-width: 1366px) {
    .mid {
        width: 880px;
    }
    .right {
        width: 20%;
        height: 100%;
        float: left;
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
    #Add-File-Title {
        float: left;
        width: 80%;
        height: 100%;
    }
}
@media screen and (max-width: 1024px) {
    .Add-File-Title {
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
    #Add-File-Title {
        float: left;
        width: 820px;
        height: 100%;
    }
    .mid {
        width: 635px;
    }
    .div-input {
        display: inline-block;
        width: 380px;
    }
}
</style>
