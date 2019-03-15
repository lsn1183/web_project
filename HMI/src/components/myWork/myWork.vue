<template>
	<div id="myWork">
		<div id="myTree" >
			<div class="tit_sh">HMI目录</div>	
			<el-tree 
			id="tre222"
			:data="data" 
			:highlight-current='true'
			empty-text="空"
			node-key='category_id' 
			:current-node-key='first_category_id'
	    	:props="defaultProps" 
	    	@node-click="handleNodeClick"
	    	v-loading.lock="fullscreenLoading"
	    	ref="tree2">
	    	</el-tree>
	    	<div class="jindu">
	    		<span>QA表</span>
	    	</div>
			<li class="jindu_child" :class="{'active': hl==1}" @click="External_QA()">外部QA表</li>
			<li class="jindu_child" :class="{'active': hl==2}" @click="Internal_QA()">内部QA表</li>
			<li class="jindu_child" :class="{'active': hl==6}" @click="External_BUG()">外部BUG表</li>	
			<div class="jindu">
	    		<span>统计表</span>
	    	</div>
			<li class="jindu_child" :class="{'active': hl==3}" @click="Statistic_Class">分类统计表</li>
			<li class="jindu_child" :class="{'active': hl==4}" @click="Statistic_author_Category">担当统计表</li>
			<li class="jindu_child" :class="{'active': hl==5}" @click="Statistic_screen_it">画面统计表</li>
			<li class="jindu_child" :class="{'active': hl==8}" @click="TAGL_IT_Schedule">IT进度统计表</li>
			
		</div>		
		<div id="my_work_view">
			<!--<keep-alive>-->
				<router-view></router-view>
			<!--</keep-alive>-->
		</div>		
	</div>
</template>

<script>
 	export default{
 		props: ['work'],
		components: {
		},
		created() {
		},
		data(){
			return{
				fullscreenLoading:false,
				data: [],
		        defaultProps: {
		          children: 'sub_category_list',
		          label: 'category_name'
		        },
		        dataid:{},
		        workStatus: '',
				hl:0,
				group_flag:false,
				group_id:[],
				group_value:"",
				group:[],
				first_category_id: ""
			}
		},
	    mounted(){
    		this.request();		
		},
		methods: {
			handleNodeClick(data) {
				this.hl=0;
			window.sessionStorage.setItem("b",data.category_id);  //设置b为"isaac"
			this.dataid = data.category_id
			this.$store.state.user_data = data.category_id
			this.$router.push('/hmi/list')
			},
			request: function(){
				this.fullscreenLoading = true
				this.$axios.get(this.Ip+'/HmiCategory')
				.then(res=> {
					if(res.data.content.length != 0){
						this.$store.state.user_data = res.data.content[0].category_id
					  	this.data = res.data.content;
					  	this.first_category_id = this.data[0].category_id
					}else{
						this.$store.state.user_data = null
					  	this.data = [];
					  	this.first_category_id = ''
					}
					this.fullscreenLoading = false
					this.group_flag = false;
					window.sessionStorage.setItem('change_status_flag',true)
					this.$router.push('/hmi/list')
				})
				.catch(function(error) {
					console.log(error)
				})      
			},
			External_QA() {
				this.group_flag = false
				this.hl = 1;
				this.$router.push('/hmi/External_QA')
			},
			Internal_QA() {
				this.group_flag = false
				this.hl = 2;
				this.$router.push('/hmi/Internal_QA')
			},
			External_BUG() {
				this.group_flag = false
				this.hl = 6;
				this.$router.push('/hmi/External_BUG')
			},
			Statistic_Class(){
				this.group_flag = false
				this.hl = 3;
				this.$router.push('/hmi/Class')
			},
			Statistic_author_Category(){
		      	this.group_flag = false
		      	this.hl = 4 ;
		      	this.$router.push('/hmi/Statistic_author_Category')
			},
			Statistic_screen_it(){
				this.group_flag = false
				this.hl = 5 ;
				this.$router.push('/hmi/Statistic_screen_it')
			},
			TAGL_IT_Schedule(){
				this.group_flag = false
		      	this.hl = 8 ;
		      	this.$router.push('/hmi/TAGL_IT_Schedule')
			},
			goAnchor(selector){
				var anchor = this.$el.querySelector(selector)
				document.body.scrollTop=anchor.offsetTop;
				document.documentElement.scrollTop = anchor.offsetTop;
			},
			getStatus (urlStr) {
				this.request();
			}
	    },
	    
		watch: {
			work(val){
				this.workStatus = val
				this.getStatus()
			}
		}
	}
</script>

<style scoped>
	#myWork{
		position: relative;
		width: 100%;
		max-width: 1920px;
		min-width: 1024px;
		height: 100%;
		background: white;
		overflow: hidden;
	}
	#myTree{
		float: left;
		/*position: absolute;*/
		display: inline-block;
		top: 0;
		bottom: 22px;
		/*width: 300px;*/
		width:16%;
		padding-left: 1%;	
		height: 100%;
		overflow: scroll;
	}
	#my_work_view{
		float: left;
		top: 0;
		width:83%;
		height: 100%;
		background-color: white;
	}
	#mytree #tre222{
		margin-left: 25px;
	}
	.tit_sh{
		color: black;
		font-weight: 600;
		margin-left: 25px;
		margin-top: 20px;
		font-size: large;
		text-align: left;
		line-height: 36px;
	}
	.tit_sh .tree_log{
		margin-left: 10px;
		width:110px;
	}
	.tit_sh .tree_log .el-input__icon+ .el-input__inner{
		height: 24px;
	}
	.jindu{
		font-weight: 600;
		margin-left: 25px;
		margin-top: 10px;
		font-size: large;
		text-align: left;
		margin-bottom: 10px;
	}
	#myTree .jindu_child{
		margin-left: 42px;
		font-size: small;
		text-align: left;
		list-style: none;
		cursor: pointer;
		line-height: 36px;
	}
	#myTree .jindu_child_ex{
		margin-left: 16px;
	}
	#myTree .jindu_child:hover{
		color: #42b983;
		cursor: pointer;
	}
	.jiancha{
		font-weight: 600;
		margin-left: 25px;
		margin-top: 10px;
		font-size: large;
		text-align: left;
		margin-bottom: 10px;
	}
	#myTree .jiancha_child{
		margin-left: 42px;
		font-size: small;
		text-align: left;
		list-style: none;
		cursor: pointer;
		line-height: 36px;
	}

	#myTree .jiancha_child:hover{
		color: #42b983;
		cursor: pointer;
	}
	.active{
		color: #42b983;
		font-weight: bold;
	}
	.el-tree{
		border: 0 none;
	}
	.group{
		position: absolute;
		left: 39.5%;
		top: 20px;
		line-height: 30px;
		z-index:1000;
		height: 30px;
	}
	.group .el-select{
		width: 122px;
	}
 	 .group_size{
		color: black;
	/*	font-weight: 600;    
		font-size: large;*/
		margin-left:5px;
		font-size: 14px;
	}
/*	.group .el-select .el-input .el-input__inner{
	  height: 30px;
	}*/
</style>
