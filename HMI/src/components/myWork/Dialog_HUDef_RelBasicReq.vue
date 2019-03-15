<template>
	<div class="g_dialog_shadow" v-show="show">
			<div class="g_dialog g_dialog_ex">
				<!-- dialog标题 -->
				<h2 class="g_dialog_header">
					<span class="s_section_left">{{HMI_params}}</span>
					<!-- 点x关闭弹出框 -->
					<i class="section_right close el-icon-close" @click="close()"></i>
				</h2>
				<div class="g_dialog_body">	    	  	    	    	  	    
    	  	    	<!-- TAGL表格 -->
    	  	    	<div class="s_section">		    	     								
						<el-input v-if="this.input_percent_type == 'text'?true:false" class="s_textarea" type="textarea" :rows="5" v-model="input_data"></el-input>
						<el-input v-if="this.input_percent_type == 'number_limit_area'?true:false" type="textarea" v-model="input_data" @change="checkNum" :maxlength=3 onkeypress="return event.keyCode>=48&&event.keyCode<=57" size="small" ></el-input>	
						<el-input v-if="this.input_percent_type == 'number_only'?true:false" type="number" v-model="input_data"></el-input>
						<el-date-picker v-if="this.input_percent_type == 'date'?true:false" type="date" class="s_right s_textarea"  placeholder="选择日期" v-model="input_data" format @change="setDate"></el-date-picker>
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
	export default{
		props: ['hu_data', 'dialog_show','HMI_params'],

		data() {
			return {
				show : false,
				hu_data_copy : {},
//				array_development_state:['未联调','联调中','需要QA','同件','完成(联调完成，有Bug)','调整（TAGL分析非Application对应)','调整（TAGL除外）','效确NG','','调整（无TAGL分析要件ID）','调整（TAGL分析无时序图）']
				input_data:'',
				input_percent_type : 'text'
			}
		},
		
		methods: {
			onshow() {
				this.input_percent_type = 'text'
				switch (this.HMI_params){
					case 'ScreenID':
						this.input_data = this.hu_data.screen_id
						break;
					case 'APL是否为大连对应':
						this.input_data = this.hu_data.is_dalian
						break;
					case '负责人':
						this.input_data = this.hu_data.charger
						break;
					case '担当':
						this.input_data = this.hu_data.author
						break;	
					case 'APL日程':
						this.input_data = this.hu_data.apl_schedule
						this.input_percent_type = 'date'
						break;	
					case '结合日程':
						this.hu_data.it_schedule  = this.input_data
						this.input_percent_type = 'date'
						break;		
					case 'APL进度':
						this.input_data = this.hu_data.apl_progress
						this.input_percent_type = 'number_limit_area'
						break;	
					case '结合测试进度':
						this.input_data = this.hu_data.it_progress
						break;
					case '结合测试Release版本':
						this.input_data = this.hu_data.it_release_ver
						break;
					case '开发状态':
						this.input_data = this.hu_data.dev_status
						this.input_percent_type = 'number_limit_area'
						break;
					case '备考':
						this.input_data = this.hu_data.dev_remark
						break;
					case '外部QA番号':
						this.input_data = this.hu_data.external_qa
						break;
					case '内部QA番号':
						this.input_data = this.hu_data.internal_qa
						break;
					case 'NG次数':
						this.input_data = this.hu_data.ng_num
						this.input_percent_type = 'number_only'
						break;
					default:
						break;
				}
				this.show = true;
				
			},

			close() {
		    	this.$emit('dialog_close', [false, this.hu_data]);
				this.show = false;
			},
			save(){
				switch (this.HMI_params){
					case 'ScreenID':
						this.hu_data.screen_id = this.input_data
						break;
					case 'APL是否为大连对应':
						this.hu_data.is_dalian = this.input_data
						break;
					case '负责人':
						this.hu_data.charger = this.input_data
						break;
					case '担当':
						this.hu_data.author = this.input_data
						break;	
					case 'APL日程':
						this.hu_data.apl_schedule = this.input_data
						break;	
					case '结合日程':
						this.hu_data.it_schedule  = this.input_data
						break;	
					case 'APL进度':
						this.hu_data.apl_progress = parseInt(this.input_data)
						this.input_percent_type = true
						break;	
					case '结合测试进度':
						this.hu_data.it_progress = parseInt(this.input_data)
						break;
					case '结合测试Release版本':
						this.hu_data.it_release_ver = this.input_data
						break;
					case '开发状态':
						this.hu_data.dev_status = parseInt(this.input_data)
						break;
					case '备考':
						this.hu_data.dev_remark = this.input_data
						break;
					case '外部QA番号':
						this.hu_data.external_qa = this.input_data
						break;
					case '内部QA番号':
						this.hu_data.internal_qa = this.input_data
						break;
					case 'NG次数':
						this.hu_data.ng_num = parseInt(this.input_data)
						break;
					default:
						break;
				}
				this.$emit('dialog_close', [true, this.hu_data]);
				this.show = false;
			},
			checkNum(){
				let reg = /^[0-9]*$/g;
				if(new RegExp(reg).test(this.input_data) == false){
					this.input_data = ''
				}else{
					this.input_data = this.input_data.replace(/\b(0+)/gi,'')
					if(this.input_data > 100){
						this.input_data = 100
					}else{
						
					}
				}
			},
			setDate(val){
				this.input_data = val
			}
		},

		watch : {
			dialog_show(v) {
				if (this.dialog_show) {
					this.onshow();
				}else{
					
				}
			},
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
    text-align: center;
    margin: 15px 0;	
}

.g_dialog_body .s_section .s_left{
    width: 30%;        
    text-align: right;    
    padding-right: 10px;
    display: inline-block;        
}

.g_dialog_body .s_section .s_right{
                	
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
