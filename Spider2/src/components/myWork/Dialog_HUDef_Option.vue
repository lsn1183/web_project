<template>
	<div class="g_dialog_shadow" v-show="show">
			<div class="g_dialog g_dialog_ex">
				<!-- dialog标题 -->
				<h2 class="g_dialog_header">
					<span class="s_section_left">オプション項目</span>
					<!-- 点x关闭弹出框 -->
					<i class="s_section_right s_close el-icon-close" @click="close()"></i>
				</h2>
				<div class="g_dialog_body">	    	  	    	    	  	    
    	  	    	<p class="s_section">
    	  	    		<span class="s_left">AMP</span>
						<el-select class="s_right" v-model="HU_all_data.amp" placeholder="请选择" size='small'>
						    <el-option v-for="item in AMP" :key="item.value" :label="item.value" :value="item.value" >
						      <span>{{ item.value }} : {{ item.label }}</span>							      
						    </el-option>
						</el-select>		    	  	    		
    	  	    	</p>	  	    
    	  	    	<p class="s_section">
    	  	    		<span class="s_left">DSRC</span>
						<el-select class="s_right" v-model="HU_all_data.dsrc" placeholder="请选择" size='small'>
						    <el-option v-for="item in DSRC" :key="item.value" :label="item.value" :value="item.value" >
						      <span>{{ item.value }} : {{ item.label }}</span>							      
						    </el-option>
						</el-select>		    	  	    		
    	  	    	</p>	

    	  	    	<p class="s_section">
    	  	    		<span class="s_left">DCM</span>
						<el-select class="s_right" v-model="HU_all_data.dcm" placeholder="请选择" size='small'>
						    <el-option v-for="item in DCM" :key="item.value" :label="item.value" :value="item.value" >
						      <span>{{ item.value }} : {{ item.label }}</span>							      
						    </el-option>
						</el-select>		    	  	    		
    	  	    	</p>

    	  	    	<p class="s_section">
    	  	    		<span class="s_left">RSE</span>
						<el-select class="s_right" v-model="HU_all_data.rse" placeholder="请选择" size='small'>
						    <el-option v-for="item in RSE" :key="item.value" :label="item.value" :value="item.value" >
						      <span>{{ item.value }} : {{ item.label }}</span>							      
						    </el-option>
						</el-select>		    	  	    		
    	  	    	</p>
    	  	    	
    	  	    	<p class="s_section">
    	  	    		<span class="s_left">TouchPad</span>
						<el-select class="s_right" v-model="HU_all_data.touch_pad" placeholder="请选择" size='small'>
						    <el-option v-for="item in TouchPad" :key="item.value" :label="item.value" :value="item.value" >
						      <span>{{ item.value }} : {{ item.label }}</span>							      
						    </el-option>
						</el-select>		    	  	    		
    	  	    	</p>
    	  	    
	    	  	    <p class="s_section">
    	  	    		<span class="s_left">SeparateDisp</span>
						<el-select class="s_right" v-model="HU_all_data.separate_disp" placeholder="请选择" size='small'>
						    <el-option v-for="item in SeparateDisp" :key="item.value" :label="item.value" :value="item.value" >
						      <span>{{ item.value }} : {{ item.label }}</span>							      
						    </el-option>
						</el-select>		    	  	    		
    	  	    	</p>    	 
    	  	    	
	    	  	    <p class="s_section">
    	  	    		<span class="s_left">システム構成</span>	    	  	    		
    	  	    		<el-input class="s_right s_textarea" type="textarea" :rows="5" v-model="HU_all_data.system_conf"></el-input>	    	  	    				    	  	    		
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
		props: ['hu_data', 'dialog_show','arl_system_conf'],
		data() {
			return {
				show : false,
				HU_all_data : {},
				hu_open_data:'',
				hu_close_data:'',
				AMP: [
					{
			        	value: '0',
			        	label: 'don’t care'
			      	},
			      	{
			        	value: '1',
			        	label: 'MOSTAMP'
			        }, 
			        {
			          value: '2',
			          label: 'D0AMP(AVCLAN外付け)'
			        }, 
			        {
			          value: '3',
			          label: 'D4AMP(内臓)'
			        }
			    ],
				DSRC: [
					{
			        	value: '0',
			        	label: 'don’t care'
			        },
			        {
			        	value: '1',
			        	label: '無'
			        },
			        {
			          value: '2',
			          label: 'USB接続'
			        }, 
			        {
			          value: '3',
			          label: 'LAN接続'
			        },
			        {
			          value: '2/3',
			          label: 'USB接続/LAN接続'
			        }
			    ],
				DCM: [
					{
			        	value: '0',
			        	label: 'don’t care'
			        }, 
			        {
			        	value: '1',
			        	label: '無'
			        },
			        {
			          value: '2',
			          label: '有'
			        }
			    ],
				RSE: [
					{
			        	value: '0',
			        	label: 'don’t care'
			        }, 
			        {
			        	value: '1',
			        	label: '無'
			        }, 
			        {
			          value: '2',
			          label: 'フルRSE/シートバックRSE'
			        },
			        {
			          value: '3',
			          label: '簡易RSE'
			        },
			        {
			          value: '2/3',
			          label: 'フルRSE/シートバックRSE/簡易RSE'
			        }
			    ],
				TouchPad: [
					{
			        	value: '0',
			        	label: 'don’t care'
			        }, 
			        {
			        	value: '1',
			        	label: '無'
			        }, 
			        {
			          value: '2',
			          label: '有'
			        }
			    ],
				SeparateDisp: [
					{
			        	value: '0',
			        	label: 'don’t care'
			        }, 
			        {
			        	value: '1',
			        	label: '無'
			        }, 
			        {
			          value: '2',
			          label: '有'
			        	}
			    ],
				
				HU_option_data_check:{},
				option_value_check:[],
				old_system_conf:'',
				node_data:'',
				count:'',
				value_amp:'',
				value_dsrc:'',
				value_dcm:'',
				value_rse:'',
				value_touch_pad:'',
				value_separatedisp:'',
			}
		},
		created:function(){
		},
		methods: {
			onshow() {
				this.HU_all_data = JSON.parse(JSON.stringify(this.hu_data));
				this.hu_open_data = JSON.stringify(this.HU_all_data)
				this.$axios.get(this.Ip+'/HuOption')
					.then(res =>{
						this.HU_option_data_check = res.data;
						this.show = true;
					})
			},
			save() {
					this.show = false;
					this.$emit('dialog_close', [true, this.HU_all_data]);
				
			},
			//取消和dialog的关闭
			close(){
				this.hu_close_data = JSON.stringify(this.HU_all_data)
//				this.$message.closeAll()
				if (this.hu_close_data == this.hu_open_data) {
					this.$emit('dialog_close', [false, this.HU_all_data]);
					this.show = false;
				} else{
					this.$confirm('您有未提交的内容，确定离开?','提示',{
				    		confirmButtonText:"确定",
				    		cancelButtonText:"取消",
				    		type:"warning"
				    		
				   }).then(() => {
						this.$emit('dialog_close', [false, this.HU_all_data]);
						this.show = false;
				    }).catch(() => {
				    	
				    })
				}
			},
		},
		watch : {
			dialog_show() {
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
	/*width: 22%;*/	
	min-width: 369.38px;
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
    /*border: 1px solid #ccc;*/
}

.g_dialog_body .s_section .s_right{
    width: 60%;            	
}

.g_dialog_body .s_section .s_textarea{	
	vertical-align: middle;
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
