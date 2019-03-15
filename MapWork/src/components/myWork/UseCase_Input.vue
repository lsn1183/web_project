<template>
    <div class="wrapper">
            <div class="block-box Asa-box" v-if="show_table_flag">
                <el-table :data="tableData" border style="width: 100%;" @cell-click="handleEdit" @row-contextmenu="row_click">
                    <el-table-column prop="sec_title" label="UseCase Name" min-width="80">
                    </el-table-column>
                    <el-table-column prop="explain" label="说明（变更点/对应内容等）" min-width="240">
                        <template slot-scope="scope">
                            <span v-if="scope.row.show_flag">{{scope.row.explain}}</span>
                            <el-input  type='textarea' v-model="scope.row.explain" v-else ></el-input> 
                        </template>
                    </el-table-column>
                    <el-table-column prop="func_list" label="关联式样书" min-width="240">
                        <template slot-scope="scope">
                            <span v-if="scope.row.func_list.length !== 0">
                                <li  v-for="(item,index) of scope.row.func_list" :key="index" >
                                    
                                    <a :href="item.html_url" target="_blank" rel="noopener noreferrer">{{item.spec_file_name}}&nbsp;{{item.func_name}}&nbsp;{{item.func_id}}</a>
                                    <i class="el-icon-delete margin-left" title="删除" @click="del_fun_list_item(scope.row.func_list,index)"></i>
                                </li>
                            </span>
                            
                            <el-button type="text"   @click="add_fun_list(scope.row)" style="font-size:12px">
                                <i class="el-icon-circle-plus"></i>关联式样书</el-button>
                        </template>
                    </el-table-column>
                    <el-table-column prop="sec_id" label="操作" width='120'>
                        <template slot-scope="scope">
                            <el-button type="text" @click="add_usecase_level_2(scope.row)">添加二级UseCase</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div  class="block-box Asa-box" v-show="show_table_flag==false">
                <el-table :data="tableData" border style="width: 100%;" :span-method="objectSpanMethod" 
                 @cell-click="handleEdit" @row-contextmenu="row_click">
                        <el-table-column prop="sec_title" label="UseCase Name" min-width="80">
                            <template slot-scope="scope">
                                    <span>{{scope.row.sec_title}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="sec_title_2" label="SubUseCase" min-width="80">
                            <template slot-scope="scope">
                                <span v-if="scope.row.show_flag">{{scope.row.sec_title_2}}</span>
                                <el-input  type='textarea'  v-model="scope.row.sec_title_2" v-else ></el-input> 
                            </template>
                        </el-table-column>
                        <el-table-column prop="explain" label="说明（变更点/对应内容等）" min-width="240">
                            <template slot-scope="scope">
                                <span v-if="scope.row.show_flag">{{scope.row.explain}}</span>
                                <el-input  type='textarea'  v-model="scope.row.explain" v-else ></el-input> 
                            </template>
                        </el-table-column>
                        <el-table-column prop="func_list" label="关联式样书" min-width="240">
                            <template slot-scope="scope">
                                <span v-if="scope.row.func_list.length !== 0">
                                    <li v-for="(item,index) in scope.row.func_list" :key="index" >
                                        <a :href="item.html_url" target="_blank" rel="noopener noreferrer">{{item.spec_file_name}}&nbsp;{{item.func_name}}&nbsp;{{item.func_id}}</a>
                                        <i class="el-icon-delete margin-left" title="删除" @click="del_fun_list_item(scope.row.func_list,index)"></i>
                                    </li>
                                </span>
                                    
                                <el-button type="text"   @click="add_fun_list(scope.row)" style="font-size:12px">
                                    <i class="el-icon-circle-plus"></i>关联式样书</el-button>
                            </template>
                        </el-table-column>
                        <el-table-column label="操作" width='120'>
                            <template slot-scope="scope">
                                <el-button type="text" @click="del_usecase(scope.row,scope.$index)">[ 删除 ]</el-button>
                                <el-button type="text" @click="add_usecase(scope.row,scope.$index)">[添加]</el-button>
                            </template>
                        </el-table-column>
                                    
                    </el-table>
                     
            </div>
             <!-- 添加关联式样书模块 -->
            <el-dialog title="关联式样书" :visible.sync="dialog_flag" :modal="false">
                <el-button type="text" class="bar-add" @click="add_new_fun"><i class="el-icon-circle-plus " title="添加下一本式样书"></i></el-button>
                <el-form :model="dialog_form_obj">
                    <div v-for="(item,index) in dialog_form" :key="index" class="form-border">
                        <el-form-item :label="'式样书('+ (index+1) + ')'" label-width="120px">
                        <el-select v-model="item.spec_file_name" placeholder="请选择式样书" @change='change_fun_list_value(item.spec_file_name,item)' 
                        filterable default-first-option style="width:100%">
                            <el-option
                                v-for="item in func_list"
                                :key="item.ver_id"
                                :label="item.spec_file_name"
                                :value="item.ver_id">
                            </el-option>
                        </el-select>
                        </el-form-item>
                        <el-form-item :label="'章节号'+(index+1) " label-width="120px">
                            <el-input v-model="item.func_name" ></el-input>
                        </el-form-item>
                        <el-form-item :label="'机能ID'+(index+1) " label-width="120px">
                            <el-input v-model="item.func_id" ></el-input>
                        </el-form-item>
                    </div>
                    
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="dialog_save">确 定</el-button>

                    <el-button @click="dialog_flag = false">取 消</el-button>
                </div>
            </el-dialog>

        
    </div>
</template>
<script>
export default {
    props:["sec_id"],
    data(){
        return{
            secId:this.sec_id,
            tableData: [],
            dialog_flag:false,
            dialog_form_obj:{},
            dialog_form:[
                {
                    'gid': 0,
                    'ver_id': '',
                    'func_name': '',
                    'func_id':'',
                    'html_url':'',
                    'spec_file_name': '',
                },
            ],
            func_list:[],
            show_table_flag:false
        }
    },
    mounted() {
    },
    methods: {
        default_mounted(){
            this.$axios.get(this.Ip + "/DSUcLevel2/"+ this.sec_id).then(res=>{
                // console.log(res,'DSUcLevel2')
                if (res.data.result == 'OK') {
                    this.take_apart_data_fun(res.data.content)
                }else{
                    this.$message({
                        type:'error',
                        message:'请求数据失败'
                    })
                }
            })
        },
        take_apart_data_fun(take_data){//拆解数据结构方法
        // console.log(take_data,'take_data')
            this.tableData = []
            let push_data = {}
            let content_data =  take_data
            if (content_data.level2_list.length !== 0) {
                this.show_table_flag = false
                for (let item of content_data.level2_list) {//拆数据
                    push_data = {
                        'sec_title' : content_data.sec_title,
                        'sec_id' : content_data.sec_id,
                        'explain': item.explain,
                        'sec_title_2':item.sec_title,
                        'sec_id_2':item.sec_id,
                        'func_list':item.func_list,
                        'micro_ver_2':item.micro_ver,
                        'micro_ver':content_data.micro_ver,
                        'show_flag':true
                    }
                    this.tableData.push(push_data)
                }
                // console.log(this.tableData,'this.tableData')
            }else{
                content_data.show_flag = true
                this.show_table_flag = true
                // console.log(take_data,'take_data')
                
                this.tableData.push(content_data)

                // return
                // console.log(this.tableData,'this.tabledata')
            }
        },
        handleEdit(row, column, cell, event){
            // console.log(row, column, cell, event,'点击')
            if (column.label == "关联式样书" || column.label == "操作") {
                return
            }else{
                row.show_flag = false
            }
        },
        row_click(row){
            // console.log(row,'右点击')
            setTimeout(()=>{
                row.show_flag = true
            },100)
        },
        add_usecase(add_data,index){
            // console.log(add_data,index)
            let new_add_data = JSON.parse(JSON.stringify(add_data))//copy data
            // 清空数据
            new_add_data.func_list = []
            new_add_data.sec_id_2 = 0
            new_add_data.sec_title_2 = ''
            new_add_data.explain = ''
            new_add_data.micro_ver_2 = 0 //新增版本为0
            this.tableData.push(new_add_data)
            // console.log(this.tableData)
        },
        add_usecase_level_2(add_data){
            // console.log(add_data,'add')
            let add_level2_list_item = {
                'sec_id':0,
                'sec_title':'',
                'explain' :'',
                'micro_ver':0,
                "func_list":[]
            }
            add_data.level2_list.push(add_level2_list_item)
            // console.log(add_data,'add_data')
            // return
            this.take_apart_data_fun(add_data)
        },
        
        add_fun_list(data){
            // console.log('tianjia',data)
            this.dialog_flag = true //打开添加关联式样书框
            this.dialog_form =[ {
                'gid': 0,
                'ver_id': '',
                'func_name': '',
                'func_id':'',
                'html_url':'',
                'spec_file_name': '',
            }]//dialog表单清空
            // 请求式样书数据
            sessionStorage.setItem('table_item_data',JSON.stringify(data))//记录点击表格哪一行
            this.$axios.get(this.Ip + '/UsecaseSpec/' + sessionStorage.getItem('proj_id')).then(res=>{
                // console.log(res,'-----')
                if (res.data.result == 'OK') {
                    this.func_list = res.data.content
                }
            })
        },
        change_fun_list_value(ver_id,item){
            // console.log(ver_id,'ver_id',item)
            // console.log(this.func_list,'this.func_list')
            // console.log(this.dialog_form,'this.dialog_form')
            for (let func_list_item of this.func_list) {
                    if (func_list_item.ver_id == ver_id ) {//先判断选择的ver_id 与 func列表哪一条数据匹配
                        item.ver_id = ver_id
                        item.spec_file_name = func_list_item.spec_file_name
                        item.html_url = func_list_item.html_url

                    }
            }
        },
        dialog_save(){
            // dialog_form表单数据插入位置
            let table_item_data = JSON.parse(sessionStorage.getItem('table_item_data'))
            for (let item of this.tableData) {
                if (item.sec_id_2 == table_item_data.sec_id_2) {//判断添加记录匹配成功后fun_list插入dialog表单数据
                    item.func_list = this.dialog_form
                    break
                }
            }
            // console.log(this.dialog_form,'插入')
            // console.log(this.tableData,'this.tableData，插入后的tabledata')
            this.dialog_flag = false

        },
        lessen_data_fun(){//还原table数据结构方法
            let new_table_data = {}
            let new_level2_list_item = {}
            if (this.tableData.length >=1 && this.tableData[0].level2_list == undefined) {//还原数据结构待提交
                new_table_data.explain = null
                new_table_data.func_list = []
                new_table_data.level2_list = []
                new_table_data.commit_user = sessionStorage.getItem("Uall")
                for (let item of this.tableData) {
                    new_table_data.sec_id = item.sec_id
                    new_table_data.sec_title = item.sec_title
                    new_table_data.micro_ver = item.micro_ver
                    new_level2_list_item = {
                        explain: item.explain ,
                        func_list: item.func_list,
                        micro_ver: item.micro_ver_2,
                        sec_id: item.sec_id_2 ,
                        sec_title: item.sec_title_2,
                    }
                    new_table_data.level2_list.push(new_level2_list_item)
                }
            }else{
                new_table_data = this.tableData[0]
            }
            return new_table_data
        },
        del_usecase(del_data,del_index){
            // need to do 权限未加
            // console.log(del_data,del_index,'----------')
            let new_table_data = this.lessen_data_fun()//先调用数据还原结构方法
            // console.log(new_table_data,'new_table_data未删除前')

            new_table_data.level2_list.splice(del_index,1)//执行删除
            // console.log(new_table_data,'new_table_data')

            // return

            this.take_apart_data_fun(new_table_data)//删除完后调用数据重组方法，把数据封装是与渲染
            // console.log(this.tableData,'this.tableData')
        },
        del_fun_list_item(del_data,del_index){
            del_data.splice(del_index,1)//删除某本选中的式样书
        },
        save(){
            //提交判断：1.没有二级的时候，tableData.length === 1,否则>1
           let new_table_data = this.lessen_data_fun()//还原数据结构
            this.$axios.post(this.Ip + "/DSUcLevel2",new_table_data).then(res=>{
                // console.log(res,'保存提交')
                if (res.data.result == 'OK') {
                    this.$message({
                        type:'success',
                        message:'保存成功！',
                        showClose: true,
                        duration:5000
                    })
                }else{
                    if (res.data.result == 'NG') {
                       this.$message({
                        type:'info',
                        message:res.data.error
                    }) 
                    }
                }
            })

        },
        
        objectSpanMethod({ row, column, rowIndex, columnIndex }) {
            if (columnIndex === 0) {
                if (rowIndex % this.tableData.length === 0) {
                    return {
                        rowspan: this.tableData.length,
                        colspan: 1
                    };
                } else {
                    return {
                        rowspan: 0,
                        colspan: 0
                    };
                }
            }
        },
        add_new_fun(){
            let add_new_form = {
                    'gid': 0,
                    'ver_id': '',
                    'func_name': '',
                    'func_id':'',
                    'html_url':'',
                    'spec_file_name': '',
            }
            this.dialog_form.push(add_new_form)
            // console.log(this.dialog_form,'this.dialog_form')
        }
    },
}
</script>
<style lang="" scope>
    .wrapper {
        width: 100%;
        height: 100%;
        min-width: 1024px;
        color: #606266;
        overflow: hidden;
    }
    ul,li{
        list-style: none;
        /* float: left; */
    }
    
    .margin-left{
        /* margin-left: 20px; */
        float: right;
        cursor: pointer;
        float: right;
        padding: 5px 0 0;
    }
    .el-textarea__inner{
        padding: 5px 5px;
    }
    .el-table .cell{
        padding-left: 0px;
        padding-right: 0px;
    }
    .el-table .cell, .el-table th div, .el-table--border td:first-child .cell, .el-table--border th:first-child .cell{
        padding-left: 0px;
        padding-right: 0px;
    }
    .form-border{
        padding-top: 20px;
        border: 1px solid #ebeef5;
        background-color: #edf9f5;
        margin-bottom: 10px
    }
    .el-dialog{
        position: relative;
    }
    .el-dialog__body{
        padding: 10px 20px 20px 20px;
    }
    .bar-add{
        position: absolute;
        top: 13px;
        left: 120px;
        width: 40px;
    }
    
    
</style>