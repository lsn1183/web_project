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
    	  	    	<div class="s_section center_select">	
    	  	    		
    	  	    		<p class="s_section">
		  	    			<!--<span class="s_left">小分类</span>-->
		  	    			<el-select v-model="HMI_status" placeholder="请选择" class="s_right s_select">
	     						<el-option class="s_right s_textarea" v-for="item in array_for_option" :key="item.value" :label="item.value" :value="item.value"></el-option>
	     					</el-select>		    	  	    		
		  	    		</p> 
		  	    		
		  	    		<!--<p class="s_section">
		  	    			<span class="s_left">中分类</span>
		  	    			<el-select v-model="HMI_status" placeholder="请选择" class="s_right s_select">
	     						<el-option class="s_right s_textarea" v-for="item in array_for_option" :key="item.value" :label="item.value" :value="item.value"></el-option>
	     					</el-select>		    	  	    		
		  	    		</p> -->

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
				HMI_status:'',
				array_for_option:[],
				array_development_state : [],
//				array_development_state: [
//					{
//			        	value: '完成',
//			        	label: '完成'
//			        },
//			        {
//			          value: 'HMI制御',
//			          label: 'HMI制御'
//			        },
//			        {
//			        	value: 'Service制御',
//			        	label: 'Service制御'
//			        },
//			        {
//			        	value: 'Service不備',
//			        	label: 'Service不備'
//			        },
//			        {
//			        	value: 'ServiceIF不明',
//			        	label: 'ServiceIF不明'
//			        },
//			        {
//			        	value: '调整（设备依赖）',
//			        	label: '调整（设备依赖）'
//			        },
//			        {
//			        	value: '调整（依赖非TAGL范围的Service）',
//			        	label: '调整（依赖非TAGL范围的Service）'
//			        },
//			        {
//			        	value: '调整（依赖其他APP，无法测试）',
//			        	label: '调整（依赖其他APP，无法测试）'
//			        },
//			        {
//			        	value: '未联调',
//			        	label: '未联调'
//			        },
//			        {
//			        	value: '联调中',
//			        	label: '联调中'
//			        },
//			        {
//			        	value: '需要QA',
//			        	label: '需要QA'
//			        },
//			        {
//			        	value: '同件',
//			        	label: '同件'
//			        },
//			        {
//			        	value: '完成(联调完成，有Bug)',
//			        	label: '完成(联调完成，有Bug)'
//			        },
//			        {
//			        	value: '调整（TAGL分析非Application对应)',
//			        	label: '调整（TAGL分析非Application对应)'
//			        },
//			        {
//			        	value: '调整（TAGL除外）',
//			        	label: '调整（TAGL除外）'
//			        },
//			        {
//			        	value: '效确NG',
//			        	label: '效确NG'
//			        },
//			        {
//			        	value: '调整（无TAGL分析要件ID）',
//			        	label: '调整（无TAGL分析要件ID）'
//			        },
//			        {
//			        	value: '调整（TAGL分析无时序图）',
//			        	label: '调整（TAGL分析无时序图）'
//			        },
//				],
				array_test_result: [
					{
			        	value: '完成',
			        	label: '完成'
			        },
			        {
			          value: '未完成',
			          label: '未完成'
			        },
			        {
			        	value: ' ',
			        	label: ' '
			        },
				],
				array_APL_Dalian_Correspondence: [
					{
			        	value: ' ',
			        	label: ' '
			        },
			        {
			          value: '是',
			          label: '是'
			        },
			        {
			        	value: '否',
			        	label: '否'
			        },
				],
				show : false,
				hu_data_copy : {},
				hu_open_data:'',
				hu_close_data:'',
				
			}
		},
		mounted(){
			this.get_HmiDevStatus()
		},
		methods: {
			get_HmiDevStatus(){
				this.$axios.get(this.Ip + '/HmiDevStatus')
				.then(res => {
					let development_state_data =[]
					development_state_data = JSON.parse(JSON.stringify(development_state_data))
					for(let i = 0;i<res.data.content.length;i++){
						this.array_development_state.push({
					        	value: development_state_data[i].status,
					        	label: development_state_data[i].status
			       		})
					}
//					this.array_development_state = JSON.parse(JSON.stringify(res.data.content).replace(/status_id/g,'label').replace(/status_name/g,'value'))
				})
				.catch(res =>{})
			},
			onshow() {
				this.hu_data_copy = JSON.parse(JSON.stringify(this.hu_data));
				this.show = true;
			},
			close() {
		    	this.$emit('dialog_close', [false, this.hu_data]);
				this.show = false;
			},
			save(){
				if(this.HMI_params == '开发状态'){
					this.hu_data.dev_status = this.HMI_status
				}else if(this.HMI_params == 'APL是否为大连对应'){
					this.hu_data.is_dalian = this.HMI_status;
				}else{
					
				}
				this.$emit('dialog_close', [true, this.hu_data]);
				this.show = false;
			},
		},

		watch : {
			dialog_show(v) {
				if (this.dialog_show) {
					if(this.HMI_params == '开发状态'){
						this.array_for_option = this.array_development_state;
						this.HMI_status = this.hu_data.dev_status
					}else if(this.HMI_params == 'APL是否为大连对应'){
						this.HMI_status = this.hu_data.is_dalian
						this.array_for_option = this.array_APL_Dalian_Correspondence;
					}else{
						
					}
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
.g_dialog_body .center_select{
	text-align: center;
}
</style>
