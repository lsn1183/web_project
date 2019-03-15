<template>
	<div class="dialog"  id="dialog" v-show="show" v-loading.fullscreen.lock="fullscreenLoading" element-loading-text="正在保存中,请稍等... ...">		    
			<!--TAGL要件分析的弹窗-->
 		     <dialog_taglana_reason @dialog_close = "taglana_dialog_return" v-bind:dialog_show='tagl_ana_reason_show' v-bind:tagl_ana_data="tagl_record">		     	
		     </dialog_taglana_reason>

		     <dialog_taglana_seqdiagram @dialog_close = "taglana_dialog_return" v-bind:dialog_show='tagl_ana_seqdiagram_show' v-bind:tagl_ana_data="tagl_record">		     	
		     </dialog_taglana_seqdiagram>

			 <dialog_taglana_other @dialog_close = "taglana_dialog_return" v-bind:dialog_show='tagl_ana_other_show' v-bind:tagl_ana_data="tagl_record">	
			 </dialog_taglana_other>

			 <dialog_taglana_worker @dialog_close = "taglana_dialog_return" v-bind:dialog_show='tagl_ana_worker_show' v-bind:tagl_ana_data="tagl_record">
			 </dialog_taglana_worker>

			 <dialog_taglana_relbasicreq  @dialog_close = "taglana_dialog_return" v-bind:dialog_show='tagl_ana_relrequirement_show' v-bind:tagl_ana_data="tagl_record">
		    </dialog_taglana_relbasicreq>

		    <dialog_taglana_basicreq  @dialog_close = "taglana_dialog_return" v-bind:dialog_show='tagl_ana_basicreq_show' v-bind:tagl_ana_data="tagl_record">
		    </dialog_taglana_basicreq>

			 <dialog_taglana_point @dialog_close = "taglana_dialog_return" v-bind:dialog_show='tagl_ana_point_show' v-bind:tagl_ana_data="tagl_record">
			 </dialog_taglana_point>
			
			<dialog_taglana_reqpost @dialog_close = "taglana_dialog_return" v-bind:dialog_show='tagl_ana_reqpost_show' v-bind:tagl_ana_data="tagl_record">
			 </dialog_taglana_reqpost>
			
			<div class="dialog_html">
				<!-- dialog标题 -->
				<h2 class="dialog_title" style="margin:0">
					<span class="dialog_size fl">內容更新</span>
					<!-- 点x关闭弹出框 -->
					<i style="float: right;" class="fr el-icon-close close" @click="dialog_close()"></i>
				</h2>
				<!-- arl的新增保存等按钮，新增保存等功能都在这俩个地方加事件 -->
	   	    	<div style="height:40px;width:100%;marginRight:28px;lineHeight:40px;borderBottom:1px solid #dfe6ec"  class="hu_span">
	   	    		<span class="fr hu_span" style="fontWeight:bold;color:#ccc;"><i class="el-icon-upload2"> 目前无法保存</i></span>
	   	    		<!--<span class="fr hu_span" style="fontWeight:bold;color:#42b983;"  @click="checkRull()"><i class="el-icon-upload2"> 保存</i></span>-->
	   	    	</div>
				<div class="arl_table">
		   	    	<div style="clear: both;"></div>
	    	     	<!-- TAGLANA表格 -->
	    	     	<div style="marginLeft:15px;" v-for="(taglana_record,taglana_index) in tabledata1" class="taglana_div">
 		    	    	<div class="title_arl" >
 		    	     		<span class="fl"  @click="accordion(4,taglana_index)"><i class="el-icon-arrow-right"></i>{{taglana_record.title}}</span>
 		    	     		<img src="../../assets/img/lock_2.png" alt="闭锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;" v-show="taglana_record.lock_status == 1?true:false" @click="lock_Ana(taglana_record.lock_status,taglana_index)"/>
		 					<img src="../../assets/img/unlock_2.png" alt="开锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;"v-show="taglana_record.lock_status == 0?true:false" @click="lock_Ana(taglana_record.lock_status,taglana_index)"/>
		 					<span class="fl" style="marginLeft: 26px;">
 		    	     			任務状態
 		    	     			<template>
 		    	     				<el-select v-model="taglana_record.job_status" placeholder="请选择" :disabled="TAGLAna_stuate_flog||taglana_record.lock_status?true:false" style="width:135px;">
 		    	     					<el-option v-for="item in taglana_record.ana_option" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled"></el-option>
 		    	     				</el-select>
 		    	     			</template>
 		    	     		</span>
 		    	     		<!--<div style="float: right;">
 								<span class="fr" style="color:#42b983" @click="taglana_delete(taglana_index)" v-if="taglana_record.lock_status == 0?true:false"><i class="el-icon-delete" disabled> 删除</i></span>
 								<span class="fr" style="color:#bfcbd9" @click="taglana_delete(taglana_index)" v-if="taglana_record.lock_status == 1?true:false"><i class="el-icon-delete" disabled> 删除</i></span>
 		    	     		</div>-->
 		    	     	</div>
		    	    	<div class="taglana_table"  :class="taglana_record.lock_status == 1?'lock_show':''">
		    	    		<div class='table_content' style="width:200px">
		    	    			<p class="table_title">
		    	    				<span>シーケンス図</span>
		    	    			</p>
		    	    			<p class="table_msg table_msg_hover content_scroll" title="" style="textAlign:center" @dblclick="taglana_select_item(taglana_index,dialog_taglana_seqdiagram)" :class="taglana_record.lock_status == 1?'lock_show':''">
		    	    			    {{taglana_record.seq_diagram}}  
		    	    			</p>
		    	    		</div>
		    	    		<div class='table_content' style="width:200px">
		    	     			<p class="table_title">
		    	     				<span>転記内容</span>
		    	     			</p>			
		    	     			<!--只有ID为B、C、D开头的taglana才可编辑转记-->
		    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="taglana_select_item(taglana_index, dialog_taglana_reqpost)" :class="taglana_record.lock_status == 1||(taglana_record.definition_id.substring(0,1) != 'B' &&'C' && 'D')?'lock_show':''">
									<span class="option" style="fontWeight:bold">TAGL要件定義ID:	
										<span style="fontWeight:normal">{{taglana_record.definition_id}}</span>
									</span>
									<span class="option" style="fontWeight:bold">大分類:	
										<span style="fontWeight:normal">{{taglana_record.major_category}}</span>
									</span>
									<span class="option" style="fontWeight:bold">中分類:	
										<span style="fontWeight:normal">{{taglana_record.medium_category}}</span>
									</span>
									<span class="option" style="fontWeight:bold">小分類:	
										<span style="fontWeight:normal">{{taglana_record.small_category}}</span>
									</span>
									<span class="option" style="fontWeight:bold">詳細:	
										<span style="fontWeight:normal">{{taglana_record.detail}}</span>
									</span>
									<!--<span class="option" style="fontWeight:bold">基本要件:	
										<span style="fontWeight:normal">{{taglana_record.basic_req}}</span>
									</span>-->
									<!--<span class="option" style="fontWeight:bold">関連基本要件:	
										<span style="fontWeight:normal">{{taglana_record.rel_requirement}}</span>
									</span>-->
								</p>
		    	     		</div>
		    	    		<div class='table_content' style="width:432px">
		    	     			<p class="table_title">
		    	     				<span>TAGL-PF</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="taglana_select_item(taglana_index, dialog_taglana_worker)" :class="taglana_record.lock_status == 1?'lock_show':''">
		    	     				<span v-for="(analist_record, analist_index) in taglana_record.sequence_list">
		    	     					<span class="option" style="fontWeight:bold">({{analist_index+1}})</br>設備:
			    	     					<span style="fontWeight:normal" v-if="analist_record.name!=''">{{analist_record.name}}</span>
			    	     					<span style="fontWeight:normal" v-if="analist_record.info!=''">({{analist_record.info}})</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">状態:
			    	     					<span style="fontWeight:normal">{{analist_record.status}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">トリガー:
			    	     					<span style="fontWeight:normal">{{analist_record.trigger}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">動作:
			    	     					<span style="fontWeight:normal">
			    	     						{{analist_record.action}}
			    	     					</span>
			    	     				</span>
		    	     				</span>
		    	     			</p>
		    	     		</div>
		    	    		<div class='table_content' style="width:250px">
		    	     			<p class="table_title">
		    	     				<span>变更理由与日期</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" :title="taglana_record.reason" @dblclick="taglana_select_item(taglana_index, dialog_taglana_reason)" :class="taglana_record.lock_status == 1?'lock_show':''">
		    	     				<span class="option" style="fontWeight:bold">变更理由:	
										<span style="fontWeight:normal">{{taglana_record.reason}}</span>
									</span>
									<span class="option" style="fontWeight:bold">日付:	
										<span style="fontWeight:normal">{{taglana_record.new_date}}</span>
									</span>
								</p>
		    	     		</div>
		    	     		<div class='table_content_hidden' style="width:200px">
		    	     			<p class="table_title">
		    	     				<span>指摘</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" :class="taglana_record.lock_status == 1 || taglana_record.point_list.length == 0 ?'lock_show':''" @dblclick="taglana_select_item(dialog_taglana_point)" v-if="taglana_record.point_list.length !=0?true:false">
 						    	   	<span v-for="(point_record, point_index) in taglana_record.point_list" >
			    	     				<span class="option" style="fontWeight:bold">({{point_index+1}})<br />指摘拿到日:
											<span style="fontWeight:normal" v-html="point_record.point_date"></span>
										</span>
										<span class="option" style="fontWeight:bold">レビュー結果:	
											<span style="fontWeight:normal" v-html="point_record.review_result"></span>
										</span>
										<span class="option" style="fontWeight:bold"> 指摘No:
											<span style="fontWeight:normal" v-html="point_record.pointout_no"></span>
										</span>
										<span class="option" style="fontWeight:bold">ステータス:
											<span style="fontWeight:normal" v-html="point_record.pointout_status"></span>
										</span>
										<span class="option" style="fontWeight:bold"> コメント:
											<span style="fontWeight:normal" v-html="point_record.pointout_comment"></span>
										</span>
										<span class="option" style="fontWeight:bold"> リーダチェック:
											<span style="fontWeight:normal" v-html="point_record.reader_check"></span>
										</span>
										<span class="option" style="fontWeight:bold"> リーダ２チェック:
											<span style="fontWeight:normal" v-html="point_record.reader2_check"></span>
										</span>
										<span class="option" style="fontWeight:bold"> 最終チェック:
											<span style="fontWeight:normal" v-html="point_record.final_check"></span>
										</span>
										<span class="option" style="fontWeight:bold"> 担当:
											<span style="fontWeight:normal" v-html="point_record.pointout_charger"></span>
										</span>
										<span class="option" style="fontWeight:bold"> 優先度:
											<span style="fontWeight:normal" v-html="point_record.pointout_priority"></span>
										</span>
										<span class="option" style="fontWeight:bold"> 指摘提出日:
											<span style="fontWeight:normal" v-html="point_record.pointout_date"></span>
										</span>
										<span class="option" style="fontWeight:bold"> Suntecステータス:
											<span style="fontWeight:normal">{{point_record.suntec_status}}</span>
										</span>
										<span class="option" style="fontWeight:bold"> 修正済み:
											<span style="fontWeight:normal">{{point_record.fixed}}</span>
										</span>
										<span class="option" style="fontWeight:bold"> Suntec備考:
											<span style="fontWeight:normal">{{point_record.suntec_remark}}</span>
										</span>
										<span class="option" style="fontWeight:bold">ARL関連指摘:
											<span style="fontWeight:normal" v-html="point_record.arl_rel"></span>
										</span>
										<span class="option" style="fontWeight:bold"> Suntec修正不可:
											<span style="fontWeight:normal">{{point_record.suntec_cannot_modify}}</span>
										</span>
			    	     			</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" :class="taglana_record.lock_status == 1 || taglana_record.point_list.length == 0 ?'lock_show':''" v-if="taglana_record.point_list.length ==0?true:false">
			    	     				
		    	     			</p>
		    	     		</div>
		    	     		<div class='table_content_hidden' style="width:250px">
		    	     			<p class="table_title">
		    	     				<span>関連基本要件</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" :title="taglana_record.rel_requirement" @dblclick="taglana_select_item(taglana_index, dialog_taglana_relbasicreq)" :class="taglana_record.lock_status == 1?'lock_show':''">
		    	     			
		    	     			    <span>{{taglana_record.rel_requirement}}</span> 
		    	     			</p>
		    	     		</div>
		    	     		<div class='table_content_hidden' >
		    	     			<p class="table_title">
		    	     				<span>基本要件</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" :title="taglana_record.basic_req" @dblclick="taglana_select_item(taglana_index, dialog_taglana_basicreq)"  :class="taglana_record.lock_status == 1?'lock_show':''">
		    	     			
		    	     			    <span>{{taglana_record.basic_req}}</span> 
		    	     			</p>
		    	     		</div> 

                            <div class='table_content_hidden' >
							    <p class="table_title">
									<span>其他</span>
								</p>
								<p class="table_msg table_msg_hover content_scroll" @dblclick="taglana_select_item(taglana_index, dialog_taglana_other)" :class="taglana_record.lock_status == 1?'lock_show':''">
								    <span class="option" style="fontWeight:bold"> 担当:
								        <span>{{taglana_record.author_name}}</span> 
								    </span>
								    <span class="option" style="fontWeight:bold"> 補足参照仕様書:
								        <span>{{taglana_record.supple_spec}}</span> 
								    </span>
								    <span class="option" style="fontWeight:bold"> 未検証:
								        <span>{{taglana_record.uncheck}}</span> 
								    </span> 
								    <span class="option" style="fontWeight:bold"> 備考:
								        <span>{{taglana_record.remark}}</span>
								    </span> 
								    <span class="option" style="fontWeight:bold"> 更新日:
								        <span>{{taglana_record.new_date}}</span>
								    </span> 
								    <span class="option" style="fontWeight:bold"> astaファイル名 :
								        <span>{{taglana_record.asta_filename}}</span>
								    </span>
								    <span class="option" style="fontWeight:bold"> 除外 :
								        <span>{{taglana_record.exception}}</span>
								    </span>
								</p>
                            </div>
		    	     		<div class='table_content' style="width:122px;border:0 none">
		    	     			<p class="table_title">
		    	     				<span></span>
		    	     			</p>
		    	     			<p class="table_msg table_msg_hover" title="">
		    	     				<el-button type="text" class="table_move" @click="show_more(4,taglana_index)"><i class="el-icon-d-arrow-right"></i></el-button>
		    	     			</p>
		    	     		</div>
		    	     	</div>
	    	     	</div>
		   	   	</div>
			</div>
	</div>
</template>
<script>

import Dialog_TAGLAna_Reason from './Dialog_TAGLAna_Reason'
import Dialog_TAGLAna_SeqDiagram from './Dialog_TAGLAna_SeqDiagram'
import Dialog_TAGLAna_Reqpost from './Dialog_TAGLAna_Reqpost'
import Diag_TAGLAna_Other from './Dialog_TAGLAna_Other'
import Dialog_TAGLAna_Worker from './Dialog_TAGLAna_Worker'
import Dialog_TAGLAna_RelBasicReq from './Dialog_TAGLAna_RelBasicReq.vue'
import Dialog_TAGLAna_BasicReq from './Dialog_TAGLAna_BasicReq.vue'
import Dialog_TAGLAna_Point from './Dialog_TAGLAna_Point'
require('../../assets/js/jquery-1.8.3.min.js')
export default{
	props: ['input_show','input_change_params_id' ], 
	components:{
		dialog_taglana_reason : Dialog_TAGLAna_Reason,
        dialog_taglana_seqdiagram : Dialog_TAGLAna_SeqDiagram,
        dialog_taglana_reqpost : Dialog_TAGLAna_Reqpost,
        dialog_taglana_other : Diag_TAGLAna_Other,
        dialog_taglana_worker : Dialog_TAGLAna_Worker,
        dialog_taglana_relbasicreq : Dialog_TAGLAna_RelBasicReq,
        dialog_taglana_basicreq : Dialog_TAGLAna_BasicReq,
        dialog_taglana_point : Dialog_TAGLAna_Point
	},
	data(){
		return{
			hu_list_num: 0,
			definition_list_num: 0,
			analysis_list_num: 0,
			save_array: [],
			open_array: [],
			tabledata1_copy:[],
			boolean_save_title: true,
			
			dialog_open_data: '',
			dialog_save_data: '',
			
            show : false,
            change_params_id:'',
            select_item_name : '',    // select
//          hu_index : 0,        // select index
            tagl_index : 0,      // select index
            tabledata1:[],
            tagl_record : {},
          	arl_system_conf:"",
          	BTN_type:window.sessionStorage.getItem('Type'),
            
            dialog_taglana_reason : "dialog_taglana_reason",
            tagl_ana_reason_show : false,
            
            dialog_taglana_seqdiagram : "dialog_taglana_seqdiagram",
            tagl_ana_seqdiagram_show : false,

			dialog_taglana_reqpost : "dialog_taglana_reqpost",
            tagl_ana_reqpost_show : false,
            
            dialog_taglana_other : "dialog_taglana_other",
            tagl_ana_other_show : false,
            
            dialog_taglana_worker : "dialog_taglana_worker",
            tagl_ana_worker_show : false,
            
            dialog_taglana_relbasicreq : "dialog_taglana_relrequirement",               
            tagl_ana_relrequirement_show : false,

            dialog_taglana_basicreq : "dialog_taglana_basicreq",               
            tagl_ana_basicreq_show : false,

            dialog_taglana_point : "dialog_taglana_point",
            tagl_ana_point_show : false,
 			
 			num:0,
 			names:[],
 			user_group_value:[],
// 			HU_stuate_flog:false,
// 			TAGLDef_stuate_flog:false,
 			TAGLAna_stuate_flog:false,
 			options:[
 			{
				value:1,
				label:'初始狀態，待作業',
				disabled:true,
			},
			{
				value:2,
				label:'作業完了，待翻譯',
				disabled:true,
			},
 			{
 				value:3,
 				label:'翻譯完了',
 				disabled:true,
 			},
 			],
 			fullscreenLoading:false,
 			Roles:"Member", 
 			leadGp:[],
 			p_list:[],
 			old_group:'',
		}
	},
	mounted(){
		this.getLeadGroup()
	},
	computed:{

	},
	methods:{
		lock_Ana(lock_flag,taglana_index){
			if(this.Roles == 'PL' || this.Roles == 'Admin'){
				if(lock_flag ==1){
					this.tabledata1[taglana_index].lock_status = 0
//					if(this.tabledata1[hu_index].definition_list[definition_index].lock_status == 2){
//						this.tabledata1[hu_index].definition_list[definition_index].lock_status = 0
//					}
					
				}else{
					this.tabledata1[taglana_index].lock_status = 1
//					if(this.tabledata1[hu_index].definition_list[definition_index].lock_status == 0){
//						this.tabledata1[hu_index].definition_list[definition_index].lock_status = 2
//					}
				}
			}else{
				this.$notify({
					type:'error',
					message:'您的权限不足，无法更改',
				})	
			}
		},
		statusOption(){
			if(this.tabledata1.length!=0){

				for(var k=0;k<this.tabledata1.length;k++){

					this.tabledata1[k].ana_option=this.options;
					
					if(this.tabledata1[k].control_list.length!=0){

						for(var l=0;l<this.tabledata1[k].control_list.length;l++){

							var third = this.tabledata1[k].control_list[l]

							if(this.tabledata1[k].job_status==third){

								for(var m=0;m<this.tabledata1[k].control_list.length;m++){
									this.tabledata1[k].ana_option[this.tabledata1[k].control_list[m]-1].disabled=false;
								}
							}
						}
						
					}else{
						this.TAGLAna_stuate_flog=true
					}
				}
			}
		},
		onshow () {
            this.change_params_id =  this.input_change_params_id;  
            this.BTN_type = window.sessionStorage.getItem('Type')
            this.$axios.get(this.Ip+'/BasicTreeInfo/'+this.BTN_type+'/'+this.change_params_id+'/'+window.sessionStorage.getItem('admin')+'/'+1)
				.then(res => {
					this.Roles = window.sessionStorage.getItem('Roles')
					this.tabledata1 = [];
					
					this.tabledata1 = JSON.parse(JSON.stringify(res.data.content));
					this.tabledata1[0]['modify_user_id']=window.sessionStorage.getItem('admin');
					this.user_group_value = []
					this.user_group_value[0]  = this.tabledata1[0].group_id
					this.user_group_value[1]  = this.tabledata1[0].user_id
					this.old_group = res.data.content[0]['group_id']
					this.arl_system_conf = this.tabledata1[0].sys_conf_id
					this.show = true;
					this.statusOption();
					
					
					this.tabledata1_copy = JSON.parse(JSON.stringify(this.tabledata1))
					this.hu_list_num = this.tabledata1.length;
					let tagl_array = [];
					let taglana_array = []
					
					for(let k=0;k<this.tabledata1.length;k++){
						
						taglana_array.push('1')
					}
						
					tagl_array.push(taglana_array)
					this.open_array.push(tagl_array)	
					this.open_array.push(tagl_array)
					
					this.dialog_open_data = JSON.stringify(this.tabledata1[0])
					this.dialog_save_data = JSON.stringify(this.tabledata1[0])	
					
				})
				.catch(res=>{
					this.tabledata1=[];
					this.changdu = 0;
				});
			
		},
		getLeadGroup(){
			this.$axios.get(this.Ip+'/UserContent/'+window.sessionStorage.getItem('admin'))
				.then(res => {
					this.p_list=res.data.content;
					if(this.p_list.permission_list.length!=0){
						for(var i=0;i<this.p_list.permission_list.length;i++){
							if(this.p_list.permission_list[i].roles.length!=0){
								for(var j=0;j<this.p_list.permission_list[i].roles[j];j++){
									switch(this.p_list.permission_list[i].roles[j]){
										case 4:
											this.leadGp.push(this.p_list.permission_list[i].group_id)
										break;
										default:
										break;
									}
								}
							}
						}
					}
					
				})
		},
		checkRull(){
			this.Roles = window.sessionStorage.getItem('Roles')
			if(this.Roles=="Admin"||this.Roles=="PL"){
				this.save();
			}else if(this.Roles=="Leader"){
				var a = false;
				if(this.leadGp.length!=0){
					for(var i=0;i<this.leadGp.length;i++){
						if(this.old_group == this.leadGp[i]){
							a = true;
						}
					}
				}
				if(a==true){
					this.save();
				}else if(window.sessionStorage.getItem('admin')==this.tabledata1[0]['user_id']){
					this.save();
				}else{
					this.$notify({
						type:'error',
						message:'您的权限不足，无法保存',
						showClose:true,
						duration:'0',
					})
				}
			}else if(this.Roles=="Member"){
				if(window.sessionStorage.getItem('admin')==this.tabledata1[0]['user_id']){
					this.save();
				}else{
					this.$notify({
						type:'error',
						message:'您的权限不足，无法保存',
						showClose:true,
						duration:'0',
					})
				}
					
			}else if(this.Roles=="Translator"){
				this.save();
			}else{
				this.$notify({
					type:'error',
					message:'您的权限不足，无法保存',
					showClose:true,
					duration:'0',
				})
			}
		},
		get_save_array(){
			this.save_array = []
			let tagl_array = []
			let taglana_array = []
			for(let k=0;k<this.tabledata1.length;k++){
				taglana_array.push('1')
			}
			tagl_array.push(taglana_array)	
			this.save_array.push(tagl_array)
		},
		save(){
			this.boolean_save_title = true
			this.get_save_array()
			
			
			for(let j=0;j<this.open_array.length;j++){
				if(this.open_array.length == 1){
					if(this.save_array.length ==1){
						if(this.tabledata1[0].reason == this.tabledata1_copy[0].reason){
							let taglana_delete_data = JSON.parse(JSON.stringify(this.tabledata1[0]))
							let taglana_delete_data_copy = JSON.parse(JSON.stringify(this.tabledata1[0]))
							delete taglana_delete_data.lock_status
							delete taglana_delete_data.job_status
							
							delete taglana_delete_data_copy.lock_status
							delete taglana_delete_data_copy.job_status

							if(JSON.stringify(taglana_delete_data)!=JSON.stringify(taglana_delete_data_copy)){
								this.boolean_save_title  = this.boolean_save_title && false
							}
						}
					}
					
				}
			}
			if(this.boolean_save_title){
				this.fullscreenLoading = true;
				
				this.$axios.get(this.Ip + '/ServiceStatus')
					.then(res => {
						if(res.data.result == 'NG'){
							this.$notify({
								type:'error',
								message:'其他人正在release，请耐心等待!',
								showClose:true,
								duration:'0',
							})
							return;
						}else{
							this.$axios.post(this.Ip+'/PostBasicContent',this.tabledata1)
								.then(res=>{
									if(res.data.result=="OK"){
										this.$axios.get(this.Ip+'/BasicTreeInfo/'+this.BTN_type+'/'+this.change_params_id+'/'+window.sessionStorage.getItem('admin')+'/'+1)
										.then(res => {			
											this.tabledata1 = JSON.parse(JSON.stringify(res.data.content));
											this.open_array = []
											this.tabledata1[0]['modify_user_id']=window.sessionStorage.getItem('admin');
											let tagl_array = [];
											let taglana_array = []
											for(let k=0;k<this.tabledata1.length;k++){
												taglana_array.push('1')
											}
											tagl_array.push(taglana_array)
											this.open_array.push(tagl_array)
											this.user_group_value[0]  = this.tabledata1[0].group_id
											this.user_group_value[1]  = this.tabledata1[0].user_id
											this.statusOption();
											
											this.tabledata1_copy = JSON.parse(JSON.stringify(this.tabledata1))
											
											this.dialog_open_data = JSON.stringify(this.tabledata1[0])
											this.dialog_save_data = JSON.stringify(this.tabledata1[0])
											this.arl_system_conf = this.tabledata1[0].sys_conf_id
											
											this.fullscreenLoading = false; 

											this.$notify({
												type:'success',
												message:'保存成功'
											})
											this.$emit('dialog_vue_close');
										})
										.catch(res=>{
											this.fullscreenLoading = false;

											this.$notify({							
												type:'error',
												message:'网络异常，请重新刷新',
												showClose:true,
												duration:'0',
											})
										});
									}else{
										this.fullscreenLoading = false;
							            this.$notify({
											type:'error',
											message:res.data.error,
											showClose:true,
											duration:'0',
										})
									}
								}).catch(res=>{
									this.fullscreenLoading = false;

						            this.$notify({
										type:'error',
										message:'保存失败!',
										showClose:true,
										duration:'0',
									})
								})
						}
					})
			}else{ 	

	        	this.$notify({
					type:'error',
					message:'变更理由未修改!',
					showClose:true,
					duration:'0',
				})
	        	
			}
		},
		show_more(table_id,index) {
			var _this = this;
			if(table_id==4){
				if($(".taglana_table").eq(0).children(".table_content_hidden").css("display")=="none"){
					$(".taglana_table").eq(0).children(".table_content_hidden").css({"display":"block"})
					$(".taglana_table").eq(0).animate({width:2016},1000, function() {});
					$(".taglana_table").eq(0).find(".el-icon-d-arrow-right").eq(0).removeClass().addClass("el-icon-d-arrow-left");
				}else{
					$(".taglana_table").eq(0).animate({width:1206.3},400, function() {
						$(".taglana_table").eq(0).children(".table_content_hidden").css({"display":"none"})
					});
					$(".taglana_table").eq(0).find(".el-icon-d-arrow-left").eq(0).removeClass().addClass("el-icon-d-arrow-right");	
				}
			}	   
		},
        taglana_select_item(ret_tagl_index, select_item){
            this.tagl_index = ret_tagl_index;
            this.tagl_record = this.tabledata1[0];
            this.select_item_name = select_item;
           
            if(this.tabledata1[0].lock_status == 1){
            	return
            }
            switch (this.select_item_name) {
            	case this.dialog_taglana_reason :
	                this.tagl_ana_reason_show = true;
	                break; 
	            case this.dialog_taglana_seqdiagram :
	                this.tagl_ana_seqdiagram_show = true;
	                break; 	                
	            case this.dialog_taglana_reqpost :
	            	if(this.tabledata1[0].definition_id.substring(0,1) != 'B' &&'C' && 'D'){
						return
					}
	                this.tagl_ana_reqpost_show = true;
	                break;
	            case this.dialog_taglana_other :
	                this.tagl_ana_other_show = true;
	                break;     
	            case this.dialog_taglana_worker :
	                this.tagl_ana_worker_show = true;
	                break;
	            case this.dialog_taglana_relbasicreq :
	                this.tagl_ana_relrequirement_show = true;
	                break;
	            case this.dialog_taglana_basicreq :
	                this.tagl_ana_basicreq_show = true;
	                break;
	            case this.dialog_taglana_point :
	            	if( this.tagl_record.point_list.length == 0){
    					return
    				}
	                this.tagl_ana_point_show = true;
	                break;
	           	default :
	                break;
            };
           
		},
        taglana_dialog_return (params) {
        	if (params[0]) {
        		var ret_taglana_record = params[1];
        		this.tabledata1[0] = ret_taglana_record;
        	}
        	switch (this.select_item_name) {  
        	    case this.dialog_taglana_reason :
	                this.tagl_ana_reason_show = false;    
	                break;  
	            case this.dialog_taglana_seqdiagram :
	                this.tagl_ana_seqdiagram_show = false;    
	                break; 
	            case this.dialog_taglana_reqpost :
	                this.tagl_ana_reqpost_show = false;
	                break;
	            case this.dialog_taglana_other :
	                this.tagl_ana_other_show = false;   
	                break; 
	            case this.dialog_taglana_worker :
	                this.tagl_ana_worker_show = false;    
	                break;
	            case this.dialog_taglana_relbasicreq :
	                this.tagl_ana_relrequirement_show = false;
	                break;
	            case this.dialog_taglana_basicreq :
	                this.tagl_ana_basicreq_show = false;
	                break;
	            case this.dialog_taglana_point :
	                this.tagl_ana_point_show = false;    
	                break;    
	            default :
	                break;
            };
        },   
//      taglana_delete(taglana_index){
//      	if(this.Roles=="Admin"||this.Roles=="PL"||this.Roles=="Leader"){
//				if(this.tabledata1taglana_index[0].lock_status == 1){
//	            	return
//	            }
//	        	this.$confirm('此操作将永久删除数据，是否继续?','提示',{
//	        		confirmButtonText:"确定",
//	        		cancelButtonText:"取消",
//	        		type:'warning'
//	        	}).then(()=>{
//					this.tabledata1taglana_index.splice(0,1)
//					this.get_save_array()
//	        	}).catch(() => {
//				    	
//				    })
//			}else{
//				this.$notify({
//					type:'error',
//					message:'您的权限不足，无法删除',
//					showClose:true,
//					duration:'0',
//				})
//			}
//      },
		dialog_close() {
			this.dialog_save_data = JSON.stringify(this.tabledata1[0])
			var this_ = this;

			if(this.dialog_save_data == this.dialog_open_data){
				$(".dialog_html").animate({height:0},500,function(){
					this_ .show = false;
					$(".taglana_table").css({display:"none"})
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
						$(".taglana_table").css({display:"none"})
					});
					this.$emit('dialog_close', [false]);	
			  }).catch(() => {
			    	
			    })
			}
		},
		accordion(table_id,taglana_index){
			if(table_id==4){
				$(".taglana_div").eq(0).children(".taglana_table").eq(0).toggle(function(){})
			}
		}, 
		user_group(){
			this.tabledata1.group_id = this.user_group_value[0]
			this.tabledata1.user_id = this.user_group_value[1]
		}
	},
	watch:{
	    input_show(v) {
            if (this.input_show) {
                this.onshow();
                this.Roles = window.sessionStorage.getItem('Roles')
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
	display: none;
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
/*.table_msg_hover{
	transition:0.5s;
}*/
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
	display:none;
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
	display:none;
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
