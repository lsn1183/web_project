<template>
	<div id='USERs'>
		<!-- 左边标题 -->
		<div class="left_menu left_menu_ex fl">
			<div>
				<ul>
					<li :class="{'active': hl==1}"  @click='VIP()' >迁入状态</li>
				</ul>
			</div>
		</div>
		<!-- 右边内容 -->				
		<div class="right">
			<div class="sumbit_table sumbit_tabke_ex">
				<el-table :data="tableData"
					border
					style="width: 100%;height: 90%;max-height:800;overflow-y: scroll;"
					>
					<el-table-column
						type="index"
						label="序号"
						width="65"
						>
					</el-table-column>
					
					<el-table-column
						prop="dev_major_category"
						label="大分类"
						>
						<template scope="scope">
							<!--<el-input v-model="scope.row.dev_major_category" ></el-input>-->
							<el-select v-model="scope.row.category" placeholder="请选择大分类" >
		     						<el-option v-for="item in array_detail" :key="item.value" :label="item.value" :value="item.value"></el-option>
		     					</el-select>
						</template>
					</el-table-column>
					
					<el-table-column
						prop="status"
						label="小分类"
						>
						<template scope="scope">
							<el-input v-model="scope.row.status" ></el-input>
						</template>
					</el-table-column>
					
				</el-table>
				<el-button @click="req_eidt_dev_status()" type="primary" style="float: right;margin:10px 0;">提交修改</el-button>
			</div>
		 	<div class="table table_ex" v-show="G_flag == true">
		 		<!-- 新增开发状态 -->
		 		<h3 style="padding-left: 60px;padding-bottom: 10px;">新增迁入状态</h3>
		 		<el-form :model="dynamicValidateForm[0]" ref="dynamicValidateForm" label-width="80px" class="demo-dynamic">
		 			<div style="overflow-y: scroll;max-height: 500px;margin-bottom: 5px;">
		 				<el-form-item
			 				prop="category"
			 				label="大分类"
			 				:rules="{
			 						required: true,message: '内容不能为空',trigger:'blur'
			 					}"
			 				>
			 				<el-select v-model="dynamicValidateForm[0].category" placeholder="请选择大分类" style="width: 235px;">
	     						<el-option v-for="item in array_detail" :key="item.value" :label="item.value" :value="item.value"></el-option>
	     					</el-select>
			 			</el-form-item>
		 				
		 				<el-form-item
			 				prop="status"
			 				label="小分类"
			 				:rules="{
			 						required: true,message: '内容不能为空',trigger:'blur'
			 					}"
			 				>
			 				<el-input v-model="dynamicValidateForm[0].status" placeholder="请选择小分类"></el-input>
			 			</el-form-item>
			 			
		 			</div>
		 			
		 			<el-form-item>
		 				<el-button type="primary" @click="submitForm('dynamicValidateForm')">提交</el-button>
<!-- 		 				<el-button @click="addDomain">新增详细选项</el-button> -->
		 				<el-button @click="resetForm('dynamicValidateForm')">重置</el-button>
		 			</el-form-item>
		 			
		 		</el-form>
			</div>

		</div>
	</div>
</template>

<script>
	export default {
		name: 'User',
		data(){
			
			return {
				boolean_edit_flag:true,
				array_detail:[
					{
						value:'完成',
						label:'完成',
					},
					{
						value:'QA',
						label:'QA',
					},
					{
						value:'未完成',
						label:'未完成',
					},
				],
				tableData:[],
				tableData_copy:[],
				dynamicValidateForm: [{
					status:'',
					category:'',
					dev_major_category:'',
					detail:[
						{
							dev_major_category:''
						}
					],
				}],
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
				empty_flag:false
      		}
		},
		watch:{
			
		},
		mounted:function() {
			this.get_HmiDevStatus();
//			const that = this;
//			window.onresize = function temp() {
//				that.innerHeight = window.innerHeight
//			}
	   },
		methods:{
			add_detail(item){
				for(let i=0;i<this.tableData.length;i++){
					if(this.tableData[i].status_id == item.status_id){
						this.tableData[i].detail.push('')
					}else{
						
					}
				}
			},
			del_detail(item,index){
				this.$confirm('此操作将删除数据，是否继续?','提示',{
			    		confirmButtonText:"确定",
			    		cancelButtonText:"取消",
			    		type:"warning"
			    		
			    }).then(() => {
			    	for(let i=0;i<this.tableData.length;i++){
						if(this.tableData[i].status_id == item.status_id){
							this.tableData[i].detail.splice(index,1)
						}else{
							
						}
					}
			    }).catch(() => {
			    	
			    })
				
			},
			eidt_dev_status(){
				this.boolean_edit_flag = true
			},
			req_eidt_dev_status(){
				
				let Array_req_dev_status = []
				for(let i=0;i<this.tableData.length;i++){
					if( JSON.stringify(this.tableData[i]) !=  JSON.stringify(this.tableData_copy[i]) ){
						Array_req_dev_status.push(this.tableData[i])
					}
				}
				for(let j=0;j<this.tableData.length;j++){
					for(let item in this.tableData[j]){
						if(typeof(this.tableData[j][item]) == 'string'){
							if(this.tableData[j][item] ==''){
								this.empty_flag = true
							}
						}else{
//							for(let k=0;k<this.tableData[j][item].length;k++){
//								if(this.tableData[j][item][k]==''){
//									this.empty_flag = true
//								}
//							}
						}
					}
				}
				if(this.empty_flag == true){
					this.empty_flag = false
					alert('提交内容不能为空')
					return
				}
				let data_change = {classify:"screen",status_list:Array_req_dev_status}
				this.$axios.post(this.Ip + '/UpdateDevStatus',data_change)
						.then(res =>{
							console.log(res)
							if(res.data.result =="OK"){
								this.get_HmiDevStatus()
								this.boolean_edit_flag = false
								alert("提交成功")
								this.empty_flag = false
							}else if(res.data.result =="NG"){
								alert("提交失败")
								this.empty_flag = false
							}
							
						})
						.catch(res =>{alert("网络异常");this.empty_flag = false})
			},
			get_HmiDevStatus(){
				this.$axios.get(this.Ip + '/HmiDevStatus/screen')
				.then(res => {
					console.log(res)
					this.tableData = res.data.content
					this.tableData_copy = JSON.parse(JSON.stringify(res.data.content))
				})
				.catch(res =>{})
			},
			submitForm(formName){
				this.$refs[formName].validate( (res) => {
					if(res){
						let Array_add_dev_state = []
						let Array_detail = []
						Array_add_dev_state = this.dynamicValidateForm
						for(let item of this.dynamicValidateForm[0].detail){
							let detail_item = ''
							detail_item = item.dev_major_category
							Array_detail.push(detail_item)
						}
						Array_add_dev_state[0].detail = []
						Array_add_dev_state[0].detail = Array_detail
						let data_add = {classify:"screen",status_list:Array_add_dev_state}
						this.$axios.post(this.Ip + '/AddDevStatus',data_add)
						.then(res =>{
							this.get_HmiDevStatus()
							this.dynamicValidateForm = [{
								status:'',
								category:'',
								dev_major_category:'',
								detail:[
									{
										dev_major_category:''
									}
								],
							}]
							this.$message({
								type:'success',
								message:'提交成功！',
								showClose:true,
								duration:'0',
							})
						})
						.catch(res =>{
							this.$message({
								type:'error',
								message:'网络异常',
								showClose:true,
								duration:'0',
							})
						})
					}else{
						this.$message({
							type:'error',
							message:'提交失败！',
							showClose:true,
							duration:'0',
						})
						return false;
					}
				})
			},
			resetForm(formName){
				this.$refs[formName].resetFields();
			},
			removeDomain(item){
		    	var index = this.dynamicValidateForm[0].detail.indexOf(item)
//				if(index !== -1){
//					if(this.dynamicValidateForm[0].detail.length != 1){
						this.dynamicValidateForm[0].detail.splice(index,1)
//					}else{
//						
//					}
//				}
			},
			// addDomain(){
			// 	this.dynamicValidateForm[0].detail.push({
			// 		dev_major_category:''
			// 	});
			// },
	     	VIP(){
	     		this.hl=1;
	        	this.G_flag =true
	        	this.G_flag2 =false
	        	this.L_flag =false;
	      },
			//取消和dialog的关闭
			cancel_close(){
				this.CreateGroup_Flag = false;
				this.d_handleEdit = false;
				this.handleEdit_role = false;
			},    
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
		height: 100%;
		border-right:solid 1px #dfe6ec;
		margin-top: 20px;
		font-size: large;
		font-weight: bold;
		overflow-x: hidden;
		overflow: scroll;
	}
	.left_menu_ex{
		width: 300px;	
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
	    display: flex;
	 }
	.
	{
		height: 90%;
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
	.table_ex{
		display: inline-block;
		/*float: left;*/
		width: 30%;
		/*height: 500px;*/
		/*overflow-y: scroll;*/
		margin-top: 20px;
	}
	#USERs .right .table .el-input, .el-input__inner{
		width: 235px;
	}
	.sumbit_table {
		margin-top: 20px;
		marginLeft:20px;
		display: inline-block;
	}
	.sumbit_tabke_ex {
		width: 70%;
	}
	@media only screen and (max-width: 1600px) {
		.sumbit_tabke_ex {
			width: 60%;
		}
		.table_ex{
			display: inline-block;
			width: 40%;
			margin-top: 20px;
		}
		.left_menu_ex{
			width: 200px;
		}
		.right{
			position: absolute;
		 	left: 200px;
		 	right: 0;
		 	top: 0;
		 	bottom:22px;
		 	/*overflow: hidden;*/
		    height: 100%;
		    display: flex;
		}
	}
</style>
