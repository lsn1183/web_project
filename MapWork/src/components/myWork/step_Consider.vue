<template>
    <div id="consider">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="场景(必填)">1</el-step>
                    <el-step class="jump" title="修改点影响点(必填)">2</el-step>
                    <el-step class="jump" title="考虑点(必填)" icon="el-icon-edit" status="process">3</el-step>
                    <el-step class="jump" title="DRBFM(必填)">4</el-step>
                </el-steps>
            </div>
        </div>
        <div class="cbody">
            <div class="mid">
                <div class="mid-top">
                    <div class="scene-title">
                        <h2 style="fontSize: 22px;fontWeight:bolder;backgroundColor:#6bcca0; color: white;lineHeight: 25px;height:25px">
                            <span style="lineHeight:25px;float:left;paddingLeft: 10px;">考虑点</span>
                            <i class="el-icon-question" style="fontSize:15px; lineHeight:25px;float:left;marginLeft:5px" title="请选择Usecase使用的场景，比如Usecase A关联了timer的使用，则Usecase A场景选择时必须包含timer；不同场景的选择会关联不同的设计确认点，请认真选择"></i>
                        </h2>
                    </div>

                    <div style="height: auto;">
                        <div class="checkBox">
                            <div class="big-box">

                                <el-carousel v-loading="loading" :autoplay="autoplay" indicator-position="outside" height="580px" class="show-type">
                                    <!-- :label="item[0].work_status? 'O' : 'X'" -->
                                    <el-carousel-item v-for="(item,index) in step2.consider" :key="item[0].tag_id" :label="item[0].tag">
                                        <div class="checked-input-list">
                                            <table>
                                                <thead>
                                                    <tr>
                                                        <th rowspan="2">编号</th>
                                                        <th colspan="2">修改点/影响点</th>
                                                        <th rowspan="2">选择关联模块</th>
                                                        <th rowspan="2">已选关联模块</th>
                                                        <th rowspan="2">确认结果</th>
                                                    </tr>
                                                    <tr>
                                                        <th>修改前</th>
                                                        <th>修改后</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <template v-for="(items, indexs) in item[0].change_list">
                                                        <tr :class="indexs%2 == 1 ? 'gray_col': ''">
                                                            <td :rowspan="items.model_list.length">{{indexs + 1}}</td>
                                                            <td :rowspan="items.model_list.length" :title="items.before_change">{{items.before_change}}</td>
                                                            <td :rowspan="items.model_list.length" :title="items.change">{{items.change}}</td>
                                                            <td :rowspan="items.model_list.length">
                                                                <!-- <el-select v-model="items.model_name_list" multiple @remove-tag="remove(index)" @change="look(index)" value-key="model_name" placeholder="请选择模块">
                                                                    <el-option v-for="items in options" :key="items.model_id" :label="items.model_name" :value="items">
                                                                    </el-option>
                                                                </el-select> -->
                                                                <span class='caret' @click='cg_show(index,indexs)'>请选择<i class="el-icon-caret-bottom"></i></span>
                                                                <div class="cg-box">
                                                                    <el-checkbox-group v-model="items.model_name_list">

                                                                        <el-checkbox v-for="(item_options, item_options_index) in options" :label="item_options.model_name" :key="item_options_index" @change="checked => handle_click_checkbox(checked, item_options, items.model_list, items, indexs, item, index)">{{item_options.model_name}}
                                                                        </el-checkbox>

                                                                    </el-checkbox-group>
                                                                </div>
                                                            </td>
                                                            <td >
                                                                <span style="cursor: pointer;"@click="open_inner_dialog2(index,indexs,items.model_list[0].failure_id_list,item,items.model_list[0])">{{items.model_list[0].model_name}}</span>
                                                            </td>
                                                            <td>
                                                                <span v-if="items.model_list[0].checked"@click="open_inner_dialog2(index,indexs,items.model_list[0].failure_id_list,item,items.model_list[0])">{{items.model_list[0].result}}</span>
                                                                <span v-else style="color: red"@click="open_inner_dialog2(index,indexs,items.model_list[0].failure_id_list,item,items.model_list[0])">{{items.model_list[0].result}}</span>
                                                            </td> 
                                                        </tr>
                                                        <tr :class="index%2 == 1 ? 'gray_col': ''" v-for="son_item in items.model_list.length - 1">
                                                            <td :title="items.model_list[son_item].model_name" >
                                                                <span style="cursor: pointer;"@click="open_inner_dialog2(index,indexs,items.model_list[son_item].failure_id_list,item,items.model_list[son_item])">{{items.model_list[son_item].model_name}}</span>
                                                            </td>
                                                            <td :title="items.model_list[son_item].completion">
                                                                <span v-if="items.model_list[son_item].checked"@click="open_inner_dialog2(index,indexs,items.model_list[son_item].failure_id_list,item,items.model_list[son_item])">{{items.model_list[son_item].result}}</span>
                                                                <span v-else style="color: red"@click="open_inner_dialog2(index,indexs,items.model_list[son_item].failure_id_list,item,items.model_list[son_item])">{{items.model_list[son_item].result}}</span>
                                                            </td>
                                                        </tr>
                                                    </template>
                                                </tbody>
                                            </table>
                                        </div>
                                    </el-carousel-item>
                                </el-carousel>

                            </div>
                            <div>
                                <el-dialog title="Failure mode" :visible.sync="innerVisible" :before-close="inner_dialog_before_close">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Failure mode</th>
                                                <th>文档编号</th>
                                                <th>文档标题</th>
                                                <th>是否确认</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <template v-for="(item, index) in FailureMode">
                                                <tr v-for="son_item in item.doc_list.length">
                                                    <td :rowspan="item.doc_list.length" :title="item.failure_mode" v-if="son_item === 1">{{item.failure_mode}}</td>
                                                    <td>{{item.doc_list[son_item-1].doc_id}}</td>
                                                    <td class="doc-text" @click="go_doc_text(item.doc_list[son_item-1])">{{item.doc_list[son_item-1].doc_title}}</td>
                                                    <td>
                                                        <el-select v-model="item.doc_list[son_item-1].value" placeholder="请确认">
                                                            <el-option v-for="items in op" :key="items.value" :label="items.label" :value="items.value">
                                                            </el-option>
                                                        </el-select>
                                                    </td>
                                                </tr>
                                            </template>
                                        </tbody>
                                    </table>
                                    <div slot="footer" class="dialog-footer">
                                        <el-button @click="inner_dialog_cancle">取 消</el-button>
                                        <el-button @click="inner_dialog_close" type="primary">确 定</el-button>
                                    </div>
                                </el-dialog>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="prev()">
                        <i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button size="mini" type="primary" @click="save()">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="next()">下一步
                        <i class="el-icon-arrow-right"></i>
                    </el-button>
                </div>
            </div>
            <div class="right">

            </div>

        </div>

    </div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
$(document).click(function(){
  $(".cg-box").slideUp(300);
});
export default {
    data() {
        return {
            active: Number(window.sessionStorage.getItem('Step')),
            scene: [],
            step2: {
                doc_id: 0,
                micro_ver: Number(window.sessionStorage.getItem('ver')),
                commit_user: window.sessionStorage.getItem('Uall'),
                consider: []
            },

            loading: true,
            choosesence: [],
            sceneslist: [],
            get_data: '',
            save_data: '',
            dbrfmFlag: false,

            autoplay: false,
            op: [
                {
                    value: '1',
                    label: 'O'
                },
                {
                    value: '0',
                    label: 'X'
                }
            ],
            tag_id: 0,
            tag: '',
            first_index: 0,
            last_index: 0,
            title_value: [],
            outerVisible: false,
            innerVisible: false,
            options: [],
            options2: [],
            FailureMode: [],
            model_op:{},
            model_check_flag:false,
            model_name_temp:""

        }
    },
    mounted() {
        this.getConsider()
        this.getModelRef()
        var self = this
        setTimeout(() => {
            $('.jump').on('click', function(e) {
                self.jump_to($(this).text())
            })
        }, 10)
        if (this.$route.query.params) {
            this.dbrfmFlag = this.$route.query.params
        }
    },
    methods: {
        handle_click_checkbox(checked, model, model_list, items, indexs, item, index) {
            if (checked) {
                // console.log(items, indexs, item, index,"本层，本层序列，外层，外层映射")
                // 勾选时，弹出dialog，在dialog内部进行选择
                this.tag_id = item[0].tag_id
                this.first_index = index
                this.last_index = indexs
                this.model_check_flag = true
                this.model_name_temp = model.model_name
                const model_copy = {
                    checked: model.checked,
                    model_id:model.model_id,
                    model_name:model.model_name,
                    failure_id_list:model.failure_id_list,
                    result : "",
                }
                this.model_op = model_copy
                // console.log(model_copy,"mc")
                // console.log(this.model_op,"mo")
                this.open_inner_dialog()
                // 在dialog中点击确定之后 执行
            } else {
                // 取消勾选时，删除当前关联模块
                // model_list = model_list.filter(item => {
                //     item.model_name != model_name
                // })
                for (let i = 0; i < model_list.length; i++) {
                    if (model.model_name == model_list[i].model_name) {
                        model_list.splice(i, 1)
                        if (model_list.length === 0) {
                            // 因为表格根据数据动态刷新，如何model_list为[],表格行数会对不齐出现混乱
                            let module_item = {
                                model_id: 0,
                                model_name: '',
                                checked: false,
                                failure_id_list: [],
                                result: ''
                            }
                            model_list.push(module_item) // 所以添加一个假数据对象，这个假数据对象要在在新增关联模块时删除
                        }
                        break
                    }
                }
                this.look(this.first_index)
            }
        },
        del_opt(index, son_index) {
            this.step2.content[index].changes.splice(son_index, 1)
        },
        add_opt(index, son_index) {
            let row = {
                gid: 0,
                before_change: '',
                changes: '',
                address: '',
                zip: ''
            }
            this.step2.content[index].changes.splice(son_index + 1, 0, row)
        },

        getModelRef() {
            this.$axios
                .get(this.Ip + '/ModelRefGet/' + Number(window.sessionStorage.getItem('DocId')))
                .then(res => {
                    if (res.data.result == 'OK') {
                        // console.log(res, 'md')
                        var da = JSON.stringify(res.data.content)
                        this.options = JSON.parse(da)
                        this.options2 = JSON.parse(da)
                    }
                })
                .catch(res => {
                    // console.log(res,"md")
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error'
                    })
                })
        },
        change_open_dialog(value) {
            if (!value) {
                this.outerVisible = true
            } else {
            }
        },
        go_doc_text(val) {
            // console.log(val)
            let data = {
                data: val,
                server_ip: this.Ip
            }
            window.sessionStorage.setItem('listDocID', JSON.stringify(data))
            window.open('../../../static/DocList-item.html')
        },
        look(index) {
            var op = JSON.stringify(this.options2)
            this.options = JSON.parse(op)
            var flag = true
            var cflag = true
            for (var change of this.step2.consider[index]) {
                var fenmu = change.change_list.length
                var xiaofenmu = 1

                var num = 0
                for (var mm of change.change_list) {
                    for (var md of mm.model_list) {
                        if (md.model_id == 0) {
                            cflag = false
                        } else{
                            xiaofenmu = mm.model_list.length
                            var xiaofenzi = 0
                            if (md.checked == true) {
                                xiaofenzi = xiaofenzi + 1
                            } else {
                                flag = false 
                            }
                            num += xiaofenzi / xiaofenmu / fenmu
                            // console.log(num,xiaofenzi,xiaofenmu,"num")
                        }
                       
                    }
                }
                if (flag && cflag) {
                    change.work_status = true
                } else {
                    change.work_status = false
                }
                change.completion = parseInt(num * 100) + '%'
                // console.log(change.completion,"color")
            }
            this.change_el_carousel_style()
        },
        change_el_carousel_style() {
            const that = this
            this.$nextTick(() => {
                $('.el-carousel__indicators--labels .el-carousel__indicator button').each(function(index, element) {
                    $(this).css('fontWeight', 'bold')
                    $(this).css(
                        'background',
                        'linear-gradient(to right,#42b983 0%,#42b983 ' +
                            that.step2.consider[index][0].completion +
                            ',#c0c4cc 0,#c0c4cc 100%)'
                    )
                })
            })
        },

        open_inner_dialog() {
            this.FailureMode = []
            // var ck = checkedlist
            this.$axios.get(this.Ip + '/FailureModeByTag/' + this.tag_id).then(res => {
                console.log(res, 'fm')
                this.FailureMode = res.data.content
            })
            this.innerVisible = true
        },
        open_inner_dialog2(index,indexs,checkedlist,item,options) {
            this.model_check_flag = false
            this.tag_id = item[0].tag_id
            this.first_index = index
            this.last_index = indexs
            const model_copy = {
                    checked: options.checked,
                    model_id:options.model_id,
                    model_name:options.model_name,
                    failure_id_list:options.failure_id_list,
                    result : options.result,
                }
            this.model_op = model_copy
            // console.log(this.first_index,this.last_index, 'inde')
            // console.log(checkedlist, 'in_checklist')
            this.FailureMode = []
            this.$axios.get(this.Ip + '/FailureModeByTag/' + this.tag_id).then(res => {
                // console.log(res, 'fm')
                this.FailureMode = res.data.content
                for (var i = 0; i < this.FailureMode.length; i++) {
                    for (var j = 0; j < this.FailureMode[i].doc_list.length; j++) {
                        if (checkedlist.havething_list.length > 0) {
                            for (var k = 0; k < checkedlist.havething_list.length; k++) {
                                if (checkedlist.havething_list[k] == res.data.content[i].doc_list[j].doc_id) {
                                    this.FailureMode[i].doc_list[j].value = '1'
                                }
                            }
                        }
                        if (checkedlist.nothing_list.length > 0) {
                            for (var k = 0; k < checkedlist.nothing_list.length; k++) {
                                if (checkedlist.nothing_list[k] == res.data.content[i].doc_list[j].doc_id) {
                                    this.FailureMode[i].doc_list[j].value = '0'
                                }
                            }
                        }
                    }
                }
            })
            // console.log(this.matrix_data2,"2")
            this.innerVisible = true
        },
        inner_dialog_close() {
            var doc_lis = {
                havething_list:[],
                nothing_list:[],
            }
            var fenmu = 0
            var fenzi = 0
            for (var i = 0; i < this.FailureMode.length; i++) {
                for (var j = 0; j < this.FailureMode[i].doc_list.length; j++) {
                    fenmu+=1
                    if (this.FailureMode[i].doc_list[j].value == '1') {
                        fenzi+=1
                        doc_lis.havething_list.push(this.FailureMode[i].doc_list[j].doc_id)
                    }
                    if (this.FailureMode[i].doc_list[j].value == '0') {
                        fenzi+=1
                        doc_lis.nothing_list.push(this.FailureMode[i].doc_list[j].doc_id)
                    }
                }
            }
            // console.log(this.FailureMode,"0!0")
            this.model_op.result = fenzi + '/' + fenmu
            this.model_op.failure_id_list = doc_lis
            // var number = fenzi/fenmu
            // console.log(fenzi,fenmu,"0.0")
            if(fenzi==fenmu){
                this.model_op.checked = true
            }
            // console.log(this.model_op,"1")
            if (this.model_check_flag){
                // 在dialog中点击确定之后 执行
                if (this.step2.consider[this.first_index][0].change_list[this.last_index].model_list[0].model_id == 0) {
                    // 判断是否是假数据对象,
                    // model_list.splice(0, 1, { xxxx })
                    this.step2.consider[this.first_index][0].change_list[this.last_index].model_list.splice(0,1,this.model_op)
                } else {
                    this.step2.consider[this.first_index][0].change_list[this.last_index].model_list.push(this.model_op)
                }
            }else{
                for (let i = 0; i < this.step2.consider[this.first_index][0].change_list[this.last_index].model_list.length; i++) {
                    // console.log(this.step2.consider[this.first_index][0].change_list[this.last_index].model_list,"3")
                    // console.log(this.model_op,"2")
                    if (this.model_op.model_name == this.step2.consider[this.first_index][0].change_list[this.last_index].model_list[i].model_name) {
                        // console.log(this.step2.consider[this.first_index][0].change_list[this.last_index].model_list[i],"5")
                        this.step2.consider[this.first_index][0].change_list[this.last_index].model_list.splice(i, 1, this.model_op)
                        break
                    }
                }
            }
            // this.matrix_data[0].title_value[this.OSS_index].failure_id_list = doc_lis
            this.look(this.first_index)
            // console.log(this.model_op,"0*0")
            this.innerVisible = false
        },
        inner_dialog_before_close(done) {
            this.$confirm('确认关闭？')
                .then(_ => {
                    // this.inner_dialog_close()
                    if(this.model_check_flag){
                        // console.log(this.model_check_flag,"fa")
                        for(let i=0; i < this.step2.consider[this.first_index][0].change_list[this.last_index].model_name_list.length; i++) {
                            if(this.step2.consider[this.first_index][0].change_list[this.last_index].model_name_list[i] == this.model_name_temp) {
                                // console.log(this.step2.consider[this.first_index][0].change_list[this.last_index].model_name_list[i],"na")
                                this.step2.consider[this.first_index][0].change_list[this.last_index].model_name_list.splice(i, 1)
                                break
                            }
                        }
                    }
                    done()
                })
                .catch(_ => {})
        },
        inner_dialog_cancle(){
            if(this.model_check_flag){
                // console.log(this.model_check_flag,"fa")
                for(let i=0; i < this.step2.consider[this.first_index][0].change_list[this.last_index].model_name_list.length; i++) {
                    if(this.step2.consider[this.first_index][0].change_list[this.last_index].model_name_list[i] == this.model_name_temp) {
                        // console.log(this.step2.consider[this.first_index][0].change_list[this.last_index].model_name_list[i],"na")
                        this.step2.consider[this.first_index][0].change_list[this.last_index].model_name_list.splice(i, 1)
                        break
                    }
                }
            }
            this.innerVisible = false
        },
        getConsider() {
            this.$axios.get(this.Ip + '/DSTag/' + Number(window.sessionStorage.getItem('DocId'))).then(res => {
                if (res.data.result == 'OK') {
                    this.step2.micro_ver = res.data.micro_ver
                    this.step2.consider = []
                    for (var i_c of res.data.content) {
                        for (let item of i_c.change_list) {  
                            if (item.model_list.length === 0) {
                                // 因为表格根据数据动态刷新，如何model_list为[],表格行数会对不齐出现混乱
                                let module_item = {
                                    model_id: 0,
                                    model_name: '',
                                    checked: false,
                                    failure_id_list: [],
                                    result: ''
                                }
                                item.model_list.push(module_item) // 所以添加一个数据对象，这个数据对象要在在新增关联模块时删除
                            }
                            item.model_name_list = item.model_list.map(items => items.model_name)
                        }
                        var list = []
                        list.push(i_c)
                        this.step2.consider.push(list)
                    }
                    this.loading = false
                } else {
                    this.step2.micro_ver = res.data.micro_ver
                    var list = []
                    this.step2.consider.push(list)
                    this.loading = false
                }
                this.get_data = JSON.stringify(this.step2)
                this.change_el_carousel_style()
            })
        },

        prev() {
            this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
        },
        next() {
            this.step2.doc_id = window.sessionStorage.getItem('DocId')
            this.$axios
                .post(this.Ip + '/DSTag', this.step2)
                .then(res => {
                    // console.log(res)
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                        if (window.sessionStorage.getItem('Step') > '3') {
                            window.sessionStorage.setItem('Step', 4)
                        } else if (window.sessionStorage.getItem('Step') == '2') {
                            window.sessionStorage.setItem('Step', 3)
                        }
                        this.$router.push({ path: '/tagl/step4', query: { params: this.dbrfmFlag } })
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败!' + res.data.error,
                            type: 'error',
                            duration: 0
                        })
                    }
                })
                .catch(res => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0
                    })
                })
        },
        JumpAndSave() {
            this.step2.doc_id = window.sessionStorage.getItem('DocId')
            this.$axios
                .post(this.Ip + '/DSTag', this.step2)
                .then(res => {
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                    }
                })
                .catch(res => {})
        },
        save() {
            this.step2.doc_id = window.sessionStorage.getItem('DocId')
            this.$axios
                .post(this.Ip + '/DSTag', this.step2)
                .then(res => {
                    if (res.data.result == 'OK') {
                        window.sessionStorage.setItem('ver', res.data.micro_ver)
                        // this.showScene()
                        this.$message({
                            type: 'success',
                            message: '保存成功!'
                        })
                        this.getConsider()
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败!' + res.data.error,
                            type: 'error',
                            duration: 0
                        })
                    }
                })
                .catch(res => {
                    // console.log(res,"error")
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0
                    })
                })
        },
        cancel() {
            this.save_data = JSON.stringify(this.step2)
            if (this.save_data == this.get_data) {
                window.sessionStorage.removeItem('Step')
                this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        window.sessionStorage.removeItem('Step')
                        this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                    })
                    .catch(() => {})
            }
        },
        jump_to(index) {
            switch (index) {
                case '场景(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step1', query: { params: this.dbrfmFlag } })
                    break
                case '修改点影响点(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
                    break
                // case '考虑点(必填)':
                //     this.JumpAndSave()
                //     this.$router.push({ path: '/tagl/step3', query: { params: this.dbrfmFlag } })
                //     break
                case 'DRBFM(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step4', query: { params: this.dbrfmFlag } })
                    break
            }
        },
        cg_show(index,indexs){
            event.stopPropagation()
            $('.cg-box').hide()
            // find 寻找下面所有子元素!
            $('.checked-input-list').eq(index).find('.cg-box').eq(indexs).toggle(function(){})
        }
    }
}
</script>

<style scoped>
#consider {
    margin: 0 auto;
    width: 100%;
    height: 100%;
}
.countent {
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
.cbody {
    float: left;
    height: 100%;
    width: 84%;
    padding-left: 1%;
    border-left: 1px solid #c0c4cc;
    /*overflow-y: scroll;*/
    /*border: 1px solid red;*/
}

.el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    /*opacity: 0.75;*/
    line-height: 50px;
    margin: 0;
    background-color: white;
}

/*.el-carousel__item:nth-child(2n) {
  background-color: #dcdfe6;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #4EAB49;
}*/

.green {
    color: green;
}
.red {
    color: red;
}

.checkBox {
    margin: 20px 0 0 20px;
}
.scene-title {
    margin: 40px 0 20px 0;
}
.mid {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
    padding-right: 20px;
    padding-bottom: 55px;
    border-right: 1px solid #ccc;
    /*overflow-y: scroll;*/
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
}
.big-box {
    margin: 20px 0 0 0;
    overflow-x: hidden;
    width: 100%;
    height: 100%;
}
.doc-text {
    /*float:left;*/
    text-align: left;
    padding-left: 10px;
}
.doc-text:hover {
    font-weight: bold;
    cursor: pointer;
}

.casc {
    width: 350px;
}
.checked-input-list-title {
    margin-bottom: 15px;
    font-size: 18px;
}
/*.checked-input-list{
  margin-top: 40px;
}*/
.gray_col {
    background-color: #FAFAFA;
}
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
    padding: 5px 0;
}
thead {
    color: #909399;
    background-color: #edf9f5;
}
tbody {
    color: #606266;
}
th {
    padding: 3px 0;
}
td{
    position: relative;
}
.append-span {
    float: left;
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
}
.cg-box{
    position: absolute;
    z-index: 666;
    min-width: 200px;
    top:85%;
    left: 0;
    background-color: rgba(255,255,255,.9);
    border-radius: 5px;
    box-shadow: #666 0px 0px 10px;
    display: none;
    min-height: 100px;
}
.cg-box .el-checkbox+.el-checkbox{
    float: left;
}
.cg-box .el-checkbox{
    margin-top: 10px;
}
.caret{
    cursor: pointer;
}
@media screen and (max-width: 1334px) {
    .countent {
        max-width: 300px;
        min-width: 200px;
        width: 15%;
        height: 100%;
        padding: 20px;
        float: left;
    }
    .cbody {
        float: left;
        width: 80%;
        height: 100%;
        overflow-y: scroll;
    }
}
@media screen and (max-width: 1024px) {
    #consider {
        width: 1024px;
    }
    .header-top {
        display: none;
    }
    .header {
        height: 100%;
        padding: 10%;
        clear: both;
    }
}
</style>

