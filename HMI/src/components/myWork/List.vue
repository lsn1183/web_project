<template>
<div id="ARLlist">
	<div class="BTN">
		<div id="BTN_top">
			<div class="fl" style="margin-left:9px">
		        <font color="#42b983"><i class="el-icon-document" ></i></font>
				<el-select  class="button_tree" v-model="arr_v" @change="Summary_ARL">
					<el-option class="button_tree_option" v-for="item in arr"
					:key="item.value"
					:label="item.label"
					:value="item.value"
					>
					</el-option>
				</el-select>
			</div>
<!-- 			<div class="input_search" style="margin-left:48px" @keyup.enter="List_search(input_value)">
				<el-input placeholder="请输入搜索ID" size="mini" v-model="input_value"  >
					<el-button slot="append" class="el-icon-search" @click="List_search(input_value)" ></el-button>
				</el-input>
			</div> -->
		</div>
	</div>
	<div id="treeMap"  class="fl" v-loading.lock="fullscreenLoading">
			<el-checkbox-group v-model="checkedC" @change="CheckedChange">
				<div style="margin: 0px 0;"></div>
				<ul id="ul">
					<li class="li first_li" v-if="hmi_falg">
						<span class="cy ID">ID</span>
						<span class="msy ID" style="width:11%">APL日程</span>
						<span class="msy ID" style="width:10%">APL进度</span>
						<span class="msy ID" style="width:10%">外部QA番号</span>
						<span class="msy ID" style="width:15%">结合测试进度</span>
						<span class="msy ID" style="width:15%">结合测试Release版本</span>
						<span class="cy ID" style="width:7%;">
							<span style="display:block;width:100%;height:100%">担当</span>	
						</span>
						<span class="cy ID" style="width:7%;">
							<span style="display:block;width:100%;height:100%;fontSize:13px;">负责人
							</span>
						</span>
						<span class="cz ID">操作</span>
					</li>
	
					<li class="li first_li" v-if="picture_falg">
						<span class="cy ID">HMI画面ID</span>
						<span class="msy ID" style="width:10%">HMI画面进度</span>
						<span class="msy ID" style="width:25%">外部QA番号</span>
						<span class="msy ID" style="width:15%">是否为入口画面</span>
						<span class="cy ID" style="width:25%;">
							<span style="display:block;width:100%;height:100%">备注</span>	
						</span>
						<span class="cz ID">操作</span>
					</li>

					<li class="li_scroll">
						<ul class="ul_scroll">
							<li class="li"  v-for="(item,index) in table1" @click.stop='change1(item.hu_id)' :key="index" v-if="hmi_falg">
								<i class="Asa_i"  :title="item.title"></i>
								<span class="cy span_width" v-show="cy" @click.stop='change1(item.hu_id)' :class="{'active':num == index}"  :title="item.title">
									<span style="marginLeft:42px">{{item.title}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info"  style="width:11%">
									<span style="display:block;width:100%;height:100%;" :title="item.apl_schedule">{{item.apl_schedule}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info"  style="width:10%">
									<span style="display:block;width:100%;height:100%;" :title="item.apl_progress">{{item.apl_progress}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info"  style="width:10%">
									<span style="display:block;width:100%;height:100%;" :title="item.external_qa">{{item.external_qa}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info"  style="width:15%">
									<span style="display:block;width:100%;height:100%;" :title="item.it_progress">{{item.it_progress}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info"  style="width:15%">
									<span style="display:block;width:100%;height:100%;" :title="item.it_release_ver">{{item.it_release_ver}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" :title="item.author">{{item.author}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" :title="item.charger">{{item.charger}}</span>
								</span>
								<span class="cz cen" v-show="cy" @click="amint()"><i class="el-icon-d-arrow-left"> 详细</i></span>
							</li>
							
							<li class="li"  v-for="(item,index) in table1" @click.stop='change1(item.screen_id)' :key="index" v-if="picture_falg">
								<i class="Asa_i"  :title="item.screen_id"></i>
								<span class="cy span_width" v-show="cy" @click.stop='change1()' :class="{'active':num == index}"  :title="item.screen_id">
									<span style="marginLeft:42px">{{item.screen_id}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info"  style="width:10%">
									<span style="display:block;width:100%;height:100%;" :title="item.screen_progress">{{item.screen_progress}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info"  style="width:25%">
									<span style="display:block;width:100%;height:100%;" :title="item.external_qa">{{item.external_qa}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info"  style="width:15%">
									<span style="display:block;width:100%;height:100%;" :title="item.remark">{{item.remark}}</span>
								</span>
								<span class="msy" style="width:25%">
									<span style="display:block;width:100%;height:100%;" :title="item.is_enter_screen">{{item.is_enter_screen}}</span>
								</span>
								<span class="cz cen" v-show="cy" @click="amint()"><i class="el-icon-d-arrow-left"> 详细</i></span>
							</li>

						</ul>
					</li>
				</ul>
			</el-checkbox-group>

	</div>
	<div id="list" v-show="show_flag">
	 	<div>
		    <div v-show="Maptree" id="Maptree"></div>
		    <div v-if="Maplist" id="Maplist">
		    	<div class="nav">
		    		<i class="el-icon-d-arrow-right fl" style="marginRight:5px" @click="back_up()"></i>
		    	</div>
		    	<el-collapse  accordion>
			    	<div class="user_name_title">
			    		<span><img src="../../assets/img/Icon/user_icon_2.png" class="user_icon"/> {{userNames}}</span>
			    	</div>
		    	</el-collapse>
			    <el-collapse  accordion v-for="(table_msg,arl_index) in tabledata1" :key="arl_index">
					<el-collapse-item  :title="table_msg.hu_id">
						<div class="arl_table">
							<div class='table_content' style="width:9%">
								<p class="table_title">
									<span>HU ID</span>
								</p>
								<p class="table_msg" >
									{{table_msg.hu_id}}
								</p>
							</div>
							<div class='table_content' style="width:10%">
								<p class="table_title">
									<span>ScreenID</span>
								</p>
								<p class="table_msg" :title='table_msg.screen_id'>
									<span>{{table_msg.screen_id}}</span>
								</p>
							</div>
							<div class='table_content' style="width:24%">
								<p class="table_title">
									<span>時序図</span>
								</p>
								<p class="table_msg" :title="table_msg.seq_diagram_file">
									<span>{{table_msg.seq_diagram_file}}</span>
								</p>
							</div>
							<div class='table_content' style="width:26%">
								<p class="table_title">
									<span>Application</span>
								</p>
								<p class="table_msg" :title="table_msg.application">
									<span>{{table_msg.application}}</span>
								</p>
							</div>
							<div class='table_content' style="width:21%">
								<p class="table_title">
									<span>除外</span>
								</p>
								<p class="table_msg" :title="table_msg.ana_exception">
									<span>{{table_msg.ana_exception}}</span>
								</p>
							</div>
							
							<div class='table_content last' style="width:10%;" >
								<p class="table_title">
									<span>操作</span>
								</p>
								<p class="table_msg" title="">
									<el-button type="text" class="table_move" @click="editClick()" v-if="BTN_type == 'arl'?true:false"><i class="el-icon-edit"> 更新</i></el-button>
								</p>
							</div>
						</div>
			        </el-collapse-item>
			    </el-collapse>
			</div>
		</div>
	</div>
	<div id="foot">
		<div id="number" class="fr">
			<div class="number_now fr">
				<!-- <el-pagination
				id="search_page"
				v-if="search_flag == true"
				@current-change="searchPageChange"
				:current-page="page"
				:page-size="page_size"
				layout="total, prev, pager, next,jumper"
				:total="changdu"
				></el-pagination> -->
				<el-pagination
				id="list_page"
				v-if="list_flag == true"
				@current-change="listPageChange"
				:current-page="page"
				:page-size="page_size"
				layout="total, prev, pager, next,jumper"
				:total="changdu"
				></el-pagination>
			</div>

		</div>
	</div>
	<arl_dialog  @dialog_close = "arl_dialog_return" @dialog_vue_close = "change1(change_params_id,change_params_index)" v-bind:input_show='HU_flag'  v-bind:input_arl_id="select_arl_id" v-bind:input_hu_id="select_hu_id">
	</arl_dialog>
</div>
</template>

<script >
import dialog from './dialog.vue'
require('../../assets/js/jquery-1.8.3.min.js')
export default{
components:{
	arl_dialog:dialog
},
data(){
	return {
		picture_falg:false,
		hmi_falg:true,
		change_params_id: '',
		change_params_index: '',
		fullscreenLoading:false,
		select_arl_id : "",
		select_hu_id : "",
		json:{
			user_id: '',
			type:'',
			category_id:'',
			condition:{}
		},
		input_value:'',
		msg:"更多",
		HU_flag:false,
		DEF_flag:false,
		list_flag: true,
		BTN_type:1,
		num: 0,
		show_flag:false,
		search_flag:false,
		names_flag:false,
		page:1,
		page_size:200,
		changdu:0,
		tabledata1: [],
		table1:[],
		arl_id:'',
		hu_id:'',
		cate_id:window.sessionStorage.getItem('b'),
		Maptree:false,
		Maplist:false,
		data:'',
		arr:[
		{value:"arl",label:"HU"},
		{value:"hu",label:"Screen画面"},
		],
		arr_v:"arl",
		checkAll:true,
		checkedC:[],
		cx:false,
		cy:true,
		isIndeterminate:false,
		Maptree:{},
		groups:[],
		info:'',
        form: {
          arl:[],
          user_id:'',
          group_id:'',
        },
        Id:0,
		userNames:"",
		names: [],
		complete_value:""
	}
},

mounted(){
	this.Id = Number(window.sessionStorage.getItem('admin'));
	this.Summary_ARL()
},
computed: {
	getUserIcons(){
		return this.$store.state.user_data
	}
},
watch: {
	getUserIcons(val){
		window.sessionStorage.setItem('b',val)
		this.cate_id = window.sessionStorage.getItem('b');
		this.num = -1
		this.Summary_ARL()
	}
},
methods:{
	search_user(command){
		this.List_search();
	},
	search_state(command){
		this.List_search();
	},
	arl_dialog_return(params){
		this.HU_flag = params[0];
	},
	hu_dialog_return(params){
		this.DEF_flag = params[0];
	},
	search_axios(size,page){
		this.json.type = this.BTN_type;
		this.json.size = size;
		this.json.page = page;
		this.Summary_axios(size,page)
	},
	// List_search(){
	// 	this.list_flag = false;
	// 	this.search_flag = true;
	// 	this.names_flag = false;
	// 	this.fullscreenLoading = true;
	// 	this.search_axios(200,1)
	// },
	Summary_axios(size,page){
		var name ='';
		var title=[];
		if(this.BTN_type=="arl"){
			this.picture_falg=false;
			this.hmi_falg=true;
			this.$axios.get(this.Ip+'/SummaryHmi/'+ this.cate_id+'/'+page+'/'+size).then(res=>{
				this.table1=[]
				this.table1=res.data.data;
				this.changdu = res.data.rowcount;
			}).catch(res=>{
				this.table1=[]
				this.changdu = 0;
			})
		}else if(this.BTN_type=="hu"){
			this.picture_falg=true;
			this.hmi_falg=false;
			this.$axios.post(this.Ip+'/Screen',{"page":page,"size":size}).then(res=>{
	
				this.table1=[]
				this.table1=res.data.content[1];
				this.changdu = res.data.content[0];
			}).catch(res=>{
				this.table1=[]
				this.changdu = 0;
			})
		}
	},
	Summary_ARL(){
		this.search_flag = false;
		this.list_flag = true;
		this.names_flag = false;
		this.page = 1;
		this.BTN_type = this.arr_v;
		this.Summary_axios(200,1)
	},
	listPageChange(val){
		this.BTN_type = this.arr_v;
		this.Summary_axios(200,val)
	},
	searchPageChange(val){
		var user_id = "";
		var group_id = "";
		this.BTN_type = this.arr_v;
		this.page = val;
		if(window.sessionStorage.getItem('workType')=="my"){
			this.search_axios(this.Id,0,200,this.page)
		}else if(window.sessionStorage.getItem('workType')=="group"){
			this.search_axios(0,window.sessionStorage.getItem('groups_id'),200,this.page)
		}else{
			this.search_axios(0,0,200,this.page)
		}
	},
	CheckedChange(value){
		let checkedCount = value.length;
		this.checkAll = checkedCount === this.table1.length;
		this.isIndeterminate = checkedCount > 0 && checkedCount < this.table1.length;
	},
	change1:function(id,index){
		this.num = index;
		var self=this;
		this.Map=false
		this.Maplist=true;
		this.Maptree=false;
		this.right_flag=false;
		this.list_flag=true;

		if(id!=""){
			this.select_hu_id = id
			if(this.BTN_type=="arl"){
				this.$axios.get(this.Ip+'/HmiDetailByID/'+id)
					.then(res => {
						this.tabledata1 = []
						this.tabledata1 = res.data.detail
					})
			}else{
				this.$axios.get(this.Ip+'/HmiDetailBySreenId/'+id)
					.then(res => {
						this.tabledata1 = []
						this.tabledata1 = res.data.detail
					})
			}	
		}
	},
	editClick(){
		this.HU_flag = true;
		$(".dialog_html").animate({height:785},800,function(){
			$(".arltable").eq(0).css({display:"block"})
		})
	},
	amint(){
		this.show_flag = true;
		var span_width = $(".span_width").width()
		$("#list").animate({left:span_width},1000)
	},
	back_up(){
		var this_=this;
		$("#list").animate({left:2000},1000,function(){
			this_.show_flag = false
		})
	}	
  }
}
</script>

<style scoped>
.el-dialog--small{
width: 80%;
}
#ARLlist{
position: relative;
height: 100%;
width: 100%;
overflow:hidden;
font-family: "微软雅黑";
font-size: 14px;
top:10px;
}
#treeMap{
position: absolute;
top:49px;
bottom: 49px;
left: 0;
width: 100%;
text-align: center;
font-size: 14px;
background: #fff;
}
.li_scroll{
list-style:none;
}
.ul_scroll{
width: 100%;
overflow-y:scroll;
height:770px;
overflow-x: hidden;
}
#foot{
position: absolute;
bottom: 0;
left: 0;
width: 100%;
height:50px;
line-height: 24px;
font-size: 14px;
background: #fff;
border-top: 1px solid #dfe6ec;
}
#ARLlist .BTN{
position: fixed;
z-index: 688;
left:16%;
width: 83%;
min-width: 1024px;
background-color: rgb(243,243,243);
}
#ARLlist .BTN #BTN_top{
background-color: white;
position: relative;
}
#BTN_top{
width: 100%;
padding-bottom: 5px;
border-bottom:  1px solid #dfe6ec;
height: 50px;
line-height:50px;
}
#ARLlist .BTN #BTN_title_top{
position: relative;
background-color: white;
height: 46px;
}
#ARLlist .BTN #BTN_num{
position: relative;
width:100%;
background-color: white;
}
#ARLlist .BTN #BTN_title_top #BTN_title_top_left{
position: absolute;
left: 0px;
top: 0px;
height: 46px;
line-height: 46px;
width: 210px;
text-align: center;
color: #20A0FF;
font-size: 20px;
}
#ARLlist .BTN #BTN_title_top #BTN_title_top_right{
position: absolute;
top: 0;
right: 0;
left: 210px;
height: 46px;
line-height: 46px;
text-align: center;
color: #20A0FF;
font-size: 20px;
}
#ARLlist .BTN .button_tree{
margin-left: 2px;
margin-right: 2px;
padding-left: 2px;
padding-right: 2px;
width: 118px;
text-align:center;;
}

#ARLlist .BTN .pi{
padding-left: 13px;
padding-right: 13px;
}
#Maptree{
position: absolute;
top: 14px;
left: 10px;
right: 0;
width: 750px;
height: 500px;
}
#Maplist{
position: absolute;
top: 11px;
left: 5px;
right: 0px;
z-index: 1000;
height: 100%;
overflow: scroll;
}
#list{
position: absolute;
left: 1700px;
width: 87.5%;
right: -47px;
top:50px;
bottom: 0;
background: #fff;
box-shadow: 0px 3px 10px rgba(0,0,0,.3);
z-index:999;
}

.li{
list-style: none;
width: 100%;
cursor: pointer;
height: 40px;
line-height:39px;
background-color: white;
margin-left: 0;
text-align: left;
border-bottom: 1px solid #dfe6ec;
min-width:770px;
}

.li:hover{
list-style: none;
cursor: pointer;
background-color: #EEF1F6;
position: relative;
}
#ARLlist #treeMap .li .cb{
float: left;
left: 5px;
}
#ARLlist #treeMap .li .cy{
float: left;
display: block;
width: 12.5%;

border-right: 1px solid #dfe6ec;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
}

.LTM{
background-color: white;
}
.active{
color:#42b983;
font-weight: bold;
}
.Asa_i{
position:absolute;
z-index: 50;
width: 130px;
height: 40px;
left:25px
}

.rightmenu_first{
width: 100%;
border: 0 none;
text-align: left;

}
#Map_List_title{
position: absolute;
bottom: 0;
left: 228px;
}
.treeMap_title{
width: 100%;
height: 40px;
background: #fff;
border-bottom:  1px solid #dfe6ec;
min-width: 1200px;
}
.treeMap_content{
margin-left: 60px;
width: 12.5%;
height:40px;
display: block;
line-height: 40px;
font-size:20px;
font-weight: bold;
float: left;
min-width: 185px;
}
.treeMap_caozuo{
margin-left: 60px;
height:40px;
float: left;
line-height: 40px;
font-size:20px;
font-weight: bold;
margin-left: 60px;
}
.treeMap_arl{
float: left;
min-width:400px;
width:65%;
}
.msy{
display: block;
text-align: center;
width:75%;
float: left;
border-right:1px solid #dfe6ec;
height:40px;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
}
.msg_msy{
display: block;
text-align: left;
width:95%;
float: left;
height:40px;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
margin-left:14px;
}
.cz{
width:12.5%;
height:40px;
float: left;
text-align: center;
line-height: 40px;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
color: #42b983
}
.ul{
overflow: hidden;
}
.fl{
float: left;
}
.fr{
float: right;
}
.input_search{
float: left;
margin-left: 10px;
margin-top: -1.4px;
}
.ID{
text-align: center;
font-size: 15px;
font-weight: bold;
color: #1f2d3d
}
.first_li{
border-top: 1px solid #dfe6ec;
overflow-y:scroll
}
.msg_caoz{
width:20%;
min-width:210px;
float: left;
}
.nav{
width: 100%;
height: 35px;
line-height: 35px;
}
.el-icon-d-arrow-right{
line-height: 35px;
margin-left: 15px;
font-weight: bold;
font-size: 20px;
cursor: pointer;
}
.el-icon-d-arrow-right:hover{
color: #42b983
}
.center{
display: block;
margin: 0 auto;
text-align: center;
color: #42b983;
font-size: 12px;
}



/*fenlichuqu*/
.el-dialog__body{
height: 730px;
}

.arl_table{
overflow:hidden;
height: 144px;
margin-right: 20px;
position:relative;
width:100%;
border:1px solid #dfe6ec;
}
.title_arl{
font-weight: bold;
height: 60px;
line-height: 60px;
}
.title_arl span{
cursor: pointer;
	margin-right: 30px;
}
.title_arl .fr:hover{
color: #42b983;
}
.hu_sapn span{
height: 30px;
line-height: 30px;
cursor: pointer;
margin-right: 30px;
}
.hu_sapn .fr:hover{
color: #42b983
}
.arltable{
position:relative;
width:100%;
border:1px solid #dfe6ec;
}
.arltable,.hutable,.tagltable,.tagl_table,.ana_table{
height: 169px;

}
.hutable{
position:relative;
width:100%;
border:1px solid #dfe6ec;
}
.table_content{
float: left;
width:245px;
border-right: 1px solid #dfe6ec;
height: 165px;
font-size: 14px;
background-color: white;
}
.table_title{
height: 30px;
line-height: 30px;
font-weight: bold;
text-align: center;
background:#eef1f6;
font-size: 14px;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
}
.table_msg{
margin: 5px;
overflow: hidden;
text-overflow: ellipsis;
height: 125px;
}
.table_move{
display: block;
margin:30% auto;
}
.dialog{
width: 100%;
height: 100%;
background:rgba(0,0,0,.3);
position: fixed;
top:0;
left: 0;
right: 0;
bottom: 0;
z-index:2000;
}
.dialog_html{
width: 80%;
margin: 0 auto;
height:0px;
margin-top:100px;
background: #fff;
border-radius: 2px;
box-shadow: 0 1px 3px rgba(0,0,0,.3);
padding:10px 10px 10px 20px;
}
.dialog_title{
width: 100%;
height: 45px;
line-height: 45px;
margin-bottom: 30px;
}
.el-icon-close{
line-height:45px;
cursor: pointer;
}
.el-icon-close:hover{
color: #42b983
}
.content_scroll{
overflow-y: scroll;
}
.option{
display: block;
width: 100%;
line-height: 25px;
}
.tagltable{
width: 100%;
border: 1px solid #dfe6ec;
}
.tagl_table{
width: 100%;
border: 1px solid #dfe6ec;
}
.ana_table{
width: 100%;
border: 1px solid #dfe6ec;
}
.center_{
margin: 0;
text-align: center;
width: 100%;
}
.number_now{
margin-right: 76px;
}
.user_name_title{
margin: 0 auto;
margin-left: 16px;

height: 30px;
line-height: 30px;
font-weight:bold;
font-size: 14px;
}
.msy>span{
font-size: 13px;
}
.user_icon{
width: 16px;
vertical-align: middle;
}
.change_time{
margin-right:10.2%;
}
.span_width{
	display:block;width:100%;height:100
}
.el-dropdown-menu{
overflow-y: scroll;
  max-height: 60%;
  height: auto;
}
</style>

