<template>
    <div>
        <div class="drbfm-table-div">
            <p class="message" v-if="hiddenTable == 'NO_SCENE'?true:false">暂无数据</p>
            <p class="message" v-if="hiddenTable == 'NO_CONTENT'?true:false">暂无填写内容</p>
            <h3 style="font-weight:normal;padding:10px 0;font-size:15px" v-if="hiddenTable == 'normal'?true:false">
                {{tableData[0].name}}
                <span class="append_span" style="fontWeight:500" @click="show_diff_drbfm_data()" v-if="showDiffDrbfmFlag == true"> &nbsp;[ 显示全部内容 ]</span>
                <span class="append_span" style="fontWeight:500" @click="show_diff_drbfm_data()" v-if="showDiffDrbfmFlag == false"> &nbsp;[ 只显示已填内容 ]</span>
            </h3>
            <table id="table1" v-if="hiddenTable == 'normal'?true:false">
                <thead>
                    <tr>
                        <td :colspan="theadData.colLength">
                            <table class="table2">
                                <tr>
                                    <td class="td-width-ex word-weight">项目</td>
                                    <td>
                                        <table class="table3" style="table-layout:fixed;">
                                            <tr>
                                                <td class="td-width" style="width:200px;">
                                                    <p class="td-p-style word-weight">担心点</p>
                                                </td>
                                                <td class="td-width" v-for="(item, index) in theadData.sceneArray" :key="index">
                                                    <p class="td-ex word-weight" :title="item.scene">{{item.scene}}</p>
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
                                            <tr v-for="(itemss, itemssIndex) in items.sub" :key="itemssIndex">
                                                <td class="td-width" style="width:200px;border-bottom: solid 1px #ebeef5;" >
                                                    <p class="td-p-style" :title="itemss.name">{{itemss.name}}</p>
                                                </td>
                                                <td class="td-width" v-for="(scenesItem, scenesItemIndex) in itemss.scenes" style="border-bottom: solid 1px #ebeef5;" :key="scenesItemIndex">
                                                    <p class="td-ex" :title="scenesItem.content" >{{scenesItem.content}}</p>
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
    name: 'drbfmTable',
    props: {
        // tableData: {
        //     type: Array
        // },
        UseCaseID: {
            type: Number
        }
    },
    data() {
        return {
            hiddenTable: false,
            theadData: [],
            tableData: [],
            showDiffDrbfmFlag: true,
            writeDrbfmFlag: false
        }
    },
    mounted() {
        this.request_diff_data()
    },
    watch: {
        UseCaseID(val) {
            this.request_diff_data()
        },
        showDiffDrbfmFlag() {
            this.request_diff_data()
        }
    },
    methods: {
        request_diff_data() {
            if (this.showDiffDrbfmFlag) {
                //默认显示填过的
                this.$axios
                    .get(this.Ip + '/Section/' + this.UseCaseID + '/DRBFM/YES')
                    .then(res => {
                        if (res.data.result == 'OK') {
                            if (res.data.status == 'normal') {
                                this.hiddenTable = 'normal'
                                this.transfer_req_data_to_display_data(res.data.content)
                            } else if (res.data.status == 'NO_SCENE') {
                                //没场景
                                this.hiddenTable = 'NO_SCENE'
                            } else if (res.data.status == 'NO_CONTENT') {
                                //有场景没数据
                                this.hiddenTable = 'NO_CONTENT'
                            } else {
                                //do nothing 
                            }
                        }
                    })
                    .catch(err => {})
            } else {
                //显示全部
                this.$axios
                    .get(this.Ip + '/Section/' + this.UseCaseID + '/DRBFM')
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.transfer_req_data_to_display_data(res.data.content)
                        }
                    })
                    .catch(err => {})
            }
        },
        transfer_req_data_to_display_data(val) {
            this.tableData = val
            this.theadData.colLength = val[0].sub.length
            this.theadData.sceneArray = val[0].sub[0].sub[0].scenes
        },
        show_diff_drbfm_data() {
            this.showDiffDrbfmFlag = !this.showDiffDrbfmFlag
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
    width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    line-height: 26px;
}
.drbfm-table-div {
    padding-left: 20px;
}

.word-weight {
    font-weight:bold;
}

@media screen and (max-width: 1024px) {
    .td-ex {
        width: 150px;
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
.append_span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
}
</style>

