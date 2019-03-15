<template>
	<div class="g_dialog_shadow" v-show="show">
		<div class="g_dialog g_dialog_ex">
			<!-- dialog标题 -->
			<h2 class="g_dialog_header">
				<span class="s_section_left">其他</span>
				<!-- 点x关闭弹出框 -->
				<i class="s_section_right s_close el-icon-close" @click="close()"></i>
			</h2>
			<div class="g_dialog_body g_dialog_body_ex">
				<p class="s_section">	
	  	    		<span class="s_left">担当</span>
					<el-input class="s_right s_textarea" v-model="hu_data_copy.author" disabled></el-input>	    	  	    		
	  	    	</p>
				<p class="s_section">	
	  	    		<span class="s_left">テスト結果</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.test_results"></el-input>	    	  	    		
	  	    	</p>	
	  	        <p class="s_section">
	  	    		<span class="s_left">未要件分析</span>
					<el-select class="s_right s_select" v-model="hu_data_copy.future_req" size='small'>
					    <el-option v-for="item in NO_ANALYSIS" :key="item.value" :label="item.label" :value="item.value"></el-option>
					</el-select>
	  	    	</p>
	  	    	<p class="s_section">
	  	    		<span class="s_left">備考1</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.remark1"></el-input>			    	  	    		
	  	    	</p>
	  	    	<p class="s_section">
	  	    		<span class="s_left">備考2</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.remark2"></el-input>			    	  	    		
	  	    	</p>	
	  	    	<p class="s_section">
	  	    		<span class="s_left">要件漏れチェック</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.leak_check"></el-input>			    	  	    		
	  	    	</p>
    	  	    <p class="s_section">
	  	    		<span class="s_left">最終修正担当</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.last_modifier"></el-input>			    	  	    		
	  	    	</p>    
	  	    	<p class="s_section">
	  	    		<span class="s_left">日付</span>
	  	    		<el-date-picker class="s_right s_textarea" type="date" placeholder="选择日期" v-model="hu_data_copy.new_date" format @change="setDate"></el-date-picker>		    	  	    		
	  	    	</p>
	  	    	<p class="s_section">
	  	    		<span class="s_left">除外</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="hu_data_copy.exception"></el-input>			    	  	    		
	  	    	</p>  
    	    </div>
	   	   	<div class="g_dialog_footer s_confirmcancel">
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
				hu_before_reason:'',
				hu_after_reason:'',
				
				NO_ANALYSIS: [
						{
				        	value: '○',
				        	label: '○'
				      	},
				        {
				          value: '×',
				          label: '×'
				        },
				        {
				          value: ' ',
				          label: ' '
				        }
				    ], 
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
				this.hu_close_data = JSON.stringify(this.hu_data_copy)
				this.$emit('dialog_close', [true, this.hu_data_copy]);
				this.show = false;
			},
			setDate(val){
				this.hu_data_copy.new_date = val
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
	min-width: 380px;
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
.g_dialog_header .s_close {
	font-size: 14px; 	
} 
.g_dialog_body{
	font-size: 14px;    
    border-top: 1px solid rgb(225,225,225);
    border-bottom : 1px solid rgb(225,225,225);
    padding: 10px;
}
.g_dialog_body_ex {
	
}
.g_dialog_body .s_section{
    width: 100%;        
    vertical-align: middle;
    margin: 15px 0;
    
    padding-left: 15px;    	
}
.g_dialog_body .s_section .s_left{
    width:36%;        
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
.g_dialog_body .s_section .s_select{	
	width: 50%;
}
.g_dialog_footer{
	height: 36px;
	width: 100%;
	margin-top: 15px;			
}
.g_dialog_footer .s_section_right,.s_confirmcancel{
	text-align: right;
}

</style>
