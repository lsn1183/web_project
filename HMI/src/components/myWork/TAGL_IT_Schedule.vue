<template>
	<div id="Statistic_Function" v-loading.fullscreen.lock='loading' element-loading-text="正在导出,请稍等... ...">
		<div style="position: absolute;top: 8px;width: 100%">
			<b style="font-size: 15px;">预定完成日:</b>
			<el-date-picker v-model="date_value" type="date" placeholder="选择日期" @change="getTable">
			</el-date-picker>
			<el-button class="s_buttom" type="primary" @click="ExportAuthor()"><i class="el-icon-caret-bottom"> IT进度统计表导出</i></el-button>
		</div>
		<div id="Statistic_Table" v-loading.lock="fullscreenLoading">
			<div id="Statistic_Function_header">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;;border: solid 1px #dfe6ec;font-size: 14px;">
					<tr style="background-color:#eef1f6;width: 100%;">
						<!-- <th style="width: 5%;min-width: 100px;borderRight: none;">负责人</th> -->
						<th style="width:100%;borderLeft: none;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;max-height: 60px;">
								<tr>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:120px;min-width:100px;" rowspan="3">担当</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">Delay</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">总数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">对象外</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">QA数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">转出</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">Block</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">完成数</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">暂停</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">同件</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">类似件</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">残件数</td>
									<td style="border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;min-width: 198px;" colspan="6">全部统计</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;max-width:70px;min-width:50px;" rowspan="3">更新日期</td>
									<!-- <td style="border:solid 1px #dfe6ec;borderLeft:solid 3px #dfe6ec;borderRight:solid 3px #dfe6ec;min-width: 198px;" colspan="5" rowspan="2">今日统计</td> -->
								</tr>
								<tr>
									<td style="width: 5%;borderLeft:solid 3px #dfe6ec;min-width: 60px;">未开始</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">①与FW16一起分析要件</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">②要件->具体模块分析(结合代码得出Astah图)</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">③完成自己模块的UT</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">④完成自己模块+1的IT</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">⑤完成自己模块+N的IT</td>
								</tr>
							</table>
						</th>
					</tr>
				</table>
			</div>
			<div id="Statistic_Function_body">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;height: 60px;border: solid 1px #dfe6ec;font-size: 14px;border-bottom: none;">
					<tr v-for="item in list_User" class="tr1_hover">
						<td style="width: 100%;border: none;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;height: 100%;">
								<tr style="width: 100%;"  v-for="item_kids_kids in item.user_list">
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 100px; borderRight:solid 3px #dfe6ec;">{{item_kids_kids.author}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;color:red">{{item_kids_kids.sum_delay}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px; ">{{item_kids_kids.sum_all}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_not_object}}</td>
									
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_qa}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_out}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_block}}</td>

									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_finish}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_stop}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_same}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_analogy}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_no_finish}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.no_start}}</td>

									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_dev_fw16}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_dev_model}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_dev_ut}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_dev_it}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{item_kids_kids.sum_dev_itn}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">
										<el-input type="textarea" size="medium" v-model="item_kids_kids.update_time"></el-input>
									</td>
								</tr>

							</table>
						</td>
					</tr>
				</table>
			</div>
			<div style="position: absolute;bottom: 30px;width: 100%;overflow-y: scroll;overflow-x: auto;">
				<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;height: 30px;border: solid 1px #dfe6ec;font-size: 14px;border-bottom: none;">
					<tr class="tr1_hover">
						<!-- <td style="width: 5%;overflow:hidden;text-overflow: ellipsis;min-width: 100px;border-right: none;">{{Sum_Name}}</td> -->
						<td style="width: 100%;">
							<table border="0" style="border-collapse: collapse;text-align: center;width: 100%;height: 100%;">
								<tr style="width: 100%;">
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 100px;">{{Sum_Name}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px; color:red">{{sum_delay}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_all}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_not_object}}</td>
									
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_qa}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_out}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_block}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px; ">{{sum_finish}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px; ">{{sum_stop}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_same}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_analogy}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_no_finish}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{no_start}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_dev_fw16}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_dev_model}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_dev_ut}}</td>

									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_dev_it}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">{{sum_dev_itn}}</td>
									<td style="width: 5%;border:solid 1px #dfe6ec;min-width: 60px;">
										<el-button type="primary" @click="save">保存</el-button>
									</td>
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
			this.$axios.get(this.Ip + "/Report/it_progress_report/" + time + '/SP31')
				.then(res => {
					if(res.data.result == "OK") {
						this.fullscreenLoading = false
						this.list_User = res.data.content
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
				no_start: 0,
				sum_all: 0,
				sum_block: 0,
				sum_delay: 0,
				sum_dev_fw16: 0,
				sum_dev_it: 0,

				sum_dev_itn: 0,
				sum_dev_model: 0,
				sum_dev_ut: 0,
				sum_finish: 0,
				sum_no_finish: 0,
				sum_not_object: 0,
				sum_out: 0,
				sum_qa: 0,
				sum_stop:0,
				sum_same:0,
				sum_analogy:0,
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
				],
				select_time: "",
				loading: false,
				sum:[]
			}
		},
		methods: {
			clear() {
				this.no_start = 0
				this.sum_all = 0
				this.sum_block = 0
				this.sum_delay = 0
				this.sum_dev_fw16 = 0
				this.sum_dev_it = 0

				this.sum_dev_itn = 0
				this.sum_dev_model = 0
				this.sum_dev_ut = 0
				this.sum_finish = 0
				this.sum_no_finish = 0
				this.sum_not_object = 0
				this.sum_out = 0
				this.sum_qa = 0
				this.sum_stop = 0
				this.sum_same = 0
				this.sum_analogy = 0
			},
			getTable(val, sp) {
				this.select_time = val
				sp = this.arr_v
				this.fullscreenLoading = true
				this.$axios.get(this.Ip + "/Report/it_progress_report/" + val + '/' + sp)
					.then(res => {
						console.log(res)
						if(res.data.result == "OK") {
							this.fullscreenLoading = false
							this.list_User = res.data.content

							this.no_start = res.data.sum.no_start
							this.sum_all = res.data.sum.sum_all
							this.sum_block = res.data.sum.sum_block
							this.sum_delay = res.data.sum.sum_delay
							this.sum_dev_fw16 = res.data.sum.sum_dev_fw16
							this.sum_dev_it = res.data.sum.sum_dev_it

							this.sum_dev_itn = res.data.sum.sum_dev_itn
							this.sum_dev_model = res.data.sum.sum_dev_model
							this.sum_dev_ut = res.data.sum.sum_dev_ut
							this.sum_finish = res.data.sum.sum_finish
							this.sum_no_finish = res.data.sum.sum_no_finish
							this.sum_not_object = res.data.sum.sum_not_object
							this.sum_out = res.data.sum.sum_out
							this.sum_qa = res.data.sum.sum_qa
							this.sum_stop = res.data.sum.sum_stop
							this.sum_same = res.data.sum.sum_same
							this.sum_analogy = res.data.sum.sum_analogy
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
				this.$axios.get(this.Ip + '/ItProgressExport/' + this.select_time)
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
			save(){
				let data = []
				// console.log(this.list_User)
				for(var i = 0; i <this.list_User.length;i++){
					data.push({"date_time":this.select_time,"author":this.list_User[i].user_list[0].author,"update_time":this.list_User[i].user_list[0].update_time})
				}
				this.$axios.post(this.Ip + "/ItSaveUpdateTime", data).then(res => {
					if(res.data.result == 'OK') {
						this.$message({
							type: 'success',
							message: '保存成功',
						});
					}else{
						this.$message({
							type: 'info',
							message: '保存失败',
						});
					}
				}).catch(res => {
					this.$message({
						type: 'info',
						message: '连接服务器失败',
					});
				});
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
		top: 98px;
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