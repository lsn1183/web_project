<template>
    <div class="warpper">
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
        <div class="content excel-5">
            <hot-table :settings="settings" ref="hot" ></hot-table>
        </div>
    </div>
</template>
<script>
import { get_chapter_list, uodate_chapter_list,select_opeType,select_condition,select_display ,ope_list} from "@/api/api";
import { HotTable } from "@handsontable-pro/vue";
import "../../../node_modules/handsontable-pro/dist/handsontable.full.min.css";
import '../../../node_modules/handsontable-pro/languages/zh-CN.js' //中文
import config from "@/components/Plugins/config/PlugPublicConfig"
import fn from "@/components/Plugins/config/gloable_fn";
import '@/components/Plugins/style/handsontable.less';
import '@/components/Plugins/style/handsontable.5.less';
import Hamburger from '@/components/FoldBtn'
import { mapGetters } from 'vuex'
export default {
    components: {
        HotTable,
        Hamburger
    },
    data() {
        return {
            loading: false,
            settings: config,
            screen_gid: null,
            func: fn,
            select_list: [],
            width: 0,
            height:0,
            proj_id: null,
            type: 5,
            user_id: null,
            screenId:'',
            screenName:""
        };
    },
    computed: {
        ...mapGetters([
            'sidebar'
        ])
    },
    mounted() {
        this.default_mounted_fun();
    },
    updated() {
        window.onresize = () => {
            this.toggleSideBar()
        };
    },
    destroyed(){
        this.settings.data={}
    },
    methods: {
        toggleSideBar() {
            setTimeout(() => {
                this.$refs.hot.hotInstance.updateSettings({
                    width: '100%',
                    height:'100%'
                })
            }, 280); // transition 0.28s
            this.$store.dispatch('toggleSideBar')
        },
        default_mounted_fun() {
            this.screen_gid = this.$route.query.screen_gid
            this.proj_id = this.$route.query.proj_id
            this.user_id = this.$cookies.get('userId')
            this.promise_all()
        },
        promise_all() {
            this.loading = true
            get_chapter_list(this.screen_gid, this.type).then(res => {//创建请求
                // console.log(res,'===========');
                if (res.data.result == "OK") {
                    const table_data = res.data.content
                    //创建表格数据方法 
                    table_data.length>0?this.created_table(table_data):this.loading = false
                } else {
                    this.$message({ type: 'error', message: res.data.error })
                }
                this.loading = false
            });
            ope_list(this.screen_gid).then(res=>{
                if (res.data.result == "OK") {
                    console.log(res,'---------');
                    this.screenId = res.data.content.screen_id
                    this.screenName = res.data.content.screen_name
                } else {
                    this.$message({ type: 'error', message: res.data.error })
                }
            })
        },
        created_table(table_all_data) {
            /*
             1.获取设定的header_name与 prop的key对应关系表
             2.获取表头 列表
             3.id化：hk_ope_type，active_condition_phrase，hk_action，id化的字段使用选择框
            4.colWidths：设置每一列宽度
             */
            let header_matchup = this.func.header_matchup_data5(),//表5配置数据
                columns_arr = this.func.hasKeyFn(header_matchup),
                avg_widtn = 40,
                promise = new Promise((resolve, reject)=>{
                    resolve ("success")
                })
            promise.then(()=>{
                this.setHeader(columns_arr, avg_widtn)
            }).then(()=>{
                this.setMethods()
            }).then(()=>{
                this.setWidth(avg_widtn)
            }).then(()=>{
                this.settings.data = table_all_data
            })
            // console.log(this.settings.data,'this.settings.data');
            // this.settings.data = table_all_data
        },
        setHeader(columns_arr, avg_widtn) {
            this.settings.columns = columns_arr.map((item,index) => {
                if (item.value == 'init_ope_type' || item.value == 'init_condition_phrase' || item.value == 'init_action') {
                    return { data: item.value, type: "autocomplete", source: this.select_list,strict: false, 
                        filter: false, trimDropdown: false, }
                } else {
                    if (item.value == 'init_chapter'||item.value == 'init_no'||item.value == 'init_state_no'||item.value == 'init_status') {
                        return { data: item.value, type: 'text',readOnly:true }
                    } else {
                        return { data: item.value, type: 'text' }
                    }
                }
            });
            // console.log(this.settings.colHeaders,'this.settings.colHeaders');
            this.settings.nestedHeaders = [
                [this.type,{ label: "Initialized Status", colspan: 3 }, "Formula",{ label: "Condition of Action", colspan: 2 },
                    "Action in Such Condition", "Transition", "Remark",'','UUID','Event', { label: 'View Model', colspan: 2 },
                    'Func of Model', 'Observer', 'Reply', 'TransType','TransID'],
            ];
        },
        setWidth(avg_widtn) {
            this.settings.colWidths = [
                avg_widtn,
                avg_widtn,
                avg_widtn,
                avg_widtn * 7,
                avg_widtn * 2,
                avg_widtn,
                avg_widtn * 9,
                avg_widtn * 8,
                avg_widtn * 6,
                avg_widtn * 3,
                avg_widtn * 2,
                // avg_widtn * 2,//分割线
                avg_widtn * 8,
                avg_widtn * 3,
                avg_widtn * 1,
                avg_widtn * 4,
                avg_widtn * 3,
                avg_widtn * 3,
                avg_widtn * 4,
                avg_widtn * 2,
                avg_widtn * 2,
            ];
        },
        setMethods() {
            let this_ = this
            this.settings.contextMenu = {
                items: {
                    row_below: {},// name: '下方插入一行'
                    // col_right: {},
                    hsep1: '---------', //提供分隔线
                    // remove_row: {},
                    // remove_col: {},//删除列
                    hsep2: '---------'
                }
            };
            this.settings.contextMenu.items.row_below = {
                disabled() {
                    return false
                },
                //下方插入行
                callback() {
                    const curRowIndex = this.getSelectedLast()[0]
                    const curRowData = JSON.parse(JSON.stringify(this_.settings.data[curRowIndex]))
                    // console.log(curRowData ,'curRowData',this.getSelectedLast()[0])
                    delete curRowData.chapter5_id
                    this_.settings.data.splice(curRowIndex + 1, 0, curRowData)
                }
            };
            this.settings.afterChange = (changes, source) => {
                // console.log(changes, 'changes', source,'afterChange进来了')
                if (changes == null) {
                    return false
                }
                if (source == 'edit') {
                    changes.forEach(([row, prop, oldValue, newValue]) => {
                        // console.log(row, prop, oldValue, newValue,'row, prop, oldValue, newValue')
                        if (prop == 'init_condition_phrase') {
                            for (const item of this.select_list) {
                                if (newValue == item.display) {
                                    this.settings.data[row].fun_of_model = item.ope_event
                                    break
                                }
                            }
                        }else if(prop == 'init_ope_type'){
                            for (const item of this.select_list) {
                                if (newValue == item.ope_type) {
                                    this.settings.data[row].hk_event = item.ope_event
                                    break
                                }
                            }
                        }else if(prop =='init_action'){
                            for (const item of this.select_list) {
                                if (newValue == item.condition) {
                                    this.settings.data[row].view_model = item.ope_event
                                    break
                                }
                            }
                        }
                    })
                }
                
            };
            this.settings.afterOnCellMouseDown = (event, coords, TD) => {//点击表格获取相应位置方法
                // console.log( coords, TD,'afterOnCellMouseDown进来了')
                let MouseDown_req_flag = this.settings.columns[coords.col].type
                if (MouseDown_req_flag) {
                    const req_fn = new req_select_fn(),
                    type_name = this.settings.columns[coords.col].data
                    this.select_list.length = 0//清空选择框
                    if (type_name == "init_ope_type") {
                        req_fn.select_opeType_fn(this.proj_id)
                    }else if(type_name == "init_condition_phrase"){
                        req_fn.select_condition_fn(this.proj_id)
                    }else if(type_name == "init_action"){
                        req_fn.select_display_fn(this.proj_id)
                    }
                    
                } else {
                    return false
                }
                // console.log(this.settings.data[coords.row],'row');
                // console.log(this.settings.columns[coords.col],'aaaaa');
            };
            function clear_attributes_fun(data, columns_name) {//合并相同行
                if (columns_name == 'sub1' || columns_name == 'sub2' || columns_name == 'category_name') {
                    let make_index_arr = [],
                        index_value = null;
                    for (let i = 0; i < data.length; i++) {
                        if (i == 0) {
                            make_index_arr.push(1)
                            index_value = 0
                        } else {
                            if (data[i][columns_name] == data[i - 1][columns_name]) {
                                make_index_arr[index_value] += 1
                                make_index_arr.push(0)
                            } else {
                                make_index_arr.push(1)
                                index_value = i
                            }
                        }
                    }
                    for (let j = 0; j < make_index_arr.length; j++) {
                        if (make_index_arr[j] == 0) {
                            data[j][columns_name] = ""
                        } else {
                            data[j][columns_name] = data[j][columns_name]
                        }
                    }
                    return data
                }

            }
            class req_select_fn {
                select_opeType_fn(proj_id){
                    select_opeType(proj_id).then(res=>{
                        // console.log(res,'------------------aaa');
                        if (res.data.result == 'OK') {
                            for (const item of res.data.content) {
                                this_.select_list.push(item.ope_type)
                            }
                        } else {
                            this.$message({
                                type:"error",
                                message:"失败！"+res.data.error
                            })
                        }
                    })
                }
                select_condition_fn(proj_id){
                    select_condition(proj_id).then(res=>{
                        // console.log(res,'------------------bbb',);
                        if (res.data.result == 'OK') {
                            
                            for (const item of res.data.content) {
                                this_.select_list.push(item.view_model)
                            }
                        } else {
                            this.$message({
                                type:"error",
                                message:"失败！"+res.data.error
                            })
                        }
                    })
                }
                select_display_fn(proj_id){
                    select_display(proj_id).then(res=>{
                        // console.log(res,'------------------ccc',this_.select_list);
                        if (res.data.result == 'OK') {
                            for (const item of res.data.content) {
                                this_.select_list.push(item.fun_of_model)
                            }
                        } else {
                            this.$message({
                                type:"error",
                                message:"失败！"+res.data.error
                            })
                        }
                    })
                }
            }
        },
        save() {
            let save_data = {
                proj_id: Number(this.proj_id),
                screen_gid: Number(this.screen_gid),
                commit_user: Number(this.user_id),
                chapter_list: this.settings.data
            }
            // console.log(save_data);
            uodate_chapter_list(this.type, save_data).then(res => {
                // console.log(res, 'aaaaaaaaaa');
                if (res.data.result == 'OK') {
                    this.$message({
                        type:"success",
                        message:"保存成功！"
                    })
                } else {
                    this.$message({
                        type:"error",
                        message:"失败！"+res.data.error
                    })
                }
            })

        },
        cancel(){
            this.$router.push('/project_list')
        }

    }
};
</script>

<style  scoped lang="less">
// 通用大模块样式
.warpper {
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

}
</style>
