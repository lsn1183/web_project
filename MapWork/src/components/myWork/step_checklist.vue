<template>
    <div id="CheckList" ref="CheckList">
        <div class="checklist-content">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="场景(必填)">1</el-step>
                    <el-step class="jump" title="变更变化点(必填)">2</el-step>
                    <el-step class="jump" title="考虑点(必填)">3</el-step>
                    <el-step class="jump" title="DRBFM(必填)" icon="el-icon-edit" status="process">4</el-step>
                </el-steps>
            </div>
        </div>
        <div class="content-box">
            <div class="mid">
                <div class="mid-top">
                    <div class="sequence-title">
                        <h2 style="font-size:22px;background-color: #6bcca0; color: white;line-height:25px;padding-left: 10px;">DRBFM
                            <i class="el-icon-question" title='提示：请填写与DRBFM相关的信息（系统后期会导出相关的DRBFM素材）' style="font-size:15px;height:20px;vertical-align:middle"></i>
                        </h2>
                    </div>
                    <div v-bind:style="{height:widthDD + 'px'}">
                        <drbfm-table></drbfm-table>
                    </div>
                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="prev()">
                        <i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button size="mini" type="info" disabled>&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="success()">&nbsp;&nbsp;完&nbsp;&nbsp;&nbsp;成&nbsp;&nbsp;</el-button>
                </div>
            </div>

            <div class="right">
                <!-- <showLeftCheck></showLeftCheck> -->
            </div>
        </div>
    </div>

</template>

<script>
// import showLeftCheck from './step_showLeftCheck'
import drbfmTable from './DRBFM'
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    components: {
        // showLeftCheck: showLeftCheck,
        drbfmTable: drbfmTable
    },
    data() {
        return {
            widthDD: window.innerHeight - 216,
            active: Number(window.sessionStorage.getItem('Step')),
            listcheck: [],
            leafe_flag: false,
            ck_ls: [],
            showck: [],
            tableData: [],
            theadData: {},
            elementTableData: [],
            colConfigs: [],
            hiddenTable: true,
            monitorFlag: true,
            cancelFlag: true,
            drbfm_diff_data: {},
            dbrfmFlag: false
        }
    },
    mounted() {
        this.widthDD = window.innerHeight - 216
        const that = this
        window.onresize = () => {
            return (() => {
                that.widthDD = window.innerHeight - 216
            })()
        }
        $(document).ready(function() {
            $('table').on('click', '.td-ex', function(event) {
                $('.td-ex').css('background-color', 'white')
                $(this).css('background-color', '#ecf5ff')
            })
        })
        var self = this
        $('.jump').on('click', function(e) {
            self.jump_to($(this).text())
        })
    },
    created() {
        // this.reqTableData()
    },
    // mounted() {
    //     var self = this
    //     $('.jump').on('click', function(e) {
    //         self.jump_to($(this).text())
    //     })
    //     if (this.$route.query.params) {
    //         this.dbrfmFlag = this.$route.query.params
    //     }
    // },
    methods: {
        prev() {
            this.$router.push({ path: '/tagl/step3', query: { params: this.dbrfmFlag } })
        },
        cancel() {
            this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
        },
        JumpAndSave(val, val_id) {
            let objData = {
                sec_type: 'DRBFM',
                content: []
            }
            let tableDataCopy = this.tableData[0]
            let subTableData = []
            for (let i = 0; i < tableDataCopy.sub.length; i++) {
                for (let j = 0; j < tableDataCopy.sub[i].sub.length; j++) {
                    for (let k = 0; k < tableDataCopy.sub[i].sub[j].scenes.length; k++) {
                        let objContent = JSON.parse(JSON.stringify(tableDataCopy.sub[i].sub[j].scenes[k]))
                        objContent.item_id = tableDataCopy.sub[i].sub[j].item_id
                        let valContent = tableDataCopy.sub[i].sub[j].scenes[k].content
                        objContent.drbfm_content = valContent
                        objContent.sec_id = window.sessionStorage.getItem('stepTwoSecId')
                        delete objContent.content
                        delete objContent.scene
                        objData.content.push(objContent)
                    }
                }
            }
            this.$axios
                .post(this.Ip + '/Section', objData)
                .then(res => {
                    if (res.data.result == 'OK') {
                    }
                })
                .catch(err => {})
        },
        jump_to(index) {
            switch (index) {
                case '场景(必填)':
                    // this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step1', query: { params: this.dbrfmFlag } })
                    break
                case '变更变化点(必填)':
                    // this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
                    break
                case '考虑点(必填)':
                    // this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step3', query: { params: this.dbrfmFlag } })
                    break
                // case 'DRBFM(必填)':
                //     this.JumpAndSave()
                //     this.$router.push({ path: '/tagl/step4', query: { params: this.dbrfmFlag } })
                //     break
            }
        },
        success() {
            this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
        }
    }
}
</script>

<style scoped>
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
}
tbody {
    color: #606266;
}
th {
    padding: 3px 0;
}
.append-span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
}
#CheckList {
    margin: 0 auto;
    width: 100%;
    height: 100%;
}
.checklist-content {
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
.content-box {
    float: left;
    width: 84%;
    padding-left: 1%;
    border-left: 1px solid #c0c4cc;
    height: 100%;
    /*overflow-y: scroll;*/
}
.sequence-title {
    margin: 40px 0 20px 0;
}
.mid {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
    padding-right: 20px;
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
.footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}
.right {
    width: 20%;
    height: 100%;
    float: left;
    overflow-y: scroll;
    overflow-x: hidden;
}

@media screen and (max-width: 1334px) {
    .checklist-content {
        max-width: 300px;
        min-width: 200px;
        width: 15%;
        height: 100%;
        padding: 20px;
        float: left;
    }
    .content-box {
        float: left;
        width: 80%;
        height: 100%;
        /*overflow-y: scroll;*/
        /*border: 1px solid red;*/
    }
}
@media screen and (max-width: 1024px) {
    .header-top {
        display: none;
    }
    .header {
        height: 100%;
        padding: 10%;
        clear: both;
    }
    .content-box {
        float: left;
        width: 820px;
        height: 100%;
        /*overflow-y: scroll;*/
        /*border: 1px solid red;*/
    }
}
table {
    /* width: 100%; */
    border-collapse: collapse;
    text-align: center;
}
table th,
td {
    border: 1px solid #999;
    font-size: 14px;
}
.table2 tr td:nth-child(1) {
    border-left: 0;
}
.table2 tr td:nth-last-child(1) {
    border-right: 0;
}
.table2 tr:nth-child(1) td {
    border-top: 0;
}
.table2 tr:nth-last-child(1) td {
    border-bottom: 0;
}
.td-width {
    width: 100px;
}
.td-width-ex {
    width: 100px;
    min-width: 100px;
}
.td-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.td-p-style {
    /* display: inline-block; */
    width: 200px;
    /* height: 26px; */
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.td-ex {
    height: 26px;
    width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    cursor: pointer;
    line-height: 26px;
}
.message {
    text-align: center;
    padding: 20px;
    font-size: 14px;
    color: #5e6d82;
    border: 1px solid #ebeef5;
    margin-top: 10px;
    margin: 10px 0 0 -20px;
}
</style>

