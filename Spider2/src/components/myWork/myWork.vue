<template>
	<div id="myWork">
		<div class="group" v-show="group_flag">
	        <font color="#42b983"><i class="el-icon-document" style="fontSize:14px;"></i></font>
			<el-select  v-model="group_value" @change="select_group">
				<el-option class="button_tree_option" v-for="(item,index) in group"
				:key="index"
				:label="item.group_name"
				:value="item.group_id"
				>
				</el-option>
			</el-select>
			<span class="group_size">的要求式样书</span>
		</div>
		<div id="myTree" >
			<div class="tit_sh">要求式样书目录
				<el-select  class="tree_log" v-model="tree_log" placeholder="">
					<el-option  v-for="item in tree_log_list"
					:key="item.value"
					:label="item.label"
					:value="item.value"
					>
					</el-option>
				</el-select>
			</div>
			
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
	    	<!-- <div class="jindu">
	    		<span>基本要件</span>
	    	</div>
			<li class="jindu_child jindu_child_ex" :class="{'active': hl==6}" @click="BasicRequirement(1)"><span class="el-tree-node__expand-icon" style="margin-right: 8px;"></span>HU要件定義</li>
			<li class="jindu_child jindu_child_ex" :class="{'active': hl==7}" @click="BasicRequirement(2)"><span class="el-tree-node__expand-icon" style="margin-right: 8px;"></span>TAGL要件定義</li>
			<li class="jindu_child jindu_child_ex" :class="{'active': hl==8}" @click="BasicRequirement(3)"><span class="el-tree-node__expand-icon" style="margin-right: 8px;"></span>TAGL要件分析</li> -->
	    	<!-- <div class="jindu">
	    		<span>进度统计</span>
	    	</div>
			<li class="jindu_child" :class="{'active': hl==1}" @click="Statistic_Major_Category">大分类统计</li>
			<li class="jindu_child" :class="{'active': hl==5}" @click="Statistic_Minor_Category">小分类统计</li>
			<li class="jindu_child" :class="{'active': hl==2}" @click="Statistic_Group">组别统计</li>			
	    	<div class="jiancha">
				<span>检查规则</span>
	    	</div>
			<li class="jiancha_child" :class="{'active': hl==3}" @click="CheckRule_HU" >机能式样</li>
			<li class="jiancha_child" :class="{'active': hl==4}" @click="CheckRule_TAGL">要件定义</li> -->
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
				tree_log:1,
				tree_log_list:[
				{value:1,label:"V 0.40"},
				],
				group_flag:false,
				group_id:[],
				group_value:"",
				group:[],
				first_category_id: ""
			}
		},
	    mounted(){
    		this.request();
    		if(window.sessionStorage.getItem('workType')=='group'){
    			this.group_flag = true;
    			this.$axios.get(this.Ip+'/UserMyGroup/'+window.sessionStorage.getItem('admin'))
	    		.then(res=> {
	    			for(var i = 0; i<res.data.length ; i++){
		    			this.group_id.push(res.data[i].group_id)
		    			this.group  =res.data
		    			this.group_value =  this.group[0].group_id
		    			window.sessionStorage.setItem('groups_id',this.group_value)
	    			}
	    		})
    		}else{
    			this.group_flag = false;
    		}
			
		},
		methods: {
	      handleNodeClick(data) {
	      	this.hl=0;
			window.sessionStorage.setItem("b",data.category_id);  //设置b为"isaac"
			this.dataid = data.category_id
			this.$store.state.user_data = data.category_id
			this.$router.push('/homepage/mywork/list')
			if(window.sessionStorage.getItem('workType')=='group'){
				this.group_flag = true;
			}else{
				this.group_flag = false;
			}
	      },
	      request: function(){
	      	this.fullscreenLoading = true
	      	if(window.sessionStorage.getItem('workType')=='my'){
	      		this.group_flag = false;
	      		this.$axios.get(this.Ip+'/ARLUserCategory/'+window.sessionStorage.getItem('admin'))
	          	.then(response=> {
	          		if(response.data.content.length == 0){
	          			this.data = []
		          		this.$store.state.user_data = null
		          		this.first_category_id = ''
	          		}else{
	          			this.data = []
		          		this.data = response.data.content;
		          		this.first_category_id = response.data.content[0].category_id
		          		this.$store.state.user_data = this.data[0].category_id
		          		
	          		}
	          		this.fullscreenLoading = false
	          		this.group_flag = false;
	          		window.sessionStorage.setItem('change_time_flag',true)          		
	          	})
	          	.catch(function(error) {
	          		console.log(error)
				})
	          	
	      	}else if(window.sessionStorage.getItem('workType')=='group'){
	      		this.fullscreenLoading = true
	      		this.group_id = []
	      		this.group_flag = true;
	      		this.$axios.get(this.Ip+'/UserMyGroup/'+window.sessionStorage.getItem('admin'))
  			    	.then(res=> {
  			    		if(res.data == ""){
  			    			this.data = []
  			    			this.fullscreenLoading = false
  			    			this.group_flag = false;
  			    			this.$store.state.user_data = null
  			    			this.first_category_id = ''
  			    		}else{
	  			    		for(var i = 0; i<res.data.length ; i++){
	  			    			this.group_id.push(res.data[i].group_id)
	  			    			this.group  = res.data
	  			    			this.group_value =  this.group[0].group_id
	  			    		}
	  			    		// this.group.push({"group_id":0,"group_name":"全体组"})
				      		if(this.group_id.length!=0){
			  					this.$axios.post(this.Ip+'/ARLGroupCategory',{"group_id":this.group_id})
			  			    	.then(res=> {
//			  			    		this.data = res.data.content;
//			  			    		this.first_category_id = res.data.content[0].category_id
//	 	    						this.$store.state.user_data = this.data[0].category_id
//			  			    		this.fullscreenLoading = false
//			  			    		window.sessionStorage.setItem('change_status_flag',true)
			  			    		
			  			    		if(res.data.content.length == 0){
					          			this.data = res.data.content;
				  			    		this.first_category_id = ''
		 	    						this.$store.state.user_data = null
				  			    		this.fullscreenLoading = false
				  			    		window.sessionStorage.setItem('change_status_flag',true)
					          		}else{
					          			this.data = res.data.content;
				  			    		this.first_category_id = res.data.content[0].category_id
		 	    						this.$store.state.user_data = this.data[0].category_id
				  			    		this.fullscreenLoading = false
				  			    		window.sessionStorage.setItem('change_status_flag',true)
						          		
					          		}
			  			    		
			  			    	})
				      		}
				      		
  			    		}
  			    	})
	      	}else{
	      		this.fullscreenLoading = true
	      		this.$axios.get(this.Ip+'/ARLCategory')
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
				    
			      })
			      .catch(function(error) {
			      	console.log(error)
			      })
			      
			}       
	      },
	      select_group(){
	     //  	if(this.group_value==0){
	     //  		this.fullscreenLoading = true
  				// this.$axios.post(this.Ip+'/ARLGroupCategory',{"group_id":this.group_id})
  		  //   	.then(res=> {
  		  //   		this.data = res.data.content;
  		  //   		this.fullscreenLoading = false
  		  //   	})
	     //  	}else{
	      		var groups_id = []
	      		groups_id.push(this.group_value)
	      		this.fullscreenLoading = true
	      		window.sessionStorage.setItem('groups_id',this.group_value)
  				this.$axios.post(this.Ip+'/ARLGroupCategory',{"group_id":groups_id})
  		    	.then(res=> {
  		    		this.data = res.data.content;
  		    		this.fullscreenLoading = false
  		    	})
	      	// }
	      },
	      CheckRule_HU(){
	      	this.group_flag = false
	      	this.hl = 3;
	      	this.$router.push('/homepage/mywork/CheckRule_HU')
	      },
	      CheckRule_TAGL(){
	      	this.group_flag = false
	      	this.hl = 4;
	      	this.$router.push('/homepage/mywork/CheckRule_TAGL')
	      },
	      Statistic_Major_Category(){
	      	this.group_flag = false
	      	this.hl = 1 ;
	      	this.$router.push('/homepage/mywork/Statistic_Function')
	      },
	      Statistic_Minor_Category(){
	      	this.group_flag = false
	      	this.hl = 5 ;
	      	this.$router.push('/homepage/mywork/Statistic_Minor_Category')
	      },
	      Statistic_Group(){
	      	this.group_flag = false
	      	this.hl = 2;
	      	this.$router.push('/homepage/mywork/Statistic_Group')
	      },
	      BasicRequirement(val){
	      	//初始状态传值并监听
	        this.group_flag = false	      	
	      	if (val == 1) {
	      		this.hl = 6;
	      		this.$store.state.basic_type = 'hu'
	      		window.sessionStorage.setItem('Type', 'hu');
	      		this.$router.push('/homepage/mywork/HUDef_BasicRequirement')
	      	} else if(val == 2){
	      		this.hl = 7;
				this.$store.state.basic_type = 'tagl_def'
				window.sessionStorage.setItem('Type', 'tagl_def');
				this.$router.push('/homepage/mywork/TAGLDef_BasicRequirement')
	      	}else{
	      		this.hl = 8;
	      		this.$store.state.basic_type = 'tagl_ana'
	      		window.sessionStorage.setItem('Type', 'tagl_ana');
	      		this.$router.push('/homepage/mywork/TAGLAna_BasicRequirement')
	      	}
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
