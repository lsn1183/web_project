<template>
<div style="height:100%">
	<div class="history_content">
		<div class="left_menu fl">
		   	<div>
		   		<ul>
		   			<li :class="{'active': szPointer=='MyLog'}" @click="OnMyLog()">我的履历</li>
					<li :class="{'active': szPointer=='AllLog'}" @click="OnAllLog()">全体履历</li>
					<li :class="{'active': szPointer=='SearchLog'}" @click="OnSearchLog()">搜索履历</li>
		   		</ul>
		   	</div>
		</div>
		<div class="history_msg" v-show="szPointer=='MyLog'">
			
			<div class="history_menu">
				<el-row>
				<template>
					<div class="first">
						<el-date-picker v-model="defaultValue" type="daterange"  align="right" range-separator='  ~  ' placeholder="选择查看日期范围" :picker-options="OnPicker" @change="check">
						</el-date-picker>
					</div>
					<el-button  class="history_btn" @click="Commit_my"><i class="el-icon-search"> 查询</i></el-button>
				</template>
				
				</el-row>
			</div>
			<div class="right_menu fl">
				<template>
				  <el-table  :data="tableData" border   height=:30
				  	style="width: 100%;height:100%;overflow:auto"  class="right_table" >
				    <el-table-column prop="commit_time" label="日期"  width="250">
				    </el-table-column>
				    <!-- <el-table-column prop="group_name" label="组名"  width="150">
				    </el-table-column> -->
				    <el-table-column prop="user_name" label="姓名"   width="150">
				    </el-table-column>
				    <el-table-column prop="str" label="修改內容" >
				    </el-table-column>
				    <el-table-column prop="" label="修改详细"  width="120">
				    	<template scope="props">
				    		<el-button type="text" @click="log_msg(props.$index)"><i class="el-icon-view"> 查看</i></el-button>
				    	</template>
				    </el-table-column>
				  </el-table>      
				</template>
			</div>
		</div>
		<div class="history_msg" v-show="szPointer=='AllLog'">
			
			<div class="history_menu">
				
				<template>
					<div class="first">
						<el-date-picker v-model="defaultValue" type="daterange"  align="right" range-separator='  ~  ' placeholder="选择查看日期范围" :picker-options="OnPicker" @change="check">
						</el-date-picker>
					</div>
					<!-- <el-select v-model="Group_id" class="second" clearable filterable placeholder="请选择组" >
						<el-option v-for="item in Ggroups"  :key="item.group_id" :label="item.group_name" :value="item.group_id"></el-option>
					</el-select> -->
					<el-select v-model="member_id" class="second" clearable filterable placeholder="请选择人" >
						<el-option v-for="item in members"  :key="item.user_id" :label="item.user_name" :value="item.user_id"></el-option>
					</el-select>
					
					<el-button class="history_btn" @click="Commit"><i class="el-icon-search"> 查询</i></el-button>
				</template>
				
			 	
			</div>
			
			<div class="right_menu fl">
				<template>
				  <el-table  :data="tableData" border   height=:30
				  	style="width: 100%;height:100%;overflow:auto"   class="right_table" >
				    <el-table-column prop="commit_time" label="日期"  width="250">
				    </el-table-column>
				   <!--  <el-table-column  prop="group_name" label="组名"  width="150">
				    </el-table-column> -->
				    <el-table-column prop="user_name" label="姓名"  width="150">
				    </el-table-column>
				    <el-table-column prop="str" label="修改內容" >
				    </el-table-column>
				    <el-table-column prop="" label="修改详细"  width="120">
				    	<template scope="props">
				    		<el-button type="text" @click="log_msg(props.$index)"><i class="el-icon-view"> 查看</i></el-button>
				    	</template>
				    </el-table-column>
				  </el-table>      
				</template>
			</div>
		</div>
		<div class="history_msg" v-show="szPointer=='SearchLog'">
			<div class="history_menu">
				<template>
					<div class="first" @keyup.enter="SearchComit">
						<el-input :placeholder=placeholderContent v-model="search_id" style="  width:410px">
							<el-select v-model="search_type" slot="prepend" placeholder="请选择类型" style="width:140px" @change="SetPlaceholder">
								<el-option label="要求式样" value="arl"></el-option>
								<el-option label="机能式样" value="hu"></el-option>
								<el-option label="要件定義" value="definition"></el-option>
								<el-option label="要件分析" value="analysis"></el-option>
							</el-select>
							<el-button slot="append" icon="search" @click="SearchComit" style="width:38px;height: 38px"></el-button>
						</el-input>
					</div>
				</template>
			</div>
			<div class="right_menu fl">
				<template>
				  <el-table  :data="tableData" border   height=:30
				  	style="width: 100%;height:100%;overflow:auto"  class="right_table" >
				    <el-table-column prop="commit_time" label="日期" >
				    </el-table-column>
				    <!-- <el-table-column prop="group_name" label="组名" >
				    </el-table-column> -->
				    <el-table-column prop="user_name" label="姓名" >
				    </el-table-column>
				    <el-table-column prop="" label="修改详细"  >
				    	<template scope="props">
				    		<el-button type="text" @click="search_log_msg(props.$index)"><i class="el-icon-view"> 查看</i></el-button>
				    	</template>
				    </el-table-column>
				  </el-table>      
				</template>
			</div>
		</div>
		<div class="pagecount">
			<el-pagination
			v-if="search_log_page_flag"
			id="search_log_page"
			@current-change="searchLogPageChange"
			:current-page="page"
			:page-size="page_size"
			layout="total, prev, pager, next"
			:total="changdu"
			></el-pagination>
			<el-pagination
			v-if="log_page_flag"
			id="log_page"
			@current-change="logPageChange"
			:current-page="page"
			:page-size="page_size"
			layout="total, prev, pager, next"
			:total="changdu"
			></el-pagination>
					
		</div>
		<HLlog v-if="log_flag" class="hello" @guanbi="close" :commit_id="commit_id" :comit_m_id="commit_m_id"></HLlog>	
		<!--搜索履历通信传值-->
		<Searchlog v-if="search_flag" class="hello" @guanbi="close" :commit_id="commit_id" :comit_m_id="commit_m_id"></Searchlog>	
	</div>
</div>
</template>
<script>

import HL_log from './History_log.vue';
import Searchlog from './Search_log.vue';

require('../../assets/js/jquery-1.8.3.min.js');
	export default{
		name:'History',
		props:[],
		components:{
			"HLlog":HL_log,
			"Searchlog":Searchlog,
			// "TAGLDlog":TAGLD_log,
			// "TAGLAlog":TAGLA_log,
		},
		data(){
			return {
				placeholderContent:'',
				OnPicker: {
			         shortcuts: [
			         {
			           text: '最近一周',
			           onClick(picker) {
			             const end = new Date();
			             const start = new Date();
			             start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
			             picker.$emit('pick', [start, end]);
			           }
			         }, 
			         {
			           text: '最近一个月',
			           onClick(picker) {
			             const end = new Date();
			             const start = new Date();
			             start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
			             picker.$emit('pick', [start, end]);
			           }
			         }, 
			         {
			           text: '最近三个月',
			           onClick(picker) {
			             const end = new Date();
			             const start = new Date();
			             start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
			             picker.$emit('pick', [start, end]);
			           }
			         }
			    ]
			       },

			    szPointer:'MyLog',   

				defaultValue: new Date()- 3600 * 1000 * 24 * 30,
				tableData: [],
				Ggroups:[],
				members:[],
				Group_id:null,
				member_id:null,
				new_date:"",
				msg_log:false,
				logtable:[],
				logtable_two:[],
				my_log:false,
				all_log:true,
				log_flag:false,
				search_flag:false,
				// TAGL_log_flag:false,
				// TAGL_ana_log_flag:false,
				commit_id:0,
				last_id:0,
				page_size:200,
				page:1,
				changdu:0,

				search_log_page_flag:false,
				log_page_flag:true,
				
				search_id:'',
				search_type:'',
				commit_m_id:0,
			}
		},
		mounted(){
			this.myload(0,window.sessionStorage.getItem('admin'));
			this.$axios.get(this.Ip+"/GroupAllGroups")
			.then(res=>{
				this.Ggroups = res.data.content;
			})
			this.getmembers();	
		},
		methods:{
			SetPlaceholder(){
				if(this.search_type == 'analysis'|| this.search_type == 'basic_req_analysis'){
					this.placeholderContent="请输入(要件定义ID+'.'+UniqueID)"
				}else{
					this.placeholderContent="请输入查询ID"
				}
			},
			myload(Group_id,my_id){
				var str = "";
				var formatDate = function(date){
					var y = date.getFullYear();
					var m = date.getMonth()+1;
					m = m< 10 ? '0' + m : m;
					var d = date.getDate();
					d = d <10 ? ('0'+d) : d;
					return y + '-' + m + '-' + d;
				}
				const end = new Date();
				const start = new Date();
				start.setTime(start.getTime() - 3600 * 1000 * 24 * 180);
				var start_time = formatDate(start)
				var end_time  = formatDate(end)
				this.$axios.get(this.Ip+"/CommitLog/"+Group_id+'/'+my_id+'/'+start_time+'/'+end_time+'/'+this.page_size+'/'+1).then(res=>{
					if(res.data.result=="OK"){
						this.tableData = res.data.content
						this.changdu = res.data.total_count;
						for(var i=0;i<this.tableData.length;i++){
							str = "";
							for(var j=0;j<this.tableData[i].classify.length;j++){
								if(this.tableData[i].classify[j]=="arl"){
									str = str+"指派人員改變;"
								}else if(this.tableData[i].classify[j]=="hu"){
									str = str+"机能式样;"
								}else if(this.tableData[i].classify[j]=="definition"){
									str = str+"要件定义;"
								}else if(this.tableData[i].classify[j]=="analysis"){
									str = str+"要件分析;"
								}
								this.tableData[i].str=str;
							}
						}
					}else{
		     				this.tableData = [];
		     				this.changdu = 0;
			     		}
				})
				// console.log(start_time,"start")
				// console.log(end_time,"end")
			},
			load(Group_id,my_id){
				var str = "";
				var formatDate = function(date){
					var y = date.getFullYear();
					var m = date.getMonth()+1;
					m = m< 10 ? '0' + m : m;
					var d = date.getDate();
					d = d <10 ? ('0'+d) : d;
					return y + '-' + m + '-' + d;
				}
				const end = new Date();
				const start = new Date();
				start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
				var start_time = formatDate(start)
				var end_time  = formatDate(end)
				this.$axios.get(this.Ip+"/CommitLog/"+Group_id+'/'+my_id+'/'+start_time+'/'+end_time+'/'+this.page_size+'/'+1).then(res=>{
					// console.log(res,"99999")
//					console.log(this.Ip+"/CommitLog/"+Group_id+"/"+my_id+"/"+time1+'/'+time2+'/'+this.page_size+'/'+1,"id")
					if(res.data.result=="OK"){
						this.tableData = res.data.content
						this.changdu = res.data.total_count;
						for(var i=0;i<this.tableData.length;i++){
							str = "";
							for(var j=0;j<this.tableData[i].classify.length;j++){
								if(this.tableData[i].classify[j]=="arl"){
									str = str+"指派人員改變;"
								}else if(this.tableData[i].classify[j]=="hu"){
									str = str+"机能式样;"
								}else if(this.tableData[i].classify[j]=="definition"){
									str = str+"要件定义;"
								}else if(this.tableData[i].classify[j]=="analysis"){
									str = str+"要件分析;"
								}
								this.tableData[i].str=str;
							}
						}
					}else{
		     				this.tableData = [];
		     				this.changdu = 0;
			     		}
				})
			},
			OnMyLog(){
				this.tableData=[];
				this.szPointer = 'MyLog';
				this.log_page_flag = true;
				this.search_log_page_flag = false;
				this.page = 1;
				this.commit_m_id=0;
				this.myload(0,window.sessionStorage.getItem('admin'));
				this.close()

			},
			OnSearchLog(){
				this.tableData=[];
				this.szPointer = 'SearchLog';
				this.log_page_flag = true;
				this.search_log_page_flag = false;
				// this.page = 1;
				this.changdu =0;
				this.close()
			},
			OnAllLog(){
				this.tableData=[];
				this.szPointer = 'AllLog';
				this.log_page_flag = true;
				this.search_log_page_flag = false;
				this.page = 1;
				this.commit_m_id=0;
				this.load(0,0);
				this.close()
			},
			logPageChange(val){
				var page = val;
				var formatDate = function(date){
					var y = date.getFullYear();
					var m = date.getMonth()+1;
					m = m< 10 ? '0' + m : m;
					var d = date.getDate();
					d = d <10 ? ('0'+d) : d;
					return y + '-' + m + '-' + d;
				}
				if(this.szPointer == 'MyLog'){
					const end = new Date();
					const start = new Date();
					start.setTime(start.getTime() - 3600 * 1000 * 24 * 180);
					var start_time = formatDate(start)
					var end_time  = formatDate(end)
					this.Loaxios(0,window.sessionStorage.getItem('admin'),start_time,end_time,page)
				}else if(this.szPointer == 'AllLog'){
					const end = new Date();
					const start = new Date();
					start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
					var start_time = formatDate(start)
					var end_time  = formatDate(end)
					this.Loaxios(0,0,start_time,end_time,page)
				}
				
			},
			Loaxios(Group_id,my_id,time1,time2,page){
				var str= ''
				this.$axios.get(this.Ip+"/CommitLog/"+Group_id+'/'+my_id+'/'+time1+'/'+time2+'/'+this.page_size+'/'+page).then(res=>{
					// console.log(res,"99999")
//					console.log(this.Ip+"/CommitLog/"+Group_id+"/"+my_id+"/"+time1+'/'+time2+'/'+this.page_size+'/'+page,"id2")
					if(res.data.result=="OK"){
						this.tableData = res.data.content
						this.changdu = res.data.total_count;
						for(var i=0;i<this.tableData.length;i++){
							str = ""
							for(var j=0;j<this.tableData[i].classify.length;j++){
								if(this.tableData[i].classify[j]=="arl"){
									str = str+"指派人員改變;"
								}else if(this.tableData[i].classify[j]=="hu"){
									str = str+"机能式样;"
								}else if(this.tableData[i].classify[j]=="definition"){
									str = str+"要件定义;"
								}else if(this.tableData[i].classify[j]=="analysis"){
									str = str+"要件分析;"
								}
								this.tableData[i].str=str
							}
						}
					}
				})
			},
			searchLogPageChange(val){
				var time1=this.new_date.substring(0,10)
		     	var time2=this.new_date.substring(15,25)
		     	var page = val;
				if(this.Group_id!=null&&this.member_id!=null){
					this.LogAxios(this.Group_id,this.member_id,time1,time2,page)
		     	}else if(this.Group_id!=null&&this.member_id==null){
		     		this.LogAxios(this.Group_id,0,time1,time2,page)
		     	}else if(this.Group_id==null&&this.member_id!=null){
		     		this.LogAxios(0,this.member_id,time1,time2,page)
		     	}else if(this.Group_id==null&&this.member_id==null){
		     		this.LogAxios(0,0,time1,time2,page)
		     	}
				
			},
			LogAxios(G_id,m_id,time1,time2,page){
				var str = ""
				this.$axios.get(this.Ip+"/CommitLog/"+G_id+'/'+m_id+'/'+time1+'/'+time2+'/'+this.page_size+'/'+page)
				.then(res=>{
					if(res.data.result=="OK"){
						this.tableData = res.data.content
						this.changdu = res.data.total_count;
						for(var i=0;i<this.tableData.length;i++){
							str = ""
							for(var j=0;j<this.tableData[i].classify.length;j++){
							if(this.tableData[i].classify[j]=="arl"){
								str = str+"指派人員改變;"
							}else if(this.tableData[i].classify[j]=="hu"){
								str = str+"机能式样;"
							}else if(this.tableData[i].classify[j]=="definition"){
								str = str+"要件定义;"
							}else if(this.tableData[i].classify[j]=="analysis"){
								str = str+"要件分析;"
							}
							this.tableData[i].str=str
						}
						}
						// console.log(this.tableData,"History.vue")
					}else{
					    this.$notify({
					      iconClass:'message_icon_info',
					      message: '没有查询结果 ',
						})
						
					}
				})
			},
		    formatter(row, column) {
		        return row.address;
		    },
		    getmembers(){
		     	this.$axios.get(this.Ip+"/AllUsers")
					.then(des=>{
						this.members = des.data.content;
					})
		    },
		    check(val){
		     	this.new_date = val
		    },
		    getCommit(Group_id,m_id,time1,time2){
				var str = ""
		     	if(time1!=""&&time2!=""){
			     	this.$axios.get(this.Ip+"/CommitLog/"+Group_id+'/'+m_id+'/'+time1+'/'+time2+'/'+this.page_size+'/'+1).then(res=>{
			     		if(res.data.result=="OK"){
				     		this.tableData = res.data.content
				     		this.changdu = res.data.total_count;
				     		for(var i=0;i<this.tableData.length;i++){
				     			str = ""
				     			for(var j=0;j<this.tableData[i].classify.length;j++){
									if(this.tableData[i].classify[j]=="arl"){
										str = str+"指派人員改變;"
									}else if(this.tableData[i].classify[j]=="hu"){
										str = str+"机能式样;"
									}else if(this.tableData[i].classify[j]=="definition"){
										str = str+"要件定义;"
									}else if(this.tableData[i].classify[j]=="analysis"){
										str = str+"要件分析;"
									}
									this.tableData[i].str=str
								}
				     		}
				     		// console.log(this.tableData,"History.vue")
			     	}else{
		     			    this.$notify({
		     			      iconClass:'message_icon_info',
		     			      message: '没有查询结果 ',
		     				})
		     				this.tableData = [];
		     				this.changdu = 0;
			     		}
			     	})
			     }else{
		     	    this.$notify({
		     	      iconClass:'message_icon_info',
		     	      message: '请选择相应的时间段',
		     		})
			     }
		    },
		    Commit(){
		    	this.search_log_page_flag = true;
		    	this.log_page_flag = false;
		    	this.page=1;
		    	var time1=this.new_date.substring(0,10)
		     	var time2=this.new_date.substring(15,25)
		     	// this.last_id = 0;
		     	if(this.Group_id!=null&&this.member_id!=null){
		     		var Group_id = this.Group_id;
					var user_id = this.member_id;
					this.getCommit(Group_id,user_id,time1,time2);
		     	}else if(this.Group_id!=null&&this.member_id==null){
		     		var Group_id = this.Group_id;
					var user_id = 0;
					this.getCommit(Group_id,user_id,time1,time2);
		     	}else if(this.Group_id==null&&this.member_id!=null){
		     		var Group_id = 0;
					var user_id = this.member_id;
					this.getCommit(Group_id,user_id,time1,time2);
		     	}else if(this.Group_id==null&&this.member_id==null){
		     		var Group_id = 0;
					var user_id = 0;
					this.getCommit(Group_id,user_id,time1,time2);
		     	}
		    },
		    Commit_my(){
		    	this.search_log_page_flag = true;
		    	this.log_page_flag = false;
		    	this.page=1;
		    	var time1=this.new_date.substring(0,10)
		     	var time2=this.new_date.substring(15,25)
				var Group_id = 0;
				var my_id = window.sessionStorage.getItem('admin');
				this.getCommit(Group_id,my_id,time1,time2)
		    },
		    //搜索履历--查询ID
		    SearchComit(){
		     	this.$axios.get(this.Ip+"/CommitLogByClassifyAndId"+"/"+this.search_type+"/"+this.search_id)
		     	.then(res=>{
					if(res.data.result=="OK"){
						this.tableData = res.data.content
						this.changdu = res.data.total_count;
//						console.log(this.tableData,"History.vue")
						
						
					}else{
						this.$notify({
							iconClass:'message_icon_info',
							message: '没有查询结果 ',
						})
						this.tableData = [];
						this.changdu = 0;
					}
				})
		     	
		    },
		    close(val){
		     	this.log_flag =false;
		     	this.search_flag =false;

		    },
		    //测试用
		    log_text(){
		     	this.commit_id = 373;
		     	this.$axios.get(this.Ip+"/DetailLog"+"/"+this.commit_id+"/"+131247)
		     	.then(res=>{
					if(res.data.result=="OK"){
						this.log_flag = true;
					}
				})
		    },
		    //我的和全体履历
		    log_msg(index){
		     	// this.msg_log=!this.msg_log
		     	this.commit_id = this.tableData[index].commit_id;
		     	this.$axios.get(this.Ip+"/DetailLog"+"/"+this.commit_id+"/"+0)
		     	.then(res=>{
					if(res.data.result=="OK"){
				     	this.log_flag = true;
						this.search_flag =false;
					}
		     	})
		    },
		    //搜索履历
		    search_log_msg(index){
		    	this.commit_id = this.tableData[index].commit_id;

		     	this.commit_m_id = this.tableData[index].commit_log_ref_id;
		     	this.$axios.get(this.Ip+"/DetailLog"+"/"+this.commit_id+"/"+this.commit_m_id)
		     	.then(res=>{
					if(res.data.result=="OK"){
				     	this.log_flag = false;
				     	this.search_flag =true;
					}
		     	})
		    },
		}
	}
</script>
<style scoped>
	*{
		margin: 0;
		padding: 0;
	}
	.history_content{
		height:100%;
		width:100%;
	}
	.fl{
		float: left;
	}
	.fr{
		float: right;
	}
	.history_menu{
		margin-top: 20px;
		width: 100%;
		height:50px;
		border-bottom:solid 1px #dfe6ec
	}
	.history_msg{
		/*float: left;
		width: 82%;*/
		/*margin-left:1%;*/
		position: absolute;
		left: 300px;
		right: 0;
		top: 0;
		bottom: 70px;
	}
	.el-table::before{
		height: 0;
	}
	.first{
		float: left;
		margin-left: 20px;
	}
	.second{
		float: left;
		width: 140px;
		margin-left: 12px;
	}
	.third{
		float: left;
		width: 170px;
		margin-left: 12px;
	}
	.history_btn2{
		position: absolute;
		margin-left: 20px;		
		/*top: 5px;*/
		width: 100px;
		height: 48px;
		font-size:16px;
		border:0 none;
		font-family: "微软雅黑";
		color:#42b983;
	}	
	.history_btn{
		position: absolute;
		right: 38px;
		/*top: 5px;*/
		width: 100px;
		height: 48px;
		font-size:16px;
		border:0 none;
		font-family: "微软雅黑";
		color:#42b983;
	}
	.block{
		height: 48px;
		line-height: 48px;
		margin-left:6%;
	}
	.left_menu{
		padding-left: 45px;
		width: 300px;	
/*		width:17%;
		float: left;
*/
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

	.pagecount{
		position: absolute;
		left: 300px;
		right: 0;
		bottom: 0;
		height: 30px;
		width: 100%;
		/*border: 1px solid red;*/
		background-color: white;
	}
	.el-menu-vertical-demo{
		width:100%;
	}
	.right_menu{
		width: 100%;
		height: 95%;
	}
	.right_table{
/*		margin: 0 auto;
		margin-top: 30px;
		max-height: 700px;*/
	}
	.el-dialog--small{
		width: 80%;
	}
	.msg_log_span{

	}
	.hello{
		z-index: 9000;
		position: relative;
		bottom: 0;
		top: 60px;

	}
</style>
