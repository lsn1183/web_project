<template>
    <div class="container" v-loading.fullscreen.lock="fullscreeLoading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(0, 0, 0, 0.8)">
        <div class="title">
            <el-breadcrumb separator-class="el-icon-arrow-right" style="padding-top: 10px;font-weight: normal;">
                <el-breadcrumb-item>{{title.projName}}</el-breadcrumb-item>
                <el-breadcrumb-item>{{title.quotationName}}</el-breadcrumb-item>
                <el-breadcrumb-item>{{title.version}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div id="example-container" class="hottable-wrapper">
            <HotTable :root="root" ref="textHot" :settings="hotSettings" v-if="showTable"></HotTable>
        </div>

        <!-- 覆盖层 -->
        <div class="shadow" @mousedown.stop>
            <i class="el-icon-d-arrow-right" @click='hideHistory()'></i>
            <div style="position: absolute; top: 0px; bottom: 0; left: 44px; right: 0px;overflow: hidden;" v-loading="taskRecordLoading">
                <HotTable :root="root" ref="detailTable" :settings="detailSettings" v-if="showDetailTable"></HotTable>
            </div>
        </div>
    </div>
</template>
<script>
import '../../../../node_modules/handsontable-pro/dist/handsontable.full.css'
import TaskRecord from '../views/taskRecord' //履历组件
import Handsontable from 'handsontable-pro'
import { HotTable } from '@handsontable-pro/vue'
import 'handsontable-pro/languages/zh-CN' //中文包
require('../../../assets/js/jquery-1.8.3.min.js')

import { reqSummaryAccount, reqTaskHistory, reqDetailQuote, reqDetail } from '../../../api/hansontable.js' //请求接口方法
import basicConfig from './basicConfig' //表格基础配置
import { getTaskIndex, getPrimedColPropList, getDynamicColPropList, clearRepeatData, getDetailDynamicColPropList } from './someMethods' //整理数据方法
import { lookDetail } from './contextMenu.js'
export default {
    name: 'SummaryAccount',
    components: {
        HotTable,
        TaskRecord
    },
    data: function() {
        return {
            fullscreeLoading: false,
            taskRecordLoading: false,
            quotationId: '',
            showTable: false,
            showDetailTable: false,
            root: 'preview-hot',
            rootDetail: 'detail-table',
            hotSettings: {},
            detailSettings: {},
            funcTaskList: [],
            costList: [],
            groupList: [],
            optionList: [],
            taskRecordList: [],
            title: {
                projName: '',
                quotationName: '',
                version: ''
            },
            firstDetail: true
        }
    },
    created() {
        let that = this
        this.userId = this.$cookies.get('userId')
        this.quotationId = location.href.split('?')[1].split('=')[1]
        this.fullscreeLoading = true
        this.hotSettings = JSON.parse(JSON.stringify(basicConfig)) //excel基本配置
        this.detailSettings = JSON.parse(JSON.stringify(basicConfig))
        this.hotSettings.fillHandle = false
        this.hotSettings.contextMenu.items.lookDetail = lookDetail
        this.hotSettings.contextMenu.items.lookDetail.callback = function() {
            const selectedCell = this.getSelected()
            const row = selectedCell[0][0]
            const col = selectedCell[0][1]
            const rowData = this.getSourceData()[row]
            const funcId = rowData.func_id
            that.showHistory(funcId)
        }
        this.getDetailQuote()
        this.getSummaryAccount()
    },
    mounted() {},
    methods: {
        getDetail(funcId) {
            reqDetail(funcId).then(res => {
                if(res.data.content.data_list.length === 0) {
                    this.showDetailTable = false
                    this.firstDetail = true
                } else {
                    this.getDetailDynamicBasicConfig(res)
                } 
                this.taskRecordLoading = false
            })
        },
        getDetailDynamicBasicConfig(res) {
            
            let settingsColumns = []
            let settingsData = []
            let nestedHeaders = [[], [], []]
            let settingFiexedLeftNum = 0

            let data = res.data.content
            /**
             * 表格列配置
             */
            let colPropList = getPrimedColPropList(data) //处理数据，返回预处理的列表头数据，用来下一步计算
            let dynamicColPropList = getDetailDynamicColPropList(colPropList) ////获得表头列columns（不是固定列的部分）
            settingFiexedLeftNum = colPropList[0].length//固定列数
            colPropList[0].map(item => {
                //固定的前几列: task、sub
                let singleColSetting = {
                    data: item,
                    readOnly: true
                }
                settingsColumns.push(singleColSetting)
            })
            
            dynamicColPropList.map((item, index) => {
                // options
                let optionProp = item.split('.')[2]
                let singleColSetting = {
                    data: item,
                    readOnly: true
                }
                settingsColumns.push(singleColSetting)
            })
            
            let funcTaskList = res.data.content.func_task_list
            let funcTaskLen = res.data.content.func_task_list.length
            let quoteList = res.data.content.data_list
            let quoteLen = res.data.content.data_list.length - 1
            if (quoteList.length != 0) {
                settingsData = clearRepeatData(funcTaskLen, quoteLen, funcTaskList, quoteList) //清理固定列重复数据
                for (let item of settingsData) {
                    item.superGroup = typeof item.group_id[0] == 'undefined' ? '' : item.group_id[0]
                    item.group = typeof item.group_id[1] == 'undefined' ? '' : item.group_id[1]
                }
            }

            /**
             * ================================================================================================
             * 合并表头list
             */
            let groupSum = 0
            for(let item of colPropList[2]) {
                groupSum += item.length
            }
            const numOfOptions = groupSum
            // 获得表头第三列数据
            nestedHeaders[2] = nestedHeaders[2].concat(colPropList[0])
            for (let i = 0; i < numOfOptions; i++) {
                nestedHeaders[2] = nestedHeaders[2].concat(colPropList[3])
            }
           
            // 获得表头第二列数据
            const numOfFixed = colPropList[0].length
            for (let i = 0; i < numOfFixed; i++) {
                nestedHeaders[1].push('')
            }
            // for (let i = 0; i < colPropList[1].length; i++) {
            for (let j = 0; j < colPropList[2].length; j++) {
                for(let item of colPropList[2][j]) {
                    nestedHeaders[1].push({
                        label: item,
                        colspan: 4
                    })
                }
            }
           
            // }
            // 获得表头第一列数据
            for (let i = 0; i < numOfFixed; i++) {
                nestedHeaders[0].push('')
            }
            for (let i = 0; i < colPropList[1].length; i++) {
                nestedHeaders[0].push({
                    label: colPropList[1][i],
                    colspan: colPropList[2][i].length * colPropList[3].length
                })
            }
            
            if (this.firstDetail === true) {
                //第一次进入，获取不到this.$refs.textHot.hotInstance
                this.detailSettings.fixedColumnsLeft = settingFiexedLeftNum //固定列数
                this.detailSettings.columns = settingsColumns
                this.detailSettings.data = settingsData
                this.detailSettings.nestedHeaders = nestedHeaders
                this.firstDetail = false
                let copyright_logo = document.getElementById('hot-display-license-info')
                copyright_logo.style = 'display:none'
            } else {
                this.$refs.detailTable.hotInstance.updateSettings({
                    fixedColumnsLeft: settingFiexedLeftNum, //固定列数
                    columns: settingsColumns,
                    data: settingsData,
                    nestedHeaders: nestedHeaders
                })
                
            }
            this.showDetailTable = true
        },
        getDynamicBasicConfig(res) {
            let settingsColumns = []
            let settingsData = []
            let nestedHeaders = [[], ['category']]
            let settingFiexedLeftNum = 0

            let data = res.data.content
            this.funcTaskList = data.func_task_list //sub、task
            this.groupList = data.group_list //组名
            this.costList = data.cost_list //组下面的选项（days，precondition，comment，status）
            this.optionList = data.option_list //option

            /**
             * 表格列配置
             */
            let colPropList = getPrimedColPropList(data).filter(item => {
                return item.length != 0
            }) //处理数据，返回预处理的列表头数据，用来下一步计算
            let dynamicColPropList = getDynamicColPropList(colPropList) ////获得表头列columns（不是固定列的部分）
            settingFiexedLeftNum = colPropList[0].length + 1 //固定列数
            settingsColumns.push({
                //手动添加category列，这里可以改进合并进下面代码
                data: 'category_name',
                readOnly: true
            })
            colPropList[0].map(item => {
                //固定的前几列: task、sub
                let singleColSetting = {
                    data: item,
                    readOnly: true
                }
                settingsColumns.push(singleColSetting)
            })
            dynamicColPropList.map((item, index) => {
                // options
                let optionProp = item.split('.')[2]
                let singleColSetting = {
                    data: item,
                    readOnly: true
                }
                settingsColumns.push(singleColSetting)
            })
            let that = this
            function detailCellStyle(instance, td, row, col, prop, value, cellProperties) {
                const escaped = Handsontable.helper.stringify(value)
                let btn = null
                let btnValue = document.createTextNode('详细')
                btn = document.createElement('BUTTON')
                btn.appendChild(btnValue)

                Handsontable.dom.addEvent(btn, 'mousedown', function(event) {
                    const rowData = instance.getSourceData()[row]
                    const funcId = rowData.func_id
                    
                    that.showHistory(funcId)
                    event.preventDefault()
                })

                Handsontable.dom.empty(td)
                td.appendChild(btn)
                return td
            }
            settingsColumns.push({
                data: 'detainBtn',
                readOnly: true,
                renderer: detailCellStyle
            }) //后期额外增加一列（用来存放详细按钮）
            let funcTaskList = res.data.content.func_task_list
            let funcTaskLen = res.data.content.func_task_list.length
            let quoteList = res.data.content.data_list
            let quoteLen = res.data.content.data_list.length - 1
            if (quoteList.length != 0) {
                settingsData = clearRepeatData(funcTaskLen, quoteLen, funcTaskList, quoteList) //合并重复数据
            }

            // 获得表头第二列数据
            const numOfFixed = colPropList[0].length + 1
            for (let item of colPropList[0]) {
                nestedHeaders[1].push(item)
            }
            for (let i = 0; i < colPropList[1].length; i++) {
                for (let j = 0; j < colPropList[2].length; j++) {
                    nestedHeaders[1].push(colPropList[2][j])
                }
            }
            nestedHeaders[1].push('') //后期额外增加一列（用来存放详细按钮）
            //获得表头第一列数据
            nestedHeaders[0].push('Item and Scope')
            for (let i = 1; i < numOfFixed; i++) {
                nestedHeaders[0].push('')
            }
            for (let i = 0; i < colPropList[1].length; i++) {
                nestedHeaders[0].push({
                    label: colPropList[1][i],
                    colspan: 4
                })
            }
            nestedHeaders[0].push('详细') //后期额外增加一列（用来存放详细按钮）
            this.hotSettings.fixedColumnsLeft = settingFiexedLeftNum //固定列数
            this.hotSettings.columns = settingsColumns
            this.hotSettings.data = settingsData
            this.hotSettings.nestedHeaders = nestedHeaders
        },
        getSummaryAccount() {
            reqSummaryAccount(this.quotationId, this.userId)
                .then(res => {
                    this.getDynamicBasicConfig(res)
                    this.showTable = true
                    this.fullscreeLoading = false
                })
                .catch(err => {
                    this.fullscreeLoading = false
                })
        },
        getDetailQuote() {
            reqDetailQuote(this.quotationId).then(res => {
                const data = res.data.content
                if (res.data.result == 'OK') {
                    this.title.projName = '项目名：' + data.proj_name
                    this.title.quotationName = '报价名：' + data.quotation_name
                    this.title.version = '版本：' + data.quotation_ver
                }
            })
        },
        showHistory(funcId) {
            let that = this
            this.taskRecordLoading = true
            $('.shadow').animate({ right: '1px' }, 1000, function() {
                that.getDetail(funcId)
                that.taskRecordLoading = false
            })
            
        },
        hideHistory() {
            $('.shadow').animate({ right: '-2000px' }, 1000)
        }
    }
}
</script>
<style scoped>
@import './handsontable.css';
.container {
    width: 100%;
    height: 100%;
}
.title {
    float: left;
    font-size: 30px;
    font-weight: 600;
    margin-top: 10px;
    margin-left: 10px;
}
.btn-switch {
    float: right;
    padding: 10px 15px 0 0;
}
.hottable-wrapper {
    position: absolute;
    left: 0;
    right: 0;
    top: 50px;
    bottom: 0;
    overflow: hidden;
}
#test-hot {
    width: 100%;
    height: 800px;
    overflow: hidden;
}
.shadow {
    width: 55%;
    height: calc(100% - 48px);
    position: fixed;
    background: rgba(255, 254, 255);
    top: 48px;
    right: -2000px;
    z-index: 666;
    text-align: left;
    border-radius: 5px;
    filter: drop-shadow(0 3px 5px black);
}
.el-icon-d-arrow-right {
    font-size: 24px;
    padding: 10px;
    cursor: pointer;
}
</style>
