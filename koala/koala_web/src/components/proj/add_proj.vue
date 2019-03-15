<template>
	<div class="Project-content">
		<div class="pro-content">
			<h2 class="title-size">项目修改</h2>
			<div class="msg-box">
				<div class="detail-box">
					<span>项目系列</span>
					<el-select v-model="value_type" filterable placeholder="请选择">
					    <el-option v-for="item in value_type_options" :key="item.type_id" :label="item.proj_type" :value="item.type_id">
					    </el-option>
					</el-select>
				</div>
				<div class="detail-box">
					<span>项目内部名称</span>
				<!-- 	<el-select v-model="inside_name" filterable  placeholder="请选择">
					    <el-option v-for="item in inside_name_options" :key="item.inside_id" :label="item.inside_name" :value="item.inside_id">
					    </el-option>
					</el-select> -->
					<!-- 
					修改为:
					<el-input v-model="new_inside_name" style='width:217px' placeholder="手动输入"></el-input> -->
					<el-autocomplete
					  popper-class="my-autocomplete"
					  v-model="inside_name"
					  :fetch-suggestions="querySearch"
					  placeholder="请输入内容"  @select="handleSelect">
					  <i
					    class="el-icon-edit el-input__icon"
					    slot="suffix"  @click="handleIconClick">
					  </i>
					  <template slot-scope="{ item }">
					    <div class="name">{{ item.inside_name }}</div>
					    <!-- <span class="addr">{{ item.inside_id }}</span> -->
					  </template>
					</el-autocomplete>
				</div>
				<div class="detail-box">
					<span>项目客户名称</span>
					<el-input v-model="outside_name" placeholder="请输入项目客户名称" class='outside_name_input'></el-input>
				</div>
				<div class="describe-box">
					<p>项目描述</p>
					<el-input type="textarea" :rows="8" placeholder="请输入内容" v-model="describe" class="describe_input">
					</el-input>
				</div>
				<div class="footer">
					<el-button type="primary" class='footer-btn' @click="post_data()">确认</el-button>
					<el-button type="primary" class='footer-btn' @click="logout_pro()">返回</el-button>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
import {new_add_input,get_project_list,get_project_info,get_res_info,get_project_type,get_project_inside,add_project,change_project} from '@/api/content_api'
	export default {
		name: 'proj_list',
		data () {
			return {
				value_type_options: [],
				inside_name_options:[],
				value_type:'',
				inside_name:"",
				outside_name:"",
				describe:"",
				proj_id:'',
				post_flag:true,
				new_inside_name:"",
				state3: ''
			}
		},
		mounted() {
			this.get_value_type()
			this.get_inside_name()
			this.proj_id = this.$route.params.pro_id
            this.get_data()
		},
		watch: {
		    $route(to, from) {
		        this.proj_id = this.$route.params.pro_id
		    }
		},
		methods: {
			get_data(){
				if(this.proj_id!="" && this.proj_id!=null){
                    get_project_info(this.proj_id).then(res=>{
                        if(res.data.result=="OK"){
					    	this.outside_name = res.data.content.outside_name
					    	this.value_type = res.data.content.proj_type
					    	this.describe = res.data.content.describe
					    	this.post_flag = false
					    	for(let item of this.inside_name_options){
					    		if(item.inside_id == res.data.content.inside_name){
					    			this.inside_name = item.inside_name
					    		}

					    	}
					    }
                    })
					
				}
			},
			get_value_type(){
                get_project_type().then(res=>{
                    if(res.data.result=="OK"){
				    	this.value_type_options = res.data.content
				    }
                })
			},
			get_inside_name(){
                get_project_inside().then(res=>{
                    if(res.data.result=="OK"){
				    	this.inside_name_options = res.data.content
				    }
                })
				
			},
			post_data(){
				let data = {
					"outside_name":this.outside_name,
					"proj_type":this.value_type,
					"inside_name":this.inside_name,
					"describe":this.describe,
					"commit_user":window.sessionStorage.getItem('login_user'),
					'new_inside_name':this.new_inside_name
				}
                change_project(this.proj_id,data).then(res=>{
                    if(res.data.result=="OK"){
                		this.$router.push('/proj/projQuoteList')
				    	this.$message({
				    	    type: 'success',
                            message: '修改成功!',
                            duration: 2000,
                            showClose: false
				    	})
				    }else {
                        // this.$message({
                        //     type: 'error',
                        //     message: res.data.error
                        // })
                	}
				})
				
			},
			logout_pro(){
				this.$confirm('是否退出?', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
				}).then(() => {
					this.$router.push('/proj/projQuoteList')
					window.sessionStorage.removeItem('proj_id')
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
			    console.log(ev,'aaa');
			}
		}
	}
</script>
<style scoped>
	.msg-box{
		font-size: 14px;
	}
	.Project-content{
		width: 1280px;
		margin: 0 auto;
		height: 100%;
		overflow-y:scroll;
	}
	.pro-tree,.pro-content{
		/*float: left;*/
		height: 100%;
		background: #fff
	}

	.pro-tree{
		width:300px;
		border-right: solid 1px #e6e6e6;
	}
	.table-box{
		width:95%;
		margin:20px 0 0 20px;
	}
	.title-size{
		color: #5e6d82;
		font-size: 20px;
		padding: 20px 0 0 20px;
	}
	.msg-box{
		width: 800px;
		height: 70%;
		min-height: 540px;
		/*border:1px solid #ebebeb;*/
		border-radius: 3px;
		margin: 30px 0 0 20px;
		transition: .2s;
	}
	.detail-box{
		height: 40px;
		line-height: 40px;
		margin:30px 0 0 20px;
	}
	.detail-box span,.describe-box p{
		color: #5e6d82;
		font-size: 15px;
		margin-right: 20px;
		font-weight: bold;
		display: block;
		float: left;
		width: 96px;
	}
	.outside_name_input{
		width: 400px;
	}
	.describe_input{
		width: 600px;
		margin:0px 0 0 116px;
	}
	.describe-box{
		margin:30px 0 0 20px;
	}
	.footer{
		margin-top: 40px;
		text-align: center;
	}
	.footer-btn{
		width: 100px;
	}
</style>