<template>
    <div class="excel-container">
        <div class="header">
            <div class="left">
                <el-breadcrumb separator-class="el-icon-arrow-right" style="padding-top: 3px;font-weight: bold;font-size: 22px;">
                    <el-breadcrumb-item>{{screenId}}</el-breadcrumb-item>
                    <el-breadcrumb-item>{{screenName}}</el-breadcrumb-item>
                </el-breadcrumb>
            </div>
            <div class="right">
                <el-button class="el-btn" @click="save()" size="small" type='primary'>保存</el-button>
                <el-button class="el-btn" @click="cancel()" size="small">退出</el-button>
                <hamburger
                    :isActive="sidebar.opened"
                    :toggleClick="toggleSideBar"
                    class="hamburger-container"
                ></hamburger>
            </div>
        </div>
        <div class="excel-main">
        <hot-table v-if="isVisible" :root="root" ref="textHot" :settings="settings"></hot-table>
        </div>
    </div>
  
</template>
<script>
import { HotTable } from '@handsontable-pro/vue'
import Handsontable from 'handsontable-pro'
import "../../../../node_modules/handsontable-pro/dist/handsontable.full.css";
import { Message, MessageBox } from 'element-ui' // element UI
import 'handsontable-pro/languages/zh-CN' //中文包
import basicHotSettings from '@/components/Handsontable/basicConfig' //表格基础配置

import Hamburger from '@/components/FoldBtn'
import { mapGetters } from 'vuex'
import { getExcelData, saveExcelData, getOpeInfo, getSelectedData } from '@/api/excel'

import { columns, nestedHeaders, afterGetColHeader, afterGetRowHeader } from '@/views/excel/excelOne/columns'

export default {
  name: "item3",
  components:  {
    HotTable,
    Hamburger
  },
  data () {
    return {
      settings: basicHotSettings,
      root: 'excel',
      screenId: '',
      screenName: '',
      isVisible: false,

      displayArr: [],
      displayConditionArr: [],
      propertyTypeArr: [],
      opeTypeArr: [],
      eventArr: [],

      relDisplayConditionArr: [],
      relDisplayArr: [],
      relPropertyTypeArr: [],
      
      
    };
  },
  created() {
    const projId = this.$route.query.proj_id
    const gid = this.$route.query.screen_gid
    let data = []

    // Display Condition
    const displayConditionPromise = new Promise((resolve, reject) => {
      getSelectedData('Condition',projId).then(res => {
        let tempObj = {}
        for(let item of res.data.content) {
          const keys = item['condition']
          const value = item['view_model']
          tempObj[keys] = value
        }
        this.relDisplayConditionArr = tempObj
        resolve(res.data.content)
      })
    })

    // Display in Such Condition
    const displayPromise = new Promise((resolve, reject) => {
      getSelectedData('Display',projId).then(res => {
        let tempObj = {}
        for(let item of res.data.content) {
          const keys = item['display']
          const value = item['fun_of_model']
          tempObj[keys] = value
        }
        this.relDisplayArr = tempObj
        resolve(res.data.content)
      })
    })

    // Property Type
    const propertyTypePromise = new Promise((resolve, reject) => {
      getSelectedData('Property',projId).then(res => {
        let tempObj = {}
        for(let item of res.data.content) {
          const keys = item['condition']
          const value = item['view_model']
          tempObj[keys] = value
        }
        this.relPropertyTypeArr = tempObj
        resolve(res.data.content)
      })
    })

    const promiseArr = [displayConditionPromise, displayPromise, propertyTypePromise]
    Promise.all(promiseArr).then(resArr => {
      columns[8].source = this.displayConditionArr = resArr[0].map(item => {
        return item.condition
      })
      columns[9].source = this.displayArr = resArr[1].map(item => {
        return item.display
      })
      columns[10].source = this.propertyTypeArr = resArr[2].map(item => {
        return item.property
      })
    }).then(() => {
      getExcelData(gid, 1).then(res => {
        data = res.data.content
        // 下拉框列
        let that = this
        this.settings.afterChange = function(arr, source) {
          if (arr == null) {
            return
          }
          for(let item of arr) {
            const row = item[0]
            const colProp = item[1]
            const oldValue = item[2]
            const newValue = item[3]
            const colArr = ['display_condition_phrase', 'display_action', 'display_property_type']
            if (newValue != '' && newValue != oldValue && colArr.indexOf(colProp) != -1) {
              let settingsColumns = this.getSettings().__proto__.columns
              switch (colProp) {
                case 'display_condition_phrase':
                  if(that.displayConditionArr.indexOf(newValue) != -1) { //有对应值
                    this.setDataAtCell(row, 19, that.relDisplayConditionArr[newValue])
                  } else { //无对应值
                    //筛选是否有相同的选项
                    const hasDiffArr = that.displayConditionArr.filter(item => {
                        return item === newValue
                    })
                    if (hasDiffArr.length == 0) {
                        //'前提'元格:可以自己手动增加下拉选项
                        that.displayConditionArr.push(newValue)
                    }
                  }
                  break;
                case 'display_action':
                  if(that.displayArr.indexOf(newValue) != -1) {
                    this.setDataAtCell(row, 17, that.relDisplayArr[newValue])
                  } else {
                    //筛选是否有相同的选项
                    const hasDiffArr = that.displayArr.filter(item => {
                        return item === newValue
                    })
                    if (hasDiffArr.length == 0) {
                        //'前提'元格:可以自己手动增加下拉选项
                        that.displayArr.push(newValue)
                    }
                  }
                  break;
                case 'display_property_type':
                  if(that.propertyTypeArr.indexOf(newValue) != -1) {
                    this.setDataAtCell(row, 16, that.relPropertyTypeArr[newValue])
                  } else {
                    //筛选是否有相同的选项
                    const hasDiffArr = that.propertyTypeArr.filter(item => {
                        return item === newValue
                    })
                    if (hasDiffArr.length == 0) {
                        //'前提'元格:可以自己手动增加下拉选项
                        that.propertyTypeArr.push(newValue)
                    }
                  }
                  break;
                default:
                  break;
              }
            }
          }
        }
        
        this.settings.afterGetColHeader = afterGetColHeader;
        this.settings.afterGetRowHeader = afterGetRowHeader;
        this.settings.nestedHeaders = nestedHeaders
        this.settings.columns = columns
        this.settings.data = data
        this.isVisible = true
      })
    })

    
    getOpeInfo(29).then(res => {
      this.screenId = res.data.content.screen_id
      this.screenName = res.data.content.screen_name
    })
    
    
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ])
  },
  methods: {
    toggleSideBar() {
      setTimeout(() => {
        this.$refs.textHot.hotInstance.updateSettings({
          width: '100%'
        })
      }, 280); // transition 0.28s
      this.$store.dispatch('toggleSideBar')
    },
    cancel() {
      const projId = this.$route.query.proj_id
      const pathObj = { path: "/project_detail", query: { 'proj_id': projId } }
      this.$router.push(pathObj)
    },
    save() {
      const data = {
        proj_id: this.$route.query.proj_id,
        screen_gid: this.$route.query.screen_gid,
        commit_user: this.$cookies.get('userId'),
        chapter_list: this.$refs.textHot.hotInstance.getSourceData()
      }
      saveExcelData(1, data).then(() => {
        this.$message({
            type:"success",
            message:"保存成功",
            duration: 2000,
            showClose: false
        })
      })
    }
  }
}
</script>
<style scoped lang="less">
@import "../style/excel.css";
.header {
        display: flex;
        height: 50px;
        // line-height: 50px;
        justify-content: space-between;
        flex-flow:  row nowrap;
        align-items: center;
       .right{
           display: flex;

       }
    }
    .el-btn{
        margin-right:20px;
        padding: 0px 15px;
        height: 30px;
    }
</style>