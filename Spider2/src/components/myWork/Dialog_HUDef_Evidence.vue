<template>
	<div class="g_dialog_shadow" v-show="show">
		<div class="g_dialog g_dialog_ex">
			<!-- dialog标题 -->
			<h2 class="g_dialog_header">
				<span class="s_section_left">機能配置を判断したエビデンス</span>
				<!-- 点x关闭弹出框 -->
				<i class="s_section_right close el-icon-close" @click="close()"></i>
			</h2>
			<div class="g_dialog_body g_dialog_body_ex">
				<p class="s_title_base"><i class="el-icon-document" ></i> 001 システム仕様書</p>	
	  	    	<p class="s_section">
	  	    		<span class="s_left">章/ページ番号</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.sys_spec_chapter"></el-input>	    	  	    		
	  	    	</p>	
	  	        <p class="s_title"><i class="el-icon-document" ></i> 003 共通アプリ・AVC-LAN仕様書</p>	
	  	    	<p class="s_section">
	  	    		<span class="s_left">章/ページ番号</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.common_chapter"></el-input>			    	  	    		
	  	    	</p>
	  	    	<p class="s_section">
	  	    		<span class="s_left">シーケンス仕様</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.common_seq_spec"></el-input>			    	  	    		
	  	    	</p>
	  	    	<p class="s_section">
	  	    		<span class="s_left">シーケンス番号</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.common_seq_no"></el-input>			    	  	    		
	  	    	</p>	  	    	
	  	    	<p class="s_section">
	  	    		<span class="s_left">コマンドガイド</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.common_cmd_guide"></el-input>			    	  	    		
	  	    	</p>
    	  	    <p class="s_section">
	  	    		<span class="s_left">OPC</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.common_opc"></el-input>			    	  	    		
	  	    	</p>    
	  	    	
	  	    	<p class="s_title"><i class="el-icon-document" ></i> 318 DCU-MEU間連携仕様書DCU-MEU</p>	
	  	    	<p class="s_section">
	  	    		<span class="s_left">機能配置・機能仕様</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.inter_loc_spec"></el-input>			    	  	    		
	  	    	</p> 
	  	    	<p class="s_section">
	  	    		<span class="s_left">章/ページ番号</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.inter_chapter"></el-input>			    	  	    		
	  	    	</p>  	
	  	    	<p class="s_title"><i class="el-icon-document" ></i> その他資料</p>	
	  	    	<p class="s_section">
	  	    		<span class="s_left">ドキュメント名<br/><font color="red">※トヨタ仕様の場合は仕様番号も記載する事</font></span>
					<el-input class="s_right s_textarea_ex" type="textarea" :rows="1" v-model="hu_data_copy.other_doc"></el-input>			    	  	    			  	    		
	  	    	</p> 
	  	    	<p class="s_section">
	  	    		<span class="s_left">章/ページ番号</span>
	  	    		<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.other_chapter"></el-input>		    	  	    		
	  	    	</p> 	
    	    </div>
	   	   	<div class="g_dialog_footer confirmcancel">
	   	   		<el-button type="primary" @click="save()">确定</el-button>
		 		<el-button @click="close()">取消</el-button>	 				   	   	
	   	   	</div>	
		</div>
	</div>
</template>

<script>
	export default{
		props: ['hu_data', 'hu_model_list', 'dialog_show'],

		data() {
			return {
				show : false,
				hu_data_copy : {},
				hu_open_data:'',
				hu_close_data:'',
			}
		},

		methods: {
			onshow() {
				this.hu_data_copy = JSON.parse(JSON.stringify(this.hu_data));
				this.show = true;
				this.hu_open_data = JSON.stringify(this.hu_data_copy)
			},

			close() {
				this.hu_close_data = JSON.stringify(this.hu_data_copy)
				if (this.hu_close_data == this.hu_open_data) {
					this.$emit('dialog_close', [false, this.hu_data_copy]);
					this.show = false;
				} else{
					this.$confirm('您有未提交的内容，确定离开?','提示',{
				    		confirmButtonText:"确定",
				    		cancelButtonText:"取消",
				    		type:"warning"
				    		
				   }).then(() => {
						this.$emit('dialog_close', [false, this.hu_data_copy]);
						this.show = false;
				    }).catch(() => {
				    	
				    })
				}
			},
			save(){
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_HUDEF_DOC_SYSTEM, this.hu_data_copy.sys_spec_chapter) == false){
					this.$alert('001 システム仕様書格式不正确!!');
					return;
				}
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_HUDEF_DOC_AVCLAN, this.hu_data_copy.common_chapter) == false){
					this.$alert('003 共通アプリ・AVC-LAN仕様書格式不正确!!');
					return;
				}
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_HUDEF_DOC_AVCLAN, this.hu_data_copy.common_seq_spec) == false){
					this.$alert('003 共通アプリ・AVC-LAN仕様書格式不正确!!');
					return;
				}
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_HUDEF_DOC_AVCLAN, this.hu_data_copy.common_seq_no) == false){
					this.$alert('003 共通アプリ・AVC-LAN仕様書格式不正确!!');
					return;
				}
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_HUDEF_DOC_AVCLAN, this.hu_data_copy.common_cmd_guide) == false){
					this.$alert('003 共通アプリ・AVC-LAN仕様書格式不正确!!');
					return;
				}
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_HUDEF_DOC_AVCLAN, this.hu_data_copy.common_opc) == false){
					this.$alert('003 共通アプリ・AVC-LAN仕様書格式不正确!!');
					return;
				}
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_HUDEF_DOC_AVCLAN, this.hu_data_copy.inter_loc_spec) == false){
					this.$alert('318 DCU-MEU間連携仕様書格式不正确!!');
					return;
				}
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_COMMON_NOT_EMPTY, this.hu_data_copy.inter_chapter) == false){
					this.$alert('318 DCU-MEU間連携仕様書格式不正确!!');
					return;
				}
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_COMMON_NOT_EMPTY, this.hu_data_copy.other_chapter) == false){
					this.$alert('318 DCU-MEU間連携仕様書格式不正确!!');
					return;
				}
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_COMMON_NOT_EMPTY, this.hu_data_copy.other_doc) == false){
					this.$alert('その他資料格式不正确!!');
					return;
				}
				this.$emit('dialog_close', [true, this.hu_data_copy]);
				this.show = false;
			},
		},

		watch : {
			dialog_show(v) {
				if (this.dialog_show) {
					this.onshow();
				}
			}
    	},
	}
</script>

<style scoped>
/* g_dialog是base式样，g_dialog_ex需要扩展，根据需要自行调整，尤其是width，请自行添加*/
.g_dialog {
	width: 22%;
    margin: 10% auto 0;        
    border-radius: 2px;
    padding: 15px;
    background: white;
    -webkit-box-shadow: 0 1px 3px rgba(0,0,0,.3);
    box-shadow: 0 1px 3px rgba(0,0,0,.3);
}
.g_dialog_ex {
	width: 25%;	
	min-width: 380px;
	margin: 5% auto 0;
}

.g_dialog_shadow {
	width: 100%;
	height: 100%;
	background: rgba(0,0,0,.3);
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	z-index:2001;	
}

.g_dialog_header {
	width: 100%;
    height: 45px;
    line-height: 45px;
    margin-bottom: 12px;
    font-size:18px;
}
.g_dialog_header .s_section_left {
	float: left;
} 
.g_dialog_header .s_section_right {
	float: right;	
}
.g_dialog_header .close {
	font-size: 14px; 	
} 
.g_dialog_body{
	font-size: 14px;    
    border-top: 1px solid rgb(225,225,225);
    border-bottom : 1px solid rgb(225,225,225);
    padding: 10px;
}
.g_dialog_body_ex {
	overflow-y: auto;
	height: 643px;
}
.g_dialog_body .s_section{
    width: 100%;        
    vertical-align: middle;
    margin: 15px 0;
    
    padding-left: 15px;    	
}

.g_dialog_body .s_title_base{
    width: 100%;        
    vertical-align: middle;
    margin: 15px 0;    	
}

.g_dialog_body .s_title{
    width: 100%;        
    vertical-align: middle;
    margin: 15px 0;   
    
    margin-top: 30px; 	
}

.g_dialog_body .s_section .s_left{
    width:40%;        
    text-align: right;    
    padding-right: 10px;
    
    display: inline-block;        
    /*border: 1px solid #ccc;*/
}

.g_dialog_body .s_section .s_right{
                	
}
.g_dialog_body .s_section .s_textarea{	
	width: 50%;
	vertical-align: middle;
}
.g_dialog_body .s_section .s_textarea_ex{	
	width: 50%;
}
.g_dialog_footer{
	height: 36px;
	width: 100%;
	margin-top: 15px;			
}
.g_dialog_footer .s_section_right,.confirmcancel{
	text-align: right;
}

</style>
