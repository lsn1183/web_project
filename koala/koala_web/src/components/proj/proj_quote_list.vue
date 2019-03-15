<template>
    <div class="proj-quote-list" v-loading="loading">
        <div class="container">
            <el-collapse v-model="activeNames" @change="handleChange">
                <el-collapse-item title="项目列表" name="project">
                    <template slot="title">
                        <!-- <i class="el-icon-info" style="padding-left: 50px;"></i> -->
                        <h2 >项目列表
                            <i class="el-icon-plus" @click.stop="refresh" @click='addProject()' style="padding-left: 10px;" ></i>&nbsp;

                            <i :class="projRefreshIcon" @click.stop="refresh('proj')"></i>
                        </h2>
                    </template>
                    <div class="table-wrapper">
                        <div class="table-flex">
                            <el-table :data="projList" style="width: 100%;" :row-class-name="tableRowClassName" size="medium">
                                <el-table-column prop="inside_name" label="项目名" width="180">
                                    <template slot-scope="scope">
                                        <span class="link-type" @click="goProjDetail(scope.row)">{{scope.row.inside_name}}</span>
                                    </template>
                                </el-table-column>

                                <el-table-column prop="proj_type" label="系列名" width="100">
                                </el-table-column>
                                <el-table-column prop="describe" label="描述">
                                </el-table-column>
                                <el-table-column align="center" prop="update_time" label="日期" width="180">
                                </el-table-column>
                                </el-table-column>
                                <el-table-column align="center" label="操作" width="100">
                                    <template slot-scope="scope">
                                        <i class="el-icon-edit" @click="editProj(scope.row)"></i>&nbsp;&nbsp;
                                        <i class="el-icon-message"></i>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </div>
                </el-collapse-item>
                <el-collapse-item title="报价列表" name="quote">
                    <template slot="title">
                        <!-- <i class="el-icon-info" style="padding-left: 50px;"></i> -->
                        <h2>报价列表
                            <!-- <i class="el-icon-plus" style="padding-left: 10px;"></i>&nbsp; -->
                            <i :class="quoteRefreshIcon" @click.stop="refresh('quote')"></i>
                        </h2>
                    </template>
                    <div class="table-wrapper">
                        <div class="table-flex">
                            <el-table :data="quoteList" style="width: 100%;" :row-class-name="tableRowClassName" size="medium">
                                <el-table-column prop="quotation_name" label="报价名称" width="180">
                                    <!-- <template slot-scope="scope">
                                        <span class="link-type">{{scope.row.parent_quotation_name}}</span>
                                    </template> -->
                                </el-table-column>

                                <el-table-column prop="proj_name" label="项目名称" width="100">
                                </el-table-column>
                                <el-table-column prop="quotation_ver" label="报价版本" width="80">
                                </el-table-column>
                                <el-table-column prop="status.status_cn" label="报价状态" width="100">

                                </el-table-column>
                                <el-table-column prop="destribe" label="描述">
                                </el-table-column>
                                <el-table-column prop="count_issue" label="指摘" width="80">
                                </el-table-column>
                                <el-table-column align="center" prop="update_time" label="日期" width="180">
                                </el-table-column>
                                <template v-if="SALES || SGL">
                                    <el-table-column align="center" prop="count_not_assign" label="待分配数" width="80">
                                        <template slot-scope="scope">
                                            <el-button v-if="scope.row.check_status_flag" :disabled="!scope.row.checkout_flag" type='text' @click="assignHourMan(scope.row.proj_id, scope.row.quotation_id)">{{scope.row.count_not_assign}}</el-button>
                                            <el-button v-else type='text' @click="assignHourMan(scope.row.proj_id, scope.row.quotation_id)">{{scope.row.count_not_assign}}</el-button>

                                        </template>
                                    </el-table-column>
                                </template>
                                <template v-if="SGL">
                                    <el-table-column align="center" prop="count_not_confirm" label="待确认数" width="80">
                                        <template slot-scope="scope">
                                            <el-button  v-if="scope.row.check_status_flag" type='text' :disabled="!scope.row.checkout_flag">{{scope.row.count_not_confirm}}</el-button>
                                            <a v-else  :href="'cell.html?quotationId=' + scope.row.quotation_id + '&projId=' + scope.row.proj_id" target="_blank" rel="noopener noreferrer">
                                                <el-button type='text' >{{scope.row.count_not_confirm}}</el-button>
                                            </a>
                                        </template>
                                    </el-table-column>
                                </template>
                                <template v-if="GL">
                                    <el-table-column align="center" prop="count_not_quotation" label="待报价数" width="80">
                                        <template slot-scope="scope">
                                            <el-button  v-if="scope.row.check_status_flag" type='text' :disabled="!scope.row.checkout_flag">{{scope.row.count_not_quotation}}</el-button>

                                            <a v-else :href="'cell.html?quotationId=' + scope.row.quotation_id + '&projId=' + scope.row.proj_id" target="_blank" rel="noopener noreferrer">
                                                <el-button type='text'>{{scope.row.count_not_quotation}}</el-button>
                                            </a>
                                        </template>
                                    </el-table-column>
                                </template>
                                <template v-if="SALES">
                                    <el-table-column align="center" prop="count_not_admit" label="工数汇总" width="100">
                                        <template slot-scope="scope">
                                            <el-button type='text' @click='goSummaryAccount(scope.row.quotation_id)'>工数汇总</el-button>
                                        </template>
                                    </el-table-column>
                                </template>
                               
                                
                            </el-table>
                        </div>
                    </div>
                </el-collapse-item>
            </el-collapse>
        </div>
    </div>
</template>
<script>
import { getProjList, getQuoteList } from '@/api/content_api'
import IP from '@/axios_config/ip_address'
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
            quoteList: [],
            loading:false
        }
    },
    created() {
        let cookie = this.$cookies.get('role')
        this.SALES = false;
        this.SGL = false;
        this.GL = false;
        if (cookie.indexOf('SALES') > -1){
            this.SALES = true;
        }else if (cookie.indexOf('SGL') > -1){
            this.SGL = true
        }else{
            this.GL = true;
        }
        this.reqProjQuote()
        
    },
    methods: {
        reqProjQuote() {
            const userId = this.$cookies.get('userId')
            const getProjPromise = new Promise((resolve, reject) => {
                getProjList(userId).then(res => {
                    resolve(res.data.content)
                })
            })

            const getQuotePromise = new Promise((resolve, reject) => {
                getQuoteList(userId).then(res => {
                    resolve(res.data.content)
                })
            })
            this.loading = true
            Promise.all([getProjPromise, getQuotePromise]).then(res => {
                this.projList = res[0]
                for (let i = 0; i < res[1].length; i++) {
                    const element = res[1][i];
                    element.check_status_flag = false
                    if (element.status.status_cn == "新建" ) {
                        if (this.$cookies.get("role").indexOf("SALES")==-1) {
                            element.check_status_flag = true //如果是新建状态，并且当前登录人不是SALES的话，禁止点击
                        }else{
                            element.check_status_flag = false
                        }
                    }
                }
                // console.log("res",res[1])
                this.quoteList = res[1]
                this.loading = false
            })
        },
        reqProjList() {
            this.projRefreshIcon = 'el-icon-loading'
            const userId = window.sessionStorage.getItem('login_user')
            getProjList(userId).then(res => {
                this.projList = res.data.content
                this.projRefreshIcon = 'el-icon-refresh'
            })
        },
        reqQuoteList() {
            this.quoteRefreshIcon = 'el-icon-loading'
            const userId = window.sessionStorage.getItem('login_user')
            getQuoteList(userId).then(res => {
                this.quoteList = res.data.content
                this.quoteRefreshIcon = 'el-icon-refresh'
                // console.log(res.data.content, '8888888888')
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
            // if (rowIndex % 2 === 1) {
            //     return 'warning-row'
            // } else {
            //     // return 'success-row'
            // }
            return 'row-type'
        },
        goProjDetail(row) {
            this.$router.push({ path: '/proj/pro_detail/' + row.proj_id })
        },
        editProj(row) {
            this.$router.push({ path: '/proj/add_project/' + row.proj_id })
        },
        addProject() {
            this.$router.push('/proj/addProject_c')
        },
        goSummaryAccount(quotationId) {
            let routeData = this.$router.resolve({
                name: 'summaryAccount',
                query: { quotation_id: quotationId }
            })
            window.open(routeData.href, '_blank')
        },
        addProject() {
            this.$router.push('/proj/add_project_c')
        },
        assignHourMan(projId, quoteId) {
		    this.$router.push({path:'/featurePage/FeatureList',query:{'quotation_id':quoteId,'proj_id':projId}})
        }
    }
}
</script>
<style scoped>
.proj-quote-list {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: scroll;
    background: #f0f0f0;
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