<template>
	<div id='USERs'>
		<!-- 左边标题 -->
		<div class="left_menu fl">
			<div>
				<ul>
					<li :class="{'active': hl==1}"  @click='VIP()' >组别管理</li>
					<li :class="{'active': hl==2}" @click='list()' >人员管理</li>
				</ul>
			</div>
		</div>
		<!-- 右边内容 -->				
		<div class="right">
		 	<div class="table table_ex" v-show="G_flag == true">
		 		<!-- 新建组 -->				
		 		<div class="l_tnav">
			        <el-button type="text" size="small" style="float: right;margin-right: 38px;font-size: 16px;">
			        	<i class="el-icon-plus" @click="CreateGroup_Flag = true"> 新建组</i>
			        </el-button>

		 		</div>
		 		<!--新建组弹框-->
		 		<el-dialog title="新建组" :visible.sync="CreateGroup_Flag" :before-close="cancel_close">
		 			<el-form :model="form">
		 				<el-form-item label="名称 " :label-width="formLabelWidth">
		 					<el-input v-model="form.Group_name" auto-complete="off"></el-input>
		 				</el-form-item>
		 			</el-form>
		 			<div slot="footer" class="dialog-footer">
		 				<el-button type="primary" @click="CreateGroup">确定</el-button>
		 				<el-button @click="cancel_close">取消</el-button>
		 			</div>
		 		</el-dialog>

		 		<!--组别管理-->
		    	<el-table :data="Vgroups" height=:30
		    		 style="width:100%;overflow: auto;height:100%;border: 1px solid #dfe6ec;-webkit-box-shadow: 2px 2px 5px rgba(0,0,0,0.2); box-shadow: 2px 2px 5px rgba(0,0,0,0.2);" border>
			      	<el-table-column type="index" label="No." width="250"></el-table-column>
			      	<el-table-column prop="group_name" label="组名" style="width: 50%;">
			      		<template scope="scope">
			      			<span class="a_group" type="text" @click="mal_group(scope.$index, scope.row)" >{{scope.row.group_name}}</span>
			        	</template>
			    	</el-table-column>
			      	<el-table-column prop="count" label="用户数" style="width: 15%;"></el-table-column>
			      	<el-table-column label="操作" style="width: 15%;">
				    	<template scope="scope" >
				        	<el-button type="text"><i class="el-icon-edit" @click="handleEdit(scope.$index, scope.row)"> 修改</i></el-button>
				        	<el-button type="text"><i class="el-icon-delete" @click="handleDelete(scope.$index, scope.row)"> 删除</i></el-button>
				      	</template>
		      		</el-table-column>
		    	</el-table>
			    <!--编辑指定组名-->
		 		<el-dialog title="编辑组名" :visible.sync="d_handleEdit"	 :before-close="cancel_close">
		 			<el-form :model="form_ed">
		 				<el-form-item label="名称 " :label-width="formLabelWidth">
		 					<el-input v-model="form_ed.Group_name" auto-complete="off"></el-input>
		 				</el-form-item>
		 			</el-form>
		 			<div slot="footer" class="dialog-footer">
		 				<el-button type="primary" @click="handleEdit2()">确定</el-button>
		 				<el-button @click="cancel_close">取消</el-button>
		 			</div>
		 		</el-dialog>
			</div>

			 <!-- 组详细信息 -->
			 	<div class="table" v-show="G_flag2 == true">
			 		<div class="l_tnav">
			 			组&nbsp;<span style="color: #999;">：</span>&nbsp;{{SeeGroup}}
			 		</div>
			    	<el-table :data="GroupMember" height=:30
			    		style="width:48%;margin-top:2%;margin-left:10%;margin-right:5%;margin-bottom:50px;height:85%;float: left;overflow-y: auto;border-bottom:1px solid #dfe6ec;" border>
				      	<el-table-column prop="user_name" label="用户" style="width: 25%;">
				      		<template scope="scope" >
					        	<span><img src="../../assets/img/Icon/user_icon_2.png" class="user_icon"/>{{scope.row.user_name}}</span>
					      	</template>
				      	</el-table-column>
				      	<el-table-column prop="role" label="角色" style="width: 25%;"></el-table-column>
				      	<el-table-column label="操作" style="width: 15%;">
					      	<template scope="scope" >
					        	<el-button type="text"><i class="el-icon-edit" @click="handleEdit_Gpm(scope.$index, scope.row)" v-show="change_role"> 修改</i></el-button>
					          	<el-button type="text"><i class="el-icon-delete" @click="Gp_memberDelete(scope.$index, scope.row)"> 删除</i></el-button>
					      	</template>
			      		</el-table-column>
			    	</el-table>
					<!--编辑详细列表的用户角色-->
			 		<el-dialog title="编辑角色" :visible.sync="handleEdit_role"	:before-close="cancel_close">
			 			<div>
			 				<p class="s_dialog_body_left">角色</p>
							<template>
			 					<el-checkbox-group v-model="RoleList" class="s_dialog_body_right" :indeterminate="false">
			 						<el-checkbox v-for="role_item in Roles" :key="role_item.label" :label="role_item.label" :value="role_item.value" >{{role_item.label}}</el-checkbox>
			 					</el-checkbox-group>
			 				</template>
			 			</div>
			 			<div slot="footer" class="dialog-footer">
			 				<el-button type="primary" @click="handleEdit_Gpm2()">确定</el-button>
			 				<el-button @click="cancel_close">取消</el-button>
			 			</div>
			 		</el-dialog>
			    	<!--新建用户-->
					<div  style="width:22%;margin-top:2%; border-radius: 5px;margin-right:10%;margin-bottom:50px;height: 84%;float: right;border: 1px solid #dfe6ec;">
		 				<p style="line-height: 30px;background: rgb(255, 255, 255);padding: 0px 18px;position: absolute;top: 85px;left: 73%;font-size: 14px;font-weight: bold;">
		 					新建用户
		 				</p>
		 				<el-input type="text"  placeholder="搜索" v-model="input_value" @change="List_search(input_value)" 
		 					style="width: 70%;display: block;margin: 20px 0 20px 40px;text-align: left;letter-spacing: 0.8em;"></el-input>
		 				<!--多选框用户列表-->
		 				<template>
		 					<el-checkbox-group style="width: 80%;margin:  20px 0 0 40px;height: 73%;overflow-y: auto;overflow-x: hidden;" v-model="checkList">
		 						<el-checkbox v-for="Gpmember_item in checkList_group" :key="Gpmember_item.user_id" :label="Gpmember_item" :value="Gpmember_item"
		 							style="width: 100%;margin-left: 0;margin-bottom: 15px;">{{Gpmember_item.user_name }}</el-checkbox>
		 					</el-checkbox-group>
		 				</template>
		 				<el-button @click="Add_Gpmember('checkList')" style="margin: 20px 0 0 40px;" size="small" type="primary">新增</el-button>
		 			</el-form>
			 	</div>
			</div>
			<!-- 人员管理 -->
			<div class="table" v-show="L_flag == true">							
				<el-table :data="members" height=:30
		    		 style="width:100%;overflow: auto;height: 100%;border: 1px solid #dfe6ec;-webkit-box-shadow: 2px 2px 5px rgba(0,0,0,0.2); box-shadow: 2px 2px 5px rgba(0,0,0,0.2);" border>
			      	<el-table-column type="index" label="No." width="250"></el-table-column>
			      	<el-table-column prop="user_name" label="姓名" style="width: 25%;"></el-table-column>
			      	<el-table-column label="操作"  style="width: 15%;">
			      		<template scope="scope" >
			        		<el-button type="text"><i class="el-icon-delete" @click="memberDelete(scope.$index)"> 删除</i></el-button>
			      		</template>
			      	</el-table-column>
			    </el-table>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'User',
		data(){

			return {
	        	edit_index:'',
	        	old_name:'',
				G_flag:true,
				G_flag2:false,
				L_flag:false,
		        hl:1,
			    //修改角色权限
			    change_role:false,
			    mal_group_row:'',
		        //管理员页面的组列表
		        Vgroups: [
		       	{
		       		group_id:1,
		       		group_name:"Admin"
		       	},
		       	{
		       		group_id:2,
		       		group_name:"Data"
		       	},
		       	{
		       		group_id:3,
		       		group_name:"group01"
		       	}
		       	],
		       	//member中的组和所有组
		       	GroupMember:[],
		       	//详细列表传组的id和name
		       	SeeGroup:'',
		       	SeeGname:'',
		       	Gp_row:'',
		       	Gp_index:'',
		       	//分页器默认数据
		       	page_size: 7,
				page_number: 1,
				total:9,
				currentPage:1,
				//组长搜索
				members:[],
			    //新建组
		        CreateGroup_Flag:false,
		        form:{
		        	Group_name:''
		        },
		        //编辑指定组名
		        d_handleEdit:false,
		        form_ed:{
		        	Group_name:''
		        },
		        formLabelWidth:'120px',
		        //编辑用户角色
		        handleEdit_role:false,
				Roles: [
			      	 {
			        	value: '4',
			        	label: 'Leader'
			        }, 
			        {
			          value: '5',
			          label: 'Member'
			        }, 
			        {
			          value: '6',
			          label: 'Translator'
			        }, 
			    ],
			    RoleList:[],
			    Role:{
			    	role:[],
			    	user_id:null,
			    	group_id:null,
			    },
			    role_index:'',
	        	new_role:'',
	        	//多选框
	        	checkList_group:[],
	        	checkList_search:[],
	        	checkList: [],
				//搜索
				input_value:'',
      		}
		},
		mounted:function() {
			this.getVgroups();
	      	this.getmembers();
	   },
		methods:{
	     	VIP(){
	     		this.hl=1;
	        	this.G_flag =true
	        	this.G_flag2 =false
	        	this.L_flag =false;
	        	this.getVgroups();
	        },
	      	list(){
	      		this.getmembers();
	      		this.hl=2;
	      		this.G_flag =false;
	      		this.G_flag2 =false;
	      		this.L_flag = true;
	      	},
	      	getVgroups(){
	      		this.$axios.get(this.Ip+"/GroupAllGroups")
	      		.then(res=>{
	      			this.Vgroups = res.data.content;
	      		})
	      		
	      	},
			getmembers(){
				this.$axios.get(this.Ip+"/AllUsers")
				.then(res=>{
					this.members = res.data.content;
				})
			},
			//新建组
			CreateGroup(){
				if (this.form.Group_name != "") {					
			    	this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG'){
								this.$notify({
									type:'error',
									message:'其他人正在release，请耐心等待!',
									showClose:true,
									duration:'0',
								})
								return;
							}else{
								this.$axios.get(this.Ip+"/GroupAdd/"+this.form.Group_name)
									.then(res=>{
										if(res.data.result=="OK"){
						            		this.$notify({
												type:'success',
												message:'添加成功'
											});
											this.CreateGroup_Flag = false;
											//即时更新
											this.getVgroups();
						               }else{
						                	this.$notify({
												type:'error',
												message:'该组名已被用',
												duration:'0',
												showClose:true,
											}) ;
						                } 
						          })
							}
						})
					
				} else{
		                this.$notify({
						iconClass:'message_icon_info',
						message:'组名不能为空',
					});
				}
				
			},
			//取消和dialog的关闭
			cancel_close(){
				this.CreateGroup_Flag = false;
				this.d_handleEdit = false;
				this.handleEdit_role = false;
			},
			//编辑指定组名
			handleEdit(index, row){
				this.edit_index = index
		        this.old_name = this.Vgroups[index].group_name
				this.d_handleEdit =true;
				this.form_ed.Group_name = this.Vgroups[index].group_name
			},
			handleEdit2(){
				this.new_name = this.form_ed.Group_name
		        if (this.new_name=='') {
		        	this.$notify({
						iconClass:'message_icon_info',
						message:'组名不能为空',
					});
		        } else{
		        	if (this.new_name==this.old_name) {
		        		this.$notify({
							type:'error',
							message:'与原组名重复',
							duration:'0',
							showClose:true,
						}) ;
		        	} else{
		        		this.$axios.get(this.Ip + '/ServiceStatus')
							.then(res => {
								if(res.data.result == 'NG'){
									this.$notify({
										type:'error',
										message:'其他人正在release，请耐心等待!',
										showClose:true,
										duration:'0',
									})
									return;														
								}else{
									this.$axios.get(this.Ip+'/ARLUpdateGroupName/'+this.Vgroups[this.edit_index].group_id+'/'+this.new_name)
				        			.then(res=>{
							            if(res.data.result=="OK"){
							            		this.Vgroups[this.edit_index].group_name = this.new_name;
				        						this.d_handleEdit =false;
							               }else{
							                	this.$notify({
													type:'error',
													message:'该组名已被用',
													duration:'0',
													showClose:true,
												}) ;
							                }
							            })
								}
							})
		        		
		        	}
		        }
		    },
		    //组列表--删除指定组
		    handleDelete(index, row) {
		    	this.$confirm('此操作将永久删除该组，是否继续?','提示',{
		    		confirmButtonText:"确定",
		    		cancelButtonText:"取消",
		    		type:"warning"
		    	}).then(() => {
		    		var id = row.group_id;
		    		this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG'){
								this.$notify({
									type:'error',
									message:'其他人正在release，请耐心等待!',
									showClose:true,
									duration:'0',
								})
								return;
							}else{
								this.$axios.get(this.Ip+"/GroupDelete/"+id)
							        .then(res=>{
						      			//即时更新
							        	this.getVgroups();
						      		})
						    }
							}).catch(() => {
						    })
						})
		    },
		    //点击组名进入到指定组的用户列表
		    mal_group(index, row) {
		    	this.input_value = ''
		    	this.checkList = []
		        this.G_flag =false;
		        this.G_flag2 =true;
		        this.SeeGroup=row.group_name
		        this.SeeGname=row.group_id
		      	this.$axios.get(this.Ip+"/GroupGetMembers/"+row.group_id)
	      		.then(res=>{
	      			this.GroupMember = res.data.rontent;
	      			if (this.GroupMember != undefined) {
	      				if (this.GroupMember.length != 0) {
	      					for(var u=0;u<this.GroupMember.length;u++){
			      				this.GroupMember[u].role = this.GroupMember[u].role.join(',')
			    			}
	      				} else{
	      					
	      				}
	      			} else{
	      				
	      			}
	      			if(row.group_id == 1 || row.group_id == 2){
	      				this.change_role = false;
	      			}else{
	      				this.change_role = true;
	      			}
	      			this.mal_group_row = row
	      		})
	      		//检索--用户列表
	      		this.$axios.get(this.Ip+"/AllUsers")
				.then(res=>{
					this.checkList_group = res.data.content;
					this.checkList_search =res.data.content;
					for(let i=0;i<this.checkList_group.length;i++){
						this.checkList_group[i].group_id = this.SeeGname;
					}
				})
	      		this.Gp_row = row
	      		this.Gp_index = index
	      		
		    },
		    //编辑详细列表的用户角色
		    handleEdit_Gpm(index, row) {
		    	this.role_index = index
		        this.handleEdit_role =true;
		        //解决checkbox数据联动
		        this.RoleList = this.GroupMember[this.role_index].role.split(',')
		    },
		    handleEdit_Gpm2(){
		    	this.Role.user_id = this.GroupMember[this.role_index].user_id
		    	this.Role.group_id = this.SeeGname
		    	this.GroupMember[this.role_index].role =  this.GroupMember[this.role_index].role.split(',')
		    	this.new_role = this.GroupMember[this.role_index].role
		    	this.Role.role = []
				for(var m=0;m<3;m++){
	    			if(this.RoleList[m]=="Leader"){
	    				this.Role.role.push(4)
	    			}else if(this.RoleList[m]=="Member"){
	    				this.Role.role.push(5)
	    			}else if(this.RoleList[m]=="Translator"){
	    				this.Role.role.push(6)
	    			}
    			}
				this.$axios.get(this.Ip + '/ServiceStatus')
					.then(res => {
						if(res.data.result == 'NG'){
							this.$notify({
								type:'error',
								message:'其他人正在release，请耐心等待!',
								showClose:true,
								duration:'0',
							})
							return;														
						}else{
							this.$axios.post(this.Ip+'/GpUpdateRole',this.Role)
			    			.then(res=>{
		        				if (res.data.result=="OK") {
		        					this.GroupMember[this.role_index].role = this.new_role;
									this.$notify({
								    	type:'success',
							    		message:'修改成功'
							    	}) ;
							    	this.handleEdit_role =false;
							    	//即时更新左侧列表
									this.$axios.get(this.Ip+"/GroupGetMembers/"+this.SeeGname)
							      		.then(res=>{
							      			this.GroupMember = res.data.rontent;
							      			if (this.GroupMember != undefined) {
							      				if (this.GroupMember.length != 0) {
							      					for(var u=0;u<this.GroupMember.length;u++){
									      				this.GroupMember[u].role = this.GroupMember[u].role.join(',')
									    			}
							      				} else{
							      					
							      				}
							      			} else{
							      				
							      			}
							      		})
		        				} else{
		        					this.$notify({
								    	type:'error',
							    		message:'修改失败',
							    		duration:'0',
							    		showClose:true,
							    	}) ;
		        				}
							})
						}
					})
		    	
		    },
		    //从组内删除用户
		    Gp_memberDelete(index, row){
		    	this.$confirm('此操作将该用户从组内永久删除，是否继续?','提示',{
		    		confirmButtonText:"确定",
		    		cancelButtonText:"取消",
		    		type:"warning"
		    	}).then(() => {
		    		var SeeGname=this.SeeGname
			    	var	id=this.GroupMember[index].user_id
			    	this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG'){
								this.$notify({
									type:'error',
									message:'其他人正在release，请耐心等待!',
									showClose:true,
									duration:'0',
								})
								return;														
							}else{
								this.$axios.get(this.Ip+"/GpMemberDel/"+SeeGname+"/"+id)
								    .then(res=>{
								    	if(res.data.result="OK"){
											//即时更新左侧列表
											this.$axios.get(this.Ip+"/GroupGetMembers/"+this.SeeGname)
									      		.then(res=>{
									      			this.GroupMember = res.data.rontent;
									      			if (this.GroupMember != undefined) {
									      				if (this.GroupMember.length != 0) {
									      					for(var u=0;u<this.GroupMember.length;u++){
											      				this.GroupMember[u].role = this.GroupMember[u].role.join(',')
											    			}
									      				} else{
									      					
									      				}
									      			} else{
									      				
									      			}
									      		})
								    	}else{
								    	}
								    })
							}
						})
				    
		    	}).catch(() => {
		    	})
		    },
		    //检索框
			List_search(queryString){
				if (this.input_value == '') {
					this.checkList =[]
					this.checkList_group = this.checkList_search
				} else{
					var checkList_search = this.checkList_search
					this.checkList_group= queryString ? this.checkList_search.filter(this.createStateFilter(queryString)): this.checkList_search;
				}
			},
			createStateFilter(queryString){
				return (checkList_search) =>{
					return (checkList_search.user_name.indexOf(queryString.toLowerCase())===0)
				}

			},
			//新增用户到组
			Add_Gpmember(checkList) {
				if(this.checkList.length == 0){
					this.$notify({
						iconClass:'message_icon_info',
						message:'新增用户不能为空',
					});
				}else{
					this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG'){
								this.$notify({
									type:'error',
									message:'其他人正在release，请耐心等待!',
									showClose:true,
									duration:'0',
								})
								return;														
							}else{
								this.$axios.post(this.Ip+"/GpMemberAdd",this.checkList)
					          		.then(res=>{
					          			if(res.data.result=="OK"){
					          				this.$notify({
												type:'success',
												message:'添加成功',
											});
					          				//即时更新左侧列表
											this.$axios.get(this.Ip+"/GroupGetMembers/"+this.SeeGname)
									      		.then(res=>{
									      			this.GroupMember = res.data.rontent;
									      			if (this.GroupMember != undefined) {
									      				if (this.GroupMember.length != 0) {
									      					for(var u=0;u<this.GroupMember.length;u++){
											      				this.GroupMember[u].role = this.GroupMember[u].role.join(',')
											    			}
									      				} else{
									      					
									      				}
									      			} else{
									      				
									      			}
									      			if(this.mal_group_row.group_id == 1 || this.mal_group_row.group_id == 2){
									      				this.change_role = false;
									      			}else{
									      				this.change_role = true;
									      			}
									      			//即时清空搜索框和复选框列表
									      			this.checkList =[]
									      		})
					          			}else if(res.data.result=="REPEAT"){
					          				this.$notify({
					          					iconClass:'message_icon_info',
												message:'请勿重复添加已有组员',
					          				});
					          			}
						      		})
					          		.catch(res=>{
						      			this.$notify({
				          					type:'error',
											message:'添加失败',
											showClose:true,
											duration:'0',
				          				});
						      		})
							}
						})
				}
		      },
		    //成员列表--删除
		    memberDelete(index, row){
		    	this.$confirm('此操作将永久删除该用户，是否继续?','提示',{
		    		confirmButtonText:"确定",
		    		cancelButtonText:"取消",
		    		type:"warning"
		    	}).then(() => {
		    		var	user_id=this.members[index].user_id
		    		this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG'){
								this.$notify({
									type:'error',
									message:'其他人正在release，请耐心等待!',
									showClose:true,
									duration:'0',
								})
								return;														
							}else{
								this.$axios.get(this.Ip+"/UserDel/"+user_id)
								    .then(res=>{
								    	//即时更新
								    	this.getmembers();
								    })
							}
						})
		    	}).catch(() => {
		    	})   
		    }
		}
		
	}
</script>

<style scoped>
	body,html,ul,li{
		margin:0;
		padding:0;
		list-style: none;
	}
	.a_group{
		color: #42b983;
		cursor: pointer;
	}
	#USERs{
		position: relative;
		width: 100%;
		height: 100%;
	}
	.left_menu{
		padding-left: 45px;	
		width: 300px;
		height: 100%;
		border-right:solid 1px #dfe6ec;
		margin-top: 20px;
		font-size: large;
		font-weight: bold;
		overflow-x: hidden;
		overflow: scroll;
	}
	.fl{
		float: left;
	}
	.left_menu div li{
		list-style: none;
		line-height: 36px;
		cursor: pointer;
	}

	.active{
		color: #42b983;
		font-weight: bold;
	}
	.right{
		position: absolute;
	 	left: 300px;
	 	right: 0;
	 	top: 0;
	 	bottom:22px;
	 	/*overflow: hidden;*/
	    height: 100%;
	 }
	.table{
	   	margin-top: 20px;
	   	width: 100%;
	   	height: 95.5%;
	   	border-collapse: collapse;
	}
	.table_ex{
		height: 90%;
	}
	.l_tnav{
		/*border-top-left-radius: 10px;
		border-top-right-radius: 10px;
		overflow: hidden;*/
		line-height: 50px;
		text-indent: 30px;
		/*font-weight: 500;*/
		/*letter-spacing: 4px;*/
		margin-top: 20px;
	    width: 100%;
	    height: 50px;
	    border-bottom: solid 1px #dfe6ec;
	    /*padding-left: 30px;*/
	}
	.transfer{
		float: left;
		top: 50px;
		left: 10px;
	}
	.ipt_hover:before {
	    position: absolute;
	    top: 30%;
	    left: 30%;
	    color: #bfcbd9;
	}
	.right .table>.el-table::before{
		height: 0;
	}
	
	.s_dialog_body_right{
	    line-height: 2;
	}
	p.s_dialog_body_left{
	    float: left;
	    /* width: 120px; */
	    width: 20%;
	    text-align: right;
	    line-height: 2;
	    padding-right: 12px;
	}
	.user_icon{
		width: 16px;
		vertical-align: middle;
	}
</style>
