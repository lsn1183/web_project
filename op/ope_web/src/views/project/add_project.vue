<template>
    <div class="Project-content">
        <div class="pro-content">
            <h2 class="title-size">{{project_type}}</h2>
            <div class="msg-box">
                <!-- <div class="detail-box">
                    <span>项目系列</span>
                    <el-select filterable placeholder="请选择" v-model="value_type">
                        <el-option
                            :key="item.type_id"
                            :label="item.proj_type"
                            :value="item.type_id"
                            v-for="item in value_type_options"
                        ></el-option>
                    </el-select>
                </div> -->
                <div class="detail-box">
                    <span>项目名称</span>
                    <!-- :fetch-suggestions="querySearch"
                        @select="handleSelect" -->
                        <el-input
                            class="outside_name_input"
                            placeholder="请输入项目客户名称"
                            v-model="project_data.proj_name"
                        ></el-input>
                    <!-- <el-autocomplete
                        
                        
                        placeholder="请输入内容"
                        popper-class="my-autocomplete"
                        v-model="project_data.proj_name"
                    > -->
                        <!-- <i
                            @click="handleIconClick"
                            class="el-icon-edit el-input__icon"
                            slot="suffix"
                        ></i>
                        <template slot-scope="{ item }">
                            <div class="name">{{ item.inside_name }}</div>
                        </template> -->
                    </el-autocomplete>
                </div>
                <!-- <div class="detail-box">
                    <span>项目客户名称</span>
                    <el-input
                        class="outside_name_input"
                        placeholder="请输入项目客户名称"
                        v-model="outside_name"
                    ></el-input>
                </div> -->
                <div class="describe-box">
                    <p>项目描述</p>
                    <el-input
                        :rows="8"
                        class="describe_input"
                        placeholder="请输入内容"
                        type="textarea"
                        v-model="project_data.describe"
                    ></el-input>
                </div>
                <div class="footer">
                    <el-button @click="post_data()" class="footer-btn" type="primary">确认</el-button>
                    <el-button @click="logout_pro()" class="footer-btn" type="primary">返回</el-button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { add_project,project_detail,edit_project } from '@/api/api'

export default {
    name: 'add_project',
    data() {
        return {
            project_type:"添加项目",
            project_data:{
                proj_name:"",
                project_describe:"",
                proj_id:""
            },

            value_type_options: [],
            inside_name_options: [],
            value_type: '',
            inside_name: "",
            outside_name: "",
            describe: "",
            proj_id: '',
            post_flag: true,
            new_inside_name: "",
            state3: ''
        }
    },
    mounted() {
        if (this.$route.query.proj_id) {
            this.get_project_detail()
        }
    },
   
    methods: {
        get_project_detail(){
            this.proj_id = this.$route.query.proj_id
            project_detail(this.proj_id).then(res=>{
                this.project_data=res.data.content
                this.project_data.type = "edit"
            })
        },
        post_data() {
            let data = this.project_data
            console.log(data,'a----------');
            if (data.type == 'edit') {
               edit_project(data).then(res=>{
                    console.log(res,'edit')
                    this.$message({
                        type: 'success',
                        message: "修改成功！"
                    })
                })
            }else{
                add_project(data).then(res=>{
                    console.log(res,'aaa');
                    this.$message({
                        type: 'success',
                        message: "添加成功！"
                    })
                })
            }

        },
        get_value_type() {
            get_project_type().then(res => {
                if (res.data.result == "OK") {
                    this.value_type_options = res.data.content
                }
            })
        },
        get_inside_name() {
            get_project_inside().then(res => {
                if (res.data.result == "OK") {
                    this.inside_name_options = res.data.content
                }
            })

        },
       
        logout_pro() {
            this.$confirm('是否退出?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$router.push('/project_list')
            }).catch(() => {

            })
        },
        querySearch(queryString, cb) {
            var restaurants = this.inside_name_options;
            var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
            // 调用 callback 返回建议列表的数据
            cb(results);
        },
        createFilter(queryString) {
            return (restaurant) => {
                return (restaurant.inside_name.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
            };
        },
        handleSelect(item) {
            this.inside_name = item.inside_name
        },
        handleIconClick(ev) {
            console.log(ev, 'aaa');
        }
    }
}
</script>
<style scoped>
.msg-box {
    font-size: 14px;
}
.Project-content {
    width: 1280px;
    margin: 0 auto;
    height: 100%;
    overflow-y: scroll;
}
.pro-tree,
.pro-content {
    /*float: left;*/
    height: 100%;
    background: #fff;
}

.pro-tree {
    width: 300px;
    border-right: solid 1px #e6e6e6;
}
.table-box {
    width: 95%;
    margin: 20px 0 0 20px;
}
.title-size {
    color: #5e6d82;
    font-size: 20px;
    padding: 20px 0 0 20px;
}
.msg-box {
    width: 800px;
    height: 70%;
    min-height: 540px;
    /*border:1px solid #ebebeb;*/
    border-radius: 3px;
    margin: 30px 0 0 20px;
    transition: 0.2s;
}
.detail-box {
    height: 40px;
    line-height: 40px;
    margin: 30px 0 0 20px;
}
.detail-box span,
.describe-box p {
    color: #5e6d82;
    font-size: 15px;
    margin-right: 20px;
    font-weight: bold;
    display: block;
    float: left;
    width: 96px;
}
.outside_name_input {
    width: 400px;
}
.describe_input {
    width: 600px;
    margin: 0px 0 0 116px;
}
.describe-box {
    margin: 30px 0 0 20px;
}
.footer {
    margin-top: 40px;
    text-align: center;
}
.footer-btn {
    width: 100px;
}
</style>