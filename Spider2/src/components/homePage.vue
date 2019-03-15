<template>
	<div id="homepage">
		<!--头部组件-->
		<div id="header">
			<a href="javasript:;">
				<div id="brand"  @click='OnSpider'>
					<img src="../assets/img/Icon/Spider_Icon.png" alt="商标"/>
					<span>Spider</span>
				</div>
			</a>
			<div id="nav">
				<el-menu :default-active="activeIndex2" class="el-menu-demo header_li" mode="horizontal" >
					<el-submenu index="1">
				    	<template slot="title">要求式样管理</template>
				    	<!--<el-menu-item index="1-1" @click='OnMyARL'  :class="szPointer =='MyARL'?'el-icon-caret-right':''">我的要求式样</el-menu-item>-->
				    	<el-menu-item index="1-1" @click='OnAllARL' id="first_arl" :class="szPointer =='AllARL'?'el-icon-caret-right':''">全体要求式样</el-menu-item>
				    	<el-menu-item index="1-4" 	@click='OnGroup' :class="szPointer =='GroupARL'?'el-icon-caret-right':''" v-show="group_flag">组的要求式样</el-menu-item>
				    	<!--<el-menu-item index="1-2"  @click='OnAllARL' id="first_arl" :class="szPointer =='AllARL'?'el-icon-caret-right':''">全体要求式样</el-menu-item>-->
				    	<el-menu-item index="1-2"  @click='OnMyARL'  :class="szPointer =='MyARL'?'el-icon-caret-right':''">我的要求式样</el-menu-item>
				    	<el-menu-item index="1-3"  @click='OnImputExport' :class="szPointer =='ImportExport'?'el-icon-caret-right':''">导入/导出</el-menu-item>
				    	<el-menu-item index="1-5" v-show="u_man"  @click='OnRelease' :class="szPointer =='Release'?'el-icon-caret-right':''">Release</el-menu-item>
              				<el-menu-item index="1-6" @click='OnWhiteList' :class="szPointer =='whitelist'?'el-icon-caret-right':''">白名单</el-menu-item>
					</el-submenu>
			 		<el-menu-item index="2" @click="OnHistory" id="heng" :class="szPointer =='History'?'bbb':''">履历管理</el-menu-item>
					<el-menu-item index="3" v-show="u_man" @click="OnUser" id="user" :class="szPointer =='User'?'bbb':''">用户管理</el-menu-item>
					<el-submenu index="10" >
				    	<template slot="title">{{user_name}}</template>
					<!-- 	<el-menu-item index="10-1"  @click="OnAccount" :class="szPointer =='Account'?'el-icon-caret-right':''">账号设置</el-menu-item> -->
				    	<el-menu-item index="10-2"  @click='OnLogout' :class="szPointer =='Logout'?'el-icon-caret-right':''">退出</el-menu-item>
					</el-submenu>
				</el-menu>
			</div>
		</div>
		<div id="homepageView">
			<!--<keep-alive>-->
				<router-view v-bind:work="workType"></router-view>
			<!--</keep-alive>-->
		</div>
	</div>
</template>
<script>
	export default{
		data(){
			return{
				szPointer:'MyARL',
				 user_name: '',
				 fullscreenLoading:false,
				 activeIndex2: '1',
				 workType: 'my',
				 u_man:false,
				 //u_count:false,
				 p_list:[],

				 admin_flag:false,
				 pl_flag:false,
				 leader_flag:false,
				 member_flag:false,
				 translation_flag:false,

				 Admin:false,
				 PL:false,
				 Leader:false,
				 leadGp:[],


				 group_flag:false
			}
		},
		mounted: function () {
			if(window.localStorage.getItem('WorkTypeStatus') != null){
				this.szPointer = window.localStorage.getItem('WorkTypeStatus')
			}
			this.user_name = window.sessionStorage.getItem('Uall')
			this.$axios.get(this.Ip+'/UserContent/'+window.sessionStorage.getItem('admin'))
				.then(res => {
					this.p_list=res.data.content;
					if(this.p_list.permission_list.length!=0){
						for(var i=0;i<this.p_list.permission_list.length;i++){
							if(this.p_list.permission_list[i].roles.length!=0){
								for(var j=0;j<this.p_list.permission_list[i].roles[j];j++){
									switch(this.p_list.permission_list[i].roles[j]){
										case 3:this.admin_flag = true;
										break;
										case 7:this.pl_flag = true;
										break;
										case 4:this.leader_flag = true;
										break;
										case 5:this.member_flag = true;
										break;
										case 6:this.translation_flag = true;
										break;
										default:
										break;
									}
								}
							}
						}
					}

					if(this.admin_flag==true){
						window.sessionStorage.setItem('Roles',"Admin")
						this.Admin=true;
						this.u_man =true;
						this.group_flag = true;
					}else if(this.admin_flag!=true&&this.pl_flag==true){
						window.sessionStorage.setItem('Roles',"PL")
						this.PL = true;
						this.u_man =true;
						this.group_flag = true;
					}else if(this.admin_flag!=true&&this.pl_flag!=true&&this.leader_flag==true){
						window.sessionStorage.setItem('Roles',"Leader")
						this.Leader = true;
						this.group_flag = true;
					}else if(this.admin_flag!=true&&this.pl_flag!=true&&this.leader_flag!=true&&this.translation_flag==true){
						window.sessionStorage.setItem('Roles',"Translator")
					}else if(this.admin_flag!=true&&this.pl_flag!=true&&this.leader_flag!=true&&this.translation_flag!=true){
						window.sessionStorage.setItem('Roles',"Member")
					}else{
						window.sessionStorage.setItem('Roles','Member')
					}
			})


		},
		methods: {
	        handleSelect(key, keyPath) {
	      	    event.preventDefault();
	        },
	        OnSpider() {
		    	this.szPointer = 'MyARL'
		    	window.sessionStorage.setItem('workType','my')
		    	window.localStorage.setItem('WorkTypeStatus','MyARL')
		    	this.workType = window.sessionStorage.getItem('workType')
		    	this.$store.state.release_type = ''
		    	this.$router.push('/homepage/mywork/list')
	        },

	        OnLogout() {
	        	/*
		        this.$confirm('退出登录?', '提示', {
		          confirmButtonText: '确定',
		          cancelButtonText: '取消',
		          type: 'warning'
		        }).then(() => {
		          this.$notify({
		            type: 'success',
		            message: '退出成功!'
		          })
		          this.$router.push('/login')
		        }).catch(() => {
		          this.$notify({
		            type: 'info',
		            message: '已取消退出'
		          })
		        });
				*/
				window.sessionStorage.removeItem('admin')
				window.sessionStorage.removeItem('Uall')
				window.sessionStorage.removeItem('workType')
				window.localStorage.removeItem('WorkTypeStatus')
		        this.$router.push('/login')
		    },
		    OnAllARL() {
		    	this.szPointer = 'AllARL'
		    	window.localStorage.setItem('WorkTypeStatus','AllARL')
		    	window.sessionStorage.setItem('workType','all')
		    	this.workType = window.sessionStorage.getItem('workType')
		    	this.$store.state.user_data = null
		    	this.$store.state.release_type = ''
		    	this.$router.push('/homepage/mywork/list')

		    },
		    OnMyARL() {
		    	this.szPointer = 'MyARL'
		    	window.localStorage.setItem('WorkTypeStatus','MyARL')
		    	window.sessionStorage.setItem('workType','my')
		    	this.workType = window.sessionStorage.getItem('workType')
		    	this.$store.state.user_data = null
		    	this.$store.state.release_type = ''
		    	this.$router.push('/homepage/mywork/list')

		    },
		    OnGroup(){
		    	this.szPointer = 'GroupARL'
				window.localStorage.setItem('WorkTypeStatus','GroupARL')
		    	window.sessionStorage.setItem('workType','group')
		    	this.workType = window.sessionStorage.getItem('workType')
		    	this.$store.state.user_data = null
		    	this.$store.state.release_type = ''
		    	this.$router.push('/homepage/mywork/list')
		    },
		    export_HU(){
		    	this.fullscreenLoading = true;
		    	this.$axios.get(this.Ip+'/Export/HU/'+Date.now())
		    	.then(res => {
					window.location.href=this.Ip+ res.data.datapath
		    		this.fullscreenLoading = false;
		    	})
		    },
		    export_TAGL(){
		    	this.fullscreenLoading = true;
		    	this.$axios.get(this.Ip+'/Export/TAGLDEF/'+Date.now())
		    	.then(res => {
					window.location.href=this.Ip+ res.data.datapath
		    		this.fullscreenLoading = false;
		    	})
		    },
		    OnUser(){
		    	this.szPointer = 'User'
				window.localStorage.setItem('WorkTypeStatus','User')
				this.$store.state.release_type = ''
		    	this.$router.push('/homepage/USER')
		    },
		    OnAccount(){
		    	this.szPointer = 'Account'
				window.localStorage.setItem('WorkTypeStatus','Account')
				this.$store.state.release_type = ''
		    	this.$router.push('/homepage/Account')
		    },
		    OnImputExport(){
		    	this.szPointer = 'ImportExport'
				window.localStorage.setItem('WorkTypeStatus','ImportExport')
				this.$store.state.release_type = 'Export'
		    	this.$router.push('/homepage/ImportExport')
		    },
		    OnRelease(){
		    	this.szPointer = 'Release'
				window.localStorage.setItem('WorkTypeStatus','Release')
				this.$store.state.release_type = 'Release'
		    	this.$router.push('/homepage/ImportExport')
		    },
        	    OnWhiteList(){
        	    this.szPointer = 'whitelist'
        	    window.localStorage.setItem('WorkTypeStatus','ImportExport')
        	    this.$store.state.release_type = 'whitelist'
        	    this.$router.push('/homepage/ImportExport')
        	    },
		    check_rule(event){
		    	this.$store.state.release_type = ''
		    	this.$router.push('/homepage/check_rule')
		    },
		    OnHistory(){
		    	this.szPointer = 'History'
				window.localStorage.setItem('WorkTypeStatus','History')
		    	this.$router.push('/homepage/History')
		    }
	    }
	}
</script>

<style scoped>
	.bbb{
	    border-bottom: 5px solid #42b983;
	}

	#homepage{
		position: absolute;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}
	#header{
		position: absolute;
		left: 0;
		top: 0;
		right: 0;
		width: 100%;
		height:60px ;
		background-color: white;
		z-index:1000;
		box-shadow: 0 0 1px rgba(0,0,0,0.25)
	}
	#homepageView{
		position: absolute;
		left: 0;
		right: 0;
		top: 60px;
		bottom: 0px;
		overflow: hidden;
		width: 100%;
		background: white;
	}
	#footer{
		position: absolute;
		z-index: 700;
		left: 0;
		right: 0;
		bottom: 0;
		width: 100%;
		height: 22px;
		background-color: white;
		text-align: right;
		line-height:22px ;
	}
	#brand{
		position: absolute;
		left: 40px;
		top: 3px;
		width: 150px;
		height: 54px;
		font-size: 30px;
		color: #2c3e50;
		line-height: 40px;
		font-weight:500;
		font-family: "Dosis","Source Sans Pro","Helvetica Neue",Arial,sans-serif;
	}
	#brand img{
		width: 55px;
		height: 55px;
		vertical-align: middle;
		margin-right: 0px;
	}
	#brand span{
		font-size:24px;
	}
	#logout{
		position: absolute;
		right: 90px;
	}
	#nav{
		position: absolute;
		right: 40px;
		top: 10px;
		height: 60px;
	}
	.liqq{
		float: right;
		right:70px;
	}
	#header .el-menu {
	    border-radius: 2px;
	    list-style: none;
	    position: relative;
	    margin: 0;
	    padding-left: 0;
	    background-color: white;
	}
	#header .el-menu--horizontal .el-menu-item {
	    float: left;
	    height: 40px;
	    line-height: 40px;
	    margin: 0;
	    cursor: pointer;
	    position: relative;
	    box-sizing: border-box;
	    margin-left: 10px;
	    margin-right: 10px;
	}

	#header .el-menu--horizontal.el-menu--dark .el-submenu .el-menu-item.is-active, .el-menu-item.is-active {
	    border-bottom: 5px solid #fff;
	}

</style>
