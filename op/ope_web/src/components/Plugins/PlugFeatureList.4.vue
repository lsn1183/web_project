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
        <div class="content excel-4">
            <hot-table :settings="settings" ref="hot" ></hot-table>
        </div>
    </div>
</template>
<script>
import { get_chapter_list, uodate_chapter_list,select_opeType,select_condition,select_display,ope_list } from "@/api/api";
import { HotTable } from "@handsontable-pro/vue";
import "../../../node_modules/handsontable-pro/dist/handsontable.full.min.css";
import '../../../node_modules/handsontable-pro/languages/zh-CN.js' //中文
import config from "@/components/Plugins/config/PlugPublicConfig"
import fn from "@/components/Plugins/config/gloable_fn";
import '@/components/Plugins/style/handsontable.less';
import '@/components/Plugins/style/handsontable.4.less';
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
            type: 4,
            user_id: null,
            ope_type_select_data:[],
            condition_select_data:[],
            display_select_data:[],
            screenId:'',
            screenName:""
        };
    },
    computed: {
        ...mapGetters([
            'sidebar'
        ]),
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
            // this.loading = true
            get_chapter_list(this.screen_gid, this.type).then(res => {//创建list请求
                // console.log(res.data,'11111111');
                if (res.data.result == "OK") {
                    let table_data = res.data.content
                    //创建表格数据方法 
                    table_data.length>0?this.created_table(table_data):this.loading = false
                } else {
                    this.$message({ type: 'error', message: res.data.error })
                }
                this.loading = false
            }).then(()=>{
                ope_list(this.screen_gid).then(res=>{
                    if (res.data.result == "OK") {
                        // console.log(res,'---------');
                        this.screenId = res.data.content.screen_id
                        this.screenName = res.data.content.screen_name
                    } else {
                        this.$message({ type: 'error', message: res.data.error })
                    }
                })
            })
            
        },
        created_table(table_all_data) {
            /*
             1.获取设定的header_name与 prop的key对应关系表
             2.获取表头 列表
             3.id化：hk_ope_type，active_condition_phrase，hk_action，id化的字段使用选择框
            4.colWidths：设置每一列宽度
             */
            class req_select_fn {//请求下拉框函数
                select_opeType_fn(proj_id){
                    select_opeType(proj_id).then(res=>{
                        // console.log(res,'------------------aaa');
                        if (res.data.result == 'OK') {
                            this_.ope_type_select_data = res.data.content
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
                            this_.condition_select_data = res.data.content
                           
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
                            this_.display_select_data = res.data.content
                        } else {
                            this.$message({
                                type:"error",
                                message:"失败！"+res.data.error
                            })
                        }
                    })
                }
            }
            const req_fn = new req_select_fn(),
            this_ = this
            let header_matchup = this.func.header_matchup_data4(),
                columns_arr = this.func.hasKeyFn(header_matchup),
                avg_widtn = 40,
                promise = new Promise((resolve, reject)=>{
                    resolve ("success")
                })
            promise.then(()=>{
                // let plugins = this.$refs.hot.hotInstance.getPlugin('ganttChart')
                // console.log(plugins,'aplugins');
                
                // plugins.setRangeBarColors(
                //     {
                //         1: 'red' ,
                //         4: ['#2A74D0', '#588DD0'] 
                //     }
                // )
                this.setMethods()
            }).then(()=>{
                this.setWidth(avg_widtn)
            }).then(()=>{
                this.setHeader(columns_arr, avg_widtn)
            }).then(()=>{
                this.settings.data = table_all_data
                
            }).then(()=>{
                req_fn.select_opeType_fn(this.proj_id)
            }).then(()=>{
                req_fn.select_condition_fn(this.proj_id)
            }).then(()=>{
                req_fn.select_display_fn(this.proj_id)
            })
           
        },
        setHeader(columns_arr,avg_widtn) {
            this.settings.columns = columns_arr.map((item,index) => {
                if (item.value == 'hk_ope_type' || item.value == 'hk_condition_phrase' || item.value == 'hk_action') {
                    return { data: item.value, type: "autocomplete", source: this.select_list,strict: false, 
                        filter: false, trimDropdown: false, }
                } else {
                    if (item.value == 'hk_chapter'||item.value == 'hk_sub_chapter'||item.value == 'hk_dev_name'||item.value == 'hk_no'||
                    item.value == 'hk_state_no'||item.value =='hk_name') {
                        return { data: item.value, type: 'text',readOnly:true }
                        
                    } else {
                        return { data: item.value, type: 'text' }
                    }
                }
            });
            // console.log(this.settings.columns.slice[0,4],'slice');
            // console.log(columns_arr,'columns_arr');
            this.settings.nestedHeaders = [
                ["4", { label: "Hard Key Action", colspan: columns_arr.length - 1 }],
                ["4", "1", 'Dev Name', { label: "Normal", colspan: 3 }, "Ope Type", "Formula", { label: "Condition of Action", colspan: 2 },
                    "Action in Such Condition", "Transition", "Sound", "DuringDriving", "Remark", '','UUID','HardKey Event', { label: 'View Model', colspan: 2 },
                    'Func of Model', 'Observer', 'Reply','TransType','TransID' ],
            ];
        },
        setWidth(avg_widtn) {
            avg_widtn = 40
            this.settings.colWidths = [
                avg_widtn,
                avg_widtn,
                avg_widtn,
                avg_widtn,
                avg_widtn,
                avg_widtn * 6,
                avg_widtn * 2,
                avg_widtn * 3,
                avg_widtn,
                avg_widtn * 6,
                avg_widtn * 8,
                avg_widtn * 3,
                avg_widtn * 3,
                avg_widtn * 3,
                avg_widtn * 4,
                avg_widtn * 2,
                avg_widtn * 6,
                avg_widtn * 2,
                avg_widtn,
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
                    const curRowIndex = this.getSelectedLast()[0],
                    curRowData = JSON.parse(JSON.stringify(this_.settings.data[curRowIndex]))
                    // console.log(curRowData ,'curRowData',this.getSelectedLast()[0])
                    delete curRowData.chapter4_id
                    this_.settings.data.splice(curRowIndex + 1, 0, curRowData)
                }
            };
            
            this.settings.afterChange = (changes, source) => {
                // console.log(changes, 'changes', source,'afterChange进来了')
                if (changes == null) {
                    return false
                }
                
                // return
                if (source == 'edit') {
                    changes.every(([row, prop, oldValue, newValue]) => {
                        console.log( prop,'prop')
                        console.log( newValue,'newValue')
                        console.log( this.select_list,'select_list_data')
                        console.log(this.settings.data[row],'row-item');
                        let check_select_fn = (row,newValue,prop,table_data,select_all_data,parent_key,child_key)=>{
                            //prop:选择框的类型，row:行数，newValue:选择的值，select_list_data:选择框的数据,
                            // table_data: this.settings.data ; select_all_data : 选择框原始数据 
                            let select_relation_table = [
                                {parent:"hk_condition_phrase",child:"hk_condition_code"},
                                {parent:"hk_action",child:"hk_action_model"},
                                {parent:"hk_ope_type",child:"hk_event"},
                                {parent:"init_condition_phrase",child:"init_condition_code"},
                                {parent:"init_action",child:"init_action_model"},
                                {parent:"status_change_condition_f_phrase",child:"hk_condition_code"},
                                {parent:"status_change_condition_b_phrase",child:"status_change_condition_b_code"},
                                {parent:"status_change_condition_i_phrase",child:"status_change_condition_i_code"},
                                {parent:"status_change_f_action",child:"status_change_f_action_model"},
                                {parent:"status_change_b_action",child:"status_change_b_action_model"},
                                {parent:"status_change_i_action",child:"status_change_i_action_model"},
                                {parent:"transition_condition_f_phrase",child:"transition_condition_f_code"},
                                {parent:"transition_condition_b_phrase",child:"transition_condition_b_code"},
                                {parent:"transition_condition_i_phrase",child:"transition_condition_i_code"},
                                {parent:"transition_f_action",child:"transition_f_action_model"},
                                {parent:"transition_b_action",child:"transition_b_action_model"},
                                {parent:"transition_i_action",child:"transition_i_action_model"},
                                {parent:"trig_condition_phrase",child:"trig_condition_code"},
                                {parent:"trig_action",child:"trig_action_model"},
                                {parent:"trig_name",child:"trig_trig"},

                                {parent:"display_condition_phrase",child:"display_condition_code"},
                                {parent:"display_action",child:"display_action_model"},
                                {parent:"display_property_type",child:"display_property"},
                                {parent:"active_condition_phrase",child:"active_condition_code"},
                                {parent:"active_action",child:"active_action_model"},
                                {parent:"active_property_type",child:"active_property"},
                                {parent:"action_condition_phrase",child:"action_condition_code"},
                                {parent:"action_action",child:"action_action_model"},
                                {parent:"action_ope_type",child:"action_event"},

                            ],
                            /*
                                1.获取表格的选择的一行数据，
                                2.取所有的（select_relation_table）的（item.parent）字段与prop的比对，从而得到 需要被赋值的字段（item.child）
                                3.赋值 表格该行的（item.child字段）的value，所以需要找出下拉框总数据(select_all_data)里面的parent字段的值与 newValue相等后取select_all_data的该item的 child_key 的value
                             */
                            table_row_data = table_data[row] //1.表格某一行的数据
                            console.log(parent_key,child_key,'parent_key,child_key');
                            
                            for (let select_relation_table_item of select_relation_table) {
                                if ( select_relation_table_item.parent === prop ) { //
                                    let key = select_relation_table_item.child //表格的某一行需要被联动赋值的key
                                    for (let select_all_data_item of select_all_data) {
                                        if ( select_all_data_item[parent_key] === newValue ) {//从下拉框原数据取需要的值
                                            table_row_data[key] = select_all_data_item[child_key]
                                            break
                                        }
                                    }
                                    break
                                }
                            }
                            // console.log(table_data,'table_data');
                            // console.log(this_.settings.data,'daaa');
                            
                            return table_data
                        }
                        if (prop == 'hk_condition_phrase') {
                             check_select_fn(row,newValue,prop,this.settings.data,this.condition_select_data,'condition','view_model')
                        }else if(prop == 'hk_ope_type'){
                           check_select_fn(row,newValue,prop,this.settings.data,this.ope_type_select_data,'ope_type','ope_event')
                        }else if(prop =='hk_action'){
                           check_select_fn(row,newValue,prop,this.settings.data,this.display_select_data,'display','fun_of_model')                            
                        }
                    })

                }
                
            };
            this.settings.afterOnCellMouseDown = (event, coords, TD) => {//点击表格获取相应位置方法
                // console.log( coords, TD,'afterOnCellMouseDown进来了')
                let MouseDown_req_flag = this.settings.columns[coords.col].type,
                    for_fn = (data,parentKey,childrenKey)=>{
                         for (let item of data) {
                            this.select_list.push(item[parentKey])
                        }
                    }
                if (MouseDown_req_flag) {
                    const type_name = this.settings.columns[coords.col].data
                    this.select_list.length = 0//清空选择框
                    if (type_name == "hk_ope_type") {
                        console.log(this.ope_type_select_data,'oooooooooo');
                        for_fn(this.ope_type_select_data,'ope_type','ope_event')
                    }else if(type_name == "hk_condition_phrase"){
                        console.log(this.condition_select_data,'oooooooooo');
                        for_fn(this.condition_select_data,'condition','view_model')
                    }else if(type_name == "hk_action"){
                        console.log(this.display_select_data,'oooooooooo');
                        for_fn(this.display_select_data,'display','fun_of_model')
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
// @import './style/handsontable.less';
// @import './style/handsontable.4.less';
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
