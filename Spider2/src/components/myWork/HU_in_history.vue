<template>
	<div class="fl loghtml">

		<!-- title -->
		<div class="logbody fl" id="title">
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px;width: 552px;">
						ARLID
					</span>
				</div>
			</div>
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
					<span class="unique_id" style="lineHeight:35px; width: 552px">
						版本号
					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 552px">
						小版本号
					</span>
				</div>
			</div>
			<div class="logcontent fl">
				<div class="logtitle fl">
					<span class="logspan">
						オプション項目
					</span>
				</div>
				<div class="logmsg fl">
					<span class="opt" style="fontSize:14px">AMP
					</span>
					<span class="opt" style="fontSize:14px">DSRC
					</span>
					<span class="opt" style="fontSize:14px">DCM
					</span>
					<span class="opt" style="fontSize:14px">RSE
					</span>
					<span class="opt" style="fontSize:14px">TouchPad
					</span>
					<span class="opt" style="fontSize:14px">SeparateDisp
					</span>
					<span class="opt" style="fontSize:14px;border:0 none">システム構成
					</span>
				</div>

			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px; width: 553px">
						関連基本要件
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:67px; width: 553px">
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
			<div class="logcontent fl" style="height:400px;">
				<div class="logtitle fl">
					<span class="logspan" style="lineHeight:400px;width:135px">
						責務分担
					</span>
				</div>
				<div class="logtitle fl">
					<span class="dcu" style="width:118px">
						DCU
					</span>
					<span class="meu">
						MEU
					</span>
				</div>
				<div class="logtitle fl">
					<span class="dcu_status">
						状態
					</span>
					<span class="dcu_action">
						動作
					</span>
					<span class="duc_trigger">
						トリガー
					</span>
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
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:35px; width: 553px">
						ユニークID
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:auto;border-left:  1px solid #dfe6ec;border-bottom:  1px solid #dfe6ec" v-if="MM_list">
				<div class="fl" id="model" style="width:144px;line-height: 67px;">
					<span class="logspan" style="width:143px;font-size:12px;">
						H/U以外のＭＭ部品
					</span>
				</div>
				<div class="logmsg fl" style="width: 229px;border-bottom: none;">
					<span class="modellist" v-for="item in logtabletwo.mm_model_list">
						{{item.name}}
					</span>
				</div>
				<div class="logmsg fl" style="width: 180px;border-left: none;border-right: none;border-bottom: none;">
					<span class="modellist" v-for="item in logtabletwo.mm_model_list">
						{{item.title}}
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:auto;border-left:  1px solid #dfe6ec;border-bottom:  1px solid #dfe6ec" v-if="Other_list">
				<div class=" fl" id="model" style="width:186px;padding:0;line-height: 67px;">
					<span class="logspan" style="width:185px;padding:0;font-size:12px;">
						他部署設計部品(部品名は参考)
					</span>
				</div>
				<div class="logmsg fl" style="width: 122px;">
					<span class="modellist" v-for="item in logtabletwo.other_model_list">
						{{item.name}}
					</span>
				</div>
				<div class="logmsg fl" style="width:245px;">
					<span class="modellist" v-for="item in logtabletwo.other_model_list">
						{{item.title}}
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:670px;">
				<div class="logtitle fl">
					<span class="logspan" style="lineHeight:400px;width:185px;padding:0;font-size:12px;lineHeight:670px">
						機能配置を判断したエビデンス
					</span>
				</div>
				<div class="logmsg fl" style="width: 122px">
					<span class="modellist">
						001 システム仕様書
					</span>
					<span class="modellist" style="height:335px;lineHeight:74px">
						003 共通アプリ・AVC-LAN仕様書
					</span>
					<span class="modellist" style="height:134px;lineHeight:40px">
						318 DCU-MEU間連携仕様書DCU-MEU interaction spec.
					</span>
					<span class="modellist" style="height:134px;lineHeight:40px">
						その他資料Other document.
					</span>
				</div>
				<div class="logmsg fl" style="width:245px;">
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						章　Chapter/Sectionor ページ番号 Page No
					</span>
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						章　Chapter/Sectionor ページ番号 Page No
					</span>
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						シーケンス仕様Sequence spec.
					</span>
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						シーケンス番号Sequence No.
					</span>
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						コマンドガイドCommand guide
					</span>
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						OPC
					</span>
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						機能配置・機能仕様Function location and spec.
					</span>
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						章　Chapter/Sectionor ページ番号 Page No
					</span>
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						ドキュメント名※トヨタ仕様の場合は仕様番号も記載する事
					</span>
					<span class="modellist" style="fontSize:12px;lineHeight:30px">
						章　Chapter/Sectionor ページ番号 Page No
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						テスト結果
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
						備考
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						備考1
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						備考2
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						要件漏れチェック
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
			<div class="logcontent fl" style="height:60px;">
				<div class="logtitle fl">
					<span class="unique_id" style="lineHeight:60px;width: 552px;">
						変更理由
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
					<span class="unique_id" style="lineHeight:26px;width: 552px;">
						作业状态
					</span>
				</div>
			</div>
		</div>
		<!-- tableA -->
		<div id="tableA" class="logbody fl" style="width: 245px">
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.arl_id.old_val" v-html="logtabletwo.arl_id.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.hu_id.old_val" v-html="logtabletwo.hu_id.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.author.old_val" v-html="logtabletwo.author.old_val">

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
			<div class="logcontent fl">
				<div class="logmsg fl">
					<span class="olog" style="fontSize:14px" :title="logtabletwo.amp.old_val" v-html="logtabletwo.amp.old_val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.dsrc.old_val" v-html="logtabletwo.dsrc.old_val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.dcm.old_val" v-html="logtabletwo.dcm.old_val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.rse.old_val" v-html="logtabletwo.rse.old_val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.touch_pad.old_val" v-html="logtabletwo.touch_pad.old_val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.separate_disp.old_val" v-html="logtabletwo.separate_disp.old_val">
					</span>
					<span class="olog" style="fontSize:12px;border:0 none" :title="logtabletwo.system_conf.old_val" v-html="logtabletwo.system_conf.old_val">
					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl">
					<span style="overflow-y: auto; width: 245px" :title="logtabletwo.rel_requirement.old_val" v-html="logtabletwo.rel_requirement.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl">
					<span  style="lineHeight:67px; width: 245px"
					:title="logtabletwo.basic_req.old_val"
					v-html="logtabletwo.basic_req.old_val">

					</span>
				</div>
			</div>

			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="overflow-y: auto; width: 245px" :title="logtabletwo.exception.old_val" v-html="logtabletwo.exception.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:400px;">
				<div class="logmsg fl">
					<span class="dcu_status_o" :title="logtabletwo.dcu_status.old_val" v-html="logtabletwo.dcu_status.old_val">

					</span>
					<span class="dcu_action_o" :title="logtabletwo.dcu_action.old_val" v-html="logtabletwo.dcu_action.old_val">
						<!-- {{logtabletwo.dcu_action.old_val}} -->
					</span>
					<span class="duc_trigger_o" :title="logtabletwo.dcu_trigger.old_val" v-html="logtabletwo.dcu_trigger.old_val">

					</span>
					<span class="dcu_status_o" :title="logtabletwo.meu_status.old_val" v-html="logtabletwo.meu_status.old_val">

					</span>
					<span class="dcu_action_o" :title="logtabletwo.meu_action.old_val" v-html="logtabletwo.meu_action.old_val">

					</span>
					<span class="duc_trigger_o" style="border:0 none;" :title="logtabletwo.meu_trigger.old_val" v-html="logtabletwo.meu_trigger.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;line-height: 35px;" :title="logtabletwo.unique_id.old_val" v-html="logtabletwo.unique_id.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:auto;" v-if="MM_list">
				<div class="logmsg fl">
					<span class="modellist_o" v-for="item in logtabletwo.mm_model_list" :title="item.old_val" v-html="item.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:auto;" v-if="Other_list">
				<div class="logmsg fl" style="width:245px;">
					<span class="modellist_o" v-for="item in logtabletwo.other_model_list" :title="item.old_val" v-html="item.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:670px;">
				<div class="logmsg fl" style="width:245px;">
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.sys_spec_chapter.old_val" v-html="logtabletwo.sys_spec_chapter.old_val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.common_chapter.old_val" v-html="logtabletwo.common_chapter.old_val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.common_seq_spec.old_val" v-html="logtabletwo.common_seq_spec.old_val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.common_seq_no.old_val" v-html="logtabletwo.common_seq_no.old_val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.common_cmd_guide.old_val" v-html="logtabletwo.common_cmd_guide.old_val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.common_opc.old_val" v-html="logtabletwo.common_opc.old_val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.inter_loc_spec.old_val" v-html="logtabletwo.inter_loc_spec.old_val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.inter_chapter.old_val" v-html="logtabletwo.inter_chapter.old_val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.other_doc.old_val" v-html="logtabletwo.other_doc.old_val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :title="logtabletwo.other_chapter.old_val" v-html="logtabletwo.other_chapter.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.test_results.old_val" v-html="logtabletwo.test_results.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">

				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.future_req.old_val" v-html="logtabletwo.future_req.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.remark.old_val" v-html="logtabletwo.remark.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.remark1.old_val" v-html="logtabletwo.remark1.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.remark2.old_val" v-html="logtabletwo.remark2.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.leak_check.old_val" v-html="logtabletwo.leak_check.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;line-height: 35px;" :title="logtabletwo.new_date.old_val" v-html="logtabletwo.new_date.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:60px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.reason.old_val" v-html="logtabletwo.reason.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.update_time.old_val" v-html="logtabletwo.update_time.old_val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.translation_flag.old_val" v-html="logtabletwo.translation_flag.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.agree_flag.old_val" v-html="logtabletwo.agree_flag.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.has_problem.old_val" v-html="logtabletwo.has_problem.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" v-if="lock_flag">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;line-height: 35px;" :title="logtabletwo.lock_status.old_val" v-html="logtabletwo.lock_status.old_val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;line-height: 35px;" :title="logtabletwo.job_status.old_val" v-html="logtabletwo.job_status.old_val">

				</div>
			</div>
		</div>
		<!-- tableB -->
		<div id="tableB" class="logbody fl" style="width: 250px">
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.arl_id.val" :class="{red_active:logtabletwo.arl_id.changed=='change',blue_active:logtabletwo.arl_id.changed=='add',}" v-html="logtabletwo.arl_id.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width: 245px;" :title="logtabletwo.hu_id.val" :class="{red_active:logtabletwo.hu_id.changed=='change',blue_active:logtabletwo.hu_id.changed=='add',}" v-html="logtabletwo.hu_id.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px;width:245px;" :title="logtabletwo.author.val" :class="{red_active:logtabletwo.author.changed=='change',blue_active:logtabletwo.author.changed=='add',}" v-html="logtabletwo.author.val">

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
			<div class="logcontent fl">
				<div class="logmsg fl">
					<span class="olog" style="fontSize:14px;" :title="logtabletwo.amp.val" :class="{red_active:logtabletwo.amp.changed=='change',blue_active:logtabletwo.amp.changed=='add',}" v-html="logtabletwo.amp.val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.dsrc.val" :class="{red_active:logtabletwo.dsrc.changed=='change',blue_active:logtabletwo.dsrc.changed=='add',}" v-html="logtabletwo.dsrc.val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.dcm.val" :class="{red_active:logtabletwo.dcm.changed=='change',blue_active:logtabletwo.dcm.changed=='add',}" v-html="logtabletwo.dcm.val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.rse.val" :class="{red_active:logtabletwo.rse.changed=='change',blue_active:logtabletwo.rse.changed=='add',}" v-html="logtabletwo.rse.val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.touch_pad.val" :class="{red_active:logtabletwo.touch_pad.changed=='change',blue_active:logtabletwo.touch_pad.changed=='add',}" v-html="logtabletwo.touch_pad.val">
					</span>
					<span class="olog" style="fontSize:14px" :title="logtabletwo.separate_disp.val" :class="{red_active:logtabletwo.separate_disp.changed=='change',blue_active:logtabletwo.separate_disp.changed=='add',}" v-html="logtabletwo.separate_disp.val">
					</span>
					<span class="olog" style="fontSize:12px;border:0 none" :title="logtabletwo.system_conf.val" :class="{red_active:logtabletwo.system_conf.changed=='change',blue_active:logtabletwo.system_conf.changed=='add',}" v-html="logtabletwo.system_conf.val">
					</span>
				</div>

			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl">
					<span style=" width: 245px" :title="logtabletwo.rel_requirement.val" :class="{red_active:logtabletwo.rel_requirement.changed=='change',blue_active:logtabletwo.rel_requirement.changed=='add',}" v-html="logtabletwo.rel_requirement.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:67px;">
				<div class="logmsg fl">
					<span  style="lineHeight:67px; width: 245px"
					:title="logtabletwo.basic_req.val"
					:class="{red_active:logtabletwo.basic_req.changed=='change',blue_active:logtabletwo.basic_req.changed=='add',}"
					v-html="logtabletwo.basic_req.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style=" width: 245px" :title="logtabletwo.exception.val" :class="{red_active:logtabletwo.exception.changed=='change',blue_active:logtabletwo.exception.changed=='add',}" v-html="logtabletwo.exception.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:400px;">
				<div class="logmsg	 fl">
					<span class="dcu_status_o" :title="logtabletwo.dcu_status.val" :class="{red_active:logtabletwo.dcu_status.changed=='change',blue_active:logtabletwo.dcu_status.changed=='add',}" v-html="logtabletwo.dcu_status.val">

					</span>
					<span class="dcu_action_o" :title="logtabletwo.dcu_action.val" :class="{red_active:logtabletwo.dcu_action.changed=='change',blue_active:logtabletwo.dcu_action.changed=='add',}" v-html="logtabletwo.dcu_action.val">

					</span>
					<span class="duc_trigger_o" :title="logtabletwo.dcu_trigger.val" :class="{red_active:logtabletwo.dcu_trigger.changed=='change',blue_active:logtabletwo.dcu_trigger.changed=='add',}" v-html="logtabletwo.dcu_trigger.val">

					</span>
					<span class="dcu_status_o" :title="logtabletwo.meu_status.val" :class="{red_active:logtabletwo.meu_status.changed=='change',blue_active:logtabletwo.meu_status.changed=='add',}" v-html="logtabletwo.meu_status.val">

					</span>
					<span class="dcu_action_o" :title="logtabletwo.meu_action.val" :class="{red_active:logtabletwo.meu_action.changed=='change',blue_active:logtabletwo.meu_action.changed=='add',}" v-html="logtabletwo.meu_action.val">

					</span>
					<span class="duc_trigger_o" style="border:0 none;" :title="logtabletwo.meu_trigger.val" :class="{red_active:logtabletwo.meu_trigger.changed=='change',blue_active:logtabletwo.meu_trigger.changed=='add',}" v-html="logtabletwo.meu_trigger.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;line-height: 35px" :title="logtabletwo.unique_id.val" :class="{red_active:logtabletwo.unique_id.changed=='change',blue_active:logtabletwo.unique_id.changed=='add',}" v-html="logtabletwo.unique_id.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:auto;" v-if="MM_list">
				<div class="logmsg fl">
					<span class="modellist_o" v-for="item in logtabletwo.mm_model_list" :class="{red_active:item.changed=='change',blue_active:item.changed=='add',}" :title="item.val" v-html="item.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:auto;" v-if="Other_list">
				<div class="logmsg fl" style="width:245px;">
					<span class="modellist_o" v-for="item in logtabletwo.other_model_list" :class="{red_active:item.changed=='change',blue_active:item.changed=='add',}" :title="item.val" v-html="item.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:670px;">
				<div class="logmsg fl" style="width:245px;">
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.sys_spec_chapter.changed=='change',blue_active:logtabletwo.sys_spec_chapter.changed=='add',}" :title="logtabletwo.sys_spec_chapter.val" v-html="logtabletwo.sys_spec_chapter.val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.common_chapter.changed=='change',blue_active:logtabletwo.common_chapter.changed=='add',}" :title="logtabletwo.common_chapter.val" v-html="logtabletwo.common_chapter.val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.common_seq_spec.changed=='change',blue_active:logtabletwo.common_seq_spec.changed=='add',}" :title="logtabletwo.common_seq_spec.val" v-html="logtabletwo.common_seq_spec.val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.common_seq_no.changed=='change',blue_active:logtabletwo.common_seq_no.changed=='add',}" :title="logtabletwo.common_seq_no.val" v-html="logtabletwo.common_seq_no.val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.common_cmd_guide.changed=='change',blue_active:logtabletwo.common_cmd_guide.changed=='add',}" :title="logtabletwo.common_cmd_guide.val" v-html="logtabletwo.common_cmd_guide.val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.common_opc.changed=='change',blue_active:logtabletwo.common_opc.changed=='add',}" :title="logtabletwo.common_opc.val" v-html="logtabletwo.common_opc.val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.inter_loc_spec.changed=='change',blue_active:logtabletwo.inter_loc_spec.changed=='add',}" :title="logtabletwo.inter_loc_spec.val" v-html="logtabletwo.inter_loc_spec.val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.inter_chapter.changed=='change',blue_active:logtabletwo.inter_chapter.changed=='add',}" :title="logtabletwo.inter_chapter.val" v-html="logtabletwo.inter_chapter.val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.other_chapter.changed=='change',blue_active:logtabletwo.other_chapter.changed=='add',}" :title="logtabletwo.other_doc.val" v-html="logtabletwo.other_doc.val">

					</span>
					<span class="modellist_o" style="fontSize:12px;" :class="{red_active:logtabletwo.other_chapter.changed=='change',blue_active:logtabletwo.other_chapter.changed=='add',}" :title="logtabletwo.other_chapter.val" v-html="logtabletwo.other_chapter.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.test_results.val" :class="{red_active:logtabletwo.test_results.changed=='change',blue_active:logtabletwo.test_results.changed=='add',}" v-html="logtabletwo.test_results.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.future_req.val" :class="{red_active:logtabletwo.future_req.changed=='change',blue_active:logtabletwo.future_req.changed=='add',}" v-html="logtabletwo.future_req.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" :title="logtabletwo.remark.val">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :class="{red_active:logtabletwo.remark.changed=='change',blue_active:logtabletwo.remark.changed=='add',}" v-html="logtabletwo.remark.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" :title="logtabletwo.remark1.val">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :class="{red_active:logtabletwo.remark1.changed=='change',blue_active:logtabletwo.remark1.changed=='add',}" v-html="logtabletwo.remark1.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.remark2.val" :class="{red_active:logtabletwo.remark2.changed=='change',blue_active:logtabletwo.remark2.changed=='add',}" v-html="logtabletwo.remark2.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.leak_check.val" :class="{red_active:logtabletwo.leak_check.changed=='change',blue_active:logtabletwo.leak_check.changed=='add',}" v-html="logtabletwo.leak_check.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;line-height: 35px" :title="logtabletwo.new_date.val" :class="{red_active:logtabletwo.new_date.changed=='change',blue_active:logtabletwo.new_date.changed=='add',}" v-html="logtabletwo.new_date.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:60px;" :title="logtabletwo.reason.val">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :class="{red_active:logtabletwo.reason.changed=='change',blue_active:logtabletwo.reason.changed=='add'}" v-html="logtabletwo.reason.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl">
					<span style="lineHeight:35px; width: 245px" :title="logtabletwo.update_time.val" :class="{red_active:logtabletwo.update_time.changed=='change',blue_active:logtabletwo.update_time.changed=='add',}" v-html="logtabletwo.update_time.val">

					</span>
				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" :title="logtabletwo.translation_flag.val">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :class="{red_active:logtabletwo.translation_flag.changed=='change',blue_active:logtabletwo.translation_flag.changed=='add',}" v-html="logtabletwo.translation_flag.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.agree_flag.val" :class="{red_active:logtabletwo.agree_flag.changed=='change',blue_active:logtabletwo.agree_flag.changed=='add',}" v-html="logtabletwo.agree_flag.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto" :title="logtabletwo.has_problem.val" :class="{red_active:logtabletwo.has_problem.changed=='change',blue_active:logtabletwo.has_problem.changed=='add',}" v-html="logtabletwo.has_problem.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;" v-if="lock_flag">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;line-height: 35px;" :title="logtabletwo.lock_status.val" :class="{red_active:logtabletwo.lock_status.changed=='change',blue_active:logtabletwo.lock_status.changed=='add',del_active:logtabletwo.lock_status.changed=='delete'}" v-html="logtabletwo.lock_status.val">

				</div>
			</div>
			<div class="logcontent fl" style="height:35px;">
				<div class="logmsg fl" style="width:245px;text-align: left;overflow: auto;line-height: 35px;" :title="logtabletwo.job_status.val" :class="{red_active:logtabletwo.job_status.changed=='change',blue_active:logtabletwo.job_status.changed=='add',del_active:logtabletwo.job_status.changed=='delete'}" v-html="logtabletwo.job_status.val">

				</div>
			</div>
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
				duc_trigger_red_flag: false,
				duc_trigger_blue_flag: true,
				sumbit_type: '',
				work_status: 4,
				MM_list: true,
				Other_list: true,
				lock_flag:false,
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
							if(res.data.content.lock_status == null) {
								this.lock_flag = false;
							}else{
								this.lock_flag = true;
							};
							if(res.data.content.mm_model_list.length == 0) {
								this.MM_list = false;
							} else {
								this.MM_list = true;
							};
							if(res.data.content.other_model_list.length == 0) {
								this.Other_list = false;
							} else {
								this.Other_list = true;
							};
							this.getWorkStatus();
							//				     	this.$emit('get_Boolean_Examine',1)
						} else {
							this.logtabletwo = [];
							this.$alert("没数据o(╥﹏╥)o")
						}
					})
			},
			getWorkStatus() {
				this.$axios.get(this.Ip + "/LookStatus/" + this.logtabletwo.hu_id.val + '/' + this.sumbit_type.classify)
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
		overflow-x: auto;
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
		line-height: 200px;
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
		overflow: hidden;
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
		width: 295px;
	}
	/**/

	.dcu_status_o,
	.dcu_action_o,
	.duc_trigger_o {
		border-bottom: 1px solid #dfe6ec;
		height: 67px;
		text-align: center;
		width: 245px;
		overflow-y: scroll;
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
		text-align: center;
		overflow: hidden;
	}
	/**/

	.blue_active {
		color: blue;
	}

	.red_active {
		color: red;
	}

	.del_active {
		text-decoration: line-through;
	}

	#tableA span {
		text-align: left;
		overflow-y: auto;
	}

	#tableB span {
		text-align: left;
		overflow-y: auto;
	}

	#model {
		border: none;
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
