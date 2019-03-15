<template>
	<div class="g_dialog_shadow" v-show="show">
			<div class="g_dialog g_dialog_ex">
				<!-- dialog标题 -->
				<h2 class="g_dialog_header">
					<span class="s_section_left">指摘</span>
					<!-- 点x关闭弹出框 -->
					<i class="s_section_right s_close el-icon-close" @click="close()"></i>
				</h2>
			<div class="g_dialog_body g_dialog_body_ex">
				<div class=""  v-for="(point_info, index) in this.tagl_data_copy.point_list">
					<h4>
						<span class="s_left">({{index+1}})指摘拿到日:</span>
						<span class="s_right s_textarea" v-html="point_info.point_date"></span>
					</h4>
					<div style="width: 55%;height: 630px;float: left;overflow:auto;border: solid 1px #bfcbd9;">
						<p style="font-size: 16px;height: 35px;line-height: 52px;font-weight: bold;">&nbsp;&nbsp;&nbsp;客户端指摘</p>
						<p class="s_section s_section_ex">
							<span class="s_left">レビュー結果:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.review_result"></el-input>
						</p>
						<p class="s_section s_section_ex">
							<span class="s_left">指摘No:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.pointout_no"></el-input>
						</p>
						<p class="s_section s_section_ex">
							<span class="s_left">ステータス:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.pointout_status"></el-input>
						</p>
						<p class="s_section s_section_ex">
							<span class="s_left">コメント:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="8" style="font-style: normal;font-size: 12px;" v-html="point_info.pointout_comment"></el-input>
						</p>
						<p class="s_section s_section_ex">
							<span class="s_left">リーダチェック:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.reader_check"></el-input>
						</p>
						<p class="s_section s_section_ex">
							<span class="s_left">リーダ２チェック:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.reader2_check"></el-input>
						</p>
						<p class="s_section s_section_ex">
							<span class="s_left">最終チェック:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.final_check"></el-input>
						</p>
						<p class="s_section s_section_ex">
							<span class="s_left">担当:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.pointout_charger"></el-input>
						</p>
						<p class="s_section s_section_ex">
							<span class="s_left">優先度:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.pointout_priority"></el-input>
						</p>
						<p class="s_section s_section_ex">
							<span class="s_left">指摘提出日:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.pointout_date"></el-input>
						</p>
						<!--<p class="s_section s_section_ex">
							<span class="s_left">ARL関連指摘:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="1" style="font-style: normal;font-size: 12px;" v-html="point_info.arl_rel"></el-input>
						</p>-->
					</div>
					<div style="width: 45%;height: 630px;float: left;border: solid 1px #bfcbd9;border-left: none;">
						<p style="font-size: 16px;height: 35px;line-height: 52px;font-weight: bold;">&nbsp;&nbsp;&nbsp;SUNTEC对应</p>
						<p class="s_section">
							<span class="s_left">Suntecステータス:</span>
							<el-select class="s_right s_select" v-model="point_info.suntec_status" placeholder="请选择" size='small'>
    	     					<el-option v-for="item in Point_Suntec_Status" :key="item.value" :label="item.label" :value="item.value"></el-option>
    	     				</el-select>
						</p>
						<p class="s_section">
							<span class="s_left">修正済み:</span>
							<el-select class="s_right s_select" v-model="point_info.fixed" size='small'>
								<el-option v-for="item in Point_Fixed" :key="item.value" :label="item.value" :value="item.value"></el-option>
							</el-select>
						</p>
						<p class="s_section">
							<span class="s_left">要求式样书関連指摘:</span>
							<el-select class="s_right s_select" v-model="point_info.arl_rel" size='small'>
								<el-option v-for="item in Point_ARL" :key="item.value" :label="item.value" :value="item.value"></el-option>
							</el-select>
						</p>
						<!--<p class="s_section">
							<span class="s_left">Suntecステータス:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="8" v-model="point_info.suntec_status"></el-input>
						</p>
						<p class="s_section">
							<span class="s_left">修正済み:</span>
							<el-select class="s_right s_select" v-model="point_info.fixed" size='small'>
								<el-option v-for="item in DONE" :key="item.value" :label="item.value" :value="item.value"></el-option>
							</el-select>
						</p>-->
						<p class="s_section">
							<span class="s_left">Suntec備考:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="8" v-model="point_info.suntec_remark"></el-input>
						</p>
						<p class="s_section">
							<span class="s_left">Suntec修正不可:</span>
							<el-input class="s_right s_textarea" type="textarea" :rows="8" v-model="point_info.suntec_cannot_modify"></el-input>					</el-input>
						</p>
					</div>
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
		props: ['tagl_def_data', 'dialog_show'],

		data() {
			return {
				show: false,
				tagl_data_copy : {},
				tagl_opened_data : '',
				tagl_closed_data : '',
				DONE: [
						{
				        	value: '○',
				        	label: '○'
				        },
				        {
				          value: '×',
				          label: '×'
				        }
				    ],
				Point_Suntec_Status: [
						{
				        	value: 'SUNTEC清書完',
				        	label: 'SUNTEC清書完'
				        },
				        {
				          value: '検討中',
				          label: '検討中'
				        },
				        {
				        	value: '',
				        	label: ''
				        },
				    ],
				Point_Fixed: [
						{
				        	value: '修正済み',
				        	label: '修正済み'
				        },
				        {
				          value: '修正不要',
				          label: '修正不要'
				        },
				        {
				          value: '修正待ち',
				          label: '修正待ち'
				        },
				        {
				        	value: '未着手',
				        	label: '未着手'
				        },
				        {
				        	value: '',
				        	label: ''
				        }
				    ],
			    Point_ARL: [
					{
			        	value: '×',
			        	label: '×'
			        },
			        {
			          value: '〇',
			          label: '〇'
			        },
			        {
			        	value: '',
			        	label: ''
			        }
			    ],    
			}
		},

		methods: {
			onshow() {
				this.tagl_data_copy = JSON.parse(JSON.stringify(this.tagl_def_data));
//				if(this.tagl_data_copy.point_list.length==0){
//					this.tagl_data_copy.point_list.unshift({"review_result": '','pointout_no': '','pointout_status': '','pointout_comment': '','reader_check': '',
//			             'reader2_check': '','final_check': '','pointout_charger': '','pointout_priority': '','pointout_date': '','fixed': '','suntec_remark': ''})
//				}else{
//					this.tagl_data_copy.point_list.unshift(this.tagl_data_copy.point_list[0])
//				}
				this.tagl_opened_data = JSON.stringify(this.tagl_data_copy.point_list)
				this.show = true;
			},
			close() {
				this.tagl_closed_data = JSON.stringify(this.tagl_data_copy.point_list)
				if(this.tagl_closed_data != this.tagl_opened_data) {
					//修改数据 要执行的方法
					this.$confirm('您有未提交的内容，确定离开?', '提示', {
						confirmButtonText: "确定",
						cancelButtonText: "取消",
						type: "warning"

					}).then(() => {
						this.$emit('dialog_close', [false, this.tagl_data_copy]);
						this.show = false;
					}).catch(() => {

					})

				} else {
					this.$emit('dialog_close', [false, this.tagl_data_copy]);
					this.show = false;
				}
			},
			save() {
				for(let i = 0;i<this.tagl_data_copy.point_list.length;i++){
					if(this.tagl_data_copy.point_list[i].suntec_remark == ''){
						if(this.tagl_data_copy.point_list[i].suntec_status == '' && this.tagl_data_copy.point_list[i].fixed == ''){
							this.$notify({
								type:'error',
								message:'Suntec備考不能为空',
								showClose:true,
								duration:'0',
							})
							return;
						}	
					}
				}
				this.$emit('dialog_close', [true, this.tagl_data_copy]);
				this.show = false;
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
		width: 50%;
		margin-top: 5%;
		height: 785px;
		padding: 10px;
		border-bottom: 1px solid rgb(225,225,225);
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
		height: 45px;
		line-height: 45px;
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
		height: 650px;
		overflow: auto;
		padding-top: 0;
		border-top: 0px solid rgb(225, 225, 225);
	}
	
	.g_dialog_body .s_section{
	    width: 100%;        
	    vertical-align: middle;
	    margin: 15px 0;
	
	    padding-left: 15px;    	
	}
	.g_dialog_body .s_section_ex{
	    margin-bottom: 20px;    	
	}
	.g_dialog_body .s_section .s_left{
	    width:36%;        
	    text-align: right;    
	    padding-right: 10px;
	    display: inline-block;        
	}
	
	.g_dialog_body .s_section .s_right{
	                	
	}
	.g_dialog_body .s_section .s_textarea{	
		width: 55%;
		vertical-align: middle;
	}
	.g_dialog_body .s_section .s_select{	
		width: 55%;
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
	
	.g_dialog_body .s_section .right {}
	
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
	
	.g_dialog_footer .s_section_right,
	.confirmcancel {
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
	
	.s_table {
		position: relative;
		height: 132px;
		border: 1px solid #dfe6ec;
		display: block;
	}
	
	.s_worker_section {
		/*border-left: 1px solid #dfe6ec;
	border-bottom: 1px solid #dfe6ec;*/
	}
</style>