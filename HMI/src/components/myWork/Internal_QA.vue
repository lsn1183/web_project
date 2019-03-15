<template>
	<div>
		<!--<div class="input_search" @keyup.enter="Table_search(input_value)">-->
		<!--<el-input placeholder="请输入搜索ID" size="small" v-model="input_value">-->
		<!--<el-button slot="append" class="el-icon-search" @click="Table_search(input_value)"></el-button>-->
		<!--</el-input>-->
		<!--</div>-->
		<div id="table_OA" v-loading.lock="fullscreenLoading" element-loading-text="正在载入,请稍等... ...">
			<el-table border style="width: 100% ;top: 10px;height: 100%;line-height: 40px" ref="multipleTable" :data="tableData" @selection-change="select_line" max-height="700">
				<el-table-column type="selection" width="30" header-align="left">
				</el-table-column>
				<el-table-column label="NO" header-align="center" width="50">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.qa_no" v-if="scope.row.seen" size="mini"></el-input>
						<span class="text_show" v-else="">{{ scope.row.qa_no }}</span>
					</template>
				</el-table-column>
				<el-table-column label="状態" header-align="center" width="100">
					<template scope="scope">
						<el-select class="s_section_right" v-model="scope.row.status" placeholder="請選擇狀態" size='medium' v-if="scope.row.seen">
							<el-option :label="scope.row.status" :value="scope.row.status"></el-option>
						</el-select>
						<span class="text_show" v-else="">{{ scope.row.status }}</span>
					</template>
				</el-table-column>
				<el-table-column label="内容" header-align="center">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.question" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" v-else>{{ scope.row.question }}</span>
					</template>
				</el-table-column>
				<el-table-column label="提问日" header-align="center" width="120">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.qa_date" v-if="scope.row.seen" size="mini"></el-input>
						<span class="text_show" v-else>{{ scope.row.qa_date }}</span>
					</template>
				</el-table-column>
				<el-table-column label="提问者" header-align="center" width="100">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.qa_author" v-if="scope.row.seen" size="mini"></el-input>
						<span class="text_show" v-else>{{ scope.row.qa_author}}</span>
					</template>
				</el-table-column>
				<el-table-column label="回答希望日" header-align="center" width="120">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.hope_answer_date" v-if="scope.row.seen" size="mini"></el-input>
						<!--<el-date-picker v-model="scope.row.hope_answer_date" format="yyyy-MM-dd" value-format="yyyy-MM-dd" v-if="scope.row.seen" placeholder="选择日期" align="right" size="medium"></el-date-picker>-->
						<span class="text_show" v-else>{{ scope.row.hope_answer_date}}</span>
					</template>
				</el-table-column>
				<el-table-column label="回答" header-align="center">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.answerer" v-if="scope.row.seen" size="medium"></el-input>
						<span class="text_show" v-else>{{ scope.row.answerer }}</span>
					</template>
				</el-table-column>
				<el-table-column label="回答日" header-align="center" width="120">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.answer_date" v-if="scope.row.seen" size="mini"></el-input>
						<!--<el-date-picker v-model="scope.row.answer_date" format="yyyy-MM-dd" value-format="yyyy-MM-dd" v-if="scope.row.seen" placeholder="选择日期" align="right" size="medium"></el-date-picker>-->
						<span class="text_show" v-else>{{ scope.row.answer_date }}</span>
					</template>
				</el-table-column>
				<el-table-column label="回答者" header-align="center" width="100">
					<template scope="scope">
						<el-input type="textarea" v-model="scope.row.answer_detail" v-if="scope.row.seen" size="mini"></el-input>
						<span class="text_show" v-else>{{ scope.row.answer_detail }}</span>
					</template>
				</el-table-column>
				<el-table-column label="编辑" header-align="center" width="50">
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
				input_value: '',
				changdu:0,
				page:1,
				page_size:200,
				selection_val: [],
				tableData: [],
				//	get_tableData: [],
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
				this.$axios.get(this.Ip + "/HmiInternalQA/"+page+'/'+page_size).then(res => {
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
			listPageChange(val){
				this.page = val
				this.get_table(this.page,this.page_size)
			},
			Edit(row, column, cell, event) {
				//Edit_flag与row.seen状态对立，一对二的关系，每
				//        console.log(row)
				if(this.Edit_flag == false) {
					if(row.seen == true) {
						row.seen = false;
						//this.Edit_flag = true的时候是关闭编辑按钮
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
						this.$axios.post(this.Ip + "/HmiInternalQADel", Del_data).then(res => {
							if(res.datat.result == 'OK') {
								this.$message({
									type: 'success',
									message: '删除成功',
								});
							}
						}).catch(res => {
							this.$message({
								type: 'info',
								message: '链接服务器失败',
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
				//		发送数据给后台
				this.$axios.post(this.Ip + "/HmiInternalQA", up_data).then(res => {
					//          console.log(res, "发送回调")
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
		font-size: 12px
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
</style>