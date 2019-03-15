<template>
	<div  class="wrapper">
		<div class="form-table">
			<div class="header">
				<span style="width:50%;display:inline-block" @keyup.enter="search_click(searchValue)" >
					<el-input clearable @clear="clear_click()" v-on:input="clear_click()" size="small" placeholder="请输入搜索内容" v-model="searchValue" class="input-with-select">
						<el-button slot="append" icon="el-icon-search" @click="search_click(searchValue)"></el-button>
					</el-input>
				</span>
				<span class="append-span" @click="Add_Doc()">[ 添加文档 ]</span>
			</div>
			<div class="main" style="margin-top:20px">
				<el-table  :data='tableData' style="width: 97%;" :max-height="adaptivePageHeight" border>
					<el-table-column prop='doc_id' label="文档编号" width="130" header-align="center" align="center">
					</el-table-column>
					<el-table-column prop='doc_title' align='left' header-align='center' label="文档标题" min-width="300" label-position="left">
						<template slot-scope="scope">
							<span @click="go_doc_text(scope.row)" class="go-doc-text">
								{{scope.row.doc_title}}
							</span>
						</template>
					</el-table-column>
					<el-table-column prop='committer' label="提交人" min-width="120" align='left' header-align='center'>
					</el-table-column>
					<el-table-column prop="doc_id" label="编辑" align='center' header-align='center' min-width="150" >
						<template slot-scope="scope">
							<span @click="edit_tag(scope.row)" class="column-span mg10">[ 编辑 ]</span>
							<span @click="delete_tag(scope.row.doc_id)" class="column-span mg10">[ 删除 ]</span>
						</template>
					</el-table-column>
				</el-table>
			</div>
			<div class="form-page">
				<el-pagination id="list_page" @current-change="listPageChange" :current-page="page" :page-size="page_size" layout="total, prev, pager, next,jumper" :total="changdu"></el-pagination>
			</div>

		</div>
		
	</div>
</template>
<script>
export default {
	data () {
		return {
			auto_up_flag: false,
			input_flag: true,
			up_ip: this.Ip + "/Doc",
			dialogFormVisible: false,
			up_disable_flag: true,
			ruleForm: {
				doc_type: '',
				doc_title: '',
				path: '',
				Tags: [],
				ver: 1,
				committer: window.sessionStorage.getItem("Uall"),
			},
            page: 1,
			page_copy: null,            
			page_size: 20,
			changdu: 0,
			datas: [],
			tableData: [],
			tag_id: "",
			user_name: window.sessionStorage.getItem("Uall"),
			msg_content: '',
			DOC_content_flag: false,
			timeValue: "",
			DocList_flag: true,
			CountList_flag: false,
			tableData2: [],
			searchValue: '',
			searchType: "",
			url_showFlag: false,
			down_showFlag: false,
			text_showFlag: false,
            adaptivePageHeight: window.innerHeight - 200,
            failure_mode_search:null
		}
	},
	destroyed () {
		window.sessionStorage.removeItem('diffTitleFlag')
		window.sessionStorage.removeItem('tag_id')
	},
	computed: {
		getUserIcons () {
			return this.$store.state.text_type
        },
	},
	watch: {
		getUserIcons (val) {
            // console.log(val,'val')
            if (!val) {
                this.tag_id=''
                this.get_node_click()
                return
            }
            if (val.type == "failure_mode") {//failure_mode
                this.failure_mode_search=val
                this.get_failure_mode(val)
            }else{
                this.page=1
                this.tag_id = Number(val)
                this.get_node_click();
            }
        },
    },
    mounted () {
        this.windowOnresize()
        if (this.$route.query.params) {
            this.tag_id = this.$route.query.params
        }
        if (this.$route.query.page) {
            let page = Number(this.$route.query.page);
            this.$nextTick(() => {
                this.listPageChange(page)
            })
        } else {
            this.get_node_click()
        }
    },
    beforeDestroy () {
        // 存储下一个页面页数
        // var pageNum =Number(JSON.stringify(this.page_copy))
        // window.sessionStorage.setItem("pagination",JSON.stringify(pageNum))
    },
	methods: {
        get_failure_mode(val){
            this.searchType = "failure_mode"
            if (val.tag == "Failure mode") {//请求所有
                this.$axios.get(this.Ip + "/DocByFailureMode/" + this.page + "/" + this.page_size).then(res => {
                    // console.log(res)
                    if (res.data.result =='OK') {
                        this.tableData = res.data.content;
					    this.changdu = res.data.count
                    } else {
                        this.$message({
							type: "error",
							message: "服务器异常"
						})
						this.tableData = []
                    }
                })
            }else{
                this.$axios.get(this.Ip + "/DocByFailureMode/" + this.page + "/" + this.page_size +'/' + val.tag).then(res => {
                    // console.log(res)
                    if (res.data.result =='OK') {
                        this.tableData = res.data.content;
					    this.changdu = res.data.count
                    } else {
                        this.$message({
							type: "error",
							message: "服务器异常"
						})
						this.tableData = []
                    }
                })
            }
            
        },
		get_node_click () {
            // this.page = 1
			this.searchType = ""
            //调用所有文章
            // console.log('进来了',this.tag_id)
			if (!this.tag_id) {
				this.$axios.get(this.Ip + "/DocByTag/" + this.page + "/" + this.page_size).then(res => {
					if (res.data.result == "OK") {
						this.tableData = []
						this.tableData = res.data.content;
						this.changdu = res.data.count
					} else {
						this.$message({
							type: "error",
							message: "服务器异常"
						})
						this.tableData = []
					}
				})
			} else {
				this.$axios.get(this.Ip + "/DocByTag/" + this.page + "/" + this.page_size + "/" + this.tag_id).then(res => {
					if (res.data.result == "OK") {
						this.tableData = []
						this.tableData = res.data.content;
						this.changdu = res.data.count
					} else {
						this.$message({
							type: "error",
							message: "服务器异常"
						})
						this.tableData = []
					}
				})
			}
		},
		Add_Doc () {
			// newAdd:
			if (this.userPurviewManage('Knowledge条目_添加') == true) {
				this.$axios.get(this.Ip + "/TagRequiredGroups").then(res => {
					const tagData = JSON.stringify(res.data.content);
					window.sessionStorage.setItem("tagData", tagData);
				})
				//跳转路由，新界面、
				this.$router.push("/tagl/Form_Modle/Add_Form");
			} else {
				this.$message({
					type: "warning",
					message: "您没有权限操作！"
				})
			}

		},
		delete_tag (val) {
			if (this.userPurviewManage('Knowledge条目_删除') == true) {
				if (val != "") {
					this.$confirm(this.globalData.hint.delete, '提示', {
						confirmButtonText: "确定",
						cancelButtonText: "取消",
						type: 'warning'
					}).then(() => {
						this.$axios.delete(this.Ip + "/Doc/" + val).then(res => {
							if (res.data.result == 'OK') {
								let id = this.$store.state.text_type
								this.get_node_click(id);
								this.$store.state.basic_type = id;
							} else {
								this.$message({
									type: 'error',
									message: "删除失败"
								})
							}
						})
					})
				}
			} else {
				this.$message({
					type: "warning",
					message: "您没有操作权限！"
				})
			}
		},
		edit_tag (val) {
            if (this.userPurviewManage('Knowledge条目_编辑') == true) {
                if (val) {
                    window.sessionStorage.setItem("doc_id", JSON.stringify(val.doc_id))
                    let doc_id = JSON.parse(window.sessionStorage.getItem("doc_id"));
                    this.$store.state.form_item_id = doc_id;
                    // newAdd 必填tag请求：
                    this.$axios.get(this.Ip + "/TagRequiredGroups").then(res => {
                        const tagData = JSON.stringify(res.data.content);
                        window.sessionStorage.setItem("tagData", tagData);
                    })
                    let routeValue = { path: '/tagl/Form_Modle/Edit_Form', query: { page: this.page_copy } }
                    this.$router.push(routeValue);
                }
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有权限操作！"
                })
            }

        },
        go_doc_text (val) {
            let data = {
                'data':val,
                'server_ip':this.Ip
            }
            window.sessionStorage.setItem("listDocID", JSON.stringify(data))
            window.open("../../../static/DocList-item.html")

        },
        fileDown (file) {
            if (file) {
                window.open(this.Ip + '/DownFile/' + file)
            } else {
                this.$message({
                    type: 'error',
                    message: '无法下载'
                })
            }
        },
        // 分页
        listPageChange (val) {
            if (val) {
                // 存储所点击页面页数，用于存储session
                this.page_copy = Number(val)
            }
            if (this.searchType == "search") {
                this.$axios.get(this.Ip + "/DocQuery/" + val + "/" + this.page_size + "/" + this.searchValue).then(res => {
                    if (res.data.result == "OK") {
                        this.tableData = res.data.content
                        // 默认高亮哪一页
                        this.page = this.page_copy
                        this.changdu = res.data.count
                    } else {
                        this.$message({
                            type: "error",
                            message: "暂无内容"
                        })
                        this.tableData = []
                    }
                })
            } else if(this.searchType == 'failure_mode'){
                if (this.failure_mode_search.tag == "Failure mode") {
                    this.$axios.get(this.Ip + "/DocByFailureMode/" + val + "/" + this.page_size).then(res=>{
                        if (res.data.result =='OK') {
                            this.tableData = res.data.content;
                            this.changdu = res.data.count
                        } else {
                            this.$message({
                                type: "error",
                                message: "服务器异常"
                            })
                            this.tableData = []
                        }
                    }) 
                }else{
                    this.$axios.get(this.Ip + "/DocByFailureMode/" + val + "/" + this.page_size +'/'+ this.failure_mode_search.tag).then(res=>{
                        if (res.data.result =='OK') {
                            this.tableData = res.data.content;
                            this.changdu = res.data.count
                        } else {
                            this.$message({
                                type: "error",
                                message: "服务器异常"
                            })
                            this.tableData = []
                        }
                    }) 
                }
            }else {
                if (!this.tag_id) {
                    this.$axios.get(this.Ip + "/DocByTag/" + val + "/" + this.page_size).then(res => {
                        if (res.data.result == "OK") {
                            // 默认高亮哪一页
                            this.page = this.page_copy
                            this.tableData = res.data.content;
                            this.changdu = res.data.count
                            
                        } else {
                            this.$message({
                                type: "error",
                                message: "服务器异常"
                            })
                            this.tableData = []
                        }
                    })
                } else {
                    this.$axios.get(this.Ip + "/DocByTag/" + val + "/" + this.page_size + "/" + this.tag_id).then(res => {
                        if (res.data.result == "OK") {
                            // 默认高亮哪一页
                            this.page = this.page_copy
                            this.tableData = res.data.content;
                            this.changdu = res.data.count
                            
                        } else {
                            this.$message({
                                type: "error",
                                message: "服务器异常"
                            })
                            this.tableData = []
                        }
                    })
                }
            }
        },
        // 统计：
        CountFun () {
            this.CountList_flag = true;
            this.DocList_flag = false;
            this.$axios.get(this.Ip + "/DocGroupUser").then(res => {
                if (res.data.result == "OK") {
                    this.tableData2 = res.data.content;
                } else {
                    this.$message({
                        type: "error",
                        message: res.data.result
                    })
                }
            })
        },
        GetDate (value) {
            if (value != null) {
                let time = value;
                this.$axios.get(this.Ip + "/DocGroupUser/" + time).then(res => {
                    if (res.data.result == "OK") {
                        this.tableData2 = res.data.content;
                    } else {
                        this.tableData2 = []
                    }
                })
            } else {
                this.CountFun();
            }
        },
        search_click () {
            this.page = 1
            this.searchType = "search"
            this.$axios.get(this.Ip + "/DocQuery/" + this.page + "/" + this.page_size + "/" + this.searchValue).then(res => {
                if (res.data.result == "OK") {
                    this.tableData = res.data.content
                    this.changdu = res.data.count
                } else {
                    this.$message({
                        type: "error",
                        message: "暂无内容"
                    })
                    this.tableData = []
                    this.changdu = 0
                }
            })
        },
        clear_click () {
            this.searchType = ""
            this.get_node_click()
        },
        windowOnresize () {
            this.adaptivePageHeight = window.innerHeight - 200
            const that = this
            window.onresize = () => {
                return (() => {
                    that.adaptivePageHeight = window.innerHeight - 200
                })()
            }
        },
    },
}
</script>
<style scoped>
.wrapper {
    width: 100%;
    height: 100%;
    max-width: 1920px;
    min-width: 480px;
    padding-left: 25px;
    position: relative;
    color: #606266;
}
.form-table {
    line-height: 30px;
    padding-top: 20px;
}
.go-doc-text {
    cursor: pointer;
}
.go-doc-text:hover {
    color: #42b983;
}
.column-span {
    padding: 10px;
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear;
    cursor: pointer;
}
.column-span:hover {
    color: #6bcca0;
}
.append-span {
    float: right;
    margin-right: 47px;
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}
.form-page {
    position: absolute;
    bottom: 20px;
}
</style>
