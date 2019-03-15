<template>
  <div id="ARLlist">
    <div class="BTN">
      <div id="BTN_top">
        <div class="input_search" @keyup.enter="List_search(input_value)">
          <el-input placeholder="请输入搜索ID" size="mini" v-model="input_value">
            <el-button slot="append" class="el-icon-search" @click="List_search(input_value)"></el-button>
          </el-input>
        </div>
      </div>
    </div>
    <div id="treeMap" class="fl" v-loading.lock="fullscreenLoading">
      <ul id="ul">
        <li class="li first_li">
          <span class="cy ID">ID</span>
          <span class="cy ID">名称</span>
          <span class="msy ID" style="width:54%">転記してきた要件</span>
          <span class="cy ID" style="width:7%;">
						<span style="display:block;width:100%;height:100%;">指派给</span>
					</span>
          <span class="cz ID">操作</span>
        </li>
        <li class="li_scroll">
          <ul class="ul_scroll">
            <li class="li" v-for="(item,index) in table1"
                @click.stop='change_up(item.hu_id,index)':key="index">
              <i class="Asa_i" :title="item.hu_id"></i>
              <span class="cy span_width"
                    @click.stop='change_up(item.hu_id,index)'
                    :class="{'active':num == index}" :title="item.hu_id">
								<span style="marginLeft:42px">{{item.hu_id}}</span>
							</span>
              <span class="cy span_width"    :title="item.title">
								<span style="marginLeft:42px">{{item.title}}</span>
							</span>
              <span class="msy" :title="item.info" style="width:54%">
								<span class="msg_msy ">{{item.info}}</span>
							</span>
              <span class="msy" style="width:7%">
								<span style="display:block;width:100%;height:100%;" :title="item.user_name">{{item.user_name}}</span>
							</span>
              <span class="cz cen" @click="amint(item.hu_id,index)"><i class="el-icon-d-arrow-left"> 详细</i></span>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <!--详细：隐藏列表清单-->
    <div id="list" v-show="show_flag">
      <div id="Maplist">
        <div class="nav">
          <i class="el-icon-d-arrow-right fl" style="marginRight:5px" @click="back_up()"></i>
        </div>
        <el-collapse accordion>
          <div class="user_name_title">
            <span><img src="../../assets/img/Icon/user_icon_2.png" class="user_icon"/> {{userNames}}</span>
          </div>
        </el-collapse>
        <el-collapse accordion v-for="(hu_record,hu_index) in tabledata1" :key="hu_index">
          <el-collapse-item :title="hu_record.title" :key="hu_record.title" :name="hu_record.hu_id">
            <div id="hu_table">
              <div class="hutable">
                <div class='table_content' style="width:8%">
                  <p class="table_title">
                    <span>ユニークID</span>
                  </p>
                  <p class="table_msg " :title="hu_record.unique_id" style="textAlign:center">
                    {{hu_record.unique_id}}
                  </p>
                </div>
                <div class='table_content' style="width:51.5% ">
                  <p class="table_title">
                    <span>責務分担</span>
                  </p>
                  <div class="table_msg content_scroll">
                    <p title="" v-for="(sequence_record, sequence_index) in hu_record.sequence_list"
                       :key="sequence_index">
												<span class="option" style="fontWeight:bold">({{sequence_index + 1}}) <br>設備:

													<span style="fontWeight:normal"
                              v-if="sequence_record.name!=''">{{sequence_record.name}}</span>
													<span style="fontWeight:normal"
                              v-if="sequence_record.info!=''">({{sequence_record.info}})</span>

												</span>
                      <span class="option" style="fontWeight:bold" :title='sequence_record.status'>状態:
													<span style="fontWeight:normal">{{sequence_record.status}}</span>
												</span>
                      <span class="option" style="fontWeight:bold" :title='sequence_record.trigger'>トリガー:
													<span style="fontWeight:normal">{{sequence_record.trigger}}</span>
												</span>
                      <span class="option" style="fontWeight:bold" :title='sequence_record.action'>動作:
													<span style="fontWeight:normal">{{sequence_record.action}}</span>
												</span>
                    </p>
                  </div>
                </div>
                <div class='table_content' style="width:24.5%">
                  <p class="table_title">
                    <span>变更理由与日期</span>
                  </p>
                  <div class="table_msg content_scroll" :title="hu_record.reason">
											<span class="option" style="fontWeight:bold">变更理由：
												<span style="fontWeight:normal">{{hu_record.reason}}</span>
											</span>
                    <span class="option" style="fontWeight:bold">日付：
												<span style="fontWeight:normal">{{hu_record.new_date}}</span>
											</span>
                  </div>
                </div>
                <div class='table_content' style="width:7%;textAlign:center">
                  <p class="table_title">
                    <span>任務状態</span>
                  </p>
                  <p class="table_msg content_scroll" :title="hu_record.job_status_name" style="textAlign:center">
                    <span>{{hu_record.job_status_name}}</span>
                  </p>
                </div>
                <div class='table_content' style="width:9%;border:0 none">
                  <p class="table_title">
                    <span>操作</span>
                  </p>
                  <p class="table_msg" title="">
                    <el-button type="text" @click="editClick1(hu_record.hu_id,hu_index)" class="table_move" disabled><i class="el-icon-edit"> 更新</i></el-button>
                  </p>
                </div>					
              </div>
            </div>
            <el-collapse accordion v-for="(definition_record,definition_index) in hu_record.definition_list" :key="definition_index">
              <el-collapse-item :title="definition_record.title" :key="definition_record.title" :name="definition_record.definition_id">
                <div id="tagl_table">
                  <div class="tagl_table">
                    <div class='table_content' style="width:7%">
                      <p class="table_title">
                        <span>ユニークID</span>
                      </p>
                      <p class="table_msg " :title="definition_record.unique_id" style="textAlign:center">
                        {{definition_record.unique_id}}
                      </p>
                    </div>
                    <div class='table_content' style="width:53%">
                      <p class="table_title">
                        <span>責務分担</span>
                      </p>
                      <p class="table_msg content_scroll" title="">
												<span v-for="(sequence_record, sequence_index) in definition_record.sequence_list">
													<span class="option" style="fontWeight:bold">({{sequence_index + 1}}) <br>設備:
														<span style="fontWeight:normal" v-if="sequence_record.name!=''">{{sequence_record.name}}</span>
														<span style="fontWeight:normal" v-if="sequence_record.info!=''">({{sequence_record.info}})</span>
													</span>
													<span class="option" style="fontWeight:bold" :title='sequence_record.status'>状態:
														<span style="fontWeight:normal">{{sequence_record.status}}</span>
													</span>
													<span class="option" style="fontWeight:bold" :title='sequence_record.trigger'>トリガー:
														<span style="fontWeight:normal">{{sequence_record.trigger}}</span>
													</span>
													<span class="option" style="fontWeight:bold" :title='sequence_record.action'>動作:
														<span style="fontWeight:normal">{{sequence_record.action}}</span>
													</span>
												</span>
                      </p>
                    </div>
                    <div class='table_content' style="width:25%;">
                      <p class="table_title" :title='definition_record.reason'>
                        <span>变更理由与日期</span>
                      </p>
                      <div class="table_msg content_scroll" :title="definition_record.reason">
						<span class="option" style="fontWeight:bold">变更理由：
							<span style="fontWeight:normal">{{definition_record.reason}}</span>
						</span>
                        <span class="option" style="fontWeight:bold">日付：
							<span style="fontWeight:normal">{{definition_record.new_date}}</span>
						</span>
                      </div>
                    </div>
                    <div class='table_content' style="width:7%;textAlign:center">
                      <p class="table_title" style="textAlign:center">
                        <span>任務状態</span>
                      </p>
                      <p class="table_msg content_scroll" :title="definition_record.job_status_name">
                        <span>{{definition_record.job_status_name}}</span>
                      </p>
                    </div>
                    <div class='table_content' style="width:8%;border:0 none">
                      <p class="table_title">
                        <span>操作</span>
                      </p>
                      <p class="table_msg" title="">
                        <el-button type="text" class="table_move" @click="editClick2(hu_id,definition_record.definition_id,hu_index,definition_index)" disabled>
                          <i class="el-icon-edit"> 更新</i></el-button>
                      </p>
                    </div>
                  </div>
                </div>
                <el-collapse accordion v-for="(taglana_record,taglana_index) in definition_record.analysis_list" :key="taglana_index">
                  <el-collapse-item :title="taglana_record.title" :key="taglana_record.title" :name="taglana_record.definition_id">
                    <div id="taglana_table">
                      <div class="ana_table">
                        <div class='table_content' style="width:6%">
                          <p class="table_title">
                            <span>ユニークID</span>
                          </p>
                          <p class="table_msg" :title="taglana_record.unique_id" style="textAlign:center">
                            {{taglana_record.unique_id}}
                          </p>
                        </div>
                        <div class='table_content' style="width:54.5%">
                          <p class="table_title">
                            <span>TAGL-PF</span>
                          </p>
                          <p class="table_msg content_scroll ">
							<span v-for="(analist_record, analist_index) in taglana_record.sequence_list">
    	     					<span class="option" style="fontWeight:bold">({{analist_index + 1}})</br>設備:
	    	     					<span style="fontWeight:normal" v-if="analist_record.name!=''">{{analist_record.name}}</span>
	    	     					<span style="fontWeight:normal" v-if="analist_record.info!=''">({{analist_record.info}})</span>
	    	     				</span>
	    	     				<span class="option" style="fontWeight:bold" :title='analist_record.status'>状態:
	    	     					<span style="fontWeight:normal">{{analist_record.status}}</span>
	    	     				</span>
	    	     				<span class="option" style="fontWeight:bold" :title='analist_record.trigger'>トリガー:
	    	     					<span style="fontWeight:normal">{{analist_record.trigger}}</span>
	    	     				</span>
	    	     				<span class="option" style="fontWeight:bold" :title='analist_record.action'>動作:
	    	     					<span style="fontWeight:normal">
	    	     						{{analist_record.action}}
	    	     					</span>
	    	     				</span>
    	     				</span>
                          </p>
                        </div>
                        <div class='table_content' style="width:25.5%">
                          <p class="table_title">
                            <span>变更理由与日期</span>
                          </p>
                          <div class="table_msg content_scroll" :title="taglana_record.reason">
							<span class="option" style="fontWeight:bold">变更理由：
								<span style="fontWeight:normal">{{taglana_record.reason}}</span>
							</span>
                            <span class="option" style="fontWeight:bold">日付：
								<span style="fontWeight:normal">{{taglana_record.new_date}}</span>
							</span>
                          </div>
                        </div>
                        <div class='table_content' style="width:7%;textAlign:center">
                          <p class="table_title" style="textAlign:center">
                            <span>任務状態</span>
                          </p>
                          <p class="table_msg content_scroll" :title="taglana_record.job_status_name">
                            <span>{{taglana_record.job_status_name}}</span>
                          </p>
                        </div>
                        <div class='table_content' style="width:7%;border:0 none">
                          <p class="table_title">
                            <span>操作</span>
                          </p>
                          <p class="table_msg" title="">
                            <el-button type="text" class="table_move" @click="editClick3(hu_record.hu_id,definition_record.definition_id,hu_index,definition_index)" disabled>
                              <i class="el-icon-edit"> 更新</i></el-button>
                          </p>
                        </div>
                      </div>
                    </div>
                  </el-collapse-item>
                </el-collapse>
              </el-collapse-item>
        	  </el-collapse>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>
    <div id="foot">
      <div id="number" class="fr">
        <div class="number_now fr">
          <el-pagination
            id="search_page"
            v-if="search_flag == true"
            @current-change="searchPageChange"
            :current-page="page"
            :page-size="page_size"
            layout="total, prev, pager, next,jumper"
            :total="changdu"
          ></el-pagination>
          <el-pagination
            id="list_page"
            v-if="list_flag == true"
            @current-change="listPageChange"
            :current-page="page"
            :page-size="page_size"
            layout="total, prev, pager, next,jumper"
            :total="changdu"
          ></el-pagination>
        </div>

      </div>
    </div>
    <hu_dialog @dialog_close="hu_dialog_return" @dialog_vue_close="change_up(change_params_id,change_params_index)" v-bind:input_show='HU_flag' v-bind:input_change_params_id="change_params_id">
    </hu_dialog>
  </div>
</template>

<script>
  import dialog_basicreq_hudef from './dialog_basicreq_hudef.vue'

  require('../../assets/js/jquery-1.8.3.min.js')
  export default {
    components: {
      hu_dialog: dialog_basicreq_hudef
    },
    data() {
      return {
        change_params_id: '',
        change_params_index: '',
        fullscreenLoading: false,
        json: {
          user_id: '',
          type: '',
          condition: {}
        },
        input_value: '',
        HU_flag: false,
        BTN_type: window.sessionStorage.getItem('Type'),
        //active初始样式清空
        num: -1,
        noData: '',
        show_flag: false,
        search_flag: false,
        list_flag: true,
        page: 1,
        page_size: 200,
        changdu: 0,
        tabledata1: [],
        table1: [],
        hu_id: '',
        definition_id:'',
        data: '',
        info: '',
        Id: 0,
        nodes: [],
        links: [],
        ndata: [],
        user_names: [],
        userNames: "",
      }
    },
    mounted() {
      this.Id = Number(window.sessionStorage.getItem('admin'));
      this.$axios.get(this.Ip + "/AllUsers")
        .then(res => {
          this.user_names = res.data.content;
        })
      this.Summary_ARL()
    },
    computed: {
      getBasicType() {
        return this.$store.state.basic_type
      }
    },
    watch: {
      getBasicType(val) {
        this.BTN_type = window.sessionStorage.getItem('Type');
        this.num = -1
        this.Summary_ARL()
      }
    },
    methods: {
      hu_dialog_return(params) {
        this.HU_flag = params[0];
      },
      search_axios(user_id, group_id, size, page) {
	      this.json.like_condition = {}
	      this.json.like_condition.hu_id = this.input_value
        this.json.condition.user_id = user_id
        this.json.condition.group_id = group_id;
        this.json.type = this.BTN_type;
        this.json.size = size;
        this.json.page = page;
        this.$axios.post(this.Ip + '/SummaryBasic', this.json)
          .then(res => {
            console.log(res.data)
            if (res.data.result == "OK") {
              this.table1 = res.data.content
              this.changdu = res.data.total_count
              this.fullscreenLoading = false;
            } else {
              this.table1 = []
              this.changdu = 0
              this.fullscreenLoading = false;
            }
          })
      },
      List_search() {
        this.list_flag = false;
        this.search_flag = true;
        this.fullscreenLoading = true;
        if (window.sessionStorage.getItem('workType') == "my") {
          this.search_axios(this.Id, 0, 200, 1)
        } else if (window.sessionStorage.getItem('workType') == "group") {
          this.search_axios(0, window.sessionStorage.getItem('groups_id'), 200, 1)
        } else {
          this.search_axios(0, 0, 200, 1)
        }
      },
      Summary_axios(type, user_id, group_id, like_condition, size, page) {
        var name = '';
        var title = [];
        this.$axios.get(this.Ip + '/ServiceStatus')
				.then(res => {
					if(res.data.result == 'NG'){
						this.$notify({
							type:'error',
							message:'其他人正在release，请耐心等待!',
							showClose:true,
							duration:'0',
						})
						return;
					}else{
						this.$axios.post(this.Ip + '/SummaryBasic', {
		          "type": type,
		          "condition": {"user_id": user_id, "group_id": group_id},
		          "like_condition": {},
		          "size": size,
		          "page": page
		        }).then(res => {
		          this.table1 = []
		          this.table1 = res.data.content;
		          this.changdu = res.data.total_count;
		        }).catch(res => {
		          this.table1 = []
		          this.changdu = 0;
		        })
					}
				})
      },
      Summary_ARL() {
        this.search_flag = false;
        this.list_flag = true;
        this.noData = '';
        this.page = 1;
        if (window.sessionStorage.getItem('workType') == "my") {
          this.Summary_axios(this.BTN_type, this.Id, 0, "", 200, 1)
        } else if (window.sessionStorage.getItem('workType') == "group") {
          this.Summary_axios(this.BTN_type, 0, window.sessionStorage.getItem('groups_id'), "", 200, 1)

        } else {
          this.Summary_axios(this.BTN_type, 0, 0, "", 200, 1)
        }
      },
      listPageChange(val) {
        var user_id = "";
        var group_id = "";
        if (window.sessionStorage.getItem('workType') == "my") {
          this.Summary_axios(this.BTN_type, this.Id, group_id, "", 200, val)
        } else if (window.sessionStorage.getItem('workType') == "group") {
          this.Summary_axios(this.BTN_type, user_id, window.sessionStorage.getItem('groups_id'), "", 200, val)
        } else {
          this.Summary_axios(this.BTN_type, user_id, group_id, "", 200, val)
        }
      },
      searchPageChange(val) {
        var user_id = "";
        var group_id = "";
        this.page = val;
        if (window.sessionStorage.getItem('workType') == "my") {
          this.search_axios(this.Id, 0, 200, this.page)
        } else if (window.sessionStorage.getItem('workType') == "group") {
          this.search_axios(0, window.sessionStorage.getItem('groups_id'), 200, this.page)
        } else {
          this.search_axios(0, 0, 200, this.page)
        }
      },
      change_up:function(id,index){    
      	this.change_params_id = id     
        this.change_params_index = index
        this.num = index;
        var self=this;
        this.list_flag=true;
        this.search_flag = false;
        if(id!=""){
          this.$axios.get(this.Ip+'/BasicTreeInfo/'+this.BTN_type+'/'+this.change_params_id+'/'+window.sessionStorage.getItem('admin')+'/'+1)
            .then(res => {
              this.tabledata1 = []
              this.tabledata1 = res.data.content
              for(var i = 0; i<this.user_names.length; i++){
                if(this.tabledata1!=""){
                  if(this.tabledata1[0].user_id == this.user_names[i].user_id ){
                    this.userNames= this.user_names[i].user_name
                  }
                }
              }
              if(this.tabledata1!=""&&this.tabledata1!=0){
								for(var k = 0;k<this.tabledata1.length;k++){
									this.tabledata1[k].job_status_name=""
				
									if(this.tabledata1[k].job_status == 1){
				
										this.tabledata1[k].job_status_name ="初始狀態，待作業"
				
									}else if(this.tabledata1[k].job_status == 2){
				
										this.tabledata1[k].job_status_name ="作業完了，待翻譯"
				
									}else if(this.tabledata1[k].job_status == 3){
				
										this.tabledata1[k].job_status_name ="翻譯完了"
				
									}
									for(var z = 0;z<this.tabledata1[k].definition_list.length;z++){
				
										this.tabledata1[k].definition_list[z].job_status_name=""
				
										if(this.tabledata1[k].definition_list[z].job_status == 1){
				
											this.tabledata1[k].definition_list[z].job_status_name ="初始狀態，待作業"
				
										}else if(this.tabledata1[k].definition_list[z].job_status == 2){
				
											this.tabledata1[k].definition_list[z].job_status_name ="作業完了，待翻譯"
				
										}else if(this.tabledata1[k].definition_list[z].job_status == 3){
				
											this.tabledata1[k].definition_list[z].job_status_name ="翻譯完了"
				
										}
				
				
										for(var j = 0;j< this.tabledata1[k].definition_list[z].analysis_list.length;j++){
											this.tabledata1[k].definition_list[z].analysis_list[j].job_status_name=""
				
											if(this.tabledata1[k].definition_list[z].analysis_list[j].job_status == 1){
				
												this.tabledata1[k].definition_list[z].analysis_list[j].job_status_name ="初始狀態，待作業"
				
											}else if(this.tabledata1[k].definition_list[z].analysis_list[j].job_status == 2){
				
												this.tabledata1[k].definition_list[z].analysis_list[j].job_status_name ="作業完了，待翻譯"
				
											}else if(this.tabledata1[k].definition_list[z].analysis_list[j].job_status == 3){
				
												this.tabledata1[k].definition_list[z].analysis_list[j].job_status_name="翻譯完了"
				
											}
										}
									}
								}
							}
            })
         }
      },
	    editClick1(hu_id, hu_index) {
	      this.select_hu_id = hu_id;
	      this.HU_flag = true;
	      var this_ = this;
	      $(".dialog_html").animate({height: 785}, 800, function () {
	        $(".hu_table").eq(hu_index).css({display: "block"})
	      })
	    },
	    editClick2(hu_id, definition_id, hu_index, def_index) {
	      this.select_definition_id = hu_id;
	      this.HU_flag = true;
	      var this_ = this;
	      $(".dialog_html").animate({height: 785}, 800, function () {
	        $(".hu_table").eq(hu_index).css({display: "block"})
	        $(".hu_div").eq(hu_index).children(".tagl_div").children(".tagltable").eq(def_index).css({display: "block"})
	      })
	    },
	    editClick3(hu_id, definition_id, hu_index, def_index) {
	      this.select_definition_id = hu_id;
	      this.HU_flag = true;
	      var this_ = this;
	      $(".dialog_html").animate({height: 785}, 800, function () {
	        $(".hu_div").eq(hu_index).children(".tagl_div").children(".tagltable").eq(def_index).css({display: "block"})
	        $(".hu_div").eq(hu_index).children(".tagl_div").eq(def_index).children(".taglana_div").eq(0).children(".taglana_table").eq(0).css({display: "block"})
	      })
	    },
      key_down(event, input_value) {
        if (event.keyCode == 13) {
          this.List_search(input_value);
        }
      },
      amint() {   
      	this.show_flag = true;
        var span_width = $(".span_width").width()
        $("#list").animate({left: span_width}, 1000)
      },
      back_up() {
      	var this_ = this;
      	$("#list").animate({left:2000},1000,function(){
					this_.show_flag = false
				})
      },
    }
  }
</script>

<style scoped>
  .el-dialog--small {
    width: 80%;
  }

  #ARLlist {
    position: relative;
    height: 100%;
    width: 100%;
    overflow: hidden;
    font-family: "微软雅黑";
    font-size: 14px;
    top: 10px;
  }

  #treeMap {
    position: absolute;
    top: 49px;
    bottom: 49px;
    left: 0;
    width: 100%;
    text-align: center;
    font-size: 14px;
    background: #fff;
  }

  .li_scroll {
    list-style: none;
  }

  .ul_scroll {
    width: 100%;
    overflow-y: scroll;
    height: 770px;
    overflow-x: hidden;
  }

  #foot {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50px;
    line-height: 24px;
    font-size: 14px;
    background: #fff;
    border-top: 1px solid #dfe6ec;
  }

  #ARLlist .BTN {
    position: fixed;
    z-index: 688;
    left: 16%;
    width: 83%;
    min-width: 1024px;
    background-color: rgb(243, 243, 243);
  }

  #ARLlist .BTN #BTN_top {
    background-color: white;
    position: relative;
  }

  #BTN_top {
    width: 100%;
    padding-bottom: 5px;
    border-bottom: 1px solid #dfe6ec;
    height: 50px;
    line-height: 50px;
  }

  #ARLlist .BTN #BTN_title_top {
    position: relative;
    background-color: white;
    height: 46px;
  }

  #ARLlist .BTN #BTN_num {
    position: relative;
    width: 100%;
    background-color: white;
  }

  #ARLlist .BTN #BTN_title_top #BTN_title_top_left {
    position: absolute;
    left: 0px;
    top: 0px;
    height: 46px;
    line-height: 46px;
    width: 210px;
    text-align: center;
    color: #20A0FF;
    font-size: 20px;
  }

  #ARLlist .BTN #BTN_title_top #BTN_title_top_right {
    position: absolute;
    top: 0;
    right: 0;
    left: 210px;
    height: 46px;
    line-height: 46px;
    text-align: center;
    color: #20A0FF;
    font-size: 20px;
  }

  #ARLlist .BTN .button_tree {
    margin-left: 2px;
    margin-right: 2px;
    padding-left: 2px;
    padding-right: 2px;
    width: 118px;
    text-align: center;;
  }

  #ARLlist .BTN .pi {
    padding-left: 13px;
    padding-right: 13px;
  }

  #Maplist {
    position: absolute;
    top: 11px;
    left: 5px;
    right: 0px;
    z-index: 1000;
    height: 100%;
    overflow: scroll;
  }

  #list {
    position: absolute;
    left: 1700px;
    width: 87.5%;
    right: -47px;
    top: 50px;
    bottom: 0;
    background: #fff;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, .3);
    z-index: 999;
  }

  .li {
    list-style: none;
    width: 100%;
    cursor: pointer;
    height: 40px;
    line-height: 39px;
    background-color: white;
    margin-left: 0;
    text-align: left;
    border-bottom: 1px solid #dfe6ec;
    min-width: 770px;
  }

  .li:hover {
    list-style: none;
    cursor: pointer;
    background-color: #EEF1F6;
    position: relative;
  }

  #ARLlist #treeMap .li .cb {
    float: left;
    left: 5px;
  }

  #ARLlist #treeMap .li .cy {
    float: left;
    display: block;
    width: 12.5%;

    border-right: 1px solid #dfe6ec;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .LTM {
    background-color: white;
  }

  .active {
    color: #42b983;
    font-weight: bold;
  }

  .Asa_i {
    position: absolute;
    z-index: 50;
    width: 130px;
    height: 40px;
    left: 25px
  }

  .msy {
    display: block;
    text-align: center;
    width: 75%;
    float: left;
    border-right: 1px solid #dfe6ec;
    height: 40px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .msg_msy {
    display: block;
    text-align: left;
    width: 95%;
    float: left;
    height: 40px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-left: 14px;
  }

  .cz {
    width: 12.5%;
    height: 40px;
    float: left;
    text-align: center;
    line-height: 40px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #42b983
  }

  .ul {
    overflow: hidden;
  }

  .fl {
    float: left;
  }

  .fr {
    float: right;
  }

  .input_search {
    float: left;
    margin-left: 10px;
    margin-top: -1.4px;
  }

  .ID {
    text-align: center;
    font-size: 15px;
    font-weight: bold;
    color: #1f2d3d
  }

  .first_li {
    border-top: 1px solid #dfe6ec;
    overflow-y: scroll
  }

  .msg_caoz {
    width: 20%;
    min-width: 210px;
    float: left;
  }

  .nav {
    width: 100%;
    height: 35px;
    line-height: 35px;
  }

  .el-icon-d-arrow-right {
    line-height: 35px;
    margin-left: 15px;
    font-weight: bold;
    font-size: 20px;
    cursor: pointer;
  }

  .el-icon-d-arrow-right:hover {
    color: #42b983
  }

  .center {
    display: block;
    margin: 0 auto;
    text-align: center;
    color: #42b983;
    font-size: 12px;
  }

  /*fenlichuqu*/
  .el-dialog__body {
    height: 730px;
  }

  .arl_table {
    overflow: hidden;
    height: 144px;
    margin-right: 20px;
    position: relative;
    width: 100%;
    border: 1px solid #dfe6ec;
  }

  .title_arl {
    font-weight: bold;
    height: 60px;
    line-height: 60px;
  }

  .title_arl span {
    cursor: pointer;
    margin-right: 30px;
  }

  .title_arl .fr:hover {
    color: #42b983;
  }

  .hu_sapn span {
    height: 30px;
    line-height: 30px;
    cursor: pointer;
    margin-right: 30px;
  }

  .hu_sapn .fr:hover {
    color: #42b983
  }

  .hutable {
    position: relative;
    width: 100%;
    border: 1px solid #dfe6ec;
  }

  .table_content {
    float: left;
    width: 245px;
    border-right: 1px solid #dfe6ec;
    height: 165px;
    font-size: 14px;
    background-color: white;
  }

  .table_title {
    height: 30px;
    line-height: 30px;
    font-weight: bold;
    text-align: center;
    background: #eef1f6;
    font-size: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .table_msg {
    margin: 5px;
    overflow: hidden;
    text-overflow: ellipsis;
    height: 125px;
  }

  .table_move {
    display: block;
    margin: 30% auto;
  }

  .dialog {
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, .3);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 2000;
  }

  .dialog_html {
    width: 80%;
    margin: 0 auto;
    height: 0px;
    margin-top: 100px;
    background: #fff;
    border-radius: 2px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, .3);
    padding: 10px 10px 10px 20px;
  }

  .dialog_title {
    width: 100%;
    height: 45px;
    line-height: 45px;
    margin-bottom: 30px;
  }

  .el-icon-close {
    line-height: 45px;
    cursor: pointer;
  }

  .el-icon-close:hover {
    color: #42b983
  }

  .content_scroll {
    overflow-y: scroll;
  }

  .option {
    display: block;
    width: 100%;
    line-height: 25px;
  }

  .tagltable {
    width: 100%;
    border: 1px solid #dfe6ec;
  }

  .tagl_table {
    width: 100%;
    border: 1px solid #dfe6ec;
  }

  .ana_table {
    width: 100%;
    border: 1px solid #dfe6ec;
  }

  .center_ {
    margin: 0;
    text-align: center;
    width: 100%;
  }

  .number_now {
    margin-right: 76px;
  }

  .user_name_title {
    margin: 0 auto;
    margin-left: 16px;

    height: 30px;
    line-height: 30px;
    font-weight: bold;
    font-size: 14px;
  }

  .msy > span {
    font-size: 13px;
  }

  .user_icon {
    width: 16px;
    vertical-align: middle;
  }
  .hutable,.tagltable,.tagl_table,.ana_table{
	height: 169px;
  }
</style>

