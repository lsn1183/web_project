<template>
    <div class="Add-File-Title">
        <div class="Add-File-Title-nav">
        </div>
        <div id="Add-File-Title">
            <div class="mid">
                <div class="mid-top">
                    <div class="div-centers">
                        <div class="div-title div-title-ex">
                            <h2>模块关联</h2>
                        </div>
                    </div>
                    <div class="badesign">
                        <div class="header">
                            <span style="display:inline-block;width:50%;" @keyup.enter="search_click(searchValue)">
                                <el-input clearable @clear="clear_click()" v-on:input="clear_click()" size="small" :placeholder=placeholderTitle v-model="searchValue" class="input-with-select">
                                    <el-button slot="append" icon="el-icon-search" @click="search_click(searchValue)"></el-button>
                                </el-input>
                            </span>
                        </div>
                        <el-table :data="ModelList" border :max-height="adaptivePageHeight">
                            <el-table-column prop="model_id" sortable label="模块编号" width='110' align='center' header-align='center'></el-table-column>
                            <el-table-column prop="title" sortable label="模块名称" align='center' header-align='center' min-width='150'>
                                <template slot-scope="scope">
                                    <span class="a_group" :title="title" type="text">{{scope.row.title}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="model_ref" label="关联模块" align='center' header-align='center' min-width='250'>
                                <template slot-scope="scope">
                                    <!-- <el-select multiple filterable remote  reserve-keyword placeholder="请输入模块名称" :remote-method="remoteMethod" :loading="loading">
                                        <el-option v-for="item in opt">

                                        </el-option>
                                    </el-select> -->
                                </template>
                            </el-table-column>
                            <!-- <el-table-column prop="" label="操作" align='center' width=160 header-align='center'>
                                <template slot-scope="scope">
                                    <el-button type='text' class="column-span" @click="editModel(scope.$index, scope.row)">
                                        [ 编辑 ]</el-button>
                                    <el-button type='text' class="column-span" @click="delModel(scope.$index, scope.row)">
                                        [ 删除 ]</el-button>
                                </template>
                            </el-table-column> -->
                        </el-table>
                    </div>
                </div>
                <div class="form-page">
                    <!-- <el-pagination id="list_page" @current-change="listPageChange" :current-page="page" :page-size="page_size" layout="total, prev, pager, next,jumper" :total="page_count"></el-pagination> -->
                </div>
                <div class="min-footer">
                    <div class="div-input" style="text-align: right;width:100%">
                        <el-button @click="save()" type="primary" size="mini">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
                        <el-button @click="cancel()" type="primary" size="mini">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    </div>
                </div>
            </div>
            <div class="footer"></div>

        </div>
    </div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    data() {
        return {
            ModelList: [],
            searchValue: '',
            modelTitleName: '点击查阅模块负责人',
            placeholderTitle: '请输入模块名称或担当',
            page: 1,
            page_size: 50,
            page_count: 0,
            tableType: null,
            adaptivePageHeight: window.innerHeight - 240,
            modelName: '',
            loading: false
        }
    },
    mounted() {
        this.reqModelList()
    },
    computed: {
        fpm_id(val) {
            return this.$store.state.fpm_id
        }
    },
    watch: {
        fpm_id(val) {
            this.reqModelList()
        }
    },
    methods: {
        reqModelList() {
            this.tableType = 'normal'
            window.sessionStorage.getItem('proj_id')
            window.sessionStorage.getItem('proj_name')
            this.$axios
                .get(this.Ip + '/MoldRefModel/' + window.sessionStorage.getItem('proj_id'))
                .then(res => {
                    console.log(res.data.model_list, 'res')
                    this.ModelList = res.data.model_list
                    // if (res.data.result == 'OK') {
                    //     console.log(res.data.content)
                    //     this.ModelList = res.data.model_list
                    //     // this.page_count = res.data.count
                    // } else {
                    //     this.ModelList = []
                    // }
                })
                .catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
            })
        },
        search_click() {
            this.tableType = 'search'
            this.$axios
                .get(this.Ip + '/ModelQuery/' + this.page + '/' + this.page_size + '/' + this.searchValue)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.ModelList = res.data.content
                        this.page_count = res.data.count
                        window.sessionStorage.removeItem('model_id')
                    } else {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '无数据'
                        })
                        this.ModelList = []
                        this.page_count = 0
                    }
                })
                .catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
                })
        },
        clear_click() {
            if (this.searchValue === '') {
                this.reqModelList()
                return
            }
        },
        listPageChange(pageNum) {
            this.page = pageNum
            if (this.tableType == 'search') {
                this.$axios
                    .get(this.Ip + '/ModelQuery/' + this.page + '/' + this.page_size + '/' + this.searchValue)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.ModelList = res.data.content
                            this.page_count = res.data.count
                            window.sessionStorage.removeItem('model_id')
                        } else {
                            this.$message({
                                type: 'error',
                                showClose: true,
                                message: '无数据'
                            })
                        }
                    })
                    .catch(err => {
                        this.$message({
                            type: 'error',
                            message: '服务异常'
                        })
                    })
            } else {
                this.$axios
                    .get(this.Ip + '/Model/' + this.page + '/' + this.page_size)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.ModelList = res.data.content
                            this.page_count = res.data.count
                            window.sessionStorage.removeItem('model_id')
                        } else {
                            this.$message({
                                type: 'error',
                                showClose: true,
                                message: '无数据'
                            })
                        }
                    })
                    .catch(err => {
                        this.$message({
                            type: 'error',
                            message: '服务异常'
                        })
                    })
            }
        },
        cancel() {
            this.$router.push('/tagl/Add_NewProject/ModuleRelationship')
        }
    }
}
</script>

<style scoped>
.Add-File-Title {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}
.Add-File-Title-nav {
    max-width: 300px;
    min-width: 200px;
    width: 15%;
    height: 100%;
    padding: 20px;
    float: left;
    border-right: 1px solid #c0c4cc;
}
.mid {
    width: 80%;
    height: 100%;
    float: left;
    padding-top: 40px;
    border-right: 1px solid #c0c4cc;
    padding-right: 1%;
    /*overflow-y: scroll;*/
    position: relative;
}
.mid-top {
    position: absolute;
    top: 0;
    bottom: 55px;
    width: 100%;
    padding-right: 20px;
}
.footer {
    width: 20%;
    height: 100%;
}
#Add-File-Title {
    float: left;
    margin: 0 auto;
    width: 84%;
    height: 100%;
    padding-left: 1%;
}

.div-centers {
    width: 100%;
    text-align: left;
    margin: 20px 0 0 0;
    padding: 0 0 20px;
}
.div-center {
    width: 100%;
    text-align: left;
    padding: 0 0 20px;
}
.div-center-label {
    margin-left: 10px;
}
.div-center-label:last-child {
    margin: 0;
}
.div-title {
    display: inline-block;
    width: 90px;
    text-align: right;
    margin-right: 20px;
    color: #4d4d4d;
    font-weight: bold;
    font-size: 15px;
}
.div-title-ex {
    margin: 0;
    padding: 0;
    width: 100%;
    text-align: left;
}
h2 {
    font-size: 22px;
    font-weight: 600;
    color: white;
    padding-left: 10px;
    background-color: #6bcca0;
    height: 25px;
    line-height: 25px;
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
.min-footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}
.input-btn {
    text-align: right;
    width: 100%;
}
#Add-File-Title .el-input__inner {
    height: 36px;
    line-height: 36px;
}
.header {
    padding: 20px 0;
    clear: both;
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
    .checked_input_list {
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
    #Add-File-Title {
        float: left;
        width: 80%;
        height: 100%;
    }
}
@media screen and (max-width: 1024px) {
    .Add-File-Title {
        width: 1024px;
    }
    .header {
        padding: 20px 0;
        clear: both;
    }
    #Add-File-Title {
        float: left;
        width: 820px;
        height: 100%;
    }
    .mid {
        width: 635px;
    }
    .div-input {
        display: inline-block;
        width: 380px;
    }
    .checked_input_list {
        margin-left: 20px;
        float: left;
        height: 400px;
    }
}
.badesign {
    position: absolute;
    top: 45px;
    left: 0;
    right: 20px;
    bottom: 0;
}
.form-page {
    position: absolute;
    left: 0;
    right: 200px;
    bottom: 20px;
}
</style>
