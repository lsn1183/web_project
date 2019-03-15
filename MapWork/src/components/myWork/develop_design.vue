<template>
    <div class="wrapper">
        <div class="wrapper-content">
            <div class="wrapper-content-header">
                <span>项目名称&nbsp;&nbsp;&nbsp;&nbsp;</span>
                <el-select v-model="proj_id" filterable placeholder="请选择项目">
                    <el-option v-for="item in project_list" :key="item.proj_id" :label="item.proj_name" :value="item.proj_id">
                    </el-option>
                </el-select>
                <span>&nbsp;&nbsp;&nbsp;&nbsp;</span>
                <el-radio-group v-model="radio">
                    <el-radio label="ALL">全显示</el-radio>
                    <el-radio label="PART">只显示有设计书</el-radio>
                </el-radio-group>
            </div>
            <el-table :data="model_list" style="width: 100%" stripe border v-loading="loading">
                <el-table-column :label="item.name" v-for="(item, index) of dynamic_list" align="left" header-align="center" :key="item.field">
                    <template slot-scope="scope">
                        <span>{{scope.row[item.field].title}}</span>
                    </template>
                </el-table-column>
                <el-table-column :label="item.name" v-for="(item, index) of basic_list" align="center" :key="item.field">
                    <template slot-scope="scope">
                        <span :class="{'to-do-span': scope.row[item.field].title != '-'}" @click="goPreview(scope.row[scope.row.sub_level].id, scope.row[item.field].title, scope.row[item.field].id, item.field, item.name)">{{scope.row[item.field].title}}</span>
                    </template>
                </el-table-column>
                <!-- <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <span class="to-do-span">编辑</span>
                    </template>
                </el-table-column> -->
            </el-table>
        </div>
    </div>
</template>
<script>
export default {
    name: 'DevelopDesign',
    created() {
        this.$axios.get(this.Ip + '/Project').then(res => {
                if (res.data.result == 'OK') {
                    this.project_list = res.data.content
                    this.proj_id = this.project_list[0].proj_id
                } else {
                    if (res.data.error == '') {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '您暂无项目。'
                        })
                    } else {
                        // do nothing
                    }
                }
            })
            .catch(err => {
                this.$message({
                    type: 'error',
                    showClose: true,
                    message: '服务异常'
                })
            })
    },
    mounted() {},
    watch: {
        proj_id(proj_id_val) {
            this.get_proj_dev_design(proj_id_val, this.radio)
        },
        radio(radio_val) {
            this.get_proj_dev_design(this.proj_id, radio_val)
        }
    },
    data() {
        return {
            proj_id: null,
            project_list: [],
            model_list: [],
            dynamic_list: [],
            basic_list: [],
            loading: false,
            radio: 'ALL',
            dialogVisible: true
        }
    },
    methods: {
        goPreview(model_id, title, doc_id, doc_type, col_name) {
            const name = col_name
            window.sessionStorage.setItem('docType', doc_type)
            sessionStorage.setItem('proj_id',this.proj_id)
            let datas = {
                "proj_id": this.proj_id,
                "model_id": model_id,
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '设计书_查看') == true) {
                        
                        if(!(doc_type == 'basic_design' || doc_type == 'detail_design' || doc_type == 'IF_stylebook')) {
                            return
                        }
                        if (title == 'TODO') {
                            this.$confirm('是否创建' + name + '文档?', '提示', {
                                confirmButtonText: '确定',
                                cancelButtonText: '取消',
                                type: 'warning'
                            }).then(() => {
                                const data = {
                                    proj_id: this.proj_id,
                                    model_id: model_id,
                                    doc_type: doc_type,
                                    commit_user: window.sessionStorage.getItem('Uall')
                                }

                                this.$axios
                                    .post(this.Ip + '/NewDSDoc', data)
                                    .then(res => {
                                        window.sessionStorage.setItem('docId', res.data.content)
                                        if (doc_type == 'IF_stylebook') {
                                            this.$router.push({ path: '/tagl/Edit_IF/' + res.data.content + '/' + doc_type})
                                        } else if (doc_type == 'basic_design' || doc_type == 'detail_design'){
                                            this.$router.push({ path: '/tagl/File_design/Preview/' + res.data.content + '/' + doc_type})
                                        } else {
                                            // continue code
                                        }
                                    })
                                    .catch(err => {
                                        this.$message({
                                            type: 'error',
                                            showClose: true,
                                            message: '服务异常'
                                        })
                                    })
                            })
                        } else if (title == '-') {
                            // do nothing
                        } else {
                            window.sessionStorage.setItem('docId', doc_id)
                            if (doc_type == 'IF_stylebook') {
                                this.$router.push({ path: '/tagl/Edit_IF/' + doc_id + '/' + doc_type})
                            } else if (doc_type == 'basic_design' || doc_type == 'detail_design') {
                                this.$router.push({ path: '/tagl/File_design/Preview/' + doc_id + '/' + doc_type})
                            } else {
                                // continue code
                            }
                        }

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

            
        },
        get_proj_dev_design(proj_id, type) {
            this.model_list = []
            this.dynamic_list = []
            this.basic_list = []
            this.loading = true
            this.$axios.get(this.Ip + '/DesignTop/' + proj_id + '/' + type).then(res => {
                this.model_list = res.data.content.model_list
                this.dynamic_list = res.data.content.dynamic_list
                this.basic_list = res.data.content.basic_list
                this.loading = false
            })
        }
    }
}
</script>
<style scoped>
.wrapper {
    width: 100%;
    height: 100%;
    min-width: 1024px;
    color: #606266;
    overflow: scroll;
}
.wrapper-content {
    margin: 0 100px;
}
.wrapper-content-header {
    height: 60px;
    padding: 10px 0;
}
.to-do-span {
    cursor: pointer;
}
.to-do-span:hover {
    color: #42b983;
}
</style>