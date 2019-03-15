<template>
	<div class="g_dialog_shadow" v-show="show">
			<div class="g_dialog g_dialog_ex">
				<!-- dialog标题 -->
				<h2 class="g_dialog_header">
					<span class="s_section_left">变更理由与日期</span>
					<!-- 点x关闭弹出框 -->
					<i class="section_right close el-icon-close" @click="close()"></i>
				</h2>
		   	   	<div class="g_dialog_body">	    	  	    	    	  	    
    	  	    	<!-- TAGL表格 -->
					<p class="s_section">
    	  	    		<span class="s_left">变更理由</span>	    	  	    		
    	  	    		<el-input class="s_right s_textarea" type="textarea" :rows="5" :placeholder=tagl_ana_data_copy.reason v-model='tagl_ana_reason_copy'></el-input>	    	  	    				    	  	    		
    	  	    	</p> 
    	  	    	<p class="s_section">
		  	    		<span class="s_left">日付</span>
		  	    		<el-date-picker class="s_right s_textarea" type="date" placeholder="选择日期" v-model="tagl_ana_data_copy.new_date" format @change="setDate"></el-date-picker>		    	  	    		
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
		props: ['tagl_ana_data', 'dialog_show'],

		data() {
			return {
				show : false,
				tagl_ana_data_copy : {},
				tagl_ana_opened_data:'',
				tagl_ana_closed_data:'',
				tagl_ana_reason_open: '',
				tagl_ana_reason_copy: '',
			}
		},

		methods: {
			onshow() {		
				this.tagl_ana_data_copy = JSON.parse(JSON.stringify(this.tagl_ana_data));
				this.show = true;
				this.tagl_ana_opened_data = JSON.stringify(this.tagl_ana_data_copy);
				this.tagl_ana_reason_open = JSON.parse(JSON.stringify(this.tagl_ana_data)).reason
				this.tagl_ana_reason_copy = ''
			},

			close() {
				if(this.tagl_ana_reason_copy !=''){
					this.tagl_ana_data_copy.reason = this.tagl_ana_reason_copy
				}
				this.tagl_ana_closed_data = JSON.stringify(this.tagl_ana_data_copy)
				if (this.tagl_ana_closed_data == this.tagl_ana_opened_data) {
					this.$emit('dialog_close', [false, this.tagl_ana_data_copy]);
					this.show = false;
				} else{
					this.$confirm('您有未提交的内容，确定离开?','提示',{
				    		confirmButtonText:"确定",
				    		cancelButtonText:"取消",
				    		type:"warning"
				    		
				    }).then(() => {
				    	this.tagl_ana_data_copy.reason = this.tagl_ana_reason_open
				    	this.$emit('dialog_close', [false, this.tagl_ana_data_copy]);
						this.show = false;
				    }).catch(() => {
//				    	this.tagl_ana_data_copy.reason = this.tagl_ana_reason_open
				    })
				}
			},
			save(){
				if(this.tagl_ana_reason_copy !=''){
					this.tagl_ana_data_copy.reason = this.tagl_ana_reason_copy
				}
				this.tagl_ana_closed_data = JSON.stringify(this.tagl_ana_data_copy)
				if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_COMMON_NOT_EMPTY, this.tagl_ana_data_copy.reason) == false){
					this.$alert('变更理由不能为空!!');
//					this.tagl_ana_data_copy.reason = this.tagl_ana_reason_open
					return;
				}
				if(this.$HUCheck.check(this.tagl_ana_opened_data,this.tagl_ana_closed_data)){
					this.$alert('变更理由不能与上次重复!!');
//					this.tagl_ana_data_copy.reason = this.tagl_ana_reason_open
					return;
				}
				this.$emit('dialog_close', [true, this.tagl_ana_data_copy]);
				this.show = false;
			},
			setDate(val){
				this.tagl_ana_data_copy.new_date = val
			}
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

<style scoped="scoped">
/* g_dialog是base式样，g_dialog_ex需要扩展，根据需要自行调整，尤其是width，请自行添加*/
.g_dialog {
	/*width: 22%;*/
    margin: 10% auto 0;        
    border-radius: 2px;
    padding: 15px;
    background: white;
    -webkit-box-shadow: 0 1px 3px rgba(0,0,0,.3);
    box-shadow: 0 1px 3px rgba(0,0,0,.3);
}
.g_dialog_ex {
	width: 22%;	
	margin-top: 15%;
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
.g_dialog_header .section_right {
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
.g_dialog_body .s_section{
    width: 100%;        
    vertical-align: middle;
    margin: 15px 0;	
}

.g_dialog_body .s_section .s_left{
    width: 30%;        
    text-align: right;    
    padding-right: 10px;
    display: inline-block;        
}

.g_dialog_body .s_section .s_right{
    width: 60%;       	
}
.g_dialog_body .s_section .s_title{
    margin-bottom: 5px;  	
}

.g_dialog_body .s_section .s_textarea{	
	/* width: 215px;*/
	vertical-align: middle;
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
