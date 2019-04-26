<template>
    <div class="Project-content warpper">
        <div class="pro-content">
            <ul class="pro-nav">
                <div class="menu">
                    <el-breadcrumb separator-class="el-icon-arrow-right">
                        <el-breadcrumb-item>项目列表</el-breadcrumb-item>
                        <el-breadcrumb-item>项目详细</el-breadcrumb-item>
                    </el-breadcrumb>
                </div>
                <li>
                    <span @click="cancel_fun()" class="cursor">[ 返回 ]</span>
                </li>
            </ul>
            <div class="msg-box">
                <ul class="msg-ul">
                    <li>
                        <p class="msg-title">项目名称</p>
                        <p class="msg-content">{{data_json.proj_name}}</p>
                    </li>

                    <li>
                        <p class="msg-title">描述</p>
                        <p class="msg-content">{{data_json.describe}}</p>
                    </li>
                    <li>
                        <p class="msg-title">式样书列表</p>
                    </li>
                    <li>
                        <el-table :data="op_list" border style="width: 100%">
                            <el-table-column label="Screen ID" prop="screen_id">
                                <template slot-scope="scope">
                                    <el-button
                                        @click="go_to_excel(scope.row)"
                                        type="text"
                                    >{{scope.row.screen_id}}</el-button>
                                </template>
                            </el-table-column>
                            <el-table-column label="Screen Name" prop="screen_name">
                            </el-table-column>
                            <el-table-column label="Outline" prop="outline"></el-table-column>
                            <el-table-column label="User" prop="update_user"></el-table-column>
                            <el-table-column label="Lock" prop="locked">
                                <template slot-scope="scope">
                                    <span class="img" v-if="scope.row.locked">
                                        <img src="../../../static/img/unlock (2).png" alt="Lock" srcset="">
                                    </span>
                                    <span v-else class="img">
                                        <img src="../../../static/img/unlock (1).png" alt="unlock" srcset="">
                                    </span>
                                </template>
                            </el-table-column>
                        </el-table>
                        <el-pagination
                            :total="total"
                            @current-change="current_change"
                            layout="prev, pager, next"
                            small
                            v-if="total!=0"
                        ></el-pagination>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>
<script>
import { project_detail, get_op_list } from '@/api/api'

export default {
    data() {
        return {
            proj_id: '',
            userId: null,
            data_json: [],
            op_list: [],
            Sales_SGL: false,
            Sales: false,
            check_workers_flag: false,
            SALES: false,
            SGL: false,
            GL: false,
            total: 0,
            page: 1,
            size: 10
        }
    },
    mounted() {
        this.get_data()
    },
    methods: {
        get_data() {
            this.proj_id = this.$route.query.proj_id
            project_detail(this.proj_id).then(res => {
                // console.log(this.proj_id,res,'--',this.proj_id);
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
            }).then(() => {
                this.get_op_list_data()
            })
        },
        get_op_list_data() {
            get_op_list(this.proj_id).then(res => {
                console.log(this.proj_id, res, '--', this.proj_id);
                if (res.data.result == 'OK') {
                    this.op_list = res.data.content
                } else {
                    this.$message({
                        type: 'error',
                        message: '服务器异常！'
                    })
                }
                this.loading = false
            })
        },
        go_to_excel(val) {
            let router = { path: "/item1", query: { screen_gid: val.screen_gid, proj_id: this.proj_id } }
            this.$router.push(router)
        },
        cancel_fun() {
            this.$router.push('/project_list')
        },

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
.cursor {
    cursor: pointer;
    font-size: 14px;
    color: #5e6d82;
}
.img img{
    width: 22px;
}
</style>
