<template>
	<div class="dialog"  id="dialog" v-show="show" v-loading.fullscreen.lock="fullscreenLoading" element-loading-text="正在保存中,请稍等... ...">
<!--审核弹窗-->
			<dialog_check_list  @dialog_close = "CheckListReturn" v-bind:dialog_show='check_list_show' :check_list_type='Array_Check_List' :all_data='arl_tree' :upload_id='arl_id'>
		    </dialog_check_list>
		    
		    <dialog_recheck_list  @dialog_close = "ReCheckListReturn" v-bind:dialog_show='re_check_list_show' :check_list_type='Array_Check_List' :all_data='arl_tree' :upload_id='arl_id'>
		    </dialog_recheck_list>
		    <!--<dialog_check_list_admit  @dialog_close = "CheckListReturn" v-bind:dialog_show='check_list_show' v-bind:check_list_type='Array_Check_List'>
		    </dialog_check_list_admit>-->
		    
<!--HU的弹窗-->
			<dialog_hudef_reason  @dialog_close = "hu_dialog_return" v-bind:dialog_show='hu_reason_show'  v-bind:hu_data="hu_record">
		    </dialog_hudef_reason>
		    
            <dialog_hudef_worker  @dialog_close = "hu_dialog_return" v-bind:dialog_show='hu_work_show'  v-bind:hu_data="hu_record">
		    </dialog_hudef_worker>

			<dialog_hudef_option  @dialog_close = "hu_dialog_return" v-bind:dialog_show='hu_option_show' v-bind:hu_data="hu_record" :arl_system_conf="arl_system_conf">
		    </dialog_hudef_option>

			<dialog_hudef_evidence  @dialog_close = "hu_dialog_return" v-bind:dialog_show='hu_funcconfig_show' v-bind:hu_data="hu_record">
		    </dialog_hudef_evidence>

			<dialog_hudef_others  @dialog_close = "hu_dialog_return" v-bind:dialog_show='hu_others_show' v-bind:hu_data="hu_record">
		    </dialog_hudef_others>

			<dialog_hudef_remark  @dialog_close = "hu_dialog_return" v-bind:dialog_show='hu_remark_show' v-bind:hu_data="hu_record">
		    </dialog_hudef_remark>

			<dialog_hudef_relbasicreq  @dialog_close = "hu_dialog_return" v-bind:dialog_show='hu_relrequirement_show' v-bind:hu_data="hu_record">
		    </dialog_hudef_relbasicreq>

		    <dialog_hudef_basicreq  @dialog_close = "hu_dialog_return" v-bind:dialog_show='hu_basicreq_show' v-bind:hu_data="hu_record">
		    </dialog_hudef_basicreq>
		    
		    <dialog_hudef_point @dialog_close = 'hu_dialog_return' v-bind:dialog_show='hu_point_show' v-bind:hu_data="hu_record">
		    </dialog_hudef_point>
		    
<!--TAGL要件定义的弹窗-->
			<dialog_tagldef_reason  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_reason_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_reason>

			<dialog_tagldef_others  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_others_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_others>

		    <dialog_tagldef_remark  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_remark_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_remark>
		    
		    <dialog_tagldef_refdoc  @dialog_close = "tagl_dialog_return" v-bind:dialog_show='tagl_def_reference_show' v-bind:tagl_def_data="tagl_record">
		    </dialog_tagldef_refdoc>

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
	   	    		<!--<span class="fr hu_span" style="fontWeight:bold;color:#42b983;"  @click="setReCheckList()"><i class="el-icon-upload2"> 审核</i></span>-->
	   	    	</div>
				<div class="arl_table">
		   	    	<div style="clear: both;"></div>
					<!-- ARL表格 -->
					<div  v-for="(arl_record, arl_index) in arl_tree">
						<!-- arl的复制删除等功能目前不做 -->
					 	<div class="title_arl accordion" id="arl_title">
					 		<span class="fl "  @click="accordion(1,arl_index)"><i class="el-icon-arrow-right"></i>{{arl_record.title}}</span>
					 		<span class="fl"  style="marginLeft: 189px;marginRight:6px;">指派给 </span>
						<!-- 	<el-select v-model="arl_record.user_id" placeholder="请选择" style="width:135px;">
								<el-option v-for="item in names" :key="item.user_id" :label="item.user_name" :value="item.user_id"></el-option>
							</el-select> -->
							
							<el-cascader :options="options_names" v-model="user_group_value"  filterable @change='user_group()' :disabled="arl_record.lock_status ==1?true:false"></el-cascader>
							<div style="float: right;height:40px">
								<!-- <span class="fr hu_span" style="fontWeight:bold;marginRight:20px;color:#42b983"><i class="el-icon-plus"@click="hu_new()"> 新增</i></span> -->
			    	     		<el-dropdown>
									<span class="fr " style="display:block;fontWeight:normal;color:black;color:#42b983" id="menu_pr"><i class="el-icon-plus" id="el-icon-plus"></i> 新增</span>
									<el-dropdown-menu slot="dropdown">
										<el-dropdown-item>
											<span style="display:block;width:100%;height:100%;fontSize:12px" @click="hu_new()">HU要件定義</span>
										</el-dropdown-item>
									</el-dropdown-menu>
								</el-dropdown>
							</div>
					 	</div>
					 	 <!-- 数据只做显示 -->
		    	     	<div class="arltable" :class="arl_record.lock_status == 1?'lock_show':''">
		    	     		<!-- 这个是只显示重要信息的  只留一个table_content 渲染就好 重要信息是长显示-->
		    	     		<div class='table_content' style="width:366px">
		    	     			<p class="table_title">
		    	     				<span>転記してきた要件</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll" :title="arl_record.req_post" :class="arl_record.lock_status == 1?'lock_show':''">
		    	     				<span>{{arl_record.req_post}}</span>
		    	     			</p>
		    	     		</div>
		    	     		<div class='table_content' style="width:160px">
		    	     			<p class="table_title">
		    	     				<span>備考、不明点</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll" :title="arl_record.remark" :class="arl_record.lock_status == 1?'lock_show':''">
		    	     			    <span>{{arl_record.remark}}</span>
		    	     			</p>
		    	     		</div>
		    	     		
		    	     		<div class='table_content' style="width:200px">
		    	     			<p class="table_title">
		    	     				<span>状態</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll" :title="arl_record.status" :class="arl_record.lock_status == 1?'lock_show':''">
		    	     				<span>{{arl_record.status}}</span>
		    	     			</p>
		    	     		</div>
		    	     		<div class='table_content' >
		    	     			<p class="table_title">
		    	     				<span>トリガー</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll" :title="arl_record.trigger" :class="arl_record.lock_status == 1?'lock_show':''">
		    	     				<span>{{arl_record.trigger}}</span>
		    	     			</p>
		    	     		</div>
		    	     		<div class='table_content' >
		    	     			<p class="table_title">
		    	     				<span>動作</span>
		    	     			</p>
		    	     			<p class="table_msg content_scroll" :title="arl_record.action" :class="arl_record.lock_status == 1?'lock_show':''">
		    	     				<span>{{arl_record.action}}</span>
		    	     			</p>
		    	     		</div>
							<!-- 这个是显示全部信息的  ，点击操作更多  让其显示  -->
							<div class='table_content' v-show="arl_more" >
								<div class='table_content' >
									<p class="table_title">
										<span>预留</span>
									</p>
									<p class="table_msg" title="初期値は無し">
										预留
									</p>
								</div>
							</div>
		    	     		<!-- arl表格最后一项 操作，点击操作会显示全部信息  因为有动画效果 需要动态的增加arltable的宽度，同时显示隐藏的那些信息将arl_more变成true 方法在show_more里面 -->
		      	     		<div class='table_content last' style="width:122px;border:0 none" >
		    	     			<p class="table_title">
		    	     				<span></span>
		    	     			</p>
		    	     			
		    	     			<p class="table_msg" title="">
		    	     				<el-button type="text" class="table_move" style="color:#ccc"><i class="el-icon-d-arrow-right"></i></el-button>
		    	     			<!--	 <el-button type="text" class="table_move" @click="show_more(1,arl_index)"><i class="el-icon-more"> 更多</i></el-button> -->
		    	     			</p>
		    	     			
		    	     		</div>
		    	     	</div>
		    	     	<!-- ARL connent end -->
		    	  	    <!-- HU表格 -->
		    	     	<div style="marginLeft:15px" v-for="(hu_record, hu_index) in arl_record.hu_list" class="hu_div">
		    	     		<!-- hu的title  删除 复制功能皆开放 -->
			    	     	<div class="title_arl" >
			    	     		<span class="fl"  @click="accordion(2,hu_index)"><i class="el-icon-arrow-right"></i>{{hu_record.title}}</span>
			    	     			<img src="../../assets/img/lock_2.png" alt="闭锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;marginLeft: 58px;" v-if="hu_record.lock_status == 1?true:false" @click="lock_hu(hu_record.lock_status,hu_index)"/>
					 				<img src="../../assets/img/unlock_2.png" alt="开锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;marginLeft: 58px;"v-if="hu_record.lock_status == 0?true:false" @click="lock_hu(hu_record.lock_status,hu_index)"/>
					 				<img src="../../assets/img/unlock_22.png" alt="半锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;marginLeft: 58px;"v-if="hu_record.lock_status == 2?true:false" @click="lock_hu(hu_record.lock_status,hu_index)"/>
			    	     		<span class="fl" style="marginLeft:24px">
			    	     			任務状態 
			    	     			<template>
			    	     				<el-select v-model="hu_record.job_status" placeholder="请选择" :disabled="hu_record.lock_status ==1?true:false">
			    	     					<el-option v-for="item in hu_record.hu_option" :disabled="item.disabled" :key="item.value" :label="item.label" :value="item.value"></el-option>
			    	     				</el-select>
			    	     			</template>
			    	     		</span>
			    	     		<div style="float:right;height:40px;">
									<!--<span class="fr"  style="color:#42b983" @click="hu_delete(hu_index)" v-if="hu_record.lock_status == 0?true:false"><i class="el-icon-delete"> 删除</i></span>-->
									<!--<span class="fr"  style="color:#bfcbd9" @click="hu_delete(hu_index)" v-if="hu_record.lock_status == 1 || hu_record.lock_status == 2?true:false"><i class="el-icon-delete"> 删除</i></span>-->
				    	     		<span class="fr"  style="color:#42b983" @click="hu_copy(hu_index)"><i class="el-icon-share"> 复制</i></span>
				    	     		<el-dropdown>
										<span class="fr " style="display:block;fontWeight:normal;color:black;color:#42b983" id="menu_pr"><i class="el-icon-plus" id="el-icon-plus"></i> 新增</span>
										<el-dropdown-menu slot="dropdown">
											<el-dropdown-item>
												<span style="display:block;width:100%;height:100%;fontSize:12px" @click="hu_new(hu_index)">HU要件定義</span>
											</el-dropdown-item>
											<el-dropdown-item>
												<span style="display:block;width:100%;height:100%;fontSize:12px" @click="definition_new(hu_index)">TAGL要件定義
												</span>
											</el-dropdown-item>
										</el-dropdown-menu>
									</el-dropdown>
			    	     		</div>
			    	     	</div>
			    	     	<!-- 只显示重要的信息 ，同理arl-->
			    	     	<div class="hutable hu_table" :class="hu_record.lock_status == 1?'lock_show':''">
			    	     		
			    	     		<div class='table_content' style="width:100px">
			    	     			<p class="table_title">
			    	     				<span>ユニークID</span>
			    	     			</p>
			    	     			<p class="table_msg" title="" style="textAlign:center" :class="hu_record.lock_status == 1?'lock_show':''">
			    	     			     {{hu_record.unique_id}}
			    	     			</p>
			    	     		</div>
			    	     		<div class='table_content' style="width:562px">
			    	     			<p class="table_title">
			    	     				<span>責務分担</span>
			    	     			</p>
			    	     			<div class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(arl_index, hu_index, dialog_hudef_worker)" :class="hu_record.lock_status == 1 || hu_record.lock_status == 2?'lock_show':''">
										<p title="" v-for="(sequence_record, sequence_index) in hu_record.sequence_list" >
											<span class="option" style="fontWeight:bold">({{sequence_index+1}})<br> 設備:	
												<span style="fontWeight:normal" v-if="sequence_record.name!=''">{{sequence_record.name}}</span>
												<span style="fontWeight:normal" v-if="sequence_record.info!=''">({{sequence_record.info}})</span>
											</span>
											<span class="option" style="fontWeight:bold"> 状態:
												<span style="fontWeight:normal">{{sequence_record.status}}</span>
											</span>
											<span class="option" style="fontWeight:bold">トリガー:
												<span style="fontWeight:normal">{{sequence_record.trigger}}</span>
											</span>
											<span class="option" style="fontWeight:bold"> 動作:
												<span style="fontWeight:normal">{{sequence_record.action}}</span>
											</span>
										</p>
			    	     			</div>
			    	     		</div>
			    	     		<div class='table_content' style="width:250px">
			    	     			<p class="table_title">
			    	     				<span>变更理由与日期</span>
			    	     			</p>			    	     			
			    	     			<p class="table_msg content_scroll table_msg_hover" :title="hu_record.reason"  @dblclick="hu_select_item(arl_index, hu_index, dialog_hudef_reason)" :class="hu_record.lock_status == 1?'lock_show':''">
										<span class="option" style="fontWeight:bold">变更理由:	
											<span style="fontWeight:normal">{{hu_record.reason}}</span>
										</span>
										<span class="option" style="fontWeight:bold">日付:	
											<span style="fontWeight:normal">{{hu_record.new_date}}</span>
										</span>
									</p>
			    	     		</div> 
			    	     		<div class='table_content' style="width:200px">
			    	     			<p class="table_title">
			    	     				<span>指摘</span>
			    	     			</p>
			    	     			<div class="table_msg content_scroll table_msg_hover" v-if="hu_record.point_list.length != 0?true:false" :class="hu_record.lock_status == 1 || hu_record.point_list.length == 0?'lock_show':''" @dblclick="hu_select_item(arl_index, hu_index, dialog_hudef_point)">
										<p title="" v-for="(point_record, point_index) in hu_record.point_list">
											<span class="option" style="fontWeight:bold">({{point_index+1}})<br>
												<!--指摘拿到日:
												<span style="fontWeight:normal" v-html="point_record.point_date"></span>-->
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
										</p>
			    	     			</div>
			    	     			<div class="table_msg content_scroll table_msg_hover" v-if="hu_record.point_list.length == 0?true:false" :class="hu_record.lock_status == 1 || hu_record.point_list.length == 0?'lock_show':''">
			    	     			</div>
			    	     		</div>
								<!-- 这个是显示全部信息的  ，点击操作更多  让其显示  -->
								<div class='table_content_hidden' style="width:250px">
			    	     			<p class="table_title">
			    	     				<span>オプション項目</span>
			    	     			</p>
			    	     			<!-- 6个option  如果option是默认选项则只显示システム構成 -->
			    	     			<p class="table_msg content_scroll table_msg_hover" title=""  @dblclick="hu_select_item(arl_index, hu_index, dialog_hudef_option)" :class="hu_record.lock_status == 1?'lock_show':''">
			    	     				<span class="option" style="fontWeight:bold">AMP:
			    	     					<span style="fontWeight:normal">{{hu_record.amp}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">DSRC:
			    	     					<span style="fontWeight:normal">{{hu_record.dsrc}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">DCM:
			    	     					<span style="fontWeight:normal">{{hu_record.dcm}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">RSE:
			    	     					<span style="fontWeight:normal">{{hu_record.rse}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">TouchPad:
			    	     					<span style="fontWeight:normal">{{hu_record.touch_pad}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">SeparateDisp:
			    	     					<span style="fontWeight:normal">{{hu_record.separate_disp}}</span>
			    	     				</span>
			    	     				<span class="option" style="fontWeight:bold">システム構成:
			    	     					<span style="fontWeight:normal">{{hu_record.system_conf}}</span>
			    	     				</span>
			    	     			</p>
			    	     		</div>
			    	     		
			    	     		<div class='table_content_hidden' style="width:250px">
			    	     			<p class="table_title">
			    	     				<span>関連基本要件</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover" :title="hu_record.rel_requirement"  @dblclick="hu_select_item(arl_index, hu_index, dialog_hudef_relbasicreq)"  :class="hu_record.lock_status == 1?'lock_show':''">
			    	     			    <span>{{hu_record.rel_requirement}}</span> 
			    	     			</p>
			    	     		</div>   
								<div class='table_content_hidden' >
			    	     			<p class="table_title">
			    	     				<span>基本要件</span>
			    	     			</p>
			    	     			<p class="table_msg content_scroll table_msg_hover" :title="hu_record.basic_req" @dblclick="hu_select_item(arl_index, hu_index, dialog_hudef_basicreq)" :class="hu_record.lock_status == 1?'lock_show':''">
			    	     			    <span>{{hu_record.basic_req}}</span> 
			    	     			</p>
			    	     		</div> 
								<div class='table_content_hidden'>
									<p class="table_title">
										<span>備考</span>
									</p>
									<p class="table_msg table_msg_hover" :title="hu_record.remark" @dblclick="hu_select_item(arl_index, hu_index, dialog_hudef_remark)" :class="hu_record.lock_status == 1?'lock_show':''">
										<span>{{hu_record.remark}}</span>
									</p>
								</div>
                                <div class='table_content_hidden'>
								    <p class="table_title">
										<span>機能配置を判断したエビデンス</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(arl_index, hu_index, dialog_hudef_evidence)"  :class="hu_record.lock_status == 1?'lock_show':''">
									    <span class="option" style="fontWeight:bold"> 001 システム仕様書--章Chapter/Section or ページ番号 Page No:
									        <span>{{hu_record.sys_spec_chapter}}</span> 
									    </span>
									    <span class="option" style="fontWeight:bold"> 003 共通アプリ?AVC-LAN仕様書--章　Chapter/Section or ページ番号 Page No:
									        <span>{{hu_record.common_chapter}}</span> 
									    </span> 
									    <span class="option" style="fontWeight:bold"> シーケンス仕様 Sequence spec:
									        <span>{{hu_record.common_seq_spec}}</span>
									    </span> 
									    <span class="option" style="fontWeight:bold"> シーケンス番号Sequence No:
									        <span>{{hu_record.common_seq_no}}</span>
									    </span> 
									    <span class="option" style="fontWeight:bold">コマンドガイドCommand guide:
									        <span>{{hu_record.common_cmd_guide}}</span>
									    </span>  
									    <span class="option" style="fontWeight:bold"> OPC:
                                            <span>{{hu_record.common_opc}}</span> 
									    </span> 
									    <span class="option" style="fontWeight:bold"> 318 DCU-MEU間連携仕様書DCU-MEU interaction spec.--機能配置?機能仕様 Function location and spec:
									        <span>{{hu_record.inter_loc_spec}}</span> 
 									    </span> 
									    <span class="option" style="fontWeight:bold"> 章　Chapter/Section or ページ番号 Page No :
									        <span>{{hu_record.inter_chapter}}</span>
									    </span> 
									    <span class="option" style="fontWeight:bold"> その他資料Other document --- ドキュメント名 ※トヨタ仕様の場合は仕様番号も記載する事:
									        <span>{{hu_record.other_doc}}</span> 
									    </span> 									    
									    <span class="option" style="fontWeight:bold">章　Chapter/Section or ページ番号 Page No:
									        <span>{{hu_record.other_chapter}}</span> 
									    </span> 										
									</p>
                                </div>
                                <div class='table_content_hidden'  >
								    <p class="table_title">
										<span>其他</span>
									</p>
									<p class="table_msg content_scroll table_msg_hover" @dblclick="hu_select_item(arl_index, hu_index, dialog_hudef_others)"  :class="hu_record.lock_status == 1?'lock_show':''">
										<span class="option" style="fontWeight:bold"> 担当:
									        <span>{{hu_record.author}}</span> 
									    </span>
									    <span class="option" style="fontWeight:bold"> テスト結果:
									        <span>{{hu_record.test_results}}</span> 
									    </span>
									    <span class="option" style="fontWeight:bold"> 未要件分析:
									        <span>{{hu_record.future_req}}</span> 
									    </span> 
									    <span class="option" style="fontWeight:bold"> 備考1:
									        <span>{{hu_record.remark1}}</span>
									    </span> 
									    <span class="option" style="fontWeight:bold"> 備考2:
									        <span>{{hu_record.remark2}}</span>
									    </span> 
									    <span class="option" style="fontWeight:bold"> 要件漏れチェック:
									        <span>{{hu_record.leak_check}}</span>
									    </span>  
									    <span class="option" style="fontWeight:bold"> 最終修正担当:
                                            <span>{{hu_record.last_modifier}}</span> 
									    </span> 
									    <span class="option" style="fontWeight:bold"> 日付:
									        <span>{{hu_record.new_date}}</span> 
 									   </span> 
 									   <span class="option" style="fontWeight:bold"> 除外:
									        <span>{{hu_record.exception}}</span> 
									    </span>
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
			    	   		<!-- TAGL表格 -->
				    	    <div style="marginLeft:15px;" v-for="(definition_record, definition_index) in hu_record.definition_list" class="tagl_div">
				    	    	<div class="title_arl" >
				    	     		<span class="fl"  @click="accordion(3,hu_index,definition_index)"><i class="el-icon-arrow-right"></i>{{definition_record.title}}</span>
				    	     			<img src="../../assets/img/lock_2.png" alt="闭锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;marginLeft: 15px;" v-if="definition_record.lock_status == 1?true:false" @click="lock_Def(definition_record.lock_status,hu_index,definition_index)"/>
					 					<img src="../../assets/img/unlock_2.png" alt="开锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;marginLeft: 15px;"v-if="definition_record.lock_status == 0?true:false" @click="lock_Def(definition_record.lock_status,hu_index,definition_index)"/>
					 					<img src="../../assets/img/unlock_22.png" alt="半锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;marginLeft: 15px;"v-if="definition_record.lock_status == 2?true:false" @click="lock_Def(definition_record.lock_status,hu_index,definition_index)"/>
				    	     		<span class="float"  style="marginLeft:26px">
				    	     			任務状態
				    	     			<template>
				    	     				<el-select v-model="definition_record.job_status" placeholder="请选择" :disabled="TAGLDef_stuate_flog||definition_record.lock_status?true:false" style="width:135px;">
				    	     					<el-option v-for="item in definition_record.def_option" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled"></el-option>
				    	     				</el-select>
				    	     			</template>
				    	     		</span>
				    	     		<div style="float: right;height:40px;">
										<!--<span class="fr" style="color:#42b983" @click="definition_delete(hu_index, definition_index)"><i class="el-icon-delete" v-if="definition_record.lock_status == 0?true:false"> 删除</i></span>-->
										<!--<span class="fr" style="color:#bfcbd9" @click="definition_delete(hu_index, definition_index)"><i class="el-icon-delete" v-if="definition_record.lock_status == 1||definition_record.lock_status == 2?true:false"> 删除</i></span>-->

				    	     			<span class="fr" style="color:#42b983" @click="definition_copy(hu_index,definition_index)"><i class="el-icon-share"> 复制</i></span>
				    	     			<el-dropdown>
				    	     				<span class="fr"style="fontWeight:normal;color:#42b983" ><i class="el-icon-plus"> 新增</i></span>
				    	     				<el-dropdown-menu slot="dropdown">
				    	     					<el-dropdown-item >
				    	     						<span style="display:block;width:100%;height:100%;fontSize:12px" @click="definition_new(hu_index)">TAGL要件定義</span>
				    	     					</el-dropdown-item>
				    	     					<el-dropdown-item>
				    	     						<span style="display:block;width:100%;height:100%;fontSize:12px"  @click="taglana_new(hu_index,definition_index)">TAGL要件分析</span>
				    	     					</el-dropdown-item>
				    	     				</el-dropdown-menu>
				    	     			</el-dropdown>
				    	     		</div>
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
		    	    		 		<div class='table_content' style="width:547px">
				    	     			<p class="table_title">
				    	     				<span>責務分担</span>
				    	     			</p>
				    	     			<p class="table_msg content_scroll table_msg_hover" title="" @dblclick="tagl_select_item(arl_index, hu_index, definition_index, dialog_tagldef_worker)" :class="definition_record.lock_status == 1 || definition_record.lock_status == 2?'lock_show':''">
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
				    	     			<p class="table_msg content_scroll table_msg_hover" :title="definition_record.reason"  @dblclick="tagl_select_item(arl_index, hu_index, definition_index, dialog_tagldef_reason)" :class="definition_record.lock_status == 1?'lock_show':''">
				    	     			    <span class="option" style="fontWeight:bold">变更理由:	
												<span style="fontWeight:normal">{{definition_record.reason}}</span>
											</span>
											<span class="option" style="fontWeight:bold">日付:	
												<span style="fontWeight:normal">{{definition_record.new_date}}</span>
											</span>
										</p>
				    	     		</div> 
				    	     		<div class='table_content' style="width:200px">
				    	     			<p class="table_title">
				    	     				<span>指摘</span>
				    	     			</p>
				    	     			<p class="table_msg content_scroll table_msg_hover" title=""  v-if="definition_record.point_list.length != 0?true:false" :class="definition_record.lock_status == 1 || definition_record.point_list.length == 0?'lock_show':''" @dblclick="tagl_select_item(arl_index, hu_index, definition_index, dialog_tagldef_point)" >
				    	     				<span v-for="(point_record, point_index) in definition_record.point_list">
				    	     					<span class="option" style="fontWeight:bold">({{point_index+1}})<br />
				    	     					<!--指摘拿到日:
													<span style="fontWeight:normal" v-html="point_record.point_date"></span>-->
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
				    	     			<p class="table_msg content_scroll table_msg_hover" :title="definition_record.rel_requirement"  @dblclick="tagl_select_item(arl_index, hu_index, definition_index, dialog_tagldef_relbasicreq)" :class="definition_record.lock_status == 1?'lock_show':''">
				    	     			    <span>{{definition_record.rel_requirement}}</span> 
				    	     			</p>
				    	     		</div> 
				    	     		
				    	     		<div class='table_content_hidden' >
				    	     			<p class="table_title">
				    	     				<span>基本要件</span>
				    	     			</p>
				    	     			<p class="table_msg content_scroll table_msg_hover" :title="definition_record.basic_req"  @dblclick="tagl_select_item(arl_index, hu_index, definition_index, dialog_tagldef_basicreq)" :class="definition_record.lock_status == 1?'lock_show':''">
				    	     			
				    	     			    <span>{{definition_record.basic_req}}</span> 
				    	     			</p>
				    	     		</div> 
				    	     		<div class='table_content_hidden'>
										<p class="table_title">
											<span>備考</span>
										</p>
										<p class="table_msg table_msg_hover" @dblclick="tagl_select_item(arl_index, hu_index, definition_index, dialog_tagldef_remark)" :class="definition_record.lock_status == 1?'lock_show':''">      
											<span>{{definition_record.remark}}</span>
										</p>
								    </div>
				    	     		<div class='table_content_hidden'>
										<p class="table_title">
											<span>責務分担の特記事項</span>
										</p>
										<p class="table_msg table_msg_hover ontent_scroll" @dblclick="tagl_select_item(arl_index, hu_index,definition_index,dialog_tagldef_notice)" :class="definition_record.lock_status == 1?'lock_show':''">
											<span>{{definition_record.notice}}</span>
										</p>
								    </div>
                                    <div class='table_content_hidden'>
    								    <p class="table_title">
    										<span>参考文献</span>
    									</p>
    									<p class="table_msg table_msg_hover  content_scroll" @dblclick="tagl_select_item(arl_index, hu_index, definition_index, dialog_tagldef_refdoc)" :class="definition_record.lock_status == 1?'lock_show':''">
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
										<p class="table_msg table_msg_hover content_scroll" @dblclick="tagl_select_item(arl_index, hu_index, definition_index, dialog_tagldef_others)" :class="definition_record.lock_status == 1?'lock_show':''">
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
				    	     				<el-button type="text" class="table_move" @click="show_more(3,hu_index,definition_index)"><i class="el-icon-d-arrow-right"></i></el-button>
				    	     			</p>
				    	     		</div>
				    	     	</div>
				    	     	<!-- TAGLANA表格 -->
				    	     	<div style="marginLeft:15px;" v-for="(taglana_record,taglana_index) in definition_record.analysis_list" class="taglana_div">
    	     		    	    	<div class="title_arl" >
    	     		    	     		<span class="fl"  @click="accordion(4,hu_index,definition_index,taglana_index)"><i class="el-icon-arrow-right"></i>{{taglana_record.title}}</span>
    	     		    	     		<img src="../../assets/img/lock_2.png" alt="闭锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;" v-show="taglana_record.lock_status == 1?true:false" @click="lock_Ana(taglana_record.lock_status,hu_index,definition_index,taglana_index)"/>
					 					<img src="../../assets/img/unlock_2.png" alt="开锁图标" style="width: auto;height: 18px;float: left;marginTop: 11px;"v-show="taglana_record.lock_status == 0?true:false" @click="lock_Ana(taglana_record.lock_status,hu_index,definition_index,taglana_index)"/>
    	     		    	     		<span class="fl" style="marginLeft: 26px;">
    	     		    	     			任務状態
    	     		    	     			<template>
    	     		    	     				<el-select v-model="taglana_record.job_status" placeholder="请选择" :disabled="TAGLAna_stuate_flog||taglana_record.lock_status?true:false" style="width:135px;">
    	     		    	     					<el-option v-for="item in taglana_record.ana_option" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled"></el-option>
    	     		    	     				</el-select>
    	     		    	     			</template>
    	     		    	     		</span>
    	     		    	     		<div style="float: right;">
    	     								<!--<span class="fr" style="color:#42b983" @click="taglana_delete(hu_index,definition_index,taglana_index)" v-if="taglana_record.lock_status == 0?true:false"><i class="el-icon-delete"> 删除</i></span>-->
    	     								<!--<span class="fr" style="color:#bfcbd9" @click="taglana_delete(hu_index,definition_index,taglana_index)" v-if="taglana_record.lock_status == 1?true:false"><i class="el-icon-delete"> 删除</i></span>-->
    	     		    	     			<!-- <span class="fr" style="color:#42b983"><i class="el-icon-share"> 复制</i></span> -->
    	     		    	     		<!--	<span class="fr"  style="color:#42b983"><i class="el-icon-plus"> 新增</i></span>-->
    	     		    	     		</div>
    	     		    	     	</div>
 					    	    	<div class="taglana_table"  :class="taglana_record.lock_status == 1?'lock_show':''">
 					    	    		<div class='table_content' style="width:200px">
 					    	    			<p class="table_title">
 					    	    				<span>シーケンス図</span>
 					    	    			</p>
 					    	    			<p class="table_msg table_msg_hover content_scroll" title="" style="textAlign:center" @dblclick="taglana_select_item( arl_index, hu_index, definition_index,dialog_taglana_seqdiagram,taglana_index)" :class="taglana_record.lock_status == 1?'lock_show':''">
 					    	    			    {{taglana_record.seq_diagram}}  
 					    	    			</p>
 					    	    		</div>
 					    	    		<div class='table_content' style="width:432px">
 					    	     			<p class="table_title">
 					    	     				<span>TAGL-PF</span>
 					    	     				
 					    	     			</p>
 					    	     			<p class="table_msg content_scroll table_msg_hover" @dblclick="taglana_select_item( arl_index, hu_index, definition_index, dialog_taglana_worker,taglana_index)" :class="taglana_record.lock_status == 1?'lock_show':''">
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
					    	     			<p class="table_msg content_scroll table_msg_hover" :title="taglana_record.reason" @dblclick="taglana_select_item( arl_index, hu_index, definition_index, dialog_taglana_reason,taglana_index)" :class="taglana_record.lock_status == 1?'lock_show':''">
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
 					    	     			<p class="table_msg content_scroll table_msg_hover" :class="taglana_record.lock_status == 1 || taglana_record.point_list.length == 0 ?'lock_show':''" @dblclick="taglana_select_item(arl_index, hu_index, definition_index, dialog_taglana_point)" v-if="taglana_record.point_list.length !=0?true:false">
 						    	     			<span v-for="(point_record, point_index) in taglana_record.point_list" >
 						    	     				<span class="option" style="fontWeight:bold">({{point_index+1}})<br />
 						    	     				<!--指摘拿到日:<span style="fontWeight:normal" v-html="point_record.point_date"></span>-->
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
					    	     			<p class="table_msg content_scroll table_msg_hover" :title="taglana_record.rel_requirement" @dblclick="taglana_select_item( arl_index, hu_index, definition_index, dialog_taglana_relbasicreq,taglana_index)" :class="taglana_record.lock_status == 1?'lock_show':''">
					    	     			
					    	     			    <span>{{taglana_record.rel_requirement}}</span> 
					    	     			</p>
					    	     		</div>
 					    	     		<div class='table_content_hidden' >
					    	     			<p class="table_title">
					    	     				<span>基本要件</span>
					    	     			</p>
					    	     			<p class="table_msg content_scroll table_msg_hover" :title="taglana_record.basic_req" @dblclick="taglana_select_item(arl_index, hu_index, definition_index, dialog_taglana_basicreq,taglana_index)"  :class="taglana_record.lock_status == 1?'lock_show':''">
					    	     			
					    	     			    <span>{{taglana_record.basic_req}}</span> 
					    	     			</p>
					    	     		</div> 

 		                                <div class='table_content_hidden' >
 										    <p class="table_title">
 												<span>其他</span>
 											</p>
 											<p class="table_msg table_msg_hover content_scroll" @dblclick="taglana_select_item(arl_index, hu_index, definition_index, dialog_taglana_other,taglana_index)" :class="taglana_record.lock_status == 1?'lock_show':''">
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
 					    	     				<el-button type="text" class="table_move" @click="show_more(4,hu_index,definition_index,taglana_index)"><i class="el-icon-d-arrow-right"></i></el-button>
 					    	     			</p>
 					    	     		</div>
 					    	     	</div>
				    	     	</div>
				    	     	<!-- TAGLANA  end-->
				    	    </div>
				    	    <!-- TAGL end -->
		    	     	</div>  
		    	     	<!-- HU表格end -->
					</div> 
                    <!-- arl表格end -->
		   	   	</div>
			</div>
	</div>
</template>
<script>
import Dialog_Check_List from './Dialog_Check_List'
import Dialog_Recheck_List from './Dialog_Recheck'
	
import Dialog_HUDef_Reason from './Dialog_HUDef_Reason.vue'
import Dialog_HUDef_Worker from './Dialog_HUDef_Worker.vue'
import Dialog_HUDef_Option from './Dialog_HUDef_Option.vue'
import Dialog_HUDef_RelBasicReq from './Dialog_HUDef_RelBasicReq.vue'
import Dialog_HUDef_BasicReq from './Dialog_HUDef_BasicReq.vue'
import Dialog_HUDef_Remark from './Dialog_HUDef_Remark.vue'
import Dialog_HUDef_Evidence from './Dialog_HUDef_Evidence.vue'
import Dialog_HUDef_Others from './Dialog_HUDef_Others.vue'
import Dialog_HUDef_Point from './Dialog_HUDef_Point'

import Dialog_TAGLDef_Reason from './Dialog_TAGLDef_Reason.vue'
import Dialog_TAGLDef_Worker from './Dialog_TAGLDef_Worker.vue'
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
    props: ['input_show', 'input_arl_id', 'input_hu_id'], 

	components:{
		dialog_recheck_list: Dialog_Recheck_List,
		dialog_check_list : Dialog_Check_List,
		dialog_hudef_reason : Dialog_HUDef_Reason,
       	dialog_hudef_worker : Dialog_HUDef_Worker,
		dialog_hudef_option : Dialog_HUDef_Option,
		dialog_hudef_relbasicreq : Dialog_HUDef_RelBasicReq,
		dialog_hudef_basicreq : Dialog_HUDef_BasicReq,
		dialog_hudef_remark : Dialog_HUDef_Remark,
		dialog_hudef_evidence : Dialog_HUDef_Evidence,
		dialog_hudef_others : Dialog_HUDef_Others,
		dialog_hudef_point: Dialog_HUDef_Point,
		dialog_tagldef_reason : Dialog_TAGLDef_Reason,
		dialog_tagldef_worker : Dialog_TAGLDef_Worker,
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
			Array_Check_List:['','',''],
			hu_list_num: 0,
			definition_list_num: 0,
			analysis_list_num: 0,
			save_array: [],
			open_array: [],
			arl_tree_copy:[],
//			IsChangeReason: true,
			
            arl_more : false,
            hu_more : false,
            tagl_more : false,
			
			dialog_open_data: '',
			dialog_save_data: '',
			
            show : false,
            arl_id : "",
            hu_id : "",
            select_item_name : '',    // select
            arl_index : 0,       // select index
            hu_index : 0,        // select index
            tagl_index : 0,      // select index
            taglana_index: 0,
            arl_tree : [],
            data_before_save: [],
            hu_record : {},
            tagl_record : {},
          	arl_system_conf:"",
          	
          	dialog_recheck_list : 'recheck_list',
          	re_check_list_show : false,
          	
          	dialog_check_list : 'check_list',
          	check_list_show : false,
          	
            dialog_hudef_reason : "hu_reason",
            hu_reason_show : false,
          	
            dialog_hudef_worker : "hu_work",
            hu_work_show : false,
            
            dialog_hudef_option : "hp_option",
            hu_option_show : false,
            
            dialog_hudef_evidence : "funcconfig",
            hu_funcconfig_show : false,
            
            dialog_hudef_others : "others",
            hu_others_show : false,
            
            dialog_hudef_remark : "remark",
            hu_remark_show : false,

            dialog_hudef_relbasicreq : "hu_relrequirement",               
            hu_relrequirement_show : false,  

            dialog_hudef_basicreq : "hu_basicreq",               
            hu_basicreq_show : false,  
            
            dialog_hudef_point : "hu_point",
            hu_point_show : false, 
            
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
		this.getLeadGroup()
		this.Group()
	},
	computed:{

	},
	methods:{
		setCheckList(){
			if(this.Array_Check_List.toString() == ['','',''].toString()){
				this.fullscreenLoading = true
				this.$axios.post(this.Ip+'/PostFullContent',this.arl_tree)
				.then(res=>{
					if(res.data.result=="OK"){
						this.onshow()
						this.fullscreenLoading = false
						this.$notify({
							type:'success',
							message:'保存成功'
						})
					}else{
						this.fullscreenLoading = false
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
			}else{
				this.check_list_show = true	
			}
		},
		setReCheckList(){
			if(this.Roles=="Admin"||this.Roles=="PL"){
				this.SaveAndCheckData(2)
			}else if(this.Roles=="Leader"){
				var b = false;
				if(this.leadGp.length!=0){
					for(var i=0;i<this.leadGp.length;i++){
						if(this.old_group == this.leadGp[i]){
							b = true;
						}
					}
				}
				if(b==true){
					this.SaveAndCheckData(2)
				}else if(window.sessionStorage.getItem('admin')==this.arl_tree[0]['user_id']){
					this.SaveAndCheckData(2)
				}else{
					this.$notify({
						type:'error',
						message:'您的权限不足，无法审核',
						showClose:true,
						duration:'0',
					})
				}
			}else if(this.Roles=="Member"){
					this.$notify({
						type:'error',
						message:'您的权限不足，无法更改',
						showClose:true,
						duration:'0',
					})		
			}else if(this.Roles=="Translator"){
				this.SaveAndCheckData(2)
			}else{
				this.$notify({
					type:'error',
					message:'您的权限不足，无法审核',
					showClose:true,
					duration:'0',
				})
			}

		},
		ReCheckListReturn(params){
			this.re_check_list_show = false
			if (params[0] == false) {
				this.arl_tree = JSON.parse(JSON.stringify(this.data_before_save))
				this.arl_tree[0].list2 = params[1] 
			} else{
				this.onshow()
			}
			
		},
		CheckListReturn(params){
			this.check_list_show = false
			if(params[0]){
				this.onshow()
			}else{
				this.arl_tree = this.data_before_save
				this.arl_tree[0].list1 = params[1][0].list1
			}
			
		},
		lock_hu(lock_flag,hu_index){
			if(this.Roles == 'PL' || this.Roles == 'Admin'){
				if(lock_flag ==1){
					let bansuo_flag = false
					
					if(bansuo_flag == true ){
				
					}else{
						this.arl_tree[0].hu_list[hu_index].lock_status = 0
					}
					
				}else if(lock_flag == 0){
					this.arl_tree[0].hu_list[hu_index].lock_status = 1
				}else{
					this.arl_tree[0].hu_list[hu_index].lock_status = 1
				}
			}else{
				this.$notify({
					type:'error',
					message:'您的权限不足，无法更改',
				})
			}
		},
		lock_Def(lock_flag,hu_index,definition_index){
			if(this.Roles == 'PL' || this.Roles == 'Admin'){
				if(lock_flag == 1){
					//子级没有闭锁的情况下，父级为闭锁时，点击闭锁，变为开锁
					this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].lock_status = 0
				}else{
					//子级没有闭锁的情况下，父级为开锁时，点击开锁，变为闭锁
					this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].lock_status = 1
				}
			}else{
				this.$notify({
					type:'error',
					message:'您的权限不足，无法更改',
				})
			}
		},
		lock_Ana(lock_flag,hu_index,definition_index,taglana_index){
			if(this.Roles == 'PL' || this.Roles == 'Admin'){
				if(lock_flag ==1){
					this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].analysis_list[taglana_index].lock_status = 0				
				}else{
					this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].analysis_list[taglana_index].lock_status = 1
				}
			}else{
				this.$notify({
					type:'error',
					message:'您的权限不足，无法更改',
				})
			}
		},
		Group(){
			this.$axios.get(this.Ip+"/GpGroupDetail")
	      		.then(res=>{
	      		      	for(var i = 0 ; i < res.data.length ;i++){
	      				this.options_names.push({"label":res.data[i].group_name,"value":res.data[i].group_id,"children":[]})
	      				for(var j = 0 ; j < res.data[i].user_list.length ;j++){
	      					this.options_names[i].children.push({'label':res.data[i].user_list[j].user_name,"value":res.data[i].user_list[j].user_id})
	      				}	
	      			}
	      		})	
		},
		statusOption(){
			if(this.arl_tree[0].hu_list.length!=0){
				for(var i=0;i<this.arl_tree[0].hu_list.length;i++){

					this.arl_tree[0].hu_list[i].hu_option=this.options;

					if(this.arl_tree[0].hu_list[i].control_list.length!=0){
						for(var j=0;j<this.arl_tree[0].hu_list[i].control_list.length;j++){

							var first = this.arl_tree[0].hu_list[i].control_list[j]
							if(this.arl_tree[0].hu_list[i].job_status==first){
								for(var k=0;k<this.arl_tree[0].hu_list[i].control_list.length;k++){
									this.arl_tree[0].hu_list[i].hu_option[this.arl_tree[0].hu_list[i].control_list[k]-1].disabled = false;

								}
								
							}

						}
					}else{
						this.HU_stuate_flog=true
					}
					
					if(this.arl_tree[0].hu_list[i].definition_list.length!=0){
						for(var j=0;j<this.arl_tree[0].hu_list[i].definition_list.length;j++){

							this.arl_tree[0].hu_list[i].definition_list[j].def_option=this.options;

							if(this.arl_tree[0].hu_list[i].definition_list[j].control_list.length!=0){

								for(var k=0;k<this.arl_tree[0].hu_list[i].definition_list[j].control_list.length;k++){

									var sec = this.arl_tree[0].hu_list[i].definition_list[j].control_list[k]

									if(this.arl_tree[0].hu_list[i].definition_list[j].job_status==sec){

										for(var l=0;l<this.arl_tree[0].hu_list[i].definition_list[j].control_list.length;l++){

											this.arl_tree[0].hu_list[i].definition_list[j].def_option[this.arl_tree[0].hu_list[i].definition_list[j].control_list[l]-1].disabled = false;
										}
										
									}
								}
							}else{
								this.TAGLDef_stuate_flog=true

							}
							if(this.arl_tree[0].hu_list[i].definition_list[j].analysis_list.length!=0){

								for(var k=0;k<this.arl_tree[0].hu_list[i].definition_list[j].analysis_list.length;k++){

									this.arl_tree[0].hu_list[i].definition_list[j].analysis_list[k].ana_option=this.options;
									
									if(this.arl_tree[0].hu_list[i].definition_list[j].analysis_list[k].control_list.length!=0){

										for(var l=0;l<this.arl_tree[0].hu_list[i].definition_list[j].analysis_list[k].control_list.length;l++){

											var third = this.arl_tree[0].hu_list[i].definition_list[j].analysis_list[k].control_list[l]

											if(this.arl_tree[0].hu_list[i].definition_list[j].analysis_list[k].job_status==third){

												for(var m=0;m<this.arl_tree[0].hu_list[i].definition_list[j].analysis_list[k].control_list.length;m++){
													this.arl_tree[0].hu_list[i].definition_list[j].analysis_list[k].ana_option[this.arl_tree[0].hu_list[i].definition_list[j].analysis_list[k].control_list[m]-1].disabled=false;
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
					
				}
			}
		},
		onshow () {
			this.Array_Check_List = ['','','']
            this.arl_id =  this.input_arl_id; 
            this.hu_id = this.input_hu_id;  
			this.$axios.get(this.Ip+'/ArlTreeInfo/'+this.arl_id+'/'+window.sessionStorage.getItem('admin')+'/'+1)
				.then(res => {
					this.Roles = window.sessionStorage.getItem('Roles')
					this.arl_tree = [];
					this.arl_tree = JSON.parse(JSON.stringify(res.data.content));
					this.arl_tree[0]['modify_user_id']=window.sessionStorage.getItem('admin');
					this.user_group_value = []
					this.user_group_value[0]  = this.arl_tree[0].group_id
					this.user_group_value[1]  = this.arl_tree[0].user_id
					this.old_group = res.data.content[0]['group_id']
					this.hu_tree = this.arl_tree[0].hu_list;
					this.arl_system_conf = this.arl_tree[0].sys_conf_id
					this.show = true;
					this.statusOption();
					this.arl_tree_copy = JSON.parse(JSON.stringify(this.arl_tree))
					this.hu_list_num = this.arl_tree[0].hu_list.length;
					this.open_array = []
					for(let i = 0;i<this.arl_tree[0].hu_list.length;i++){
						let tagl_array = [];
						for(let j=0;j<this.arl_tree[0].hu_list[i].definition_list.length;j++){
							let taglana_array = []
							for(let k=0;k<this.arl_tree[0].hu_list[i].definition_list[j].analysis_list.length;k++){
								taglana_array.push('1')
							}
							tagl_array.push(taglana_array)
						}
						this.open_array.push(tagl_array)
					}
					this.dialog_open_data = JSON.stringify(this.arl_tree[0])
					this.dialog_save_data = JSON.stringify(this.arl_tree[0])	

				})
				.catch(res=>{
					this.$notify({
						type:'error',
						message:'网络异常，请重新刷新',
						showClose:true,
						duration:'0',
					})
					this.arl_tree=[];
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
			if(window.sessionStorage.getItem('Uall')=='test'&&this.Ip == 'http://192.168.0.56:5000'){
				return
			}
			this.Roles = window.sessionStorage.getItem('Roles')
			if(this.Roles=="Admin"||this.Roles=="PL"){
				this.SaveAndCheckData(1);
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
					this.SaveAndCheckData(1);
				}else if(window.sessionStorage.getItem('admin')==this.arl_tree[0]['user_id']){
					this.SaveAndCheckData(1);
				}else{
					this.$notify({
						type:'error',
						message:'您的权限不足，无法更改',
						showClose:true,
						duration:'0',
					})
				}
			}else if(this.Roles=="Member"){
				if(window.sessionStorage.getItem('admin')==this.arl_tree[0]['user_id']){
					this.SaveAndCheckData(1);
				}else{
					this.$notify({
						type:'error',
						message:'您的权限不足，无法更改',
						showClose:true,
						duration:'0',
					})
				}
					
			}else if(this.Roles=="Translator"){
				this.SaveAndCheckData(1);
			}else{
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
			for(let i = 0;i<this.arl_tree[0].hu_list.length;i++){
				let tagl_array = [];
				for(let j=0;j<this.arl_tree[0].hu_list[i].definition_list.length;j++){
					let taglana_array = []
					for(let k=0;k<this.arl_tree[0].hu_list[i].definition_list[j].analysis_list.length;k++){
						taglana_array.push('1')
					}
					tagl_array.push(taglana_array)					
				}
				this.save_array.push(tagl_array)
			}
		},
		SaveAndCheckData(val){
			let IsChangeReason = true
			this.get_save_array()
			this.data_before_save = JSON.parse(JSON.stringify(this.arl_tree))
			
			//判断是否新增或删除内容，来显示不同类型的审核
			if(this.open_array.length != this.save_array.length){
						this.Array_Check_List[0] = 'hu'
						//判断是否新增内容，来显示不同类型的审核
						if(this.open_array.length < this.save_array.length){
							for(let i = this.open_array.length;i<this.save_array.length;i++){
								if(this.save_array[i].length != 0){
									this.Array_Check_List[1] = 'definition'
									for(let k = 0;k<this.save_array[i].length;k++){
										if(this.arl_tree[0].hu_list[i].definition_list[k].analysis_list.length != 0){
											this.Array_Check_List[2] = 'analysis'
										}
									}
								}
							}
						}
						//判断是否删除内容，来显示不同类型的审核
						if(this.open_array.length > this.save_array.length){
							for(let i = this.save_array.length;i<this.open_array.length;i++){
								if(this.open_array[i].length != 0){
									this.Array_Check_List[1] = 'definition'
									for(let k = 0;k<this.open_array[i].length;k++){
										if(this.arl_tree_copy[0].hu_list[i].definition_list[k].analysis_list.length != 0){
											this.Array_Check_List[2] = 'analysis'
										}
									}
								}
							}
						}
				}
			//根据是否修改了内容，来显示不同类型的审核
			for(let i=0;i<this.open_array.length;i++){
				if(this.save_array[i] != undefined) {
					if(this.open_array[i].length != this.save_array[i].length){
						this.Array_Check_List[1] = 'definition'
					}
					if(this.arl_tree[0].hu_list[i].reason == this.arl_tree_copy[0].hu_list[i].reason){
						let hu_delete_data = JSON.parse(JSON.stringify(this.arl_tree[0].hu_list[i]))
						let hu_delete_data_copy = JSON.parse(JSON.stringify(this.arl_tree_copy[0].hu_list[i]))
						delete hu_delete_data.lock_status
						delete hu_delete_data.definition_list
						delete hu_delete_data_copy.lock_status
						delete hu_delete_data_copy.definition_list
						
						if(JSON.stringify(hu_delete_data)!=JSON.stringify(hu_delete_data_copy)){
							this.Array_Check_List[0] = 'hu'
						}
						
						delete hu_delete_data.job_status
						delete hu_delete_data_copy.job_status

						if(JSON.stringify(hu_delete_data)!=JSON.stringify(hu_delete_data_copy)){
							IsChangeReason = IsChangeReason && false;
						}
					}
					else{
						if((this.Roles =="Member"||this.Roles =="Leader")&&(this.arl_tree[0].hu_list[i].job_status==3)){
							this.arl_tree[0].hu_list[i].job_status = 2
						}
					}
					for(let k=0;k<this.open_array[i].length;k++){
						if(this.save_array[i][k] != undefined){
						//判断definition_list中的每一个
							if(this.arl_tree[0].hu_list[i].definition_list[k].reason == this.arl_tree_copy[0].hu_list[i].definition_list[k].reason){
								let tagldef_delete_data = JSON.parse(JSON.stringify(this.arl_tree[0].hu_list[i].definition_list[k]))
								let tagldef_delete_data_copy = JSON.parse(JSON.stringify(this.arl_tree_copy[0].hu_list[i].definition_list[k]))
								delete tagldef_delete_data.lock_status
								delete tagldef_delete_data.analysis_list
								delete tagldef_delete_data_copy.lock_status
								delete tagldef_delete_data_copy.analysis_list
								if(JSON.stringify(tagldef_delete_data)!=JSON.stringify(tagldef_delete_data_copy)){
									this.Array_Check_List[1] = 'definition'
								}
								delete tagldef_delete_data.job_status
								
								delete tagldef_delete_data_copy.job_status

								if(JSON.stringify(tagldef_delete_data)!=JSON.stringify(tagldef_delete_data_copy)){
									IsChangeReason  = IsChangeReason && false
								}
							}
							else{
								if((this.Roles =="Member"||this.Roles =="Leader")&&(this.arl_tree[0].hu_list[i].definition_list[k].job_status==3)){
									this.arl_tree[0].hu_list[i].definition_list[k].job_status = 2
								}
							}
//							//判断taglana_list的每一个
							if(this.arl_tree[0].hu_list[i].definition_list[k].analysis_list.length != this.arl_tree_copy[0].hu_list[i].definition_list[k].analysis_list.length){
								this.Array_Check_List[2] = 'analysis'
							}
							for(let j=0;j<this.open_array[i][k].length;j++){
								if(this.save_array[i][k][j] != undefined){
									if(this.arl_tree[0].hu_list[i].definition_list[k].analysis_list[j].reason == this.arl_tree_copy[0].hu_list[i].definition_list[k].analysis_list[j].reason){
										let taglana_delete_data = JSON.parse(JSON.stringify(this.arl_tree[0].hu_list[i].definition_list[k].analysis_list[j]))
										let taglana_delete_data_copy = JSON.parse(JSON.stringify(this.arl_tree_copy[0].hu_list[i].definition_list[k].analysis_list[j]))
										delete taglana_delete_data.lock_status
										delete taglana_delete_data_copy.lock_status
										
										if(JSON.stringify(taglana_delete_data)!=JSON.stringify(taglana_delete_data_copy)){
											this.Array_Check_List[2] = 'analysis'
										}
										
										delete taglana_delete_data.job_status											
										delete taglana_delete_data_copy.job_status

										if(JSON.stringify(taglana_delete_data)!=JSON.stringify(taglana_delete_data_copy)){
											IsChangeReason  = IsChangeReason && false
										}
									}
									else{
										if((this.Roles =="Member"||this.Roles =="Leader")&&(this.arl_tree[0].hu_list[i].definition_list[k].analysis_list[j].job_status==3)){
											this.arl_tree[0].hu_list[i].definition_list[k].analysis_list[j].job_status = 2
										}
									}
								}
							}
						}
					}	
				}
			}
			if(IsChangeReason){
//				this.fullscreenLoading = true;
				for(let i=0;i<this.open_array.length;i++){
					//判断save_array.hu_list里有没有对象，如果没有，就不用对比；有的话就比较
					if(this.save_array[i] != undefined) {	
						for(let k=0;k<this.open_array[i].length;k++){
							//判断save_array.hu_list[i].definition_list里有没有对象，如果没有，就不用对比；有的话就比较
							if(this.save_array[i][k] != undefined){
									if(this.open_array[i][k].length != 0){
										//TAGL_Ana的reason无变化，去查看上一层数据有无变化
										for(let j =0;j<this.open_array[i][k].length;j++){
											if(this.save_array[i][k][j] != undefined){
												if(this.arl_tree[0].hu_list[i].definition_list[k].analysis_list[j].reason == this.arl_tree_copy[0].hu_list[i].definition_list[k].analysis_list[j].reason){
													//TAGL_Def的责任分担和reason都有变化时，修改TAGL_Ana的reason
													//TAGL_Def的reason无变化时，向上一层查看数据有无变化
													if(this.arl_tree[0].hu_list[i].definition_list[k].reason == this.arl_tree_copy[0].hu_list[i].definition_list[k].reason){
														//只有HU_def的责任分担(sequence_list)中的DCU('type':'DCU')变化时,责任分担才算变化（新增和删除‘DCU’都算变化）
														let array_Open_HUSequeceList = []
														let array_Save_HUSequeceList = []
														if(this.arl_tree[0].hu_list[i].sequence_list.length!=0){
															for(let m = 0;m<this.arl_tree[0].hu_list[i].sequence_list.length;m++){
																let Squence_Open_type = this.arl_tree[0].hu_list[i].sequence_list[m].type
																if( Squence_Open_type== 'DCU'||Squence_Open_type== 'MEU'||Squence_Open_type== 'DCU/MEU'){
																	array_Open_HUSequeceList.push(this.arl_tree[0].hu_list[i].sequence_list[m])
																}
															}
														}
														
														if(this.arl_tree_copy[0].hu_list[i].sequence_list.length!=0){
															for(let m = 0;m<this.arl_tree_copy[0].hu_list[i].sequence_list.length;m++){
																let Squence_Save_type = this.arl_tree_copy[0].hu_list[i].sequence_list[m].type
																if(Squence_Save_type== 'DCU'||Squence_Save_type== 'MEU'||Squence_Save_type== 'DCU/MEU'){
																	array_Save_HUSequeceList.push(this.arl_tree_copy[0].hu_list[i].sequence_list[m])
																}
															}
														}	
														//HU_Def的责任分担和reason都变化时，修改TAGL_Def的reason
														if(this.arl_tree[0].hu_list[i].reason != this.arl_tree_copy[0].hu_list[i].reason && JSON.stringify(array_Open_HUSequeceList) != JSON.stringify(array_Save_HUSequeceList)){
															this.arl_tree[0].hu_list[i].definition_list[k].reason = this.arl_tree[0].hu_list[i].reason
															this.arl_tree[0].hu_list[i].definition_list[k].job_status = 2
														}
													}
													
													else{
														//只有TAGL_def的责任分担(sequence_list)中的DCU('type':'DCU')变化时,责任分担才算变化（新增和删除‘DCU’都算变化）
														let array_Open_TAGLDEFSequeceList = []
														let array_Save_TAGLDEFSequeceList = []
														if(this.arl_tree[0].hu_list[i].definition_list[k].sequence_list.length!=0){
															for(let m = 0;m<this.arl_tree[0].hu_list[i].definition_list[k].sequence_list.length;m++){
																let Squence_Open_type = this.arl_tree[0].hu_list[i].definition_list[k].sequence_list[m].type
																if(Squence_Open_type== 'DCU'||Squence_Open_type== 'MEU'||Squence_Open_type== 'DCU/MEU'){
																	array_Open_TAGLDEFSequeceList.push(this.arl_tree[0].hu_list[i].definition_list[k].sequence_list[m])
																}
															}
														}
														if(this.arl_tree_copy[0].hu_list[i].definition_list[k].sequence_list.length!=0){
															for(let m = 0;m<this.arl_tree_copy[0].hu_list[i].definition_list[k].sequence_list.length;m++){
																let Squence_Save_type = this.arl_tree_copy[0].hu_list[i].definition_list[k].sequence_list[m].type
																if(Squence_Save_type== 'DCU'||Squence_Save_type== 'MEU'||Squence_Save_type== 'DCU/MEU'){
																	array_Save_TAGLDEFSequeceList.push(this.arl_tree_copy[0].hu_list[i].definition_list[k].sequence_list[m])
																}
															}
														}
														if(JSON.stringify(array_Open_TAGLDEFSequeceList) != JSON.stringify(array_Save_TAGLDEFSequeceList)){
															this.arl_tree[0].hu_list[i].definition_list[k].analysis_list[j].reason = this.arl_tree[0].hu_list[i].definition_list[k].reason
															this.arl_tree[0].hu_list[i].definition_list[k].analysis_list[j].job_status =2
														}
													}	
												}else{
													//TAGL_Def的reason无变化时，向上一层查看数据有无变化
													if(this.arl_tree[0].hu_list[i].definition_list[k].reason == this.arl_tree_copy[0].hu_list[i].definition_list[k].reason){
														//只有HU_def的责任分担(sequence_list)中的DCU('type':'DCU')变化时,责任分担才算变化（新增和删除‘DCU’都算变化）
														let array_Open_HUSequeceList = []
														let array_Save_HUSequeceList = []
														if(this.arl_tree[0].hu_list[i].sequence_list.length!=0){
															for(let m = 0;m<this.arl_tree[0].hu_list[i].sequence_list.length;m++){
																let Squence_Open_type = this.arl_tree[0].hu_list[i].sequence_list[m].type
																if( Squence_Open_type== 'DCU'||Squence_Open_type== 'MEU'||Squence_Open_type== 'DCU/MEU'){
																	array_Open_HUSequeceList.push(this.arl_tree[0].hu_list[i].sequence_list[m])
																}
															}
														}
														
														if(this.arl_tree_copy[0].hu_list[i].sequence_list.length!=0){
															for(let m = 0;m<this.arl_tree_copy[0].hu_list[i].sequence_list.length;m++){
																let Squence_Save_type = this.arl_tree_copy[0].hu_list[i].sequence_list[m].type
																if(Squence_Save_type== 'DCU'||Squence_Save_type== 'MEU'||Squence_Save_type== 'DCU/MEU'){
																	array_Save_HUSequeceList.push(this.arl_tree_copy[0].hu_list[i].sequence_list[m])
																}
															}
														}
														//HU_Def的责任分担和reason都变化时，修改TAGL_Def的reason
														if(this.arl_tree[0].hu_list[i].reason != this.arl_tree_copy[0].hu_list[i].reason && JSON.stringify(array_Open_HUSequeceList) != JSON.stringify(array_Save_HUSequeceList)){
															this.arl_tree[0].hu_list[i].definition_list[k].reason = this.arl_tree[0].hu_list[i].reason
															this.arl_tree[0].hu_list[i].definition_list[k].job_status = 2
														}	
													}
												}
											}else{
												//TAGL_Def的reason无变化时，向上一层查看数据有无变化
													if(this.arl_tree[0].hu_list[i].definition_list[k].reason == this.arl_tree_copy[0].hu_list[i].definition_list[k].reason){
														//只有HU_def的责任分担(sequence_list)中的DCU('type':'DCU')变化时,责任分担才算变化（新增和删除‘DCU’都算变化）
														let array_Open_HUSequeceList = []
														let array_Save_HUSequeceList = []
														if(this.arl_tree[0].hu_list[i].sequence_list.length!=0){
															for(let m = 0;m<this.arl_tree[0].hu_list[i].sequence_list.length;m++){
																let Squence_Open_type = this.arl_tree[0].hu_list[i].sequence_list[m].type
																if( Squence_Open_type== 'DCU'||Squence_Open_type== 'MEU'||Squence_Open_type== 'DCU/MEU'){
																	array_Open_HUSequeceList.push(this.arl_tree[0].hu_list[i].sequence_list[m])
																}
															}
														}
														
														if(this.arl_tree_copy[0].hu_list[i].sequence_list.length!=0){
															for(let m = 0;m<this.arl_tree_copy[0].hu_list[i].sequence_list.length;m++){
																let Squence_Save_type = this.arl_tree_copy[0].hu_list[i].sequence_list[m].type
																if(Squence_Save_type== 'DCU'||Squence_Save_type== 'MEU'||Squence_Save_type== 'DCU/MEU'){
																	array_Save_HUSequeceList.push(this.arl_tree_copy[0].hu_list[i].sequence_list[m])
																}
															}
														}
														//HU_Def的责任分担和reason都变化时，修改TAGL_Def的reason
														if(this.arl_tree[0].hu_list[i].reason != this.arl_tree_copy[0].hu_list[i].reason && JSON.stringify(array_Open_HUSequeceList) != JSON.stringify(array_Save_HUSequeceList)){
															this.arl_tree[0].hu_list[i].definition_list[k].reason = this.arl_tree[0].hu_list[i].reason
															this.arl_tree[0].hu_list[i].definition_list[k].job_status = 2
														}	
													}
											}
										}	
											
									}else{
										//TAGL_Def的reason无变化时，向上一层查看数据有无变化
										if(this.arl_tree[0].hu_list[i].definition_list[k].reason == this.arl_tree_copy[0].hu_list[i].definition_list[k].reason){
											let array_Open_HUSequeceList = []
											let array_Save_HUSequeceList = []
											if(this.arl_tree[0].hu_list[i].sequence_list.length!=0){
												for(let m = 0;m<this.arl_tree[0].hu_list[i].sequence_list.length;m++){
													let Squence_Open_type = this.arl_tree[0].hu_list[i].sequence_list[m].type
													if( Squence_Open_type== 'DCU'||Squence_Open_type== 'MEU'||Squence_Open_type== 'DCU/MEU'){
														array_Open_HUSequeceList.push(this.arl_tree[0].hu_list[i].sequence_list[m])
													}
												}
											}
											
											if(this.arl_tree_copy[0].hu_list[i].sequence_list.length!=0){
												for(let m = 0;m<this.arl_tree_copy[0].hu_list[i].sequence_list.length;m++){
													let Squence_Save_type = this.arl_tree_copy[0].hu_list[i].sequence_list[m].type
													if(Squence_Save_type== 'DCU'||Squence_Save_type== 'MEU'||Squence_Save_type== 'DCU/MEU'){
														array_Save_HUSequeceList.push(this.arl_tree_copy[0].hu_list[i].sequence_list[m])
													}
												}
											}
											//HU_Def的责任分担和reason都变化时，修改TAGL_Def的reason
											if(this.arl_tree[0].hu_list[i].reason != this.arl_tree_copy[0].hu_list[i].reason && JSON.stringify(array_Open_HUSequeceList) != JSON.stringify(array_Save_HUSequeceList)){
												this.arl_tree[0].hu_list[i].definition_list[k].reason = this.arl_tree[0].hu_list[i].reason
												this.arl_tree[0].hu_list[i].definition_list[k].job_status = 2
											}
										}
									}
							}
						}
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
						if(val == 1){
							this.setCheckList();
						}else if(val == 2){
							this.re_check_list_show = true
						}
						
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
		show_more(table_id,index,definition_index,taglana_index) {
			var _this = this;
			if(table_id==1){
				if(_this.arl_more == false){
					$(".arltable").eq(index).animate({width:1450},800, function() {
		            _this.arl_more = true
		   		 });
				}else{
					$(".arltable").eq(index).animate({width:1250},200, function() {
		            _this.arl_more = false;
		   		 });
				} 
			}else if(table_id==2){
				if($(".hu_table").eq(index).children(".table_content_hidden").css("display")=="none"){
					$(".hu_table").eq(index).children(".table_content_hidden").css({"display":"block"})
					$(".hu_table").eq(index).animate({width:2456,},800, function(){});
					$(".hu_table").eq(index).find(".el-icon-d-arrow-right").eq(0).removeClass().addClass("el-icon-d-arrow-left");
				}else{
					$(".hu_table").eq(index).animate({width:1236},200, function() {
		            $(".hu_table").eq(index).children(".table_content_hidden").css({"display":"none"})
		            $(".hu_table").eq(index).find(".el-icon-d-arrow-left").eq(0).removeClass().addClass("el-icon-d-arrow-right");
		   		 });
				}
			}else if(table_id==3){
				if($(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".tagltable").eq(0).children(".table_content_hidden").css("display")=="none"){
					$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".tagltable").eq(0).children(".table_content_hidden").css({"display":"block"})
					$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".tagltable").eq(0).animate({width:2371},800, function() {
		           	$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".tagltable").eq(0).find(".el-icon-d-arrow-right").eq(0).removeClass().addClass("el-icon-d-arrow-left");
		   		 });
				}else{
					$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".tagltable").eq(0).animate({width:1221},200, function() {
		           $(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".tagltable").eq(0).children(".table_content_hidden").css({"display":"none"})
		           $(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".tagltable").eq(0).find(".el-icon-d-arrow-left").eq(0).removeClass().addClass("el-icon-d-arrow-right");
		   		 });
				}
			}else if(table_id==4){
				if($(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".taglana_div").eq(taglana_index).children(".taglana_table").eq(0).children(".table_content_hidden").css("display")=="none"){
					$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".taglana_div").eq(taglana_index).children(".taglana_table").eq(0).children(".table_content_hidden").css({"display":"block"})
					$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".taglana_div").eq(taglana_index).children(".taglana_table").eq(0).animate({width:1816},800, function() {});
					$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".taglana_div").eq(taglana_index).children(".taglana_table").eq(0).find(".el-icon-d-arrow-right").eq(0).removeClass().addClass("el-icon-d-arrow-left");
				}else{
					$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".taglana_div").eq(taglana_index).children(".taglana_table").eq(0).animate({width:1206.3},200, function() {
						$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".taglana_div").eq(taglana_index).children(".taglana_table").eq(0).children(".table_content_hidden").css({"display":"none"})
					});
					$(".hu_div").eq(index).children(".tagl_div").eq(definition_index).children(".taglana_div").eq(taglana_index).children(".taglana_table").eq(0).find(".el-icon-d-arrow-left").eq(0).removeClass().addClass("el-icon-d-arrow-right");	
				}
			}	   
		},
		hu_select_item(ret_arl_index, ret_hu_index, select_item) {

			this.arl_index = ret_arl_index;
            this.hu_index = ret_hu_index;
            this.hu_record = this.arl_tree[this.arl_index].hu_list[this.hu_index];
            this.select_item_name = select_item;
            if(this.arl_tree[0].hu_list[this.hu_index].lock_status == 1){
            	return
            }
    		switch (this.select_item_name) {
    			case this.dialog_hudef_reason :
    			    this.hu_reason_show = true;
    			    break;
    			case this.dialog_hudef_worker :
    				let lock_status_kids_flag = true
//  				for(let i=0;i<this.hu_record.definition_list.length;i++){
//  					if(this.hu_record.definition_list[i].lock_status == 1 ){
//  						lock_status_kids_flag = lock_status_kids_flag && false
//  						break
//  					}
//  				}
					if(this.hu_record.lock_status == 2){
						lock_status_kids_flag = lock_status_kids_flag && false
					}
    				if(lock_status_kids_flag){
    					this.hu_work_show = true;	
    				}
    			   	
    			    break;
    			case this.dialog_hudef_option :
    			    this.hu_option_show = true;
    			    break;
    			case this.dialog_hudef_evidence :
    			    this.hu_funcconfig_show = true;
    			    break;
    			case this.dialog_hudef_others :
    			    this.hu_others_show = true;
    			    break; 
    			case this.dialog_hudef_remark :
    			    this.hu_remark_show = true;
    			    break;
    			case this.dialog_hudef_relbasicreq :
    			    this.hu_relrequirement_show = true;
    			    break; 
    			case this.dialog_hudef_basicreq :
    			    this.hu_basicreq_show = true;
    			    break;
    			case this.dialog_hudef_point :
    				if(this.hu_record.point_list.length == 0){
    					return
    				}
    			    this.hu_point_show = true;
    			    break;
    			default :
    			    break;
    			};  
		},
        hu_dialog_return (params) {
        	if (params[0]) {
        		let data_first = JSON.parse(JSON.stringify(this.arl_tree[this.arl_index].hu_list[this.hu_index]))
        		delete data_first.definition_list
        		let data_last = JSON.parse(JSON.stringify(params[1]))
        		delete data_first.definition_list
        		if(JSON.stringify(data_first) != JSON.stringify(data_last)){
        			if(this.Roles =="Member"||this.Roles =="Leader"){
						params[1].job_status = 2 
					}
        			this.Array_Check_List[0] = 'hu'
        		}
        		var ret_hu_record = params[1];
        		this.arl_tree[this.arl_index].hu_list[this.hu_index] = ret_hu_record;
        	}

            switch (this.select_item_name) {
	            case this.dialog_hudef_reason :
	                this.hu_reason_show = false;
	                break;	
	            case this.dialog_hudef_worker :
	                this.hu_work_show = false;
	                break;
	            case this.dialog_hudef_option :
	                this.hu_option_show = false;
	                break;                
	            case this.dialog_hudef_evidence :
	                this.hu_funcconfig_show = false;    
	                break;
	            case this.dialog_hudef_others :
	                this.hu_others_show = false;    
	                break;
	            case this.dialog_hudef_remark :
	                this.hu_remark_show = false;    
	                break;
	            case this.dialog_hudef_relbasicreq :
	                this.hu_relrequirement_show = false; 
	                break;
	            case this.dialog_hudef_basicreq :
	                this.hu_basicreq_show = false;
	                break;
	            case this.dialog_hudef_point :
	                this.hu_point_show = false; 
	                break; 
	            default :
	                break;
            };
        },
        tagl_select_item(ret_arl_index, ret_hu_index, ret_tagl_index, select_item){
			this.arl_index = ret_arl_index;
            this.hu_index = ret_hu_index;
            this.tagl_index = ret_tagl_index;
            this.tagl_record = this.arl_tree[this.arl_index].hu_list[this.hu_index].definition_list[this.tagl_index];
            this.select_item_name = select_item;
            if(this.arl_tree[0].hu_list[this.hu_index].definition_list[this.tagl_index].lock_status == 1){
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
		            case this.dialog_tagldef_notice :
		                this.tagl_def_notice_show = true;
		                break;
			  	    case this.dialog_tagldef_worker :
			  	    	let lock_status_kids_flag = true
//	    				for(let i=0;i<this.tagl_record.analysis_list.length;i++){
//	    					if(this.tagl_record.analysis_list[i].lock_status == 1 || this.tagl_record.analysis_list[i].lock_status == 2){
//	    						lock_status_kids_flag = lock_status_kids_flag && false
//	    						break
//	    					}
//	    				}
						if(this.tagl_record.lock_status == 2){
							lock_status_kids_flag = lock_status_kids_flag && false
						}
	    				if(lock_status_kids_flag){
	    					this.tagl_def_worker_show = true;	
	    				}
		                
		                break;
		            case this.dialog_tagldef_relbasicreq :
		                this.tagl_def_relbasicreq_show = true;
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
        		let data_first = JSON.parse(JSON.stringify(this.arl_tree[this.arl_index].hu_list[this.hu_index].definition_list[this.tagl_index]))
        		delete data_first.analysis_list
        		let data_last = JSON.parse(JSON.stringify(params[1]))
        		delete data_first.analysis_list
        		if(JSON.stringify(data_first) != JSON.stringify(data_last)){
        			if(this.Roles =="Member"||this.Roles =="Leader"){
						params[1].job_status = 2
					}
        			this.Array_Check_List[1] = 'definition'
        		}
        		var ret_tagl_record = params[1];
        		this.arl_tree[this.arl_index].hu_list[this.hu_index].definition_list[this.tagl_index] = ret_tagl_record;
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
        taglana_select_item(ret_arl_index, ret_hu_index, ret_tagl_index, select_item,taglana_index){
			this.arl_index = ret_arl_index;
            this.hu_index = ret_hu_index;
            this.tagl_index = ret_tagl_index;
            this.taglana_index = taglana_index
            this.tagl_record = this.arl_tree[this.arl_index].hu_list[this.hu_index].definition_list[this.tagl_index].analysis_list[this.taglana_index];
            this.select_item_name = select_item;
           
            if(this.arl_tree[0].hu_list[this.hu_index].definition_list[this.tagl_index].analysis_list[this.taglana_index].lock_status == 1){
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
        		let data_first = JSON.parse(JSON.stringify(this.arl_tree[this.arl_index].hu_list[this.hu_index].definition_list[this.tagl_index].analysis_list[this.taglana_index]))
        		let data_last = JSON.parse(JSON.stringify(params[1]))
        		if(JSON.stringify(data_first) != JSON.stringify(data_last)){
        			if(this.Roles =="Member"||this.Roles =="Leader"){
						params[1].job_status = 2 
					}
        			this.Array_Check_List[2] = 'analysis'
        		}
        		var ret_taglana_record = params[1];
        		this.arl_tree[this.arl_index].hu_list[this.hu_index].definition_list[this.tagl_index].analysis_list[this.taglana_index] = ret_taglana_record;
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
        // arl_new() {
        // 	var arl_record_new = {	"action": "", "arl_id": "0", "arl_record_id": 0, "arl_user": "", "author": "", "category": "", "center_spec": null, 
							 //        "charge": null, "company_rule": null, "dealer": null, "detail": "0", "developer": null, "exception": null, 
							 //        "func_chapter": "", "func_file_name": "", "func_page": "-", "func_spec_no": null, "func_summary_en": null, 
							 //        "func_summary_jp": "", "func_version": "", "future_req": "", "group_id": 0, "hmi_chapter": null, "hmi_file_name": null, 
							 //        "hmi_page": null, "hmi_spec_no": null, "hmi_version": null, "hu_list": [], "id1": "0", "id2": "0", "id3": "0", "if_spec": "0", 
							 //        "law": null, "level1": "", "level2": "", "level3,id4": null, "level4": "", "major_category": "", "major_ver": "", 
							 //        "md5_key": null, "medium_catetory": "", "mm_item": null, "mm_new_num": "", "old_bug": null, "other_spec": null, 
							 //        "policy": null, "remark": "", "req_omission": "", "req_post": "", "same_req": null, "small_category": "", 
							 //        "small_ver": null, "status": null, "subid": null, "supplier": "", "supply": null, "sys_conf_id": null, 
							 //        "tagl_exclude": null, "trigger": "", "user_id": null };
        //     this.arl_tree.push(arl_record_new);
        // },
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
        definition_new(hu_index) {
        	if(this.Roles=="Translator"){
				this.$notify({
					type:'error',
					message:'您的权限不足，无法保存',
					showClose:true,
					duration:'0',
				})
        	}else{
        		if(this.Roles=="Admin"||this.Roles=="PL"){
        			var definition_record_new = {   "lock_status" : 0,"agree_flag": null, "analysis": "x", "analysis_list": [], "author_name": "SUNTEC", "complete_flag": 0, 
				                                "dcu_meu": "DCU/MEU", "definition_id": "", "exception": null, "has_problem": null, "hu_def_id": "", "point_list":[],
				                                "implementation": "o", "lock_status": 0,"major_ver": null, "md5_key": "", "new_date":"", "notice": null, "other_spec": "-", 
				                                "reason": "\u65b0\u898f\u8ffd\u52a0", "rel_flow_diagram": "-", "rel_hal_design": "-","rel_requirement": null,"basic_req": null, "remark": null, "sequence_list": [], 
				                                "small_ver": null, "title": "", "translation_flag": null, "unique_id": 0, "unrequire": "-","def_option":[{value:1,label:'初始狀態，待作業',disabled:false,},{value:2,label:'作業完了，待确认',disabled:false,},{value:3,label:'确认完了',disabled:false},],"job_status":1,};
				
        		}else{
        			var definition_record_new = {   "lock_status" : 0,"agree_flag": null, "analysis": "x", "analysis_list": [], "author_name": "SUNTEC", "complete_flag": 0, 
				                                "dcu_meu": "DCU/MEU", "definition_id": "", "exception": null, "has_problem": null, "hu_def_id": "", "point_list":[],
				                                "implementation": "o", "lock_status": 0,"major_ver": null, "md5_key": "", "new_date":"", "notice": null, "other_spec": "-", 
				                                "reason": "\u65b0\u898f\u8ffd\u52a0", "rel_flow_diagram": "-", "rel_hal_design": "-","rel_requirement": null,"basic_req": null, "remark": null, "sequence_list": [], 
				                                "small_ver": null, "title": "", "translation_flag": null, "unique_id": 0, "unrequire": "-","def_option":[{value:1,label:'初始狀態，待作業',disabled:false,},{value:2,label:'作業完了，待确认',disabled:false,},{value:3,label:'确认完了',disabled:true},],"job_status":1,};
				
        		}
	        	
				var time = new Date();
				definition_record_new["new_date"] =  this.formatDate(time);
				
				definition_record_new["title"] = "TAGL要件定義: "+this.arl_tree[this.arl_index].hu_list[hu_index].hu_id+'.'+this.arl_tree[0].hu_list[hu_index].definition_list.length
				definition_record_new["definition_id"] = this.arl_tree[this.arl_index].hu_list[hu_index].hu_id+'.'+this.arl_tree[0].hu_list[hu_index].definition_list.length
	            this.arl_tree[this.arl_index].hu_list[hu_index].definition_list.push(definition_record_new);
				this.$notify({
					type:'success',
					message:'新增成功'
				})
	        }
        },
        definition_copy(hu_index,definition_index){
        	var definition_copy = JSON.parse(JSON.stringify(this.arl_tree[this.arl_index].hu_list[hu_index].definition_list[definition_index]))
        	definition_copy["title"] = "TAGL要件定義: "+this.arl_tree[this.arl_index].hu_list[hu_index].hu_id+'.'+this.arl_tree[0].hu_list[hu_index].definition_list.length
       	 	definition_copy["definition_id"] = this.arl_tree[this.arl_index].hu_list[hu_index].hu_id+'.'+this.arl_tree[0].hu_list[hu_index].definition_list.length
       	 	definition_copy.analysis_list = []
       	 	definition_copy.lock_status = 0
        	this.arl_tree[this.arl_index].hu_list[hu_index].definition_list.push(definition_copy);
			this.$notify({
				type:'success',
				message:'复制成功'
			})

        },
        definition_delete(del_hu_index, del_definition_index) {		
        	if(this.Roles=="Admin"||this.Roles=="PL"||this.Roles=="Leader"){
				if(this.arl_tree[0].hu_list[del_hu_index].definition_list[del_definition_index].lock_status == 1 || this.arl_tree[0].hu_list[del_hu_index].definition_list[del_definition_index].lock_status == 2){
	            	return;
	          	}	
	        	this.$confirm('此操作将永久删除数据，是否继续?','提示',{
	        		confirmButtonText:"确定",
	        		cancelButtonText:"取消",
	        		type:'warning'
	        	}).then(()=>{
	        		if(this.arl_tree[this.arl_index].hu_list[del_hu_index].definition_list[del_definition_index].analysis_list!=""){
	        			this.$alert("该条 TAGL要件定義 下含有 TAGL要件分析，不可删除")
	        		}else{
						var definition_tmp = [];
			        	var definition_num = this.arl_tree[this.arl_index].hu_list[del_hu_index].definition_list.length;
			        	if (del_definition_index + 1 > definition_num) {
			                return;
			        	};
	
			    		for (var i = definition_num - 1; i > del_definition_index; i-- ) {
			                 definition_tmp.push(this.arl_tree[this.arl_index].hu_list[del_hu_index].definition_list.pop());
			    		};
			    		this.arl_tree[this.arl_index].hu_list[del_hu_index].definition_list.pop();
			    		for (var j = (definition_tmp.length - 1); j >= 0  ; j--) {
			                this.arl_tree[this.arl_index].hu_list[del_hu_index].definition_list.push(definition_tmp.pop());
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
        taglana_new(hu_index,definition_index){
        	if(this.Roles=="Translator"){
				this.$notify({
					type:'error',
					message:'您的权限不足，无法保存',
					showClose:true,
					duration:'0',
				})
        	}else{
        		if(this.Roles=="Admin"||this.Roles=="PL"){
        			var taglana_record_new = { "lock_status" : 0,"agree_flag": null ,"analysis_rc_id": null ,"author_name": "SUNTEC" ,"complete_flag": 0 ,"create_time": "" ,"definition_id":"" ,
	        								"exception": null ,"has_problem": null ,"job_status": null , "md5_key": null ,"new_date": "","reason": "\u65b0\u898f\u8ffd\u52a0" ,"remark":null,"point_list":[],
	        								"seq_diagram": "" ,"sequence_list": [] ,"small_ver": "" ,"rel_requirement": null,"basic_req": null,"supple_spec": "" ,"title": "" ,"translation_flag": null ,"uncheck": null ,
	        								"unique_id": 0,"user_id": null, "asta_filename" : "","ana_option":[{value:1,label:'初始狀態，待作業',disabled:false,},{value:2,label:'作業完了，待确认',disabled:false,},{value:3,label:'确认完了',disabled:false},],"job_status":2,
	        		}
        		}else{
        			var taglana_record_new = { "lock_status" : 0,"agree_flag": null ,"analysis_rc_id": null ,"author_name": "SUNTEC" ,"complete_flag": 0 ,"create_time": "" ,"definition_id":"" ,
	        								"exception": null ,"has_problem": null ,"job_status": null , "md5_key": null ,"new_date": "","reason": "\u65b0\u898f\u8ffd\u52a0" ,"remark":null,"point_list":[],
	        								"seq_diagram": "" ,"sequence_list": [] ,"small_ver": "" ,"rel_requirement": null,"basic_req": null,"supple_spec": "" ,"title": "" ,"translation_flag": null ,"uncheck": null ,
	        								"unique_id": 0,"user_id": null, "asta_filename" : "","ana_option":[{value:1,label:'初始狀態，待作業',disabled:false,},{value:2,label:'作業完了，待确认',disabled:false,},{value:3,label:'确认完了',disabled:true},],"job_status":2,
	        		}
        	}

				var time = new Date();
				taglana_record_new["new_date"] =  this.formatDate(time);
				
				taglana_record_new["title"] = "TAGL要件分析: " +this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].definition_id+'.'+this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].analysis_list.length
//
	        	taglana_record_new["definition_id"] = this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].definition_id+'.'+this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].analysis_list.length
				
//	        	taglana_record_new["title"] = "TAGL要件分析: " +this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].definition_id

//	        	taglana_record_new["definition_id"] = this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].definition_id
//	      		if(this.arl_tree[this.arl_index].hu_list[hu_index].definition_list[definition_index].analysis_list<1){
	      			this.arl_tree[this.arl_index].hu_list[hu_index].definition_list[definition_index].analysis_list.push(taglana_record_new)
	      			this.$notify({
						type:'success',
						message:'新增成功'
					})
//	      		}else{
//	      			this.$alert('TAGL要件分析只允许添加一条')
//	      		}
	      	}
        },
        taglana_delete(hu_index,definition_index,taglana_index){
        	if(this.Roles=="Admin"||this.Roles=="PL"||this.Roles=="Leader"){
				if(this.arl_tree[0].hu_list[hu_index].definition_list[definition_index].analysis_list[taglana_index].lock_status == 1){
	            	return
	            }
	        	this.$confirm('此操作将永久删除数据，是否继续?','提示',{
	        		confirmButtonText:"确定",
	        		cancelButtonText:"取消",
	        		type:'warning'
	        	}).then(()=>{
					this.arl_tree[this.arl_index].hu_list[hu_index].definition_list[definition_index].analysis_list.splice(taglana_index,1)
					this.get_save_array()
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
			this.dialog_save_data = JSON.stringify(this.arl_tree[0])
			var this_ = this;

			if(this.dialog_save_data == this.dialog_open_data){
				$(".dialog_html").animate({height:0},500,function(){
					this_ .show = false;
					$(".arltable").css({display:"none"})
					$(".hu_table").css({display:"none"})
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
						$(".arltable").css({display:"none"})
						$(".hu_table").css({display:"none"})
						$(".tagltable").css({display:"none"})
						$(".taglana_table").css({display:"none"})
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
		user_group(){
			this.arl_tree[0].group_id = this.user_group_value[0]
			this.arl_tree[0].user_id = this.user_group_value[1]
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
