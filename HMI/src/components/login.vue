<template>
	<div id="login">
		<div class="content">
			<section class="section">
				<div><img src="../assets/img/Icon/HMI.png" class="log_img" alt="Spider Logo" /></div>
				<p>欢 迎 来 到 HMI 管 理 网 站</p>
			</section>
		</div>
		<header>
			<div class="fl"><span class="hmi_size">HMI</span></div>
			<span class="fr" style="margin-right: 35px;cursor: pointer;" @click="login_popup_show">登录</span>
		</header>
		<div id="popup" v-if="popup_flag == true">
			<div id="popup_close" @click="pop_up_close">
				×
			</div>
			<div class="login_content" v-if="Login_flag">
				<div class="login_fr">
					<div class="big_re">
						<p class="Regist fl" @click="ToLogin" style="border-bottom: 2px solid #42b983;">登录</p>
						<p class="Regist fr" style="color: #999;">注册</p>
					</div>
					<div @keyup.enter="sub()">
						<p class="value_content">
							<el-input v-model="user" placeholder="用户名" @blur="admin_name2(R_user2)" @change="admin_name2(R_user2)"></el-input>
							<p class="login_admin" v-show="admin_flag4 == true">用户名不能为空</p>
						</p>
						<p class="value_content">
							<el-input type="password" v-model="pwd" placeholder="密码" @blur="admin_pwd2(R_pwd2)" @change="admin_pwd2(R_pwd2)"></el-input>
							<p class="login_key2" v-show="pwd_flag5 == true">密码不能为空</p>
							<p class="login_key2" v-show="flag == true">用户名或密码错误</p>
						</p>
					</div>
					<el-button type="primary" @click="sub()" size="midium" style="letter-spacing: 2px;width: 35%;margin-left: 116px;position: absolute;top: 46.5%;">立即登录</el-button>
					<!--</div>-->

				</div>
			</div>
			<!-- 注册页面 -->
			<div class="login_content" v-if="Regist_flag">
				<p class="bitian">*</p>
				<p class="bitian2">*</p>
				<p class="bitian3">*</p>
				<div class="login_fr">
					<div class="big_re">
						<p class="Regist fl" @click="ToLogin" style="color: #999;">登录</p>
						<p class="Regist fr" style="border-bottom: 2px solid #42b983;">注册</p>
					</div>
					<div @keyup.enter="SUB()">
						<p class="value_content">
							<el-input v-model="R_user" placeholder="用户名" @blur="admin_name(R_user)" @change="admin_name(R_user)"></el-input>
							<p class="login_admin" v-show="admin_flag == true">用户名重复</p>
							<p class="login_admin" v-show="admin_flag2 == true">用户名不能为空</p>
							<div class="correct_img2" v-show="correct_img2 == true">
								<img src="../assets/img/reg_icons.png" />
							</div>
						</p>
						<p class="value_content">
							<el-input v-model="R_pwd" type="password" placeholder="输入密码" @blur="admin_pwd(R_pwd)" @focus="admin_pwd(R_pwd)" @change="admin_pwd(R_pwd)"></el-input>
							<p class="login_key2" v-show="pwd_flag4 == true">密码不能为空</p>
							<p class="login_key2" v-show="pwd_flag == true">长度为6-15个字符</p>
							<div class="correct_img" v-show="correct_img == true">
								<img src="../assets/img/reg_icons.png" />
							</div>
						</p>
						<p class="value_content">
							<el-input v-model="REpwd" type="password" placeholder="确认密码" @blur="re_pwd(REpwd)" @change="re_pwd(REpwd)" @focus="re_pwd(REpwd)"></el-input>
							<span class="re_key" v-show="repwd_flag2 == true">密码不能为空</span>
							<span class="re_key" v-show="repwd_flag == true">两次密码不一致</span>
							<div class="correct_img3" v-show="correct_img3 == true">
								<img src="../assets/img/reg_icons.png" />
							</div>
						</p>
						<p class="value_content">
							<el-input v-model="RMail" placeholder="邮箱名">
								<template slot="append">@security.suntec.net</template>
							</el-input>
						</p>
					</div>
					<p class="zhushi" v-show="zhushi_flag == true">*&nbsp;&nbsp;为必填项</p>
					<el-button type="primary" @click="SUB()" size="midium" style="letter-spacing: 2px;width: 35%;margin-left: 116px;position: absolute;top: 76.5%;">立即注册</el-button>
				</div>
			</div>
		</div>
		<footer>Copyright&nbsp;&copy;&nbsp;2017 Suntec</footer>
	</div>

</template>

<script>
	export default {
		name: 'login',
		data() {
			return {
				correct_img: false,
				correct_img2: false,
				correct_img3: false,
				correct_flag: false,
				popup_flag: false,
				repwd_flag: false,
				repwd_flag2: false,
				admin_flag: false,
				admin_flag2: false,
				pwd_flag: false,
				pwd_flag2: false,
				pwd_flag3: false,
				pwd_flag4: false,
				zhushi_flag: true,
				user: '',
				pwd: '',
				msg: '',
				valueup: {
					pwd: '',
					user: ''
				},
				flag: false,
				admin_flag4: false,
				pwd_flag5: false,
				Login_flag: true,
				Regist_flag: false,
				R_user: '',
				R_user2: '',
				R_pwd: '',
				R_pwd2: '',
				Ggroups: [],
				REpwd: '',
				RMail: '',
				usermember: '',
				testCheckData: '1111'
			}
		},
		mounted() {
			this.getGgroups();
			this.getMembers();
			this.$Check.doCheck('HUDef', 'option', this.testCheckData)
		},
		methods: {
			admin_name(name) {
				this.$axios.get(this.Ip + "/AllUsers")
					.then(res => {
						for(var i = 0; i < res.data.content.length; i++) {
							if(this.R_user == "") {
								this.admin_flag = false
								this.admin_flag2 = true
								this.correct_img2 = false
							} else {
								if(name == res.data.content[i].user_name) {
									this.admin_flag = true
									this.admin_flag2 = false
									this.correct_img2 = false
									return
								} else {
									this.admin_flag = false
									this.admin_flag2 = false
									this.correct_img2 = true
								}
								if(this.R_user != '' && this.R_pwd != '' && this.REpwd != '') {
									this.zhushi_flag = false
								} else {
									this.zhushi_flag = true
								}
							}
						}
					})

			},
			admin_name2(R_user2) {
				if(this.user == "") {
					this.admin_flag4 = true;
					this.flag = false;
				} else {
					this.admin_flag4 = false;
					this.flag = false;
				}
			},
			admin_pwd(R_pwd) {
				if(R_pwd == "") {
					//如何密码为空时 ，focus和blur时提示出现
					this.pwd_flag = false
					this.pwd_flag4 = true
					this.correct_img = false
					//				this.correct_flag = false
				} else {

					//密码不为空时，进行判断，以此显示不同的响应状态
					var P_pwd = new RegExp(/^[\s\w]{6,15}$/)
					if(P_pwd.test(R_pwd) == true) {
						this.pwd_flag = false
						this.pwd_flag4 = false
						//	 				this.correct_flag = true
						this.correct_img = true
					} else {
						this.pwd_flag = true
						this.pwd_flag4 = false
						//	 				this.correct_flag = false
						this.correct_img = false
					}

				}
				if(this.R_pwd != '' && this.REpwd != '') {
					if(this.R_pwd == this.REpwd) {
						this.correct_img3 = true
						this.repwd_flag2 = false
						this.repwd_flag = false
					} else {
						this.correct_img3 = false
						this.repwd_flag2 = false
						this.repwd_flag = true
					}
				}

				if(this.R_user != '' && this.R_pwd != '' && this.REpwd != '') {
					this.zhushi_flag = false
				} else {
					this.zhushi_flag = true
				}
			},
			admin_pwd2(R_pwd2) {
				if(this.pwd == "") {
					this.pwd_flag5 = true;
					this.flag = false;
				} else {
					this.pwd_flag5 = false;
					this.flag = false;
				}
			},
			re_pwd(REpwd) {
				if(this.REpwd == "") {
					this.repwd_flag2 = true
					this.repwd_flag = false
					this.correct_img3 = false
				} else {
					if(REpwd == this.R_pwd) {
						this.correct_img3 = true
						this.repwd_flag2 = false
						this.repwd_flag = false
					} else {
						this.correct_img3 = false
						this.repwd_flag2 = false
						this.repwd_flag = true
					}

				}

				if(this.R_user != '' && this.R_pwd != '' && this.REpwd != '') {
					this.zhushi_flag = false
				} else {
					this.zhushi_flag = true
				}
			},
			pop_up_close() {
				this.popup_flag = false
			},
			login_popup_show() {
				this.popup_flag = true
			},
			sub: function() {
				if(this.user && this.pwd != '') {
					this.valueup.pwd = this.pwd;
					this.valueup.user = this.user;
					this.$axios.get(this.Ip + '/login/' + this.valueup.user + '/' + this.valueup.pwd).then(res => {
						if(res.data.result == true) {
							this.flag = false;
							window.localStorage.setItem('WorkTypeStatus','MyARL')
							window.sessionStorage.setItem('admin', res.data.content.user_id)
							window.sessionStorage.setItem('Uall', res.data.content.user_name)
							window.sessionStorage.setItem('workType', 'my')
							this.$router.push('/hmi/list')
						} else {
							this.flag = true;
						}
					})
				}
			},
			//  ToRegist(){
			//    this.Login_flag = false;
			//    this.Regist_flag = true;
			//  },
			ToLogin() {
				this.Login_flag = true;
				this.Regist_flag = false;
			},
			getGgroups() {
				this.$axios.get(this.Ip + "/GroupAllGroups")
					.then(res => {
						this.Ggroups = res.data.content;
					})
			},
			getMembers() {
				this.$axios.get(this.Ip + "/AllUsers")
					.then(res => {
						this.usermember = res.data.content;
					})
			},
			SUB() {
				var user = this.R_user;
				var pwd = this.R_pwd;
				var Rpwd = this.REpwd;
				var email = this.RMail + "@security.suntec.net";
				var P_pwd = new RegExp(/^[\s\w]{6,15}$/)
				if(P_pwd.test(pwd) == true) {
					if(pwd == Rpwd) {
						this.$axios.get(this.Ip + "/register/" + user + "/" + pwd + "/" + email)
							.then(res => {
								if(res.data.result == true) {
									this.$notify({
										type: 'success',
										message: '注册成功'
									});
									//										this.$message.closeAll()
									this.ToLogin();
								} else {
									this.$notify({
										type: 'error',
										message: '注册失败',
										showClose: true,
										duration: '0',
									});
								}
							}).catch(res => {
								this.$notify({
									type: 'error',
									message: '注册失败',
									showClose: true,
									duration: '0',
								});
							})
					}
				} else {
					this.$notify({
						type: 'error',
						message: '注册失败',
						showClose: true,
						duration: '0',
					});
				}

			}

		}
	}
</script>

<style>
	* {
		margin: 0;
		padding: 0
	}
	
	html,
	body {
		font-family: "Dosis", "Source Sans Pro", "Helvetica Neue", Arial, sans-serif;
		font-size: 14px;
	}
	
	a {
		text-decoration: none;
	}
	ul,ol,li{
		list-style: none;
	}
	.fl{
		float: left;
	}
	.fr{
		float: right;
	}
	#login{
		position: absolute;
		width: 100%;
		height: 100%;
	}
	header{
		width: 100%;
		height: 60px;
		position: fixed;
		top: 0;
		left: 0;
		background: #f8fafc;
		box-shadow: 3px 0 5px #dedede;
		-webkit-box-shadow: 3px 0 5px #dedede;
		line-height: 60px;
	}
	header img{
		width: 20%;
		height: 20%;
		vertical-align: middle;
		margin-left: 35px;
		
	}
	header span{
		color: #4d555d;
	}
	footer{
		width: 100%;
		height: 60px;
		position: fixed;
		bottom: 0;
		left: 0;
		background: #f8fafc;
		line-height: 60px;
		color: #93999f;
		font-size: 12px;
		text-align: center;
		box-shadow: -3px 0 5px #dedede;
		-webkit-box-shadow: -3px 0 5px #dedede;
	}
	.content{
		width: 100%;
		height: 100%;
		background: #fff;
		position: fixed;
		top: 60px;
		bottom: 0;
		left: 0;
	}
	.section {
		width: 100%;
		height: 250px;
		position: relative;
		top: 22%;
	}
	.section div img {
		width: 210px;
		height: 210px;
		position: absolute;
		top:-15px;
		left: 50%;
		margin-left: -105px;
	}
	.section p {
		width: 100%;
		height: 24px;
		line-height: 24px;
		text-align: center;
		position: absolute;
		top: 210px;
		color: #2c3e50;
		font-size: 24px;
	}
	
	#popup {
		position: fixed;
		width: 336px;
		min-height: 380px;
		left: 50%;
		top: 46%;
		margin-left: -168px;
		margin-top: -190px;
		/* z-index: 100; */
		background-color: #fff;
		border-radius: 4px;
		-webkit-box-shadow: 2px 1px 9px #ccc;
		box-shadow: 2px 1px 9px #ccc;
	}
	
	#popup_close {
		position: absolute;
		width: 30px;
		height: 30px;
		right: 5px;
		top: 5px;
		color: #999;
		cursor: pointer;
		text-align: center;
		line-height: 30px;
	}
	
	.login_content {
		width: 340px;
		height: 394px;
		margin: 0 auto;
	}
	
	.login_fl {
		width: 350px;
		text-align: center;
		margin-left: -2px;
	}
	
	.logo {
		width: 25%;
	}
	
	.size {
		font-size: 22px;
		color: #20A0FF;
	}
	
	.login_fr {
		margin-top: 10px;
		margin-right: 35px;
	}
	
	.login_key {
		background: #f9f9f9;
		border: 1px solid #ddd;
		box-shadow: 1px 1px 1px #efefef;
		width: 218px;
		height: 70px;
		position: absolute;
		top: 37%;
		left: 96%;
		color: #666;
		font-size: 0.8em;
		list-style: circle;
		padding-top: 5px;
		padding-left: 26px;
		line-height: 20px;
	}
	
	.correct_img {
		position: absolute;
		left: 309px;
		top: 170px;
		width: 13px;
		height: 13px;
	}
	
	.correct_img img {
		width: 13px;
		height: 13px;
	}
	
	.correct_img2 {
		position: absolute;
		left: 309px;
		top: 104px;
		width: 13px;
		height: 13px;
	}
	
	.correct_img2 img {
		width: 13px;
		height: 13px;
	}
	
	.correct_img3 {
		position: absolute;
		left: 309px;
		top: 236px;
		width: 13px;
		height: 13px;
	}
	
	.correct_img3 img {
		width: 13px;
		height: 13px;
	}
	
	.login_key li {
		list-style: circle;
	}
	
	.login_key:before {
		content: '';
		height: 0;
		width: 0;
		position: absolute;
		top: 10px;
		left: -20px;
		border-right: 10px solid #efefef;
		border-left: 10px solid transparent;
		border-top: 10px solid transparent;
		border-bottom: 10px solid transparent;
	}
	
	.re_key {
		width: 218px;
		height: 5px;
		position: absolute;
		top: 63%;
		left: 15%;
		color: #fc4343;
		font-size: 0.8em;
	}
	
	.login_admin {
		width: 218px;
		height: 5px;
		position: absolute;
		top: 32%;
		left: 15%;
		color: #fc4343;
		color: #fc4343\0;
		font-size: 0.8em;
	}
	
	.login_admin2 {
		display: block;
		width: 218px;
		height: 5px;
		position: absolute;
		top: 31%;
		left: 15%;
		color: #fc4343;
		font-size: 0.8em;
	}
	
	.login_admin3 {
		display: block;
		width: 218px;
		height: 5px;
		position: absolute;
		top: 46%;
		left: 15%;
		color: #fc4343;
		font-size: 0.8em;
	}
	
	.login_key2 {
		width: 218px;
		height: 5px;
		position: absolute;
		top: 47.5%;
		left: 15%;
		color: #fc4343;
		font-size: 0.8em;
	}
	
	.login_title {
		font-size: 26px;
		color: rgb(137, 125, 94);
		margin-top: 110px;
	}
	
	.value_content {
		margin-top: 30px;
		margin-left: 40px;
	}
	
	.value_img>img {
		max-width: 100%;
		height: 42px;
	}
	
	.Asa_user {
		border: 0 none;
		height: 25px;
		width: 230px;
		background-color: rgb(211, 207, 196);
		border-bottom: 1px solid rgb(54, 54, 54);
		outline: none;
		font-family: Arial, Helvetica, sans-serif;
		line-height: 10px;
		font-size: 18px;
		margin-left: 10px;
		padding-left: 5px;
		padding-top: 17px;
	}
	input::-webkit-input-placeholder, textarea::-webkit-input-placeholder { 
		font-size: 14px;
	} 
	input:-moz-placeholder, textarea:-moz-placeholder { 
		font-size: 14px;
	} 
	input::-moz-placeholder, textarea::-moz-placeholder { 
		font-size: 14px;
	} 
	input:-ms-input-placeholder, textarea:-ms-input-placeholder { 
		font-size: 14px;
	}
	
	.sub_btn {
		margin: 30px 0 0 52px;
		width: 216px;
		height: 50px;
		line-height: 50px;
		background-color: rgb(204, 164, 59);
		color: #e5e5e5;
		font-size: 18px;
		text-align: center;
		border: 0 none;
		outline: none;
		cursor: pointer;
	}
	
	.hint {
		width: 488px;
		height: 116px;
		background-color: rgba(71, 79, 90, 0.9);
		position: absolute;
		top: 50%;
		left: 50%;
		margin: -58px 0 0 -244px;
		z-index: 6666
	}
	
	.hint_size {
		margin-top: 8px;
		width: 100%;
		text-align: center;
		font-size: 18px;
		color: rgb(204, 164, 59);
	}
	
	.hitn_btn {
		display: block;
		*display: block;
		width: 104px;
		height: 28px;
		margin: 0 auto;
		margin-top: 8px;
		border: 0 none;
		color: #fff;
		background-color: rgb(204, 164, 59);
		outline: none;
		cursor: pointer;
	}
	
	.Regist {
		font-size: 16px;
		width: 50%;
		cursor: pointer;
		color: #42b983;
		padding-bottom: 6px;
		font-weight: bold;
		display: inline-block;
		text-align: center;
	}
	
	.Rselect {
		width: 88%;
		margin: 20px 0 0px 39px;
	}
	select::-webkit-input-placeholder, option::-webkit-input-placeholder{ 
	color: rgb(140,138,133); 
	font-size: 18px;
	} 
	select:-moz-placeholder, option:-moz-placeholder { 
	color: rgb(140,138,133); 
	font-size: 18px;
	} 
	select::-moz-placeholder, option::-moz-placeholder { 
	color: rgb(140,138,133); 
	font-size: 18px;
	} 
	select:-ms-input-placeholder, option:-ms-input-placeholder { 
	color: rgb(140,138,133); 
	font-size: 18px;
	}
	
	.value_content .el-input__inner {
		border: 1px solid #bfcbd9;
	}
	
	.login_fr .el-button {
		width: 35%;
		margin-top: 30px;
		margin-left: 116px;
	}
	
	.big_re {
		width: 80%;
		margin-left: 15%;
		margin-top: 35px;
		height: 30px;
		border-bottom: 1px solid #eee;
	}
	
	.bitian {
		/*color: #999;*/
		color: #fc4343;
		position: absolute;
		top: 25%;
		left: 93%;
	}
	
	.bitian2 {
		/*color: #999;*/
		color: #fc4343;
		position: absolute;
		top: 39.5%;
		left: 93%;
	}
	
	.bitian3 {
		/*color: #999;*/
		color: #fc4343;
		position: absolute;
		top: 55%;
		left: 93%;
	}
	
	.correct {
		color: #5bc92e;
	}
	
	.error {
		color: #fc4343;
	}
	
	.zhushi {
		width: 80%;
		height: 20px;
		text-indent: 1rem;
		line-height: 20px;
		color: #fc4343;
		font-size: 0.8em;
		position: absolute;
		top: 78%;
		left: 35px;
	}
	.hmi_size{
		display: block;
		font-weight: 600;
		font-size: 24px;
		color: #42b983;
		margin-left:30px;
	}
	.log_img{
		display: block;
		border-radius: 50%;
		opacity: .9;
		margin-bottom: 20px;
	}
</style>
