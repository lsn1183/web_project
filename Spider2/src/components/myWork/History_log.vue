<template>
	<div class="log_dialog" id="log_dialog">
		<div class="left">
			<div class="list">
				<div style="margin-top: 20px;">
					<li class="li" v-for="(item,index) in loglist" :class="{'active':num == index}" @click="Tosee(item.commit_log_ref_id,index)">
						<span style="margin-left: 40px;"></span><span :class="{'active':num == index}">{{item.title}}</span>
					</li>
				</div>
			</div>
			<div class="page">
				<el-pagination small id="list_log_page" @current-change="listChange" :current-page="page" :page-size="page_size" layout="total, prev, pager, next" :total="changdu"></el-pagination>
			</div>
		</div>
		<div class="right">
			<div style="margin-top: 20px"></div>
			<h3 class="title">
				<span style="margin-left: 2%;">样式图例</span>
				<span style="color: blue;">新增</span>
				<span style="color: red;">修改</span>
				<s style="font-style: italic;">删除</s>
				<div v-show="num_flag" style="display: inline-block;margin-left: 735px;">

					<el-button type="text" style="color:#42b983;fontWeight:bold" @click="crunt()">上一条</el-button>
					<el-button type="text" style="color:#42b983;fontWeight:bold" @click="next()">下一条</el-button>
					<i class="el-icon-close" style="margin-left: 10px;" @click="guanbi"></i>
				</div>
				<div v-show="num_close_flag" style="display: inline-block;">
					<i class="el-icon-close" style="margin-left: 847px;" @click="guanbi"></i>
				</div>
			</h3>
			<div class="solid" style="position: relative;">
				<div class="logcontent fl" style="height:35px;">
					<div class="fl" style="width:554px;text-align: center;background-color: #eef1f6;line-height:35px;">
						标题
					</div>
				</div>
				<div class="logcontent fl" style="height:35px;">
					<div class="fl" style="width: 247px;text-align: center;background-color: #eef1f6;line-height:35px;">
						旧版本内容
					</div>
				</div>
				<div class="logcontent fl" style="height:35px;">
					<div class="fl" style="width: 246px;text-align: center;background-color: #eef1f6;line-height:35px;">
						新版本内容
					</div>
				</div>
				<div class="logcontent fl" style="height:35px;height:35px;position: absolute;left: 1067px;top:0px;width: 200px;text-align: center;z-index: 9002;">
					<div class="fl" style="width: 200px;text-align: center;background-color: #eef1f6;line-height:35px;">
						作业状态
					</div>
				</div>
				<div style="height:35px;position: absolute;left: 1067px;top:35px;width: 200px;text-align: center;z-index: 9002;">
					<div style="line-height: 35px;border: solid 1px #dfe6ec;margin-bottom: 10px;">
						<span type="primary" v-if="work_status == 1?true:false">审核失败</span>
						<span type="primary" v-if="work_status == 2?true:false">未审核</span>
						<span type="primary" v-if="work_status == 3?true:false">审核成功</span>
					</div>
					<div>
						<!--<el-button type="primary" class="el-button_ex el-button--primary_ex" @click="examine(1)" v-if=" Roles == true && work_status== 2?true:false">拒绝</el-button>-->
						<!--<el-button type="primary" class="el-button_ex el-button--primary_ex" @click="examine(3)" v-if=" Roles == true && work_status == 2?true:false">确认</el-button>-->
					</div>
				</div>
			</div>
			<ARLlist v-if="ARL_log_flag" class="show_HU" :commit_id="ct_id" :commit_m_id="ct_m_id"></ARLlist>
			<HUlist v-if="HU_log_flag" class="show_HU" :commit_id="ct_id" :commit_m_id="ct_m_id" @get_Boolean_Examine='set_Boolean_Examine' :Boolean_Examine_Flag='work_status'></HUlist>
			<HUBasiclist v-if="HU_basic_log_flag" class="show_HU" :commit_id="ct_id" :commit_m_id="ct_m_id" @get_Boolean_Examine='set_Boolean_Examine' :Boolean_Examine_Flag='work_status'></HUBasiclist>
			<!--new-add-->
			<TAGLDeflist v-if="TAGL_log_flag" class="show_HU" :commit_id="ct_id" :commit_m_id="ct_m_id" @get_Boolean_Examine='set_Boolean_Examine' :Boolean_Examine_Flag='work_status'></TAGLDeflist>
			<TAGLDefBasiclist v-if="TAGL_log_basic_flag" class="show_HU" :commit_id="ct_id" :commit_m_id="ct_m_id" @get_Boolean_Examine='set_Boolean_Examine' :Boolean_Examine_Flag='work_status'></TAGLDefBasiclist>
			<TAGLAnalist v-if="TAGL_ana_log_flag" class="show_HU" :commit_id="ct_id" :commit_m_id="ct_m_id" @get_Boolean_Examine='set_Boolean_Examine' :Boolean_Examine_Flag='work_status'></TAGLAnalist>
			<TAGLAnaBasiclist v-if="TAGL_ana_basic_log_flag" class="show_HU" :commit_id="ct_id" :commit_m_id="ct_m_id" @get_Boolean_Examine='set_Boolean_Examine' :Boolean_Examine_Flag='work_status'></TAGLAnaBasiclist>
			<!--new-add-->
		</div>

	</div>
</template>
<script>
	import ARL_list_log from './ARL_in_history.vue'
	import HU_list_log from './HU_in_history.vue'
	import HU_list_basic_log from './HU_in_basic_history.vue'
	import TAGLDef_list_log from './TAGLDef_in_history.vue'
	import TAGLDef_list_basic_log from './TAGLDef_in_basic_history.vue'
	import TAGLAna_list_log from './TAGLAna_in_history.vue'
	import TAGLAna_list_basic_log from './TAGLAna_in_basic_history.vue'
	require('../../assets/js/jquery-1.8.3.min.js')
	export default {
		props: ["commit_id", "comit_m_id"],
		components: {
			"ARLlist": ARL_list_log,
			"HUlist": HU_list_log,
			"HUBasiclist": HU_list_basic_log, //new add
			"TAGLDeflist": TAGLDef_list_log,
			"TAGLDefBasiclist": TAGLDef_list_basic_log, //new add
			"TAGLAnalist": TAGLAna_list_log,
			"TAGLAnaBasiclist": TAGLAna_list_basic_log //new add
		},
		data() {
			return {
				leadGp: [],
				p_list: [],
				old_group: '',
				Roles: false,
				work_status: 4,
				ARL_log_flag: false,
				HU_log_flag: false,
				HU_basic_log_flag: false, //new add
				TAGL_log_flag: false,
				TAGL_log_basic_flag: false, //new add
				TAGL_ana_log_flag: false,
				TAGL_ana_basic_log_flag: false, //new add
				ct_id: this.commit_id,
				ct_m_id: this.comit_m_id,
				logtabletwo: {},
				loglist: [],
				loglist2: [],
				changdu: 0,
				end_id: 0,
				start_id: 0,
				num:0,
				page: 1,
				page_size: 200,
				num_flag: true,
				num_close_flag: true,
			}
		},
		mounted() {
			this.getLeadGroup()
			if(this.ct_m_id == "0") {
				this.getBrief();
				this.getDetial();

				this.num_flag = true
				this.num_close_flag = false
			} else {
				this.$axios.get(this.Ip + "/DetailLog" + "/" + this.ct_id + "/" + this.ct_m_id)
					.then(res => {
						//搜索履历时,上、下一条隐藏
						this.num_flag = false
						this.num_close_flag = true
						if(res.data.result == "OK") {
							this.logtabletwo = res.data.content;
							switch(res.data.classify) {
								case 'arl':
									this.ARL_log_flag = true;
									this.HU_log_flag = false;
									this.HU_basic_log_flag = false;
									this.TAGL_log_flag = false;
									this.TAGL_log_basic_flag = false;
									this.TAGL_ana_log_flag = false;
									this.TAGL_ana_basic_log_flag = false;
									break;
								case 'hu':
									this.ARL_log_flag = false;
									this.HU_log_flag = true;
									this.HU_basic_log_flag = false;
									this.TAGL_log_flag = false;
									this.TAGL_log_basic_flag = false;
									this.TAGL_ana_log_flag = false;
									this.TAGL_ana_basic_log_flag = false;
									break;
								case 'basic_req_hu':
									this.ARL_log_flag = false;
									this.HU_log_flag = false;
									this.HU_basic_log_flag = true;
									this.TAGL_log_flag = false;
									this.TAGL_log_basic_flag = false;
									this.TAGL_ana_log_flag = false;
									this.TAGL_ana_basic_log_flag = false;
									break;
								case 'definition':
									this.ARL_log_flag = false;
									this.HU_log_flag = false;
									this.HU_basic_log_flag = false;
									this.TAGL_log_flag = true;
									this.TAGL_log_basic_flag = false;
									this.TAGL_ana_log_flag = false;
									this.TAGL_ana_basic_log_flag = false;
									break;
								case 'basic_req_definition':
									this.ARL_log_flag = false;
									this.HU_log_flag = false;
									this.HU_basic_log_flag = false;
									this.TAGL_log_flag = false;
									this.TAGL_log_basic_flag = true;
									this.TAGL_ana_log_flag = false;
									this.TAGL_ana_basic_log_flag = false;
									break;
								case 'basic_req_analysis':
									this.ARL_log_flag = false;
									this.HU_log_flag = false;
									this.HU_basic_log_flag = false;
									this.TAGL_log_flag = false;
									this.TAGL_log_basic_flag = false;
									this.TAGL_ana_log_flag = false;
									this.TAGL_ana_basic_log_flag = true;
									break;
								default:
									this.ARL_log_flag = false;
									this.HU_log_flag = false;
									this.HU_basic_log_flag = false;
									this.TAGL_log_flag = false;
									this.TAGL_log_basic_flag = false;
									this.TAGL_ana_log_flag = true;
									this.TAGL_ana_basic_log_flag = false;
									break;
							};
						} else {
							this.logtabletwo = [];
							this.$alert("没数据o(╥﹏╥)o")
						}

					})
			}

		},
		methods: {
			getLeadGroup() {
				this.$axios.get(this.Ip + '/UserContent/' + window.sessionStorage.getItem('admin'))
					.then(res => {
						this.p_list = res.data.content;
						if(this.p_list.permission_list.length != 0) {
							for(var i = 0; i < this.p_list.permission_list.length; i++) {
								if(this.p_list.permission_list[i].roles.length != 0) {
									for(var j = 0; j < this.p_list.permission_list[i].roles[j]; j++) {
										switch(this.p_list.permission_list[i].roles[j]) {
											case 4:
												this.leadGp.push(this.p_list.permission_list[i].group_id)
												break;
											default:
												break;
										}
									}
								}
							}
						}

					})
			},
			checkRull() {
				var Roles_Agree = window.sessionStorage.getItem('Roles')
				if(Roles_Agree == "Admin" || this.Roles == "PL") {
					this.Roles = true;
				} else if(Roles_Agree == "Leader") {
					this.Roles = false;
					if(this.leadGp.length != 0) {
						for(var i = 0; i < this.leadGp.length; i++) {
							if(this.old_group == this.leadGp[i]) {
								this.Roles = true;
							}
						}
					}
				} else {

				}
			},
			set_Boolean_Examine(val) {
				this.work_status = val
			},
			getBrief() {
				this.$axios.get(this.Ip + "/BriefLog/" + this.ct_id + "/" + 200 + "/" + 1)
					.then(des => {
						if(des.data.result == "OK") {
							this.loglist = des.data.content;
							for(var i = 0; i < this.loglist.length; i++) {
								switch(this.loglist[i].classify) {
									case 'arl':
										var ARLID = "要求式样" + this.loglist[i].id
										this.loglist[i].title = ARLID
										break;
									case 'hu':
										var HU = "机能式样" + this.loglist[i].id
										this.loglist[i].title = HU
										break;
									case 'definition':
										var DEF = "要件定義" + this.loglist[i].id
										this.loglist[i].title = DEF
										break;
									default:
										var ANA = "要件分析" + this.loglist[i].id
										this.loglist[i].title = ANA
										break;

								};
							}
							this.changdu = des.data.total_count;
							this.ct_m_id = des.data.content[0].commit_log_ref_id
							switch(des.data.content[0].classify) {
								case 'arl':
									this.ARL_log_flag = true;
									break;
								case 'hu':
									this.HU_log_flag = true;
									break;
								case 'definition':
									this.TAGL_log_flag = true;
									break;
								case 'basic_req_hu':
									this.HU_basic_log_flag = true;
									break;
								case 'basic_req_definition':
									this.TAGL_log_basic_flag = true;
									break;
								case 'basic_req_analysis':
									this.TAGL_ana_basic_log_flag = true;
									break;
								default:
									this.TAGL_ana_log_flag = true;
									break;
							};
						} else {
							this.$message({
								type: 'error',
								message: '无数据，请检查'
							})
						}
					})
			},
			getDetial() {
				this.$axios.get(this.Ip + "/DetailLog" + "/" + this.ct_id + "/" + 0)
					.then(res => {
						if(res.data.result == "OK") {
							this.logtabletwo = res.data.content;
							this.end_id = res.data.end_log_ref_id;
							this.start_id = res.data.start_log_ref_id;
						} else {
							this.logtabletwo = [];
							this.$alert("没数据o(╥﹏╥)o")
						}

					})
			},
			guanbi() {
				this.$emit('guanbi', "")

			},
			ListAxios(ct_id, size, page) {
				this.$axios.get(this.Ip + "/BriefLog/" + ct_id + "/" + size + "/" + page)
					.then(des => {
						if(des.data.result == "OK") {
							this.loglist = des.data.content;
							for(var i = 0; i < this.loglist.length; i++) {
								switch(this.loglist[i].classify) {
									case 'arl':
										var ARLID = "要求式样ID" + this.loglist[i].id
										this.loglist[i].title = ARLID
										break;
									case 'hu':
										var HU = "机能式样" + this.loglist[i].id
										this.loglist[i].title = HU
										break;
									case 'definition':
										var DEF = "要件定義" + this.loglist[i].id
										this.loglist[i].title = DEF
										break;
									default:
										var ANA = "要件分析" + this.loglist[i].id
										this.loglist[i].title = ANA
										break;

								};
							}
							this.changdu = des.data.total_count;
							this.ct_m_id = des.data.content[0].commit_log_ref_id
							switch(des.data.content[0].classify) {
								case 'arl':
									this.ARL_log_flag = true;
									break;
								case 'hu':
									this.HU_log_flag = true;
									break;
								case 'definition':
									this.TAGL_log_flag = true;
									break;
								case 'basic_req_hu':
									this.HU_basic_log_flag = true;
									break;
								case 'basic_req_definition':
									this.TAGL_log_basic_flag = true;
									break;
								case 'basic_req_analysis':
									this.TAGL_ana_basic_log_flag = true;
									break;
								default:
									this.TAGL_ana_log_flag = true;
									break;

							};
						}
					})
			},
			listChange(val) {
				var page = val;
				this.ListAxios(this.ct_id, this.page_size, page)
			},
			Tosee(ct_m_id, index) {
				this.ARL_log_flag = false;
				this.HU_log_flag = false;
				this.HU_basic_log_flag = false;
				this.TAGL_log_flag = false;
				this.TAGL_log_basic_flag = false;
				this.TAGL_ana_log_flag = false;
				this.TAGL_ana_basic_log_flag = false;
				this.ct_m_id = ct_m_id;
				this.num = index;
				this.seelog(ct_m_id)
			},
			seelog(val) {
				if(typeof(val) == 'number') {
					this.$axios.get(this.Ip + "/DetailLog" + "/" + this.ct_id + "/" + val)
						.then(res => {
							if(res.data.result == "OK") {
								this.logtabletwo = res.data.content;
								this.end_id = res.data.end_log_ref_id;
								this.start_id = res.data.start_log_ref_id;
								switch(res.data.classify) {
									case 'arl':
										this.ARL_log_flag = true;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'hu':
										this.ARL_log_flag = false;
										this.HU_log_flag = true;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'definition':
										this.ARL_log_flag = false;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = true;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'basic_req_hu':
										this.ARL_log_flag = false;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = true;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'basic_req_definition':
										this.ARL_log_flag = false;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = true;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'basic_req_analysis':
										this.ARL_log_flag = false;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = true;
										break;
									default:
										this.ARL_log_flag = false;
										this.TAGL_ana_log_flag = true;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = true;
										this.TAGL_ana_basic_log_flag = false;
										break;
								};

							} else {
								// this.logtabletwo =[];
								this.$alert("没数据o(╥﹏╥)o")
							}

						})
				} else {
					this.$axios.get(this.Ip + "/DetailLog" + "/" + this.ct_id + "/" + this.ct_m_id)
						.then(res => {
							if(res.data.result == "OK") {
								this.logtabletwo = res.data.content;
								this.end_id = res.data.end_log_ref_id;
								this.start_id = res.data.start_log_ref_id;
								switch(res.data.classify) {
									case 'arl':
										this.ARL_log_flag = true;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'hu':
										this.ARL_log_flag = false;
										this.HU_log_flag = true;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'definition':
										this.ARL_log_flag = false;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = true;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'basic_req_hu':
										this.ARL_log_flag = false;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = true;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'basic_req_definition':
										this.ARL_log_flag = false;
										this.HU_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = true;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = false;
										break;
									case 'basic_req_analysis':
										this.ARL_log_flag = false;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = false;
										this.TAGL_ana_basic_log_flag = true;
										break;
									default:
										this.ARL_log_flag = false;
										this.TAGL_ana_log_flag = true;
										this.HU_log_flag = false;
										this.HU_basic_log_flag = false;
										this.TAGL_log_flag = false;
										this.TAGL_log_basic_flag = false;
										this.TAGL_ana_log_flag = true;
										this.TAGL_ana_basic_log_flag = false;
										break;
								};

							} else {
								// this.logtabletwo =[];
								this.$alert("没数据o(╥﹏╥)o")
							}

						})
				}

			},
			next() {
				if(this.ct_m_id == this.end_id) {
					this.$alert("本页没有下一条信息了")

				} else {
					//					this.ARL_log_flag = false;
					//					this.HU_log_flag = false;
					//					this.TAGL_log_flag = false;
					//					this.TAGL_ana_log_flag = false;
					//					new ADD
					this.ARL_log_flag = false;
					this.HU_log_flag = false;
					this.HU_basic_log_flag = false;
					this.TAGL_log_flag = false;
					this.TAGL_log_basic_flag = false;
					this.TAGL_ana_log_flag = false;
					this.TAGL_ana_basic_log_flag = false;
					this.ct_m_id = this.ct_m_id + 1;
					this.num = this.num + 1;
					this.seelog();
				}

			},
			examine(val) {
				if(val == 1) {
					this.work_status = 1
				} else if(val == 3) {
					this.work_status = 3
				} else {
					this.work_status = 2
				}
			},
			crunt() {
				if(this.ct_m_id == this.start_id) {
					this.$alert("本页没有上一条信息了")
				} else {
					//					this.ARL_log_flag = false;
					//					this.HU_log_flag = false;
					//					this.HU_basic_log_flag = false;
					//					this.TAGL_log_flag = false;
					//					this.TAGL_ana_log_flag = false;
					//					this.TAGL_ana_basic_log_flag = false;
					//          new ADD
					this.ARL_log_flag = false;
					this.HU_log_flag = false;
					this.HU_basic_log_flag = false;
					this.TAGL_log_flag = false;
					this.TAGL_log_basic_flag = false;
					this.TAGL_ana_log_flag = false;
					this.TAGL_ana_basic_log_flag = false;
					this.ct_m_id = this.ct_m_id - 1;
					this.num = this.num - 1;
					this.seelog();
				}

			},
			// check_rule(item){
			// 	if(item.type =1){
			// 		if(item.old_val=''&&item.val!=''){
			// 			this.item.blue_flag = true;
			// 		}else if(item.old_val!=''&&item.val!=''){
			// 			this.item.red_flag = true;
			// 		}else if(item.old_val!=''&&item.val=''){
			// 			this.item.del_flag = true;
			// 		}
			// 	}
			// },

		}
	}
</script>
<style scoped>
	* {
		margin: 0;
		padding: 0;
		font-size: 14px;
	}

	.log_dialog {
		width: 100%;
		/*min-width: 1452px;*/
		position: fixed;
		background: rgba(255, 255, 255, 1);
		z-index: 999;
		/*display: none;*/
	}

	.left {
		position: absolute;
		left: 0;
		height: 100%;
		width: 15%;
		min-width: 300px;
		overflow-y: scroll;
		border-right: 1px solid #dfe6ec;
	}

	.list {
		position: absolute;
		top: 0;
		left: 0;
		bottom: 40px;
		min-width: 300px;
		overflow-y: scroll;
	}

	.page {
		position: absolute;
		bottom: 0;
		left: 0;
		height: 40px;
	}

	.right {
		position: absolute;
		left: 20%;
		right: 0;
		height: 100%;
		width: 80%;
		/*border: 1px solid blue;*/
		min-width: 1151px
	}

	.fl {
		float: left;
	}

	.el-icon-close {
		line-height: 35px;
		cursor: pointer;
	}

	.el-icon-close:hover {
		color: #42b983
	}

	.li {
		cursor: pointer;
		height: 36px;
		line-height: 36px;
		list-style: none;
	}

	.li:hover {
		background-color: #dfe6ec;
	}

	.active {
		color: #42b983;
		font-weight: bold;
	}

	.show_HU {
		z-index: 9001;
		position: relative;
		bottom: 0;
		top: 0px;
	}

	.el-button_ex {
		display: inline-block;
		line-height: 1;
		white-space: nowrap;
		cursor: pointer;
		background: #fff;
		border: 1px solid #c4c4c4;
		color: #1f2d3d;
		margin: 0;
		padding: 10px 15px;
		border-radius: 4px;
	}

	.el-button--primary_ex {
		color: #fff !important;
		background-color: #42b983;
		border-color: #42b983;
	}
</style>
