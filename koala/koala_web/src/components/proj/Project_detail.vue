<template>
    <div class="Project-content warpper">
        <div class="pro-content">
            <ul class='pro-nav'>
                <div class="menu">
                    <el-breadcrumb separator-class="el-icon-arrow-right">
                        <el-breadcrumb-item>项目列表</el-breadcrumb-item>
                        <el-breadcrumb-item>项目详细</el-breadcrumb-item>
                    </el-breadcrumb>
                </div>
                <li>
                    <span class="cursor" @click='cancel_fun()'>[ 返回 ]</span>
                </li>
                <li>
                    <!-- <span class="cursor" @click="input_list_fun()">[ Input资料 ]</span> -->
                </li>
                <li>
                    <span class="cursor" @click='push_quotation()' v-if="SALES">[ 发起报价 ]</span>
                </li>
                <li>
                    <span class="cursor" @click='push_system_table()' v-if="SALES || SGL">[ 修改体制 ]</span>
                </li>
            </ul>
            <div class="msg-box">
                <ul class="msg-ul">
                    <li>
                        <p class="msg-title">项目名称</p>
                        <p class="msg-content">
                            {{data_json.inside_i_name}}
                        </p>
                    </li>
                    <li>
                        <p class="msg-title">状态</p>
                        <p class="msg-content">
                            {{data_json.proj_i_state}}
                        </p>
                    </li>
                    <li>
                        <p class="msg-title">项目系列</p>
                        <p class="msg-content">
                            {{data_json.proj_i_type}}
                        </p>
                    </li>
                    <li>
                        <p class="msg-title">创建时间</p>
                        <p class="msg-content">
                            {{data_json.commit_time}}
                        </p>
                    </li>
                    <li>
                        <p class="msg-title">修改时间</p>
                        <p class="msg-content">
                            {{data_json.update_time}}
                        </p>
                    </li>
                    <li>
                        <p class="msg-title">描述</p>
                        <p class="msg-content">
                            {{data_json.describe}}
                        </p>
                    </li>
                    <li>
                        <p class="msg-title">报价列表</p>
                    </li>
                    <li>
                        <el-table :data="quotations_list" border style="width: 100%">
                            
                            <el-table-column prop="quotation_name" label="报价名称">
                            </el-table-column>
                            <el-table-column prop="quotation_ver" label="报价版本" width="80">
                            </el-table-column>
                            <el-table-column prop="status" label="报价状态" width="100">
                            </el-table-column>
                            <!-- <el-table-column label="Featurelist" v-if="SALES || SGL">
                                <template slot-scope="scope">
                                    <el-button v-if="SALES" type="text" @click="look_quotation_fun(scope.row.quotation_id)">
                                        查看
                                    </el-button>
                                    <el-button v-else type="text" :disabled="scope.row.check_workers_flag" @click="look_quotation_fun(scope.row.quotation_id)">
                                        查看
                                    </el-button>
                                </template>
                            </el-table-column> -->
                            <el-table-column prop="destribe" label="描述">
                            </el-table-column>
                            <el-table-column prop="create_user" label="创建人">
                            </el-table-column>
                            <el-table-column prop="create_time" label="创建日期">
                            </el-table-column>
                            <el-table-column prop="update_time" label="更新日期">
                            </el-table-column>
                            <!-- <el-table-column label="报价查看">
						    	<template slot-scope="scope">
						    	    
                                    <el-button v-if="SALES" type="text" @click="goSummaryAccount(scope.row.quotation_id)">
						    	    	查看
						    	   	</el-button>
                                    
                                     <a v-else :href="'cell.html?quotationId=' + scope.row.quotation_id + '&projId=' + scope.row.proj_id" target="_blank"
                                      rel="noopener noreferrer">
                                        <el-button type='text' :disabled="scope.row.check_workers_flag">查看</el-button>
                                    </a>
						    	</template>
						    </el-table-column> -->
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
                                        <el-button v-if="scope.row.check_status_flag" type='text' :disabled="!scope.row.checkout_flag">{{scope.row.count_not_confirm}}</el-button>
                                        <a v-else :href="'cell.html?quotationId=' + scope.row.quotation_id + '&projId=' + scope.row.proj_id" target="_blank" rel="noopener noreferrer">
                                            <el-button type='text'>{{scope.row.count_not_confirm}}</el-button>
                                        </a>
                                    </template>
                                </el-table-column>
                            </template>
                            <template v-if="GL">
                                <el-table-column align="center" prop="count_not_quotation" label="待报价数" width="80">
                                    <template slot-scope="scope">
                                        <el-button v-if="scope.row.check_status_flag" type='text' :disabled="!scope.row.checkout_flag">{{scope.row.count_not_quotation}}</el-button>

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

                            <el-table-column label="单次报价构成图">
                                <template slot-scope="scope">
                                    <el-button type="text" @click="look_quotation_pie(scope.row.quotation_id)">
                                        查看
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>
<script>
import { get_project_info, get_quotation_list } from '@/api/content_api'
export default {
    data() {
        return {
            pro_id: '',
            userId: null,
            data_json: [],
            quotations_list: [],
            Sales_SGL: false,
            Sales: false,
            check_workers_flag: false,
            SALES: false,
            SGL: false,
            GL: false,
        }
    },
    mounted() {
        this.pro_id = this.$route.params.pro_id
        this.userId = this.$cookies.get('userId')
        this.get_data()
        this.get_quotation_list_data()
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
    },
    watch: {
        $route(to, from) {
            this.pro_id = this.$route.params.pro_id
        }
    },
    methods: {
        get_data() {
            get_project_info(this.pro_id).then(res => {
                if (res.data.result == 'OK') {
                    this.data_json = res.data.content
                } else {
                    this.$message({
                        type: 'error',
                        message: res.data.content,
                        duration: 0,
                        showClose: true
                    })
                }
            })
        },
        get_quotation_list_data() {
            get_quotation_list(this.pro_id, this.userId).then(res => {
                if (res.data.result == 'OK') {
                    this.quotations_list = res.data.content.map(item => {
                        if (item.status == '新建') {
                            item.check_workers_flag = true
                            return item
                        } else {
                            item.check_workers_flag = false
                            return item
                        }
                    })
                } else {
                    this.$message({
                        type: 'error',
                        message: '服务器异常！'
                    })
                }
            })
        },
        push_quotation() {
            this.$router.push({ path: '/proj/quotation/' + this.pro_id })
        },
        input_list_fun() {
            this.$router.push({ path: '/Input/InputList', query: { proj_id: this.pro_id } })
        },
        look_quotation_fun(id) {
            this.$router.push({ path: '/featurePage/FeatureList', query: { quotation_id: id, proj_id: this.pro_id } })
        },
        cancel_fun() {
            this.$router.push('/proj/projQuoteList')
        },
        push_system_table() {
            this.$router.push({ path: '/system_table/system_table_view/' + this.pro_id })
        },
        look_quotation_pie(quotation_id) {
            this.$router.push({ path: '/proj/quotation_pie/' + quotation_id + '/' + this.pro_id })
        },
        goSummaryAccount(quotationId) {
            let routeData = this.$router.resolve({
                name: 'summaryAccount',
                query: { quotation_id: quotationId }
            })
            window.open(routeData.href, '_blank')
        },
        assignHourMan(projId, quoteId) {
		    this.$router.push({path:'/featurePage/FeatureList',query:{'quotation_id':quoteId,'proj_id':projId}})
        }
    }
}
</script>
<style scoped>
ul,
li {
    list-style: none;
}
.Project-content {
    height: 100%;
}
.pro-content {
    width: 1280px;
    margin: 0 auto;
    height: 100%;
    background: #fff;
    overflow-y: auto;
}

.pro-tree {
    width: 300px;
    border-right: solid 1px #e6e6e6;
}
.table-box,
.add-box {
    width: 95%;
    margin: 20px 0 0 20px;
}
.add-box {
    height: 20px;
    line-height: 20px;
}
.add-box span {
    float: right;
    cursor: pointer;
}
.pro-nav {
    width: 95%;
    height: 40px;
    line-height: 40px;
    padding-top: 20px;
    list-style: none;
    margin-left: 20px;
}
.pro-nav li {
    float: right;
    margin: 0 10px;
}
.msg-box {
    margin-top: 20px;
}
.msg-ul {
    width: 95%;
    margin-left: 20px;
    overflow: hidden;
}
.msg-ul li {
    width: 100%;
    overflow: hidden;
    margin: 20px 0;
}
.msg-title,
.msg-content {
    float: left;
}
.msg-title {
    width: 150px;
    color: #5e6d82;
    font-weight: bold;
}
.msg-content {
    font-size: 14px;
    font-weight: 500;
    color: #5e6d82;
}
</style>
