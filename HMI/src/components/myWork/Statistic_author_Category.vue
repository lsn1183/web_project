<template>
	<div id="Statistic_Function" v-loading.fullscreen.lock='loading' element-loading-text="正在导出,请稍等... ...">
		<div style="position: absolute;top: 8px;width: 100%">
			<b style="font-size: 15px;">预定完成日:</b>
			<el-date-picker v-model="date_value" type="date" placeholder="选择日期" @change="getTable">
			</el-date-picker>
			<el-select class="button_tree" v-model="arr_v" @change="selectsp">
				<el-option class="button_tree_option" v-for="item in arr" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<el-button class="s_buttom" type="primary" @click="ExportAuthor()"><i class="el-icon-caret-bottom"> 每日汇总导出</i></el-button>
			<el-button class="s_buttom" type="primary" @click="ExportAuthor2()"><i class="el-icon-caret-bottom"> 昨日完成明细</i></el-button>
			<el-button class="s_buttom" type="primary" @click="ExportAuthor3()">查阅数据图表<i class="el-icon-d-arrow-right"></i></el-button>
		</div>
		<div id="Statistic_Table" v-loading.lock="fullscreenLoading">
			<div id="Statistic_Function_header">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;;border: solid 1px #dfe6ec;font-size: 14px;">
					<tr style="background-color:#eef1f6;width: 100%;">
						<th style="width: 5%;min-width: 100px;borderRight: none;">负责人</th>
						<th style="width: 95%;borderLeft: none;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;max-height: 60px;">
								<tr>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:120px;min-width:116px;" rowspan="3">担当</td>
									<td style="border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;min-width: 198px;" colspan="17">全部统计</td>
									<td style="border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;borderRight:solid 3px #dfe6ec;min-width: 198px;" colspan="5" rowspan="2">今日统计</td>
								</tr>
								<tr>
									<td style="width:5%;border:solid 1px #dfe6ec;max-width:120px;min-width:120px;" colspan="6">总汇</td>
									<td style="border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;min-width: 198px;" colspan="5">代表（结合日程）</td>
									<td style="border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;borderRight:solid 3px #dfe6ec;min-width: 198px;" colspan="6">非代表（APL日程）</td>
								</tr>
								<tr>
									<td style="width: 4.29%;borderLeft:solid 3px #dfe6ec;min-width: 60px;">总数</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">对象外</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">已完成</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">未完成</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">QA数</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">Delay数</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">总数</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">已完成</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">未完成</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">QA数</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">Delay</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">总数</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">已完成</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">未完成</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">结合测试完成</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">QA数</td>
									<td style="width: 4.29%;borderLeft:solid 1px #dfe6ec;min-width: 60px;">Delay</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;borderLeft:solid 3px #dfe6ec;">今日总数</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">今日代表要件</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;borderRight:solid 3px #dfe6ec;min-width: 60px;">今日非代表要件</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">昨日代表要件完成件数</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;borderRight:solid 3px #dfe6ec;min-width: 60px;">昨日非代表要件完成件数</td>
								</tr>
							</table>
						</th>
					</tr>
				</table>
			</div>
			<div id="Statistic_Function_body">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;height: 60px;border: solid 1px #dfe6ec;font-size: 14px;border-bottom: none;">
					<tr v-for="item in list_User" class="tr1_hover">
						<td style="width: 5%;overflow:hidden;text-overflow: ellipsis;min-width: 100px;border-right: none;">{{item.charger}}</td>
						<td style="width: 95%;border: none;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;height: 100%;">
								<tr v-for="item_kids_kids in item.user_list" style="width: 100%;">
									<td style="width: 5%;height:30px;border:solid 1px #dfe6ec;max-width:116px;min-width:116px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;borderRight:solid 3px #dfe6ec;" :title="item_kids_kids.author">{{item_kids_kids.author}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_num}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_exclude}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_finished}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_unfinished}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_qa}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px; color:red">{{item_kids_kids.all_delay}}</td>
									<!-- 结合条件 -->
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_num_represent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_finished_represent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_unfinished_represent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_qa_represent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;color:red">{{item_kids_kids.all_delay_represent}}</td>

									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_num_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_finished_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_unfinished_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.it_progress_success}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.all_qa_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px; color:red">{{item_kids_kids.all_delay_not_rep}}</td>

									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;borderLeft:solid 3px #dfe6ec;">{{item_kids_kids.today_plan}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.today_plan_reprent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.today_plan_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.yesterday_finished_reprent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.yesterday_finished_not_rep}}</td>
								</tr>

							</table>
						</td>
					</tr>
				</table>
			</div>
			<div style="position: absolute;bottom: 30px;width: 100%;overflow-y: scroll;overflow-x: auto;">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;height: 30px;border: solid 1px #dfe6ec;font-size: 14px;border-bottom: none;">
					<tr class="tr1_hover">
						<td style="width: 9.75%;overflow:hidden;text-overflow: ellipsis;min-width: 216px;border-right: none;">{{Sum_Name}}</td>
						<td style="width: 90.25%;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;height: 100%;">
								<tr style="width: 100%;">

									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_num}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_exclude}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_finished}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_unfinished}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_qa}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px; color:red">{{all_delay}}</td>

									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_num_represent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_finished_represent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_unfinished_represent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_qa_represent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;color:red">{{all_delay_represent}}</td>

									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_num_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_finished_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_unfinished_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{it_progress_success}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{all_qa_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px; color:red">{{all_delay_not_rep}}</td>

									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;borderLeft:solid 3px #dfe6ec;">{{today_plan}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{today_plan_reprent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{today_plan_not_rep}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{yesterday_finished_reprent}}</td>
									<td style="width: 4.29%;border:solid 1px #dfe6ec;min-width: 60px;">{{yesterday_finished_not_rep}}</td>

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
	export default {
		mounted() {
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
			this.fullscreenLoading = true
			this.date_value = time
			this.select_time = time
			this.$axios.get(this.Ip + "/Report/user/" + time + '/SP31')
				.then(res => {
					if(res.data.result == "OK") {
						this.fullscreenLoading = false
						this.list_User = res.data.content
						this.all_num = res.data.sum.all_num
						this.all_exclude = res.data.sum.all_exclude
						this.all_finished = res.data.sum.all_finished
						this.all_unfinished = res.data.sum.all_unfinished
						this.all_qa = res.data.sum.all_qa
						this.all_delay = res.data.sum.all_delay
						this.all_num_represent = res.data.sum.all_num_represent
						this.all_unfinished_represent = res.data.sum.all_unfinished_represent
						this.all_finished_represent = res.data.sum.all_finished_represent
						this.all_delay_represent = res.data.sum.all_delay_represent
						this.all_qa_represent = res.data.sum.all_qa_represent
						this.all_num_not_rep = res.data.sum.all_num_not_rep
						this.all_finished_not_rep = res.data.sum.all_finished_not_rep
						this.all_unfinished_not_rep = res.data.sum.all_unfinished_not_rep
						this.all_qa_not_rep = res.data.sum.all_qa_not_rep
						this.all_delay_not_rep = res.data.sum.all_delay_not_rep
						this.today_plan = res.data.sum.today_plan
						this.today_plan_reprent = res.data.sum.today_plan_reprent
						this.today_plan_not_rep = res.data.sum.today_plan_not_rep
						this.it_progress_success = res.data.sum.it_progress_success
						this.yesterday_finished_reprent = res.data.sum.yesterday_finished_reprent
						this.yesterday_finished_not_rep = res.data.sum.yesterday_finished_not_rep
					} else {
						this.list_User = []
						this.$alert('暂无数据', {
							title: "提示"
						})
						this.clear()
					}

				})
		},
		data() {
			return {
				fullscreenLoading: false,
				list_User: [],
				date_value: '',

				Sum_Name: '总计',
				all_num: 0,
				all_exclude: 0,
				all_finished: 0,
				all_unfinished: 0,
				all_qa: 0,
				all_delay: 0,

				all_num_represent: 0,
				all_unfinished_represent: 0,
				all_finished_represent: 0,
				all_delay_represent: 0,
				all_qa_represent: 0,
				all_num_not_rep: 0,
				all_finished_not_rep: 0,
				all_unfinished_not_rep: 0,
				all_qa_not_rep: 0,
				all_delay_not_rep: 0,

				today_plan: 0,
				today_plan_reprent: 0,
				today_plan_not_rep: 0,
				it_progress_success: 0,
				yesterday_finished_reprent: "-",
				yesterday_finished_not_rep: "-",
				arr_v: "SP31",
				arr: [{
						value: "SP29",
						label: "SP29"
					},
					{
						value: "SP30",
						label: "SP30"
					},
					{
						value: "SP31",
						label: "SP31"
					},
					{
						value: "SP32",
						label: "SP32"
					},
					{
						value: "all",
						label: "全部"
					},
				],
				select_time: "",
				loading: false
			}
		},
		methods: {
			clear() {
				this.list_User = 0
				this.all_num = 0
				this.all_exclude = 0
				this.all_finished = 0
				this.all_unfinished = 0
				this.all_qa = 0
				this.all_delay = 0
				this.all_num_represent = 0
				this.all_unfinished_represent = 0
				this.all_finished_represent = 0
				this.all_delay_represent = 0
				this.all_qa_represent = 0
				this.all_num_not_rep = 0
				this.all_finished_not_rep = 0
				this.all_unfinished_not_rep = 0
				this.all_qa_not_rep = 0
				this.all_delay_not_rep = 0
				this.today_plan = 0
				this.today_plan_reprent = 0
				this.today_plan_not_rep = 0
				this.it_progress_success = 0
				this.yesterday_finished_reprent = 0
				this.yesterday_finished_not_rep = 0
			},
			getTable(val, sp) {
				this.select_time = val
				sp = this.arr_v
				this.fullscreenLoading = true
				this.$axios.get(this.Ip + "/Report/user/" + val + '/' + sp)
					.then(res => {
						if(res.data.result == "OK") {
							this.fullscreenLoading = false
							this.list_User = res.data.content
							this.all_num = res.data.sum.all_num
							this.all_exclude = res.data.sum.all_exclude
							this.all_finished = res.data.sum.all_finished
							this.all_unfinished = res.data.sum.all_unfinished
							this.all_qa = res.data.sum.all_qa
							this.all_delay = res.data.sum.all_delay
							this.all_num_represent = res.data.sum.all_num_represent
							this.all_unfinished_represent = res.data.sum.all_unfinished_represent
							this.all_finished_represent = res.data.sum.all_finished_represent
							this.all_delay_represent = res.data.sum.all_delay_represent
							this.all_qa_represent = res.data.sum.all_qa_represent
							this.all_num_not_rep = res.data.sum.all_num_not_rep
							this.all_finished_not_rep = res.data.sum.all_finished_not_rep
							this.all_unfinished_not_rep = res.data.sum.all_unfinished_not_rep
							this.all_qa_not_rep = res.data.sum.all_qa_not_rep
							this.all_delay_not_rep = res.data.sum.all_delay_not_rep
							this.today_plan = res.data.sum.today_plan
							this.today_plan_reprent = res.data.sum.today_plan_reprent
							this.today_plan_not_rep = res.data.sum.today_plan_not_rep
							this.it_progress_success = res.data.sum.it_progress_success
							this.yesterday_finished_reprent = res.data.sum.yesterday_finished_reprent
							this.yesterday_finished_not_rep = res.data.sum.yesterday_finished_not_rep
						} else {
							this.list_User = []
							this.$alert('暂无数据', {
								title: "提示"
							})
							this.clear()
						}

					})
			},
			selectsp() {
				if(this.select_time != "") {
					this.getTable(this.select_time, this.arr_v)
				} else {
					this.$alert('请选择日期', {
						title: "提示"
					})
				}

			},
			ExportAuthor() {
				this.loading = true;
				this.$axios.get(this.Ip + '/ReportExport/' + this.select_time + '/' + this.arr_v)
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
			},
			ExportAuthor2() {
				this.loading = true;
				let export_data = {
					type: '',
					date: ''
				};
				export_data.type = 'daily_finished_detail';
				export_data.date = this.select_time;
				// console.log(this.select_time)
				this.$axios.post(this.Ip + '/HmiExport', export_data)
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
			},
			ExportAuthor3() {
				//          this.group_flag = false
				this.$router.push('/hmi/Statistic_author_Category_Map')
			}
		}
	}
</script>

<style scoped>
	#Statistic_Function {
		position: relative;
		width: 100%;
		height: 100%;
	}
	
	#Statistic_Table {
		position: absolute;
		left: 0;
		top: 50px;
		right: 0px;
		bottom: 0;
		z-index: 2;
		background-color: white;
	}
	
	#Statistic_Function_header {
		position: absolute;
		left: 0;
		top: 0px;
		right: 0;
		z-index: 2;
		background-color: white;
		/*max-height:100px;*/
		overflow-x: auto;
		overflow-y: scroll;
		width: 100%;
	}
	
	#Statistic_Function_body {
		position: absolute;
		top: 100px;
		bottom: 60px;
		overflow-y: scroll;
		overflow-x: auto;
		width: 100%;
	}
	
	#table_head {
		position: absolute;
		left: 64px;
		top: 55px;
	}
	
	#Statistic_Function_right {
		position: absolute;
		left: 0;
		right: 0;
		top: 0;
		bottom: 0;
	}
	
	#table_head li {
		margin-bottom: 10px;
	}
	
	.tr1_hover:hover {
		background-color: #eef1f6;
	}
</style>