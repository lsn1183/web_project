<template>
    <div style="overflow-x: auto;">
        <div class="drbfm-table-div">
            <h3 style="font-weight:normal;padding:10px 0;font-size:15px">
                {{tableData[0].name}}
            </h3>
            <table id="table1">
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
                                                    <p class="td-ex word-weight" :title="item.scene" v-html="item.scene"></p>
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
                    <tr v-for="(item, i) in tableData" :key="i">
                        <td :colspan="item.sub.length">
                            <table class="table2">
                                <tr v-for="(items, j) in item.sub"  :key="j">
                                    <td class="td-width-ex" :title="items.name" v-html="items.name"></td>
                                    <td>
                                        <table class="table3" style="table-layout:fixed;">
                                            <tr v-for="(itemss, itemssIndex) in items.sub" :key="itemssIndex">
                                                <td class="td-width" style="width:200px;border-bottom: solid 1px #ebeef5;" >
                                                    <p class="td-p-style" :title="itemss.name" v-html="itemss.name"></p>
                                                </td>
                                                <td class="td-width" v-for="(scenesItem, scenesItemIndex) in itemss.scenes" style="border-bottom: solid 1px #ebeef5;" :key="scenesItemIndex">
                                                    <p class="td-ex" :title="scenesItem.content" v-html="scenesItem.content"></p>
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
    name: 'diffDrbfm',
    props: ['drbfmData'],
    data() {
        return {
            hiddenTable: true,
            theadData: [],
            tableData: [],
            writeDrbfmFlag: false
        }
    },
    created () {
        this.transfer_req_data_to_display_data(this.drbfmData);
    },
    methods: {
        transfer_req_data_to_display_data(val) {
            this.tableData = val
            this.theadData.colLength = val[0].sub.length
            this.theadData.sceneArray = val[0].sub[0].sub[0].scenes
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
    overflow-x: scroll;
    margin-bottom: 40px;
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

