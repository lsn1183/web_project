<template>
	<div class="dialog"  id="dialog" v-show="show" v-loading.fullscreen.lock="fullscreenLoading" element-loading-text="正在保存中,请稍等... ...">		    
			<!--TAGL要件定义的弹窗-->
			<dialog_tagldef_reason  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_reason_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_reason>

		    
			<dialog_tagldef_others  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_others_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_others>

		    <dialog_tagldef_remark  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_remark_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_remark>
		    
		    <dialog_tagldef_refdoc  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_reference_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_refdoc>

			<dialog_tagldef_hureqpost  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_hureqpost_show'  v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_hureqpost>
		    
		    <dialog_tagldef_notice  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_notice_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_notice>

			<dialog_tagldef_worker  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_worker_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_worker>
		    
		    <dialog_tagldef_relbasicreq  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_relbasicreq_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_relbasicreq>

		    <dialog_tagldef_basicreq  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_basicreq_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_basicreq>

		    <dialog_tagldef_point @dialog_close = 'tagl_dialog_return' v-bind:dialog_show='tagl_def_point_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_point>
		    
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
	    	   		<!-- TAGL表格 -->
		    	    <div style="marginLeft:15px;" v-for="(definition_record, definition_index) in tabledata1" class="tagl_div">
		    	    	<div class="title_arl" >
		    	     		<span class="fl"  @click="accordion(3,definition_index)"><i class="el-icon-arrow-right"></i>{{definition_record.title}}</span>
		    	     			<img src="../../assets/img/lock_2.png" alt="闭锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;marginLeft: 15px;" v-if="definition_record.lock_status == 1?true:false" @click="lock_Def(definition_record.lock_status,definition_index)"/>
			 					<img src="../../assets/img/unlock_2.png" alt="开锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;marginLeft: 15px;"v-if="definition_record.lock_status == 0?true:false" @click="lock_Def(definition_record.lock_status,definition_index)"/>
			 					<img src="../../assets/img/unlock_22.png" alt="半锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;marginLeft: 15px;"v-if="definition_record.lock_status == 2?true:false" @click="lock_Def(definition_record.lock_status,definition_index)"/>
		    	     		<span class="float"  style="marginLeft:26px">
		    	     			任務状態
		    	     			<template>
		    	     				<el-select v-model="definition_record.job_status" placeholder="请选择" :disabled="TAGLDef_stuate_flog||definition_record.lock_status?true:false" style="width:135px;">
		    	     					<el-option v-for="item in definition_record.def_option" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled"></el-option>
		    	     				</el-select>
		    	     			</template>
		    	     		</span>
		    	     		<!--<div style="float: right;height:40px;">
								<span class="fr" style="color:#42b983" @click="definition_delete(definition_index)"><i class="el-icon-delete" v-if="definition_record.lock_status == 0?true:false" disabled> 删除</i></span>
								<span class="fr" style="color:#bfcbd9" @click="definition_delete(definition_index)"><i class="el-icon-delete" v-if="definition_record.lock_status == 1||definition_record.lock_status == 2?true:false" disabled> 删除</i></span>
							</div>-->
		    	     	</div>
		    	    	<div class="tagltable"  :class="definition_record.lock_status == 1?'lock_show':''">
    	    		 		
		    	    		<div class='table_content' style="width:100px">
		    	    			<p class="table_title">
		    	    				<span>ユニークID</span>
		    	    			</p>
		    	    			<p class="table_msg" title="" style="textAlign:center" :class="definition_record.lock_status == 1?'lock_show':''">
		    	    			     {{definition_record.unique_id}}
		    	    			</p>
		    	    		</div>
		    	    		<div class='table_content' style="width:200px">
		    	     			<p class="table_title">
		    	     				<span>H/U要件定義書から転記</span>
		    	     			</p>
		    	     			<!--只有ID为B、C、D开头的tagl_def才可编辑HU转记-->
		    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="tagl_select_item(definition_index, dialog_tagldef_hureqpost)" :class="definition_record.lock_status == 1||(definition_record.definition_id.substring(0,1) != 'B' &&'C' && 'D')?'lock_show':''">
									<span class="option" style="fontWeight:bold">H/U要件定義ID:	
										<span style="fontWeight:normal">{{definition_record.hu_def_id}}</span>
									</span>
									<span class="option" style="fontWeight:bold">大分類:	
										<span style="fontWeight:normal">{{definition_record.major_category}}</span>
									</span>
									<span class="option" style="fontWeight:bold">中分類:	
										<span style="fontWeight:normal">{{definition_record.medium_category}}</span>
									</span>
									<span class="option" style="fontWeight:bold">小分類:	
										<span style="fontWeight:normal">{{definition_record.small_category}}</span>
									</span>
									<span class="option" style="fontWeight:bold">詳細:	
										<span style="fontWeight:normal">{{definition_record.detail}}</span>
									</span>
									<span class="option" style="fontWeight:bold">基本要件:	
										<span style="fontWeight:normal">{{definition_record.basic_req}}</span>
									</span>
									<span class="option" style="fontWeight:bold">関連基本要件:	
										<span style="fontWeight:normal">{{definition_record.rel_requirement}}</span>
									</span>
								</p>
		    	     		</div> 
    	    		 		<div class='table_content' style="width:547px">
		    	     			<p class="table_title">
		    	     				<span>責務分担</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" title="" @dblclick="tagl_select_item(definition_index, dialog_tagldef_worker)" :class="definition_record.lock_status == 1 || definition_record.lock_status == 2?'lock_show':''">
		    	     				<span v-for="(sequence_record, sequence_index) in definition_record.sequence_list">
		    	     					<span class="option" style="fontWeight:bold">({{sequence_index+1}})</br>設備:
			    	     					<span style="fontWeight:normal" v-if="sequence_record.info!=''">({{sequence_record.info}})</span>
			    	     					<span style="fontWeight:normal" v-if="sequence_record.name!=''">{{sequence_record.name}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">状態:
			    	     					<span style="fontWeight:normal">{{sequence_record.status}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">トリガー:
			    	     					<span style="fontWeight:normal">{{sequence_record.trigger}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">動作:
			    	     					<span style="fontWeight:normal">{{sequence_record.action}}</span>
			    	     				</span>
		    	     				</span>
		    	     			</p>
		    	     		</div> 
    	    		 		<div class='table_content' style="width:250px">
		    	     			<p class="table_title">
		    	     				<span>变更理由与日期</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" :title="definition_record.reason"  @dblclick="tagl_select_item(definition_index, dialog_tagldef_reason)" :class="definition_record.lock_status == 1?'lock_show':''">
		    	     			    <span class="option" style="fontWeight:bold">变更理由:	
										<span style="fontWeight:normal">{{definition_record.reason}}</span>
									</span>
									<span class="option" style="fontWeight:bold">日付:	
										<span style="fontWeight:normal">{{definition_record.new_date}}</span>
									</span>
								</p>
		    	     		</div> 		    	     		
		    	     		<div class='table_content_hidden' style="width:200px">
		    	     			<p class="table_title">
		    	     				<span>指摘</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" title="" v-if="definition_record.point_list.length != 0?true:false" :class="definition_record.lock_status == 1 || definition_record.point_list.length == 0?'lock_show':''" @dblclick="tagl_select_item( definition_index, dialog_tagldef_point)" >
		    	     				<span v-for="(point_record, point_index) in definition_record.point_list">
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
		    	     			<p class="table_msg content_scroll table_msg_hover" title="" v-if="definition_record.point_list.length == 0?true:false" :class="definition_record.lock_status == 1 || definition_record.point_list.length == 0?'lock_show':''">
		    	     				
		    	     			</p>
		    	     		</div> 
		    	     		<div class='table_content_hidden' style="width:250px">
		    	     			<p class="table_title">
		    	     				<span>関連基本要件</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" :title="definition_record.rel_requirement"  @dblclick="tagl_select_item(definition_index, dialog_tagldef_relbasicreq)" :class="definition_record.lock_status == 1?'lock_show':''">
		    	     			    <span>{{definition_record.rel_requirement}}</span> 
		    	     			</p>
		    	     		</div> 
		    	     		
		    	     		<div class='table_content_hidden' >
		    	     			<p class="table_title">
		    	     				<span>基本要件</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll table_msg_hover" :title="definition_record.basic_req"  @dblclick="tagl_select_item(definition_index, dialog_tagldef_basicreq)" :class="definition_record.lock_status == 1?'lock_show':''">
		    	     			
		    	     			    <span>{{definition_record.basic_req}}</span> 
		    	     			</p>
		    	     		</div> 
		    	     		<div class='table_content_hidden'>
								<p class="table_title">
									<span>備考</span>
								</p>
								<p class="table_msg table_msg_hover" @dblclick="tagl_select_item(definition_index, dialog_tagldef_remark)" :class="definition_record.lock_status == 1?'lock_show':''">      
									<span>{{definition_record.remark}}</span>
								</p>
						    </div>
		    	     		<div class='table_content_hidden'>
								<p class="table_title">
									<span>責務分担の特記事項</span>
								</p>
								<p class="table_msg table_msg_hover ontent_scroll" @dblclick="tagl_select_item(definition_index,dialog_tagldef_notice)" :class="definition_record.lock_status == 1?'lock_show':''">
									<span>{{definition_record.notice}}</span>
								</p>
						    </div>
                            <div class='table_content_hidden'>
							    <p class="table_title">
									<span>参考文献</span>
								</p>
								<p class="table_msg table_msg_hover  content_scroll" @dblclick="tagl_select_item(definition_index, dialog_tagldef_refdoc)" :class="definition_record.lock_status == 1?'lock_show':''">
								    <span class="option" style="fontWeight:bold"> 参考HAL設計書:
								        <span>{{definition_record.rel_hal_design}}</span> 
								    </span>
								    <span class="option" style="fontWeight:bold"> 参考ウォークスルー図:
								        <span>{{definition_record.rel_flow_diagram}}</span> 
								    </span> 
								    <span class="option" style="fontWeight:bold"> その他仕様（リファハード仕様等）:
								        <span>{{definition_record.other_spec}}</span>
								    </span> 
								</p>
                            </div>
                            <div class='table_content_hidden' >
							    <p class="table_title">
									<span>其他</span>
								</p>
								<p class="table_msg table_msg_hover content_scroll" @dblclick="tagl_select_item(definition_index, dialog_tagldef_others)" :class="definition_record.lock_status == 1?'lock_show':''">
								    <span class="option" style="fontWeight:bold"> 担当:
								        <span>{{definition_record.author_name}}</span> 
								    </span>
								    <span class="option" style="fontWeight:bold"> リファレンスハード上での実現可否:
								        <span>{{definition_record.implementation}}</span> 
								    </span>
								    <span class="option" style="fontWeight:bold"> 詳細分析可否:
								        <span>{{definition_record.analysis}}</span> 
								    </span> 
								    <span class="option" style="fontWeight:bold"> 未要件分析:
								        <span>{{definition_record.unrequire}}</span>
								    </span> 
								    <span class="option" style="fontWeight:bold"> 更新日:
								        <span>{{definition_record.new_date}}</span>
								    </span> 
								    <span class="option" style="fontWeight:bold"> 除外:
								        <span>{{definition_record.exception}}</span> 
								    </span>
								</p>
                            </div>
		    	     		<div class='table_content' style="width:122px;border:0 none">
		    	     			<p class="table_title">
		    	     				<span></span>
		    	     			</p>
		    	     			<p class="table_msg table_msg_hover" title="">
		    	     				<el-button type="text" class="table_move" @click="show_more(3,definition_index)"><i class="el-icon-d-arrow-right"></i></el-button>
		    	     			</p>
		    	     		</div>
		    	     	</div>
		    	     	<!-- TAGLANA表格 -->
		    	     	<div style="marginLeft:15px;" v-for="(taglana_record,taglana_index) in definition_record.analysis_list" class="taglana_div">
     		    	    	<div class="title_arl" >
     		    	     		<span class="fl"  @click="accordion(4,definition_index,taglana_index)"><i class="el-icon-arrow-right"></i>{{taglana_record.title}}</span>
     		    	     		<img src="../../assets/img/lock_2.png" alt="闭锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;" v-show="taglana_record.lock_status == 1?true:false" @click="lock_Ana(taglana_record.lock_status,definition_index,taglana_index)"/>
			 					<img src="../../assets/img/unlock_2.png" alt="开锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;"v-show="taglana_record.lock_status == 0?true:false" @click="lock_Ana(taglana_record.lock_status,definition_index,taglana_index)"/>
     		    	     		<span class="fl" style="marginLeft: 26px;">
     		    	     			任務状態
     		    	     			<template>
     		    	     				<el-select v-model="taglana_record.job_status" placeholder="请选择" :disabled="TAGLAna_stuate_flog||taglana_record.lock_status?true:false" style="width:135px;">
     		    	     					<el-option v-for="item in taglana_record.ana_option" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled"></el-option>
     		    	     				</el-select>
     		    	     			</template>
     		    	     		</span>
     		    	     		<!--<div style="float: right;">
     								<span class="fr" style="color:#42b983" @click="taglana_delete(definition_index)" v-if="taglana_record.lock_status == 0?true:false"><i class="el-icon-delete" disabled> 删除</i></span>
     								<span class="fr" style="color:#bfcbd9" @click="taglana_delete(definition_index)" v-if="taglana_record.lock_status == 1?true:false"><i class="el-icon-delete" disabled> 删除</i></span>
     		    	     		</div>-->
     		    	     	</div>
			    	    	<div class="taglana_table"  :class="taglana_record.lock_status == 1?'lock_show':''">
			    	    		<div class='table_content' style="width:200px">
			    	    			<p class="table_title">
			    	    				<span>シーケンス図</span>
			    	    			</p>
			    	    			<p class="table_msg table_msg_hover content_scroll" title="" style="textAlign:center" @dblclick="taglana_select_item(definition_index,dialog_taglana_seqdiagram)" :class="taglana_record.lock_status == 1?'lock_show':''">
			    	    			    {{taglana_record.seq_diagram}}  
			    	    			</p>
			    	    		</div>
			    	    		<div class='table_content' style="width:432px">
			    	     			<p class="table_title">
			    	     				<span>TAGL-PF</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="taglana_select_item(definition_index, dialog_taglana_worker)" :class="taglana_record.lock_status == 1?'lock_show':''">
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
			    	     			<p class="table_msg content_scroll table_msg_hover" :title="taglana_record.reason" @dblclick="taglana_select_item(definition_index, dialog_taglana_reason)" :class="taglana_record.lock_status == 1?'lock_show':''">
			    	     				<span class="option" style="fontWeight:bold">变更理由:	
											<span style="fontWeight:normal">{{taglana_record.reason}}</span>
										</span>
										<span class="option" style="fontWeight:bold">日付:	
											<span style="fontWeight:normal">{{taglana_record.new_date}}</span>
										</span>
									</p>
			    	     		</div>
			    	     		<div class='table_content' style="width:200px">
			    	     			<p class="table_title">
			    	     				<span>指摘</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover" :class="taglana_record.lock_status == 1 || taglana_record.point_list.length == 0 ?'lock_show':''" @dblclick="taglana_select_item( definition_index, dialog_taglana_point)" v-if="taglana_record.point_list.length !=0?true:false">
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
			    	     			<p class="table_msg content_scroll table_msg_hover" :title="taglana_record.rel_requirement" @dblclick="taglana_select_item(definition_index, dialog_taglana_relbasicreq)" :class="taglana_record.lock_status == 1?'lock_show':''">
			    	     			
			    	     			    <span>{{taglana_record.rel_requirement}}</span> 
			    	     			</p>
			    	     		</div>
			    	     		<div class='table_content_hidden' >
			    	     			<p class="table_title">
			    	     				<span>基本要件</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover" :title="taglana_record.basic_req" @dblclick="taglana_select_item(definition_index, dialog_taglana_basicreq)"  :class="taglana_record.lock_status == 1?'lock_show':''">
			    	     			
			    	     			    <span>{{taglana_record.basic_req}}</span> 
			    	     			</p>
			    	     		</div> 

                                <div class='table_content_hidden' >
								    <p class="table_title">
										<span>其他</span>
									</p>
									<p class="table_msg table_msg_hover content_scroll" @dblclick="taglana_select_item(definition_index, dialog_taglana_other)" :class="taglana_record.lock_status == 1?'lock_show':''">
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
			    	     				<el-button type="text" class="table_move" @click="show_more(4,definition_index,taglana_index)"><i class="el-icon-d-arrow-right"></i></el-button>
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

import Dialog_TAGLDef_Reason from './Dialog_TAGLDef_Reason.vue'
import Dialog_TAGLDef_Worker from './Dialog_TAGLDef_Worker.vue'
import Dialog_TAGLDef_Hureqpost from './Dialog_TAGLDef_Hureqpost.vue'
import Dialog_TAGLDef_Remark from './Dialog_TAGLDef_Remark.vue'
import Dialog_TAGLDef_Notice from './Dialog_TAGLDef_Notice.vue'
import Dialog_TAGLDef_RefDoc from './Dialog_TAGLDef_RefDoc.vue'
import Dialog_TAGLDef_Others from './Dialog_TAGLDef_Others.vue'
import Dialog_TAGLDef_RelBasicReq from './Dialog_TAGLDef_RelBasicReq.vue'
import Dialog_TAGLDef_BasicReq from './Dialog_TAGLDef_BasicReq.vue'
import Dialog_TAGLDef_Point from './Dialog_TAGLDef_Point.vue'

import Dialog_TAGLAna_Reason from './Dialog_TAGLAna_Reason'
import Dialog_TAGLAna_SeqDiagram from './Dialog_TAGLAna_SeqDiagram'
import Diag_TAGLAna_Other from './Dialog_TAGLAna_Other'
import Dialog_TAGLAna_Worker from './Dialog_TAGLAna_Worker'
import Dialog_TAGLAna_RelBasicReq from './Dialog_TAGLAna_RelBasicReq.vue'
import Dialog_TAGLAna_BasicReq from './Dialog_TAGLAna_BasicReq.vue'
import Dialog_TAGLAna_Point from './Dialog_TAGLAna_Point'
require('../../assets/js/jquery-1.8.3.min.js')
export default{
	props: ['input_show','input_change_params_id' ], 
	components:{
		dialog_tagldef_reason : Dialog_TAGLDef_Reason,
		dialog_tagldef_worker : Dialog_TAGLDef_Worker,
		dialog_tagldef_hureqpost : Dialog_TAGLDef_Hureqpost,
		dialog_tagldef_remark : Dialog_TAGLDef_Remark,
		dialog_tagldef_notice : Dialog_TAGLDef_Notice,
		dialog_tagldef_refdoc : Dialog_TAGLDef_RefDoc,
		dialog_tagldef_others : Dialog_TAGLDef_Others,
		dialog_tagldef_relbasicreq : Dialog_TAGLDef_RelBasicReq,	
		dialog_tagldef_basicreq : Dialog_TAGLDef_BasicReq,
		dialog_tagldef_point : Dialog_TAGLDef_Point,
		dialog_taglana_reason : Dialog_TAGLAna_Reason,
        dialog_taglana_seqdiagram : Dialog_TAGLAna_SeqDiagram,
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
            
            dialog_tagldef_reason : "dialog_tagldef_reason",
            tagl_def_reason_show : false,
            
            dialog_tagldef_others : "tagl_def_others",
            tagl_def_others_show : false,

            dialog_tagldef_remark : "tagl_def_remark",
            tagl_def_remark_show : false,
            
            dialog_tagldef_refdoc : "tagl_def_reference",
            tagl_def_reference_show : false,

            dialog_tagldef_notice : "tagl_notice_reference",
            tagl_def_notice_show : false,
            
            dialog_tagldef_worker : "dialog_tagldef_worker",
            tagl_def_worker_show : false,
            
            dialog_tagldef_hureqpost : "tagl_def_hureqpost",
            tagl_def_hureqpost_show : false,
            
            dialog_tagldef_relbasicreq : "dialog_tagldef_relbasicreq",               
            tagl_def_relbasicreq_show : false, 

            dialog_tagldef_basicreq : "dialog_tagldef_basicreq",               
            tagl_def_basicreq_show : false, 

            dialog_tagldef_point : "dialog_tagldef_point",
            tagl_def_point_show : false,
            
            dialog_taglana_reason : "dialog_taglana_reason",
            tagl_ana_reason_show : false,
            
            dialog_taglana_seqdiagram : "dialog_taglana_seqdiagram",
            tagl_ana_seqdiagram_show : false,

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
		lock_Def(lock_flag,definition_index){
			if(this.Roles == 'PL' || this.Roles == 'Admin'){
				//先判断子级再判断父级
				let bansuo_tagl_flag = false
				
				for(let i=0;i<this.tabledata1[definition_index].analysis_list.length;i++){
					if(this.tabledata1[definition_index].analysis_list[i].lock_status == 1){
						bansuo_tagl_flag = bansuo_tagl_flag || true 
						break;
					}
				}
				
				if(bansuo_tagl_flag == true){
					if(lock_flag == 2){
						//子级有闭锁的情况下，自身为半锁时，点击半锁，自身变为闭锁。
						this.tabledata1[definition_index].lock_status = 1
						//子级和自身都为闭锁时，父级变半锁
						if(this.tabledata1[definition_index].lock_status == 0){
							this.tabledata1[definition_index].lock_status = 2
						}
					}else{
						//子级有闭锁的情况下，自身为闭锁时，点击闭锁，自身变为半锁。
						this.tabledata1[definition_index].lock_status = 2
						if(this.tabledata1[definition_index].lock_status == 2){
							this.tabledata1[definition_index].lock_status = 0
						}
					}
				}else{
					
					if(lock_flag == 1){
						//子级没有闭锁的情况下，父级为闭锁时，点击闭锁，变为开锁
						this.tabledata1[definition_index].lock_status = 0
					}else{
						//子级没有闭锁的情况下，父级为开锁时，点击开锁，变为闭锁
						this.tabledata1[definition_index].lock_status = 1
					}
					
					let bansuo_flag = false 
					for(let i=0;i<this.tabledata1.length;i++){
						if(this.tabledata1[i].lock_status == 1){
							bansuo_flag = bansuo_flag || true
							break
						}
						
					}
				}
			}else{
//				this.$notify({
//					type:'error',
//					message:'您的权限不足，无法更改',
//				})
				this.$notify({
					type:'error',
					message:'您的权限不足，无法更改',
				})	
			}
		},
		lock_Ana(lock_flag,definition_index,taglana_index){
			if(this.Roles == 'PL' || this.Roles == 'Admin'){
				if(lock_flag ==1){
					this.tabledata1[definition_index].analysis_list[taglana_index].lock_status = 0
					if(this.tabledata1[definition_index].lock_status == 2){
						this.tabledata1[definition_index].lock_status = 0
					}
					
				}else{
					this.tabledata1[definition_index].analysis_list[taglana_index].lock_status = 1
					if(this.tabledata1[definition_index].lock_status == 0){
						this.tabledata1[definition_index].lock_status = 2
					}
				}
			}else{
//				this.$notify({
//					type:'error',
//					message:'您的权限不足，无法更改',
//				})	
				this.$notify({
					type:'error',
					message:'您的权限不足，无法更改',
				})	
			}
		},
		statusOption(){
			if(this.tabledata1.length!=0){
				for(var j=0;j<this.tabledata1.length;j++){

					this.tabledata1[j].def_option=this.options;

					if(this.tabledata1[j].control_list.length!=0){

						for(var k=0;k<this.tabledata1[j].control_list.length;k++){

							var sec = this.tabledata1[j].control_list[k]

							if(this.tabledata1[j].job_status==sec){

								for(var l=0;l<this.tabledata1[j].control_list.length;l++){

									this.tabledata1[j].def_option[this.tabledata1[j].control_list[l]-1].disabled = false;
								}
								
							}
						}
					}else{
						this.TAGLDef_stuate_flog=true

					}
					if(this.tabledata1[j].analysis_list.length!=0){

						for(var k=0;k<this.tabledata1[j].analysis_list.length;k++){

							this.tabledata1[j].analysis_list[k].ana_option=this.options;
							
							if(this.tabledata1[j].analysis_list[k].control_list.length!=0){

								for(var l=0;l<this.tabledata1[j].analysis_list[k].control_list.length;l++){

									var third = this.tabledata1[j].analysis_list[k].control_list[l]

									if(this.tabledata1[j].analysis_list[k].job_status==third){

										for(var m=0;m<this.tabledata1[j].analysis_list[k].control_list.length;m++){
											this.tabledata1[j].analysis_list[k].ana_option[this.tabledata1[j].analysis_list[k].control_list[m]-1].disabled=false;
										}
									}
								}
								
							}else{
								this.TAGLAna_stuate_flog=true
							}
						}
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
					for(let j=0;j<this.tabledata1.length;j++){
						let taglana_array = []
						for(let k=0;k<this.tabledata1[j].analysis_list.length;k++){
							taglana_array.push('1')
						}
						tagl_array.push(taglana_array)
					}
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
//					this.$notify({
//						type:'error',
//						message:'您的权限不足，无法保存',
//						showClose:true,
//						duration:'0',
//					})
					this.$notify({
						type:'error',
						message:'您的权限不足，无法更改',
						showClose:true,
						duration:'0',
					})
				}
			}else if(this.Roles=="Member"){
				if(window.sessionStorage.getItem('admin')==this.tabledata1[0]['user_id']){
					this.save();
				}else{
//					this.$notify({
//						type:'error',
//						message:'您的权限不足，无法保存',
//						showClose:true,
//						duration:'0',
//					})
					this.$notify({
						type:'error',
						message:'您的权限不足，无法更改',
						showClose:true,
						duration:'0',
					})
				}
					
			}else if(this.Roles=="Translator"){
				this.save();
			}else{
//				this.$notify({
//					type:'error',
//					message:'您的权限不足，无法保存',
//					showClose:true,
//					duration:'0',
//				})
				this.$notify({
					type:'error',
					message:'您的权限不足，无法更改',
					showClose:true,
					duration:'0',
				})
			}
		},
		get_save_array(){
			this.save_array = []
			let tagl_array = [];
			for(let j=0;j<this.tabledata1.length;j++){
				let taglana_array = []
				for(let k=0;k<this.tabledata1[j].analysis_list.length;k++){
					taglana_array.push('1')
				}
				tagl_array.push(taglana_array)					
			}
			this.save_array.push(tagl_array)
		},
		save(){
			this.boolean_save_title = true
			this.get_save_array()
			
			for(let k=0;k<this.open_array.length;k++){
				if(this.save_array[k] != undefined){
//							//判断definition_list中的每一个
					if(this.tabledata1[k].reason == this.tabledata1_copy[k].reason){
						let tagldef_delete_data = JSON.parse(JSON.stringify(this.tabledata1[k]))
						let tagldef_delete_data_copy = JSON.parse(JSON.stringify(this.tabledata1[k]))
						delete tagldef_delete_data.lock_status
						delete tagldef_delete_data.job_status
						delete tagldef_delete_data.analysis_list
						
						delete tagldef_delete_data_copy.lock_status
						delete tagldef_delete_data_copy.job_status
						delete tagldef_delete_data_copy.analysis_list
						if(JSON.stringify(tagldef_delete_data)!=JSON.stringify(tagldef_delete_data_copy)){
							this.boolean_save_title  = this.boolean_save_title && false
						}
					}
//							//判断taglana_list的每一个
					for(let j=0;j<this.open_array[k].length;j++){
						if(this.open_array[k].length == 1){
							if(this.save_array[k].length ==1){
								if(this.tabledata1[k].analysis_list[0].reason == this.tabledata1_copy[k].analysis_list[0].reason){
									let taglana_delete_data = JSON.parse(JSON.stringify(this.tabledata1[k].analysis_list[0]))
									let taglana_delete_data_copy = JSON.parse(JSON.stringify(this.tabledata1[k].analysis_list[0]))
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
				}
			}
			if(this.boolean_save_title){
				this.fullscreenLoading = true;
				
				for(let k=0;k<this.open_array.length;k++){
					//判断save_array.hu_list.definition_list里有没有对象，如果没有，就不用对比；有的话就比较
					if(this.save_array[k] != undefined){
//								for(let j=0;j<this.open_array[k].length;j++){
							if(this.open_array[k].length == 1){
								//TAGL_Ana的reason无变化，去查看上一层数据有无变化
								if(this.save_array[k].length == 1){
									if(this.tabledata1[k].analysis_list[0].reason == this.tabledata1_copy[k].analysis_list[0].reason){
										//TAGL_Def的责任分担和reason都有变化时，修改TAGL_Ana的reason
										//TAGL_Def的reason无变化时，向上一层查看数据有无变化
										
											//只有TAGL_def的责任分担(sequence_list)中的DCU('type':'DCU')变化时,责任分担才算变化（新增和删除‘DCU’都算变化）
											let array_Open_TAGLDEFSequeceList = []
											let array_Save_TAGLDEFSequeceList = []
											if(this.tabledata1[k].sequence_list.length!=0){
												for(let m = 0;m<this.tabledata1[k].sequence_list.length;m++){
													let Squence_Open_type = this.tabledata1[k].sequence_list[m].type
													if(Squence_Open_type== 'DCU'||Squence_Open_type== 'MEU'||Squence_Open_type== 'DCU/MEU'){
														array_Open_TAGLDEFSequeceList.push(this.tabledata1[k].sequence_list[m])
													}
												}
											}
											if(this.tabledata1_copy[k].sequence_list.length!=0){
												for(let m = 0;m<this.tabledata1_copy[k].sequence_list.length;m++){
													let Squence_Save_type = this.tabledata1_copy[k].sequence_list[m].type
													if(Squence_Save_type== 'DCU'||Squence_Save_type== 'MEU'||Squence_Save_type== 'DCU/MEU'){
														array_Save_TAGLDEFSequeceList.push(this.tabledata1_copy[k].sequence_list[m])
													}
												}
											}
											if(JSON.stringify(array_Open_TAGLDEFSequeceList) != JSON.stringify(array_Save_TAGLDEFSequeceList)){
												this.tabledata1[k].analysis_list[0].reason = this.tabledata1[k].reason
											}
	
									}else{
										
									}
								}else{
									
								}
									
							}else{
								
							}
//								}
					}
				}
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
											for(let j=0;j<this.tabledata1.length;j++){
												let taglana_array = []
												for(let k=0;k<this.tabledata1[j].analysis_list.length;k++){
													taglana_array.push('1')
												}
												tagl_array.push(taglana_array)
												
											}
											this.open_array.push(tagl_array)
											this.user_group_value[0]  = this.tabledata1[0].group_id
											this.user_group_value[1]  = this.tabledata1[0].user_id
											this.statusOption();
											
											this.tabledata1_copy = JSON.parse(JSON.stringify(this.tabledata1))
											
											this.dialog_open_data = JSON.stringify(this.tabledata1[0])
											this.dialog_save_data = JSON.stringify(this.tabledata1[0])
											this.arl_system_conf = this.tabledata1[0].sys_conf_id
											
											this.fullscreenLoading = false; 
				//							this.$notify({
				//								type:'success',
				//								message:'保存成功'
				//							})
											this.$notify({
												type:'success',
												message:'保存成功'
											})
											this.$emit('dialog_vue_close');
										})
										.catch(res=>{
											this.fullscreenLoading = false;
				//							this.$notify({
				//								type:'error',
				//								message:'网络异常，请重新刷新',
				//								showClose:true,
				//								duration:'0',
				//							})
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
				//		            this.$notify({
				//						type:'error',
				//						message:'保存失败!',
				//						showClose:true,
				//						duration:'0',
				//					})
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
//	        	this.$notify({
//					type:'error',
//					message:'变更理由未修改!',
//					showClose:true,
//					duration:'0',
//				})
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
			if(table_id==3){
				if($(".tagl_div").eq(index).children(".tagltable").eq(0).children(".table_content_hidden").css("display")=="none"){
					$(".tagl_div").eq(index).children(".tagltable").eq(0).children(".table_content_hidden").css({"display":"block"})
					$(".tagl_div").eq(index).children(".tagltable").eq(0).animate({width:2571},1000, function() {
		           	$(".tagl_div").eq(index).children(".tagltable").eq(0).find(".el-icon-d-arrow-right").eq(0).removeClass().addClass("el-icon-d-arrow-left");
		   		 });
				}else{
					$(".tagl_div").eq(index).children(".tagltable").eq(0).animate({width:1221},400, function() {
		           $(".tagl_div").eq(index).children(".tagltable").eq(0).children(".table_content_hidden").css({"display":"none"})
		           $(".tagl_div").eq(index).children(".tagltable").eq(0).find(".el-icon-d-arrow-left").eq(0).removeClass().addClass("el-icon-d-arrow-right");
		   		 });
				}
			}else if(table_id==4){
				if($(".tagl_div").eq(index).children(".taglana_div").eq(0).children(".taglana_table").eq(0).children(".table_content_hidden").css("display")=="none"){
					$(".tagl_div").eq(index).children(".taglana_div").eq(0).children(".taglana_table").eq(0).children(".table_content_hidden").css({"display":"block"})
					$(".tagl_div").eq(index).children(".taglana_div").eq(0).children(".taglana_table").eq(0).animate({width:1816},800, function() {});
					$(".tagl_div").eq(index).children(".taglana_div").eq(0).children(".taglana_table").eq(0).find(".el-icon-d-arrow-right").eq(0).removeClass().addClass("el-icon-d-arrow-left");
				}else{
					$(".tagl_div").eq(index).children(".taglana_div").eq(0).children(".taglana_table").eq(0).animate({width:1206.3},200, function() {
						$(".tagl_div").eq(index).children(".taglana_div").eq(0).children(".taglana_table").eq(0).children(".table_content_hidden").css({"display":"none"})
					});
					$(".tagl_div").eq(index).children(".taglana_div").eq(0).children(".taglana_table").eq(0).find(".el-icon-d-arrow-left").eq(0).removeClass().addClass("el-icon-d-arrow-right");	
				}
			}	   
		},
        tagl_select_item( ret_tagl_index, select_item){
            this.tagl_index = ret_tagl_index;
            this.tagl_record = this.tabledata1[this.tagl_index];
            this.select_item_name = select_item;
            if(this.tabledata1[this.tagl_index].lock_status == 1){
            	return
            }
            switch (this.select_item_name) {
            	case this.dialog_tagldef_reason :
	                this.tagl_def_reason_show = true;
	                break; 
	            case this.dialog_tagldef_others :
	                this.tagl_def_others_show = true;
	                break; 
	            case this.dialog_tagldef_remark :
	                this.tagl_def_remark_show = true;
	                break;   
	            case this.dialog_tagldef_refdoc :
	                this.tagl_def_reference_show = true;
	                break;
	            case this.dialog_tagldef_hureqpost :
		            if(this.tabledata1[0].definition_id.substring(0,1) != 'B' &&'C' && 'D'){
						return
					}
	                this.tagl_def_hureqpost_show = true;
	                break;
	            case this.dialog_tagldef_relbasicreq :
	                this.tagl_def_relbasicreq_show = true;
	                break;
	            case this.dialog_tagldef_notice :
	                this.tagl_def_notice_show = true;
	                break;
		  	    case this.dialog_tagldef_worker :
		  	    	let lock_status_kids_flag = true
    				for(let i=0;i<this.tagl_record.analysis_list.length;i++){
    					if(this.tagl_record.analysis_list[i].lock_status == 1 || this.tagl_record.analysis_list[i].lock_status == 2){
    						lock_status_kids_flag = lock_status_kids_flag && false
    						break
    					}
    				}
    				if(lock_status_kids_flag){
    					this.tagl_def_worker_show = true;	
    				}
	                
	                break;	 
	            case this.dialog_tagldef_basicreq :
	                this.tagl_def_basicreq_show = true;
	                break;
	            case this.dialog_tagldef_point :
		            if( this.tagl_record.point_list.length == 0){
    					return
    				}
	                this.tagl_def_point_show = true;
	                break;
	           	default :
	                break;
            };
            
		},
		tagl_dialog_return (params) {
        	if (params[0]) {
        		var ret_tagl_record = params[1];
        		this.tabledata1[this.tagl_index] = ret_tagl_record;
        	}
        	switch (this.select_item_name) {  
	        	case this.dialog_tagldef_reason :
	                this.tagl_def_reason_show = false;    
	                break;	
	            case this.dialog_tagldef_others :
	                this.tagl_def_others_show = false;    
	                break;   
	            case this.dialog_tagldef_remark :
	                this.tagl_def_remark_show = false;    
	                break; 
	            case this.dialog_tagldef_refdoc :
	                this.tagl_def_reference_show = false;    
	                break;
	            case this.dialog_tagldef_hureqpost :
	                this.tagl_def_hureqpost_show = false;
	                break;
	            case this.dialog_tagldef_notice :
	                this.tagl_def_notice_show = false;    
	                break;
	            case this.dialog_tagldef_worker :
	                this.tagl_def_worker_show = false;    
	                break; 
	            case this.dialog_tagldef_relbasicreq :
	                this.tagl_def_relbasicreq_show = false;
	                break;
	            case this.dialog_tagldef_basicreq :
	                this.tagl_def_basicreq_show = false;
	                break;
	            case this.dialog_tagldef_point :
	                this.tagl_def_point_show = false;    
	                break;     
	            default :
	                break;

            };
        },
        taglana_select_item(ret_tagl_index, select_item){
            this.tagl_index = ret_tagl_index;
            this.tagl_record = this.tabledata1[this.tagl_index].analysis_list[0];
            this.select_item_name = select_item;
           
            if(this.tabledata1[this.tagl_index].analysis_list[0].lock_status == 1){
            	return
            }
            switch (this.select_item_name) {
            	case this.dialog_taglana_reason :
	                this.tagl_ana_reason_show = true;
	                break; 
	            case this.dialog_taglana_seqdiagram :
	                this.tagl_ana_seqdiagram_show = true;
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
        		this.tabledata1[this.tagl_index].analysis_list[0] = ret_taglana_record;
        	}
        	switch (this.select_item_name) {  
        	    case this.dialog_taglana_reason :
	                this.tagl_ana_reason_show = false;    
	                break;  
	            case this.dialog_taglana_seqdiagram :
	                this.tagl_ana_seqdiagram_show = false;    
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
//      definition_delete( del_definition_index) {		
//      	if(this.Roles=="Admin"||this.Roles=="PL"||this.Roles=="Leader"){
//				if(this.tabledata1[del_definition_index].lock_status == 1){
//	            	return;
//	          	}	
//	        	this.$confirm('此操作将永久删除数据，是否继续?','提示',{
//	        		confirmButtonText:"确定",
//	        		cancelButtonText:"取消",
//	        		type:'warning'
//	        	}).then(()=>{
//	        		if(this.tabledata1[del_definition_index].analysis_list!=""){
//	        			this.$alert("该条 TAGL要件定義 下含有 TAGL要件分析，不可删除")
//	        		}else{
//						var definition_tmp = [];
//			        	var definition_num = this.tabledata1.length;
//			        	if (del_definition_index + 1 > definition_num) {
//			                return;
//			        	};
//	
//			    		for (var i = definition_num - 1; i > del_definition_index; i-- ) {
//			                 definition_tmp.push(this.tabledata1.pop());
//			    		};
//			    		this.tabledata1.pop();
//			    		for (var j = (definition_tmp.length - 1); j >= 0  ; j--) {
//			                this.tabledata1.push(definition_tmp.pop());
//			    		};
//			    		this.get_save_array()
//	        		}
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
//      	
//      },    
//      taglana_delete(definition_index){
//      	if(this.Roles=="Admin"||this.Roles=="PL"||this.Roles=="Leader"){
//				if(this.tabledata1[definition_index].analysis_list[0].lock_status == 1){
//	            	return
//	            }
//	        	this.$confirm('此操作将永久删除数据，是否继续?','提示',{
//	        		confirmButtonText:"确定",
//	        		cancelButtonText:"取消",
//	        		type:'warning'
//	        	}).then(()=>{
//					this.tabledata1[definition_index].analysis_list.splice(0,1)
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
					$(".tagltable").css({display:"none"})
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
						$(".tagltable").css({display:"none"})
						$(".taglana_table").css({display:"none"})
					});
					this.$emit('dialog_close', [false]);	
			  }).catch(() => {
			    	
			    })
			}
		},
		accordion(table_id,definition_index){
			if(table_id==3){
				$(".tagl_div").eq(definition_index).children(".tagltable").eq(0).toggle(function(){})
			}else if(table_id==4){
				$(".tagl_div").eq(definition_index).children(".taglana_div").eq(0).children(".taglana_table").eq(0).toggle(function(){})
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
