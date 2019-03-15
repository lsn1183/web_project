<template>
	<div id="Statistic_Function" >
		<div style="position: absolute;top: 8px;">
			<b style="font-size: 15px;">预定完成日:</b>
			<el-date-picker
			v-model="date_value"
			type="date"
			placeholder="选择日期"
			@change="getTable">
			</el-date-picker>
		</div>
		<div id="Statistic_Table" v-loading.lock="fullscreenLoading">
			<div id="Statistic_Function_header">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;;border: solid 1px #dfe6ec;font-size: 14px;">
					<tr style="background-color:#eef1f6;width: 100%;">
						<th style="width: 10%;min-width: 100px;borderRight: none;">小组</th>
						<th style="width: 90%;borderLeft: none;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;max-height: 60px;">
								<tr>
									<td style="width: 10%;border:solid 1px #dfe6ec;max-width:120px;min-width:120px;" rowspan="2">担当</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 67px;" rowspan="2">ARL总数</td>
									<td style="border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;min-width: 198px;" colspan="3">HU要件定义</td>											
									<td style="border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;borderRight:solid 3px #dfe6ec;min-width: 198px;" colspan="3">TAGL要件定义</td>											
									<td style="border:solid 1px #dfe6ec;min-width: 198px;" colspan="3">TAGL要件分析</td>
								</tr>
								<tr >
									<td style="width: 9%;borderLeft:solid 3px #dfe6ec;min-width: 66px;">ARL完成数</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">HU要件定义总数</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">HU要件定义预定完成数</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;min-width: 66px;">ARL完成数</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">TAGL要件定义总数</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;borderRight:solid 3px #dfe6ec;min-width: 66px;">TAGL要件定义预定完成数</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">ARL完成数</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">TAGL要件分析总数</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">TAGL要件分析预定完成数</td>
								</tr>
							</table>
						</th>
					</tr>
				</table>
			</div>
			<div id="Statistic_Function_body">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;height: 60px;border: solid 1px #dfe6ec;font-size: 14px;border-bottom: none;" >
					<tr v-for="item in list_User" class="tr1_hover">
						<td style="width: 10%;overflow:hidden;text-overflow: ellipsis;min-width: 100px;border-right: none;">{{item.group_name}}</td>
						<td style="width: 90%;border: none;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;height: 100%;">
								<tr v-for="item_kids_kids in item.user_list" style="width: 100%;">
									<td style="width: 10%;height:30px;border:solid 1px #dfe6ec;max-width:120px;min-width:120px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;" :title="item_kids_kids.user_name">{{item_kids_kids.user_name}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;" >{{item_kids_kids.all_arl_num}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;min-width: 66px;">{{item_kids_kids.hu_arl_num}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{item_kids_kids.all_hu_num}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{item_kids_kids.hu_plan_num}}</td>				
									<td style="width: 9%;border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;min-width: 66px;">{{item_kids_kids.definition_hu_num}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{item_kids_kids.all_definition_num}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;borderRight:solid 3px #dfe6ec;min-width: 66px;">{{item_kids_kids.def_plan_num}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{item_kids_kids.analysis_def_num}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{item_kids_kids.analysis_num}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{item_kids_kids.analysis_plan_num}}</td>
								</tr>				    	
						    	
							</table>
						</td>
					</tr>
				</table>
			</div>
			<div style="position: absolute;bottom: 30px;width: 100%;overflow-y: scroll;overflow-x: auto;">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;height: 30px;border: solid 1px #dfe6ec;font-size: 14px;border-bottom: none;" >
					<tr class="tr1_hover">
						<td style="width: 19.08%;overflow:hidden;text-overflow: ellipsis;min-width: 100px;border-right: none;min-width: 220px;">{{Sum_Name}}</td>
						<td style="width: 80.9%;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;height: 100%;">
								<tr style="width: 100%;">
									<td style="width: 9%;border-right:solid 1px #dfe6ec;min-width: 66px;" >{{ARL_Sum}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;min-width: 66px;">{{HUDef_ARL_Sum}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{HUDef_Sum}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{HUDef_Plan_Sum}}</td>				
									<td style="width: 9%;border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;min-width: 66px;">{{TAGL_ARL_Sum}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{TAGLDef_Sum}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;borderRight:solid 3px #dfe6ec;min-width: 66px;">{{TAGLDef_Plan_Sum}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{TAGLAna_ARL_Sum}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{TAGLAna_Sum}}</td>
									<td style="width: 9%;border:solid 1px #dfe6ec;min-width: 66px;">{{TAGLAna_Plan_Sum}}</td>												
								</tr>
							</table>
						</td>
					</tr>
				</table>
			</div>
		</div>				
	</div>
</template>

<script>
		export default{
			mounted(){	
				this.getTable()
			},
			data(){
		      return {
		      	fullscreenLoading:false,
		      	list_User: [],
		      	date_value: '',
		      	
	      		Sum_Name: '总计',
	      		ARL_Sum:  0,
		      	HUDef_ARL_Sum: 0,
		      	HUDef_Sum: 0,
		      	HUDef_Plan_Sum: 0,
		      	
		      	TAGL_ARL_Sum: 0,
		      	TAGLDef_Sum: 0,
		      	TAGLDef_Plan_Sum: 0,
		      	
		      	TAGLAna_ARL_Sum: 0,
		      	TAGLAna_Sum: 0,
		      	TAGLAna_Plan_Sum: 0
		      }
		    },
		    methods: {
				getTable(val){
					this.fullscreenLoading = true
					this.ARL_Sum =0
					this.HUDef_ARL_Sum =0 
					this.HUDef_Sum =0
					this.TAGL_ARL_Sum =0
					this.TAGLDef_Sum =0
					this.TAGLAna_ARL_Sum =0 
					this.TAGLAna_Sum =0
					
					this.HUDef_Plan_Sum = 0 
					this.TAGLDef_Plan_Sum = 0
					this.TAGLAna_Plan_Sum =0
					if(this.date_value ==''){
						this.$axios.get(this.Ip+"/SummarizeByUser")
						.then(res =>{
							if(res.data.result == 'OK'){
								this.list_User = res.data.content
								for(var i=0;i<this.list_User.length;i++){
									for(var j=0;j<this.list_User[i].user_list.length;j++){
										if(this.list_User[i].user_list[j].all_arl_num == null){
												this.list_User[i].user_list[j].all_arl_num= 0
										}
										if(this.list_User[i].user_list[j].all_definition_num == null){
											this.list_User[i].user_list[j].all_definition_num= 0							
										}
										if(this.list_User[i].user_list[j].all_hu_num == null){
											this.list_User[i].user_list[j].all_hu_num= 0								
										}
										if(this.list_User[i].user_list[j].analysis_num == null){
											this.list_User[i].user_list[j].analysis_num= 0							
										}
										if(this.list_User[i].user_list[j].definition_hu_num == null){
											this.list_User[i].user_list[j].definition_hu_num= 0						
										}
										if(this.list_User[i].user_list[j].hu_arl_num == null){
											this.list_User[i].user_list[j].hu_arl_num= 0						
										}
										if(this.list_User[i].user_list[j].analysis_def_num == null){
											this.list_User[i].user_list[j].analysis_def_num= 0						
										}
										if(this.list_User[i].user_list[j].user_name == null){
											this.list_User[i].user_list[j].user_name= 0						
										}
										
										if(this.list_User[i].user_list[j].hu_plan_num == null){
											this.list_User[i].user_list[j].hu_plan_num= 0						
										}
										if(this.list_User[i].user_list[j].def_plan_num == null){
											this.list_User[i].user_list[j].def_plan_num= 0						
										}
										if(this.list_User[i].user_list[j].analysis_plan_num == null){
											this.list_User[i].user_list[j].analysis_plan_num= 0						
										}
										
										this.ARL_Sum += this.list_User[i].user_list[j].all_arl_num
										this.HUDef_ARL_Sum +=this.list_User[i].user_list[j].hu_arl_num
										this.HUDef_Sum += this.list_User[i].user_list[j].all_hu_num
										this.TAGL_ARL_Sum += this.list_User[i].user_list[j].definition_hu_num
										this.TAGLDef_Sum += this.list_User[i].user_list[j].all_definition_num
										this.TAGLAna_ARL_Sum += this.list_User[i].user_list[j].analysis_def_num
										this.TAGLAna_Sum += this.list_User[i].user_list[j].analysis_num
										
										this.HUDef_Plan_Sum += this.list_User[i].user_list[j].hu_plan_num
										this.TAGLDef_Plan_Sum += this.list_User[i].user_list[j].def_plan_num
										this.TAGLAna_Plan_Sum += this.list_User[i].user_list[j].analysis_plan_num
									}
								}
								this.fullscreenLoading = false
							}else{
								this.fullscreenLoading = false
							}
							
						})
						.catch(res => {
							this.fullscreenLoading = false
						})
					}else{
						this.date_value = val
						this.$axios.get(this.Ip+"/SummarizeByUser/"+ this.date_value)
						.then(res =>{
							if(res.data.result == 'OK'){
								this.list_User = res.data.content
								for(var i=0;i<this.list_User.length;i++){
									for(var j=0;j<this.list_User[i].user_list.length;j++){
										if(this.list_User[i].user_list[j].all_arl_num == null){
												this.list_User[i].user_list[j].all_arl_num= 0
										}
										if(this.list_User[i].user_list[j].all_definition_num == null){
											this.list_User[i].user_list[j].all_definition_num= 0							
										}
										if(this.list_User[i].user_list[j].all_hu_num == null){
											this.list_User[i].user_list[j].all_hu_num= 0								
										}
										if(this.list_User[i].user_list[j].analysis_num == null){
											this.list_User[i].user_list[j].analysis_num= 0							
										}
										if(this.list_User[i].user_list[j].definition_hu_num == null){
											this.list_User[i].user_list[j].definition_hu_num= 0						
										}
										if(this.list_User[i].user_list[j].hu_arl_num == null){
											this.list_User[i].user_list[j].hu_arl_num= 0						
										}
										if(this.list_User[i].user_list[j].analysis_def_num == null){
											this.list_User[i].user_list[j].analysis_def_num= 0						
										}
										if(this.list_User[i].user_list[j].user_name == null){
											this.list_User[i].user_list[j].user_name= 0						
										}
										
										if(this.list_User[i].user_list[j].hu_plan_num == null){
											this.list_User[i].user_list[j].hu_plan_num= 0						
										}
										if(this.list_User[i].user_list[j].def_plan_num == null){
											this.list_User[i].user_list[j].def_plan_num= 0						
										}
										if(this.list_User[i].user_list[j].analysis_plan_num == null){
											this.list_User[i].user_list[j].analysis_plan_num= 0						
										}
										
										this.ARL_Sum += this.list_User[i].user_list[j].all_arl_num
										this.HUDef_ARL_Sum +=this.list_User[i].user_list[j].hu_arl_num
										this.HUDef_Sum += this.list_User[i].user_list[j].all_hu_num
										this.TAGL_ARL_Sum += this.list_User[i].user_list[j].definition_hu_num
										this.TAGLDef_Sum += this.list_User[i].user_list[j].all_definition_num
										this.TAGLAna_ARL_Sum += this.list_User[i].user_list[j].analysis_def_num
										this.TAGLAna_Sum += this.list_User[i].user_list[j].analysis_num
										
										this.HUDef_Plan_Sum += this.list_User[i].user_list[j].hu_plan_num
										this.TAGLDef_Plan_Sum += this.list_User[i].user_list[j].def_plan_num
										this.TAGLAna_Plan_Sum += this.list_User[i].user_list[j].analysis_plan_num
									}
								}
							}
							this.fullscreenLoading = false
						})
						.catch(res => {
							this.fullscreenLoading = false
						})
					}
				}
		    }
	}
</script>

<style scoped>
	#Statistic_Function{
		position:relative;
		width: 100%;
		height: 100%;
/*		overflow: scroll;*/
		/*margin-top: 83px;*/
	}
	#Statistic_Table{
		position: absolute;
		left: 0;
		top: 50px;
		right: 0px;
		bottom: 0;
		z-index: 2;
		background-color: white;
	}
	#Statistic_Function_header{
		position: absolute;
		left: 0;
		top: 0px;
		right: 0;
		z-index: 2;
		background-color: white;
		max-height: 63px;
		overflow-x: auto;
		overflow-y: scroll;
		width: 100%;
	}
	#Statistic_Function_body{
		position: absolute;
		top: 60px;
		bottom: 60px;
		overflow-y: scroll;
		overflow-x: auto;
		width: 100%;
		/*border-bottom: 1px solid #eef1f6;*/
	}

	#table_head{
		position: absolute;
		left: 64px;
		top: 55px;
	}
	#Statistic_Function_right{
	 	position: absolute;
	 	left: 0;
	 	right: 0;
	 	top: 0;
	 	bottom: 0;
	}
	#table_head li{
	 	margin-bottom: 10px;
	}
 	.tr1_hover:hover{
	 	background-color: #eef1f6;
	}
</style>
