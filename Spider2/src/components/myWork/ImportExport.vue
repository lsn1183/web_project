<template>
	<div class="g_page" v-loading.fullscreen.lock="fullscreenLoading" element-loading-text="正在保存中,请稍等... ...">
		<div class="s_page_left">
			<ul>
				<li :class="{'active': szPointer=='Import'}" @click="OnImport()">导入</li>
				<li :class="{'active': szPointer=='Export'}" @click="OnExport()">导出</li>
				<!--<li :class="{'active': szPointer=='CheckRule'}" @click="OnCheckRule()">检查规则</li>-->
				<!--new-->
				<li v-if="this.Roles == 'PL' || this.Roles == 'Leader'||this.Roles == 'Admin'?true:false" :class="{'active': szPointer=='Import2'}" @click="OnImport2()">ASTA文件上傳</li>
				<li v-if="Roles == 'PL' || Roles == 'Admin' ?true:false" :class="{'active': szPointer=='Release' || szPointer=='Releasing'}" @click="OnRelease()">Release</li>
				<li v-if="Roles == 'PL' || Roles == 'Admin' ?true:false" :class="{'active': szPointer=='Deblocking'}" @click="OnUnlock()">解锁</li>
				<li :class="{'active': szPointer=='whitelist'}" @click="OnWhiteList()">白名单</li>
			</ul>

		</div>

		<div class="" v-show="szPointer=='Import'">
			<!-- <i class="el-icon-warning"> 此功能暂时不对外开放</i> -->
			<div class="g_dialog g_dialog_ex">
				<div class="g_dialog_body">
					<!-- 					<p class="s_section">
						<span class="s_section_left"></span>
						<el-select class="s_section_right" v-model="lead_typeindex" placeholder="请选择导出的数据类型" size='small' @change="Onleadtype()">
						    <el-option v-for="item in lead_scope" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
					</p> -->
					<p class="s_section">
						<span class="s_section_left">类型</span>
						<el-select class="s_section_right" v-model="lead_typeindex" placeholder="请选择导入的数据范围" size='small' @change="OnleadScope()">
							<el-option v-for="item in lead_type" :key="item.value" :label="item.label" :value="item.value" v-if=" Roles == 'PL' || Roles == 'Admin' || item.value != 'ARL'"></el-option>
						</el-select>
					</p>
					<div class="s_section" style="" v-loading.fullscreen.lock="fullscreenLoading2" element-loading-text="正在上传中,请稍等... ...">
						<el-upload :action='lead_Ip' :data="msg" :on-success="lead_success" :disabled="lead_disabled" class="upload_box" :before-upload="upload" :show-file-list="file_flag">
							<el-button class="lead_btn" type="primary" @click="lead_click"><i class="el-icon-caret-bottom"> 导入</i>
							</el-button>
						</el-upload>
					</div>
				</div>
				<!--显示区块-->
				<div style="width:1080px;" class="table_tr_down" v-if="tableDisplay" id="table_check_list">
					<el-table :data="show_check" border="" maxHeight="650" @selection-change="handleSelectionChange">

						<el-table-column prop="check_project" label="工程" min-width='180' align="center">
						</el-table-column>
						<el-table-column prop="check_subject" label="チェック項目" width='350' align="center">
						</el-table-column>
						<el-table-column prop="check_methord" label="確認方法" min-width='300' align="center">
						</el-table-column>
						<el-table-column prop="" label="確認欄" min-width='150' align="center">
							<template scope="scope">
								<el-select v-model="show_check[scope.$index].check_result" placeholder="" size="small">
									<el-option v-for="(item,index) in checkType" :key="index" :label="item.label" :value="item.value"></el-option>
								</el-select>
							</template>
						</el-table-column>
						<!--<el-table-column prop="" label="レビュワー確認欄" min-width='100' align="center">-->
						<!--</el-table-column>-->
					</el-table>

					<!--<div style="height: 50px;">-->
					<!--<el-button type="primary" class="white_list_btn" @click="check_click()"><i class="el-icon-caret-bottom">check</i>-->
					<!--</el-button>-->
					<!--</div>-->
					<div style="padding-left: 40px;font-size: 14px;margin-top: 25px">注意：
						<p class="padding_p1">1.○ : 問題なし　対策を記入　</p>
						<p class="padding_p1">2.△ :一部問題有り 対策必要。</p>
						<p class="padding_p1">3.- :対象外</p>
					</div>
				</div>

			</div>
		</div>
		<div class="" v-show="szPointer=='Export'">
			<div class="g_dialog g_dialog_ex">
				<div class="g_dialog_body">

					<p class="s_section">
						<span class="s_section_left">类型</span>
						<el-select class="s_section_right" v-model="typeindex" placeholder="请选择导出的数据类型" size='small' @change="selectType()">
							<el-option v-for="item in type" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
					</p>

					<p class="s_section" v-show="checklist_flag">
						<span class="s_section_left">范围</span>
						<el-select class="s_section_right" v-model="scopeindex" placeholder="请选择导出的数据范围" size='small' @change="OnScope()">
							<el-option v-for="item in scope" :key="item.value" :label="item.label" :value="item.value" v-if=" Roles == 'PL' || Roles == 'Admin' || item.value != 'All'"></el-option>
						</el-select>
					</p>

					<p class="s_section" v-show="bCategoryDisplay">
						<span class="s_section_left">分类</span>
						<el-select class="s_section_right" v-model="categoryindex" placeholder="全部" size='small' disabled>
							<el-option v-for="item in category" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
					</p>

					<p class="s_section" v-show="checkTime_flag">
						<span class="s_section_left">时间范围</span>
						<el-date-picker v-model="time_value" type="datetimerange" :picker-options="pickerOptions" placeholder="选择时间范围" align="right" size="small" time-arrow-control="true"></el-date-picker>
					</p>
					<div class="s_section">
						<el-button class="s_buttom" type="primary" @click="OnDoExport()"><i class="el-icon-caret-bottom"> 导出</i>
						</el-button>
					</div>
					<!--<div class="s_section" v-show="check_flag">-->
					<!--<el-button class="s_buttom" type="primary" @click="OnDoExport_checklist()"><i class="el-icon-caret-bottom">-->
					<!--导出</i>-->
					<!--</el-button>-->
					<!--</div>-->

				</div>
			</div>
		</div>
		<!--New ADD import-->
		<div class="" v-show="szPointer=='Import2'">

			<div class="g_dialog g_dialog_ex">
				<div class="g_dialog_body">

					<p class="s_section">
						<span class="s_section_left">用戶組</span>
						<el-select class="s_section_right" v-model="lead_typeindex2" placeholder="請選擇上傳的組" size='small' @change="OnleadScope2()">
							<el-option v-for="(item,index) in lead_type2" :key="item.group_id" :label="item.group_name" :value="index"></el-option>
						</el-select>
					</p>
					<div class="s_section">
						<el-upload :action='lead_Ip2' :data="msg2" :on-success="lead_success2" :disabled="lead_disabled2" class="upload_box" :before-upload="upload2" :show-file-list="false">
							<el-button class="lead_btn" type="primary" @click="lead_click2()"><i class="el-icon-caret-bottom"> 导入</i>
							</el-button>
						</el-upload>
					</div>
					<div class="s_section_expro" v-if="this.Roles=='PL'||this.Roles=='Admin'?true:false">
						<el-button type="primary" @click="OnDoExport2()"><i class="el-icon-caret-bottom">全导出</i>
						</el-button>
					</div>

					<div style="width:940px;" class="table_tr_down">
						<el-table :data="show_file.data" border="" maxHeight="750">
							<el-table-column prop="user_name" label="上傳人" min-width='120' align="center">
							</el-table-column>

							<el-table-column prop="file_name" label="文件名稱" width='500' align="center">
							</el-table-column>
							<el-table-column prop="create_time" label="上傳日期" min-width='180' align="center">
							</el-table-column>
							<el-table-column prop="file_url" label="操作" min-width='120' align="center">
								<template scope="scope">
									<el-button type="text" @click="downFile(scope.$index,scope.row)" size="small"><i class="el-icon-arrow-down" style="font-style: normal">下載</i></el-button>
									<el-button type="text" @click="Delete(scope.$index,scope.row)" size="small"><i class="el-icon-delete">删除</i></el-button>
								</template>
							</el-table-column>
						</el-table>
					</div>

				</div>
			</div>
		</div>

		<div class="" v-show="szPointer=='Release'">
			<div class="g_dialog g_dialog_ex">
				<div class="g_dialog_body">
					<p class="s_section">
						<span class="s_section_left s_section_release_left">日期</span>
						<el-date-picker class="s_section_right" size='small' type="date" placeholder="选择日期" v-model="release_PostArray.date" format @change="setDate" default-value></el-date-picker>
					</p>

					<p class="s_section">
						<span class="s_section_left s_section_release_left">TMC 最新指摘</span>

						<el-input class="s_section_right" size='small' placeholder="请输入TMC 最新指摘" v-model="release_PostArray.tmc_issue"></el-input>
					</p>

					<p class="s_section">
						<span class="s_section_left s_section_release_left">Suntec 最新回答</span>

						<el-input class="s_section_right" size='small' placeholder="请输入Suntec 最新回答" v-model="release_PostArray.suntec_confirm"></el-input>
					</p>

					<p class="s_section">
						<span class="s_section_left s_section_release_left">blocklist</span>

						<el-input class="s_section_right" size='small' placeholder="请输入blocklist" v-model="release_PostArray.blocklist"></el-input>
					</p>
					<p class="s_section">
						<span class="s_section_left s_section_release_left">新建版本号</span>
						<el-input class="s_section_right" size='small' placeholder="请输入版本号" v-model="release_PostArray.version"></el-input>
					</p>
					<p class="s_section">
						<span class="s_section_left s_section_release_left">前一版本日期</span>
						<el-select class="s_section_right" v-model="release_PostArray.pre_version" placeholder="请选择版本时间" size='small'>
							<el-option v-for="item in array_pre_version" :key="item" :label="item" :value="item"></el-option>
						</el-select>
					</p>
					<p class="s_section">
						<span class="s_section_left s_section_release_left">前一版本号</span>
						<el-input class="s_section_right" size='small' v-model="array_pre_version_data[0]" disabled></el-input>
						<!--<el-select class="s_section_right" v-model="tiem" placeholder="请选择版本号" size='small'>
							<el-option v-for="item in array_pre_version_data" :key="item" :label="item" :value="item"></el-option>
						</el-select>-->
					</p>

					<div class="s_section">
						<el-button class="s_buttom s_buttom_ex" type="primary" @click="OnDoRelease()"><i class="el-icon-upload2"> release作成</i></el-button>
					</div>

				</div>
			</div>
		</div>

		<div class="" v-show="szPointer == 'Releasing'">
			<div class="g_dialog g_dialog_ex">
				<div class="g_dialog_body">
					<p class="s_section">
						<span class="s_section_left">1：第一阶段 </span>
						<span>
								<!--<i :class="release_status > 0?'el-icon-circle-check':'el-icon-loading'" style="color:#42b983"></i>-->
								<i v-if="release_status < 1?true:false" class="el-icon-loading"></i>
								<i v-if="release_status > 0?true:false" class='el-icon-circle-check' style="color:#42b983"></i>
							</span>
					</p>

					<p class="s_section">
						<span class="s_section_left">2：第二阶段 </span>
						<span>
								<!--<i :class="release_status > 1?'el-icon-circle-check':'el-icon-loading'" style="color:#42b983"></i>-->
								<i v-if="release_status < 2?true:false" class="el-icon-loading"></i>
								<i v-if="release_status > 1?true:false" class='el-icon-circle-check' style="color:#42b983"></i>
							</span>
					</p>

					<p class="s_section">
						<span class="s_section_left">3：第三阶段 </span>
						<span>
								<!--<i :class="release_status > 2?'el-icon-circle-check':'el-icon-loading'" style="color:#42b983"></i>-->
								<i v-if="release_status < 3?true:false" class="el-icon-loading"></i>
								<i v-if="release_status > 2?true:false" class='el-icon-circle-check' style="color:#42b983"></i>
							</span>
					</p>

					<p class="s_section">
						<span class="s_section_left">4：第四阶段 </span>
						<span>
								<!--<i :class="release_status > 3?'el-icon-circle-check':'el-icon-loading'" style="color:#42b983"></i>-->
								<i v-if="release_status < 4?true:false" class="el-icon-loading"></i>
								<i v-if="release_status > 3?true:false" class='el-icon-circle-check' style="color:#42b983"></i>
							</span>
					</p>

				</div>
			</div>
		</div>

		<div class="" v-show="szPointer=='Deblocking'">
			<div class="g_dialog g_dialog_ex">
				<div class="g_dialog_body">
					<p class="s_section">
						<span class="s_section_left">类型</span>
						<el-select class="s_section_right" v-model="KeyType" placeholder="请选择解锁的数据类型" size='small' @change="OnUploadLockType()">
							<el-option v-for="item in delock_type" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
					</p>

					<p class="s_section">
						<span class="s_section_left">解锁范围</span>
						<el-checkbox-group class="s_section_right s_section_checkbox" v-model="UnlockRange" placeholder="请选择解锁的数据范围">
							<el-checkbox v-for="(item,index) in checkedList" :key="index" :label="item" :value="item" disabled></el-checkbox>
						</el-checkbox-group>
					</p>

					<div class="s_section" style="" v-loading.fullscreen.lock="fullscreenLoading3" element-loading-text="正在上传中,请稍等... ...">
						<el-upload :action='deblocking_Ip' :data="DeblickingData" :on-success="unlock_success" :disabled="Deblocking_disabled" class="upload_box" :before-upload="unlock_upload" :show-file-list="file_flag">
							<el-button class="lead_btn" type="primary" @click="unlock_click"><i class="el-icon-caret-bottom"> 导入</i></el-button>
						</el-upload>
					</div>
					<div style="margin-top: 100px;padding-left: 74px;font-size: 17px;line-height: 36px;">
						注意事项:<br>
					</div>
					<div style="padding-left: 74px;font-size: 15px;">
						<p class="padding_p1">1. 请使用标准模板进行解锁/加锁的导入操作，
							<a href="ftp://chaiyu:111111Aa@192.168.0.3/user/spider/unlock/block_sample.xlsx" download="block_sample.xlsx">点击下载模板</a>
						</p>
						<p class="padding_p1">2. 在模板中共有2列，第一列为ID，第二列为O的内容将进行加锁操作，为空白的将进行解锁操作</p>
						<p class="padding_p1">3. 为了避免O符号识别错误，一切字符请使用模版内的字符进行拷贝操作，不要自己随意写入</p>
						<p class="padding_p1">4. HU要件定义，TAGL要件定义，TAGL要件分析都使用同一份模板</p>
					</div>
				</div>
			</div>
		</div>
		<div class="white_list" v-show="szPointer=='whitelist'">
			<div class="g_dialog g_dialog_ex">
				<div class="g_dialog_body">
					<p class="s_section">
						<span class="s_section_left">白名单</span>
						<el-select class="s_section_right" v-model="whiteType" placeholder="请选择提交范围" size='small' @change="selectWhiteType()">
							<el-option v-for="(item,index) in delock_type" :key="item.classify" :label="item.label" :value="item"></el-option>
						</el-select>
					</p>

					<div class="s_section">
						<el-upload :action='whitelist_ip' :data="whitelist_msg" :on-success="white_upload_success" :disabled="Deblocking_disabled" class="upload_box" :before-upload="whiteBefore_upload" :show-file-list="file_flag">
							<el-button class="lead_btn" type="primary" @click="submit_click()"><i class="el-icon-caret-bottom"> 提交</i>
							</el-button>
						</el-upload>
					</div>

					<div style="width:1040px;" class="table_tr_down">
						<el-table :data="show_white" border="" maxHeight="650" @selection-change="handleSelectionChange">
							<el-table-column type="selection" min-width='100' align="center">

							</el-table-column>
							<el-table-column prop="import_user" label="上傳人" min-width='180' align="center" sortable :filters="ArrayWhiteUserList" :filter-method="filterName" filter-placement="bottom-end">
							</el-table-column>
							<el-table-column prop="id" label="ID" width='380' align="center" sortable>
							</el-table-column>
							<el-table-column prop="import_time" label="提交日期" min-width='180' align="center" sortable>
							</el-table-column>
							<el-table-column prop="agree" label="审批操作" min-width='180' align="center" v-if="this.Roles=='PL'||this.Roles=='Admin'?true:false">
								<template scope="scope">
									<el-button type="text" @click="whitePass(scope.$index,scope.row)" size="small"><i class="el-icon-circle-check" style="font-style: normal">确认</i></el-button>
									<el-button type="text" @click="whiteFail(scope.$index,scope.row)" size="small" :class="{red_active:scope.row.agree==0}"><i class="el-icon-circle-cross">拒绝</i></el-button>
									<!--<el-checkbox-group v-model="checkbox_groupModel" @change="checkedKeyChange">-->
									<!--<el-checkbox v-for="" :label="city" :key="city">{{}}</el-checkbox>-->
									<!--</el-checkbox-group>-->
									<!--<el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @chang="checkAllChange"><全选></全选></el-checkbox>-->
								</template>
							</el-table-column>
						</el-table>
						<div style="height: 50px;">
							<el-button type="primary" class="white_list_btn" @click="submit_check()" v-if="this.Roles=='PL'||this.Roles=='Admin'?true:false"><i class="el-icon-caret-bottom">白名单确认</i>
							</el-button>
							<el-button type="primary" class="white_list_btn" @click="submit_refuse_check()" v-if="this.Roles=='PL'||this.Roles=='Admin'?true:false"><i class="el-icon-caret-bottom">白名单拒绝</i>
							</el-button>
						</div>

					</div>
				</div>
				<div class="text_note_p">
					<p>注意事项:</p>
					<p class="padding_p1">1. 请使用标准模板进行导入操作，
						<a href="ftp://chaiyu:111111Aa@192.168.0.3/user/spider/white_list/white_list.zip" download="white_list.zip">点击下载模板</a>
					</p>
					<p class="padding_p1">2. 为了避免识别错误，一切字符请使用模版内的字符进行拷贝操作，不要自己随意写入</p>
					<p class="padding_p1">3. HU要件定义，TAGL要件定义，TAGL要件分析请使用对应的模板进行导入</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'ImportExport',
		data() {
			return {
				ReleaseUploadTime: '',
				array_pre_version_data: [],
				ArrayWhiteUserList: [],
				Array_Submit: [],
				UnlockRange: [],
				checkedList: ['向上解锁', '向下解锁'],
				release_PostArray: {
					"version": "",
					"date": "",
					"pre_version": "",
					"user_id": window.sessionStorage.getItem('admin'),
					'tmc_issue': '',
					'suntec_confirm': '',
					'blocklist': ''
				},
				array_pre_version: [],
				release_status: 0,
				Roles: '',
				file_flag: false,
				type: [{
						value: 'ARL_Schedule',
						label: '要求式样'
					},
					{
						value: 'HU_Definition',
						label: '机能式样'
					},
					{
						value: 'TAGL_Definition',
						label: '要件定義'
					},
					{
						value: 'TAGL_Analysis',
						label: '要件分析'
					},
					{
						value: 'Checklist',
						label: 'Checklist'
					},
				],
				//			    msg: {"type":"","user_id":window.sessionStorage.getItem('admin')},
				msg: {},
				DeblickingData: {
					"type": "",
					"user_id": window.sessionStorage.getItem('admin'),
					"up": "no",
					"down": "no"
				},
				typeindex: '',
				lead_typeindex: "",
				KeyType: "",
				lead_type: [{
						value: 'ARL',
						label: 'ARL'
					},
					{
						value: 'ARL_Schedule',
						label: '要求式样'
					},
					{
						value: 'HU_DEF',
						label: '机能式样'
					},
					{
						value: 'TAGL_DEF',
						label: '要件定義'
					},
					{
						value: 'TAGL_ANA',
						label: '要件分析'
					},
				],
				delock_type: [{
						value: 'HU_DEF',
						label: '机能式样',
						classify: 'HU'
					},
					{
						value: 'TAGL_DEF',
						label: '要件定義',
						classify: 'DEF'
					},
					{
						value: 'TAGL_ANA',
						label: '要件分析',
						classify: 'ANA'
					},
				],
				scope: [{
						value: 'Mine',
						label: '我的'
					},
					{
						value: 'All',
						label: '全部'
					},
					{
						value: 'MyGroup',
						label: '我的组'
					}
				],
				scopeindex: '',

				category: [{
					value: 'All',
					label: '全部'
				}],
				categoryindex: '',

				bScreenLockFlag: false,
				bCategoryDisplay: false,

				szPointer: '',
				szLoadingMsg: 'haha',

				cLoading: null,
				lead_disabled: true,
				lead_disabled2: true,
				Deblocking_disabled: true,
				user_id: window.sessionStorage.getItem('admin'),

				upload_flag: false,
				fullscreenLoading: false,
				fullscreenLoading2: false,
				fullscreenLoading3: false,

				lead_Ip: this.Ip + '/ImportFromWeb',
				//        新加
				pickerOptions: {
					shortcuts: [{
						text: "最近24小时",
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24);
							picker.$emit('pick', [start, end])
						}
					}, {
						text: "最近两天",
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 2);
							picker.$emit('pick', [start, end])
						}
					}, {
						text: "最近三天",
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 3);
							picker.$emit('pick', [start, end])
						}
					}, {
						text: "最近一周",
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
							picker.$emit('pick', [start, end])
						}
					}]
				},
				time_value: "",
				checkType: [{
						value: '○',
						label: '○'
					},
					{
						value: '△',
						label: '△'
					},
					{
						value: '-',
						label: '-'
					}
				],
				checklist_flag: true,
				tableDisplay: false,
				ImportDisabled: false,
				checkTime_flag: false,
				check_flag: false,
				lead_type2: [],
				lead_typeindex2: "",
				lead_Ip2: this.Ip + '/ImportFile',
				whitelist_ip: this.Ip + '/ImportWhitelist',
				group_name: '',
				group_id: '',
				show_file: [],
				show_white: [],
				show_check: [],
				check_result: '',
				whiteType: '',
				msg2: {
					"type": "",
					"user_id": window.sessionStorage.getItem('admin'),
					"group_name": "",
					"group_id": "",
				},
				whitelist_msg: {
					"user_id": window.sessionStorage.getItem('admin'),
					"type": ''
				},
				deblocking_Ip: this.Ip + '/' + 'ImportBlock'
			}
		},
		computed: {
			getReleaseType() {
				return this.$store.state.release_type
			}
		},
		watch: {
			getReleaseType(val) {
				if(val == 'Release') {
					this.$axios.get(this.Ip + '/Release')
						.then(res => {
							if(res.data.result == 'NG') {
								this.array_pre_version = []
							} else {
								this.array_pre_version = res.data.release_list
							}
						})
					this.$axios.get(this.Ip + '/ReleaseVersion')
						.then(res => {
							if(res.data.result == 'NG') {
								this.array_pre_version_data = []
							} else {
								this.array_pre_version_data = res.data.release_list
							}
						})
				}
				this.szPointer = val
			}
		},
		mounted: function() {
			this.Roles = window.sessionStorage.getItem('Roles')
			this.release_PostArray.date = this.formatDate()
			if(this.$store.state.release_type == '') {
				this.szPointer = window.sessionStorage.getItem('release', this.szPointer)
			} else {
				this.szPointer = this.$store.state.release_type
				window.sessionStorage.setItem('release', this.szPointer)
			}
			if(this.szPointer == 'Release') {
				this.$axios.get(this.Ip + '/Release')
					.then(res => {
						if(res.data.result == 'NG') {
							this.array_pre_version = []
						} else {
							this.array_pre_version = res.data.release_list
						}
					})
				this.$axios.get(this.Ip + '/ReleaseVersion')
					.then(res => {
						if(res.data.result == 'NG') {
							this.array_pre_version_data = []
						} else {
							this.array_pre_version_data = res.data.release_list
						}
					})
			}

			window.sessionStorage.setItem('release', this.szPointer)
			this.$axios.get(
					this.Ip + '/UserContent/' + window.sessionStorage.getItem('admin')
				)
				.then(res => {
					this.p_list = res.data.content;
					this.U_id = this.p_list.user_id;
				})
			// new ADD请求用户所有的组（ASTA文件上传）
			this.permission = window.sessionStorage.getItem('admin' || 'PL');
			if(window.sessionStorage.getItem('Roles') == 'PL') {
				this.$axios.get(this.Ip + '/GpGroupDetail').then(res => {
					if(res.data.result = true) {
						let arr = []
						for(let i = 0; i < res.data.length; i++) {
							arr.push({
								'value': res.data[i].group_name,
								'group_name': res.data[i].group_name,
								'group_id': res.data[i].group_id
							})
						}
						this.lead_type2 = arr;
					}
				})
			} else {
				this.$axios.get(
					this.Ip + "/UserMyGroup" + "/" + window.sessionStorage.getItem('admin')
				).then(res => {
					if(res.data.result = true) {
						let arr = []
						for(let i = 0; i < res.data.length; i++) {
							arr.push({
								'value': res.data[i].group_name,
								'group_name': res.data[i].group_name,
								'group_id': res.data[i].group_id
							})
						}
						this.lead_type2 = arr;
					}
				}).catch(Error => {
					console.log(Error);
				})
			}
		},
		methods: {
			filterName(value, row) {
				return row.import_user === value
			},
			handleSelectionChange(val) {
				this.Array_Submit = val
			},
			submit_check() {
				if(this.Array_Submit.length == 0) {
					this.$message({
						type: "error",
						message: "请选择条目"
					});
					return;
				}

				let arr2 = [];
				for(let i = 0; i < this.Array_Submit.length; i++) {
					arr2.push({
						"classify": this.Array_Submit[i].classify,
						"id": this.Array_Submit[i].id,
						"agree": 1
					});
				};

				let whiteData = {
					"user_id": this.user_id,
					"white_list": arr2
				};
				this.$axios.post(this.Ip + "/WhiteList", whiteData).then(res => {
					if(res.data.result == "OK") {
						this.$message({
							type: "success",
							message: "审批通过"
						});
						this.Array_Submit = []
						this.selectWhiteType();
					}
				})
			},
			submit_refuse_check() {
				if(this.Array_Submit.length == 0) {
					this.$message({
						type: "error",
						message: "请选择条目"
					});
					return;
				}

				let arr2 = [];
				for(let i = 0; i < this.Array_Submit.length; i++) {
					arr2.push({
						"classify": this.Array_Submit[i].classify,
						"id": this.Array_Submit[i].id,
						"agree": 0
					});
				};

				let whiteData = {
					"user_id": this.user_id,
					"white_list": arr2
				};
				this.$axios.post(this.Ip + "/WhiteList", whiteData).then(res => {
					if(res.data.result == "OK") {
						this.$message({
							type: "success",
							message: "审批通过"
						});
						this.Array_Submit = []
						this.selectWhiteType();
					}
				})
			},
			formatDate() {
				var date = new Date();
				var y = date.getFullYear();
				var m = date.getMonth() + 1;
				m = m < 10 ? '0' + m : m;
				var d = date.getDate();
				d = d < 10 ? ('0' + d) : d;
				return y + '-' + m + '-' + d;
			},
			OnImport() {
				this.szPointer = 'Import';
			},
			OnImportARL() {
				this.szPointer = 'ARLImport';
			},
			OnExport() {
				this.szPointer = 'Export';
			},
//			OnCheckRule() {
//				this.szPointer = 'CheckRule';
//				this.$router.push('/homepage/mywork/CheckRule_HU');
//			},
			selectType() {
				if(this.typeindex == 'Checklist') {
					this.checklist_flag = false;
					this.checkTime_flag = true;
					this.bCategoryDisplay = false;
				} else {
					this.checklist_flag = true;
					this.checkTime_flag = false;
					if(this.scopeindex === "All") {
						this.bCategoryDisplay = true;
					} else {
						this.bCategoryDisplay = false;
					}
				}
			},
			OnScope() {
				if(this.scopeindex == "All") {
					this.bCategoryDisplay = true;
				} else {
					this.bCategoryDisplay = false;
				}
			},
			TryExport(szAddress) {
				this.$axios.get(this.Ip + szAddress).then(res => {
						if(res.data.result == "WAITING") {
							setTimeout(this.TryExport(res.data.datapath), 1000);
						} else if(res.data.result == 'NODATA') {
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
							this.$notify({
								type: 'error',
								message: '无数据'
							});
						} else {
							this.$notify({
								type: 'success',
								message: '导出成功'
							});
							window.location.href = this.Ip + res.data.datapath;
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
						}
					})
					.catch(err => {
						if(err.response) {
							// 服务器返回正常的异常
							this.$notify({
								type: 'error',
								message: '服务器异常: ' + err.response.status,
								showClose: true,
								duration: '0',
							});
						} else {
							// 服务器发生未处理的异常
							this.$notify({
								type: 'error',
								message: '服务器未知异常',
								showClose: true,
								duration: '0',
							});
						}

						this.bScreenLockFlag = false;

						if(this.cLoading != null) {
							this.cLoading.close();
						}
					});
			},
			OnDoExport() {
				var szTypeInfo = '';
				switch(this.typeindex) {

					case 'ARL_Schedule':
						szTypeInfo = 'ARL';
						break;

					case 'HU_Definition':
						szTypeInfo = 'HU_DEF';
						break;

					case 'TAGL_Definition':
						szTypeInfo = 'TAGL_DEF';
						break;

					case 'TAGL_Analysis':
						szTypeInfo = 'TAGL_ANA';
						break;
					case 'checklist':
						szTypeInfo = 'checklist';
						break;
				}

				var szScopeInfo = '';
				switch(this.scopeindex) {
					case 'All':
						szScopeInfo = 'All';
						break;

					case 'Mine':
						szScopeInfo = 'User';
						break;

					case 'MyGroup':
						szScopeInfo = 'Group';
						break;
				}

				if(this.typeindex == '') {
					this.$notify({
						iconClass: 'message_icon_info',
						message: '请选择类型',
					});
				} else {
					if(szTypeInfo != 'Checklist') {
						console.log("1")
						if(this.scopeindex == '') {
							this.$notify({
								iconClass: 'message_icon_info',
								message: '请选择范围',
							});
						} else {
							var szAddress = this.Ip + '/Export/' + szTypeInfo + '/' + szScopeInfo + '/' + this.U_id + '/' + Date.now();
							this.bScreenLockFlag = true;
							this.$axios.get(szAddress).then(res => {
									var szLoadingText = '导出中，请耐心等待';
									if(this.scopeindex == 'All') {
										szLoadingText = '大约需要2分钟左右，请耐心等待';
									}
									this.cLoading = this.$loading({
										lock: true,
										fullscreen: true,
										text: szLoadingText
									});
									setTimeout(this.TryExport(res.data.datapath), 1000);
								})
								.catch(err => {
									this.bScreenLockFlag = false;
									this.cLoading.close();
									if(err.response) {
										// 服务器返回正常的异常
										this.$notify({
											type: 'error',
											message: '服务器异常: ' + err.response.status,
											showClose: true,
											duration: '0',
										});
									} else {
										// 服务器发生未处理的异常
										this.$notify({
											type: 'error',
											message: '服务器未知异常',
											showClose: true,
											duration: '0',
										});
									}
									this.bScreenLockFlag = false
								});
						}
					} else {
						if(this.time_value == '') {
							this.$notify({
								iconClass: 'message_icon_info',
								message: '请选择时间',
							});
						} else {
//						  console.log("123")
							let dateTime = this.time_value;
							Date.prototype.Format = function(fmt) { //格式化时间戳方法
								var o = {
									"M+": this.getMonth() + 1, //月份
									"d+": this.getDate(), //日
									"h+": this.getHours(), //小时
									"m+": this.getMinutes(), //分
									"s+": this.getSeconds(), //秒
									"q+": Math.floor((this.getMonth() + 3) / 3), //季度
									"S": this.getMilliseconds() //毫秒
								};
								if(/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
								for(var k in o)
									if(new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
								return fmt;
							};
							let szLoadingText = '正在导出中，请耐心等待';
							this.cLoading = this.$loading({
								lock: true,
								fullscreen: true,
								text: szLoadingText
							});
							const dateStart = dateTime[0].Format("yyyy-MM-dd hh:mm:ss"),
								dateEnd = dateTime[1].Format("yyyy-MM-dd hh:mm:ss");
							let address = this.Ip + "/ExportChecklist/" + dateStart + '/' + dateEnd;
//							alert("11")
							this.$axios.get(address).then(res => {
							  console.log(res)
								let ipd = res.data.file_path.substring(1);
//							  console.log(ipd,"ipd")
								window.location.href = this.Ip + "/DownloadChecklist" + ipd;
								if(res.data.result == "OK") {
									setTimeout(() => {
										if(this.cLoading != null) {
											this.bScreenLockFlag = false;
											this.cLoading.close();
										}
									}, 200)
								}
							}).catch(err => {
								if(err.result == "NG") {
									this.bScreenLockFlag = false;
									this.cLoading.close();
									this.$notify({
										type: 'error',
										message: '服务器异常:' + err.message,
										showClose: true,
										duration: '0',
									});
								}
							});
						}
					}
				};
			},
			lead_success(response, file, fileList) {
				this.fullscreenLoading2 = false;
				this.upload_flag = false
				if(response.result == 1) {

					this.$notify({
						type: 'error',
						message: '服务器异常: ' + response.error_list,
						showClose: true,
						duration: '0',
					});
				} else {
					this.$notify({
						type: 'success',
						message: '上传成功',
						showClose: true,
						duration: '0',
					})
				}
			},
			unlock_success(response, file, fileList) {
				this.fullscreenLoading3 = false;
				this.upload_flag = false
				if(response.result == 1) {
					this.$notify({
						type: 'error',
						message: '服务器异常: ' + response.error_list,
						showClose: true,
						duration: '0',
					});
				} else {
					this.$notify({
						type: 'success',
						message: '上传成功,更新了' + response.update_count + '条数据',
						showClose: true,
						duration: '0',
					})
				}
			},
			OnUploadLockType() {
				this.DeblickingData.type = this.KeyType
				if(this.KeyType != "") {
					this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG') {
								this.Deblocking_disabled = true
							}
							return
						})
					this.Deblocking_disabled = false
				}

			},
			OnleadScope() {
				if(this.lead_typeindex != "") {
					this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG') {
								this.lead_disabled = true
								return
							}
						})
					this.lead_disabled = false
				}

				if(this.lead_typeindex == 'ARL_Schedule') {
					this.msg = {
						"user_id": window.sessionStorage.getItem('admin')
					}
					this.lead_Ip = this.Ip + '/' + 'ImportSchedule'
					this.tableDisplay = false;
					this.ImportDisabled = false;
					this.check_flag = false;
				} else if(this.lead_typeindex == 'ARL') {
					this.msg = {
						"user_id": window.sessionStorage.getItem('admin')
					}
					this.lead_Ip = this.Ip + '/' + 'ImportArl'
					this.tableDisplay = false;
					this.ImportDisabled = false;
					this.check_flag = false;
				} else {
					this.lead_disabled = true,
						this.msg = {
							"type": "",
							"user_id": window.sessionStorage.getItem('admin'),
							"check_list": ''
						},
						this.lead_Ip = this.Ip + '/' + 'ImportFromWeb',
						this.msg.type = this.lead_typeindex;
					if(this.lead_typeindex == 'HU_DEF') {
						this.tableDisplay = true;
						this.ImportDisabled = true;
						this.check_flag = true;
						let type = 'hu';
						this.$axios.get(this.Ip + '/CheckContent/' + type).then(res => {
							this.show_check = [];
							let data = res.data.hu_check_list;
							for(let i = 0; i < data.length; i++) {
								data[i].check_result = "";
							}
							this.show_check = data;
						});
					} else if(this.lead_typeindex == 'TAGL_DEF') {
						this.tableDisplay = true;
						this.ImportDisabled = true;
						this.check_flag = true;
						let type = 'definition';
						this.$axios.get(this.Ip + '/CheckContent/' + type).then(res => {
							this.show_check = [];
							let data = res.data.definition_check_list;
							for(let i = 0; i < data.length; i++) {
								data[i].check_result = "";
							}
							this.show_check = data;
						})
					} else if(this.lead_typeindex == 'TAGL_ANA') {
						this.tableDisplay = true;
						this.ImportDisabled = true;
						this.check_flag = true;
						let type = 'analysis';
						this.$axios.get(this.Ip + '/CheckContent/' + type).then(res => {
							this.show_check = [];
							let data = res.data.analysis_check_list;
							for(let i = 0; i < data.length; i++) {
								data[i].check_result = "";
							}
							this.show_check = data;
						})
					}
				}
			},
			lead_click() {
				if(this.lead_typeindex == "") {
					this.$notify({
						iconClass: 'message_icon_info',
						message: '请选择类型',
					});
				} else {
					this.msg.check_list = JSON.stringify(this.show_check);
					this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG') {
								this.$notify({
									type: 'error',
									message: '其他人正在release，请耐心等待!',
									showClose: true,
									duration: '0',
								})
								this.lead_disabled = true
								return
							}
						})
					this.upload_flag = true;
					let flag = false;
					for(let i = 0; i < this.show_check.length; i++) {
						if(this.show_check[i].check_result == '') {
							flag = true;
						}
					}
					if(flag == false) {
						this.lead_disabled = false;
						this.check_flag = false;
						if(this.check_flag = false) {
							this.$notify({
								type: 'success',
								message: "确认完毕"
							})

						}
					} else {
						this.$notify({
							type: 'error',
							message: "请检查表格是否已全选"
						})
					}
				}
			},

			unlock_click() {
				this.DeblickingData.up = 'no'
				this.DeblickingData.down = 'no'
				for(let i = 0; i < this.UnlockRange.length; i++) {
					if(this.UnlockRange[i] == '向上解锁') {
						this.DeblickingData.up = 'yes'
					}
					if(this.UnlockRange[i] == '向下解锁') {
						this.DeblickingData.down = 'yes'
					}
				}

				if(this.KeyType == "") {
					this.$notify({
						iconClass: 'message_icon_info',
						message: '请选择类型',
					});
				} else {
					this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG') {
								this.$notify({
									type: 'error',
									message: '其他人正在release，请耐心等待!',
									showClose: true,
									duration: '0',
								})
								return;
							}
						})
					for(let i = 0; i < this.UnlockRange.length; i++) {
						this.DeblickingData.up = 'no'
						this.DeblickingData.down = 'no'
						if(this.UnlockRange[i] == '向上解锁') {
							this.DeblickingData.up = 'yes'
						} else if(this.UnlockRange[i] == '向下解锁') {
							this.DeblickingData.down = 'yes'
						}
					}
					this.upload_flag = true;
				}

			},
			upload() {
				if(this.lead_typeindex == "") {
					this.$notify({
						iconClass: 'message_icon_info',
						message: '请选择类型',
					});
					return;
				} else {
					this.fullscreenLoading2 = true;
				}
			},
			unlock_upload() {
				if(this.KeyType == "") {
					this.$notify({
						iconClass: 'message_icon_info',
						message: '请选择类型',
					});
				} else {
					this.fullscreenLoading3 = true;
				}
			},
			setDate(val) {
				this.release_PostArray.date = val
				this.ReleaseUploadTime = val
			},
			OnDoRelease() {
				//				if(this.release_PostArray.tmc_issue == ''){
				//					this.$notify({
				//							type:'error',
				//							message:'TMC 最新指摘不能为空',
				//							showClose:true,
				//							duration:'0',
				//						})
				//					return;
				//				}else
				this.release_PostArray.date = this.ReleaseUploadTime
				if(this.release_PostArray.suntec_confirm == '') {
					this.$notify({
						type: 'error',
						message: 'Suntec 最新回答不能为空',
						showClose: true,
						duration: '0',
					})
					return;
				} else if(this.release_PostArray.blocklist == '') {
					this.$notify({
						type: 'error',
						message: 'blocklist不能为空',
						showClose: true,
						duration: '0',
					})
					return;
				} else if(this.release_PostArray.version == '') {
					this.$notify({
						type: 'error',
						message: '当前版本号不能为空',
						showClose: true,
						duration: '0',
					})
					return;
				} else {

				}

				if(this.array_pre_version.toString() != [].toString()) {
					if(this.release_PostArray.pre_version == '') {
						this.$notify({
							type: 'error',
							message: '前一版本号不能为空',
							showClose: true,
							duration: '0',
						})
						return;
					}
				}
				this.$axios.get(this.Ip + '/ServiceStatus')
					.then(res => {
						if(res.data.result == 'NG') {
							this.$notify({
								type: 'error',
								message: '其他人正在release，请耐心等待!',
								showClose: true,
								duration: '0',
							})
							return;
						} else {
							let szLoadingText = 'release中，请耐心等待';
							this.cLoading = this.$loading({
								lock: true,
								fullscreen: true,
								text: szLoadingText
							});

							this.$axios.post('http://192.168.0.95:5000/Release', this.release_PostArray)
								.then(res => {
									if(res.data.result == 'NG') {
										this.$notify({
											type: 'error',
											message: res.data.error,
											showClose: true,
											duration: '0',
										})
									} else {

									}
									if(res.data.attach_file != '') {
										window.location.href = 'http://192.168.0.95:5000/DownloadRelease/' + res.data.attach_file
									}
									this.$axios.get(this.Ip + '/Release')
										.then(res => {
											if(res.data.result == 'NG') {
												this.array_pre_version = []
											} else {
												this.array_pre_version = res.data.release_list
											}
										})
									this.$axios.get(this.Ip + '/ReleaseVersion')
										.then(res => {
											if(res.data.result == 'NG') {
												this.array_pre_version_data = []
											} else {
												this.array_pre_version_data = res.data.release_list
											}
										})
									this.release_PostArray.version = ''
									this.release_PostArray.pre_version = ''
									this.cLoading.close()
									//								this.szPointer = 'Releasing'
									//								var timer = setInterval(() => {
									//									if(this.release_status == 50){
									//										clearInterval(arguments.callee.caller)
									//										this.szPointer = 'Release'
									//										this.release_status = 0
									//									}
									//									this.release_status ++;
									//								},1000)
								})

								.catch(res => {
									this.cLoading.close()
									this.$notify({
										type: 'error',
										message: '网络异常，请重新刷新',
										showClose: true,
										duration: '0',
									})
								})
						}
					})

			},
			OnRelease() {
				this.$axios.get(this.Ip + '/Release')
					.then(res => {
						if(res.data.result == 'NG') {
							this.array_pre_version = []
						} else {
							this.array_pre_version = res.data.release_list
						}
					})
				this.$axios.get(this.Ip + '/ReleaseVersion')
					.then(res => {
						if(res.data.result == 'NG') {
							this.array_pre_version_data = []
						} else {
							this.array_pre_version_data = res.data.release_list
						}
					})
				this.szPointer = 'Release'
			},
			OnUnlock() {
				this.szPointer = 'Deblocking'
			},
			//新加函数
			OnImport2() {
				this.szPointer = 'Import2';
			},
			//select组
			OnleadScope2() {
				if(this.lead_typeindex2 === "") {
					this.$message({
						iconClass: 'message_icon_info',
						message: '请选择用户组',
					});
				} else {
					this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG') {
								this.lead_disabled2 = true;
								return;
							}
						})
					this.msg2.group_name = this.lead_type2[this.lead_typeindex2].group_name;
					this.msg2.group_id = this.lead_type2[this.lead_typeindex2].group_id;
					this.lead_disabled2 = false;
					this.show_file = [];
					this.$axios.get(this.Ip + "/GetFileList/" + this.msg2.group_id).then(res => {
						this.show_file = res.data;
					})
				}

			},
			lead_click2() {

				if(this.lead_typeindex2 === "") {
					this.$message({
						iconClass: 'message_icon_info',
						message: '请选择用户组',
					});

				} else {
					this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG') {
								this.$message({
									type: 'error',
									message: '其他人正在release，请耐心等待!',
									showClose: true,
									duration: '0',
								})
								return;
							}
						})
					this.upload_flag = true;
				}
			},
			upload2(file) {
				let index1 = file.name.lastIndexOf("."),
					index2 = file.name.length,
					suffix = file.name.substring(index1, index2);
				const isASTA = suffix === ".asta";
				if(this.lead_typeindex2 === "") {
					this.$message({
						iconClass: 'message_icon_info',
						message: '请刷新页面',
					});
				} else {
					this.fullscreenLoading2 = true;
					if(!isASTA) {
						this.upload_flag = false;
						this.fullscreenLoading2 = false;
						this.$message.error("只能上传asta文件");
					}
					return isASTA;
				}
			},
			lead_success2(response, file, fileList) {
				this.fullscreenLoading2 = false;
				this.upload_flag = false;
				if(response.result == 'NG') {
					this.$message({
						type: 'error',
						message: "上传异常，错误代码：" + response.error + ",请联系管理员。",
						showClose: true,
						duration: '0',
					});
				} else {
					this.$message({
						type: 'success',
						message: '上传成功',
					});
					this.OnleadScope2(); //回调刷新ASTA文件列表
				}
			},
			downFile($index, row) { //下载文件
				window.location.href = this.Ip + "/DownLoad/" + row.record_id
			},
			Delete($index, row) {
				let rec_id = row.record_id;
				this.$confirm("是否删除？").then(() => {
					this.$axios.get(this.Ip + "/DeleteFile/" + rec_id).then(res => {
						if(res.data.result == "OK") {
							this.$message({
								type: "success",
								message: "删除成功"
							});
							this.OnleadScope2();
						} else if(res.data.result == "NG") {
							this.$message({
								type: "error",
								message: "服务器异常，删除失败，请联系管理员"
							});
						} else {};
					})
				})
			},
			OnDoExport2() { //仅PL权限全导出
				this.$axios.get(this.Ip + "/DowAllGroups").then(res => {
					window.location.href = this.Ip + "/DowAllGroups"
				})
			},
			//    new add whitelist
			OnWhiteList() {
				this.szPointer = 'whitelist';
			},
			submit_click() {
				if(this.whiteType == "") {
					this.$message({
						iconClass: 'message_icon_info',
						message: '请选择类型',
					});
				} else {
					this.$axios.get(this.Ip + '/ServiceStatus')
						.then(res => {
							if(res.data.result == 'NG') {
								this.$message({
									type: 'error',
									message: '其他人正在release，请耐心等待!',
									showClose: true,
									duration: '0',
								})
								return;
							}
						})
					this.upload_flag = true;
				}
			},
			selectWhiteType() {
				this.Deblocking_disabled = false;
				this.whitelist_msg.type = this.whiteType.value;
				this.$axios.get(this.Ip + "/WhiteList").then(res => {
					if(res.data.result == "OK") {
						let arr = [];
						for(let i = 0; i < res.data.white_list.length; i++) {
							if(res.data.white_list[i].classify == this.whiteType.classify && res.data.white_list[i].agree != 1) {
								arr.push(res.data.white_list[i]);
							}
						}
						this.show_white = [];
						this.show_white = arr;
						let WhiteUserList = []
						this.ArrayWhiteUserList = []
						for(let i = 0; i < this.show_white.length; i++) {
							if(WhiteUserList.indexOf(this.show_white[i].import_user) == -1) {
								WhiteUserList.push(this.show_white[i].import_user)
							}
						}
						for(let j = 0; j < WhiteUserList.length; j++) {
							this.ArrayWhiteUserList.push({
								text: WhiteUserList[j],
								value: WhiteUserList[j]
							})
						}
					} else {
						this.$message({
							type: 'error',
							message: response.error + '服务器访问失败,请联系管理员'
						})
					}
				})
			},
			whiteBefore_upload() {
				if(this.whiteType === "") {
					this.$message({
						iconClass: 'message_icon_info',
						message: '请选择类型',
					});
				}
			},
			white_upload_success(response, file, fileList) {
				this.fullscreenLoading2 = false;
				this.upload_flag = false;
				//        this.fullscreenLoading3 = false;
				if(response.result == 0) {
					this.$message({
						type: 'success',
						message: '上传成功,更新了' + response.update_count + "条信息,有" + response.repeat_count + "条重复信息",
						showClose: true,
						duration: '0',
					});
					this.selectWhiteType(); //回调刷新
				} else if(response.result == 1) {
					this.$message({
						type: 'error',
						message: '服务器异常: ' + response.error,
						showClose: true,
						duration: '0',
					});
				}
			},
			whitePass($index, row) {
				let arr = [],
					arr2 = [];
				for(let i in row) {
					arr.push(row[i])
				};
				arr2.push({
					"classify": arr[3],
					"id": arr[4],
					"agree": 1
				});

				let whiteData = {
					"user_id": this.user_id,
					"white_list": arr2
				};

				this.$axios.post(this.Ip + "/WhiteList", whiteData).then(res => {
					if(res.data.result == "OK") {
						this.$message({
							type: "success",
							message: "审批通过"
						});
						this.selectWhiteType();
					}
				})
			},
			whiteFail($index, row) {
				let arr = [],
					arr2 = [];
				for(let i in row) {
					arr.push(row[i])
				};
				arr2.push({
					"classify": arr[3],
					"id": arr[4],
					"agree": 0
				});
				let whiteData = {
					"user_id": this.user_id,
					"white_list": arr2
				};
				this.$axios.post(this.Ip + "/WhiteList", whiteData).then(res => {
					if(res.data.result == "OK") {
						this.$message({
							type: "error",
							message: "已拒绝"
						});
						this.selectWhiteType(); //回调刷新
					}
				})
			},
		}
	}
</script>

<style scoped>
	ul,
	li {
		margin: 0;
		padding: 0;
		list-style: none;
	}

	.g_page {
		position: absolute;
		top: 0;
		left: 0;
		height: 100%;
		width: 100%;
	}

	.g_page .s_page_left {
		padding-left: 45px;
		width: 300px;
		height: 100%;
		border-right: solid 1px #dfe6ec;
		margin-top: 20px;
		font-size: large;
		font-weight: bold;
		overflow-x: hidden;
		overflow: scroll;
		float: left;
	}

	.g_page .s_page_left li {
		list-style: none;
		line-height: 36px;
		cursor: pointer;
	}

	.g_page .s_page_right {
		/*float: left;
	width: 82%;*/
		/*margin-left:1%;*/
		position: absolute;
		left: 300px;
		right: 0;
		top: 0;
		height: 90%;
	}

	.g_page .s_text {
		width: 70%;
		top: 30%;
		text-align: center;
		color: red;
		font-size: x-large;
	}

	.g_dialog_shadow {
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, .3);
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: 2001;
	}

	.g_dialog {
		position: absolute;
		left: 300px;
		width: 600px;
		background: white;
		/*
    border-radius: 2px;
    -webkit-box-shadow: 0 1px 3px rgba(0,0,0,.3);
    box-shadow: 0 1px 3px rgba(0,0,0,.3);
*/
	}

	.g_dialog_ex {
		/*width: 22%;*/
	}

	.g_dialog_ex2 {
		width: 1000px;
	}

	.g_dialog_header {
		width: 100%;
		height: 45px;
		line-height: 45px;
		/*margin-bottom: 12px;*/
		font-size: 18px;
	}

	.g_dialog_header .s_section_left {
		float: left;
	}

	.g_dialog_header .s_section_right {
		float: right;
	}

	.g_dialog_header .s_close {
		font-size: 14px;
	}

	.g_dialog_body {
		font-size: 14px;
		/*
	border-top: 1px solid rgb(225,225,225);
    border-bottom : 1px solid rgb(225,225,225);
*/
	}

	.g_dialog_body .s_section {
		width: 100%;
		vertical-align: middle;
		margin: 15px 0;
		overflow: hidden;
	}

	.g_dialog_body .s_section .s_section_left {
		width: 20%;
		height: 45px;
		line-height: 45px;
		font-size: large;
		font-weight: bold;
		text-align: right;
		padding-right: 10px;
		display: inline-block;
		/*
    border: 1px solid #ccc;
*/
	}

	.g_dialog_body .s_section .s_section_release_left {
		width: 28%;
	}

	.g_dialog_body .s_section .s_section_right {
		width: 50%;
	}

	.g_dialog_body .s_section .s_section_checkbox {
		/*text-align: center;*/
		display: inline-block;
	}

	.g_dialog_body .s_section .s_buttom {
		margin-top: 10%;
		margin-left: 58%;
		border: 1px solid #ccc;
	}

	.g_dialog_body .s_section .s_buttom_ex {
		margin-left: 58%;
	}

	.g_dialog_footer {
		height: 36px;
		width: 100%;
		margin-top: 15px;
	}

	.g_dialog_footer .s_section_right,
	.s_confirmcancel {
		text-align: right;
	}

	.active {
		color: #42b983;
		font-weight: bold;
	}

	.file {
		position: relative;
		display: inline-block;
		background-color: #fff;
		border-radius: 4px;
		border: 1px solid #42b983;
		padding: 5px 9px;
		overflow: hidden;
		color: #42b983 !important;
		text-decoration: none;
		text-indent: 0;
		font-size: 12px;
		width: 300px;
		margin-left: 12%;
	}

	.file input {
		position: absolute;
		right: 0;
		top: 0;
		opacity: 0;
		width: 100%;
		height: 100%;
	}

	.lead_btn {
		text-align: normal;
		padding: 10px 15px;
		font-size: 14px;
		display: block;
		float: left;
		margin-left: 57.5%;
	}

	.white_list_btn {
		text-align: center;
		padding: 10px 15px;
		margin: 15px 0 15px 20px;
		font-size: 14px;
		display: block;
		float: right;
	}

	.lead_upload {
		float: left;
	}

	.upload_box {
		/*float: left;*/
	}
	/*新加css样式*/

	.g_dialog_body .s_section {
		width: 600px;
	}

	.g_dialog .right_menu fl {
		width: 1000px;
		/*min-width: 600px;*/
	}

	.el-table_1_column_2 .is-leaf {
		width: 600px;
	}

	.s_section_expro {
		margin-top: -55px;
		margin-left: 55px;
		padding-bottom: 15px;
	}

	.text_note {
		margin-top: 100px;
		padding-left: 70px;
		font-size: 17px;
		line-height: 36px;
	}

	.text_note_p {
		margin-top: 20px;
		margin-left: 2px;
		font-size: 15px;
	}

	.text_note_p>p:first-child {
		color: red;
		font-size: 17px;
	}

	.red_active {
		color: red;
	}
</style>
