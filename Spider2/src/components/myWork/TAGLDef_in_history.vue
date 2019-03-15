<template>
	<div class="fl loghtml">
		<!-- title -->
		<div class="logbody fl">
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						H/U要件定義ID
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						要件定義ID
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						担当
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 553px">
						ユニークID
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 553px">
						版本号
					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 553px">
						小版本号
					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:199px;">
				<div class="logtitle fl">
					<span class="logspan" style="lineHeight:199px;width:135px">
						TAGL-PF
					</span>
				</div>
				<div class="logtitle fl">
					<span class="dcu_status">
						状態
					</span>
					<span class="dcu_action">
						動作
					</span>
					<span class="duc_trigger" style="border:0 none;lineHeight:60px">
						トリガー
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						関連基本要件
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						基本要件
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 553px">
						除外
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 553px">
						DCU/MEUどちらの想定か
					</span>
				</div>
			</div>
			<div class=" fl model" v-if="MM_list">
				<div class="logtitle fl model" id="model">
					<span class="logspan " style="width:136px;padding:5px;font-size:14px;height: 100%;line-height: 9">
						責務分担
					</span>
				</div>
				<div class="logmsg fl">
					<span style="width: 415px;line-height: 65px;" class="modellist_o" v-for="item in logtabletwo.model_list">
						{{item.name}}
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						变更理由
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						備考
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						責務分担の特記事項
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						日付
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 553px">
						创建时间
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 553px">
						更新时间
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:200px;">
				<div class="logtitle fl">
					<span class="logspan" style="lineHeight:200px;width:135px">
						参考文献
					</span>
				</div>
				<div class="logtitle fl">
					<span class="dcu_status">
						参考ウォークスルー図
					</span>
					<span class="dcu_action">
						参考HAL設計書
					</span>
					<span class="duc_trigger" style="border:0 none;lineHeight:60px">
						その他仕様（リファハード仕様等）
					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						リファレンスハード上での実現可否
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						詳細分析可否
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						未要件分析
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						翻译
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						承认
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						指摘
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" v-if="lock_flag">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						锁定状态
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 553px">
						作业状态
					</span>
				</div>
			</div>
			<!--<div class="logcontent fl" style="height:35px;">-->
			<!--<div class="logtitle fl">-->
			<!--<span class="unique_id" style="lineHeight:26px;width: 552px;">-->
			<!--完成-->
			<!--</span>-->
			<!--</div>-->
			<!--</div>-->
		</div>
		<!-- tableA -->
		<div class="logbody fl" id="tableA" style="width: 245px">
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.hu_def_id.old_val" v-html="logtabletwo.hu_def_id.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.definition_id.old_val" v-html="logtabletwo.definition_id.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.author_name.old_val" v-html="logtabletwo.author_name.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.unique_id.old_val" v-html="logtabletwo.unique_id.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.major_ver.old_val" v-html="logtabletwo.major_ver.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.small_ver.old_val" v-html="logtabletwo.small_ver.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:200px;">
				<div class="logmsg fl">
					<span class="dcu_status_o" :title="logtabletwo.pf_status.old_val" v-html="logtabletwo.pf_status.old_val">

					</span>
					<span class="dcu_action_o" :title="logtabletwo.pf_action.old_val" v-html="logtabletwo.pf_action.old_val">

					</span>
					<span class="duc_trigger_o" style="border:0 none;" :title="logtabletwo.pf_trigger.old_val" v-html="logtabletwo.pf_trigger.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.rel_requirement.old_val" v-html="logtabletwo.rel_requirement.old_val">
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.basic_req.old_val" v-html="logtabletwo.basic_req.old_val">
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.exception.old_val" v-html="logtabletwo.exception.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.dcu_meu.old_val" v-html="logtabletwo.dcu_meu.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl model" v-if="MM_list">
				<div class="logmsg fl">
					<span class="modellist_o" v-for="item in logtabletwo.model_list" :title="item.old_val" v-html="item.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">

				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.reason.old_val" v-html="logtabletwo.reason.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.remark.old_val" v-html="logtabletwo.remark.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.notice.old_val" v-html="logtabletwo.notice.old_val">

				</div>
			</div>

			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.new_date.old_val" v-html="logtabletwo.new_date.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.create_time.old_val" v-html="logtabletwo.create_time.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.update_time.old_val" v-html="logtabletwo.update_time.old_val">

					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.rel_flow_diagram.old_val" v-html="logtabletwo.rel_flow_diagram.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.rel_hal_design.old_val" v-html="logtabletwo.rel_hal_design.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:64px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.other_spec.old_val" v-html="logtabletwo.other_spec.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.implementation.old_val" v-html="logtabletwo.implementation.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.analysis.old_val" v-html="logtabletwo.analysis.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.unrequire.old_val" v-html="logtabletwo.unrequire.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.translation_flag.old_val" v-html="logtabletwo.translation_flag.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.agree_flag.old_val" v-html="logtabletwo.agree_flag.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.has_problem.old_val" v-html="logtabletwo.has_problem.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" v-if="lock_flag">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.lock_status.old_val" v-html="logtabletwo.lock_status.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.job_status.old_val" v-html="logtabletwo.job_status.old_val">

					</span>
				</div>
			</div>
			<!--<div class="logcontent fl" style="height:35px;">-->
			<!--<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;"-->
			<!--:title="logtabletwo.complete_flag.old_val"-->
			<!--v-html="logtabletwo.complete_flag.old_val">-->

			<!--</div>-->
			<!--</div>-->
		</div>
		<!-- tableB -->
		<div class="logbody fl" id="tableB" style="width: 245px">
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.hu_def_id.val" :class="{red_active:logtabletwo.hu_def_id.changed=='change',blue_active:logtabletwo.hu_def_id.changed=='add',}" v-html="logtabletwo.hu_def_id.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.definition_id.val" :class="{red_active:logtabletwo.definition_id.changed=='change',blue_active:logtabletwo.definition_id.changed=='add',}" v-html="logtabletwo.definition_id.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.author_name.val" :class="{red_active:logtabletwo.author_name.changed=='change',blue_active:logtabletwo.author_name.changed=='add',}" v-html="logtabletwo.author_name.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.unique_id.val" :class="{red_active:logtabletwo.unique_id.changed=='change',blue_active:logtabletwo.unique_id.changed=='add',}" v-html="logtabletwo.unique_id.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.major_ver.val" :class="{red_active:logtabletwo.major_ver.changed=='change',blue_active:logtabletwo.major_ver.changed=='add',}" v-html="logtabletwo.major_ver.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.small_ver.val" :class="{red_active:logtabletwo.small_ver.changed=='change',blue_active:logtabletwo.small_ver.changed=='add',}" v-html="logtabletwo.small_ver.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:200px;">
				<div class="logmsg fl ">
					<span class="dcu_status_o" :title="logtabletwo.pf_status.val" :class="{red_active:logtabletwo.pf_status.changed=='change',blue_active:logtabletwo.pf_status.changed=='add',}" v-html="logtabletwo.pf_status.val">

					</span>
					<span class="dcu_action_o" :title="logtabletwo.pf_action.val" :class="{red_active:logtabletwo.pf_action.changed=='change',blue_active:logtabletwo.pf_action.changed=='add',}" v-html="logtabletwo.pf_action.val">

					</span>
					<span class="duc_trigger_o" style="border:0 none;" :title="logtabletwo.pf_trigger.val" :class="{red_active:logtabletwo.pf_trigger.changed=='change',blue_active:logtabletwo.pf_trigger.changed=='add',}" v-html="logtabletwo.pf_trigger.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl mg" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.rel_requirement.val" :class="{red_active:logtabletwo.rel_requirement.changed=='change',blue_active:logtabletwo.rel_requirement.changed=='add',}" v-html="logtabletwo.rel_requirement.val">
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl mg" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.basic_req.val" :class="{red_active:logtabletwo.basic_req.changed=='change',blue_active:logtabletwo.basic_req.changed=='add',}" v-html="logtabletwo.basic_req.val">
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.exception.val" :class="{red_active:logtabletwo.exception.changed=='change',blue_active:logtabletwo.exception.changed=='add',}" v-html="logtabletwo.exception.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.dcu_meu.val" :class="{red_active:logtabletwo.dcu_meu.changed=='change',blue_active:logtabletwo.dcu_meu.changed=='add',}" v-html="logtabletwo.dcu_meu.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl model" v-if="MM_list">
				<div class="logmsg fl">
					<span class="modellist_o" v-for="item in logtabletwo.model_list" :title="item.val" :class="{red_active:item.changed=='change',blue_active:item.changed=='add',}" v-html="item.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">

				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.reason.val" :class="{red_active:logtabletwo.reason.changed=='change',blue_active:logtabletwo.reason.changed=='add',}" v-html="logtabletwo.reason.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.remark.val" :class="{red_active:logtabletwo.remark.changed=='change',blue_active:logtabletwo.remark.changed=='add',}" v-html="logtabletwo.remark.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.notice.val" :class="{red_active:logtabletwo.notice.changed=='change',blue_active:logtabletwo.notice.changed=='add',}" v-html="logtabletwo.notice.val">

				</div>
			</div>

			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.new_date.val" :class="{red_active:logtabletwo.new_date.changed=='change',blue_active:logtabletwo.new_date.changed=='add',}" v-html="logtabletwo.new_date.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.create_time.val" :class="{red_active:logtabletwo.create_time.changed=='change',blue_active:logtabletwo.create_time.changed=='add',}" v-html="logtabletwo.create_time.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.update_time.val" :class="{red_active:logtabletwo.update_time.changed=='change',blue_active:logtabletwo.update_time.changed=='add',}" v-html="logtabletwo.update_time.val">

					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.rel_flow_diagram.val" :class="{red_active:logtabletwo.rel_flow_diagram.changed=='change',blue_active:logtabletwo.rel_flow_diagram.changed=='add',}" v-html="logtabletwo.rel_flow_diagram.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.rel_hal_design.val" :class="{red_active:logtabletwo.rel_hal_design.changed=='change',blue_active:logtabletwo.rel_hal_design.changed=='add',}" v-html="logtabletwo.rel_hal_design.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:64px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.other_spec.val" :class="{red_active:logtabletwo.other_spec.changed=='change',blue_active:logtabletwo.other_spec.changed=='add',}" v-html="logtabletwo.other_spec.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.implementation.val" :class="{red_active:logtabletwo.implementation.changed=='change',blue_active:logtabletwo.implementation.changed=='add',}" v-html="logtabletwo.implementation.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.analysis.val" :class="{red_active:logtabletwo.analysis.changed=='change',blue_active:logtabletwo.analysis.changed=='add',}" v-html="logtabletwo.analysis.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.unrequire.val" :class="{red_active:logtabletwo.unrequire.changed=='change',blue_active:logtabletwo.unrequire.changed=='add',}" v-html="logtabletwo.unrequire.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.translation_flag.val" :class="{red_active:logtabletwo.translation_flag.changed=='change',blue_active:logtabletwo.translation_flag.changed=='add',}" v-html="logtabletwo.translation_flag.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.agree_flag.val" :class="{red_active:logtabletwo.agree_flag.changed=='change',blue_active:logtabletwo.agree_flag.changed=='add',}" v-html="logtabletwo.agree_flag.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.has_problem.val" :class="{red_active:logtabletwo.has_problem.changed=='change',blue_active:logtabletwo.has_problem.changed=='add',}" v-html="logtabletwo.has_problem.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" v-if="lock_flag">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;" :title="logtabletwo.lock_status.val" :class="{red_active:logtabletwo.lock_status.changed=='change',blue_active:logtabletwo.lock_status.changed=='add',}" v-html="logtabletwo.lock_status.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.job_status.val" :class="{red_active:logtabletwo.job_status.changed=='change',blue_active:logtabletwo.job_status.changed=='add',}" v-html="logtabletwo.job_status.val">

					</span>
				</div>
			</div>
			<!--<div class="logcontent fl" style="height:35px;">-->
			<!--<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;"-->
			<!--:title="logtabletwo.complete_flag.val"-->
			<!--:class="{red_active:logtabletwo.complete_flag.changed=='change',blue_active:logtabletwo.complete_flag.changed=='add',}"-->
			<!--v-html="logtabletwo.complete_flag.val">-->

			<!--</div>-->
			<!--</div>-->
		</div>
	</div>
</template>
<script>
	require('../../assets/js/jquery-1.8.3.min.js')
	export default {
		props: ["commit_id", "commit_m_id", "Boolean_Examine_Flag"],
		watch: {
			Boolean_Examine_Flag(val) {
				this.examine(val);
			}
		},
		data() {
			return {
				// test
				duc_trigger_red_flag: true,
				duc_trigger_blue_flag: false,

				sumbit_type: '',
				work_status: 4,
				//
				pp: '',
				MM_list: false,
				lock_flag: false,

				ct_id: this.commit_id,
				ct_m_id: this.commit_m_id,
				logtabletwo: {},
				end_id: 4430,
				start_id: 4430,
				// end_id:end_log_ref_id,
				// start_id:start_log_ref_id
			}
		},
		mounted() {
			this.getHistory();
		},
		methods: {
			getHistory() {
				this.$axios.get(this.Ip + "/DetailLog" + "/" + this.ct_id + "/" + this.ct_m_id)
					.then(res => {
						if(res.data.result == "OK") {
							this.sumbit_type = res.data
							this.logtabletwo = res.data.content;
							this.end_id = res.data.end_log_ref_id;
							this.start_id = res.data.start_log_ref_id;
							if(res.data.content.model_list.length == 0) {
								this.MM_list = false;
							} else {
								this.MM_list = true;
								$(".model").height(this.logtabletwo.model_list.length * 67)
							};
							if(res.data.content.lock_status == null) {
								this.lock_flag = false;
							} else {
								this.lock_flag = true;
							};
							this.getWorkStatus();
						} else {
							this.logtabletwo = [];
							this.$alert("没数据o(╥﹏╥)o")
						}
					})
			},
			getWorkStatus() {
				this.$axios.get(this.Ip + "/LookStatus/" + this.logtabletwo.definition_id.val + '/' + this.sumbit_type.classify)
					.then(res => {
						this.work_status = res.data.content.job_status
						this.$emit('get_Boolean_Examine', this.work_status)
					})
			},
			examine(val) {
				if(this.work_status != 2) {
					return
				}
				this.$axios.get(this.Ip + '/ReQueryStatus/' + this.logtabletwo.definition_id.val + '/' + this.sumbit_type.classify + '/' + val)
					.then(res => {
						this.getWorkStatus();
					})
					.catch()
			},
			seelog() {
				this.$axios.get(this.Ip + "/DetailLog" + "/" + this.ct_id + "/" + this.ct_m_id)
					.then(res => {
						if(res.data.result == "OK") {
							this.logtabletwo = res.data.content;
							this.end_id = res.data.end_log_ref_id;
							this.start_id = res.data.start_log_ref_id;
							if(res.data.content.model_list.length == 0) {
								this.MM_list = false;
							} else {
								this.MM_list = true;
							};
						} else {
							// this.logtabletwo =[];
							this.$alert("没数据o(╥﹏╥)o")
						}

					})
			},

			// check_rule(item){
			// 	if(this.test_opt_1.type =1){
			// 		if(this.test_opt_1.old_val=''&&this.test_opt_1.val!=''){

			// 		}else if(this.test_opt_1.old_val!=''&&this.test_opt_1.val!=''){

			// 		}else if(this.test_opt_1.old_val!=''&&this.test_opt_1.val=''){

			// 		}
			// 	}
			// },

		}
	}
</script>
<style scoped>
	* {
		margin: 0;
		padding: 0;
		font-size: 14px;
	}
	
	.fr {
		float: right;
	}
	
	.fl {
		float: left;
	}
	
	.title {
		width: 98%;
		margin: 0 auto;
		height: 35px;
		line-height: 35px;
	}
	
	.loghtml {
		width: 100%;
		min-width: 700px;
		height: 90%;
		/*border: 1px solid green;*/
		overflow-x: hidden;
		overflow-y: auto;
	}
	
	.logbody {
		width: 554px;
		height: 875px;
	}
	
	.logcontent {
		width: 100%;
		height: 200px;
	}
	
	.logtitle {
		height: 100%;
		border: solid 1px #dfe6ec;
		/*line-height: 200px;*/
	}
	
	.logtitle>span {
		display: block;
		*display: block;
		*zoom: 1;
		font-size: 15px;
	}
	
	.logmsg {
		height: 100%;
		border: solid 1px #dfe6ec;
		text-align: center;
	}
	
	.logmsg>span {
		display: block;
		*display: block;
		*zoom: 1;
		font-size: 12px;
	}
	
	.logspan {
		padding: 0 15px 0 15px;
		font-size: 16px;
		text-align: center;
		border: none;
	}
	
	.solid {
		width: 2px;
		height: 875px;
		background: red;
		border: 1px solid #ccc;
		position: fixed;
		left: 50%;
		top: 78px;
	}
	
	.optionlog {
		height: 28px;
		line-height: 28px;
		padding: 0 15px 0 15px;
		border-bottom: 1px solid #dfe6ec
	}
	
	.opt {
		width: 415px;
		height: 28px;
		line-height: 28px;
		padding: 0 15px 0 15px;
		border-bottom: 1px solid #dfe6ec
	}
	/**/
	
	.olog {
		width: 245px;
		height: 28px;
		line-height: 28px;
		overflow-y: auto;
		padding: 0 15px 0 15px;
		border-bottom: 1px solid #dfe6ec
	}
	/**/
	
	.rel,
	.remark {
		width: 96%;
		margin: 2%;
		font-size: 14px;
	}
	
	.dcu_meu {
		line-height: 400px;
		padding: 0 6px;
	}
	
	.dcu,
	.meu {
		padding: 0 41px;
		line-height: 200px;
	}
	
	.dcu {
		border-bottom: 1px solid #dfe6ec;
	}
	
	.dcu_status,
	.dcu_action,
	.duc_trigger {
		padding: 0 25px;
		border-bottom: 1px solid #dfe6ec;
		line-height: 66px;
		text-align: center;
		width: 415px;
	}
	/**/
	
	.dcu_status_o,
	.dcu_action_o,
	.duc_trigger_o {
		border-bottom: 1px solid #dfe6ec;
		height: 67px;
		text-align: center;
		width: 245px;
		overflow-y: auto;
	}
	/**/
	
	.unique_id {
		width: 135px;
		/*padding: 0 35px;*/
		text-align: center;
	}
	
	.modellist {
		height: 67px;
		line-height: 67px;
		border: 1px solid #dfe6ec;
		text-align: center;
	}
	/**/
	
	.modellist_o {
		width: 245px;
		height: 67px;
		border: 1px solid #dfe6ec;
		overflow-y: auto;
		border-right: none;
		border-left: none;
	}
	/**/
	
	.blue_active {
		color: blue;
	}
	
	.red_active {
		color: red;
	}
	
	.model {
		height: auto;
		border-left: 1px solid #dfe6ec;
	}
	
	#model {
		border: none;
	}
	
	#tableA span {
		text-align: left;
		overflow-y: auto;
		width: 245px;
	}
	
	#tableB span {
		text-align: left;
		overflow-y: auto;
		width: 245px;
	}
</style>