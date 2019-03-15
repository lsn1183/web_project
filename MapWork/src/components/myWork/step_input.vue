<template>
    <div id="basic-degign-step-one">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
            </div>
        </div>
        <div class="cbody">

            <div class="mid">
                <div class="mid-top">
                    <div class="step-one-title">
                        <h2 style="fontSize: 22px;fontWeight:bolder;backgroundColor:#6bcca0; color: white;lineHeight: 25px;height:25px">
                            <span style="lineHeight:25px;float:left;paddingLeft: 10px;">式样书</span>
                            <i class="el-icon-question" style="fontSize:15px; lineHeight:25px;float:left;marginLeft:5px" title="请提供和Usecase相关的式样书，式样书可以是要求式样书、机能式样书、操作式样书等"></i>
                            <!-- <div style="display:inline-block;" title="选择UseCase实现的式样书章节:例如，实现了机能式样书func_2_01_Map.xlsm第2.1.1章">
                                <img src="../../assets/img/wenhao10.svg" alt="" style="width:17px;height:17px;">
                            </div> -->
                        </h2>
                    </div>
                    <div class="step-one-content">
                        <el-select v-model="select_usecase_value" placeholder="请选择Usecase">
                            <el-option v-for="item in select_usecase_options" :key="item.sec_id" :label="item.label" :value="item.sec_id">
                            </el-option>
                        </el-select>
                    </div>
                    <div class="step-one-content">
                        <div class="step-one-content-books">
                            <div class="checked-input-list-title">选择不同的Usecase下的式样书（可搜索）</div>
                            <div class="select-content" style="">
                                <el-input placeholder="请输入内容" class="select-input" clearable v-model="input_spec" @focus="clear_input" @blur="loose_focus"></el-input>
                                <div v-show="spec_list_flag==true" class="select-option-box">
                                    <ul v-for="(item,index) in options" :key="index">
                                        <li v-if="item.select" :title="item.title" class="select-option-li" style="color: #42b983" @click="handleSelect(item)">
                                            {{item.title}}
                                        </li>
                                        <li v-else :title="item.title" class="select-option-li" @click="handleSelect(item)">
                                            {{item.title}}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="checked-input-list">
                        <el-table :data="table_list.content" border style="width: 98%" ref="multipleTable">
                            <el-table-column fixed prop="usecase" label="Usecase" width="130">
                                <template slot-scope="scope">
                                    <span>{{scope.row.number}}</span><span>-</span><span>{{scope.row.title}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column fixed prop="title" label="已选式样书" header-align='center'>
                                <template slot-scope="scope">
                                    <span :title="scope.row.specs.title" style="white-space: nowrap;text-overflow: ellipsis;cursor: pointer;" @click="LinkURL(scope.row.specs)">{{scope.row.specs.title}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column fixed prop="title" label="机能点" header-align='center'>
                                <template slot-scope="scope">
                                    <!-- <span :title="scope.row.title" style="white-space: nowrap;text-overflow: ellipsis;cursor: pointer;" @click="LinkURL(scope.row)">{{scope.row.title}}</span> -->
                                    <el-input type="textarea" placeholder="请输入机能点" v-model="scope.row.specs.func_id"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column fixed="right" label="操作" header-align='center' width="60">
                                <template slot-scope="scope">
                                    <!-- <el-button @click="look_input(scope.row)" type="text" size="small" style="">[ 查看 ]</el-button> -->
                                    <el-button @click="delete_input(scope.row,scope.$index)" type="text" size="small" style="">[ 删除 ]</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>

                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="save()">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="determine()">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
                </div>
            </div>
            <div class="right">
            </div>
        </div>
    </div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    name: 'CreateBasicDesignStepOne',
    data () {
        return {
            checkAll: false,
            active: Number(window.sessionStorage.getItem('Step')),
            tecBookArray: [],
            optBooksArray: [],
            // books: requireBooksOptions,
            // styleBook: '要求式样书',
            table_list: {
                doc_id: 0,
                sec_id: 0,
                micro_ver: window.sessionStorage.getItem('ver'),
                commit_user: window.sessionStorage.getItem('Uall'),
                content: [] //requireBookArray
            },
            table_list_content_copy: [],
            spec_list_flag: false,
            input_spec: "",
            select_list: [],
            options: [],
            get_data: '',
            save_data: '',
            dbrfmFlag: false,
            select_usecase_value: '',
            select_usecase_options: []
        }
    },
    computed: {
        doc_id (val) {
            return this.$store.state.doc_id
        },
    },
    watch: {
        input_spec (val, cb) {

            if (this.input_spec != "") {
                // this.SearchSpec(val,cb)
                this.SearchSpec2(val)
            } else {
                this.getSpec2()
            }

        },
    },
    mounted () {
        
        this.get_all_usecase_fun()
        this.getSpec2()
        this.get_usecase_table_list();
        var self = this
        setTimeout(() => {
            $('.jump').on('click', function (e) {
                self.jump_to($(this).text())
            })
        }, 10)
        if (this.$route.query.params) {
            this.dbrfmFlag = this.$route.query.params
        }
    },
    methods: {
        clear_input () {
            if (this.input_spec != "") {
                this.SearchSpec2(this.input_spec)
            } else {
                this.getSpec2()
            }
            this.spec_list_flag = true
            // this.input_spec = ""

        },
        loose_focus () {
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                this.spec_list_flag = false;
            }, 250);

        },
        SearchSpec2 (val) {
            this.$axios.get(this.Ip + "/ApiDSDocSpec/" + window.sessionStorage.getItem('DocId') + "/" + val).then(res => {
                // console.log(res,"....")
                if (res.data.result = "OK") {
                    // console.log(res,"....")
                    this.options = res.data.content
                    for (var i = 0; i < this.table_list.content.length; i++) {
                        for (var j = 0; j < this.options.length; j++) {
                            if (this.table_list.content[i].spec_id == this.options[j].spec_id) {
                                // console.log(this.options[j],"sps")
                                this.options[j].select = true
                            }
                        }
                    }
                }
            })

        },
        getSpec2 () {
            this.$axios.get(this.Ip + "/ApiDSDocSpec/" + window.sessionStorage.getItem('DocId')).then(res => {
                if (res.data.result = "OK") {
                    this.options = res.data.content
                    for (let i = 0, len = this.options.length; i < len; i++) {//高亮已选择过的式样书
                        for (let j = 0, leng = this.table_list.content.length; j < leng; j++) {
                            if (this.table_list.content[j].specs.spec_id == this.options[i].spec_id && this.select_usecase_value == this.table_list.content[j].sec_id) {
                                this.options[i].select = true
                            }
                        }
                    }
                }
            })
        },
        SearchSpec (val, cb) {
            this.$axios.get(this.Ip + "/Specification/" + 1 + "/" + val).then(res => {
                // console.log(res,"....")
                if (res.data.result = "OK") {
                    // console.log(res,"....")
                    this.options = res.data.content
                    cb(this.options)
                }
            })

        },
        getSpec (cb) {
            this.$axios.get(this.Ip + "/Specification").then(res => {
                if (res.data.result = "OK") {
                    // console.log(res,"sp")
                    this.options = res.data.content
                    cb(this.options)
                }
            })
        },
        querySearch (queryString, cb) {
            // console.log(queryString,"cb")
            if (queryString != "") {
                this.SearchSpec(queryString, cb)
            } else {
                this.getSpec(cb)
            }
        },
        LinkURL (data) {
            window.open(data.url)
        },
        get_usecase_table_list () {
            this.$axios.get(this.Ip + '/UcRelSpec/' + window.sessionStorage.getItem('DocId'))
                .then(res => {
                    
                    if (res.data.result == "OK") {
                        let req_data = res.data.content
                        let newArray = []
                        let req_data_item = {}
                        for (let i = 0; i < req_data.length; i++) {
                            if (req_data[i].specs.length != 0) {
                                for (let j = 0; j < req_data[i].specs.length; j++) {
                                    req_data_item = JSON.parse(JSON.stringify(req_data[i]))//改变指针指向
                                    req_data_item.specs = req_data[i].specs[j]
                                    newArray.push(req_data_item)
                                }
                            } else {
                                newArray.push(req_data[i])
                            }
                        }
                        this.table_list.content = newArray
                        this.table_list.micro_ver = res.data.micro_ver
                        // this.select_list = res.data.content
                    } else {
                        this.table_list.micro_ver = res.data.micro_ver
                    }
                    this.get_data = JSON.stringify(this.table_list)
                }).catch(err => { console.log('======', err) })

        },
        look_input (row) {

        },
        delete_input (row, index) {
            this.table_list.content.splice(index, 1)
        },
        prev () {
            // this.$router.push('/tagl/step1')
            this.$router.push({ path: '/tagl/step1', query: { params: this.dbrfmFlag } })
        },
        next () {
            this.table_list.doc_id = Number(window.sessionStorage.getItem('DocId'))
            if (window.sessionStorage.getItem('stepTwoSecId') == null) {
                this.table_list.sec_id = 0
            } else {
                this.table_list.sec_id = window.sessionStorage.getItem('stepTwoSecId')
            }
            this.$axios.post(this.Ip + '/UcRelSpec', this.table_list).then(res => {
                if (res.data.result == 'OK') {
                    window.sessionStorage.setItem('stepTwoSecId', res.data.sec_id)
                    window.sessionStorage.setItem('ver', res.data.micro_ver)
                    if (window.sessionStorage.getItem("Step") > "6") {
                        window.sessionStorage.setItem("Step", 7)
                    } else if (window.sessionStorage.getItem("Step") == "1") {
                        window.sessionStorage.setItem("Step", 2)
                    }
                    this.$router.push({ path: '/tagl/step3', query: { params: this.dbrfmFlag } })
                } else {
                    this.$message({
                        showClose: true,
                        message: res.data.error,
                        type: 'error',
                        duration: 0,
                    })
                }
            })
                .catch(err => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0,
                    })
                })
        },
        handleSelect (item) {
            var specs = []
            if (this.select_usecase_value != '') {
                for (var items of this.select_usecase_options) {
                    if (this.select_usecase_value == items.sec_id) {
                        items.specs = {
                            spec_file_name: item.spec_file_name,
                            spec_id: item.spec_id,
                            spec_name: item.spec_name,
                            spec_type: item.spec_type,
                            title: item.title,
                            url: item.url
                        }
                        specs = JSON.parse(JSON.stringify(items))//改变引用地址
                        break
                    }
                }
                this.check_list_data_fun(this.table_list.content, specs)
            } else {
                this.$alert("请选择式样书", "提示")
            }
        },
        check_list_data_fun (data, specs) {
            let flag = false
            for (var item_1 of data) {
                if (item_1.sec_id == specs.sec_id && item_1.specs.spec_id == specs.specs.spec_id) {
                    this.$alert("重复选择了式样书", "提示")
                    flag = true
                    break;
                }
            }
            if (flag == false) {
                // 归类排序
                if (this.table_list.content.length == 0) {
                    this.table_list.content.unshift(specs)
                } else {
                    let self = this
                    function insert (obj_1, obj_2) {
                        let table_usecase = []
                        for (const iterator of obj_1) {
                            table_usecase.push(iterator.sec_id)
                        }
                        if (table_usecase.indexOf(obj_2.sec_id) != -1) {
                            let index = table_usecase.indexOf(obj_2.sec_id)
                            self.table_list.content.splice(index + 1, 0, obj_2)
                        } else {
                            self.table_list.content.unshift(obj_2)
                        }
                        self.table_list_height_light(obj_2)
                    }
                    insert(this.table_list.content, specs)

                }
            }
        },
        table_list_height_light (specs) {
            if (specs) {
                this.table_list.content.forEach(row => {
                    if (JSON.stringify(row) == JSON.stringify(specs)) {
                        this.$nextTick(() => {
                            this.$refs.multipleTable.toggleRowSelection(1, true)
                        })
                    }
                });
            }
        },
        save () {
            this.table_list.doc_id = window.sessionStorage.getItem('DocId')
            // console.log(this.table_list, 'save')
            this.$axios.post(this.Ip + '/UcRelSpec', this.table_list).then(res => {
                if (res.data.result == 'OK') {
                    window.sessionStorage.setItem('ver', res.data.micro_ver)
                    this.get_usecase_table_list()
                    this.$message({
                        type: 'success',
                        message: '保存成功!'
                    })
                } else {
                    this.$message({
                        showClose: true,
                        message: res.data.error,
                        type: 'error',
                        duration: 0,
                    })
                }
            }).catch(err => {

            })
        },
        JumpAndSave () {
            this.table_list.doc_id = window.sessionStorage.getItem('DocId')
            this.$axios.post(this.Ip + '/UcRelSpec', this.table_list).then(res => {
                if (res.data.result == 'OK') {
                    window.sessionStorage.setItem('ver', res.data.micro_ver)
                }
            }).catch(err => {
                this.$message({
                    showClose: true,
                    type: 'error',
                    message: '服务异常',
                    duration: 0,
                })
            })
        },
        cancel () {
            this.save_data = JSON.stringify(this.table_list)
            if (this.save_data == this.get_data) {
                this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {

                    this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                })
                    .catch(() => { })
            }
        },
        jump_to (index) {
            switch (index) {
                case 'Usecase(必填)':
                    this.$router.push({ path: '/tagl/step1', query: { params: this.dbrfmFlag } })
                    break
                // case '式样书(必填)':
                //     this.JumpAndSave()
                //     this.$router.push({path:'/tagl/step2',query:{params:this.dbrfmFlag}})
                //     break
                case '场景(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step3', query: { params: this.dbrfmFlag } })
                    break
                case '变更变化点(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step4', query: { params: this.dbrfmFlag } })
                    break
                case 'Sequence(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step5', query: { params: this.dbrfmFlag } })
                    break
                case 'Statemachine(选填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step6', query: { params: this.dbrfmFlag } })
                    break
                case 'DRBFM(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step7', query: { params: this.dbrfmFlag } })
                    break
                case "1Usecase(必填)":
                    if (this.active == 0) {
                        this.$router.push('/tagl/step1')
                    }
                    break;
                case "2式样书(必填)":
                    if (this.active == 1) {
                        this.$router.push('/tagl/step2')
                    }
                    break;
                case "3场景(必填)":
                    if (this.active < 3) {
                        this.next()
                        // this.$router.push('/tagl/step3')
                    }
                    break;
                case "4Sequence(必填)":
                    if (this.active == 3) {
                        this.$router.push('/tagl/step4')
                    }
                    break;
                case "5Statemachine(选填)":
                    if (this.active == 4) {
                        this.$router.push('/tagl/step5')
                    }
                    break;
                case "6DRBFM(必填)":
                    if (this.active == 5) {
                        this.$router.push('/tagl/step6')
                    }
                    break;
            }
        },
        determine () {
            this.save_data = JSON.stringify(this.table_list)
            if (this.save_data == this.get_data) {
                this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
            } else {
                this.save()
                this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
            }
        },
        get_all_usecase_fun () {
            this.select_usecase_options = []
            this.$axios.get(this.Ip + '/AllUsecase/' + window.sessionStorage.getItem('DocId')).then(res => {
                if (res.data.result == 'OK') {
                    for (let items of res.data.content) {//修改selsect框显示数据格式
                        if (items.title == '') {
                            items.label = items.number
                            this.select_usecase_options.push(items)
                        }else{
                            items.label = items.number + '-' +items.title
                            this.select_usecase_options.push(items)
                        }
                    }
                } else {
                    if (res.data.result == 'NG') {
                        return
                        this.$message({
                            showClose: true,
                            type: 'error',
                            message: 'NG:无数据',
                        })
                    }
                }
            })
        }
    }
}
</script>

<style scoped>
.el-table .success-row {
    background: oldlace;
}
.el-select-dropdown__item.selected {
    color: #42b983;
}
.el-select .el-input.is-focus .el-input__inner {
    color: #42b983;
}

#basic-degign-step-one {
    /* background-color: bisque; */
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
}

.step-one-title {
    margin: 40px 0 20px 0;
}
.step-one-text {
    margin-left: 80px;
}
.checked-input-list {
    margin-left: 20px;
    margin-top: 100px;
    float: left;
    width: 100%;
    height: 400px;
}
.checked-input-list-title {
    margin-bottom: 15px;
    font-size: 18px;
}
.mid {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
    padding-right: 20px;
    padding-bottom: 55px;
    border-right: 1px solid #ccc;
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
.step-one-content {
    margin-top: 20px;
    margin-left: 20px;
}
.select_input {
    width: 50%;
}
.sequence_title_text {
    margin-left: 20px;
    margin-bottom: 20px;
    font-size: 14px;
    color: #5e6d82;
}
.select-content {
    position: relative;
    margin-top: 20px;
}
.select-option-box {
    position: absolute;
    background-color: white;
    z-index: 5;
    margin-top: 10px;
    width: 50%;
    max-height: 150px;
    overflow-y: scroll;
    border: 1px solid #ccc;
    border-radius: 5px;
}
.select-option-li {
    font-size: 14px;
    width: 98%;
    white-space: nowrap;
    list-style: none;
    line-height: 30px;
    padding-left: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #606266;
}
.select-option-li:hover {
    cursor: pointer;
    background-color: #f5f7fa;
}

@media screen and (max-width: 1366px) {
    .mid {
        width: 880px;
    }
    .right {
        width: 20%;
        height: 100%;
        float: left;
    }
    .checked-input-list {
        margin-left: 20px;
        float: left;
        height: 400px;
    }
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
    }
    .step-one-content {
    }
}
@media screen and (max-width: 1024px) {
    #basic-degign-step-one {
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
    .cbody {
        float: left;
        width: 820px;
        height: 100%;
    }
    .mid {
        width: 635px;
    }
    .step-one-content {
        margin-left: 20px;
    }
    .checked-input-list {
        margin-left: 20px;
        float: left;
        height: 400px;
    }
}
</style>
