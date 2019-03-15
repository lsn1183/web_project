<template>
	<div class="g_dialog_shadow" id="CheckListDialog" v-show="show" v-loading.fullscreen.lock="fullscreenLoading">
		<div class="g_dialog g_dialog_ex">
			<!-- dialog标题 -->
			<h2 class="g_dialog_header s_header_ex">
					<span class="s_section_left">审核</span>
					<!-- 点x关闭弹出框 -->
					<i class="s_section_right s_close el-icon-close" @click="close()"></i>
				</h2>
			<div class="g_dialog_body g_dialog_body_ex">
				<div class="s_workerl_table">
					<el-tabs v-model="activeName" @click="handleClick">
						<el-tab-pane label="H/U" name="hu" v-if="check_list_type[0] == 'hu'?true:false">
							<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;;border: solid 1px #dfe6ec;font-size: 12px;">
								<tr v-for="items in hu_data_array">
									<td style="width: 20%;">
										{{items.type}}
									</td>
									<td style="width: 80%;">
										<el-table border style="height: 100%" :data = "items.content">
														<el-table-column prop='check_subject'>
															
														</el-table-column>
														<el-table-column prop='check_methord'>
															
														</el-table-column>
														<el-table-column prop='charger_check'>
															<template scope="scope">
																<el-select v-model="scope.row.charger_check">
																	<el-option v-for="item in children"
																		:key="item.value"
																		:label="item.label"
																		:value="item.value">
																		
																	</el-option>
																</el-select>
															</template>
														</el-table-column>
										</el-table>	
									</td>
								</tr>
							</table>
						</el-tab-pane>
						<el-tab-pane label="TAGL要件定义" name="definition" v-if="check_list_type[1] == 'definition'?true:false">
							<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;;border: solid 1px #dfe6ec;font-size: 12px;">
								<tr v-for="items in def_data_array">
									<td style="width: 20%;">
										{{items.type}}
									</td>
									<td style="width: 80%;">
										<el-table border style="height: 100%" :data = "items.content">
														<el-table-column prop='check_subject'>
															
														</el-table-column>
														<el-table-column prop='check_methord'>
															
														</el-table-column>
														<el-table-column prop='charger_check'>
															<template scope="scope">
																<el-select v-model="scope.row.charger_check">
																	<el-option v-for="item in children"
																		:key="item.value"
																		:label="item.label"
																		:value="item.value">
																		
																	</el-option>
																</el-select>
															</template>
														</el-table-column>
										</el-table>	
									</td>
								</tr>
							</table>
						</el-tab-pane>
						<el-tab-pane label="TAGL要件分析" name="analysis" v-if="check_list_type[2] == 'analysis'?true:false">
							<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;;border: solid 1px #dfe6ec;font-size: 12px;">
								<tr v-for="items in ana_data_array">
									<td style="width: 20%;">
										{{items.type}}
									</td>
									<td style="width: 80%;">
										<el-table border style="height: 100%" :data = "items.content">
														<el-table-column prop='check_subject'>
															
														</el-table-column>
														<el-table-column prop='check_methord'>
															
														</el-table-column>
														<el-table-column prop='charger_check'>
															<template scope="scope">
																<el-select v-model="scope.row.charger_check">
																	<el-option v-for="item in children"
																		:key="item.value"
																		:label="item.label"
																		:value="item.value">
																		
																	</el-option>
																</el-select>
															</template>
														</el-table-column>
										</el-table>	
									</td>
								</tr>
							</table>
						</el-tab-pane>
					</el-tabs>
				</div>
			</div>
			<div class="g_dialog_footer confirmcancel">
				<el-button type="primary" @click="save()">确定</el-button>
				<el-button @click="close()">取消</el-button>
			</div>

		</div>

	</div>
</template>

<script>
	export default {
		props: ['dialog_show','all_data','check_list_type','upload_id'],
		data() {
			return {
				'fullscreenLoading': false,
				hu_data: [],
				def_data: [],
				ana_data: [],
				
				hu_data_array: [],
				def_data_array: [],
				ana_data_array: [],
				activeName: '',
				show: false,
				children:   [ 
								{
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
				check_list1:{
					'hu' : [],
					'definition' : [],
					'analysis' : [],
				}
			}	
		},

		methods: {
			handleClick(tab,event){
	
			},
			request_data(val){
				this.$axios.get(this.Ip + "/CheckContent/" + val)
				.then(res => {
					if(val == 'hu'){
						this.hu_data = [];
							this.hu_data_array = []
							for(let i = 0;i<res.data.hu_check_list.length;i++){
								if(this.hu_data.indexOf(res.data.hu_check_list[i].check_project) == -1){
									this.hu_data.push(res.data.hu_check_list[i].check_project)
								}
								
							}
							for(let i = 0;i<this.hu_data.length;i++){
								this.hu_data_array.push(
									{
										'type': this.hu_data[i],
										'content' : []
									})
							}

							for(let i = 0;i<res.data.hu_check_list.length;i++){
								for(let j = 0;j<this.hu_data_array.length;j++){
									if(this.hu_data_array[j].type == res.data.hu_check_list[i].check_project){
										let New_Data = JSON.parse(JSON.stringify(res.data.hu_check_list[i]))
										New_Data.charger_check = ''
										this.hu_data_array[j].content.push(New_Data)
									}
								}
							}
					}else if(val == 'definition'){
						this.def_data = [];
							this.def_data_array = []
							for(let i = 0;i<res.data.definition_check_list.length;i++){
								if(this.def_data.indexOf(res.data.definition_check_list[i].check_project) == -1){
									this.def_data.push(res.data.definition_check_list[i].check_project)
								}
								
							}
							for(let i = 0;i<this.def_data.length;i++){
								this.def_data_array.push(
									{
										'type': this.def_data[i],
										'content' : []
									})
							}

							for(let i = 0;i<res.data.definition_check_list.length;i++){
								for(let j = 0;j<this.def_data_array.length;j++){
									if(this.def_data_array[j].type == res.data.definition_check_list[i].check_project){
										let New_Data = JSON.parse(JSON.stringify(res.data.definition_check_list[i]))
										New_Data.charger_check = ''
										this.def_data_array[j].content.push(New_Data)
									}
								}
							}
					}else{
						this.ana_data = [];
							this.ana_data_array = []
							for(let i = 0;i<res.data.analysis_check_list.length;i++){
								if(this.ana_data.indexOf(res.data.analysis_check_list[i].check_project) == -1){
									this.ana_data.push(res.data.analysis_check_list[i].check_project)
								}
								
							}
							for(let i = 0;i<this.ana_data.length;i++){
								this.ana_data_array.push(
									{
										'type': this.ana_data[i],
										'content' : []
									})
							}

							for(let i = 0;i<res.data.analysis_check_list.length;i++){
								for(let j = 0;j<this.ana_data_array.length;j++){
									if(this.ana_data_array[j].type == res.data.analysis_check_list[i].check_project){
										let New_Data = JSON.parse(JSON.stringify(res.data.analysis_check_list[i]))
										New_Data.charger_check = ''
										this.ana_data_array[j].content.push(New_Data)
									}
								}
							}
					}
				})
				.catch()
			},
			onshow() {
//				if(this.all_data[0].list2 === undefined){
//					for(let i = 0;i<this.all_data[0].hu_list.length;i++){
//						if(this.all_data[0].hu_list[i].job_status == 2){
//								this.all_data[0].hu_list[i].job_status = 3
//								this.check_list_type[0] = 'hu'
//						}
//						
//						for(let j = 0;j<this.all_data[0].hu_list[i].definition_list.length;j++){
//								if(this.all_data[0].hu_list[i].definition_list[j].job_status == 2){
//									this.all_data[0].hu_list[i].definition_list[j].job_status = 3
//									this.check_list_type[1] = 'definition'
//							}
//							for(let k = 0;k<this.all_data[0].hu_list[i].definition_list[j].analysis_list.length;k++){
//									if(this.all_data[0].hu_list[i].definition_list[j].analysis_list[k].job_status == 2){
//										this.all_data[0].hu_list[i].definition_list[j].analysis_list[k].job_status = 3
//										this.check_list_type[2] = 'analysis'
//									}
//							}
//						}
//					}
//				}else{
//					for(let i = 0;i<this.all_data[0].hu_list.length;i++){
//						if(this.all_data[0].list2.hu.toString() == [].toString()){
//							if(this.all_data[0].hu_list[i].job_status == 2){
//								this.all_data[0].hu_list[i].job_status = 3
//								this.check_list_type[0] = 'hu'
//							}
//						}
//						
//						for(let j = 0;j<this.all_data[0].hu_list[i].definition_list.length;j++){
//							if(this.all_data[0].list2.definition.toString() == [].toString()){
//								if(this.all_data[0].hu_list[i].definition_list[j].job_status == 2){
//									this.all_data[0].hu_list[i].definition_list[j].job_status = 3
//									this.check_list_type[1] = 'definition'
//								}
//							}
//							for(let k = 0;k<this.all_data[0].hu_list[i].definition_list[j].analysis_list.length;k++){
//								if(this.all_data[0].list2.analysis.toString() == [].toString()){
//									if(this.all_data[0].hu_list[i].definition_list[j].analysis_list[k].job_status == 2){
//										this.all_data[0].hu_list[i].definition_list[j].analysis_list[k].job_status = 3
//										this.check_list_type[2] = 'analysis'
//									}
//								}	
//							}
//						}
//					}
//				}
				for(let i = 0;i<this.check_list_type.length;i++){
					if(this.check_list_type[i] != ''){
						this.activeName = this.check_list_type[i]
						break;
					}
				}
				
				if(this.all_data[0].list2 === undefined){
					for(let i = 0;i<this.check_list_type.length;i++){
						if(this.check_list_type[i] != ''){
							this.request_data(this.check_list_type[i]);
						}
					}
				}else{
					this.check_list1 = JSON.parse(JSON.stringify(this.all_data[0].list2))
					for(let item in this.check_list1){
						if(this.check_list1[item].toString() == [].toString()){
							this.request_data(item);
						}
					}
				}
				this.show = true;
			},
			close() {
					this.getCheckList()
					this.$emit('dialog_close', [false, this.check_list1]);
					this.show = false;
			},
			getCheckList(){
				this.check_list1 = {
					'hu' : [],
					'definition' : [],
					'analysis' : [],
				};
				for(let i =0;i<this.hu_data_array.length;i++){
					this.check_list1.hu.push.apply(this.check_list1.hu,this.hu_data_array[i].content)
				}
				for(let i =0;i<this.def_data_array.length;i++){
					this.check_list1.definition.push.apply(this.check_list1.definition,this.def_data_array[i].content)
				}
				for(let i =0;i<this.ana_data_array.length;i++){
					this.check_list1.analysis.push.apply(this.check_list1.analysis,this.ana_data_array[i].content)
				}
			},
			save() {
				this.fullscreenLoading = true;
				this.getCheckList()
				for(let item in this.check_list1){
					console.log(item,'item')
					for(let items of this.check_list1[item]){
						if(items.charger_check==''){
							this.$notify({
								type:'error',
								message:'提交审核内容不能为空，必须全部选择',
							})
							return;
						}
					}
				}
				
				delete this.all_data[0].list1
				this.all_data[0].list2 = this.check_list1
				this.$axios.post(this.Ip+'/PostFullContent',this.all_data)
				.then(res=>{
					if(res.data.result=="OK"){
						this.$axios.get(this.Ip+'/ArlTreeInfo/'+this.upload_id+'/'+window.sessionStorage.getItem('admin')+'/'+1)
						.then(res => {	
							this.hu_data_array = []
							this.def_data_array = []
							this.ana_data_array = []
							this.fullscreenLoading = false; 
							this.$notify({
								type:'success',
								message:'保存成功'
							})
							this.$emit('dialog_close', [true]);
							this.show = false;
						})
						.catch(res=>{
							this.fullscreenLoading = false;
							this.$emit('dialog_close', [false, this.check_list1]);
							this.$notify({
								type:'error',
								message:'网络异常，请重新刷新',
								showClose:true,
								duration:'0',
							})
						});
					}else{
						this.fullscreenLoading = false;
						this.$emit('dialog_close', [false, this.check_list1]);
			            this.$notify({
							type:'error',
							message:res.data.error,
							showClose:true,
							duration:'0',
						})
					}
				}).catch(res=>{
					this.fullscreenLoading = false;
					this.$emit('dialog_close', [false, this.check_list1]);
		            this.$notify({
						type:'error',
						message:'保存失败!',
						showClose:true,
						duration:'0',
					})
		            
				})
			},

		},

		watch: {
			dialog_show(v) {
				if(this.dialog_show) {
					this.onshow();
				}
			}
		},
	}
</script>

<style scoped>
	/* g_dialog是base式样，g_dialog_ex需要扩展，根据需要自行调整，尤其是width，请自行添加*/
	
	.g_dialog {
		margin: 10% auto 0;
		border-radius: 2px;
		padding: 15px;
		background: white;
		-webkit-box-shadow: 0 1px 3px rgba(0, 0, 0, .3);
		box-shadow: 0 1px 3px rgba(0, 0, 0, .3);
	}
	
	.g_dialog_ex {
		width: 67.5%;
		margin-top: 5%;
		height: 785px;
		padding: 10px;
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
	
	.g_dialog_header {
		width: 100%;
		height: 30px;
		line-height: 30px;
		margin-bottom: 12px;
		font-size: 18px;
	}
	
	.s_header_ex {
		margin-bottom: 0;
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
		border-top: 1px solid rgb(225, 225, 225);
		border-bottom: 1px solid rgb(225, 225, 225);
		padding: 20px;
	}
	
	.g_dialog_body_ex {
		height: 677px;
		padding-top: 0;
		border-top: 0px solid rgb(225, 225, 225);
	}
	
	.g_dialog_body .s_section {
		border: solid 1px #bfcbd9;
		overflow: hidden;
	}
	
	.g_dialog_body .s_section .s_section_children {
		text-align: center;
		float: left;
		border-right: solid 1px rgb(225, 225, 225);
	}
	
	.g_dialog_body .s_section .s_section_bottom .s_section_children {
		height: 102px;
	}
	
	.g_dialog_body .s_section .s_section_table_select {
		width: 26%;
		vertical-align: middle;
	}
	
	.g_dialog_body .s_section .s_section_table_textarea {
		width: 18%;
	}
	
	.g_dialog_body .s_section .s_section_table_act {
		width: 20%;
		border-right: solid 0px #ccc;
	}
	
	.g_dialog_body .s_section .s_section_children_ex {
		padding: 0 1%;
		font-size: 14px;
		font-weight: bold;
	}
	
	.g_dialog_body .s_section .s_section_bottom .s_section_bottom_item {
		height: 100%;
		margin: 0;
		border-bottom: solid 1px #bfcbd9;
	}
	
	.g_dialog_body .s_section .left {
		width: 30%;
		text-align: right;
		padding-right: 10px;
		display: inline-block;
	}
	
	.g_dialog_body .s_section .right {
	
	}
	
	.g_dialog_body .s_section .s_section_top {
		height: 36px;
		background-color: #eef1f6;
		border-bottom: solid 1px #bfcbd9;
		padding-right: 8px;
		/*overflow-y: scroll;*/
	}
	
	.g_dialog_body .s_section .s_section_bottom {
		width: 100%;
		overflow-y: scroll;
		vertical-align: middle;
		height: 570px;
	}
	
	.g_dialog_body .s_section .textarea {
		width: 215px;
		vertical-align: middle;
	}
	
	.g_dialog_footer {
		height: 36px;
		width: 100%;
		margin-top: 15px;
	}
	
	.g_dialog_footer .s_section_right,.confirmcancel {
		text-align: right;
	}
	
	.btn_shadow {
		color: #ccc;
	}
	
	.s_span {
		border-bottom: none;
	}
	
	.s_span_second {
		font-weight: bold;
		margin-right: 30px;
	}
	
	.s_title_top {
		height: 40px;
		width: 100%;
		margin-right: 27px;
		line-height: 40px;
		border-bottom: 1px solid #dfe6ec;
	}
	
	.s_span span {
		height: 40px;
		line-height: 40px;
		cursor: pointer;
		margin-right: 28px;
	}
	
	.s_span .fr:hover {
		color: #42b983;
	}
	
	.g_button {
		float: right;
		color: #42b983;
	}
	
	.s_workerl_table {
		overflow-y: scroll;
		height: 93%;
	}
	
	.s_title {
		font-weight: bold;
		height: 40px;
		line-height: 40px;
		background: rgba(238, 241, 246, .2);
		transition: 0.9s;
		width: 100%;
		padding-left: 15px;
	}
	/*.s_title:hover{
	background: rgba(238,241,246,.9);
}*/
	
	.s_title>div>span {
		font-weight: normal;
	}
	
	.s_title span {
		cursor: pointer;
		margin-right: 20px;
	}
	
	.s_title .fr:hover {
		color: #42b983;
	}
	
	.s_table_content {
		float: left;
		width: 200px;
		border-right: 1px solid #dfe6ec;
		/*height:149px;*/
	}
	
	.s_table_title {
		height: 30px;
		line-height: 30px;
		font-weight: bold;
		text-align: center;
		background: #eef1f6;
		font-size: 14px;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		border-bottom: solid 1px #dfe6ec;
	}
	
	.s_table_textarea {
		overflow: hidden;
		text-overflow: ellipsis;
		/*white-space: nowrap;*/
		/*height: 110px;*/
		font-size: 14px;
	}
	
	.s_tagldef_table {
		/*position: relative;*/
		/*height: 132px;*/
		border: 1px solid #dfe6ec;
		display: flex;
	}
	
	.s_worker_section {
		/*border-left: 1px solid #dfe6ec;
	border-bottom: 1px solid #dfe6ec;*/
	}

</style>
