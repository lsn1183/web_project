<template>
	<div class="fl loghtml">
		<!-- title -->
		<div class="logbody fl" id="title">
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						TAGL要件定義ID
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						ユニークID
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
						除外
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						シーケンス図
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="rel_basic_flag">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						関連基本要件
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="rel_basic_flag">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						基本要件
					</span>
				</div>
			</div>
			<div class=" fl model" v-if="MM_list" style="width:554px;">
				<div class="logtitle fl" id="model">
					<span class="logspan " style="width:136px;padding:0;font-size:14px;height: 100%;">
						責務分担
					</span>
				</div>
				<div class="fl" style="width: 415px;">
					<div class="logmsg fl" v-if="MM_list_first">
						<span style="width: 415px;height: 67px;" class="modellist" v-for="item in first_model">
							{{item.name}}
						</span>
					</div>
					<div class="logmsg fl" v-if="MM_list_scend">
						<span style="width: 415px;height: 67px;" class="modellist" v-for="item in scend_model">
							{{item.name}}
						</span>
					</div>
					<div class="logmsg fl" v-if="MM_list_third">
						<span style="width: 415px;height: 67px;" class="modellist" v-for="item in third_model">
							{{item.name}}
						</span>
					</div>
					<div class="logmsg fl" v-if="MM_list_four">
						<span style="width: 415px;height: 67px;" class="modellist" v-for="item in four_model">
							{{item.name}}
						</span>
					</div>
				</div>

			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						変更理由
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						1
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						2
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						3
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px;width: 552px;">
						4
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						補足参照仕様書
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						未検証
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						備考
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						日付
					</span>
				</div>
			</div>

			<!--<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						analysis_rc_id
					</span>
				</div>
			</div>-->
			<div class="logcontent fl" style="height:35px;" v-if="asta_flag">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						astaファイル名
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						版本号
					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						小版本号
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						创建时间
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						更新时间
					</span>
				</div>
			</div>
			<!--<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						user_id
					</span>
				</div>
			</div>	-->
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						翻译
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						承认
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						指摘
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" v-if="lock_flag">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						锁定状态
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						作业状态
					</span>
				</div>
			</div>
			<!--<div class="logcontent fl" style="height:35px;">-->
			<!--<div class="logtitle fl">-->
			<!--<span class="unique_id" style="lineHeight:35px;width: 552px;">-->
			<!--完成-->
			<!--</span>-->
			<!--</div>-->
			<!--</div>-->
		</div>

		<!-- tableA -->
		<div class="logbody fl" id="tableA" style="width: 245px">
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.definition_id.old_val" v-html="logtabletwo.definition_id.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.unique_id.old_val" v-html="logtabletwo.unique_id.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.author_name.old_val" v-html="logtabletwo.author_name.old_val">

					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.exception.old_val" v-html="logtabletwo.exception.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl">
					<span :title="logtabletwo.seq_diagram.old_val" v-html="logtabletwo.seq_diagram.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="rel_basic_flag">
				<div class="logmsg fl">
					<span :title="logtabletwo.rel_requirement.old_val" v-html="logtabletwo.rel_requirement.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="rel_basic_flag">
				<div class="logmsg fl">
					<span :title="logtabletwo.basic_req.old_val" v-html="logtabletwo.basic_req.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl model" v-if="MM_list">
				<div class="logmsg fl">
					<span class="modellist_o" v-for="item in first_model" :title="item.old_val" v-html="item.old_val">

					</span>
				</div>
				<div class="logmsg fl" v-if="MM_list_scend">
					<span class="modellist_o" v-for="item in scend_model" :title="item.old_val" v-html="item.old_val">

					</span>
				</div>
				<div class="logmsg fl" v-if="MM_list_third">
					<span class="modellist_o" v-for="item in third_model" :title="item.old_val" v-html="item.old_val">

					</span>
				</div>
				<div class="logmsg fl" v-if="MM_list_four">
					<span class="modellist_o" v-for="item in four_model" :title="item.old_val" v-html="item.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 67px;" :title="logtabletwo.reason.old_val" v-html="logtabletwo.reason.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logmsg fl">
					<span style="width: 245px;height: 67px;" :title="logtabletwo.ana_1.old_val" v-html="logtabletwo.ana_1.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logmsg fl">
					<span style="width: 245px;height: 67px;" :title="logtabletwo.ana_2.old_val" v-html="logtabletwo.ana_2.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logmsg fl">
					<span style="width: 245px;height: 67px" :title="logtabletwo.ana_3.old_val" v-html="logtabletwo.ana_3.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logmsg fl">
					<span style="width: 245px;height: 67px;" :title="logtabletwo.ana_4.old_val" v-html="logtabletwo.ana_4.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span class="mg" :title="logtabletwo.supple_spec.old_val" v-html="logtabletwo.supple_spec.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 35px;" :title="logtabletwo.uncheck.old_val" v-html="logtabletwo.uncheck.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.remark.old_val" v-html="logtabletwo.remark.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;line-height: 35px">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.new_date.old_val" v-html="logtabletwo.new_date.old_val">

					</span>
				</div>
			</div>

			<!--<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: center;"
				:title="logtabletwo.analysis_rc_id.old_val">
					{{logtabletwo.analysis_rc_id.old_val}}
				</div>
			</div>-->
			<div class="logcontent fl" style="height:35px;" v-if="asta_flag">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.asta_filename.old_val" v-html="logtabletwo.asta_filename.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.major_ver.old_val" v-html="logtabletwo.major_ver.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.small_ver.old_val" v-html="logtabletwo.small_ver.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.create_time.old_val" v-html="logtabletwo.create_time.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.update_time.old_val" v-html="logtabletwo.update_time.old_val">

					</span>
				</div>
			</div>
			<!--<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: center;"
				:title="logtabletwo.user_id.old_val">
					{{logtabletwo.user_id.old_val}}
				</div>
			</div>-->
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.translation_flag.old_val" v-html="logtabletwo.translation_flag.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.agree_flag.old_val" v-html="logtabletwo.agree_flag.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.has_problem.old_val" v-html="logtabletwo.has_problem.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" v-if="lock_flag">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.lock_status.old_val" v-html="logtabletwo.lock_status.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.job_status.old_val" v-html="logtabletwo.job_status.old_val">

					</span>
				</div>
			</div>
			<!--<div class="logcontent fl" style="height:35px;">-->
			<!--<div class="logmsg fl">-->
			<!--<span  style="width: 245px;height: 35px;"-->
			<!--:title="logtabletwo.complete_flag.old_val"-->
			<!--v-html="logtabletwo.complete_flag.old_val">-->

			<!--</span>-->
			<!--</div>-->
			<!--</div>-->
		</div>
		<!-- tableB -->
		<div class="logbody fl" id="tableB" style="width: 245px">
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.definition_id.val" :class="{red_active:logtabletwo.definition_id.changed=='change',blue_active:logtabletwo.definition_id.changed=='add',}" v-html="logtabletwo.definition_id.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.unique_id.val" :class="{red_active:logtabletwo.unique_id.changed=='change',blue_active:logtabletwo.unique_id.changed=='add',}" v-html="logtabletwo.unique_id.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.author_name.val" :class="{red_active:logtabletwo.author_name.changed=='change',blue_active:logtabletwo.author_name.changed=='add',}" v-html="logtabletwo.author_name.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.exception.val" :class="{red_active:logtabletwo.exception.changed=='change',blue_active:logtabletwo.exception.changed=='add',}" v-html="logtabletwo.exception.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl mg">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.seq_diagram.val" :class="{red_active:logtabletwo.seq_diagram.changed=='change',blue_active:logtabletwo.seq_diagram.changed=='add',}" v-html="logtabletwo.seq_diagram.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="rel_basic_flag">
				<div class="logmsg fl mg">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.rel_requirement.val" :class="{red_active:logtabletwo.rel_requirement.changed=='change',blue_active:logtabletwo.rel_requirement.changed=='add',}" v-html="logtabletwo.rel_requirement.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="rel_basic_flag">
				<div class="logmsg fl mg">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.basic_req.val" :class="{red_active:logtabletwo.basic_req.changed=='change',blue_active:logtabletwo.basic_req.changed=='add',}" v-html="logtabletwo.basic_req.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl model" v-if="MM_list">
				<div class="logmsg fl">
					<span class="modellist_o" v-for="item in first_model" :title="item.val" :class="{red_active:item.changed=='change',blue_active:item.changed=='add',}" v-html="item.val">

					</span>
				</div>
				<div class="logmsg fl" v-if="MM_list_scend">
					<span class="modellist_o" v-for="item in scend_model" :title="item.val" :class="{red_active:item.changed=='change',blue_active:item.changed=='add',}" v-html="item.val">

					</span>
				</div>
				<div class="logmsg fl" v-if="MM_list_third">
					<span class="modellist_o" v-for="item in third_model" :title="item.val" :class="{red_active:item.changed=='change',blue_active:item.changed=='add',}" v-html="item.val">

					</span>
				</div>
				<div class="logmsg fl" v-if="MM_list_four">
					<span class="modellist_o" v-for="item in four_model" :title="item.val" :class="{red_active:item.changed=='change',blue_active:item.changed=='add',}" v-html="item.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 67px;" :title="logtabletwo.reason.val" :class="{red_active:logtabletwo.reason.changed=='change',blue_active:logtabletwo.reason.changed=='add',}" v-html="logtabletwo.reason.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 67px;" :title="logtabletwo.ana_1.val" :class="{red_active:logtabletwo.ana_1.changed=='change',blue_active:logtabletwo.ana_1.changed=='add',}" v-html="logtabletwo.ana_1.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 67px;" :title="logtabletwo.ana_2.val" :class="{red_active:logtabletwo.ana_2.changed=='change',blue_active:logtabletwo.ana_2.changed=='add',}" v-html="logtabletwo.ana_2.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 67px;" :title="logtabletwo.ana_3.val" :class="{red_active:logtabletwo.ana_3.changed=='change',blue_active:logtabletwo.ana_3.changed=='add',}" v-html="logtabletwo.ana_3.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;" v-if="ana_list">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 67px;" :title="logtabletwo.ana_4.val" :class="{red_active:logtabletwo.ana_4.changed=='change',blue_active:logtabletwo.ana_4.changed=='add',}" v-html="logtabletwo.ana_4.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 67px;" :title="logtabletwo.supple_spec.val" :class="{red_active:logtabletwo.supple_spec.changed=='change',blue_active:logtabletwo.supple_spec.changed=='add',}" v-html="logtabletwo.supple_spec.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 67px;" :title="logtabletwo.uncheck.val" :class="{red_active:logtabletwo.uncheck.changed=='change',blue_active:logtabletwo.uncheck.changed=='add',}" v-html="logtabletwo.uncheck.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 35px" :title="logtabletwo.remark.val" :class="{red_active:logtabletwo.remark.changed=='change',blue_active:logtabletwo.remark.changed=='add',}" v-html="logtabletwo.remark.val">

					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:35px;line-height: 35px">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.new_date.val" :class="{red_active:logtabletwo.new_date.changed=='change',blue_active:logtabletwo.new_date.changed=='add',}" v-html="logtabletwo.new_date.val">

					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:35px;" v-if="asta_flag">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.asta_filename.val" :class="{red_active:logtabletwo.asta_filename.changed=='change',blue_active:logtabletwo.asta_filename.changed=='add',}" v-html="logtabletwo.asta_filename.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 35px;" :title="logtabletwo.major_ver.val" :class="{red_active:logtabletwo.major_ver.changed=='change',blue_active:logtabletwo.major_ver.changed=='add',}" v-html="logtabletwo.major_ver.val">

					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.small_ver.val" :class="{red_active:logtabletwo.small_ver.changed=='change',blue_active:logtabletwo.small_ver.changed=='add',}" v-html="logtabletwo.small_ver.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.create_time.val" :class="{red_active:logtabletwo.create_time.changed=='change',blue_active:logtabletwo.create_time.changed=='add',}" v-html="logtabletwo.create_time.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.update_time.val" :class="{red_active:logtabletwo.update_time.changed=='change',blue_active:logtabletwo.update_time.changed=='add',}" v-html="logtabletwo.update_time.val">

					</span>
				</div>
			</div>
			<!--<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span  style="lineHeight:35px; width: 245px"
					:title="logtabletwo.user_id.val"
					:class="{red_active:logtabletwo.user_id.changed=='change',blue_active:logtabletwo.user_id.changed=='add',}">
						{{logtabletwo.user_id.val}}
					</span>
				</div>
			</div>-->
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.translation_flag.val" :class="{red_active:logtabletwo.translation_flag.changed=='change',blue_active:logtabletwo.translation_flag.changed=='add',}" v-html="logtabletwo.translation_flag.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.agree_flag.val" :class="{red_active:logtabletwo.agree_flag.changed=='change',blue_active:logtabletwo.agree_flag.changed=='add',}" v-html="logtabletwo.agree_flag.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="width: 245px;height: 35px;" :title="logtabletwo.has_problem.val" :class="{red_active:logtabletwo.has_problem.changed=='change',blue_active:logtabletwo.has_problem.changed=='add',}" v-html="logtabletwo.has_problem.val">
						<!--  -->

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" v-if="lock_flag">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.lock_status.val" :class="{red_active:logtabletwo.lock_status.changed=='change',blue_active:logtabletwo.lock_status.changed=='add',}" v-html="logtabletwo.lock_status.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style=" width: 245px;height: 35px;line-height: 35px;" :title="logtabletwo.job_status.val" :class="{red_active:logtabletwo.job_status.changed=='change',blue_active:logtabletwo.job_status.changed=='add',}" v-html="logtabletwo.job_status.val">

					</span>
				</div>
			</div>
			<!--<div class="logcontent fl" style="height:35px;">-->
			<!--<div class="logmsg fl">-->
			<!--<span  style=" width: 245px;height: 35px;"-->
			<!--:title="logtabletwo.complete_flag.val"-->
			<!--:class="{red_active:logtabletwo.complete_flag.changed=='change',blue_active:logtabletwo.complete_flag.changed=='add',}"-->
			<!--v-html="logtabletwo.complete_flag.val">-->
			<!--</span>-->
			<!--</div>-->
			<!--</div>-->
		</div>
	</div>
</template>
<script>
	export default {
		props: ["commit_id", "commit_m_id", "Boolean_Examine_Flag"],
		data() {
			return {
				duc_trigger_red_flag: true,
				duc_trigger_blue_flag: false,
				sumbit_type: '',
				work_status: 4,
				MM_list: false,
				MM_list_first: false,
				MM_list_scend: false,
				MM_list_third: false,
				MM_list_four: false,
				ana_list: false,
				lock_flag: false,
				asta_flag: false,
				rel_basic_flag: false,
				first_model: [],
				scend_model: [],
				third_model: [],
				four_model: [],
				ct_id: this.commit_id,
				ct_m_id: this.commit_m_id,
				logtabletwo: {},
				end_id: 4430,
				start_id: 4430,

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
							if(this.logtabletwo.lock_status == null) {
								this.lock_flag = false;
							} else {
								this.lock_flag = true;
							}
							if(this.logtabletwo.asta_filename == null) {
								this.asta_flag = false;
							} else {
								this.asta_flag = true;
							}
							if(this.logtabletwo.basic_req == null && this.logtabletwo.rel_requirement == null) {
								this.rel_basic_flag = false;
							} else {
								this.rel_basic_flag = true;
							}
							if(this.logtabletwo.ana_1 == null || this.logtabletwo.ana_2 == null || this.logtabletwo.ana_3 == null || this.logtabletwo.ana_4 == null) {
								this.ana_list = false;
							} else {
								this.ana_list = true;
							}
							if(this.logtabletwo.model_list.length == 0) {
								this.MM_list = false;
							} else {
								this.MM_list = true;
								var i = 0;
								for(i; i < this.logtabletwo.model_list.length; i++) {

									if(this.logtabletwo.model_list[i].changed == null) {

										var j = 0
										for(j; j < this.logtabletwo.model_list[i].sub_list.length; j++) {

											if(this.logtabletwo.model_list[i].sub_list[j].changed == null) {

												var k = 0
												for(k; k < this.logtabletwo.model_list[i].sub_list[j].sub_list.length; k++) {

													if(this.logtabletwo.model_list[i].sub_list[j].sub_list[k].changed == null) {

														var l = 0
														for(l; l < this.logtabletwo.model_list[i].sub_list[j].sub_list[k].sub_list.length; l++) {

															if(this.logtabletwo.model_list[i].sub_list[j].sub_list[k].sub_list[l].changed == null) {

															} else {
																this.MM_list_four = true;
																this.four_model.push(this.logtabletwo.model_list[i].sub_list[j].sub_list[k].sub_list[l])
															}
														}
													} else {
														this.MM_list_third = true;
														this.third_model.push(this.logtabletwo.model_list[i].sub_list[j].sub_list[k])
													}
												}
											} else {
												this.MM_list_scend = true;
												this.scend_model.push(this.logtabletwo.model_list[i].sub_list[j])
											}
										}
									} else {
										this.MM_list_first = true;
										this.first_model.push(this.logtabletwo.model_list[i])
									}
								}

							}
							this.getWorkStatus()
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
			}
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
	
	#tableA>div span {
		text-align: left;
		overflow: auto;
		width: 245px;
		overflow-y: auto;
	}
	
	#tableB>div span {
		text-align: left;
		overflow: auto;
		width: 245px;
		overflow-y: auto;
	}
	
	.mg {
		text-align: left;
		overflow: auto;
		width: 247px;
	}
	
	.el-button_ex {
		display: inline-block;
		line-height: 1;
		white-space: nowrap;
		cursor: pointer;
		background: #fff;
		border: 1px solid #c4c4c4;
		color: #1f2d3d;
		margin: 0;
		padding: 10px 15px;
		border-radius: 4px;
	}
	
	.el-button--primary_ex {
		color: #fff !important;
		background-color: #42b983;
		border-color: #42b983;
	}
</style>