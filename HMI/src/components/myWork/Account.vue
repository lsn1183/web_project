<template>
	<div id='Account'>
		<!-- 左边标题 -->
		<div class="left_menu fl">
		   	<div>
				<li :class="{'active': hl==1}" @click="OnPasswordChange()">密码修改</li>
		   	</div>
		   	<div>
		   		<li :class="{'active': hl==2}" @click="OnEmailChange()">邮箱修改</li>
				
		   	</div>
		</div>
			<!-- 右边内容 -->
		<div class="right">

			<div id="UserManage" v-show="U_falg">
				 	<br>
					<el-row>
						<el-col :span="6" :push="2">
							原密码：<el-input type="password" v-model="form.old_password"></el-input>
						</el-col>						
					</el-row>
					<el-row>
						<el-col :span="6" :push="2">
							新密码：<el-input type="password" v-model="form.new_password"></el-input>
						</el-col>						
					</el-row>
					<el-row>
						<el-col :span="6" :push="2">
							再次输入新密码：<el-input type="password" v-model="re_password"></el-input>
						</el-col>						
					</el-row>
					<br>
					<el-col :span="6" :push="4">
						<el-button @click="PassageChange()" type=primary>修改</el-button>
					</el-col>				 					
			</div>
			<!-- 邮件管理 -->
			<div id="MailManage" v-show="M_falg">
				 	<br>
					
					<el-row>
						<el-col :span="7" :push="2">
							新邮箱：<el-input  v-model="form_mail.new_mail"><template slot="append">@security.suntec.net</template></el-input>

						</el-col>
						<el-col :span="2"></el-col>
					</el-row>
					<el-row>
						<el-col :span="7" :push="2">
							再次输入新邮箱：<el-input  v-model="re_mail"><template slot="append">@security.suntec.net</template></el-input>

						</el-col>
						
					</el-row>
					<br>
					<el-col :span="5" :push="4">
						<el-button @click="EmailChange()" type=primary>修改</el-button>
					</el-col>
				 	
				
			</div>
			
		</div>
	</div>
</template>

<script>
	export default {
		name: 'Account',
		data(){
			return {
				U_falg:true,
				M_falg:false,
				hl:0,
				form:
				{	user_id:0,
					user_name:'',
					old_password:'',
					new_password:'',
				},
				re_password:'',

				form_mail:
				{	user_id:0,
					new_mail:'',
				},
				re_mail:'',
		        
      		};
		},
		create(){
			
		},
		mounted(){
	      this.form.user_id=window.sessionStorage.getItem('admin');
	      this.form.user_name=window.sessionStorage.getItem('Uall');
	      this.form_mail.user_id=window.sessionStorage.getItem('admin');
	      this.form_mail.user_name=window.sessionStorage.getItem('Uall');
	    },
		methods:{
	     	OnPasswordChange(){
	     		this.U_falg = true;
	     		this.M_falg = false;
	     		this.hl=1;
	      	},
	      	OnEmailChange(){
	      		this.M_falg = true;
	      		this.U_falg = false;
	      		this.hl = 2;
	      	},
	      	PassageChange(){

	      		if(this.form.new_password==this.re_password){
	      			this.$axios.post(this.Ip+"/UserContent",this.form).then(res=>{
	      				if(res.data.result=="OK"){
	      					this.$alert("密码修改成功")
	      				}else{
	      					console.log(res)
	      				}
	      			})
	      		}else{
					alert("两次输入的密码不一样")
	      		}

	      	},
	      	EmailChange(){
	      		var user_id = this.form_mail.user_id
	      		var email = this.form_mail.new_mail+"@security.suntec.net"
	      		if(this.form_mail.new_mail==this.re_mail){
	      			this.$axios.get(this.Ip+"/EmailAlter/"+user_id+"/"+email).then(res=>{
	      				if(res.data.result=="OK"){
	      					this.$alert("邮箱修改成功")
	      				}
	      			}).catch(res=>{
	      				this.$alert("修改不成功")
	      			})
	      		}else{
					this.$alert("两次输入的邮箱不一样")
	      		}

	      	},
	    }  	
		
	}
</script>

<style scoped>
	#Account{
		height:100%;
		width:100%;
	}
	.fl{
		float: left;
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
	.active{
		color: #42b983;
		font-weight: bold;
	}
	.left_menu div li{
		list-style: none;
		line-height: 36px;
		cursor: pointer;
	}
	.right{
		position: absolute;
		right: 0;
		left: 300px;
		height: 100%;
	}
	.right .title{
		margin-top: 20px;
		width: 100%;
		height:50px;
		border-bottom:solid 1px #dfe6ec;
		text-align: center;
	}
	.right .title span{

	}
</style>

