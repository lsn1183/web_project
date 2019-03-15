<template>
	<div class="Project-content">
		<div class="pro-content">
			<h2 class="title-size">项目添加</h2>
			<div class="msg-box">
				<div class="detail-box">
					<span><i style="color:red;">*</i>项目系列</span>
					<el-select v-model="value_type" filterable placeholder="请选择" @change='change_proj_type(value_type)'>
					    <el-option v-for="item in value_type_options" :key="item.type_id" :label="item.proj_type" :value="item.type_id">
					    </el-option>
					</el-select>
					<el-input v-model="other_proj_type" style='width:217px' placeholder="手动输入" v-if='value_type_flag'></el-input>
				</div>
				<div class="detail-box">
					<span><i style="color:red;">*</i>项目内部名称</span>
					<el-select v-model="inside_name" filterable  placeholder="请选择" @change='change_inside_name(inside_name)'>
					    <el-option v-for="item in inside_name_options" :key="item.inside_id" :label="item.inside_name" :value="item.inside_id">
					    </el-option>
					</el-select>
					<el-input v-model="other_inside_name" style='width:217px' placeholder="手动输入"  v-if='inside_name_flag' @blur="blur_inside_name(other_inside_name)"></el-input>
					<i style="color:red;" v-if='check_proj_flag'>项目内部名称已存在</i>
				</div>
				<div class="detail-box">
					<span><i style="color:red;">*</i>项目客户名称</span>
					<el-input v-model="outside_name" placeholder="请输入项目客户名称" class='outside_name_input'></el-input>
				</div>
				<!-- 体制表继承 -->
				<div class="detail-box">
					<span>体制表</span>
					<el-select v-model="manage_id_value" filterable placeholder="继承体制表" style='margin-right:10px;'>
					    <el-option v-for="item in manager_list_options" :key="item.manage_id" :label="item.manage_name" :value="item.manage_id">
					    </el-option>
					</el-select>
					<a href="http://192.168.64.128:8081/koala/template/开发体制_template_ver0.1.xlsx" style='margin-right:10px;'>模板下载</a>
					<el-upload ref="upload" :action="upload_api"  :headers="http_header"
					:on-success='up_success' :on-error="up_error" :show-file-list='false' style='width:80px;float:right;margin-right:220px;'>
					    <el-button type="text" @click="upload_click_fun">点击上传</el-button>
					</el-upload>
				</div>
				<div class="describe-box">
					<p><i style="color:red;">*</i>项目描述</p>
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
import {new_add_input,get_project_list,get_project_info,get_res_info,get_project_type,get_project_inside,add_project,change_project,get_manager_list,get_project_check} from '@/api/content_api'
import address from '@/axios_config/ip_address'
	export default {
		name: 'proj_list',
		data () {
			return {
				value_type_options: [],
				inside_name_options:[],
				manager_list_options:[],
				value_type:'',
				inside_name:"",
				outside_name:"",
				manage_id_value:"",
				describe:"",
				proj_id:'',
				post_flag:true,
				other_inside_name:'',
				other_proj_type:'',
				upload_api:address + 'manager/import',
				file_url:'',
				value_type_flag:false,
				inside_name_flag:false,
				check_proj_data:[],
				check_proj_flag:false,
				http_header:{}
			}
		},
		mounted() {
			this.get_value_type()
			this.get_inside_name()
            this.get_manager_name()
			this.proj_id = this.$route.params.pro_id
            this.get_data()
            this.get_check_project()
		},
		computed:{
			watch_flag(){
				return this.other_inside_name
			}
		},
		watch: {
			watch_flag(val){
				this.blur_inside_name(val)
			},
		    $route(to, from) {
		        this.proj_id = this.$route.params.pro_id
		    }
		},
		methods: {
			get_check_project(){
				get_project_check().then(res=>{
					if(res.data.result == 'OK'){
						this.check_proj_data = res.data.content
					}else{
						this.$message({
						    type: 'error',
                            message: res.data.error,
						})
					}
				})
			},
			get_data(){
				if(this.proj_id!="" && this.proj_id!=null){
                    get_project_info(this.proj_id).then(res=>{
                        if(res.data.result=="OK"){
					    	this.outside_name = res.data.content.outside_name
					    	this.value_type = res.data.content.proj_type
					    	this.inside_name = res.data.content.inside_name
					    	this.describe = res.data.content.describe
					    	this.post_flag = false
					    }
                    })
					
				}
			},
			get_value_type(){
                get_project_type().then(res=>{
                    if(res.data.result=="OK"){
				    	this.value_type_options = res.data.content
				    	this.value_type_options.push({'proj_type':'其他','type_id':0
				    })
				    }
                })
			},
			get_inside_name(){
                get_project_inside().then(res=>{
                    if(res.data.result=="OK"){
				    	this.inside_name_options = res.data.content
				    	this.inside_name_options.push({'inside_name':'其他','inside_id':0})
				    }
                })
				
			},
			get_manager_name(){
				get_manager_list().then(res=>{
					if(res.data.result == 'OK'){
						this.manager_list_options = res.data.content
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
					'other_inside_name':this.other_inside_name,
					'other_proj_type':this.other_proj_type,
					'manage_id':this.manage_id_value,
					'file_url':this.file_url
				}
				// data.outside_name != "" && data.proj_type !="" && data.inside_name!="" && data.describe!=""
				if(true){
					if(this.post_flag == true){
                        add_project(data).then(res=>{
                            if(res.data.result=="OK"){
                            	// console.log(res,'data')
                            	this.$message({
                            	    type: 'success',
                                    message: '创建成功!',
                                    duration: 3000,
                                    showClose: false
                            	})
                            	this.$confirm('是否进行报价?', '提示', {
                            		confirmButtonText: '确定',
                            		cancelButtonText: '取消',
                            		type: 'warning'
                            	}).then(() => {
                            		this.$router.push('/proj/quotation/' + res.data.content)
                            	}).catch(() => {
                            		this.$router.push('/proj/projQuoteList')
                            	})
						    }else {
		                        this.$message({
		                            type: 'error',
									message: res.data.error,
									showClose:true
		                        })
	                    	}
						})
					}else{
                        change_project(this.proj_id,data).then(res=>{
                            if(res.data.result=="OK"){
						    	this.$message({
						    	    type: 'success',
                                    message: '修改成功!',
                                    duration: 3000,
                                    showClose: false
						    	})
						    }else {
		                        this.$message({
		                            type: 'error',
									message: res.data.error,
									showClose:true
		                        })
	                    	}
						})
					}
					
				}else{
					this.$alert("内容不可为空!","提示")
				}
				
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
			up_success(response, file, fileList){
			    if (response.result == 'OK') {
			    	this.file_url = response.content.file.file_url
			    	this.manager_list_options.push({
			    		'manage_name':response.content.file.file_name,
			    		'manage_id':0,
			    	})
			    	this.manage_id_value = 0
			        this.$message({
			            type: 'success',
			            message: '添加成功!',
			            duration:0,
			            showClose: true,
			        })
			    }else{
			    	this.up_error("","","",response.error)
			    }
			},
			up_error(err, file, fileList, error){
			    this.$message({
			        type: 'error',
			        message: '添加失败!'+ error,
			        duration:0,
			        showClose: true,
			    })
			},
			change_proj_type(id){
				if(id == 0){
					this.value_type_flag = true
				}else{
					this.value_type_flag = false
				}
			},
			change_inside_name(id){
				this.other_inside_name = ''
				this.check_proj_flag = false
				if(id == 0){
					this.inside_name_flag = true
				}else{
					this.inside_name_flag = false
					for(let item of this.check_proj_data){
						if(item.inside_id == id){
							this.check_proj_flag = true
						}
					}
				}
			},
			blur_inside_name(val){
				for(let item of this.check_proj_data){
					if(val == item.inside_name){
						this.check_proj_flag = true
					}else{
						this.check_proj_flag = false
					}
				}
			},
			upload_click_fun () {
				this.$refs.upload.clearFiles()//清除上传文件列表
			    const token = this.$cookies.get("token")
			    if (token) {
			        this.http_header.Authorization = 'Token ' + token;
			    }
			},
		}
	}
</script>
<style scoped>
	.msg-box{
		font-size: 14px;
	}
	.Project-content{
		height: 100%;
	}
	.pro-tree,.pro-content{
		width: 1280px;
		margin: 0 auto;
		background: #fff;
		height: 100%;
		overflow-y: scroll;
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
		width: 110px;
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