<template>
	<div class="g_dialog_shadow" id="HUWorkerDialog" v-show="show">
			<div class="g_dialog g_dialog_ex">
				<!-- dialog标题 -->
				<h2 class="g_dialog_header s_header_ex">
					<span class="s_section_left">責務分担</span>
					<!-- 点x关闭弹出框 -->
					<i class="s_section_right s_close el-icon-close" @click="close()"></i>
				</h2>
				<div class="g_dialog_body g_dialog_body_ex">	 
		   	    	<div class="s_span s_title_top">
		   	    		<span class="s_span s_span_second g_button"  @click="add_new()"><i class="el-icon-plus"> 新增</i></span>
		   	    	</div>
					<div class="s_workerl_table">
<!--			   	    	<div style="clear: both;"></div>-->
						<!-- ARL表格 -->
						<div  v-for="(seq_info, index) in tagl_def_seq_list" class="s_worker_section">
							<!-- arl的复制删除等功能目前不做 -->
						 	<div class="s_title ">
						 		<span class="fl "><i class="el-icon-arrow-right" @click="accordion(1,index)"></i>
										<el-cascader expand-trigger="hover" :options="tagl_def_all_responsible_list" v-model="tagl_def_reponsible_select_list[index]">
										</el-cascader>
						 		</span>
								
								<span class="g_button" @click="del_seq(index)"><i class="el-icon-edit" > 删除</i></span>
								<span class="g_button" @click="move_up(index)"><i class="el-icon-arrow-up" :class="index==0?'btn_shadow':''"> 上移</i></span>
								<span class="g_button" @click="move_down(index)"><i class="el-icon-arrow-down" :class="index==DataLength-1?'btn_shadow':''"> 下移</i></span>
								
						 	</div>
						 	 <!-- 数据只做显示 -->
			    	     	<div class="s_ana_table">
			    	     		<!-- 这个是只显示重要信息的  只留一个s_table_content 渲染就好 重要信息是长显示-->
			    	     		<div class='s_table_content' style="width:100%">
			    	     			<p class="s_table_title">
			    	     				<span>動作</span>
			    	     			</p>
			    	     			<p class="s_table_textarea">
			    	     				<el-input type="textarea" :autosize="{minRows:5, maxRows:5}" resize='none' v-model="seq_info.action"></el-input>
			    	     			</p>
			    	     		</div>
			    	     	</div>   
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
	export default{
		props: ['tagl_ana_data', 'dialog_show'],

		data() {
			return {
				arl_more : false,
				DataLength:'',
				show : false,
				tagl_ana_data_copy : {},
				tagl_def_seq_list : [],
				
				//存放每个modelid所对应的层级名称list
				tagl_def_model_list_id_select_dict : {}, 
				//存放每个modelid所对应的
				tagl_def_model_list_id_name_dict : {}, 
			    //責務分担选项list
				tagl_def_all_responsible_list : [],
				//責務分担选择list
				tagl_def_reponsible_select_list : [],
				tagl_ana_opened_data: '',
				tagl_ana_closed_data: '',
			}
		},

		methods: {
			onshow() {
				this.tagl_ana_data_copy = JSON.parse(JSON.stringify(this.tagl_ana_data));
				this.tagl_ana_opened_data = JSON.stringify(this.tagl_ana_data_copy.sequence_list);
				this.tagl_def_seq_list = this.tagl_ana_data_copy.sequence_list;
				this.DataLength = this.tagl_def_seq_list.length

				this.tagl_def_all_responsible_list = [];
				this.tagl_def_reponsible_select_list = [];
				this.tagl_def_model_list_id_select_dict = {}

				this.$axios.get(this.Ip+'/ForestModelTypes/analysis')
					.then(res => {
						let model_info_list = res.data;
						this.tagl_def_recursive_responsible_list(this.tagl_def_all_responsible_list, model_info_list);
						this.tagl_def_recursive_model_list_id_dict([],model_info_list)
						this.tagl_def_init_reponsible_select_list();
						this.show = true;
					})
					.catch(res=>{
					
					});
			},

			tagl_def_recursive_model_list_id_dict(parent_str_list, source_list) {
				for (let model_dict of source_list) {
					let now_parent_str_list = [...parent_str_list];
					if (model_dict.sub_list.length == 0) {
						now_parent_str_list.push(model_dict['model_id'])
						this.tagl_def_model_list_id_select_dict[model_dict['model_id']] = now_parent_str_list
						if ('info' in model_dict) {
							this.tagl_def_model_list_id_name_dict[model_dict['model_id']] = {name:model_dict['name'],
																					info:model_dict['info']}	
						}
						else {
							this.tagl_def_model_list_id_name_dict[model_dict['model_id']] = {name:model_dict['name'],
																					info:''}
						}
					}
					else {
						now_parent_str_list.push(model_dict['name'])
						this.tagl_def_recursive_model_list_id_dict(now_parent_str_list, model_dict.sub_list);
					}
				}
			},
			
			tagl_def_recursive_responsible_list(dest_list, source_list) {
				for (let model_dict of source_list) {
					let dest_model_dict = {}
					dest_model_dict['label'] = model_dict['name']					

					if (model_dict.sub_list.length > 0) {
						dest_model_dict['children'] = []
						dest_model_dict['value'] = model_dict['name']
						this.tagl_def_recursive_responsible_list(dest_model_dict['children'], model_dict.sub_list)
					}
					else {
						dest_model_dict['value'] = model_dict['model_id']
					}

					dest_list.push(dest_model_dict)
				}
			},

			tagl_def_init_reponsible_select_list() {
				for (let hu_data of this.tagl_def_seq_list) {
					let tmp_responsible_list = []
					if (hu_data.type == "DEVICE") {
						this.tagl_def_reponsible_select_list.push(this.tagl_def_model_list_id_select_dict[hu_data.id]);
					}
				}
			},

			add_new(){
				this.tagl_def_reponsible_select_list.push([]);
				this.tagl_def_seq_list.push (
					{ 
                        id: null,
						name: "", 
						info: "",
						type: "",
                        status: "",
						trigger:"("+(this.tagl_def_seq_list.length+1)+")", 
						action: "("+(this.tagl_def_seq_list.length+1)+")", 
					}
				)
				this.DataLength = this.tagl_def_seq_list.length
			},

			del_seq(index){
				this.$confirm('是否删除此条记录？','提示',{
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
				}).then(()=>{
					this.tagl_def_reponsible_select_list.splice(index,1);
					this.tagl_def_seq_list.splice(index,1);
					this.DataLength = this.tagl_def_seq_list.length
				})
				.catch(()=>{
				})
				
			},

			close() {
				this.tagl_ana_closed_data = JSON.stringify(this.tagl_ana_data_copy.sequence_list);
				if (this.tagl_ana_closed_data == this.tagl_ana_opened_data) {
					this.$emit('dialog_close', [false, this.tagl_ana_data_copy]);
					this.show = false;
				} else{
					this.$confirm('您有未提交的内容，确定离开?','提示',{
				    		confirmButtonText:"确定",
				    		cancelButtonText:"取消",
				    		type:"warning"
				    		
				    }).then(() => {
				    	this.$emit('dialog_close', [false, this.tagl_ana_data_copy]);
						this.show = false;
				    }).catch(() => {
				    	
				    })
				}
				
			},

			save(){
				for (let i=0; i < this.tagl_def_seq_list.length; i++){
					if (this.tagl_def_reponsible_select_list[i].length < 1){
						this.$alert('请选择責務分担！');
						return;
					}

					this.tagl_def_seq_list[i].type = "DEVICE";
					this.tagl_def_seq_list[i].id = this.tagl_def_reponsible_select_list[i][this.tagl_def_reponsible_select_list[i].length-1];
					this.tagl_def_seq_list[i].name = this.tagl_def_model_list_id_name_dict[this.tagl_def_seq_list[i].id].name;
					if (this.tagl_def_model_list_id_name_dict[this.tagl_def_seq_list[i].id].info.length > 0) {
						this.tagl_def_seq_list[i].info += this.tagl_def_model_list_id_name_dict[this.tagl_def_seq_list[i].id].info;	
					}
					this.tagl_def_seq_list[i].status = "";
					this.tagl_def_seq_list[i].trigger = "";

                    if (this.SpiderCheck.check_data(this.SpiderCheck.CHECK_COMMON_RESPOINSIBLE_DEVICE, this.tagl_def_seq_list[i].action) == false){
						this.$alert('動作格式不正确!!');
						return;
					}
					
				}
				
				if (!this.SpiderCheck.check_data(this.SpiderCheck.CHECK_COMMON_RESPONSIBLE_SEQ_NUMBER, this.tagl_def_seq_list)) {
					this.$alert("序号不正确！")
					return;
				}

				this.$emit('dialog_close', [true, this.tagl_ana_data_copy]);
				this.show = false;
			},
			move_up(index){
				let src_index = index;
				let dest_index = index-1;
				if (dest_index < 0){
					return;
				}
				
				this.tagl_def_seq_list = this.swap_item(this.tagl_def_seq_list, src_index, dest_index);
				this.tagl_def_reponsible_select_list = this.swap_item(this.tagl_def_reponsible_select_list, src_index, dest_index);
			},

			move_down(index) {
				let src_index = index;
				let dest_index = index+1;
				if (dest_index >= this.tagl_def_seq_list.length) {
					return;
				}

				this.tagl_def_seq_list = this.swap_item(this.tagl_def_seq_list, src_index, dest_index);
				this.tagl_def_reponsible_select_list = this.swap_item(this.tagl_def_reponsible_select_list, src_index, dest_index);
			},

			swap_item(swap_list, src_index, dest_index) {
				swap_list[src_index] = swap_list.splice(dest_index, 1, swap_list[src_index])[0]
				return swap_list
			},
			accordion(table_id,index,definition_index){
				if(table_id==1){
					$(".s_table").eq(index).toggle(function(){
					})
				}
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
    margin: 10% auto 0;        
    border-radius: 2px;
    padding: 15px;
    background: white;
    -webkit-box-shadow: 0 1px 3px rgba(0,0,0,.3);
    box-shadow: 0 1px 3px rgba(0,0,0,.3);
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
    height: 30px;
    line-height: 30px;
    margin-bottom: 12px;
    font-size:18px;
}
.s_header_ex{
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
.g_dialog_body{
	font-size: 14px;    
    border-top: 1px solid rgb(225,225,225);
    border-bottom : 1px solid rgb(225,225,225);
    padding: 20px;
}
.g_dialog_body_ex{
	height: 677px;
	padding-top: 0;
	border-top: 0px solid rgb(225,225,225);
}
.g_dialog_body .s_section{
    border: solid 1px #bfcbd9;
	overflow: hidden;
}
.g_dialog_body .s_section .s_section_children{
	text-align: center;
    float:left;
    border-right: solid 1px rgb(225,225,225);  
}

.g_dialog_body .s_section .s_section_bottom .s_section_children{
	height: 102px;
}
.g_dialog_body .s_section .s_section_table_select{
    width: 26%;
    vertical-align: middle;
}
.g_dialog_body .s_section .s_section_table_textarea{
    width: 18%;
}
.g_dialog_body .s_section .s_section_table_act{
    width: 20%;
    border-right: solid 0px #ccc;  
}
.g_dialog_body .s_section .s_section_children_ex{
    padding:0 1%;  
    font-size: 14px;
    font-weight:bold;
}
.g_dialog_body .s_section .s_section_bottom .s_section_bottom_item{
	height: 100%;
	margin: 0;
	border-bottom: solid 1px #bfcbd9;
}

.g_dialog_body .s_section .left{
    width: 30%;        
    text-align: right;    
    padding-right: 10px;
    display: inline-block;        
}

.g_dialog_body .s_section .right{
                	
}


.g_dialog_body .s_section .s_section_top{
      height:36px;
      background-color: #eef1f6;
      border-bottom: solid 1px #bfcbd9; 
      padding-right: 8px;     
      /*overflow-y: scroll;*/    	
}

.g_dialog_body .s_section .s_section_bottom{
    width: 100%;
    overflow-y: scroll;
    vertical-align: middle;
    height: 570px;         	
}
.g_dialog_body .s_section .textarea{	
	width: 215px;
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
.btn_shadow{
	color: #ccc;
}
.s_span{
	border-bottom: none;
}
.s_span_second{
	font-weight:bold;
	margin-right:30px;
}
.s_title_top{
	height:40px;
	width:100%;
	margin-right:27px;
	line-height:40px;
	border-bottom:1px solid #dfe6ec;
}

.s_span span{
	height: 40px;
	line-height: 40px;
	cursor: pointer;
	margin-right:28px;
}
.s_span .fr:hover{
	color: #42b983;
}

.g_button{
	float: right;
	color: #42b983;
}

.s_workerl_table{
	overflow-y: scroll;
	height:93%;	
}
.s_title{
	font-weight: bold;
	height: 40px;
	line-height: 40px;
	background: rgba(238,241,246,.2);
	transition: 0.9s;
	width: 100%;
	padding-left: 15px;
}
/*.s_title:hover{
	background: rgba(238,241,246,.9);
}*/
.s_title>div>span{
	font-weight: normal;
	
}
.s_title span{
	cursor: pointer;
	margin-right:20px;
}
.s_title .fr:hover{
	color: #42b983;
}
.s_table_content{
	float: left;
	width:200px;
	border-right: 1px solid #dfe6ec;
	/*height:149px;*/ 
}
.s_table_title{
	height: 30px;
	line-height: 30px;
	font-weight: bold;
	text-align: center;
	background: #eef1f6;
	font-size: 14px;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
		background-color: #fbfdff;
	border-bottom: solid 1px #dfe6ec;
}
.s_table_textarea{
	overflow: hidden;
	text-overflow: ellipsis;
	/*white-space: nowrap;*/
	/*height: 110px;*/
	font-size: 14px;
}
.s_ana_table{
	/*position:relative;*/
	/*height: 132px;*/
	border: 1px solid #dfe6ec;
	display: flex;

}
.s_worker_section{
	/*border-left: 1px solid #dfe6ec;
	border-bottom: 1px solid #dfe6ec;*/
}
</style>
