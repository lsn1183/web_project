<template>
    <div id="Scene">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="场景(必填)">1</el-step>
                    <el-step class="jump" title="修改点影响点(必填)" icon="el-icon-edit" status="process">2</el-step>
                    <el-step class="jump" title="考虑点(必填)">3</el-step>
                    <el-step class="jump" title="DRBFM(必填)" >4</el-step>
                </el-steps>
            </div>
        </div>
        <div class="cbody">
            <div class="mid">
                <div class="mid-top">
                    <div class="scene-title">
                        <h2 style="fontSize: 22px;fontWeight:bolder;backgroundColor:#6bcca0; color: white;lineHeight: 25px;height:25px">
                            <span style="lineHeight:25px;float:left;paddingLeft: 10px;">场景</span>
                            <i class="el-icon-question" style="fontSize:15px; lineHeight:25px;float:left;marginLeft:5px" title="这里的修改点和影响点，就是DRBFM的变更点和变化点。"></i>
                        </h2>
                    </div>

                    <div style="height: auto;">
                        <div class="checkBox">
                            <div class="checked-input-list-title">填写修改点和影响点</div>
                            <div class="big-box">
                                <div class="checked-input-list">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th rowspan="2">主项目</th>
                                                <th rowspan="2">场景</th>
                                                <th colspan="2">修改点</th>
                                                <th colspan="2">影响点</th>
                                                <th rowspan="2">操作</th>
                                            </tr>
                                            <tr>
                                                <th>修改前</th>
                                                <th>修改后</th>
                                                <th>影响前</th>
                                                <th>影响后</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <template v-for="(item, index) in step2.content">
                                                <tr :class="index%2 == 1 ? 'gray_col': ''">
                                                    <td :rowspan="item.changes.length" :title="item.parent_tag">{{item.parent_tag}}</td>
                                                    <td :rowspan="item.changes.length" :title="item.parent_tag">{{item.tag}}</td>
                                                    <td>
                                                        <el-input type="textarea" resize="none" :rows="3" :autosize="{ minRows: 3, maxRows: 3}" v-model="item.changes[0].before_change" :title="item.changes[0].before_change"></el-input>
                                                    </td>
                                                    <td>
                                                        <el-input type="textarea" resize="none" :rows="3" :autosize="{ minRows: 3, maxRows: 3}" v-model="item.changes[0].change" :title="item.changes[0].change"></el-input>
                                                    </td>
                                                    <td>
                                                        <el-input type="textarea" resize="none" :rows="3" :autosize="{ minRows: 3, maxRows: 3}" v-model="item.changes[0].before_influence" :title="item.changes[0].before_influence"></el-input>
                                                    </td>
                                                    <td>
                                                        <el-input type="textarea" resize="none" :rows="3" :autosize="{ minRows: 3, maxRows: 3}" v-model="item.changes[0].influence" :title="item.changes[0].influence"></el-input>
                                                    </td>
                                                    <td>
                                                        <div style="display: inline-block;width: 102px;">
                                                            <span class="append-span" @click="add_opt(index, 0)"> &nbsp;[ 新增 ]</span>
                                                            <span class="append-span" @click="del_opt(index, 0)" v-if="item.changes.length !== 1"> &nbsp;[ 删除 ]</span>
                                                        </div>
                                                    </td>
                                                </tr>
                                                <tr :class="index%2 == 1 ? 'gray_col': ''" v-for="son_item in item.changes.length - 1">
                                                    <td>
                                                        <el-input type="textarea" resize="none" :rows="3" :autosize="{ minRows: 3, maxRows: 3}" v-model="item.changes[son_item].before_change" :title="item.changes[son_item].before_change"></el-input>
                                                    </td>
                                                    <td>
                                                        <el-input type="textarea" resize="none" :rows="3" :autosize="{ minRows: 3, maxRows: 3}" v-model="item.changes[son_item].change" :title="item.changes[son_item].change"></el-input>
                                                    </td>
                                                    <td>
                                                        <el-input type="textarea" resize="none" :rows="3" :autosize="{ minRows: 3, maxRows: 3}" v-model="item.changes[son_item].before_influence" :title="item.changes[son_item].before_influence"></el-input>
                                                    </td>
                                                    <td>
                                                        <el-input type="textarea" resize="none" :rows="3" :autosize="{ minRows: 3, maxRows: 3}" v-model="item.changes[son_item].influence" :title="item.changes[son_item].influence"></el-input>
                                                    </td>
                                                    <td>
                                                        <div style="display: inline-block;width: 102px;">
                                                            <span class="append-span" @click="add_opt(index, son_item)"> &nbsp;[ 新增 ]</span>
                                                            <span class="append-span" @click="del_opt(index, son_item)"> &nbsp;[ 删除 ]</span>
                                                        </div>
                                                    </td>
                                                </tr>
                                            </template>
                                        </tbody>

                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="prev()">
                        <i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button size="mini" type="primary" @click="save()">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="next()">下一步
                        <i class="el-icon-arrow-right"></i>
                    </el-button>
                </div>
            </div>
            <div class="right">

            </div>

        </div>

    </div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    data() {
        return {
            tableData3: [
                {
                    tag_id: '2016-05-03',
                    tag: '小分类1',
                    parent_tag: '大分类1',
                    changes: [
                        {
                            gid: 1,
                            before_change: '修改前',
                            change: '修改后',
                            before_influence: '影响前',
                            influence: '影响后'
                        },
                        {
                            gid: 2,
                            before_change: '修改前2',
                            change: '修改后2',
                            before_influence: '影响前2',
                            influence: '影响后2'
                        }
                    ]
                },
                {
                    tag_id: '2016-05-03',
                    tag: '小分类1',
                    parent_tag: '大分类1',
                    changes: [
                        {
                            gid: 1,
                            before_change: '修改前',
                            change: '修改后',
                            before_influence: '影响前',
                            influence: '影响后'
                        },
                        {
                            gid: 2,
                            before_change: '修改前2',
                            change: '修改后2',
                            before_influence: '影响前2',
                            influence: '影响后2'
                        }
                    ]
                }
            ],
            active: Number(window.sessionStorage.getItem('Step')),
            scene: [],
            step2: {
                doc_id: 0,
                micro_ver: Number(window.sessionStorage.getItem('ver')),
                commit_user: window.sessionStorage.getItem('Uall'),
                type: 'CHANGE',
                content: []
            },
            defaultProps: {
                label: 'scene',
                value: 'scene_id',
                children: 'scenes'
            },
            choosesence: [],
            sceneslist: [],
            get_data: '',
            save_data: '',
            dbrfmFlag: false,
            zero: 0
        }
    },
    mounted() {
        // this.GetSceneData()
        this.showScene()
        var self = this
        setTimeout(() => {
            $('.jump').on('click', function(e) {
                self.jump_to($(this).text())
            })
        }, 10)
        if (this.$route.query.params) {
            this.dbrfmFlag = this.$route.query.params
        }
    },
    methods: {
        del_opt(index, son_index) {
            this.step2.content[index].changes.splice(son_index, 1)
        },
        add_opt(index, son_index) {
            let row = {
                gid: 0,
                before_change: '',
                changes: '',
                address: '',
                zip: ''
            }
            this.step2.content[index].changes.splice(son_index + 1, 0, row)
        },
        GetSceneData() {
            this.$axios
                .get(this.Ip + '/Scene')
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.sceneslist = res.data.content
                        //   console.log(this.sceneslist,'---------')
                        // if(this.sceneslist.length != 0 ){
                        //   for(let i = 0; i <this.sceneslist.length ; i++ ){
                        //     for(let k = 0; k <this.sceneslist[i].scenes.length;k++){
                        //       let msg_data = this.sceneslist[i].scenes[k].scene+"(" + this.sceneslist[i].scenes[k].explain + ")"
                        //       this.sceneslist[i].scenes[k].scene = msg_data
                        //     }
                        //   }
                        // }
                    }
                })
                .catch(res => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error'
                    })
                })
        },
        showScene() {
            if (window.sessionStorage.getItem('DocId') != null) {
                let doc_id = window.sessionStorage.getItem('DocId')
                this.$axios.get(this.Ip + '/Scene/' + doc_id + '/' + 'change').then(res => {
                    if (res.data.result == 'OK') {
                        this.step2.micro_ver = res.data.micro_ver
                        this.step2.content = res.data.content
                    } else {
                        this.step2.micro_ver = res.data.micro_ver
                    }
                    this.get_data = JSON.stringify(this.step2)
                })
            }
        },
        handleSelect(val) {
            // console.log(val,"c")
            for (var father of this.sceneslist) {
                if (val[0] == father.scene_id) {
                    for (var children of father.content) {
                        if (val[1] == children.scene_id) {
                            var flag = false
                            for (var doub of this.step2.content) {
                                if (doub.scene_id == val[1]) {
                                    flag = true
                                }
                            }
                            if (flag == false) {
                                this.step2.content.push(children)
                            } else {
                                this.$alert('您已选择过该场景', '提示')
                            }
                        }
                    }
                }
            }
        },
        delete_input(data, index) {
            this.step2.content.splice(index, 1)
        },
        prev() {
            // this.$router.push('/tagl/step2')
            this.$router.push({ path: '/tagl/step1', query: { params: this.dbrfmFlag } })
        },
        next() {
            this.step2.doc_id = window.sessionStorage.getItem('DocId')
            if (window.sessionStorage.getItem('DocId') == null) {
                this.step2.doc_id = 0
            } else {
                this.step2.doc_id = window.sessionStorage.getItem('DocId')
            }
            this.$axios
                .post(this.Ip + '/Scene', this.step2)
                .then(res => {
                    // console.log(res)
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('DocId', res.data.doc_id)
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                        if (window.sessionStorage.getItem('Step') > '3') {
                            window.sessionStorage.setItem('Step', 4)
                        } else if (window.sessionStorage.getItem('Step') == '1') {
                            window.sessionStorage.setItem('Step', 2)
                        }
                        this.$router.push({ path: '/tagl/step3', query: { params: this.dbrfmFlag } })
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败!' + res.data.error,
                            type: 'error',
                            duration: 0
                        })
                    }
                })
                .catch(res => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0
                    })
                })
        },
        JumpAndSave() {
            this.step2.doc_id = window.sessionStorage.getItem('DocId')
            if (window.sessionStorage.getItem('DocId') == null) {
                this.step2.doc_id = 0
            } else {
                this.step2.doc_id = window.sessionStorage.getItem('DocId')
            }
            this.$axios
                .post(this.Ip + '/Scene', this.step2)
                .then(res => {
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('DocId', res.data.doc_id)
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                    }
                })
                .catch(res => {})
        },
        save() {
            this.step2.doc_id = window.sessionStorage.getItem('DocId')
            if (window.sessionStorage.getItem('DocId') == null) {
                this.step2.doc_id = 0
            } else {
                this.step2.doc_id = window.sessionStorage.getItem('DocId')
            }
            console.log(this.step2, 'step2')
            this.$axios
                .post(this.Ip + '/Scene', this.step2)
                .then(res => {
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('DocId', res.data.doc_id)
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                        this.showScene()
                        this.$message({
                            type: 'success',
                            message: '保存成功!'
                        })
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败!' + res.data.error,
                            type: 'error',
                            duration: 0
                        })
                    }
                })
                .catch(res => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0
                    })
                })
        },
        cancel() {
            this.save_data = JSON.stringify(this.step2)
            if (this.save_data == this.get_data) {
                this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                    })
                    .catch(() => {})
            }
        },
        jump_to(index) {
            switch (index) {
                case '场景(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step1', query: { params: this.dbrfmFlag } })
                    break
                // case '修改点影响点(必填)':
                //     this.JumpAndSave()
                //     this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
                //     break
                case '考虑点(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step3', query: { params: this.dbrfmFlag } })
                    break
                case 'DRBFM(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step4', query: { params: this.dbrfmFlag } })
                    break
            }
        },
    }
}
</script>

<style scoped>
.gray_col {
    background-color: #FAFAFA;
}
table {
    width: 100%;
    border-collapse: collapse;
    text-align: center;
    font-size: 14px;
}
table th,
tr,
td {
    border: 1px solid #ebeef5;
}
thead {
    color: #909399;
    background-color: #edf9f5;
}
tbody {
    color: #606266;
}
th {
    padding: 3px 0;
}
.append-span {
    float: left;
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
}
#Scene {
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
.cbody {
    float: left;
    height: 100%;
    width: 84%;
    padding-left: 1%;
    border-left: 1px solid #c0c4cc;
    /*overflow-y: scroll;*/
    /*border: 1px solid red;*/
}

.checkBox {
    margin: 20px 0 0 20px;
}
.scene-title {
    margin: 40px 0 20px 0;
}
.mid {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
    padding-right: 20px;
    padding-bottom: 55px;
    border-right: 1px solid #ccc;
    /*overflow-y: scroll;*/
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
.right {
    width: 20%;
    height: 100%;
    float: left;
}
.big-box {
    margin: 20px 0 0 0;
}

.casc {
    width: 350px;
}
.checked-input-list-title {
    margin-bottom: 15px;
    font-size: 18px;
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
    .cbody {
        float: left;
        width: 80%;
        height: 100%;
        overflow-y: scroll;
    }
}
@media screen and (max-width: 1024px) {
    #Scene {
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
}
</style>

