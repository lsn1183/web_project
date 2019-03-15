<template>
	<div id="homepage">
		<!--头部组件-->
		<div id="header">
			<a href="javasript:;">
				<div id="brand"  @click='OnSpider'>
					<img src="../assets/img/Icon/HMI.png" class="left_hmi_img" alt="商标"/>
					<span>HMI</span>
				</div>
			</a>

			<div id="nav">
				<el-menu :default-active="activeIndex2" class="el-menu-demo header_li" mode="horizontal" >
					<el-submenu index="1">
				    	<template slot="title">HMI管理</template>
				    	<el-menu-item index="1-2"  @click='OnAllARL' :class="szPointer =='AllARL'?'el-icon-caret-right':''">全部HMI</el-menu-item>
				    	<el-menu-item index="1-3"  @click='OnImputExport' :class="szPointer =='ImportExport'?'el-icon-caret-right':''">HMI导入/导出</el-menu-item>
					</el-submenu>

<!-- 			 		<el-menu-item index="2" @click="OnHistory" id="heng" :class="szPointer =='History'?'bbb':''">履历管理</el-menu-item>
					<el-menu-item index="3" v-show="u_man" @click="OnUser" id="user" :class="szPointer =='User'?'bbb':''">用户管理</el-menu-item> -->
					<el-submenu index="2">
						<template slot="title">状态管理</template>
						<el-menu-item index="2-2" @click="OnDevState" id="user" :class="szPointer =='User'?'el-icon-caret-right':''">开发状态</el-menu-item>
						<el-menu-item index="2-3" @click="OnMoveInState" id="move" :class="szPointer =='Move'?'el-icon-caret-right':''">迁入状态</el-menu-item>
						<el-menu-item index="2-4" @click="OnAfterMoveInState" id="MoveAfter" :class="szPointer =='MoveAfter'?'el-icon-caret-right':''">后续画面迁移</el-menu-item>
						<el-menu-item index="2-5" @click="OnItProReportState" id="ITPRO" :class="szPointer =='ITPRO'?'el-icon-caret-right':''">IT流程状态</el-menu-item>
						<el-menu-item index="2-6" @click="OnItDevState" id="ITDEV" :class="szPointer =='ITDEV'?'el-icon-caret-right':''">IT开发状态</el-menu-item>
					</el-submenu>
					
					<el-submenu index="10" >
				    	<template slot="title">{{user_name}}</template>
				    	<el-menu-item index="10-2"  @click='OnLogout' :class="szPointer =='Logout'?'el-icon-caret-right':''">退出</el-menu-item>
					</el-submenu>
				</el-menu>
			</div>

		</div>
		<div id="homepageView">
			<router-view v-bind:work="workType"></router-view>
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
		    	this.$router.push('/hmi/list')
	        },

	        OnLogout() { 
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
		    	this.$router.push('/hmi/list')

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
		    	this.$router.push('/hmi/USER')
		    },
		    OnDevState(){
		    	this.szPointer = 'User'
				window.localStorage.setItem('WorkTypeStatus','User')
				this.$store.state.release_type = ''
		    	this.$router.push('/hmi/USER')
		    },
		    OnMoveInState(){
		    	this.szPointer = 'Move'
				window.localStorage.setItem('WorkTypeStatus','Move')
				this.$store.state.release_type = ''
		    	this.$router.push('/hmi/MoveIn')
		    },
		    OnAfterMoveInState(){
		    	this.szPointer = 'MoveAfter'
				window.localStorage.setItem('WorkTypeStatus','Move')
				this.$store.state.release_type = ''
		    	this.$router.push('/hmi/AfterMoveIn')
		    },
		    OnItProReportState(){
		    	this.szPointer = 'ITPRO'
				window.localStorage.setItem('WorkTypeStatus','Move')
				this.$store.state.release_type = ''
		    	this.$router.push('/hmi/ItProReportStauts')
		    },
		    OnItDevState(){
		    	this.szPointer = 'ITDEV'
				window.localStorage.setItem('WorkTypeStatus','Move')
				this.$store.state.release_type = ''
		    	this.$router.push('/hmi/ItDevStauts')
		    },
		    OnAccount(){
		    	this.szPointer = 'Account'
				window.localStorage.setItem('WorkTypeStatus','Account')
				this.$store.state.release_type = ''
		    	this.$router.push('/hmi/Account')
		    },
		    OnImputExport(){
		    	this.szPointer = 'ImportExport'
				window.localStorage.setItem('WorkTypeStatus','ImportExport')
				this.$store.state.release_type = 'Export'
		    	this.$router.push('/hmi/ImportExport')
		    },
		    check_rule(event){
		    	this.$store.state.release_type = ''
		    	this.$router.push('/hmi/check_rule')
		    },
		    OnHistory(){
		    	this.szPointer = 'History'
				window.localStorage.setItem('WorkTypeStatus','History')
		    	this.$router.push('/hmi/History')
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
	
	.left_hmi_img{
		border-radius: 50%;
	}
</style>
