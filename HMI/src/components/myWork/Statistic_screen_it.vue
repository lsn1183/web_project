<template>
	<div id="Statistic_Function" >
		<div style="position: absolute;top: 8px;width: 100%"  v-loading.fullscreen.lock='loading' element-loading-text="正在导出,请稍等... ...">
			<b style="font-size: 15px;">选择日期:</b>
			<el-date-picker v-model="date_value" type="date" placeholder="选择日期" @change="getTable">
			</el-date-picker>
			<el-button class="s_buttom" type="primary" @click="ExportAuthor()"><i class="el-icon-caret-bottom"> 画面导出</i></el-button>
		</div>
		<div id="Statistic_Table" v-loading.lock="fullscreenLoading">
			<div id="Statistic_Function_header">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;;border: solid 1px #dfe6ec;font-size: 14px;">
					<tr style="background-color:#eef1f6;width: 100%;">
						<th style="width: 5%;min-width: 65px;borderRight: none;">负责人</th>
						<th style="width:95%;max-height: 60px;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;max-height: 60px;">
								<tr>
									<td style="borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:3px solid #dfe6ec;" colspan="6">总汇</td>											
									<td style="border:solid 1px #dfe6ec;" colspan="6">一级画面</td>											
									<td style="borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;" colspan="6">二级画面</td>
									<td style="borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;" colspan="6">三级画面</td>
									<td style="borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;" colspan="6">四级画面</td>
									<td style="borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;" colspan="6">五级画面</td>
								</tr>
								<tr >
									<!-- 总汇 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">总数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">未测试</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">未完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">QA数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;">Delay</td>
									<!-- 一级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">总数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">未测试</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">未完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">QA数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;">Delay</td>
									<!-- 二级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">总数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">未测试</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">未完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">QA数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;">Delay</td>
									<!-- 三级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">总数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">未测试</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">未完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">QA数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;">Delay</td>
									<!-- 四级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">总数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">未测试</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">未完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">QA数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;">Delay</td>
									<!-- 五级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">总数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">未测试</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">未完成</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">QA数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:1px solid #dfe6ec;">Delay</td>
								</tr>
							</table>
						</th>
					</tr>
				</table>
			</div>
			<div id="Statistic_Function_body">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;border: solid 1px #dfe6ec;font-size: 14px;border-bottom: none;" >
					<tr v-for="item in list_Category" class="tr1_hover">
						<td style="width: 5%;overflow:hidden;text-overflow: ellipsis;min-width: 65px;min-width: 65px;min-width: 65px;border-right: none;">{{item.charger}}</td>
						<td style="width: 95%;max-height: 60px;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;max-height: 60px;">
								<tr style="width: 100%;" v-for="item_kids_kids in item.user_list">
									<!--总汇  -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_num}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_finished}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_no_case}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_unfinished}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_qa}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red">{{item_kids_kids.all_delay}}</td>
									<!-- 一级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_num_First}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_finished_First}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_no_case_First}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_unfinished_First}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_qa_First}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red">{{item_kids_kids.all_delay_First}}</td>
									<!-- 二级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_num_Second}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_finished_Second}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_no_case_Second}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_unfinished_Second}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_qa_Second}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red">{{item_kids_kids.all_delay_Second}}</td>
									<!-- 三级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_num_Third}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_finished_Third}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_no_case_Third}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_unfinished_Third}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_qa_Third}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red">{{item_kids_kids.all_delay_Third}}</td>
									<!-- 四级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_num_layer4}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_finished_layer4}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_no_case_layer4}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_unfinished_layer4}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_qa_layer4}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red">{{item_kids_kids.all_delay_layer4}}</td>
									<!-- 五级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:3px solid #dfe6ec;borderRight:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_num_layer5}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_finished_layer5}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_no_case_layer5}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{item_kids_kids.all_unfinished_layer5}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{item_kids_kids.all_qa_layer5}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:1px solid #dfe6ec;color:red">{{item_kids_kids.all_delay_layer5}}</td>
									
								</tr>	
							</table>
						</td>
					</tr>
				</table>
			</div>
			<div style="position: absolute;bottom: 30px;width: 100%;overflow-y: scroll;overflow-x: auto;">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;height: 30px;border: solid 1px #dfe6ec;font-size: 14px;border-bottom: none;" >
					<tr class="tr1_hover">
						<td style="width: 5%;overflow:hidden;text-overflow: ellipsis;borderRight:3px solid #dfe6ec;min-width: 65px;min-width: 65px;min-width: 65px;">{{Sum_Name}}</td>
						<td style="width: 95%;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;height: 100%;">
								<tr style="width: 100%;">
									<!-- 总汇 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:none;min-width: 42px;" >{{all_num}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_finished}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_no_case}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_unfinished}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{all_qa}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red">{{all_delay}}</td>
									<!-- 一级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:none;min-width: 42px;" >{{all_num_First}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_finished_First}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_no_case_First}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_unfinished_First}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{all_qa_First}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red">{{all_delay_First}}</td>							
									<!-- 二级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:none;min-width: 42px;" >{{all_num_Second}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_finished_Second}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_no_case_Second}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_unfinished_Second}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{all_qa_Second}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red">{{all_delay_Second}}</td>
									<!-- 三级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:none;min-width: 42px;" >{{all_num_Third}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_finished_Third}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_no_case_Third}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_unfinished_Third}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{all_qa_Third}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red;">{{all_delay_Third}}</td>
									<!-- 四级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:none;min-width: 42px;" >{{all_num_layer4}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_finished_layer4}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_no_case_layer4}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_unfinished_layer4}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{all_qa_layer4}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:3px solid #dfe6ec;color:red;">{{all_delay_layer4}}</td>
									<!-- 五级画面 -->
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:none;min-width: 42px;" >{{all_num_layer5}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_finished_layer5}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_no_case_layer5}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;">{{all_unfinished_layer5}}</td>
									<td style="width: 5%;borderTop:1px solid #dfe6ec;borderBottom:1px solid #dfe6ec;borderLeft:1px solid #dfe6ec;min-width: 42px;">{{all_qa_layer5}}</td>				
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 42px;borderRight:1px solid #dfe6ec;color:red;">{{all_delay_layer5}}</td>
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
			data(){
		      return {
		      	fullscreenLoading:false,
		      	list_Category: [],
		      	date_value: '',
		      	datatime:"",
	      		Sum_Name: '总计',
	      		all_num:0,
	      		all_finished:0,
	      		all_no_case:0,
	      		all_unfinished:0,
	      		all_qa:0,
	      		all_delay:0,

	      		all_num_First:0,
	      		all_finished_First:0,
	      		all_no_case_First:0,
	      		all_unfinished_First:0,
	      		all_delay_First:0,
	      		all_qa_First:0,

	      		all_num_Second:0,
	      		all_finished_Second:0,
	      		all_no_case_Second:0,
	      		all_unfinished_Second:0,
	      		all_qa_Second:0,
	      		all_delay_Second:0,

	      		all_num_Third:0,
	      		all_finished_Third:0,
	      		all_no_case_Third:0,
	      		all_unfinished_Third:0,
	      		all_qa_Third:0,
	      		all_delay_Third:0,

	      		all_num_layer4:0,
	      		all_finished_layer4:0,
	      		all_no_case_layer4:0,
	      		all_unfinished_layer4:0,
	      		all_qa_layer4:0,
	      		all_delay_layer4:0,

	      		all_num_layer5:0,
	      		all_finished_layer5:0,
	      		all_no_case_layer5:0,
	      		all_unfinished_layer5:0,
	      		all_qa_layer5:0,
	      		all_delay_layer5:0,

	      		loading:false
		      }
		    },
		    mounted() {
		    	//  获取当前时间
		    	var formatDate = function(date) {
		    		var y = date.getFullYear(); 
		    		var m = date.getMonth() + 1;
		    		m = m < 10 ? '0' + m : m;
		    		var d = date.getDate();
		    		d = d < 10 ? ('0' + d) : d;
		    		return y + '-' + m + '-' + d;
		    	}
		    	const start = new Date();
		    	var time = formatDate(start)

		    	this.date_value = time
		    	this.$axios.get(this.Ip+"/ScreenItReport/user/"+time)
				.then(res =>{
					if(res.data.result == 'OK'){
						this.list_Category = res.data.content
						this.all_num = res.data.sum.all_num

						this.all_finished = res.data.sum.all_finished

						this.all_no_case = res.data.sum.all_no_case

						this.all_unfinished = res.data.sum.all_unfinished

						this.all_qa = res.data.sum.all_qa

						this.all_delay = res.data.sum.all_delay


						this.all_num_First = res.data.sum.all_num_First

						this.all_finished_First = res.data.sum.all_finished_First

						this.all_no_case_First = res.data.sum.all_no_case_First

						this.all_unfinished_First = res.data.sum.all_unfinished_First

						this.all_delay_First = res.data.sum.all_delay_First

						this.all_qa_First = res.data.sum.all_qa_First


						this.all_num_Second = res.data.sum.all_num_Second

						this.all_finished_Second = res.data.sum.all_finished_Second

						this.all_no_case_Second = res.data.sum.all_no_case_Second

						this.all_unfinished_Second = res.data.sum.all_unfinished_Second

						this.all_qa_Second = res.data.sum.all_qa_Second

						this.all_delay_Second = res.data.sum.all_delay_Second


						this.all_num_Third = res.data.sum.all_num_Third

						this.all_finished_Third = res.data.sum.all_finished_Third

						this.all_no_case_Third = res.data.sum.all_no_case_Third

						this.all_unfinished_Third = res.data.sum.all_unfinished_Third

						this.all_qa_Third = res.data.sum.all_qa_Third

						this.all_delay_Third = res.data.sum.all_delay_Third


						this.all_num_layer4 = res.data.sum.all_num_layer4

						this.all_finished_layer4 = res.data.sum.all_finished_layer4

						this.all_no_case_layer4 = res.data.sum.all_no_case_layer4

						this.all_unfinished_layer4 = res.data.sum.all_unfinished_layer4

						this.all_qa_layer4 = res.data.sum.all_qa_layer4

						this.all_delay_layer4 = res.data.sum.all_delay_layer4


						this.all_num_layer5 = res.data.sum.all_num_layer5

						this.all_finished_layer5 = res.data.sum.all_finished_layer5

						this.all_no_case_layer5 = res.data.sum.all_no_case_layer5

						this.all_unfinished_layer5 = res.data.sum.all_unfinished_layer5

						this.all_qa_layer5 = res.data.sum.all_qa_layer5

						this.all_delay_layer5 = res.data.sum.all_delay_layer5

					}
					else{
						this.list_Category = []
						this.$alert("暂无数据",{title:"提示"})
						this.clear()
					}
					this.fullscreenLoading = false
				})
		    },
		    methods: {
		    	getTable(val){
		    		this.fullscreenLoading = true
		    		this.date_value = val
				this.$axios.get(this.Ip+"/ScreenItReport/user/"+val)
					.then(res =>{
						if(res.data.result == 'OK'){
							this.list_Category = res.data.content
						this.all_num = res.data.sum.all_num

						this.all_finished = res.data.sum.all_finished

						this.all_no_case = res.data.sum.all_no_case

						this.all_unfinished = res.data.sum.all_unfinished

						this.all_qa = res.data.sum.all_qa

						this.all_delay = res.data.sum.all_delay


						this.all_num_First = res.data.sum.all_num_First

						this.all_finished_First = res.data.sum.all_finished_First

						this.all_no_case_First = res.data.sum.all_no_case_First

						this.all_unfinished_First = res.data.sum.all_unfinished_First

						this.all_delay_First = res.data.sum.all_delay_First

						this.all_qa_First = res.data.sum.all_qa_First


						this.all_num_Second = res.data.sum.all_num_Second

						this.all_finished_Second = res.data.sum.all_finished_Second

						this.all_no_case_Second = res.data.sum.all_no_case_Second

						this.all_unfinished_Second = res.data.sum.all_unfinished_Second

						this.all_qa_Second = res.data.sum.all_qa_Second

						this.all_delay_Second = res.data.sum.all_delay_Second


						this.all_num_Third = res.data.sum.all_num_Third

						this.all_finished_Third = res.data.sum.all_finished_Third

						this.all_no_case_Third = res.data.sum.all_no_case_Third

						this.all_unfinished_Third = res.data.sum.all_unfinished_Third

						this.all_qa_Third = res.data.sum.all_qa_Third

						this.all_delay_Third = res.data.sum.all_delay_Third


						this.all_num_layer4 = res.data.sum.all_num_layer4

						this.all_finished_layer4 = res.data.sum.all_finished_layer4

						this.all_no_case_layer4 = res.data.sum.all_no_case_layer4

						this.all_unfinished_layer4 = res.data.sum.all_unfinished_layer4

						this.all_qa_layer4 = res.data.sum.all_qa_layer4

						this.all_delay_layer4 = res.data.sum.all_delay_layer4


						this.all_num_layer5 = res.data.sum.all_num_layer5

						this.all_finished_layer5 = res.data.sum.all_finished_layer5

						this.all_no_case_layer5 = res.data.sum.all_no_case_layer5

						this.all_unfinished_layer5 = res.data.sum.all_unfinished_layer5

						this.all_qa_layer5 = res.data.sum.all_qa_layer5

						this.all_delay_layer5 = res.data.sum.all_delay_layer5

						}
						else{
							this.list_Category = []
							this.$alert("暂无数据",{title:"提示"})
							this.clear()
						}
						this.fullscreenLoading = false
					})
		    	},
		    	clear(){
		    		this.all_num = 0
		    		this.all_finished = 0
		    		this.all_no_case = 0
		    		this.all_unfinished = 0
		    		this.all_qa = 0
		    		this.all_delay = 0

		    		this.all_num_First = 0
		    		this.all_finished_First = 0
		    		this.all_no_case_First = 0
		    		this.all_unfinished_First = 0
		    		this.all_delay_First = 0
		    		this.all_qa_First = 0

		    		this.all_num_Second = 0
		    		this.all_finished_Second = 0
		    		this.all_no_case_Second = 0
		    		this.all_unfinished_Second = 0
		    		this.all_qa_Second = 0
		    		this.all_delay_Second = 0

		    		this.all_num_Third = 0
		    		this.all_finished_Third = 0
		    		this.all_no_case_Third = 0
		    		this.all_unfinished_Third = 0
		    		this.all_qa_Third = 0
		    		this.all_delay_Third = 0

		    		this.all_num_layer4 = 0
		    		this.all_finished_layer4 = 0
		    		this.all_no_case_layer4 = 0
		    		this.all_unfinished_layer4 = 0
		    		this.all_qa_layer4 = 0
		    		this.all_delay_layer4 = 0

		    		this.all_num_layer5 = 0
		    		this.all_finished_layer5 = 0
		    		this.all_no_case_layer5 = 0
		    		this.all_unfinished_layer5 = 0
		    		this.all_qa_layer5 = 0
		    		this.all_delay_layer5 = 0
		    	},
		    	ExportAuthor(){
		    		this.loading = true;
		    		this.$axios.get(this.Ip + '/ScreenReportExport/' + this.date_value)
		    			.then(res => {
		    				if(res.data.result == 'OK') {
		    					window.location.href = this.Ip + '/HmiExportFile/' + res.data.Result_PathInfo + '/' + res.data.Result_FileInfo;
		    					this.loading = false;
		    				} else {
		    					this.$alert('服务器异常！', {
		    						title: "提示"
		    					})
		    				}
		    			})
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
		top: 62px;
		bottom: 60px;
		overflow-y: scroll;
		overflow-x: auto;
		/*border-bottom: 1px solid #eef1f6;*/
		width: 100%;
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
 /*	.tr1_hover:hover{
	 	background-color: #eef1f6;
	}*/
</style>
