<template>
	<div class="g_dialog_shadow" v-show="show">
		<div class="g_dialog g_dialog_ex">
			<!-- dialog标题 -->
			<h2 class="g_dialog_header">
				<span class="s_section_left">参考文献</span>
				<!-- 点x关闭弹出框 -->
				<i class="s_section_right s_close el-icon-close" @click="close()"></i>
			</h2>
			<div class="g_dialog_body g_dialog_body_ex">
				<p class="s_section">		    	     	
	  	    		<span class="s_left s_left_ex">参考ウォークスルー図</span>
					<el-input class="s_right s_textarea_ex" type="textarea" :rows="1" v-model="tagl_def_data_copy.rel_hal_design"></el-input>	    	  	    		
	  	    	</p>	
	  	        <p class="s_section">
	  	    		<span class="s_left">参考HAL設計書</span>
					<el-input class="s_right s_textarea" type="textarea" :rows="1" v-model="tagl_def_data_copy.rel_flow_diagram"></el-input>			    	  	    		
	  	    	</p>
	  	    	<p class="s_section">
	  	    		<span class="s_left">その他仕様(リファハード仕様等)</span>
					<el-input class="s_right s_textarea_ex" type="textarea" :rows="1" v-model="tagl_def_data_copy.other_spec"></el-input>			    	  	    		
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
		props: ['tagl_def_data', 'hu_model_list', 'dialog_show'],

		data() {
			return {
				show : false,
				tagl_def_data_copy : {},
				tagl_def_opened_data: '',
				tagl_def_closed_data: '',
			}
		},

		methods: {
			onshow() {
				this.tagl_def_data_copy = JSON.parse(JSON.stringify(this.tagl_def_data));
				this.show = true;
				this.tagl_def_opened_data = JSON.stringify(this.tagl_def_data_copy)
			},

			close() {
				this.tagl_def_closed_data = JSON.stringify(this.tagl_def_data_copy)
				if(this.tagl_def_closed_data != this.tagl_def_opened_data){
					//修改数据 要执行的方法
					this.$confirm('您有未提交的内容，确定离开?','提示',{
				    		confirmButtonText:"确定",
				    		cancelButtonText:"取消",
				    		type:"warning"
				    		
				    }).then(() => {
				    	this.$emit('dialog_close', [false, this.tagl_def_data_copy]);
						this.show = false;
				    }).catch(() => {
				    	
				    })
					
				}else{
					//这个是数据一样（未改变）
					this.$emit('dialog_close', [false, this.tagl_def_data_copy]);
					this.show = false;
				}
				
			},
			save(){
					if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_TAGLDEF_REF_DOC, this.tagl_def_data_copy.rel_hal_design) == false){
						this.$alert('参考ウォークスルー図格式不正确!!');
						return;
					}
					if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_TAGLDEF_REF_DOC, this.tagl_def_data_copy.rel_flow_diagram) == false){
						this.$alert('参考HAL設計書格式不正确!!');
						return;
					}
					if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_TAGLDEF_REF_DOC, this.tagl_def_data_copy.other_spec) == false){
						this.$alert('その他仕様(リファハード仕様等)格式不正确!!');
						return;
					}
				
					this.$emit('dialog_close', [true, this.tagl_def_data_copy]);
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
	width: 19%;
	min-width: 340px;
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
    width:38%;        
    text-align: right;    
    padding-right: 10px;
    
    display: inline-block;        
    /*border: 1px solid #ccc;*/
}
.g_dialog_body .s_section .s_left_ex{
	letter-spacing: 4px;
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
.g_dialog_footer .s_section_right,.s_confirmcancel{
	text-align: right;
}

</style>
