<template>
    <div id="Scene">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="场景(必填)" icon="el-icon-edit" status="process">1</el-step>
                    <el-step class="jump" title="修改点影响点(必填)">2</el-step>
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
                            <i class="el-icon-question" style="fontSize:15px; lineHeight:25px;float:left;marginLeft:5px" title="请选择Usecase使用的场景，比如Usecase A关联了timer的使用，则Usecase A场景选择时必须包含timer；不同场景的选择会关联不同的设计确认点，请认真选择"></i>
                        </h2>
                    </div>

                    <div style="height: auto;">
                        <div class="checkBox">
                            <div class="checked-input-list-title">
                                选择具体的场景
                                <!-- <span class="Asa-size">[ 方式一 ]</span>
                <span class="Asa-size">[ 方式二 ]</span> -->
                            </div>
                            <el-checkbox-group v-model="arr_id" @change='changecheckfun'>

                                <!-- <div class="check-content-box" v-for='check_item in sceneslist'>
                  <div class="checked-title" :title='check_item.scene_type_org'>{{check_item.scene}}</div> 
                  <div class="check-msg">
                    <span v-for='item in check_item.scenes' class="check-span" :title='item.explain'>
                      <el-checkbox :label="item.scene_id">
                        {{item.scene}}
                      </el-checkbox>
                    </span>
                  </div> -->

                                <el-table :data="sceneslist" border style="width: 98%" :header-cell-style="{background:'#edf9f5'}">
                                    <el-table-column fixed prop="scene" label="主项目" header-align='center' width="150">
                                        <template slot-scope="scope">
                                            <span style="white-space: nowrap;text-overflow: ellipsis;cursor: pointer;">{{scope.row.tag}}</span>
                                        </template>
                                    </el-table-column>
                                    <el-table-column fixed prop="sub" label="场景" header-align='center'>
                                        <template slot-scope="scope">
                                            <span v-for='item in scope.row.sub' class="check-span">
                                                <el-checkbox :label="item.tag_id">
                                                    {{item.tag}}
                                                </el-checkbox>
                                            </span>
                                        </template>
                                    </el-table-column>
                                </el-table>

                                <!-- </div>  -->
                            </el-checkbox-group>

                        </div>
                    </div>
                </div>

                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="info" @click="prev()" disabled>
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
            active: Number(window.sessionStorage.getItem('Step')),
            // scene:[],
            step2: {
                doc_id: 0,
                micro_ver: Number(window.sessionStorage.getItem('ver')),
                commit_user: window.sessionStorage.getItem('Uall'),
                content: [],
                type: 'SCENE'
            },
            defaultProps: {
                label: 'scene',
                value: 'scene_id',
                children: 'scenes'
            },
            choosesence: [],
            sceneslist: [],
            list1: [
                {
                    scene: 'mutex',
                    scene_id: 8
                },
                {
                    scene: 'local \u53c2\u6570',
                    scene_id: 9
                },
                {
                    scene: 'global \u53c2\u6570',
                    scene_id: 10
                },
                {
                    scene: '\u903b\u8f91\u3001\u7b97\u6cd5',
                    scene_id: 11
                },
                {
                    scene: '\u5272\u5165',
                    scene_id: 12
                },
                {
                    scene: 'log',
                    scene_id: 13
                },
                {
                    scene: '\u8f6f\u4ef6\u67b6\u6784',
                    scene_id: 14
                }
            ],
            list2: [
                {
                    scene: '\u542f\u52a8\u3001\u7ec8\u4e86',
                    scene_id: 15
                },
                {
                    scene: '\u5916\u8bbe',
                    scene_id: 16
                },
                {
                    scene: '\u901a\u4fe1\u65b9\u5f0f',
                    scene_id: 17
                }
            ],
            list3: [
                {
                    scene: 'flash/emmc',
                    scene_id: 18
                },
                {
                    scene: 'hardware\u53d8\u66f4',
                    scene_id: 19
                }
            ],
            list4: [
                {
                    scene: '\u5347\u7ea7',
                    scene_id: 20
                },
                {
                    scene: '\u73af\u5883\u6784\u7b51',
                    scene_id: 21
                },
                {
                    scene: '\u5de5\u5177',
                    scene_id: 22
                },
                {
                    scene: '\u8d2d\u5165\u8f6f\u4ef6',
                    scene_id: 23
                }
            ],
            get_data: '',
            save_data: '',
            dbrfmFlag: false,
            arr_id: [],
            scenes_post: []
        }
    },
    mounted() {
        this.GetSceneData()
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
        GetSceneData() {
            this.$axios
                .get(this.Ip + '/Scene')
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.sceneslist = []
                        this.sceneslist = res.data.content
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
                let doc_id = window.sessionStorage.getItem('DocId'),
                    sec_type = 'SCENES'
                this.$axios.get(this.Ip + '/Scene/' + doc_id).then(res => {
                    if (res.data.result == 'OK') {
                        this.step2.micro_ver = res.data.micro_ver
                        this.step2.content = res.data.content
                        this.arr_id = []
                        for (let i = 0; i < res.data.content.length; i++) {
                            this.arr_id.push(res.data.content[i].tag_id)
                        }
                    } else {
                        this.step2.micro_ver = res.data.micro_ver
                    }
                    this.get_data = JSON.stringify(this.step2)
                })
            }
        },
        handleSelect(val) {
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
            this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
        },
        next() {
            this.step2.content = this.arr_id
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
                        if (window.sessionStorage.getItem('Step') > '3') {
                            window.sessionStorage.setItem('Step', 4)
                        } else if (window.sessionStorage.getItem('Step') == '0') {
                            window.sessionStorage.setItem('Step', 1)
                        }
                        this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
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
            this.step2.content = this.arr_id
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
                        this.showScene()
                    }
                })
                .catch(res => {})
        },
        changecheckfun(value) {},
        save() {
            this.step2.content = this.arr_id
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
                // case '场景(必填)':
                //     this.JumpAndSave()
                //     this.$router.push({ path: '/tagl/step1', query: { params: this.dbrfmFlag } })
                //     break
                case '修改点影响点(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
                    break
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
    margin: 20px 0 0 10px;
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
    margin: 150px 0 0 0;
}

.casc {
    width: 350px;
}
.checked-input-list-title {
    margin-bottom: 15px;
    font-size: 18px;
}
.check-content-box {
    overflow: hidden;
    border: 1px solid #ccc;
    margin: 3px 0;
}
.checked-title {
    font-size: 14px !important;
    float: left;
    min-width: 20%;
    height: 100%;
    text-align: center;
    margin-top: 5px;
    color: #606266;
    cursor: pointer;
}
.check-msg {
    float: left;
    width: 65%;
    border-left: 1px solid #ccc;
    padding-left: 10px;
    /* width: 98%;
  margin:0 20px;
  border: 1px dashed #c0c4cc;
  overflow: hidden;
  display: flex;
  justify-content:flex-start*/
}
.check-span {
    display: block;
    margin: 5px 0;
    min-width: 20%;
    width: 30%;
    float: left;
}
.Asa-size {
    margin-left: 10px;
    font-size: 12px;
    cursor: pointer;
}
@media screen and (max-width: 1452px) {
    .check-span {
        width: 48%;
    }
}
@media screen and (max-width: 1200px) {
    .check-span {
        width: 50%;
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

