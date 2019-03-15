<template>
    <div class="add-project-step">
        <div class="countent">
            <div class="header-top">
            </div>
            <div class="header">
                <el-steps direction="vertical" :active="active" finish-status="success">
                    <el-step class="jump" title="项目信息">1</el-step>
                    <!-- <el-step class="jump" title="平台">2</el-step> -->
                    <el-step class="jump" title="知识库" icon="el-icon-edit" status="process">3</el-step>
                    <el-step class="jump" title="模块">4</el-step>
                    <el-step class="jump" title="模块负责组">5</el-step>
                </el-steps>
            </div>
        </div>
        <div id="Add-File-Mode">
            <div class="mid">
                <div class="mid-top">
                    <div class="step-one-title">
                        <h2>知识库
                            <i class="el-icon-question" style="font-size: 15px;" title=""></i>
                        </h2>
                    </div>
                    <div style="font-size: 16px;margin-bottom: 10px;">
                        <div style="margin:0 0 10px 0">
                            <span style="padding-left:20px">项目：{{proj_name}}</span>
                        </div>
                        <!-- <div>
                            <span style="padding-left:20px">平台：{{fw_name}}</span>
                        </div> -->
                    </div>
                    <!-- <div v-for="(One,Oneindex) in texttree" class="one-box">
                        {{One.tag}}
                        <el-checkbox v-model="One.checkAll"  @change="checkedALL"></el-checkbox>
                        <el-checkbox-group v-model="One.checked" @change="CheckedChange">

                            <el-checkbox v-for="(Two,Twoindex) in One.sub_tags" :label="Two.tag"  :key="Two.tag_id"></el-checkbox>

                        </el-checkbox-group>
                    </div> -->
                    <el-checkbox-group v-model="PostTagList.tag_list" @change="CheckedChange">
                        <div v-for="(One,Oneindex) in bigtree" class="one-box" style="">
                            <div style="clear:both;"></div>
                            <div class="checked-title" style="">{{One.tag}}</div>

                            <div v-if="One.father" class="two-box-two">
                                <el-checkbox class="checked-content-box" v-for="(Two,Twoindex) in One.sub_tags" :label="Two.tag_id" :key="Two.tag_id">
                                    {{Two.tag}}</el-checkbox>
                            </div>

                            <div v-else v-for="(Two,Twoindex) in One.sub_tags" class="two-box" style="">
                                <div class="checked-title-two">{{Two.tag}}</div>
                                <!-- <el-checkbox v-model="Two.checkAll" @change="CheckAll">{{Two.tag}}全选</el-checkbox> -->

                                <div v-if="Two.father" class="three-box" style="">

                                    <!-- <el-checkbox-group :indeterminate="Two.isIndeterminate" v-model="Two.checked" @change="CheckedChange"> -->

                                    <el-checkbox class="checked-content-box" v-for="(Three,Threeindex) in Two.sub_tags" :label="Three.tag_id" :key="Three.tag_id">{{Three.tag}}</el-checkbox>

                                    <!-- </el-checkbox-group> -->

                                </div>

                                <div v-else v-for="(Three,Threeindex) in Two.sub_tags" class="three-box">

                                    <div class="checked-title-three">{{Three.tag}}</div>
                                    <!-- <el-checkbox v-model="Two.checkAll" @change="CheckAll">{{Two.tag}}全选2</el-checkbox> -->

                                    <div v-if="Three.father">
                                        <!-- <el-checkbox-group :indeterminate="Three.isIndeterminate" v-model="Three.checked" @change="CheckedChange"> -->

                                        <el-checkbox class="checked-content-box" v-for="(four,Fourindex) in Three.sub_tags" :label="four.tag_id" :key="four.tag">{{four.tag}}</el-checkbox>

                                        <!-- </el-checkbox-group> -->
                                    </div>
                                    <div v-else>
                                    </div>

                                </div>
                            </div>

                        </div>

                        <div class="one-box">
                            <div style="clear:both;"></div>
                            <div class="checked-title" style="">平台</div>

                            <div class="two-box-two">
                                <el-checkbox v-for="(One,Oneindex) in fwtree" class="checked-content-box" :label="One.tag_id" :key="One.tag_id" disabled>
                                    {{One.tag}}</el-checkbox>
                            </div>

                        </div>
                    </el-checkbox-group>

                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="prev()"><i class="el-icon-arrow-left"></i>上一步</el-button>
                    <el-button @click="save()" type="primary" size='mini'>&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button @click="cancel()" type="primary" size='mini'>&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="next()">下一步
                        <i class="el-icon-arrow-right"></i>
                    </el-button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
require('../../../assets/js/jquery-1.8.3.min.js')
export default {
    data () {
        return {
            PostTagList: {
                proj_id: 0,
                user_name: window.sessionStorage.getItem('Uall'),
                tag_list: []
            },
            proj_name: window.sessionStorage.getItem('proj_name'),
            fw_name: window.sessionStorage.getItem('fw_name'),
            OptionsTagList: [],
            active: Number(window.sessionStorage.getItem('step_id')),
            spec_list_flag: false,
            input_spec: "",
            select_list: [],
            options: [],
            bigtree: [],
            fwtree: [],
            checked: [],
            get_data: '',
            save_data: '',
        }
    },
    // watch:{
    //     input_spec(val,cb){
    //         if(this.input_spec!=""){
    //             // this.SearchSpec(val,cb)
    //             this.SearchSpec2(val)
    //         }else{
    //             this.getSpec2()
    //         }

    //     }
    // },
    created () {
        // this.reqStepThreeData()
    },
    mounted () {
        this.reqStepThreeData()
        var self = this
        $('.jump').on('click', function (e) {
            self.jump_to($(this).text())
        });
        this.getTree()
        this.getFW()
        this.getFW_Name()
    },
    methods: {
        reqStepThreeData () {
            this.$axios.get(this.Ip + '/ProjectTag/' + window.sessionStorage.getItem('proj_id'))
                .then(res => {
                    // console.log(res,"lis")
                    if (res.data.result == 'OK') {
                        this.PostTagList.tag_list = res.data.content
                    } else {
                        // alert('服务器异常')
                    }
                    this.get_data = JSON.stringify(this.PostTagList)
                })
                .catch(err => {
                    alert(err)
                })
        },
        getFW_Name () {
            this.$axios.get(this.Ip + '/ProjectFW/' + Number(window.sessionStorage.getItem('proj_id')))
                .then(res => {
                    // console.log(res)
                    if (res.data.result == 'OK') {
                        this.fw_name = res.data.content.fw_name
                    } else {
                    }
                })
                .catch(err => {
                    alert(err)
                })
        },
        getTree () {
            this.$axios.get(this.Ip + "/DocTagProject/common").then(res => {
                if (res.data.result == "OK") {
                    this.bigtree = res.data.content
                    // console.log(res,"tag")
                    for (var i = 0; i < this.bigtree.length; i++) {

                        this.bigtree[i].checked = []

                        for (var j = 0; j < this.bigtree[i].sub_tags.length; j++) {

                            this.bigtree[i].sub_tags[j].checked = []

                        }
                    }
                } else {
                }
            })
        },
        getFW () {
            this.$axios.get(this.Ip + "/DocTagProject/special").then(res => {
                // console.log(res,"fw")
                if (res.data.result == "OK") {
                    this.fwtree = res.data.content.fw_tag

                    this.removeFWTag()

                    for (var i = 0; i < this.fwtree.length; i++) {

                        this.fwtree[i].checked = []

                        if (this.fwtree[i].tag == window.sessionStorage.getItem('fw_name')) {
                            var repeat_flag = false
                            for (var f_if of this.PostTagList.tag_list) {
                                if (f_if == this.fwtree[i].tag_id) {
                                    repeat_flag = true
                                }
                            }
                            if (repeat_flag == false) {
                                // console.log(this.fwtree[i].tag_id,"append")
                                this.PostTagList.tag_list.push(this.fwtree[i].tag_id)
                            }

                        }

                        // for(var j=0;j<this.fwtree[i].sub_tags.length;j++){

                        //         this.fwtree[i].sub_tags[j].checked=[]

                        // }
                    }
                } else {
                }
            })
        },
        CheckedChange (value) {
            // console.log(this.bigtree)
            // console.log(value)
        },
        removeFWTag () {
            for (var i = 0; i < this.PostTagList.tag_list.length; i++) {
                for (var j = 0; j < this.fwtree.length; j++) {
                    if (this.PostTagList.tag_list[i] == this.fwtree[j].tag_id) {
                        // console.log(this.PostTagList.tag_list[i],"sps")
                        var index = this.PostTagList.tag_list.indexOf(this.fwtree[j].tag_id)
                        this.PostTagList.tag_list.splice(index, 1)
                    }
                }
            }
        },

        prev () {
            // this.$router.push('/tagl/Project_Step_Two')
            let router_flag=this.$route.query.flag
            let routerValue={path:'/tagl/Project_Step_One',query:{flag:router_flag}}
            this.$router.push(routerValue)
        },
        save () {
            this.PostTagList.proj_id = window.sessionStorage.getItem('proj_id')
            this.$axios.post(this.Ip + '/ProjectTag', this.PostTagList)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.reqStepThreeData()
                        this.$message({
                            message: '保存成功',
                            type: 'success'
                        })
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败',
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
        next () {
            if (this.PostTagList.tag_list.length == 0) {
                this.$message({
                    message: '请选择技术文档',
                    type: 'error'
                })
                return
            }
            this.PostTagList.proj_id = window.sessionStorage.getItem('proj_id')
            this.$axios.post(this.Ip + '/ProjectTag', this.PostTagList)
                .then(res => {
                    if (res.data.result == 'OK') {
                        // if (window.sessionStorage.getItem('step_id') ==2) {
                        //     window.sessionStorage.setItem('step_id', 3)
                        // }

                        if (window.sessionStorage.getItem('step_id') == 1) {
                            window.sessionStorage.setItem('step_id', 2)
                        }
                        // this.$router.push('/tagl/Project_Step_Four')
                        let router_flag=this.$route.query.flag
                        let routerValue={path:'/tagl/Project_Step_Four',query:{flag:router_flag}}
                        this.$router.push(routerValue)
                    } else {
                        this.$message({
                            showClose: true,
                            message: '保存失败',
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
        jump_to (index) {
            switch (index) {
                case "项目信息":
                    // this.JumpAndSave()
                    var router_flag=this.$route.query.flag
                    if (this.$route.query.flag=="true") {
                        router_flag="false"
                    }
                    var routerValue={path:'/tagl/Project_Step_One',query:{flag:router_flag}}
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_One')
                    break;
                case "平台":
                    // this.JumpAndSave()
                    this.$router.push('/tagl/Project_Step_Two')
                    break;
                case "知识库":
                    // this.JumpAndSave()
                    var router_flag=this.$route.query.flag
                    var routerValue={path:'/tagl/Project_Step_Three',query:{flag:router_flag}}
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_Three')
                    break;
                case "模块":
                    // this.JumpAndSave()
                    var router_flag=this.$route.query.flag
                    var routerValue={path:'/tagl/Project_Step_Four',query:{flag:router_flag}}
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_Four')
                    break;
                case "模块负责组":
                    // this.JumpAndSave()
                    var router_flag=this.$route.query.flag
                    var routerValue={path:'/tagl/Project_Step_Five',query:{flag:router_flag}}
                    this.$router.push(routerValue)
                    // this.$router.push('/tagl/Project_Step_Five')
                    break;
            
                case "4模块":
                    if (this.active > 2) {
                        this.$router.push('/tagl/Project_Step_Four')
                    }
                    break;
            
            }
        },
        cancel () {
            this.save_data = JSON.stringify(this.PostTagList)
            if (this.save_data == this.get_data) {
                window.sessionStorage.removeItem('proj_id')
                window.sessionStorage.removeItem('step_id')
                this.$store.state.fpm_id = 1
                this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        window.sessionStorage.removeItem('proj_id')
                        window.sessionStorage.removeItem('step_id')
                        this.$store.state.fpm_id = 1
                        this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
                    })
                    .catch(() => { })
            }
        }
    }
}
</script>
<style scoped>
.add-project-step {
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
.mid {
    width: 80%;
    height: 100%;
    float: left;
    padding-top: 40px;
    padding-right: 1%;
    position: relative;
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
.step-one-content {
    margin-top: 20px;
    margin-left: 20px;
}
.footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}

/**/

#Add-File-Mode {
    float: left;
    margin: 0 auto;
    width: 84%;
    height: 100%;
    padding-left: 1%;
    border-left: 1px solid #c0c4cc;
}

.div-center {
    width: 100%;
    text-align: left;
    padding: 0 0 20px;
}
.div-center-label {
    margin-left: 10px;
}

.div-title {
    display: inline-block;
    width: 90px;
    text-align: right;
    margin-right: 20px;
    color: #4d4d4d;
    font-weight: bold;
}
.div-title-ex {
    margin: 0;
    padding: 0;
    width: 100%;
    text-align: left;
}
h2 {
    font-size: 22px;
    font-weight: bolder;
    color: white;
    padding-left: 10px;
    line-height: 26px;
    background-color: #6bcca0;
}
.summary {
    vertical-align: top;
    height: 66px;
    line-height: 66px;
}
.div-input {
    display: inline-block;
    width: 500px;
}

/**/
.step-one-title {
    margin: 40px 0 20px 0;
}
.step-one-text {
    margin-left: 80px;
}
.step-one-content {
    margin-top: 20px;
    margin-left: 20px;
}
.one-box {
    /*border:1px dashed red;*/
    width: 100%;
    float: left;
}
.two-box {
    margin-left: 20px;
    border: 1px dashed #c0c4cc;
    width: 380px;
    min-height: 80px;
    float: left;
}
.two-box-two {
    margin-left: 20px;
    border: 1px dashed #c0c4cc;
    width: 98%;
    min-height: 60px;
    float: left;
}
.three-box {
    /*margin-left:40px;*/
    /*border:1px dashed green;*/
}

.checked-title {
    font-size: 18px !important;
    margin: 10px 0 10px 10px;
    padding-left: 10px;
    background-color: #6bcca0;
    color: white;
    /*text-align: center;*/
}
.checked-title-two {
    font-size: 16px !important;
    text-align: center;
}
.checked-title-three {
    font-size: 14px !important;
}
.checked-content-box {
    margin-left: 20px;
    line-height: 30px;
    width: 169px;
}
@media screen and (max-width: 1366px) {
    .mid {
        width: 880px;
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
    #Add-File-Mode {
        float: left;
        width: 80%;
        height: 100%;
    }
}
@media screen and (max-width: 1024px) {
    .add-project-step {
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
    #Add-File-Mode {
        float: left;
        width: 820px;
        height: 100%;
    }
    .mid {
        width: 635px;
    }
    .div-input {
        display: inline-block;
        width: 400px;
    }
}
</style>