<template>
    <div  v-loading="loading" element-loading-text="Loading" element-loading-spinner="el-icon-loading" class="edit-drbfm-table">
        <div class="drbfm-table-div">
            <p class="message" v-if="hiddenTable == 'NO_SCENE'?true:false">请选择场景</p>
            <span class="append-span" style="fontWeight:500" @click="show_diff_drbfm_data(1)" v-if="hiddenTable == 'NO_CONTENT'?true:false"> &nbsp;[ 显示全部内容 ]</span>
            <p class="message" v-if="hiddenTable == 'NO_CONTENT'?true:false">暂无填写内容</p>
            <h3 style="font-weight:normal;padding-bottom:10px;font-size:15px" v-if="hiddenTable == 'normal'?true:false">
                {{tableData[0].name}}
                <span class="append-span" style="fontWeight:500" @click="show_diff_drbfm_data(1)" v-if="showDiffDrbfmFlag == true"> &nbsp;[ 显示全部内容 ]</span>
                <span class="append-span" style="fontWeight:500" @click="show_diff_drbfm_data(2)" v-if="showDiffDrbfmFlag == false"> &nbsp;[ 只显示已填内容 ]</span>
            </h3>
            <table id="table1" v-if="hiddenTable == 'normal'?true:false">
                <thead>
                    <tr>
                        <td :colspan="theadData.colLength">
                            <table class="table2">
                                <tr>
                                    <td class="td-width-ex" style="font-weight:bold;">项目</td>
                                    <td>
                                        <table class="table3" style="table-layout:fixed;">
                                            <tr>
                                                <td class="td-width" style="width:150px;">
                                                    <p class="td-p-style" style="font-weight:bold;">担心点</p>
                                                </td>
                                                <td class="td-width" v-for="(item, index) in theadData.sceneArray" :key="index">
                                                    <p class="td-ex" :title="item.scene +'\n' + item.explain" style="font-weight:bold;">{{item.scene}}</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </thead>
                
                <tbody>
                    <tr v-for="(item,i) in tableData" :key="i">
                        <td :colspan="item.sub.length">
                            <table class="table2">
                                <tr v-for="(items, j) in item.sub"  :key="j">
                                    <td class="td-width-ex" :title="items.name">{{items.name}}</td>
                                    <td>
                                        <table class="table3" style="table-layout:fixed;">
                                            <tr v-for="(itemss, itemssIndex) in items.sub"  :key="itemssIndex">
                                                <td class="td-width" style="width:150px;border-bottom: solid 1px #ebeef5;" >
                                                    <p class="td-p-style" :title="itemss.name">{{itemss.name}}</p>
                                                </td>
                                                <td class="td-width" :class="{ showBg: scenesItem.showFlag}" v-for="(scenesItem, scenesItemIndex) in itemss.scenes" style="border-bottom: solid 1px #ebeef5;" @click="click_table_cell_action($event)" :key="scenesItemIndex">
                                                    <el-popover
                                                        placement="top"
                                                        width="400"
                                                        trigger="click"
                                                        v-model="scenesItem.showFlag">
                                                        <el-input 
                                                        v-model="scenesItem.content"
                                                        type="textarea" 
                                                        :autosize="{ minRows: 5, maxRows: 5}" 
                                                        resize='none'
                                                        @keyup.esc.native="scenesItem.showFlag = false"></el-input>
                                                        <p slot="reference" class="td-ex" :title="scenesItem.content">{{scenesItem.content}}</p>
                                                    </el-popover>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </tbody>        
            </table>
        </div>
    </div>
</template>
<script>
export default {
    name: 'editDrbfmTable',
    props: {
        monitorNum: {
            type: Boolean
        },
        monitorLen: {
            type: Boolean
        },
        monitorCancel: {
            type: Boolean
        }
    },
    data() {
        return {
            loading: true,
            hiddenTable: 'NO_SCENE',
            theadData: [],
            tableData: [],
            showDiffDrbfmFlag: false,
            writeDrbfmFlag: false,
            UseCaseID: window.sessionStorage.getItem('stepTwoSecId'),
            micro_ver: 0,
            visible2: false,
            diffData: {
                oldData: [],
                newData: []
            }
        }
    },
    mounted() {
        this.modify_data()
    },
    watch: {
        hiddenTable () {
            this.loading = false
        },
        UseCaseID(val) {
            this.modify_data()
        },
        monitorNum (val) {
            this.add_scene()
        },
        monitorLen (val) {
            this.confirm_button()
        },
        monitorCancel(val) {
            this.diffData.newData = this.tableData
            this.$emit('sendDiffData', this.diffData)
        }
    },
    updated() {
        // this.$nextTick(() => {
        //     this.loading = false
        //     console.log(this.loading, 'updated')
        // })
    },
    methods: {
        click_table_cell_action(event) {
            this.$nextTick(function() {
                if ($('textarea').is(':visible')) {
                    $('textarea').focus()
                }
            })
        },
        modify_data() {
            if (this.showDiffDrbfmFlag) {
                //默认显示填过的
                this.$axios
                    .get(this.Ip + '/Section/' + this.UseCaseID + '/DRBFM/YES')
                    .then(res => {
                        if (res.data.result == 'OK') {
                            if (res.data.status == 'normal') {
                                this.hiddenTable = 'normal'
                                this.loading = false
                                this.diffData.oldData = JSON.parse(JSON.stringify(res.data.content))
                                this.transfer_req_data_to_display_data(res.data.content)
                            } else if (res.data.status == 'NO_SCENE') {
                                //没场景
                                this.hiddenTable = 'NO_SCENE'
                                this.loading = false
                            } else if (res.data.status == 'NO_CONTENT') {
                                //有场景没数据
                                this.hiddenTable = 'NO_CONTENT'
                                this.loading = false
                            } else {
                                //do nothing
                                this.loading = false
                            }
                            this.micro_ver = res.data.micro_ver
                        }
                    })
                    .catch(err => {
                        this.$message({
                            showClose: true,
                            message: '服务异常',
                            type: 'error'
                        })
                    })
            } else {
                //显示全部
                this.$axios
                    .get(this.Ip + '/Section/' + this.UseCaseID + '/DRBFM')
                    .then(res => {
                        if (res.data.result == 'OK') {
                            if (res.data.status == 'NO_SCENE') {
                                this.hiddenTable = 'NO_SCENE'
                                this.loading = false
                            } else {
                                this.hiddenTable = 'normal'
                                this.diffData.oldData = JSON.parse(JSON.stringify(res.data.content))
                                this.transfer_req_data_to_display_data(res.data.content)
                                this.loading = false
                            }
                            this.micro_ver = res.data.micro_ver  
                        }
                    })
                    .catch(err => {
                        this.$message({
                            showClose: true,
                            message: '服务异常',
                            type: 'error'
                        })
                    })
            }
        },
        transfer_req_data_to_display_data(val) {
            this.tableData = val
            this.theadData.colLength = val[0].sub.length
            this.theadData.sceneArray = val[0].sub[0].sub[0].scenes
        },
        show_diff_drbfm_data() {
            this.loading = true
            this.switch_drbfm_table()
            this.showDiffDrbfmFlag = !this.showDiffDrbfmFlag
            // this.modify_data()
        },
        switch_drbfm_table() {
            this.$nextTick(() => {
                let objData = {
                    sec_type: 'DRBFM',
                    doc_id: Number(window.sessionStorage.getItem('DocId')),
                    commit_user: window.sessionStorage.getItem('Uall'),
                    micro_ver: this.micro_ver,
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
                            objContent.sec_id = Number(window.sessionStorage.getItem('stepTwoSecId'))
                            delete objContent.content
                            delete objContent.scene
                            objData.content.push(objContent)
                        }
                    }
                }
                this.$axios
                    .post(this.Ip + '/Section', objData)
                    .then(res => {
                        this.modify_data()
                    })
                    .catch(err => {})
            })
        },
        add_scene() {
            if (this.hiddenTable == 'NO_SCENE' || this.hiddenTable == 'NO_CONTENT') {
                return
            }
            this.$nextTick(() => {
                let objData = {
                    sec_type: 'DRBFM',
                    doc_id: Number(window.sessionStorage.getItem('DocId')),
                    commit_user: window.sessionStorage.getItem('Uall'),
                    micro_ver: this.micro_ver,
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
                            delete objContent.showFlag
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
                            this.modify_data()
                            this.$message({
                                showClose: false,
                                message: '保存成功',
                                type: 'success'
                            })
                        } else {
                            this.$message({
                                showClose: true,
                                message: res.data.error,
                                type: 'error'
                            })
                        }
                    })
                    .catch(err => {
                        this.$message({
                            showClose: true,
                            message: err.data.error,
                            type: 'error'
                        })
                    })
            })
        },
        confirm_button() {
            if (this.hiddenTable == 'NO_SCENE'|| this.hiddenTable == 'NO_CONTENT') {
                window.sessionStorage.removeItem('stepTwoSecId')
                window.sessionStorage.removeItem('Step')
                this.$router.push('/tagl/File_design/Preview/'+window.sessionStorage.getItem('DocId'))
                return
            }
            this.$nextTick(() => {
                let objData = {
                    sec_type: 'DRBFM',
                    doc_id: Number(window.sessionStorage.getItem('DocId')),
                    commit_user: window.sessionStorage.getItem('Uall'),
                    micro_ver: this.micro_ver,
                    content: []
                }
                let tableDataCopy = this.tableData[0]
                let subTableData = []
                for (let i = 0 ;i < tableDataCopy.sub.length;i++) {
                    for(let j = 0;j < tableDataCopy.sub[i].sub.length; j++) {
                        for (let k=0;k< tableDataCopy.sub[i].sub[j].scenes.length;k++) {
                            let objContent = JSON.parse(JSON.stringify(tableDataCopy.sub[i].sub[j].scenes[k]))
                            objContent.item_id = tableDataCopy.sub[i].sub[j].item_id
                            let valContent = tableDataCopy.sub[i].sub[j].scenes[k].content
                            objContent.drbfm_content = valContent
                            objContent.sec_id = window.sessionStorage.getItem('stepTwoSecId')
                            delete objContent.showFlag
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
                            this.$message({
                                showClose: false,
                                message: '保存成功',
                                type: 'success'
                            })
                            window.sessionStorage.removeItem('stepTwoSecId')
                            window.sessionStorage.removeItem('Step')
                            this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                        } else {
                            this.$message({
                                showClose: true,
                                message: res.data.error,
                                type: 'error'
                            })
                        }
                    })
                    .catch(err => {
                        this.$message({
                            showClose: true,
                            message: err.data.error,
                            type: 'error'
                        })
                    })
            })
        }
    }
}
</script>
<style scoped>
table {
    border-collapse: collapse;
    text-align: center;
    background-color: white;
}
table th,
td {
    border: 1px solid #999;
    font-size: 14px;
    border-color: #ebeef5;
    font-family: '微软雅黑';
}
table thead {
    color: #909399;
}
table tbody {
    color: #606266;
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
    width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.td-ex {
    height: 26px;
    width: 150px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    line-height: 26px;
    padding:0 8px;
}
.drbfm-table-div {
    padding-left: 20px;
}
@media screen and (max-width: 1024px) {
    .td-ex {
        width: 150px;
        padding:0 8px;
    }
}
.show-dif-drbfm {
    color: rgb(66, 185, 131);
}
.message {
    /* margin-left: 20px; */
    text-align: center;
    padding: 20px;
    font-size: 14px;
    color: #5e6d82;
    border: 1px solid #ebeef5;
    margin-top: 10px;
}
.append-span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
}
.edit-drbfm-table {
    width: 100%;
    height:  100%;
    overflow: auto;
}
.showBg {
    background-color: #42b983;
    color: white;
}
</style>
