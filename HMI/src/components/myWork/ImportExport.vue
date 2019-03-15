<template>
	<div class="g_page" v-loading.fullscreen.lock="fullscreenLoading" element-loading-text="正在保存中,请稍等... ...">
		<div class="s_page_left">
			<ul>
				<li :class="{'active': szPointer=='Import'}" @click="OnImport()">导入</li>
				<li :class="{'active': szPointer=='Export'}" @click="OnExport()">导出</li>
				<!--<li :class="{'active': szPointer=='CheckRule'}" @click="OnCheckRule()">检查规则</li>-->
				<!--new-->
			</ul>

		</div>

		<div class="" v-show="szPointer=='Import'">
			<!-- <i class="el-icon-warning"> 此功能暂时不对外开放</i> -->
			<div class="g_dialog g_dialog_ex">
				<div class="g_dialog_body">
					<p class="s_section">
						<span class="s_section_left">类型</span>
						<el-select class="s_section_right" v-model="lead_typeindex" placeholder="请选择导入的数据范围" size='small' @change="OnleadScope()">
							<el-option v-for="item in lead_type" :key="item.value" :label="item.label" :value="item.value"></el-option>
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
					<el-table ref="clomTable" :data="show_check" border="" maxHeight="470" @selection-change="handleSelectionChange">
						<el-table-column  type="selection" width="55">
						</el-table-column>
						<el-table-column prop="col_id" label="ID" min-width='50' align="center">
						</el-table-column>
						<el-table-column prop="col_name" label="列名" min-width='50' align="center">
						</el-table-column>
						<el-table-column prop="col_disp_name" label="列名" min-width='50' align="center">
						</el-table-column>
						
					</el-table>			
				</div>
				<div style="padding-left: 40px;font-size: 14px;margin-top: 25px" v-if="tableDisplay">注意：
					<p class="padding_p1">1.选择类型后，点击左上角的按钮即可全选　</p>
				</div>
				<!-- <div style="padding-left: 40px;font-size: 14px;margin-top: 25px" v-if="tableDisplay">
					<el-button @click="dalian()">
						点击选中78列以后
					</el-button>
				</div> -->

			</div>
		</div>
		<div class="" v-show="szPointer=='Export'">
			<div class="g_dialog g_dialog_ex">
				<div class="g_dialog_body">
					
					<p class="s_section">
						<span class="s_section_left">类型</span>
						<el-select class="s_section_right" v-model="export_type_one" placeholder="请选择导入的数据范围" size='small' @change="ChooseType()">
							<el-option v-for="item in export_type" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
					</p>

					<p class="s_section" v-if="export_flag == true">
						<span class="s_section_left">STEP</span>
						<el-select class="s_section_right" v-model="typeindex" multiple placeholder="请选择导出的数据类型" size='small' key="1">
							<el-option v-for="item in type" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
					</p>

					<p class="s_section" v-if="export_flag == true">
						<span class="s_section_left">负责人</span>
						<el-select class="s_section_right" v-model="scopeindex" multiple placeholder="请选择导出的数据范围" size='small' key="2">
							<el-option v-for="item in scope" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
					</p>

					<p class="s_section" v-if="export_flag2 == true">
						<span class="s_section_left">IT负责人</span>
						<el-select class="s_section_right" v-model="itscopeindex" multiple placeholder="请选择导出的数据范围" size='small' key="3">
							<el-option v-for="item in itscope" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
					</p>
					<div class="s_section">
						<el-button class="s_buttom" type="primary" @click="OnDoExport()"><i class="el-icon-caret-bottom"> 导出</i>
						</el-button>

						<!-- <el-button class="s_buttom" type="primary" @click="test()"><i class="el-icon-caret-bottom"> ceshi</i>
						</el-button> -->
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
	</div>
</template>

<script>
	export default {
		name: 'ImportExport',
		data() {
			return {
				ReleaseUploadTime: '',
				array_pre_version_data: [],
				Array_Submit: [],
				col_names:[],

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

				Roles: '',
				file_flag: false,
				type: [],
				//			    msg: {"type":"","user_id":window.sessionStorage.getItem('admin')},
				msg: {},

				typeindex: '',
				lead_typeindex: "",
				lead_type: [{
						value: 'Req',
						label: '要件详细'}
						,{
						value: 'InternalQA',
						label: '内部QA表'
						}
						,{
						value: 'ExternalQA',
						label: '外部QA表'
						}
						,{
						value: 'BugManage',
						label: 'Bug管理表'
						},
						{
						value: 'Hmiscreen',
						label: 'Screen画面'
						},
						{
						value: 'HmiScreenIt',
						label: '画面进入状况'
						},
						{
						value: 'HmiItResultModeTransition',
						label: '结合测试书'
						},
						{
						value: 'HmiItResultModeTransition2',
						label: '設計書导入'
						},
						{
						value: 'HmiItProgressReport',
						label: 'IT进度报告导入'
						},
						{
						value: 'ItProgressQA',
						label: 'ITQA表导入'
						}

				],
				export_type: [{
						value: 'Req',
						label: '要件详细'}
						,{
						value: 'InternalQA',
						label: '内部QA表'
						}
						,{
						value: 'ExternalQA',
						label: '外部QA表'
						}
						,{
						value: 'BugManage',
						label: 'Bug管理表'
						}
						,{
						value: 'ARLPLAN',
						label: 'ARL总体计划'
						}
						,{
						value: 'HMIScreen',
						label: 'Screen画面'
						}
						,{
						value: 'HMIScreenIt',
						label: '画面进入状况'
						},
						{
						value: 'HMIItScreen',
						label: '结合测试书'
						},
						{
						value: 'HmiItProgressReport',
						label: 'IT进度报告导出'
						},
						{
						value: 'ItProgressQA',
						label: 'ITQA表导出'
						}
						
				],
				export_type_one:'',
				export_flag:false,
				export_flag2:false,

				scope: [],
				scopeindex: '',

				itscope:[],
				itscopeindex: '',

				bScreenLockFlag: false,

				szPointer: '',

				cLoading: null,
				lead_disabled: true,
				user_id: window.sessionStorage.getItem('admin'),

				upload_flag: false,
				fullscreenLoading: false,
				fullscreenLoading2: false,

				lead_Ip: this.Ip + '/HmiImport',
				//        新加
				tableDisplay: false,
				ImportDisabled: false,
				check_flag: false,
				group_name: '',
				group_id: '',
				show_check: [],
				whiteType: '',
				msg2: {
					"type": "",
					"user_id": window.sessionStorage.getItem('admin'),
					"group_name": "",
					"group_id": "",
				},
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
			this.getstep()
			this.getuser()
			this.getAuthor()

			this.Roles = window.sessionStorage.getItem('Roles')
			this.release_PostArray.date = this.formatDate()
			if(this.$store.state.release_type == '') {
				this.szPointer = window.sessionStorage.getItem('release', this.szPointer)
			} else {
				this.szPointer = this.$store.state.release_type
				window.sessionStorage.setItem('release', this.szPointer)
			}	
		},
		updated(){
			// if(this.tableDisplay == true){
			// 	this.dalian()
			// }else{

			// }
			
		},
		methods: {
			filterName(value, row) {
				return row.import_user === value
			},
			handleSelectionChange(val) {
				this.Array_Submit = val;
				this.col_names = [];
				for(var i=0;i<this.Array_Submit.length;i++){
					this.col_names.push(this.Array_Submit[i].col_name)
				}
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
			OnExport() {
				this.szPointer = 'Export';
			},
			test(){
				this.$axios.post(this.Ip + '/HmiExport',{"step":this.typeindex,"user":this.scopeindex})
				.then(res=>{
					// console.log(res,"..")
				})
				// console.log(this.typeindex,"t",this.scopeindex,"s")
			},
			getstep() {
				this.$axios.get(this.Ip + '/HmiSteps')
				.then(res=>{
					if(res.data.result =="OK"){
						for(var i=0;i<res.data.content.length;i++){
							var typeone = {};
							typeone.value = res.data.content[i];
							typeone.label = res.data.content[i];
							this.type.push(typeone);
						}
						// console.log(this.type,"step")
					}

				})
			},
			getuser() {
				this.$axios.get(this.Ip + '/HmiChargers')
				.then(res=>{
					if(res.data.result =="OK"){
						for(var i=0;i<res.data.content.length;i++){
							var typeone = {}
							typeone.value = res.data.content[i]
							typeone.label = res.data.content[i]
							this.scope.push(typeone)
						}
						var empty = {value:"empty",label:"未分配"}
						this.scope.push(empty)
						// console.log(this.scope,"user")
					}
				})
			},
			getAuthor() {
				this.$axios.get(this.Ip + '/ItAuthors')
				.then(res=>{
					if(res.data.result =="OK"){
						for(var i=0;i<res.data.content.length;i++){
							var typeone = {}
							typeone.value = res.data.content[i]
							typeone.label = res.data.content[i]
							this.itscope.push(typeone)
						}
						var empty = {value:"empty",label:"未分配"}
						this.itscope.push(empty)
						console.log(this.itscope,"user")
					}
				})
			},
			TryExport(szAddress) {
				this.$axios.get(this.Ip + '/' + szAddress).then(res => {
						if(res.data.result == "OK") {
							this.$notify({
								type: 'success',
								message: '导出成功'
							});
							// console.log(res,"export_two")
							window.location.href = this.Ip + res.data.datapath;
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
						}else if(res.data.result == "NG"){
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
							this.$notify({
								type: 'error',
								message: '服务器未知异常',
								showClose: true,
								duration: '0',
							});
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
			ChooseType(){
				if(this.export_type_one == "Req"){
					this.export_flag2 = false;
					this.export_flag = true;
				}else if(this.export_type_one == "HmiItProgressReport"){
					this.export_flag = false;
					this.export_flag2 = true;
				}else{
					this.export_flag = false;
					this.export_flag2 = false;
				}
			},
			OnDoExport(){
				var szAddress = this.Ip + '/HmiExport' 
				this.bScreenLockFlag = true;
				var szLoadingText = '导出中，请耐心等待';
				this.cLoading = this.$loading({
					lock: true,
					fullscreen: true,
					text: szLoadingText
				});
				if(this.export_type_one == "Req"){
					this.$axios.post(szAddress,{
						"type":this.export_type_one,
						"step":this.typeindex,
						"user":this.scopeindex
					})
					.then(res => {
						// console.log(res,"export")
						if(res.data.result == "OK"){
							window.location.href = this.Ip +'/HmiExportFile/' + res.data.Result_PathInfo +'/'+ res.data.Result_FileInfo;
							// console.log(window.location.href,"s")
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
						}else if(res.data.result == "NG"){
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
							this.$notify({
								type: 'error',
								message: '服务器未知异常',
								showClose: true,
								duration: '0',
							});
						}
						
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
				}else if(this.export_type_one == "HmiItProgressReport"){
					this.$axios.post(szAddress,{
						"type":this.export_type_one,
						"user":this.itscopeindex
					})
					.then(res => {
						// console.log(res,"export")
						if(res.data.result == "OK"){
							window.location.href = this.Ip +'/HmiExportFile/' + res.data.Result_PathInfo +'/'+ res.data.Result_FileInfo;
							// console.log(window.location.href,"s")
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
						}else if(res.data.result == "NG"){
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
							this.$notify({
								type: 'error',
								message: '服务器未知异常',
								showClose: true,
								duration: '0',
							});
						}
						
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
				}else{
					this.$axios.post(szAddress,{
						"type":this.export_type_one,
					})
					.then(res => {
						// console.log(res,"export")
						if(res.data.result == "OK"){
							window.location.href = this.Ip +'/HmiExportFile/' + res.data.Result_PathInfo +'/'+ res.data.Result_FileInfo;
							// console.log(window.location.href,"s")
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
						}else if(res.data.result == "NG"){
							this.bScreenLockFlag = false;
							if(this.cLoading != null) {
								this.cLoading.close();
							}
							this.$notify({
								type: 'error',
								message: '服务器未知异常',
								showClose: true,
								duration: '0',
							});
						}
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
				
			},
			lead_success(response, file, fileList) {
				this.fullscreenLoading2 = false;
				this.upload_flag = false
				if(response.result == 1) {
					console.log(response,"111")
					this.$notify({
						type: 'error',
						message: '服务器异常: ' + response.error,
						showClose: true,
						duration: '0',
					});
				}else if(response.result == "OK"){
					this.$notify({
						type: 'success',
						message: '上传成功',
						showClose: true,
						duration: '0',
					})
				}else if(response.result == "NG"){
					console.log(response,"NG")
					this.$notify({
						type: 'error',
						message: '服务器异常: ' + response.error,
						showClose: true,
						duration: '0',
					});
				}
			},
			OnleadScope() {
				this.lead_disabled = true,
				this.msg = {
					"type": this.lead_typeindex,
					"user_id": window.sessionStorage.getItem('admin'),
				},
				this.lead_Ip = this.Ip + '/HmiImport',
				this.msg.type = this.lead_typeindex;
				if(this.lead_typeindex == 'Req') {
					
					this.ImportDisabled = true;
					this.check_flag = true;
					this.$axios.get(this.Ip + '/HmiTableCols/req').then(res => {
						this.show_check = [];
						// console.log(res,"sel")
						let data = res.data.content;
						this.show_check = data;
						// console.log("NO")
						// 请求数据完成后再打开表格的显隐藏
						this.tableDisplay = true;
						// console.log("Ok")
					})

				}else if(this.lead_typeindex == 'HmiItProgressReport'){
					this.ImportDisabled = true;
					this.check_flag = true;
					this.$axios.get(this.Ip + '/HmiTableCols/it_progress_report').then(res => {
						this.show_check = [];
						// console.log(res,"sel")
						let data = res.data.content;
						this.show_check = data;
						// console.log("NO")
						// 请求数据完成后再打开表格的显隐藏
						this.tableDisplay = true;
						// console.log("Ok")
					})
				}else{
					this.tableDisplay = false;
				}
			},

			lead_click() {
				if(this.lead_typeindex == "") {
					this.$notify({
						iconClass: 'message_icon_info',
						message: '请选择类型',
					});
				}else if(this.lead_typeindex == "Req") {
					this.msg.update_cols = JSON.stringify(this.col_names);
					this.lead_disabled = false
					this.upload_flag = true;
					// console.log("11")
				}else if(this.lead_typeindex == "HmiItProgressReport"){
					this.msg.update_cols = JSON.stringify(this.col_names);
					this.lead_disabled = false
					this.upload_flag = true;
				}else{
					this.lead_disabled = false
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

			//select组
			downFile($index, row) { //下载文件
				window.location.href = this.Ip + "/DownLoad/" + row.record_id
			},

		},
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
