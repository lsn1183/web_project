<template>
    <div class="wrapper">
        <div class="tree-box" onselectstart="return false">
            <ul class="tree-ul">
                <li v-for="(node,index) in tree" class="tree-li">
                    <!-- 第一层标题 -->
                    <p @click="FirstScrollTop(index)" class="first-title">
                        <i class="el-icon-caret-right"></i> {{node.node_name}}
                    </p>
                    <!-- 第二层结构 -->
                    <ul class="child_ul">
                        <li class="child-tree-li" v-for="(child_node,child_index) in node.child_node">
                            <p @click="SecondScrillTop(index,child_index)" class="second-title">
                                {{child_node.child_node_name}}
                            </p>
                        </li>
                    </ul>

                </li>
            </ul>
        </div>
        <div class="content-box">
            <h1 class="title_h1">
                {{title}}
                <!-- <span class="edit-use-case" @click="edit_use_case()">[ 添加关联式样书 ]</span> -->

                <span class="back" @click="back()">[ 返回 ]</span>
            </h1>
            <div class="Asa-box Usecase-table">
                <h3 class="title-h3">
                    <span>Usecase列表</span>
                    <span class="edit-use-case" @click="edit_use_case()">[ 添加关联式样书 ]</span>
                    <!-- <span class="edit-use-case" @click="edit_use_case()">[ 编辑 ]</span> -->
                </h3>
                <el-table :data="UsecaseTable" border style="width:95%;margin-top:10px;">
                    <el-table-column prop="number" label="UseCase Name" header-align='center' width="250px">
                        <template slot-scope="scope">
                            <el-button size="mini" type="text">
                                <span> &nbsp;{{scope.row.sec_level1}}</span>
                            </el-button>
                        </template>
                    </el-table-column>
                    <el-table-column prop="number" label="SubUseCase" header-align='center' width="250px">
                        <template slot-scope="scope">
                            <el-button size="mini" type="text">
                                <span> &nbsp;{{scope.row.sec_level2}}</span>
                            </el-button>
                        </template>
                    </el-table-column>
                    <el-table-column prop="func_id" label="关联式样书" header-align='center'>
                        <template slot-scope="scope">
                            <div v-for="item in scope.row.func_list">
                                <a :href="item.html_url" target="_blank"> 
                                    {{item.spec_file_name}}{{item.func_name}}{{item.func_id}}
                                </a>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="explain" label="说明（变更点/对应内容等）" header-align='center'></el-table-column>
                </el-table>
            </div>
            <!-- Block -->
            <div class="block-box Asa-box" v-if='Block.length!=0'>
                <h3 class="title-h3">
                    <span>Block</span>
                    <!-- <span class="append-span" @click="block_fun('add','block')" v-if='Block.length==0'> &nbsp;[ 添加 ]</span> -->
                    <!-- <span class="append-span" @click="block_fun('edit','block')" v-else> &nbsp;[ 编辑 ]</span> -->
                </h3>
                <!-- Block 子元素块 -->
                <div class="msg-box" v-for="(block_item,index) in Block">
                    <h4 class="title-h4">
                        <span>Block {{index+1}}: {{block_item.sec_title}}</span>
                        <!-- <span class="append-span" @click="block_fun('add','block')" v-if='Block.length==0'> &nbsp;[ 添加 ]</span> -->
                        <!-- <span class="append-span" @click="block_fun('edit','block')"> &nbsp;[ 编辑 ]</span> -->
                    </h4>
                    <div class="content-size">
                        <span>Block说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='block_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in block_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='block_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                </div>
                <p class="message" v-if='Block.length==0'>暂无数据</p>
            </div>
            
            <!-- Class -->
            <div class="Class-box Asa-box">
                <h3 class="title-h3">
                    <span>Class</span>
                    <span class="append-span" @click="block_fun('add','class')" v-if='Class.length==0'> &nbsp;[ 添加 ]</span>
                    <span class="append-span" @click="block_fun('edit','class')" v-else> &nbsp;[ 编辑 ]</span>
                </h3>
                <!-- Class 子元素块 -->
                <div class="msg-box" v-for="(class_item,index) in Class">
                    <h4 class="title-h4">
                        <span>Class{{index+1}}: {{class_item.sec_title}}</span>
                        <span class="append-span" @click="block_fun('add','class')" v-if='Class.length==0'> &nbsp;[ 添加 ]</span>
                        <span class="append-span" @click="block_fun('edit','class')" v-else> &nbsp;[ 编辑 ]</span>
                    </h4>
                    <div class="content-size">
                        <span>Class说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='class_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in class_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='class_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                </div>
                <p class="message" v-if='Class.length==0'>暂无数据</p>
            </div>
            
            <!-- Usecase -->
            <div class="Usecase-box Asa-box" v-if='Usecase.length!=0'>
                <h3 class="title-h3">
                    <span>Usecase</span>
                    <!-- <span class="append-span" v-if='Usecase.length==0' @click='append_usecase("add")'> &nbsp;[ 添加 ]</span> -->
                    <!-- <span class="append-span" v-else @click='append_usecase("edit")'> &nbsp;[ 编辑 ]</span> -->
                </h3>
                <!-- Usecase 子元素块 -->
                <div class="msg-box" v-for="(usecase_item,index) in Usecase">
                    <h4 class="title-h4">
                        <span>Usecase{{index+1}}: {{usecase_item.sec_title}}</span>
                        <!-- <span class="append-span" v-if='Usecase.length==0' @click='append_usecase("add")'> &nbsp;[ 添加 ]</span> -->
                        <!-- <span class="append-span" v-else @click='append_usecase("edit")'> &nbsp;[ 编辑 ]</span> -->
                    </h4>
                    <div class="content-size">
                        <span>Usecase说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='usecase_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in usecase_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='usecase_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                </div>
                <p class="message" v-if='Usecase.length==0'>暂无数据</p>
            </div>
            
            <!-- Statemachine -->
            <div class="Std-box Asa-box" v-if='Statemachine.length!=0'>
                <h3 class="title-h3">
                    <span>Statemachine</span>
                    <!-- <span class="append-span" @click="block_fun('add','statemachine')" v-if='Statemachine.length==0'> &nbsp;[ 添加 ]</span> -->
                    <!-- <span class="append-span" @click="block_fun('edit','statemachine')" v-else> &nbsp;[ 编辑 ]</span> -->
                </h3>
                <!-- Statemachine 子元素块 -->
                <div class="msg-box" v-for="(statemachine_item,index) in Statemachine">
                    <h4 class="title-h4">
                        <span>Statemachine{{index+1}}: {{statemachine_item.sec_title}}</span>
                        <!-- <span class="append-span" @click="block_fun('edit','statemachine')"> &nbsp;[ 编辑 ]</span> -->
                    </h4>
                    <div class="content-size">
                        <span>Statemachine说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='statemachine_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in statemachine_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='statemachine_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                </div>
                <p class="message" v-if='Statemachine.length==0'>暂无数据</p>
            </div>
            <!-- Sequence -->
            <div class="Sequence-box Asa-box">
                <h3 class="title-h3">
                    <span>Sequence</span>
                    <span class="append-span" v-if='seq_list.length==0' @click='append_seq()'> &nbsp;[ 添加 ]</span>
                    <span class="append-span" v-else @click='append_seq()'> &nbsp;[ 编辑 ]</span>
                </h3>
                <!-- Sequence 子元素块 -->
                <div class="msg-box" v-for="(seq_item,index) in seq_list">
                    <h4 class="title-h4">
                        <span>Sequence{{index+1}}: {{seq_item.sec_title}}</span>
                       <span class="append-span" @click='append_seq()'> &nbsp;[ 编辑 ]</span>
                    </h4>
                    <div class="content-size">
                        <span>Sequence说明 : </span>
                        <div id="editor">
                          <mavon-editor :value='seq_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in seq_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                          <mavon-editor :value='seq_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <!-- Activity -->
                    <div class="Sequence-box" v-if="type == 'DETAIL'">
                        <h3 class="title-h3">
                            <span>Activity</span>
                            <span class="append-span" v-if='seq_item.Activity.length==0' @click='append_seq()'> &nbsp;[ 添加 ]</span>
                            <span class="append-span" v-else @click='append_seq()'> &nbsp;[ 编辑 ]</span>
                        </h3>
                        <div class="msg-box" v-for="(activity_item,index) in seq_item.Activity">
                            <h4 class="title-h4">
                                <span>Activity{{index+1}}: {{activity_item.sec_title}}</span>
                               <span class="append-span" @click='append_seq()'> &nbsp;[ 编辑 ]</span>
                            </h4>
                            <div class="content-size">
                                <span>Activity说明 : </span>
                                <div id="editor">
                                  <mavon-editor :value='activity_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                                </div>
                            </div>
                            <div class="img-box" v-for="src in activity_item.img_list">
                                <img :src="src.url" alt="" class="img-width">
                            </div>
                            <div class="content-size">
                                <span>补足说明 : </span>
                                <div id="editor">
                                  <mavon-editor :value='activity_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                                </div>
                            </div>
                        </div>       
                    </div>
                    <!-- Resource -->
                    <div class="Usecase-table">
                        <h4 class="title-h4">
                            <span>Resource</span>
                        </h4>
                        <el-table :data="seq_item.Resource" border style="width:95%">
                            <el-table-column prop="rsc_name" label="资源类型" header-align='center'></el-table-column>
                            <el-table-column prop="val" label="确认内容" header-align='center' min-width='500'>
                                <template slot-scope="scope">
                                        <span> &nbsp;{{scope.row.operator}}{{scope.row.value}}{{scope.row.unit}}</span>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
                <p class="message" v-if='seq_list.length==0'>暂无数据</p>
            </div>

            <!-- OTHER -->
            <div class="Other-box Asa-box">
                <h3 class="title-h3">
                    <span>OTHER</span>
                    <span class="append-span" @click="other_fun('add','OTHER')" v-if='Other.length==0'> &nbsp;[ 添加 ]</span>
                    <span class="append-span" @click="other_fun('edit','OTHER')" v-else> &nbsp;[ 编辑 ]</span>
                </h3>
                <!-- Other 子元素块 -->
                <div class="msg-box" v-for="(Other_item,index) in Other">
                    <h4 class="title-h4">
                        <span>OTHER{{index+1}}: {{Other_item.sec_title}}</span>
                        <span class="append-span" @click="other_fun('add','OTHER')" v-if='Other.length==0'> &nbsp;[ 添加 ]</span>
                        <span class="append-span" @click="other_fun('edit','OTHER')" v-else> &nbsp;[ 编辑 ]</span>
                    </h4>
                    <div class="content-size">
                        <span>OTHER说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='Other_item.explain' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                    <div class="img-box" v-for="src in Other_item.img_list">
                        <img :src="src.url" alt="" class="img-width">
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div id="editor">
                            <mavon-editor :value='Other_item.complement' :editable='false' :subfield='false' defaultOpen='preview' :toolbarsFlag='false' :scrollStyle='true'></mavon-editor>
                        </div>
                    </div>
                </div>
                <p class="message" v-if='Other.length==0'>暂无数据</p>
            </div>

            <!-- DRBFM  -->
            <div class="DRBFM-box Asa-box">
                <h3 class="title-h3">
                    <span>DRBFM</span>
                    <span class="append-span" v-if='DRBFM.length==0' > &nbsp;[ 添加 ]</span>
                    <span class="append-span" v-else> &nbsp;[ 编辑 ]</span>
                </h3>
                <div class="msg-box"></div>
                <p class="message" v-if='DRBFM.length==0'>暂无数据</p>
            </div>
            <!-- 关联usecase式样书组件 -->
            <div class="DRBFM-box Asa-box case-scroll" >
                <!-- <UseCaseComponent :sec_id.sync="sec_id"></UseCaseComponent> -->
            </div>
            <!-- dialog -->
            <el-dialog title="UseCase关联式样书" :visible.sync="dialogVisible" width="80%">
                <UseCaseComponent :sec_id.sync="sec_id" ref="children"></UseCaseComponent>            
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="dialog_save()">确 定</el-button>
                <el-button @click="dialogVisible = false">取 消</el-button>
            </span>
            </el-dialog>
        </div>
    </div>
</template>
<script>
require('../../assets/js/jquery-1.8.3.min.js')
import use_case_component from './UseCase_Input.vue'
document.oncontextmenu = function(){
    return false;
}
document.onselectstart = function(){
    return false;
}
document.oncopy = function(){
    return false;
}
export default {
    components:{
        "UseCaseComponent":use_case_component//usecase关联式样书组件
    },
    data () {
        return {
           arr:[],
           tree:[
           ],
           title:"",
           seq_list:[],
           DRBFM:[],
           sec_id:'', 
           usecase_id:'',
           type:'',
           doc_id:'',
           Block: [],
           Class: [],
           Usecase: [],
           Statemachine: [],
           Other:[],
           dialogVisible: false,
           UsecaseTable:[]
        }
    },
    created () {
        this.sec_id = this.$route.params.secid 
    },
    mounted () {
        this.get_seq_data()
    },
    watch: {
        
    },
    methods: {
        edit_use_case(){
            this.dialogVisible = true
            let that = this
            setTimeout(()=>{
                that.$refs.children.default_mounted();           
            },100)
            // this.$router.push({ path: '/tagl/File_design/Add_usecasetable/' + this.sec_id })
        },
        clear_data(){
            this.Block = []
            this.Class = []
            this.Usecase = []
            this.Other = []
            this.UsecaseTable = []
            this.DRBFM = []
            this.seq_list = []
            this.tree = []
            this.usecase_id = ""
            this.title = ""
            this.doc_id = ""
            this.type = ""
        },
        dialog_save(){
            this.$refs.children.save();//调用子组件保存方法
            this.dialogVisible = false
            this.get_seq_data()
        },
        get_seq_data(){
            this.clear_data()
            this.$axios.get(this.Ip + '/UsecaseDetail/'+ this.sec_id).then(res => {
                if(res.data.result == 'OK'){
                    this.type = res.data.content.doc_type
                    this.doc_id = res.data.content.doc_id
                    this.title = res.data.content.title
                    this.DRBFM = res.data.content.DRBFM
                    this.usecase_id = res.data.content.usecase_id
                    this.UsecaseTable = res.data.content.UsecaseTable
                    this.tree.push({"node_name": 'Usecase列表', 'child_node': [] })
                    this.judge_data(res.data.content)
                    this.get_Class(res.data.content.Class)
                    this.get_seq(res.data.content.Sequence)
                    this.get_Statemachine(res.data.content.Statemachine)
                    this.get_Other(res.data.content.Other)
                    
                }
            })
        },
        judge_data(data){
            if(data.Block.length != 0){
                this.tree.push({"node_name": 'Block', 'child_node': [] })
                this.get_Block(data.Block)
            }
            this.tree.push({"node_name": 'Class', 'child_node': [] })
            if(data.Usecase.length != 0){
                this.tree.push({"node_name": 'Usecase', 'child_node': [] })
                this.get_Usecase(data.Usecase)
            }
            this.tree.push({"node_name": 'Sequence', 'child_node': [] })
            if(data.Statemachine.length != 0){
                this.tree.push({"node_name": 'Statemachine', 'child_node': [] })
                this.get_Statemachine(data.Statemachine)
            }
            this.tree.push({"node_name": 'OTHER', 'child_node': [] })
            this.tree.push({"node_name": 'DRBFM', 'child_node': [] })

        },
        push_data_seq(data_json,self,name,index){
            if(data_json.length == 0){
                return
            }
            for(let item=0; item<data_json.length; item++){
                let img_json = JSON.parse(data_json[item].content)
                let Activity = []
                for(let activ_i = 0;activ_i < data_json[item].Activity.length; activ_i++){
                    let activ_json = JSON.parse(data_json[item].Activity[activ_i].content)
                    Activity.push({
                        "complement":data_json[item].Activity[activ_i].complement,
                        "img_list":activ_json,
                        "explain":data_json[item].Activity[activ_i].explain,
                        "sec_title":data_json[item].Activity[activ_i].sec_title
                    })
                }
                for(let i = 0; i < this.tree.length; i++){
                    if(this.tree[i].node_name == name){
                        this.tree[i].child_node.push({"child_node_name": name + (item+1) + ":" +data_json[item].sec_title})
                    }
                }
                self.push({
                    "Resource": data_json[item].Resource,
                    "complement": data_json[item].complement,
                    "img_list": img_json,
                    "explain": data_json[item].explain,
                    "sec_title": data_json[item].sec_title,
                    "Activity":Activity
                })
            }
        },
        get_seq(data_json){
            this.push_data_seq(data_json,this.seq_list,"Sequence")
        },
        get_Block(data_json) {
            this.push_data(data_json, this.Block, 'Block')
        },
        get_Class(data_json) {
            this.push_data(data_json, this.Class, 'Class')
        },
        get_Usecase(data_json) {
            this.push_data(data_json, this.Usecase, 'Usecase')
        },
        get_Statemachine(data_json) {
            this.push_data(data_json, this.Statemachine, 'Statemachine')
        },
        get_Other(data_json){
            this.push_data(data_json, this.Other, 'OTHER')
        },
        push_data(data_json, self, name) {
            if (data_json.length == 0) {
                return
            }
            for (let item = 0; item < data_json.length; item++) {
                let img_json = JSON.parse(data_json[item].content)
                for(let i = 0; i<this.tree.length;i++){
                    if(this.tree[i].node_name == name){
                        this.tree[i].child_node.push({
                            child_node_name: name + (item + 1) + ':' + data_json[item].sec_title
                        })
                    }
                }
                self.push({
                    complement: data_json[item].complement,
                    img_list: img_json,
                    explain: data_json[item].explain,
                    sec_title: data_json[item].sec_title
                })
            }
        },
        back(){
            let type = ""
            if(this.type == 'DETAIL'){
                type = 'detail_design'
                this.$router.push({path:'/tagl/File_design/Preview/'+ this.doc_id + '/' + type})
            }else if(this.type == 'BASIC'){
                type = 'basic_design'
                this.$router.push({path:'/tagl/File_design/Preview/'+ this.doc_id + '/' + type})
            }else if(this.type == 'IF'){
                type = 'IF_stylebook'
                this.$router.push({path:'/tagl/edit_IF/'+ this.doc_id + '/' + type})
            }
            // this.$router.go(-1)
        },
        append_seq(){
            this.$router.push({path: '/tagl/basic_design_sequence_edit/' + this.usecase_id + '/' + this.title})
        },
        FirstScrollTop(index){
            $('.first-title').css({ color: '#606266' })
            $('.second-title').css({ color: '#606266' })
            $('.first-title').eq(index).css({ color: '#42b983' })
            let sTop = document.getElementsByClassName('Asa-box')[index].offsetTop
            $('.content-box').animate({ scrollTop: sTop }, 500, function() {})
        },
        SecondScrillTop(index,second){
            $('.first-title').css({ color: '#606266' })
            $('.second-title').css({ color: '#606266' })
            $('.tree-li').eq(index).find(".second-title").eq(second).css({ color: '#42b983' })
            let sTop = $('.Asa-box').eq(index).find('.msg-box').eq(second)[0].offsetTop
            $('.content-box').animate({ scrollTop: sTop }, 500, function() {})
        },
        block_fun(type, click_type) {
            let value = {
                path: '/tagl/step_Block',
                query: {
                    data: JSON.stringify({
                        type: type,
                        sec_id: this.sec_id,
                        title: this.title,
                        click_type: click_type,
                        doc_type: this.type,
                        proj_id: sessionStorage.getItem('proj_id'),
                        model_id:this.model_id
                    })
                }
            }
            let datas = {
                "proj_id": sessionStorage.getItem('proj_id'),
                "model_id": this.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            if (type == 'add') {
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                            // to do
                            this.$router.push(value)
                        } else {
                                this.$message({
                                    type: "warning",
                                    message: "您没有权限操作"
                                })
                            }
                    } else {
                        // nothing to do
                        this.$message({
                            type: "warning",
                            message: res.data.error
                        })
                    }
                })
            } else {
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_编辑') == true) {
                            // to do
                            this.$router.push(value)
                        } else {
                                this.$message({
                                    type: "warning",
                                    message: "您没有权限操作"
                                })
                            }
                    } else {
                        // nothing to do
                        this.$message({
                            type: "warning",
                            message: res.data.error
                        })
                    }
                })
            }
        },
        other_fun(type, click_type) {
            let value = {
                path: '/tagl/step_other',
                query: {
                    data: JSON.stringify({
                        type: type,
                        sec_id: this.sec_id,
                        title: this.title,
                        click_type: click_type,
                        doc_type: this.type,
                        proj_id: sessionStorage.getItem('proj_id'),
                        model_id:this.model_id
                    })
                }
            }
            let datas = {
                "proj_id": sessionStorage.getItem('proj_id'),
                "model_id": this.model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            if (type == 'add') {
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_添加') == true) {
                            // to do
                            this.$router.push(value)
                        } else {
                                this.$message({
                                    type: "warning",
                                    message: "您没有权限操作"
                                })
                            }
                    } else {
                        // nothing to do
                        this.$message({
                            type: "warning",
                            message: res.data.error
                        })
                    }
                })
            } else {
                this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                    if (res.data.result == "OK") {
                        var userPermissionData = res.data.content
                        if (this.getCatusPurviewManage(userPermissionData, '设计书_编辑') == true) {
                            // to do
                            this.$router.push(value)
                        } else {
                                this.$message({
                                    type: "warning",
                                    message: "您没有权限操作"
                                })
                            }
                    } else {
                        // nothing to do
                        this.$message({
                            type: "warning",
                            message: res.data.error
                        })
                    }
                })
            }
        },
    }
}
</script>

<style scoped>
html,body {
    font-family: "微软雅黑";
}
.wrapper {
    width: 100%;
    height: 100%;
    min-width: 1024px;
    color: #606266;
    overflow: hidden;
}
.tree-box {
    position: relative;
    top: 0;
    left: 0;
    z-index: 9;
    margin: 0;
    padding: 0;
    width: 15%;
    height: 98%;
    background-color: white;
    border-right: 2px solid rgba(216, 231, 223, 0.5);
    overflow: scroll;
    overflow-x: hidden;
}
.content-box {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 85%;
    overflow-y: auto;
    padding-left: 20px;
}
.title_h1{
    font-weight:bold;
    font-size: 24px;
    margin-top: 10px;
    width: 95%;
}
.title-detail {
    font-size: 12px;
    color: #5e6d82;
    text-align: left;
    height: 20px;
    line-height: 20px;
    margin-top: 10px;
}
.block-box,.Class-box,.Usecase-table,.Usecase-box,.Std-box,.Sequence-box,.Other-box,.DRBFM-box,.Usecase-table{
    margin-top: 10px;
}
.Std-box,.DRBFM-box{
    margin-bottom: 40px;
}
.title-h3 {
    font-size: 20px;
    font-weight: 500;
    height: 25px;
    line-height: 25px;
    font-weight: bold;
}
.title-h4 {
    font-size: 18px;
    padding-top: 10px;
    /*font-weight: 500*/
}
.append-span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}

.content-size {
    margin-top: 10px;
}

#editor{
  width: 95%;
  margin-top: 10px;
}
.v-note-wrapper{
    min-height: 100px;
}
.msg-box,.img-box{
    margin-top: 10px;
}
.img-box{
    overflow: auto;
}
.message {
    width: 95%;
    background-color: #edf9f5;
    text-align: center;
    padding: 20px;
    font-size: 14px;
    color: #909399;
    border: 1px solid #ebeef5;
    margin-top: 10px;
}
.back{
    float: right;
    font-size: 16px;
    cursor: pointer;
    margin-top: 10px;
    font-weight: 500
}
.edit-use-case{
    /* float: left; */
    font-size: 16px;
    cursor: pointer;
    margin-top: 10px;
    font-weight: 500;
    
}
/*树*/
ul,li{
    list-style: none;
}
.tree-ul{
    overflow: hidden;
    width: 100%;
    padding-left: 20px;
}
.child_ul{
    overflow: hidden;
    padding-left: 10px;
}
.tree-li{
    margin-top: 10px;
    font-weight: bold;
    cursor: pointer;
}
.tree-li p {
    /*height: 24px;*/
    line-height: 24px;
}
.child-tree-li{
    margin-top: 5px;
    margin-left: 20px;
    font-weight: 500;
    font-size: 14px;
}
@media screen and (max-width: 1024px) {
    .wrapper {
        width: 1024px;
    }
    .tree-box {
        width: 20%;
    }
    .content-box {
        width: 80%;
    }
}
</style>

