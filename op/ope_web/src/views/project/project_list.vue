<template>
    <div class="proj-quote-list" v-loading.body="loading">
        <div class="container">
            <el-collapse @change="handleChange" v-model="activeNames">
                <el-collapse-item name="project" title="项目列表">
                    <template slot="title">
                        <!-- <i class="el-icon-info" style="padding-left: 50px;"></i> -->
                        <h2>
                            项目列表
                            <i
                                @click="addProject()"
                                class="el-icon-plus"
                                style="padding-left: 10px;"
                            ></i>&nbsp;
                            <i :class="projRefreshIcon" @click.stop="refresh('proj')"></i>
                        </h2>
                    </template>
                    <div class="table-wrapper">
                        <div class="table-flex">
                            <el-table
                                :data="projList"
                                :row-class-name="tableRowClassName"
                                size="medium"
                                style="width: 100%;"
                            >
                                <el-table-column label="项目名" prop="proj_name" width="280">
                                    <template slot-scope="scope">
                                        <span
                                            @click="go_to_proview(scope.row)"
                                            class="link-type"
                                        >{{scope.row.proj_name}}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column label="描述" prop="describe"></el-table-column>
                                <el-table-column
                                    align="center"
                                    label="日期"
                                    prop="update_time"
                                    width="250"
                                ></el-table-column>
                                <el-table-column align="center" label="操作" width="200">
                                    <template slot-scope="scope">
                                        <i
                                            @click="delete_project(scope.row)"
                                            class="el-icon-delete"
                                        ></i>&nbsp;&nbsp;
                                        <i
                                            @click="edit_project(scope.row)"
                                            class="el-icon-edit"
                                        ></i>&nbsp;&nbsp;
                                        <i
                                            @click="go_to_proview(scope.row)"
                                            class="el-icon-d-arrow-right"
                                        ></i>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </div>
                </el-collapse-item>
            </el-collapse>
        </div>
    </div>
</template>
<script>
import { project_list, delete_project } from '@/api/api'
export default {
    name: 'proj_quote_list',
    data() {
        return {
            SALES: false,
            SGL: false,
            GL: false,
            activeNames: ['project', 'quote'],
            projRefreshIcon: 'el-icon-refresh', //el-icon-loading
            quoteRefreshIcon: 'el-icon-refresh', //el-icon-loading
            projList: [],

            loading: false,
            total: 0,
            page: 1,
            size: 10,
            loading2: false
        }
    },
    mounted() {
        // let cookie = this.$cookies.get('role')

        this.reqProjQuote()

    },
    methods: {
        reqProjQuote() {
            this.loading = true
            // const userId = this.$cookies.get('userId')
            project_list().then(res => {
                console.log(res)
                this.projList = res.data.content
                this.loading = false
            })

        },
        addProject() {
            this.$router.push('add_project')
        },
        edit_project(row) {
            this.$router.push({                path: 'add_project', query: {
                    proj_id: row.proj_id, type: "edit"
                }            })
        },
        delete_project(row) {
            this.$confirm('是否删除?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                delete_project(row.proj_id).then(res => {
                    if (res.data.result == "OK") {
                        this.$message({
                            type: 'success',
                            message: "删除成功！"
                        })
                        return res
                    }

                }).then((state) => {
                    if (state) {
                        this.reqProjQuote()

                    }
                })
            }).catch(() => {

            })
        },
        go_to_proview(data) {
            let proj_id = data.proj_id,
                router = { path: "/project_detail", query: { 'proj_id': proj_id } }
            this.$router.push(router)
        },
        get_quotation_fun(userId, page, size) {
            getQuoteList(userId, page, size).then(quotation_list_data => {
                if (quotation_list_data.data.result == 'NG') {
                    throw new Error(res.data.error + 'NG')
                }
                this.quoteList = quotation_list_data.data.content.quotation_list
                this.total = quotation_list_data.data.content.count
                let leng = this.quoteList.length
                for (let i = 0; i < leng; i++) {
                    this.quoteList[i].check_status_flag = false
                    if (this.quoteList[i].status.status_cn == "新建") {
                        if (this.$cookies.get("role").indexOf("SALES") == -1) {
                            this.quoteList[i].check_status_flag = true //如果是新建状态，并且当前登录人不是SALES的话，禁止点击
                        } else {
                            this.quoteList[i].check_status_flag = false
                        }
                    }
                }
                this.loading2 = false
            })
        },
        reqProjList() {
            this.projRefreshIcon = 'el-icon-loading'
            const userId = this.$cookies.get('userId')
            getProjList(userId).then(res => {
                this.projList = res.data.content
                this.projRefreshIcon = 'el-icon-refresh'
            })
        },
        reqQuoteList() {
            this.quoteRefreshIcon = 'el-icon-loading'
            const userId = this.$cookies.get('userId')
            this.loading2 = true
            getQuoteList(userId, this.page, this.size).then(res => {
                this.quoteList = res.data.content.quotation_list
                this.total = res.data.content.count
                this.loading2 = false
                this.quoteRefreshIcon = 'el-icon-refresh'
            })
        },
        handleChange(val) {
        },
        refresh(type) {
            if (type == 'proj') {
                this.reqProjList()
            } else {
                this.reqQuoteList()
            }
        },
        tableRowClassName({ row, rowIndex }) {

            return 'row-type'
        },


        goSummaryAccount(quotationId) {
            let routeData = this.$router.resolve({
                name: 'summaryAccount',
                query: { quotation_id: quotationId }
            })
            window.open(routeData.href, '_blank')
        },

        assignHourMan(projId, quoteId) {
            this.$router.push({ path: '/featurePage/FeatureList', query: { 'quotation_id': quoteId, 'proj_id': projId } })
        },
        current_change(val) {
            const userId = this.$cookies.get('userId')
            this.page = val
            this.loading2 = true
            this.get_quotation_fun(userId, this.page, this.size)
        }
    }
}
</script>
<style scoped>
.proj-quote-list {
    /* width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: scroll;
    background: #f0f0f0; */
}
.container {
    width: 1280px;
    height: 100%;
    margin-left: auto;
    margin-right: auto;
    background: #fff;
}

i {
    cursor: pointer;
}
.link-type:hover {
    color: #337ab7;
    cursor: pointer;
}
.link-type {
    font-weight: bold;
    color: rgb(32, 160, 255);
}
.proj-tag {
    color: #ffffff;
    border-radius: 2px;
    box-shadow: inset 0 -1px 0 rgba(27, 31, 35, 0.12);
    font-size: 12px;
    font-weight: 600;
    height: 20px;
    line-height: 15px;
    padding: 0.15em 4px;
    text-decoration: none;
}
.proj-tag-unreviewed {
    background-color: #7057ff;
}

.proj-tag-submitted {
    background-color: #008672;
}

.proj-tag-point {
    background-color: #d73a4a;
}
.proj-tag-span {
    position: relative;
    line-height: 1.5 !important;
}
h2 {
    padding-left: 20px;
}
.table-wrapper {
    display: flex;
    position: relative;
}
.table-flex {
    flex: 1;
    overflow-x: hidden;
    padding-left: 20px;
}
@media screen and (max-width: 1280px) {
    .container {
        width: 100%;
    }
}
</style>