<template>
    <div class="test-case-content">
        <div class="wrapper">
            <div class="operate-header">
                <div class="operate-header-title">
                    <h2 class="title">测试用例预览
                        <div class="operate-btn-bar">
                            <i class="el-icon-more" v-popover:parent_info_pop></i>
                            <el-popover placement="bottom-end" ref='parent_info_pop' trigger="hover">
                                <p class="operate-display-icon" @click="link_to_diff()">查看履历</p>
                                <p class="operate-display-icon" @click="up_case_version(test_case_form.id)">提升版本</p>
                                <p class="operate-display-icon" @click="cancel()">返回</p>
                            </el-popover>
                        </div>
                    </h2>
                    <p class="title-detail">
                        <span>xxxxxxxxxxx</span>
                    </p>
                </div>
            </div>
            <div class="wrapper-content">
                <div class="left-view fl">
                    <div class="view-left-content">
                        <!--标题-->
                        <div class="title">
                            <h2 class="title-h2">
                                <span>123</span>
                                <!-- <span class="append-span" style="fontWeight:500"> &nbsp;&nbsp;&nbsp;version:1.0.0.0</span> -->
                                <!-- <div class="append-span statediv" style="float: right;fontWeight:500">
                            <span style="marginRight:20px" @click='link_to_diff()'>[ 查看履历 ]</span>
                        </div> -->

                            </h2>
                            <p class="title-detail">
                                <span>负责人为xxxxxx&nbsp;&nbsp;&nbsp;&nbsp; 版本:{{test_case_form.case_version}}</span>
                            </p>
                            <!-- <p class="title-content">
                        <span class="left-content">1111111</span>
                    </p> -->
                        </div>

                        <!-- 摘要 -->
                        <div class="Asta">
                            <h3 class="title-h3">
                                <span style="float:left">摘要</span>
                            </h3>
                            <div class="table-box table-box-left" style="overflow-x: scroll;" v-if="test_case_form.abstract == '' ? false : true" v-html="test_case_form.abstract">
                            </div>
                            <p class="message" v-else>暂无数据</p>
                        </div>

                        <!-- 前提 -->
                        <div class="Block">
                            <h3 class="title-h3">
                                <span>前提</span>
                            </h3>
                            <div class="table-box table-box-left" style="overflow-x: scroll;" v-if="test_case_form.premise == '' ? false: true" v-html="test_case_form.premise">

                            </div>
                            <p class="message" v-else>暂无数据</p>
                        </div>

                        <!-- 重要性 -->
                        <div class="Block">
                            <h3 class="title-h3">
                                <span>重要性</span>
                            </h3>
                            <div class="table-box table-box-left" v-if="test_case_form.importance == '' ? false: true">
                                <span v-if="test_case_form.importance === 'low'">低</span>
                                <span v-if="test_case_form.importance === 'middle'">中</span>
                                <span v-if="test_case_form.importance === 'high'">高</span>
                            </div>
                            <p class="message" v-else>暂无数据</p>
                        </div>

                        <!-- 测试方式 -->
                        <div class="Block">
                            <h3 class="title-h3">
                                <span>测试方式</span>
                            </h3>
                            <div class="table-box table-box-left" v-if="test_case_form.is_automatically == '' ? false: true">
                                <span v-if="test_case_form.is_automatically === 'automatically'">自动</span>
                                <span v-if="test_case_form.is_automatically === 'manually'">手动</span>
                            </div>
                            <p class="message" v-else>暂无数据</p>
                        </div>

                        <!-- 仕向地 -->
                        <div class="Class">
                            <h3 class="title-h3">
                                <span>仕向地</span>
                            </h3>
                            <div class="table-box table-box-left" v-if="test_case_form.dest_list.length === 0 ? false: true">
                                <el-table :data="test_case_form.dest_list" ref="caseStepTable" border size="mini">
                                    <el-table-column label="仕向地名称" align="center" prop="name">
                                    </el-table-column>
                                    <el-table-column label="仕向地简介" align="center" prop="introduce">
                                    </el-table-column>
                                </el-table>

                            </div>
                            <p class="message" v-else>暂无数据</p>
                        </div>
                        <!-- IF -->
                        <div class="IF" id="I_F">
                            <h3 class="title-h3">
                                <span>自定义字段</span>
                            </h3>
                            <div class="table-box table-box-left">
                                <el-form label-width="110px">
                                    <el-form-item :label="item.name" v-for="(item, index) in three_list.field_list" :key="index" label-position="top">
                                        <div v-if="item.type === 'input'">
                                            <el-input v-model="item.field_value" style="width: 500px;" disabled></el-input>
                                        </div>

                                        <div v-else-if="item.type === 'textarea'">
                                            <el-input v-model="item.field_value" type="textarea" disabled></el-input>
                                        </div>

                                        <div v-else-if="item.type === 'select'">
                                            <el-select v-model="item.field_value" disabled>
                                                <el-option v-for="(item_children, indexs) in item.option_list" :key="indexs" :label="item_children.label" :value="item_children.value">

                                                </el-option>
                                            </el-select>
                                        </div>

                                        <div v-else-if="item.type === 'checkbox'">
                                            <el-radio-group v-model="item.field_value" size="small" disabled>
                                                <el-radio :label="item_children.value" v-for="(item_children, indexs) in item.option_list" :key="indexs">{{item_children.label}}</el-radio>
                                            </el-radio-group>
                                        </div>

                                        <div v-else-if="item.type === 'multiSelect'">
                                            <el-checkbox-group v-model="item.field_value" disabled>
                                                <el-checkbox :label="item_children.value" :key="indexs" v-for="(item_children, indexs) in item.option_list">{{item_children.label}}</el-checkbox>
                                            </el-checkbox-group>
                                        </div>
                                    </el-form-item>
                                </el-form>
                            </div>
                            <!-- <p class="message" v-else>暂无数据</p> -->
                        </div>

                        <!-- 测试步骤 -->
                        <div class="Usecase">
                            <h3 class="title-h3">
                                <span>测试步骤</span>
                            </h3>
                            <!-- usecase共通图 -->
                            <div class="usecase-common-pic-box">
                                <!-- <h4 class="title-h4" style="paddingTop:0;border:0">
                            <span>Usecase共通图</span>
                        </h4> -->
                            </div>
                            <div class="table-box table-box-left" v-if="test_case_form.step_list.length === 0 ? false: true">
                                <el-table :data="test_case_form.step_list" ref="caseStepTable" border size="mini">
                                    <el-table-column label="测试顺序" align="center" width="100px" prop="order">
                                    </el-table-column>
                                    <el-table-column label="测试操作" align="center" prop="operate">
                                    </el-table-column>
                                    <el-table-column label="期望值" align="center" prop="expected_value">
                                    </el-table-column>
                                    <el-table-column label="测试方式" align="center" width="100px;" prop="is_automatically">
                                        <template slot-scope="scope">
                                            <span v-if="scope.row.is_automatically == true">自动</span>
                                            <span v-else>手动</span>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>

                            <p class="message" v-else>暂无数据</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="wrapper-footer-btn">
                <el-button @click="cancel()" size="small">返回</el-button>
            </div>
        </div>
    </div>
</template>
<script>
import { get_three_list, get_one_test_case, improve_case_version } from '@/api/testcase'
export default {
    name: 'test-case-preview',
    data() {
        return {
            test_case_form: {
                id: 0,
                title: '',
                case_version: '',
                charger: '',
                abstract: '',
                premise: '',
                importance: '',
                test_mode: '',
                dest_list: [],
                keyword_list: [],
                field_value_list: [],
                step_list: [
                    {
                        order: '',
                        operate: '',
                        expected_value: '',
                        is_automatically: true
                    }
                ]
            },
            three_list: {}
        }
    },
    computed: {
        module_id() {
            return this.$store.getters.tree_node_data_id
        },
        test_case_id() {
            return this.$store.getters.test_case_id
        }
    },
    created() {
        this.transfer_req_data_to_display_data()
    },
    methods: {
        cancel() {
            this.$router.go(-1)
        },
        up_case_version(case_id) {
            improve_case_version(case_id).then(res => {
                this.test_case_form.id = res.data.result.id
                this.test_case_form.case_version = res.data.result.version
            })
        },
        transfer_req_data_to_display_data() {
            const one_test_case_promise = new Promise((resolve, reject) => {
                get_one_test_case(this.test_case_id)
                    .then(res => {
                        this.test_case_form = res.data.result
                        resolve()
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
            const three_list_promise = new Promise((resolve, reject) => {
                get_three_list(this.module_id)
                    .then(res => {
                        this.three_list = res.data

                        resolve()
                    })
                    .catch(err => {
                        reject(err)
                    })
            })

            Promise.all([one_test_case_promise, three_list_promise])
                .then(() => {
                    for (let item of this.test_case_form.field_value_list) {
                        for (let field_item of this.three_list.field_list) {
                            if (item.field_id == field_item.id) {
                                field_item.field_value = JSON.parse(JSON.stringify(item.field_value))
                            }
                        }
                    }
                })
                .catch(err => {
                    console.log(err)
                })
        },
        link_to_diff() {
            this.$router.push({ path: '/testCase/diff', query: { params: this.$store.getters.test_case_id } })
        }
    }
}
</script>
<style lang="scss" scoped>
// .test-case-content {
//     overflow: hidden;
//     height: 100%;
//     overflow-y: scroll;
//     padding-right: 36px;
// }
.fl {
    float: left;
}
.fr {
    float: right;
}
.clearfix:after {
    content: '.'; /*加一段内容*/
    display: block; /*让生成的元素以块级元素显示，占满剩余空间*/
    height: 0; /*避免生成的内容破坏原有布局高度*/
    clear: both; /*清除浮动*/
    visibility: hidden; /*让生成的内容不可见*/
}
.clearfix {
    zoom: 1; /*为IE6，7的兼容性设置*/
}
.table-box-left {
    width: 98.5%;
    margin-left: 1.5%;
}
.title-h2 {
    font-size: 22px;
}
.title-h3,
.right-title {
    font-size: 18px;
    font-weight: 500;
    height: 25px;
    line-height: 25px;
    background: #6bcca0;
    padding-left: 10px;
    color: #fff;
}
.title-h4 {
    font-size: 16px;
    font-weight: 500;
    padding-top: 10px;
    border-top: 1px solid #ccc;
}
.right-view {
    width: 15%;
    height: 100%;
    position: relative;
}
.left-view {
    width: 100%;
    border-right: 3px solid rgba(228, 245, 237, 0.5);
}
.title {
    // margin-top: 20px;
    background: #f9f9f9;
    padding-left: 10px;
}
.title,
.Asta,
.Block,
.Class,
.IF,
.Usecase {
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: 1px solid #a7aaad;
    background: #f5fafc;
}
.message {
    margin-left: 20px;
    text-align: center;
    padding: 20px;
    font-size: 14px;
    color: #5e6d82;
    border: 1px solid #ebeef5;
    margin-top: 10px;
}
.title-detail {
    font-size: 12px;
    color: #5e6d82;
    text-align: left;
    height: 20px;
    line-height: 20px;
}
.title-content {
    display: block;
    margin-top: 10px;
    margin-left: 20px;
}
.left-content {
    font-size: 14px;
}
.append-span {
    /*display: block;*/
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
}
.table-box {
    margin-top: 10px;
}
.img-box,
.content-size {
    margin-left: 20px;
    margin-top: 10px;
}
.img-box img {
    display: block;
    max-width: 98%;
    cursor: pointer;
}
.img_width_msg {
    width: 98%;
}
.dialogimg {
    display: block;
    margin: 0 auto;
}
.content-size {
    margin-top: 10px;
    color: #000;
    font-size: 14px;
    line-height: 30px;
    text-align: left;
}
.Usecase-detail-box,
.intput-box,
.scene,
.scene_ul,
.Squence,
.Resource,
.Consider,
.Statemachine,
.DRBFM,
.usecase-common-pic-box {
    margin-left: 20px;
    margin-top: 10px;
}
.scene_ul {
    list-style: none;
    clear: both;
}
.scene_ul li {
    width: 33%;
    height: 32px;
    line-height: 32px;
    float: left;
}
.right-view-box {
    padding-top: 20px;
    position: fixed;
    width: 99%;
    height: 92%;
    overflow-y: scroll;
}
.right_ul {
    margin-top: 10px;
    margin-left: 20px;
    list-style: none;
    font-size: 14px;
}
.right-ul-list,
.right-ul-list-child {
    margin-left: 20px;
    font-size: 14px;
    list-style-type: none;
}
/*.right-ul-list,
.right-ul-list-child li {
    margin-top: 5px;
}*/
.right-size-title,
.right-size-title-child {
    font-size: 14px;
    padding-left: 5px;
}
.right_ul li {
    /*margin-top: 5px;*/
    /*height: 26px;*/
    line-height: 26px;
    cursor: pointer;
}
.right-size-title,
.right-size-title-child {
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear;
}
.right_ul li .right-size-title:hover {
    background: #6bcca0;
}
.right-ul-list-child li .right-size-title-child:hover {
    background: #6bcca0;
}
.dialog-title span {
    font-size: 20px;
    margin-right: 20px;
    cursor: pointer;
    color: #42b983;
}
.dialogimg2 {
    display: block;
    position: relative;
    left: 4000px;
}

.el-button--mini,
.el-button--mini.is-round {
    padding: 0px 0px;
}
.statediv {
    margin-top: 2px;
    margin-right: 10px;
}
.stateSelect {
    width: 200px;
}
.table-span {
    display: block;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    -o-text-overflow: ellipsis;
}
@media screen and (max-width: 1420px) {
    .table-span {
        width: 350px;
    }
}
@media screen and (max-width: 1200px) {
    .table-span {
        width: 250px;
    }
}
@media screen and (max-width: 1330px) {
    .img-box img {
        display: block;
        max-width: 98%;
    }
}
@media screen and (max-width: 1024px) {
    .img-box img {
        display: block;
        max-width: 98%;
    }
    .right-ul-list,
    .right-ul-list-child {
        margin-left: 15px;
        font-size: 14px;
        list-style-type: none;
    }
    .right_ul {
        margin-left: 0px;
    }

    .right-size-title,
    .right-size-title-child {
        padding-left: 0;
    }
}
.drbfm-table {
    overflow-x: auto;
}
.dialog-title {
    height: 30px;
    line-height: 30px;
    width: 170px;
    margin: 0 auto;
}
.right-size-title .el-icon-caret-right {
    color: #c0c4cc;
}
/*prewive*/
.test-case-content .el-input.el-input--suffix .el-input__inner {
    height: 26px;
}
</style>




