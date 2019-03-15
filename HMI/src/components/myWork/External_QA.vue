<template>
	<div>
		<!--<div class="input_search" @keyup.enter="Table_search(input_value)">-->
		<!--<el-input placeholder="请输入搜索ID" size="small" v-model="input_value">-->
		<!--<el-button slot="append" class="el-icon-search" @click="Table_search(input_value)"></el-button>-->
		<!--</el-input>-->
		<!--</div>-->
		<div id="table_OA_EX"  v-loading.lock="fullscreenLoading"  element-loading-text="正在载入,请稍等... ...">
			<el-table border style="top: 10px;height: 100%;width:100%;" :data="tableData" @selection-change="select_line" max-height="700" >
				<el-table-column type="selection" width="40" header-align="left">
				</el-table-column>
				<el-table-column label="问题类型" header-align="center" width="70">
					<template scope="scope">
						<!--<el-select class="s_section_right" v-model="scope.row.status" placeholder="请选择类型" size='medium' v-if="scope.row.seen">-->
						<!--<el-option :label="scope.row.status" :value="scope.row.status"></el-option>-->
						<!--</el-select>-->
						<!--<span class="text_show" v-else="">{{ scope.row.status }}</span>-->
						<el-input type="textarea" :title="scope.row.qa_type" v-model="scope.row.qa_type" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" :title="scope.row.qa_type" v-else>{{ scope.row.qa_type }}</span>
					</template>
				</el-table-column>
				<el-table-column label="问题关键字" header-align="center" width="120">
					<template scope="scope">
						<el-input type="textarea" :title='scope.row.qa_keyword' v-model="scope.row.qa_keyword" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" :title='scope.row.qa_keyword' v-else>{{ scope.row.qa_keyword }}</span>
					</template>
				</el-table-column>
				<el-table-column label="问题ID" header-align="center">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.qa_id" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" v-else>{{ scope.row.qa_id}}</span>
					</template>
				</el-table-column>
				<el-table-column label="概要" header-align="center" width="200">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.summary" v-if="scope.row.seen" size="medium" :title="scope.row.detail" ></el-input>
						<span class="text_show" v-else :title="scope.row.summary" >{{ scope.row.summary}}</span>
					</template>
				</el-table-column>
				<el-table-column label="经办人" header-align="center" width="100">
					<template scope="scope">
						<el-input type="textarea" :title="scope.row.charger" v-model="scope.row.charger" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" :title="scope.row.charger" v-else>{{ scope.row.charger}}</span>
					</template>
				</el-table-column>
				<el-table-column label="报告人" header-align="center" width="100">
					<template scope="scope">
						<el-input type="textarea" :title="scope.row.reporter" v-model="scope.row.reporter" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" :title="scope.row.reporter" v-else>{{ scope.row.reporter}}</span>
					</template>
				</el-table-column>
				<el-table-column label="优先级" header-align="center">
					<template scope="scope">
						<el-input type="textarea" :title="scope.row.priority" v-model="scope.row.priority" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" :title="scope.row.priority" v-else>{{ scope.row.priority }}</span>
					</template>
				</el-table-column>
				<el-table-column label="状态" header-align="center" width="90">
					<template scope="scope">
						<!--<el-date-picker v-model="scope.row.answer_date" format="yyyy-MM-dd" value-format="yyyy-MM-dd" v-if="scope.row.seen" placeholder="选择日期" align="right" size="small"></el-date-picker>-->
						<!--<span class="text_show" v-else>{{ scope.row.answer_date }}</span>-->
						<el-input type="textarea" :title="scope.row.status" v-model="scope.row.status" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" :title="scope.row.status" v-else>{{ scope.row.status }}</span>
					</template>
				</el-table-column>
			<!-- 	<el-table-column label="解决结果" header-align="center">
					<template scope="scope">
						<el-input type="textarea" :title="scope.row.result" v-model="scope.row.result" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" :title="scope.row.result" v-else>{{ scope.row.result}}</span>
					</template>
				</el-table-column> -->
				<el-table-column label="创建日期" header-align="center" width="100">
					<template scope="scope">
						<!--<el-input type="textarea" autosize="true" v-model="scope.row.answer_reviewer" v-if="scope.row.seen" size="medium"></el-input>-->
						<!--<span class="text_show" v-else>{{ scope.row.answer_reviewer }}</span>-->
						<el-input type="textarea" :title="scope.row.create_date" v-model="scope.row.create_date" v-if="scope.row.seen" size="mini"></el-input>
						<!--<el-date-picker v-model="scope.row.answer_date" format="yyyy-MM-dd" value-format="yyyy-MM-dd" v-if="scope.row.seen" placeholder="选择日期" align="right" size="medium"></el-date-picker>-->
						<span class="text_show" :title="scope.row.create_date" v-else>{{ scope.row.create_date}}</span>
					</template>
				</el-table-column>
				<el-table-column label="已更新" header-align="center">
					<template scope="scope">
						<el-input type="textarea" :title="scope.row.update_date" v-model="scope.row.update_date" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" :title="scope.row.update_date" v-else>{{ scope.row.update_date }}</span>
					</template>
				</el-table-column>
				<el-table-column label="到期日" header-align="center">
					<template scope="scope">
						<!--<el-input type="textarea" autosize="true" v-model="scope.row.remark" v-if="scope.row.seen" size="medium"></el-input>-->
						<!--<span class="text_show" v-else>{{ scope.row.remark }}</span>-->
						<el-input type="textarea" :title="scope.row.arrive_date" v-model="scope.row.arrive_date" v-if="scope.row.seen" size="mini"></el-input>
						<!--<el-date-picker v-model="scope.row.answer_date" format="yyyy-MM-dd" value-format="yyyy-MM-dd" v-if="scope.row.seen" placeholder="选择日期" align="right" size="medium"></el-date-picker>-->
						<span class="text_show" :title="scope.row.arrive_date" v-else>{{ scope.row.arrive_date}}</span>
					</template>
				</el-table-column>
				<el-table-column label="自定义字段（质问详细）" header-align="center">
					<template scope="scope">
						<el-input type="textarea" :title="scope.row.detail" v-model="scope.row.detail" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" :title="scope.row.detail" v-else>{{ scope.row.detail }}</span>
					</template>
				</el-table-column>
				<el-table-column label="编辑" header-align="center" width="100" fixed="right">
					<template scope="scope">
						<el-button type="text" @click="Edit(scope.row)"><span class="el-icon-edit">修改</span></el-button>
					</template>
				</el-table-column>
			</el-table>
		</div>

		<div class="btn">
				
			<el-pagination
			id="list_page"
			@current-change="listPageChange"
			:current-page="page"
			:page-size="page_size"
			layout="total, prev, pager, next,jumper"
			:total="changdu"
			></el-pagination>
			<el-button type="primary" @click="add_table()">添加</el-button>
			<el-button type="primary" @click="delete_table()">删除</el-button>
			<el-button type="primary" @click="save_table()">保存</el-button>
		</div>
	</div>
</template>
<script>
	require('../../assets/js/jquery-1.8.3.min.js')
	export default {
		mounted() {
			this.get_table(this.page,this.page_size);
		},
		data() {
			return {
				seen: false,
				Edit_flag: false,
				search_flag: false,
				changdu:0,
				page:1,
				page_size:200,
				input_value: '',
				selection_val: [],
				tableData: [],
				multipleSelection: [],
				msg: {},
				update_Ip: this.Ip + '',
				update_disabled: false, //导入开关控制
				fullscreenLoading:false
			}
		},
		watch: {
			tableData: [],
		},
		methods: {
			get_table(page,page_size) {
				this.fullscreenLoading = true
				this.$axios.get(this.Ip + "/HmiExternalQA/"+page+'/'+page_size).then(res => {
					if(res.data.result == 'OK'){
						this.changdu = res.data.rowcount
						for(let i = 0; i < res.data.content.length; i++) {
							res.data.content[i].seen = false;
						}
						this.tableData = res.data.content
						this.fullscreenLoading = false
					}else{
						this.$alert("数据异常",{title:"提示"})
					}
					
				})
			},
			select_line(val) {
				this.selection_val = val;
				//				console.log(val, "val")
			},
			Edit(row, column, cell, event) {
				//Edit_flag与row.seen状态对立，一对二的关系，每
				if(this.Edit_flag == false) {
					if(row.seen == true) {
						row.seen = false;
						this.Edit_flag = true;
					} else {
						row.seen = true;
						this.Edit_flag = false;
					}
				} else {
					if(row.seen == false) {
						row.seen = true;
						this.Edit_flag = false;
					} else {
						row.seen = false;
						this.Edit_flag = true;
					}
				}
			},
			add_table() {
				this.tableData.push({
					answer_date: '',
					answer_detail: '',
					answer_reviewer: '',
					answerer: '',
					detail: '',
					hope_answer_date: '',
					qa_author: '',
					qa_date: '',
					qa_no: '',
					qa_rc_id: '',
					qa_reviewer: '',
					question: '',
					remark: '',
					seen: false,
					status: '',
					summary: '',
				});
				//				console.log(this.tableData, "data")
			},
			listPageChange(val){
				this.page = val
				this.get_table(this.page,this.page_size)
			},
			delete_table() {
				//				console.log(this.selection_val, "选中的数据")
				if(this.selection_val.length == 0) {
					this.$notify({
						type: 'error',
						message: "请选择删除条目"
					})
				} else {
					this.$confirm("是否删除？", '提示', {
						confirmButtonText: '确定',
						cancelButtonText: '取消',
						type: 'warning'
					}).then(() => {
						let Del_data = {
							datas: '',
							user_id: ''
						};
						let datas = [];
						for(let i = 0; i < this.selection_val.length; i++) {
							datas.push({
								qa_rc_id: this.selection_val[i].qa_rc_id
							})
						};
						Del_data.datas = datas;
						Del_data.user_id = window.sessionStorage.getItem('admin');
						//            console.log(Del_data, "post-data")
						this.$axios.post(this.Ip + "/HmiExternalQADel", Del_data).then(res => {
							if(res.datat.result == 'OK') {
								this.$message({
									type: 'success',
									message: '删除成功',
								});
							}
						}).catch(res => {
							this.$message({
								type: 'info',
								message: '连接服务器失败',
							});
						});
					}).catch(() => {
						this.$message({
							type: 'info',
							message: '已取消删除',
						});
					})
				}
			},
			save_table() {
				let update_tableData = this.tableData;
				//循环遍历出seen元素，删除元素的属性
				for(var key of update_tableData) {
					//		  console.log(delete key['seen'],"key")
					if(key['seen'] == true) { // 当seen键还在的时候，把seen的状态全部改为false，画面编辑状态关闭
						key.seen = false;
					}
					delete key['seen']; //删除seen这个键
				}
				let up_data = {
					datas: '',
					user_id: ''
				};
				up_data.datas = update_tableData;
				up_data.user_id = window.sessionStorage.getItem('admin');
				//        console.log(up_data, "end_data")
				//		发送数据给后台
				this.$axios.post(this.Ip + "/HmiExternalQA", up_data).then(res => {
					if(res.data.result == OK) {
						this.$notify({
							type: "success",
							message: "保存成功"
						});
						this.get_table();
					} else {
						this.$notify({
							type: "error",
							message: "保存失败"
						});
					};
				})
			},
		}
	}
</script>

<style scoped>
	.text_show {
		margin-left: 10px;
		font-size: 12px;
		display: block;
		min-height: 50px;
		max-height: 50px;
	}
	
	.btn {
		margin-top: 40px;
		height: 20px;
		float: right;
	}
	
	.cell {
		display: grid;
	}
	
	.input_search {
		width: 250px;
	}
	/*.s_section{*/
	/*width: 100%;*/
	/*vertical-align: middle;*/
	/*margin: 15px 0;*/
	/*}*/
</style>
