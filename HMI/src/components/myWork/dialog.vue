<template>
	<div class="dialog"  id="dialog" v-show="show" v-loading.fullscreen.lock="fullscreenLoading" element-loading-text="正在保存中,请稍等... ...">
		
			<dialog_hudef_relbasicreq  @dialog_close = "hu_dialog_return" v-bind:dialog_show='hu_relrequirement_show' v-bind:hu_data="hu_record"  v-bind:HMI_params="HMI_params">
		    </dialog_hudef_relbasicreq>
		    
		    <dialog_development_state  @dialog_close = "hu_dialog_return" v-bind:dialog_show='development_state_show' v-bind:hu_data="hu_record"  v-bind:HMI_params="HMI_params">
		    </dialog_development_state>
			
			<div class="dialog_html">
				<!-- dialog标题 -->
				<h2 class="dialog_title" style="margin:0">
					<span class="dialog_size fl">內容更新</span>
					<!-- 点x关闭弹出框 -->
					<i style="float: right;" class="fr el-icon-close close" @click="dialog_close()"></i>
				</h2>
				<!-- arl的新增保存等按钮，新增保存等功能都在这俩个地方加事件 -->
	   	    	<div style="height:40px;width:100%;marginRight:28px;lineHeight:40px;borderBottom:1px solid #dfe6ec"  class="hu_span">
	   	    		<span class="fr hu_span" style="fontWeight:bold;color:#42b983;"  @click="checkRull()"><i class="el-icon-upload2"> 保存</i></span>
	   	    	</div>
				<div class="arl_table">
		   	    	<div style="clear: both;"></div>	
					<div>
		    	     	<div style="marginLeft:15px" class="hu_div">
		    	     		<!-- hu的title  删除 复制功能皆开放 -->
			    	     	<div class="title_arl">
			    	     		<span class="fl"  @click="accordion(2,hu_index)"><i class="el-icon-arrow-right"></i>HU{{input_hu_id}}</span>
			    	     		<div style="float:right;height:40px;">
				    	     		<!--<el-dropdown>
										<span class="fr " style="display:block;fontWeight:normal;color:black;color:#42b983" id="menu_pr"><i class="el-icon-plus" id="el-icon-plus"></i> 新增</span>
										<el-dropdown-menu slot="dropdown">
											<el-dropdown-item>
												<span style="display:block;width:100%;height:100%;fontSize:12px" @click="hu_new(hu_index)">HMI</span>
											</el-dropdown-item>
										</el-dropdown-menu>
									</el-dropdown>-->
			    	     		</div>
			    	     	</div>
			    	     	<!-- 只显示重要的信息 ，同理arl-->
			    	     	<div class="hutable hu_table">
			    	     		<div class='table_content' style="width:100px">
			    	     			<p class="table_title">
			    	     				<span>ScreenID</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover"   @dblclick="hu_select_item( hu_index, dialog_hudef_relbasicreq,Array_HMI_params[0])" >
			    	     			    <span>{{hu_record.screen_id}}</span> 
			    	     			</p>
			    	     		</div>
			    	     		<div class='table_content' style="width:262px">
			    	     			<p class="table_title">
			    	     				<span>APL是否为大连对应</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item( hu_index, dialog_development_state,Array_HMI_params[1])" >
			    	     			    <span>{{hu_record.is_dalian}}</span> 
			    	     			</p>
			    	     		</div>
			    	     		<div class='table_content' style="width:190px">
			    	     			<p class="table_title">
			    	     				<span>负责人</span>
			    	     			</p>			    	     			
			    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item( hu_index, dialog_hudef_relbasicreq,Array_HMI_params[2])" >
			    	     			    <span>{{hu_record.charger}}</span> 
			    	     			</p>
			    	     		</div> 
			    	     		<div class='table_content' style="width:200px">
			    	     			<p class="table_title">
			    	     				<span>担当</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[3])" >
			    	     			    <span>{{hu_record.author}}</span> 
			    	     			</p>
			    	     		</div>
								<!-- 这个是显示全部信息的  ，点击操作更多  让其显示  -->
								<div class='table_content' style="width:180px">
			    	     			<p class="table_title">
			    	     				<span>APL日程</span>
			    	     			</p>
			    	     			<!-- 6个option  如果option是默认选项则只显示システム構成 -->
			    	     			<p class="table_msg content_scroll table_msg_hover"  @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[4])" >
			    	     			    <span>{{hu_record.apl_schedule}}</span> 
			    	     			</p>
			    	     		</div>
			    	     		
			    	     		<div class='table_content' style="width:180px">
			    	     			<p class="table_title">
			    	     				<span>结合日程</span>
			    	     			</p>
			    	     			<!-- 6个option  如果option是默认选项则只显示システム構成 -->
			    	     			<p class="table_msg content_scroll table_msg_hover"  @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[5])" >
			    	     			    <span>{{hu_record.it_schedule}}</span> 
			    	     			</p>
			    	     		</div>
			    	     		
			    	     		<div class='table_content_hidden' style="width:180px">
			    	     			<p class="table_title">
			    	     				<span>APL进度</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[6])" >
			    	     			    <span>{{hu_record.apl_progress}}</span> 
			    	     			</p>
			    	     		</div>   
								<div class='table_content_hidden'>
			    	     			<p class="table_title">
			    	     				<span>结合测试进度</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[7])" >
			    	     			    <span>{{hu_record.it_progress}}</span> 
			    	     			</p>
			    	     		</div> 
								<div class='table_content_hidden'>
									<p class="table_title">
										<span>结合测试Release版本</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[8])" >
			    	     			    <span>{{hu_record.it_release_ver}}</span> 
			    	     			</p>
								</div>
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>开发状态</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(hu_index, dialog_development_state,Array_HMI_params[9])" >
			    	     			    <span>{{hu_record.dev_status}}</span> 
			    	     			</p>
                                </div>
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>备考</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[10])" >
			    	     			    <span>{{hu_record.dev_remark}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>外部QA番号</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[11])" >
			    	     			    <span>{{hu_record.external_qa}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>内部QA番号</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[12])" >
			    	     			    <span>{{hu_record.internal_qa}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>NG次数</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(hu_index, dialog_hudef_relbasicreq,Array_HMI_params[13])" >
			    	     			    <span>{{hu_record.ng_num}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>Step</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover lock_show" >
			    	     			    <span>{{hu_record.step}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>tagl要件定義ID</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover lock_show" >
			    	     			    <span>{{hu_record.definition_id}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>uniqueID</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover lock_show">
			    	     			    <span>{{hu_record.ana_unique_id}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>時序図</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover lock_show" >
			    	     			    <span>{{hu_record.seq_diagram_file}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>Application</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover lock_show" >
			    	     			    <span>{{hu_record.application}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>除外</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover lock_show" >
			    	     			    <span>{{hu_record.ana_exception}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>是否代表要件</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover lock_show" >
			    	     			    <span>{{hu_record.is_represent_req}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>親代表要件</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover lock_show" >
			    	     			    <span>{{hu_record.parent_rep_req}}</span> 
			    	     			</p>
                                </div>
                                
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>新建日期</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover lock_show" >
			    	     			    <span>{{hu_record.new_date}}</span> 
			    	     			</p>
                                </div>
                                
			    	     		<div class='table_content' style="width:122px;border:0 none">
			    	     			<p class="table_title">
			    	     				<span></span>
			    	     			</p>
			    	     			<p class="table_msg table_msg_hover" title="">
			    	     				<el-button type="text" class="table_move" @click="show_more(2,hu_index)"><i class="el-icon-d-arrow-right"></i></el-button>
			    	     			</p>
			    	     		</div>
			    	     	</div>
		    	     	</div>  
					</div> 
		   	   	</div>
			</div>
	</div>
</template>
<script>
import Dialog_HUDef_RelBasicReq from './Dialog_HUDef_RelBasicReq'
import Dialog_Development_State from './Dialog_Development_State'
require('../../assets/js/jquery-1.8.3.min.js')
export default{
    props: ['input_show', 'input_arl_id', 'input_hu_id'], 

	components:{
		dialog_hudef_relbasicreq : Dialog_HUDef_RelBasicReq,
		dialog_development_state :Dialog_Development_State
	},
	data(){
		return{
			Array_HMI_params: ['ScreenID','APL是否为大连对应','负责人','担当','APL日程','结合日程','APL进度','结合测试进度','结合测试Release版本','开发状态','备考','外部QA番号','内部QA番号','NG次数',
							   'Step','tagl要件定義ID','uniqueID','時序図','Application','除外','是否代表要件','親代表要件','新建日期'],
			HMI_params:'',
			hu_list_num: 0,
			save_array: [],
			open_array: [],
			arl_tree_copy:[],
			dialog_open_data: '',
			dialog_save_data: '',
			
            show : false,
            arl_id : "",
            hu_id : "",
            select_item_name : '',    // select
            arl_index : 0,       // select index
            hu_index : 2,        // select index
            tagl_index : 0,      // select index
            taglana_index: 0,
            arl_tree : {},
            data_before_save: [],
            hu_record : {},
            tagl_record : {},
          	arl_system_conf:"",
          	
            dialog_hudef_relbasicreq : "hu_relrequirement",
            hu_relrequirement_show : false,  

			dialog_development_state : 'dialog_development_state',
			development_state_show : false,  
			
 			user_group_value:[],
 			HU_stuate_flog:false,
 			TAGLDef_stuate_flog:false,
 			TAGLAna_stuate_flog:false,
 			options:[
 			{
				value:1,
				label:'初始狀態，待作業',
				disabled:true,
			},
			{
				value:2,
				label:'作業完了，待确认',
				disabled:true,
			},
 			{
 				value:3,
 				label:'确认完了',
 				disabled:true,
 			},
 			],
 			fullscreenLoading:false,
 			Roles:"Member", 	
 			options_names:[],
 			leadGp:[],
 			p_list:[],
 			old_group:'',
		}
	},
	mounted(){
		
	},
	computed:{

	},
	methods:{
		request_HMI_data(){
			this.$axios.get(this.Ip+'/HmiDetailByID/' + this.input_hu_id)
				.then(res => {
					this.hu_record = res.data.detail[0]
					this.dialog_open_data = JSON.stringify(this.hu_record)
				})
				.catch(res=>{
					this.$emit('dialog_close', [false]);
					this.$notify({
						type:'error',
						message:'网络异常，请重新刷新',
						showClose:true,
						duration:'0',
					})
					this.hu_record={};
					
				});
		},
		onshow () { 
			this.request_HMI_data()
			this.show = true;
		},
		checkRull(){
			this.fullscreenLoading = true
			let array_save_post = []
			let object_data = {}
			object_data = JSON.parse(JSON.stringify(this.hu_record))
			object_data.user_id = window.sessionStorage.getItem('admin')
			array_save_post.push(object_data)
			this.$axios.post(this.Ip + '/HmiFullContent',array_save_post)
			.then(res => {
				this.$notify({
					type:'success',
					message:'保存成功',
					showClose:true,
					duration:'0',
				})
				this.request_HMI_data()
				this.fullscreenLoading = false
			})
			.catch(res => {
				this.fullscreenLoading = false
				this.$notify({
					type:'error',
					message:'网络异常，请重新刷新',
					showClose:true,
					duration:'0',
				})
			})
		},
		show_more(table_id,index,definition_index,taglana_index) {
			var _this = this;
			if($(".hu_table").eq(0).children(".table_content_hidden").css("display")=="none"){
				$(".hu_table").eq(0).children(".table_content_hidden").css({"display":"block"})
				$(".hu_table").eq(0).animate({width:4296,},800, function(){});
				$(".hu_table").eq(0).find(".el-icon-d-arrow-right").eq(0).removeClass().addClass("el-icon-d-arrow-left");
			}else{
				$(".hu_table").eq(0).animate({width:1236},200, function() {
	            $(".hu_table").eq(0).children(".table_content_hidden").css({"display":"none"})
	            $(".hu_table").eq(0).find(".el-icon-d-arrow-left").eq(0).removeClass().addClass("el-icon-d-arrow-right");
	   		 });
			}  
		},
		hu_select_item(ret_hu_index, select_item,HMI_params) {
            this.hu_index = ret_hu_index;
            this.hu_data = this.hu_record;
            this.select_item_name = select_item;
            this.HMI_params = HMI_params;
            switch (this.select_item_name){
            	case this.dialog_hudef_relbasicreq:
            		this.hu_relrequirement_show = true; 
            		break;
            	case this.dialog_development_state:
            		this.development_state_show = true; 
            		break;	
            	default:
            		break;
            }
		},
        hu_dialog_return (params) {
        	if (params[0]) {
        		this.hu_record = params[1]
        	}
			this.development_state_show = false; 
	        this.hu_relrequirement_show = false; 
        },
        //获取当前日期
        formatDate(date){
			var y = date.getFullYear();
			var m = date.getMonth()+1;
			m = m< 10 ? '0' + m : m;
			var d = date.getDate();
			d = d <10 ? ('0'+d) : d;
			return  y + '-' + m + '-' + d;
        },
        hu_new() {
        	if(this.Roles=="Translator"){
        		this.$notify({
					type:'error',
					message:'您的权限不足，无法保存',
					showClose:true,
					duration:'0',
				})
        		
        	}else{
        		if(this.Roles=="Admin"||this.Roles=="PL"){
        			var hu_record_new = {   "lock_status" : 0,"agree_flag": null, "amp": "0", "arl_id": "", "author": "SUNTEC", "common_chapter": "-", "common_cmd_guide": "-", 
									"common_opc": "-", "common_seq_no": "-", "common_seq_spec": "-", "complete_flag": 0, "dcm": "0", 
									"definition_list": [], "dsrc": "0",  "exception": null, "future_req": '○', "has_problem": null ,
									"hu_id": "", "hu_record_id": 0, "inter_chapter": "-", "inter_loc_spec": "-", "last_modifier": null,  
									"leak_check": null, "major_ver": null, "md5_key": null, "new_date":"", "other_chapter": "-", "point_list":[],
									"other_doc": "-", "reason": "\u65b0\u898f\u8ffd\u52a0","rel_requirement": null,"basic_req": null, "remark": null, 
									"remark1": null, "remark2": null, "rse": "0", "separate_disp": "0", "sequence_list": [], 
									"small_ver": null, "sys_spec_chapter": "44", "system_conf": "ALL0", "test_results": null, 
									"title": "", "touch_pad": "0", "translation_flag": null, "unique_id": 0, "user_id": null,"hu_option":[{value:1,label:'初始狀態，待作業',disabled:false,},{value:2,label:'作業完了，待确认',disabled:false,},{value:3,label:'确认完了',disabled:false,},],"job_status":1,};
        		}else{
        			var hu_record_new = {   "lock_status" : 0,"agree_flag": null, "amp": "0", "arl_id": "", "author": "SUNTEC", "common_chapter": "-", "common_cmd_guide": "-", 
									"common_opc": "-", "common_seq_no": "-", "common_seq_spec": "-", "complete_flag": 0, "dcm": "0", 
									"definition_list": [], "dsrc": "0",  "exception": null, "future_req": '○', "has_problem": null ,
									"hu_id": "", "hu_record_id": 0, "inter_chapter": "-", "inter_loc_spec": "-", "last_modifier": null,  
									"leak_check": null, "major_ver": null, "md5_key": null, "new_date":"", "other_chapter": "-", "point_list":[],
									"other_doc": "-", "reason": "\u65b0\u898f\u8ffd\u52a0","rel_requirement": null,"basic_req": null, "remark": null, 
									"remark1": null, "remark2": null, "rse": "0", "separate_disp": "0", "sequence_list": [], 
									"small_ver": null, "sys_spec_chapter": "44", "system_conf": "ALL0", "test_results": null, 
									"title": "", "touch_pad": "0", "translation_flag": null, "unique_id": 0, "user_id": null,"hu_option":[{value:1,label:'初始狀態，待作業',disabled:false,},{value:2,label:'作業完了，待确认',disabled:false,},{value:3,label:'确认完了',disabled:true,},],"job_status":1,};
        		}

	            var time = new Date();
				hu_record_new["new_date"] =  this.formatDate(time);
				
	            hu_record_new["arl_id"] = this.arl_tree[0].arl_id;
	            hu_record_new["title"] = "HU要件定義: "+this.arl_tree[0].arl_id+'.'+this.arl_tree[0].hu_list.length;
	            hu_record_new["hu_id"] = this.arl_tree[0].arl_id+'.'+this.arl_tree[0].hu_list.length;
	            this.arl_tree[this.arl_index].hu_list.push(hu_record_new);
	            this.$notify({
					type:'success',
					message:'新增成功',
					showClose:true,
					duration:'0',
				})
        	}
        	
        },
        hu_copy(index){
          	var hu_record_copy =JSON.parse(JSON.stringify(this.arl_tree[this.arl_index].hu_list[index]))
          	hu_record_copy.definition_list = []
          	hu_record_copy["title"] = "HU要件定義: "+this.arl_tree[0].arl_id+'.'+this.arl_tree[0].hu_list.length;
          	hu_record_copy["lock_status"] = 0
        	this.arl_tree[this.arl_index].hu_list.push(hu_record_copy);
        	this.$notify({
					type:'success',
					message:'复制成功'
				})
        },
        hu_delete(del_hu_index) {
        	//删除只有组长及以上级别有权限，其他均无
        	if(this.Roles=="Admin"||this.Roles=="PL"||this.Roles=="Leader"){
				if(this.arl_tree[0].hu_list[del_hu_index].lock_status == 1 || this.arl_tree[0].hu_list[del_hu_index].lock_status == 2){
	            	return
	            }
	        	this.$confirm('此操作将永久删除数据，是否继续?','提示',{
	        		confirmButtonText:"确定",
	        		cancelButtonText:"取消",
	        		type:'warning'
	        	}).then(()=>{
	        		if(this.arl_tree[this.arl_index].hu_list[del_hu_index].definition_list!=""){
						this.$alert("该条 HU要件定義 下含有 TAGL要件定義，不可删除")
					}else{
						var hu_tmp = [];
				    	var hu_num = this.arl_tree[this.arl_index].hu_list.length;
				    	if (del_hu_index + 1 > hu_num) {
				            return;
				    	};
						for (var i = hu_num - 1; i > del_hu_index; i-- ) {
				             hu_tmp.push(this.arl_tree[this.arl_index].hu_list.pop());
						};
						this.arl_tree[this.arl_index].hu_list.pop();
						for (var j = (hu_tmp.length - 1); j >= 0  ; j--) {
				             this.arl_tree[this.arl_index].hu_list.push(hu_tmp[j]);
						};
						this.get_save_array()
					}
	        	}).catch(() => {
				    	
				    })
			}else{
				this.$notify({
					type:'error',
					message:'您的权限不足，无法删除',
					showClose:true,
					duration:'0',
				})
			}   
        },
		dialog_close() {
			this.dialog_save_data = JSON.stringify(this.hu_record)
			var this_ = this;
			if(this.dialog_save_data == this.dialog_open_data){
				$(".dialog_html").animate({height:0},500,function(){
					this_ .show = false;
					$(".arltable").css({display:"block"})
					$(".hu_table").css({display:"block"})
					$(".tagltable").css({display:"block"})
					$(".taglana_table").css({display:"block"})
				});
				this.$emit('dialog_close', [false]);
			}else{	
				this.$confirm('您有未提交的内容，确定离开?','提示',{
			    		confirmButtonText:"确定",
			    		cancelButtonText:"取消",
			    		type:"warning"
			    })
				.then(() => {
					$(".dialog_html").animate({height:0},500,function(){
						this_ .show = false;
						$(".arltable").css({display:"block"})
						$(".hu_table").css({display:"block"})
						$(".tagltable").css({display:"block"})
						$(".taglana_table").css({display:"block"})
					});
					this.$emit('dialog_close', [false]);	
			  }).catch(() => {
			    	
			    })
			}
		},
		accordion(table_id,hu_index,definition_index,taglana_index){
			if(table_id==1){
				$(".arltable").eq(0).toggle(function(){
					
				})
			}else if(table_id==2){
				$(".hu_table").eq(hu_index).toggle(function(){})
			}else if(table_id==3){
				$(".hu_div").eq(hu_index).children(".tagl_div").eq(definition_index).children(".tagltable").eq(0).toggle(function(){})
			}else if(table_id==4){
				$(".hu_div").eq(hu_index).children(".tagl_div").eq(definition_index).children(".taglana_div").eq(taglana_index).children(".taglana_table").eq(0).toggle(function(){})
			}
		}, 
	},
	watch:{
	    input_show(v) {
            if (this.input_show) {
                this.onshow();
            }else{
            	
            }
	    }
    },
}
</script>
<style scoped>
.dialog{
	font-family: "微软雅黑"
}
.arl_table{
	overflow: scroll;
	height:90%;	
}
.title_arl{
	font-weight: bold;
	height: 40px;
	line-height: 40px;
	background: rgba(238,241,246,.2);
	transition: 0.9s;
	width: 99.35%;
}
.title_arl:hover{
	background: rgba(238,241,246,.6);
}
.title_arl>div>span{
	font-weight: normal;
}
.title_arl span{
	cursor: pointer;
	margin-right:20px;
}
.title_arl img{
	cursor: pointer;
}
.title_arl .fr:hover{
	color: #42b983;
}

.hu_span span{
	height: 40px;
	line-height: 40px;
	cursor: pointer;
	margin-right:20px;
}
.hu_span .fr:hover{
	color: #42b983;
}
.arltable{
	position:relative;
	width:1250px;
	border:1px solid #dfe6ec;
}
.arltable,.hutable,.tagltable,.taglana_table{
	height: 170px;
	margin-right: 20px;
	border: 1px solid #dfe6ec;
	display: block;
}
.taglana_table{
	width: 1206.3px;
}
.hutable{
	position:relative;
	width:1236px;
	border:1px solid #dfe6ec;
	margin-right: 20px;
}
.table_content{
	float: left;
	width:200px;
	border-right: 1px solid #dfe6ec;
	height:169px; 
}
.table_content_hidden{
	float: left;
	width:180px;
	border-right: 1px solid #dfe6ec;
	height: 150px;
	display: none;
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

.fl{
	float: left;
}
.fr{
	float: right;
}
.table_msg{
	padding:5px;
	overflow: hidden;
	/*text-overflow: ellipsis;*/
	/*white-space: nowrap;*/
	height: 130px;
	font-size: 12px;
}
.table_msg_hover{
	box-shadow: 1px 1px 1px #9a9a9a;
	-webkit-box-shadow: 1px 1px 1px #9a9a9a;
    margin: 4px 4px 0 4px;
}

.table_move{
	display: block;
	color: #42b983;
	margin:0 auto;
	margin-top: 30px;
}.dialog{
	width: 100%;
	height: 100%;
	background:rgba(0,0,0,.3);
	position: fixed;
	top:0;
	left: 0;
	right: 0;
	bottom: 0;
	z-index:1000;
}
.dialog_html{
	width: 67.5%;
	margin: 0 auto;
	height:0px;
	margin-top:5%;
    background: #fff;
    border-radius: 2px;
    box-shadow: 0 1px 3px rgba(0,0,0,.3);
    padding:10px 10px 10px 20px;
}
.dialog_title{
	width: 100%;
	height: 30px;
	line-height: 30px;
}
.dialog_size{
	font-size: 18px;
}
.close{
	font-size: 14px;
	line-height:45px;
	cursor: pointer;
}
.el-icon-close:hover{
	color: #42b983
}
.content_scroll{
	overflow-y:scroll;
}
.option{
	display: block;
	width: 100%;
	line-height: 25px;
}
.tagltable{
	width: 1221px;
	border: 1px solid #dfe6ec;
}

.tagl_table{
	width: 1376px;
	border: 1px solid #dfe6ec;
}
.new_menu{
	position: absolute;
	z-index: 2400;
	width: 80%;
	height:80px;
	box-shadow: 2px 2px 8px #bbb;
	top: 40px;
	left:0;
	display:block;
	background: #fff;
	/*opacity: 0;*/
}
.new_menu>span{
	font-weight: normal;
	display: block;
	margin:0;
	padding: 0 10%;
}
.new_menu span:hover{
	background-color: #eef1f6
}
.tagl_menu{
	z-index: 2400;
	width: 80%;
	height:80px;
	box-shadow: 2px 2px 8px #bbb;
	top: 40px;
	left:0;
	display:block;
	background: #fff; 
	position: absolute;
}
.tagl_menu>span{
	font-weight: normal;
	display: block;
	margin:0;
	padding: 0 10%;
}
.tagl_menu>span:hover{
	background-color: #eef1f6
}

.lock_show{
	background-color: #fbfdff;
}
</style>
