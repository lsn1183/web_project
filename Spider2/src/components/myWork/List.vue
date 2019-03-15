<template>
<div id="ARLlist">
	<div class="BTN">
		<div id="BTN_top">
			<div class="fl" style="margin-left:9px">
		        <font color="#42b983"><i class="el-icon-document" ></i></font>
				<el-select  class="button_tree" v-model="arr_v" @change="Summary_ARL">
					<el-option class="button_tree_option" v-for="item in arr"
					:key="item.value"
					:label="item.label"
					:value="item.value"
					>
					</el-option>
				</el-select>
			</div>
			<div class="input_search" style="margin-left:48px" @keyup.enter="List_search(input_value)">
				<el-input placeholder="请输入搜索ID" size="mini" v-model="input_value"  >
					<el-button slot="append" class="el-icon-search" @click="List_search(input_value)" ></el-button>
				</el-input>
			</div>
			<div class="change_time fr" v-if="change_time_flag">
				<el-select  class="button_tree" v-model="change_time_value" @change="change_time_fun(change_time_value)">
					<el-option class="button_tree_option" v-for="item in change_time"
					:key="item.value"
					:label="item.label"
					:value="item.value"
					>
					</el-option>
				</el-select>
				的票
			</div>
			<div class="change_time fr" v-if="change_status_flag">
				<el-select  class="button_tree" v-model="change_status_value" @change="change_status_fun(change_status_value)">
					<el-option class="button_tree_option" v-for="item in change_status"
					:key="item.value"
					:label="item.label"
					:value="item.value"
					>
					</el-option>
				</el-select>
				的票
			</div>
		</div>
	</div>
	<div id="treeMap"  class="fl" v-loading.lock="fullscreenLoading">
			<el-checkbox-group v-model="checkedC" @change="CheckedChange">
				<div style="margin: 0px 0;"></div>
				<ul id="ul">
					<li class="li first_li" v-show="arl_li">
						<span class="cy ID">ID</span>
						<span class="msy ID" style="width:61%">転記してきた要件</span>
						<span class="cy ID" style="width:7%;">
							<!--<span style="display:block;width:100%;height:100%;">指派给</span>-->
							<!-- <i class="el-icon-arrow-down" style="marginLeft:5%;color:#42b983"></i>  -->
							<el-dropdown trigger="click">
								<span @click="changeWho" style="display:block;width:100%;height:100%">指派给<i class="el-icon-arrow-down"
                                                                                      style="marginLeft:5%;color:#42b983"></i> </span>
								<el-dropdown-menu slot="dropdown">
									<el-dropdown-item v-for="(item,index) in names" :key="index">

										<span style="display:block;width:100%;height: auto;fontSize:12px;"
                    @click="changeOn(index)">{{item.user_name}}</span>
									</el-dropdown-item>
								</el-dropdown-menu>
							</el-dropdown>
						</span>
						<span class="cy ID" style="width:7%;">
							<span style="display:block;width:100%;height:100%;fontSize:13px;color:#42b983" v-show="hu_day" @click="target_date(1)">机能式样预定日
								<i class="el-icon-arrow-down"></i>
							</span>
							<span style="display:block;width:100%;height:100%;fontSize:13px;color:#42b983" v-show="tagl_day" @click="target_date(2)">要件定義预定日
								<i class="el-icon-arrow-down"></i>
							</span>
							<span style="display:block;width:100%;height:100%;fontSize:13px;color:#42b983" v-show="ana_day" @click="target_date(3)">要件分析预定日
								<i class="el-icon-arrow-down"></i>
							</span>
						</span>
						<span class="cz ID" >操作</span>
					</li>
					<li class="li first_li" v-show="hu_li">
						<span class="cy ID">ID</span>
						<span class="msy ID" style="width:61%">動作</span>
						<span class="cy ID" style="width:7%">
							<!--<span style="display:block;width:100%;height:100%;">指派给</span>-->
							<!-- <i class="el-icon-arrow-down" style="marginLeft:5%;color:#42b983"></i>  -->
							 <el-dropdown trigger="click" @command="search_user">
								<span @click="changeWho" style="display:block;width:100%;height:100%">指派给<i class="el-icon-arrow-down"
                                                                                      style="marginLeft:5%;color:#42b983"></i> </span>
								<el-dropdown-menu slot="dropdown">
									<el-dropdown-item v-for="(item,index) in names ":key="index">

										<span style="display:block;width:100%;height:100%;fontSize:12px"
                    @click="changeOn(index)">{{item.user_name}}</span>
									</el-dropdown-item>
								</el-dropdown-menu>
							</el-dropdown>
							</span>
						<span class="cy ID" style="width:7%">
							<span style="display:block;width:100%;height:100%;">任務状態</span>
							<!-- <el-dropdown trigger="click">
								<span style="display:block;width:100%;height:100%">任務状態<i class="el-icon-arrow-down" style="marginLeft:5%;color:#42b983"></i> </span>
								<el-dropdown-menu slot="dropdown">
									<el-dropdown-item v-for="(item,index) in job_status" :key="index">
										<span style="display:block;width:100%;height:100%;fontSize:12px" >{{item.label}}</span>
									</el-dropdown-item>
								</el-dropdown-menu>
							</el-dropdown> -->
						</span>
						<span class="cz ID" >操作</span>
					</li>
					<li class="li first_li" v-show="tagl_li">
						<span class="cy ID">ID</span>
						<span class="msy ID" style="width:61%">動作</span>
						<span class="cy ID" style="width:7%">
							<!--<span style="display:block;width:100%;height:100%;">指派给</span>-->
							<!-- <i class="el-icon-arrow-down" style="marginLeft:5%;color:#42b983"></i>  -->
							<el-dropdown trigger="click">
								<span @click="changeWho" style="display:block;width:100%;height:100%">指派给<i class="el-icon-arrow-down"
                                                                                      style="marginLeft:5%;color:#42b983"></i> </span>
								<el-dropdown-menu slot="dropdown">
									<el-dropdown-item v-for="(item,index) in names" :key="index">
										<span style="display:block;width:100%;height: auto;fontSize:12px;"
                    @click="changeOn(index)">{{item.user_name}}</span>
									</el-dropdown-item>
								</el-dropdown-menu>
							</el-dropdown>
						</span>
						<span class="cy ID" style="width:7%">
							<span style="display:block;width:100%;height:100%;">任務状態</span>
							<!-- <i class="el-icon-arrow-down" style="marginLeft:5%;color:#42b983"></i>  -->
							<!-- <el-dropdown trigger="click" @command="search_state">
								<span style="display:block;width:100%;height:100%">任務状態<i class="el-icon-arrow-down" style="marginLeft:5%;color:#42b983"></i> </span>
								<el-dropdown-menu slot="dropdown">
									<el-dropdown-item v-for="item in options">
										<span style="display:block;width:100%;height:100%;fontSize:12px">{{item.label}}</span>
									</el-dropdown-item>
								</el-dropdown-menu>
							</el-dropdown> -->
						</span>
						<!-- <span class="cy ID" style="width:7%">
							<span style="display:block;width:100%;height:100%;fontWeight:normal;fontSize:14px">完成时间</span>
						</span> -->
						<span class="cz ID" >操作</span>
					</li>
					<li class="li first_li" v-show="taglana_li">
						<span class="cy ID">ID</span>
						<span class="msy ID" style="width:61%">動作</span>
						<span class="cy ID" style="width:7%">
							<!--<span style="display:block;width:100%;height:100%;">指派给</span>-->
							<!-- <i class="el-icon-arrow-down" style="marginLeft:5%;color:#42b983"></i>  -->
						<el-dropdown trigger="click">
								<span @click="changeWho" style="display:block;width:100%;height:100%">指派给<i class="el-icon-arrow-down"
                                                                                      style="marginLeft:5%;color:#42b983"></i> </span>
								<el-dropdown-menu slot="dropdown">

									<el-dropdown-item v-for="(item,index) in names" :key="index">
										<span style="display:block;width:100%;height: auto;fontSize:12px;"
                    @click="changeOn(index)">{{item.user_name}}</span>
									</el-dropdown-item>
								</el-dropdown-menu>
							</el-dropdown>
						</span>
						<span class="cy ID" style="width:7%">
							<span style="display:block;width:100%;height:100%;">任務状態</span>
							<!-- <i class="el-icon-arrow-down" style="marginLeft:5%;color:#42b983"></i>  -->
							<!-- <el-dropdown trigger="click" @command="search_state">
								<span style="display:block;width:100%;height:100%">任務状態<i class="el-icon-arrow-down" style="marginLeft:5%;color:#42b983"></i> </span>
								<el-dropdown-menu slot="dropdown">
									<el-dropdown-item v-for="item in options">
										<span style="display:block;width:100%;height:100%;fontSize:12px">{{item.label}}</span>
									</el-dropdown-item>
								</el-dropdown-menu>
							</el-dropdown> -->
						</span>
						<span class="cz ID" >操作</span>
					</li>

					<li class="li_scroll">
						<ul class="ul_scroll">
							<li class="li"  v-for="(item,index) in table1" @click.stop='change1(item.arl_id,index)' v-if="arl_li" :key="index">
								<el-checkbox class="cb" :label="item.title" :key="item.title" :value="item.arl_id" v-show="cx">
								</el-checkbox>
								<i class="Asa_i"  :title="item.title"></i>
								<span class="cy span_width" v-show="cy" @click.stop='change1(item.arl_id,index)' :class="{'active':num == index}"  :title="item.title">
									<span style="marginLeft:42px">{{item.title}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info"  style="width:61%">
									<span class="msg_msy ">{{item.from_info}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" :title="item.user_name">{{item.user_name}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" :title="item.hu_date" v-show="hu_day">{{item.hu_date}}</span>
									<span style="display:block;width:100%;height:100%;" :title="item.def_date" v-show="tagl_day">{{item.def_date}}</span>
									<span style="display:block;width:100%;height:100%;" :title="item.analysis_date" v-show="ana_day">{{item.analysis_date}}</span>
								</span>
								<span class="cz cen" v-show="cy" @click="amint(item.arl_id,index)"><i class="el-icon-d-arrow-left"> 详细</i></span>
							</li>
							<li class="li"  v-for="(item,index) in table1" @click.stop='change1(item.arl_id,index)' v-if="hu_li" :key="index">
								<el-checkbox class="cb" :label="item.title" :key="item.title" :value="item.arl_id" v-show="cx">
								</el-checkbox>
								<i class="Asa_i"  :title="item.title"></i>
								<span class="cy span_width" v-show="cy" @click.stop='change1(item.arl_id,index)' :class="{'active':num == index}" :title="item.title">
									<span style="marginLeft:36px" >{{item.title}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info" style="width:61%">
									<span class="msg_msy " :title="item.sequence_list">{{item.sequence_list}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" :title="item.user_name">{{item.user_name}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" :title="item.job_status_name">{{item.job_status_name}}</span>
								</span>
								<span class="cz" v-show="cy" @click="amint(item.arl_id,index)"><i class="el-icon-d-arrow-left"> 详细</i></span>
							</li>
							<li class="li"  v-for="(item,index) in table1" @click.stop='change1(item.arl_id,index)' v-if="tagl_li" :key="index">
								<el-checkbox class="cb" :label="item.title" :key="item.title" :value="item.arl_id" v-show="cx">
								</el-checkbox>
								<i class="Asa_i"  :title="item.title"></i>
								<span class="cy span_width" v-show="cy" @click.stop='change1(item.arl_id,index)' :class="{'active':num == index}"  :title="item.title">
									<span style="marginLeft:14px">{{item.title}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info" style="width:61%">
									<span class="msg_msy " :title="item.sequence_list">{{item.sequence_list}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" :title="item.user_name">{{item.user_name}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" :title="item.job_status_name">{{item.job_status_name}}</span>
								</span>
								<span class="cz" v-show="cy" @click="amint(item.arl_id,index)"><i class="el-icon-d-arrow-left"> 详细</i></span>
							</li>
							<li class="li"  v-for="(item,index) in table1" @click.stop='change1(item.arl_id,index)' v-if="taglana_li" :key="index">
								<el-checkbox class="cb" :label="item.title" :key="item.title" :value="item.arl_id" v-show="cx">
								</el-checkbox>
								<i class="Asa_i"  :title="item.title"></i>
								<span class="cy span_width" v-show="cy" @click.stop='change1(item.arl_id,index)' :class="{'active':num == index}"  :title="item.title">
									<span style="marginLeft:14px">{{item.title}}</span>
								</span>
								<span class="msy" v-show="cy" :title="item.from_info" style="width:61%">
									<span class="msg_msy " :title="item.sequence_list">{{item.sequence_list}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" >{{item.user_name}}</span>
								</span>
								<span class="msy" style="width:7%">
									<span style="display:block;width:100%;height:100%;" :title="item.job_status_name">{{item.job_status_name}}</span>
								</span>
								<span class="cz" v-show="cy" @click="amint(item.arl_id,index)"><i class="el-icon-d-arrow-left"> 详细</i></span>
							</li>
						</ul>
					</li>
				</ul>
			</el-checkbox-group>

	</div>
	<div id="list" v-show="show_flag">
	 	<div>
		    <div v-show="Maptree" id="Maptree"></div>
		    <div v-if="Maplist" id="Maplist">
		    	<div class="nav">
		    		<i class="el-icon-d-arrow-right fl" style="marginRight:5px" @click="back_up()"></i>
		    	</div>
		    	<el-collapse  accordion>
			    	<div class="user_name_title">
			    		<span><img src="../../assets/img/Icon/user_icon_2.png" class="user_icon"/> {{userNames}}</span>
			    	</div>
		    	</el-collapse>
			    <el-collapse  accordion v-for="(table_msg,arl_index) in tabledata1" :key="arl_index">
					<el-collapse-item  :title="table_msg.title">
						<div class="arl_table">
							<div class='table_content' style="width:9%">
								<p class="table_title">
									<span>式样ID</span>
								</p>
								<p class="table_msg" >
									{{table_msg.arl_id}}
								</p>
							</div>
							<div class='table_content' style="width:24%">
								<p class="table_title">
									<span>転記してきた要件</span>
								</p>
								<p class="table_msg" :title="table_msg.req_post">
									<span>{{table_msg.req_post}}</span>
								</p>
							</div>
							<div class='table_content' style="width:10%">
								<p class="table_title">
									<span>状態</span>
								</p>
								<p class="table_msg" :title="table_msg.status">
									<span>{{table_msg.status}}</span>
								</p>
							</div>
							<div class='table_content' style="width:24%">
								<p class="table_title">
									<span>トリガー</span>
								</p>
								<p class="table_msg" :title="table_msg.trigger">
									<span>{{table_msg.trigger}}</span>
								</p>
							</div>
							<div class='table_content' style="width:23%">
								<p class="table_title">
									<span>動作</span>
								</p>
								<p class="table_msg" :title='table_msg.action'>
									<span>{{table_msg.action}}</span>
								</p>
							</div>
							<div class='table_content last' style="width:10%;" >
								<p class="table_title">
									<span>操作</span>
								</p>
								<p class="table_msg" title="">
									<el-button type="text" class="table_move" @click="editClick()"><i class="el-icon-edit"> 更新</i></el-button>
								</p>
							</div>
						</div>
			 	       <!-- HU要件定義 -->
						<el-collapse  accordion v-for="(hu_record,hu_index) in table_msg.hu_list" :key="hu_index">
						  	<el-collapse-item  :title="hu_record.title" :key="hu_record.title" :name="hu_record.hu_id">
								<div id="hu_table">
									<!-- 只显示重要的信息 ，同理arl-->
									<div class="hutable">
										<div class='table_content' style="width:8%">
											<!--   -->
											<p class="table_title">
												<span>ユニークID</span>
											</p>
											<p class="table_msg " :title="hu_record.unique_id" style="textAlign:center">
											     {{hu_record.unique_id}}
											</p>
										</div>
										<!--<div class='table_content' style="width:20%">
											<p class="table_title">
												<span>オプション項目</span>
											</p>-->
											<!-- 6个option  如果option是默认选项则只显示システム構成 -->
											<!--<p class="table_msg content_scroll" title="">
												<span class="option" style="fontWeight:bold">AMP:
													<span style="fontWeight:normal">{{hu_record.amp}}</span>
												</span>
												<span class="option" style="fontWeight:bold">DSRC:
													<span style="fontWeight:normal">{{hu_record.dsrc}}</span>
												</span>
												<span class="option" style="fontWeight:bold">DCM:
													<span style="fontWeight:normal">{{hu_record.dcm}}</span>
												</span>
												<span class="option" style="fontWeight:bold">RSE:
													<span style="fontWeight:normal">{{hu_record.rse}}</span>
												</span>
												<span class="option" style="fontWeight:bold">TouchPad:
													<span style="fontWeight:normal">{{hu_record.touch_pad}}</span>
												</span>
												<span class="option" style="fontWeight:bold">SeparateDisp:
													<span style="fontWeight:normal">{{hu_record.separate_disp}}</span>
												</span>
												<span class="option" style="fontWeight:bold">システム構成:
													<span style="fontWeight:normal">{{hu_record.system_conf}}</span>
												</span>
											</p>
										</div>-->
										<!--<div class='table_content' style="width:22%">
											<p class="table_title">
												<span>関連基本要件</span>
											</p>
											<p class="table_msg content_scroll" :title="hu_record.rel_requirement">
											    <span>{{hu_record.rel_requirement}}</span>
											</p>
										</div>-->
										<div class='table_content' style="width:51.5% ">
											<p class="table_title">
												<span>責務分担</span>
											</p>
											<div class="table_msg content_scroll">
												<p title=""  v-for="(sequence_record, sequence_index) in hu_record.sequence_list" :key="sequence_index">
													<span class="option" style="fontWeight:bold">({{sequence_index+1}}) <br>設備:

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
												</p>
											</div>
										</div>
										<div class='table_content' style="width:24.5%">
											<p class="table_title">
												<span>变更理由与日期</span>
											</p>
											<div class="table_msg content_scroll" title="hu_record.reason">
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
												<el-button  type="text" @click="editClick1(hu_record.hu_id,hu_index)"  class="table_move"><i class="el-icon-edit"> 更新</i></el-button>
											</p>
										</div>
									</div>
								</div>
								<!--TAGL要件定義-->
								<el-collapse  accordion v-for="(definition_record,definition_index) in hu_record.definition_list" :key="definition_index">
								  	<el-collapse-item  :title="definition_record.title"  :key="definition_record.title" :name="definition_record.definition_id">
										<div id="tagl_table" >
											<div class="tagl_table" >
												<div class='table_content' style="width:7%">
													<p class="table_title">
														<span>ユニークID</span>
													</p>
													<p class="table_msg " title="" style="textAlign:center">
													     {{definition_record.unique_id}}
													</p>
												</div>
												<div class='table_content' style="width:53%">
													<p class="table_title">
														<span>責務分担</span>
													</p>
													<p class="table_msg content_scroll" title="" >
														<span v-for="(sequence_record, sequence_index) in definition_record.sequence_list">
															<span class="option" style="fontWeight:bold">({{sequence_index+1}}) <br>設備:
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
													<p class="table_title">
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
														<el-button type="text" class="table_move" @click="editClick2(hu_id,definition_record.definition_id,hu_index,definition_index)"><i class="el-icon-edit"> 更新</i></el-button>
													</p>
												</div>
											</div>
										</div>
								  		<!-- TAGL要件分析 -->
										<el-collapse  accordion  v-for="(taglana_record,taglana_index) in definition_record.analysis_list" :key="taglana_index">
											<el-collapse-item  :title="taglana_record.title" :key="taglana_record.title"  :name="taglana_record.analysis_id" >
												<div id="taglana_table">
													<div class="ana_table" >
														<div class='table_content' style="width:6%">
															<p class="table_title">
																<span>ユニークID</span>
															</p>
															<p class="table_msg" title="" style="textAlign:center">
															   {{taglana_record.unique_id}}
															</p>
														</div>
														<div class='table_content' style="width:54.5%">
															<p class="table_title">
																<span>TAGL-PF</span>
															</p>
															<p class="table_msg content_scroll ">
																<span v-for="(analist_record, analist_index) in taglana_record.sequence_list">
				 					    	     					<span class="option" style="fontWeight:bold">({{analist_index+1}})</br>設備:
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
																<el-button type="text" class="table_move" @click="editClick3(hu_record.hu_id,definition_record.definition_id,hu_index,definition_index,taglana_index)"><i class="el-icon-edit"> 更新</i></el-button>
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
			        </el-collapse-item>
			    </el-collapse>
			</div>
		</div>
		<el-dialog title="转交ARL责任人" :visible.sync="dialogFormVisible" :modal-append-to-body="false">
			<el-form :model="form">
				<el-form-item label="请先选择组" :label-width="formLabelWidth">
					<el-select v-model="form.group_id" placeholder="请选择组" @change="choose()">
						<el-option
						v-for="item in groups"
						:key="item.group_id"
						:label="item.group_name"
						:value="item.group_id">
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="再选择责任人" :label-width="formLabelWidth">
					<el-select v-model="form.user_id" placeholder="请选择责任人" >
						<el-option
						v-for="item in members"
						:key="item.user_id"
						:label="item.user_name"
						:value="item.user_id">
						</el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="dialogFormVisible = false">取 消</el-button>
				<el-button type="primary" @click="Tf">确 定</el-button>
			</div>
		</el-dialog>
		<el-dialog title="本HU的Log信息" :visible.sync="HU_log" :modal-append-to-body="false" small="80%">
			<el-form>
				<el-table :data="HU_loglist" border style="width: 100%">
					<el-table-column prop="user_name" label="操作人" width="100" >
					</el-table-column>
					<el-table-column prop="group_name" label="组名" width="100" >
					</el-table-column>
					<el-table-column prop="commit_time" label="时间" width="200">
					</el-table-column>
					<el-table-column label="修改了" >
					<el-table-column prop="column_info" label="0" >
					</el-table-column>
					</el-table-column>
				</el-table>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="HU_log = false">取 消</el-button>
				<el-button type="primary" @click="HU_log = false">确 定</el-button>
			</div>
		</el-dialog>
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
				<!--指派给  分页组件-->
				<el-pagination
				id="names_page"
				v-if="names_flag == true"
				@current-change="namesPageChange"
				:current-page="page"
				:page-size="page_size"
				layout="total, prev, pager, next,jumper"
				:total="changdu"
				></el-pagination>
			</div>

		</div>
	</div>
	<div class="right_menu"  id="rightMenu" v-show="right_flag">
		<el-button @click='TARLs' class="rightmenu_first">批量转</el-button>
	</div>
	<arl_dialog  @dialog_close = "arl_dialog_return" @dialog_vue_close = "change1(change_params_id,change_params_index)" v-bind:input_show='HU_flag'  v-bind:input_arl_id="select_arl_id" v-bind:input_hu_id="select_hu_id">
	</arl_dialog>
</div>
</template>

<script >
import dialog from './dialog.vue'
require('../../assets/js/jquery-1.8.3.min.js')
export default{
components:{
	arl_dialog:dialog
},
data(){
	return {
		change_params_id: '',
		change_params_index: '',
		change_status_flag:false,
		change_time:[
			{"label":"最近三天","value":"3"},
			{"label":"最近一周","value":"7"},
			{"label":"最近一月","value":"30"},
			{"label":"未完成","value":"incomplete"},
			{"label":"已完成","value":"complete"},
			{"label":"作業完了","value":"work_complete"},
			{"label":"被指摘","value":"point"},
		],
		hu_day:true,
		tagl_day:false,
		ana_day:false,
    change_time_value:"",
    change_status_value:"",
		change_status:[
			{"label":"未完成","value":"incomplete"},
			{"label":"作業完了","value":"work_complete"},
			{"label":"已完成","value":"complete"},
			{"label":"所有","value":""},
			{"label":"被指摘","value":"point"}
		],
		fullscreenLoading:false,
		arl_li:false,
		hu_li:false,
		tagl_li:false,
		taglana_li:false,
		select_full_arl_id : "",
		select_arl_id : "",
		select_hu_id : "",
		select_definition_id:'',
		select_type:'arl',
		json:{
			user_id: '',
			type:'',
			category_id:'',
			condition:{}
		},
		input_value:'',
		x:0,
		msg:"更多",
		arlflag:false,
		HU_flag:false,
		DEF_flag:false,
		list_flag: true,
		map_flag:true,
		BTN_type:1,
		num: 0,
		noData:'',
		show_flag:false,
		search_flag:false,
		names_flag:false,
		page:1,
		page_size:200,
		changdu:0,
		tabledata1: [],
		tabledata2: [],
		tabledata3: [],
		tabledata4: [],
		table1:[],
		table2:[],
		table3:[],
		table4:[],
		arl_id:'',
		hu_id:'',
		arl_record_id:0,
		hu_record_id:0,
		def_record_id:0,
		cate_id:window.sessionStorage.getItem('b'),
		change_time_flag:false,
		Maptree:false,
		Maplist:false,
		Map:false,
		data:'',
		s_arl:'',
		s_hu:'',
		arr:[
		{value:"arl",label:"要求式样"},
		{value:"hu",label:"机能式样"},
		{value:"tagl_def",label:"要件定義"},
		{value:"tagl_ana",label:"要件分析"}],
		arr_v:"arl",
		job_status:[
			{"label":"初始狀態，待作業","value":"1"},
			{"label":"作業完了，待确认","value":"2"},
			{"label":"确认完了","value":"3"},
		],
		titles:[],
		checkAll:true,
		checkedC:[],
		cx:false,
		cy:true,
		isIndeterminate:false,
		Maptree:{},
		members:[],
		groups:[],
		info:'',
		dialogFormVisible: false,
        HU_log:false,
        	HU_loglist:[],
        form: {
          arl:[],
          user_id:'',
          group_id:'',
        },
        formLabelWidth: '120px',
        Id:0,
        nodes :[],
		links :[],
		ndata:[],
		right_flag:this.right_menu_flag,
		ARLdata:[],
		user_names:[],
		userNames:"",
		complete_time:"",
		names: [],
		who_id: null,
		table10: [],
		complete_value:""
	}
},

mounted(){
	this.change1(window.sessionStorage.getItem('ARLId'))
	this.Id = Number(window.sessionStorage.getItem('admin'));
	this.$axios.get(this.Ip+"/AllUsers")
	.then(res=>{
		this.user_names = res.data.content;
	})
	this.Summary_ARL()
},
computed: {
	getUserIcons(){
		return this.$store.state.user_data
	}
},
watch: {
	getUserIcons(val){
		window.sessionStorage.setItem('b',val)
		this.cate_id = window.sessionStorage.getItem('b');
		this.num = -1
		this.Summary_ARL()
	}
},
methods:{
	search_user(command){
		this.List_search();
	},
	search_state(command){
		this.List_search();
	},
	arl_dialog_return(params){
		this.HU_flag = params[0];
	},
	hu_dialog_return(params){
		this.DEF_flag = params[0];
	},
	search_axios(user_id,group_id,size,page){
		if(this.BTN_type =="arl"){
			this.json.like_condition = {}
			this.json.like_condition.arl_id = this.input_value
		}else if(this.BTN_type =="hu"){
			this.json.like_condition = {}
			this.json.like_condition.hu_id = this.input_value
		}else if(this.BTN_type =="tagl_def"){
			this.json.like_condition = {}
			this.json.like_condition.definition_id = this.input_value
		}else{
			this.json.like_condition = {}
			this.json.like_condition.analysis_id = this.input_value
		}
		this.json.condition.user_id = user_id
		this.json.condition.group_id = group_id;
		this.json.type = this.BTN_type;
		this.json.size = size;
		this.json.page = page;
		this.$axios.post(this.Ip+'/SummaryAll',this.json)
			.then(res => {
				if(res.data.result=="OK"){
					this.table1 = res.data.content
					this.changdu = res.data.total_count
					this.fullscreenLoading = false;
				}else{
					this.table1 = []
					this.changdu = 0
					this.fullscreenLoading = false;
				}
			})
	},
	List_search(){
		this.list_flag = false;
		this.search_flag = true;
		this.names_flag = false;
		this.fullscreenLoading = true;
		if(window.sessionStorage.getItem('workType')=="my"){
			this.search_axios(this.Id,0,200,1)
		}else if(window.sessionStorage.getItem('workType')=="group"){
			this.search_axios(0,window.sessionStorage.getItem('groups_id'),200,1)
		}else{
			this.search_axios(0,0,200,1)
		}
	},
	Summary_axios(type,user_id,group_id,job_status,category_id,like_condition,size,page,start_date,end_date,complete){
		var name ='';
		var title=[];
		if(this.BTN_type=="arl"){
			this.arl_li=true;
			this.hu_li=false;
			this.tagl_li=false;
			this.taglana_li=false;
		}else if(this.BTN_type=="hu"){
			this.arl_li=false;
			this.hu_li=true;
			this.tagl_li=false;
			this.taglana_li=false;
		}else if(this.BTN_type=="tagl_def"){
			this.arl_li=false;
			this.hu_li=false;
			this.tagl_li=true;
			this.taglana_li=false;
		}else{
			this.arl_li=false;
			this.hu_li=false;
			this.tagl_li=false;
			this.taglana_li=true;
		}
		this.$axios.post(this.Ip+'/SummaryAll',{"type":type,"condition":{"user_id":user_id,"group_id":group_id,"job_status":job_status,"category_id":category_id,"complete":complete,"start_date":start_date,"end_date":end_date},"like_condition":{},"size":size,"page":page}).then(res=>{
				this.table1=[]
				this.table1=res.data.content;
				this.changdu = res.data.total_count;
			}).catch(res=>{
					this.table1=[]
					this.changdu = 0;
				})
	},
	Summary_Users() {
		this.$axios.post(this.Ip + '/SummaryUsers', {
			  "type": this.BTN_type,
			  "condition": {"user_id": "", "group_id": "", "job_status": "", "category_id": this.cate_id},
			  "like_condition": {},
			  "size": 20,
			  "page": 1,
			  "start_date": "",
			  "end_date": ""
		}).then(res => {
			  this.table10 = [];
			  this.table10 = res.data.content;
			}).catch(res => {
			  this.table10 = [];
		})
	},
	names_axios(type,user_id,group_id,job_status,category_id,like_condition,size,page,start_date,end_date,complete){
		this.list_flag = false;
		this.search_flag = false;
		this.names_flag = true;

		this.$axios.post(this.Ip+'/SummaryAll',{"type":type,"condition":{"user_id":user_id,"group_id":group_id,"job_status":job_status,"category_id":category_id,"complete":complete,"start_date":start_date,"end_date":end_date},"like_condition":{},"size":size,"page":page}).then(res=>{
				if(res.data.result=="OK"){
					this.table1=[]
					this.table1=res.data.content;
					this.changdu = res.data.total_count;
				}else{
					this.table1 = []
					this.changdu = 0
				}
			}).catch(res=>{
					this.table1=[]
					this.changdu = 0;
			})
	},
	Summary_ARL(start_date,end_date,complete){
		this.search_flag = false;
		this.list_flag = true;
		this.names_flag = false;
		this.noData ='';
		this.page = 1;
		this.BTN_type = this.arr_v;
		this.Summary_Users();
		if(window.sessionStorage.getItem('workType')=="my"){
			this.change_time_flag = window.sessionStorage.getItem('change_time_flag')
			this.change_status_flag = false
			this.Summary_axios(this.BTN_type,this.Id,0,"",this.cate_id,"",200,1,start_date,end_date,complete)

		}else if(window.sessionStorage.getItem('workType')=="group"){
			this.change_time_flag = false
			this.change_status_flag = window.sessionStorage.getItem('change_status_flag')
			this.Summary_axios(this.BTN_type,0,window.sessionStorage.getItem('groups_id'),"",this.cate_id,"",200,1,"","",complete)

		}else{
			this.change_time_flag = false
			this.change_status_flag = window.sessionStorage.getItem('change_status_flag')
			this.Summary_axios(this.BTN_type,0,0,"",this.cate_id,"",200,1,"","",complete)

		}
	},
	listPageChange(val){
		var user_id = "";
		var group_id = "";
		var job_status = "";
		var complete = ""
		this.BTN_type = this.arr_v;
		if(window.sessionStorage.getItem('workType')=="my"){
			this.Summary_axios(this.BTN_type,this.Id,group_id,job_status,this.cate_id,"",200,val,"","",this.complete_time)

		}else if(window.sessionStorage.getItem('workType')=="group"){
			this.Summary_axios(this.BTN_type,user_id,window.sessionStorage.getItem('groups_id'),job_status,this.cate_id,"",200,val,"","",this.complete_value)

		}else{
			this.Summary_axios(this.BTN_type,user_id,group_id,job_status,this.cate_id,"",200,val,"","",this.complete_value)
		}
	},
	searchPageChange(val){
		var user_id = "";
		var group_id = "";
		this.BTN_type = this.arr_v;
		this.page = val;
		if(window.sessionStorage.getItem('workType')=="my"){
			this.search_axios(this.Id,0,200,this.page)
		}else if(window.sessionStorage.getItem('workType')=="group"){
			this.search_axios(0,window.sessionStorage.getItem('groups_id'),200,this.page)
		}else{
			this.search_axios(0,0,200,this.page)
		}
	},
	namesPageChange(val){
		var group_id = "";
		var job_status = "";
		var like_condition = "";
		this.page = val;
		var start_date = "";
		var end_date = "";
		var complete = "";
		this.names_axios(this.BTN_type,this.who_id, "", "", this.cate_id, "", 200, this.page, "", "","");
	},
	showbox(){
		if(this.cx!=false){
			this.cx = false;
			this.cy = true;
		}else{
			this.cx = true;
			this.cy = false;
		}
	},
	Allcheck(event){
		this.checkedC = event.target.checked ? this.titles : [];
		this.isIndeterminate = false ;
	},
	CheckedChange(value){
		let checkedCount = value.length;
		this.checkAll = checkedCount === this.table1.length;
		this.isIndeterminate = checkedCount > 0 && checkedCount < this.table1.length;
	},
	TARL(index){
		this.form.arl[0]=this.tabledata1[index].arl_id;
		this.dialogFormVisible=true;
		this.$axios.get(this.Ip+"/GroupAllGroups")
		.then(res=>{
			this.groups = res.data.content;
		})
	},
	Tf(){
		if(this.form.arl.length!=0){
			this.$axios.post(this.Ip+"/ARLAssignUser",this.form)
			.then(res=>{
				this.$alert("转出成功")
			})
			.catch(res=>{
				this.$alert("转出失败")
			})
			this.dialogFormVisible=false;
		}else{
			this.$notify({
				message:"请返回勾选需要转交的项目"
			})
		}
	},
	choose(){
		var g_id = this.form.group_id;
		var name ={};
		var members=[];
		if(g_id!=""){
			this.$axios.get(this.Ip+"/GroupMembers/"+g_id)
			.then(res=>{
				this.info = res.data.content;
				for(var i = 0;i<this.info.length;i++){
					if(this.info.length!=0){
						name = {}
						name.user_id = this.info[i].user_id
						name.user_name = this.info[i].user_name
						members.push(name)
						this.members = members
					}else{
						this.members = members
					}
				}
			})
		}
	},
	TARLs(){
		this.form.arl = this.checkedC
		this.dialogFormVisible=true;
		this.$axios.get(this.Ip+"/GroupAllGroups")
		.then(res=>{
			this.groups = res.data.content;
		})
	},
	change1:function(arl_id,index){
		this.change_params_id = arl_id
		this.change_params_index = index
		if(arl_id!=""){
			this.select_arl_id = arl_id;
			this.select_full_arl_id = "ARL: " + arl_id;
			this.arl_id = arl_id;
		}
		this.num = index;
		var self=this;
		this.Map=false
		this.Maplist=true;
		this.Maptree=false;
		this.right_menu_flag=false;
		this.right_flag=false;
		this.list_flag=true;
		this.map_flag=true;
		if(arl_id!=""){
			this.$axios.get(this.Ip+'/ArlTreeInfo/'+this.arl_id+'/'+window.sessionStorage.getItem('admin')+'/'+1)
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
					if(this.tabledata1!=""&&this.tabledata1[0].hu_list!=0){
						for(var k = 0;k<this.tabledata1[0].hu_list.length;k++){
							this.tabledata1[0].hu_list[k].job_status_name=""

							if(this.tabledata1[0].hu_list[k].job_status == 1){

								this.tabledata1[0].hu_list[k].job_status_name ="初始狀態，待作業"

							}else if(this.tabledata1[0].hu_list[k].job_status == 2){

								this.tabledata1[0].hu_list[k].job_status_name ="作業完了，待确认"

							}else if(this.tabledata1[0].hu_list[k].job_status == 3){

								this.tabledata1[0].hu_list[k].job_status_name ="确认完了"

							}


							for(var z = 0;z<this.tabledata1[0].hu_list[k].definition_list.length;z++){

								this.tabledata1[0].hu_list[k].definition_list[z].job_status_name=""

								if(this.tabledata1[0].hu_list[k].definition_list[z].job_status == 1){

									this.tabledata1[0].hu_list[k].definition_list[z].job_status_name ="初始狀態，待作業"

								}else if(this.tabledata1[0].hu_list[k].definition_list[z].job_status == 2){

									this.tabledata1[0].hu_list[k].definition_list[z].job_status_name ="作業完了，待确认"

								}else if(this.tabledata1[0].hu_list[k].definition_list[z].job_status == 3){

									this.tabledata1[0].hu_list[k].definition_list[z].job_status_name ="确认完了"

								}


								for(var j = 0;j< this.tabledata1[0].hu_list[k].definition_list[z].analysis_list.length;j++){
									this.tabledata1[0].hu_list[k].definition_list[z].analysis_list[j].job_status_name=""

									if(this.tabledata1[0].hu_list[k].definition_list[z].analysis_list[j].job_status == 1){

										this.tabledata1[0].hu_list[k].definition_list[z].analysis_list[j].job_status_name ="初始狀態，待作業"

									}else if(this.tabledata1[0].hu_list[k].definition_list[z].analysis_list[j].job_status == 2){

										this.tabledata1[0].hu_list[k].definition_list[z].analysis_list[j].job_status_name ="作業完了，待确认"

									}else if(this.tabledata1[0].hu_list[k].definition_list[z].analysis_list[j].job_status == 3){

										this.tabledata1[0].hu_list[k].definition_list[z].analysis_list[j].job_status_name="确认完了"

									}


								}
							}
						}
					}
				})
		}
	},
	editClick(){
		this.HU_flag = true;
		$(".dialog_html").animate({height:785},800,function(){
			$(".arltable").eq(0).css({display:"block"})
		})
	},
	editClick1(hu_id,hu_index){
		this.select_hu_id = hu_id;
		this.HU_flag = true;
		var this_ = this;
		$(".dialog_html").animate({height:785},800,function(){
			$(".arltable").eq(0).css({display:"block"})
			$(".hu_table").eq(hu_index).css({display:"block"})
		})
	},
	editClick2(hu_id,definition_id,hu_index,def_index){
		this.select_definition_id = hu_id;
		this.HU_flag = true;
		var this_ = this;
		$(".dialog_html").animate({height:785},800,function(){
			$(".hu_table").eq(hu_index).css({display:"block"})
			$(".hu_div").eq(hu_index).children(".tagl_div").children(".tagltable").eq(def_index).css({display:"block"})
		})
	},
	editClick3(hu_id,definition_id,hu_index,def_index,taglana_index){
		this.select_definition_id = hu_id;
		this.HU_flag = true;
		var this_ = this;
		$(".dialog_html").animate({height:785},800,function(){
			$(".hu_div").eq(hu_index).children(".tagl_div").children(".tagltable").eq(def_index).css({display:"block"})
			$(".hu_div").eq(hu_index).children(".tagl_div").eq(def_index).children(".taglana_div").eq(taglana_index).children(".taglana_table").eq(0).css({display:"block"})
		})
	},
	HUlog(index){
		this.HU_log=true;
		//CommitLogByClassifyAndRecord+type+record_id
		this.$axios.get(this.Ip+"/CommitLogByClassifyAndRecord/"+0+"/"+50111)
		.then(res=>{
			this.HU_loglist = res.data.content
		})
		.catch(res=>{
		})
	},
	check(index) {
		this.data = this.tabledata1[index].arl_id
		this.$router.push({name: 'ARL_all',params:{ARL_id: this.data}})
	},
	toMap(){
		this.list_flag = false
		this.map_flag = false
		this.Maptree=true;
		this.Maplist=false;
	},
	toList(){
		this.list_flag = true
		this.map_flag = true
		this.Maplist=true;
		this.Maptree=false;
	},
	key_down(event,input_value){
		if(event.keyCode == 13){
			this.List_search(input_value);
		}
	},
	right_menu(){
			var rightMenu=document.getElementById("rightMenu")
			var event = event||window.event;
			if(event.stopPropagation()){
				event.stopPropagation();
			}else if(event.cancelBubble){
				event.preventDefault();
			}else{
				return false;
			}
			if(rightMenu!=null){
				rightMenu.style.top = event.clientY-60+"px"
				rightMenu.style.left = event.clientX-300+"px"
				this.right_flag=true
			}
	},
	amint(arl_id){
		this.show_flag = true;
		var span_width = $(".span_width").width()
		$("#list").animate({left:span_width},1000)
	},
	back_up(){
		var this_=this;
		$("#list").animate({left:2000},1000,function(){
			this_.show_flag = false
		})
	},
	change_time_fun(time){
		var complete = time
		this.complete_time=""
		var formatDate = function(date){
			var y = date.getFullYear();
			var m = date.getMonth()+1;
			m = m< 10 ? '0' + m : m;
			var d = date.getDate();
			d = d <10 ? ('0'+d) : d;
			return y + '-' + m + '-' + d;
		}
		if(time == 3){
			this.complete_time = ""
			const end = new Date();
			const start = new Date();
			start.setTime(start.getTime() - 3600 * 1000 * 24 * 3);
			var start_time = formatDate(start)
			var end_time  = formatDate(end)
			this.Summary_ARL(start_time,end_time)
		}else if(time == 7){
			const end = new Date();
			const start = new Date();
			start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
			var start_time = formatDate(start)
			var end_time  = formatDate(end)
			this.Summary_ARL(start_time,end_time)
		}else if(time == 30){
			const end = new Date();
			const start = new Date();
			start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
			var start_time = formatDate(start)
			var end_time  = formatDate(end)
			this.Summary_ARL(start_time,end_time)
		}else{
			this.complete_time = time
			this.Summary_ARL("","",this.complete_time)
		}
	},
	target_date(type){
		if(type==1){
			this.hu_day = false;
			this.tagl_day = true
			this.ana_day = false
		}else if(type==2){
			this.hu_day = false;
			this.tagl_day = false
			this.ana_day = true
		}else{
			this.hu_day = true;
			this.tagl_day = false
			this.ana_day = false
		}
	},  	
	changeWho() {
    	this.names = this.table10
    },
  	changeOn(index) {
    	this.who_id = this.names[index].user_id;
		this.names_axios(this.BTN_type,this.who_id, "", "", this.cate_id, "", 200, 1, "", "",this.complete_value);
  	},
  	change_status_fun(change_status_value){
  		this.complete_value = change_status_value
  		this.Summary_ARL("","",change_status_value)
  	}
  }
}
</script>

<style scoped>
.el-dialog--small{
width: 80%;
}
#ARLlist{
position: relative;
height: 100%;
width: 100%;
overflow:hidden;
font-family: "微软雅黑";
font-size: 14px;
top:10px;
}
#treeMap{
position: absolute;
top:49px;
bottom: 49px;
left: 0;
width: 100%;
text-align: center;
font-size: 14px;
background: #fff;
}
.li_scroll{
list-style:none;
}
.ul_scroll{
width: 100%;
overflow-y:scroll;
height:770px;
overflow-x: hidden;
}
#foot{
position: absolute;
bottom: 0;
left: 0;
width: 100%;
height:50px;
line-height: 24px;
font-size: 14px;
background: #fff;
border-top: 1px solid #dfe6ec;
}
#ARLlist .BTN{
position: fixed;
z-index: 688;
left:16%;
width: 83%;
min-width: 1024px;
background-color: rgb(243,243,243);
}
#ARLlist .BTN #BTN_top{
background-color: white;
position: relative;
}
#BTN_top{
width: 100%;
padding-bottom: 5px;
border-bottom:  1px solid #dfe6ec;
height: 50px;
line-height:50px;
}
#ARLlist .BTN #BTN_title_top{
position: relative;
background-color: white;
height: 46px;
}
#ARLlist .BTN #BTN_num{
position: relative;
width:100%;
background-color: white;
}
#ARLlist .BTN #BTN_title_top #BTN_title_top_left{
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
#ARLlist .BTN #BTN_title_top #BTN_title_top_right{
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
#ARLlist .BTN .button_tree{
margin-left: 2px;
margin-right: 2px;
padding-left: 2px;
padding-right: 2px;
width: 118px;
text-align:center;;
}

#ARLlist .BTN .pi{
padding-left: 13px;
padding-right: 13px;
}
#Maptree{
position: absolute;
top: 14px;
left: 10px;
right: 0;
width: 750px;
height: 500px;
}
#Maplist{
position: absolute;
top: 11px;
left: 5px;
right: 0px;
z-index: 1000;
height: 100%;
overflow: scroll;
}
#list{
position: absolute;
left: 1700px;
width: 87.5%;
right: -47px;
top:50px;
bottom: 0;
background: #fff;
box-shadow: 0px 3px 10px rgba(0,0,0,.3);
z-index:999;
}
.Map{
display: none;
}
.li{
list-style: none;
width: 100%;
cursor: pointer;
height: 40px;
line-height:39px;
background-color: white;
margin-left: 0;
text-align: left;
border-bottom: 1px solid #dfe6ec;
min-width:770px;
}

.li:hover{
list-style: none;
cursor: pointer;
background-color: #EEF1F6;
position: relative;
}
#ARLlist #treeMap .li .cb{
float: left;
left: 5px;
}
#ARLlist #treeMap .li .cy{
float: left;
display: block;
width: 12.5%;

border-right: 1px solid #dfe6ec;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
}

.LTM{
background-color: white;
}
.active{
color:#42b983;
font-weight: bold;
}
.Asa_i{
position:absolute;
z-index: 50;
width: 130px;
height: 40px;
left:25px
}
.right_menu{
position:relative;
z-index:999;
width: 255px;
background:rgba(255,255,255,0.9);
top:0;
left: 0;
border:1px solid #dfe6ec;
box-shadow:2px 2px 5px rgba(0,0,0,0.2);
}
.rightmenu_first{
width: 100%;
border: 0 none;
text-align: left;

}
#Map_List_title{
position: absolute;
bottom: 0;
left: 228px;
}
.treeMap_title{
width: 100%;
height: 40px;
background: #fff;
border-bottom:  1px solid #dfe6ec;
min-width: 1200px;
}
.treeMap_content{
margin-left: 60px;
width: 12.5%;
height:40px;
display: block;
line-height: 40px;
font-size:20px;
font-weight: bold;
float: left;
min-width: 185px;
}
.treeMap_caozuo{
margin-left: 60px;
height:40px;
float: left;
line-height: 40px;
font-size:20px;
font-weight: bold;
margin-left: 60px;
}
.treeMap_arl{
float: left;
min-width:400px;
width:65%;
}
.msy{
display: block;
text-align: center;
width:75%;
float: left;
border-right:1px solid #dfe6ec;
height:40px;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
}
.msg_msy{
display: block;
text-align: left;
width:95%;
float: left;
height:40px;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
margin-left:14px;
}
.cz{
width:12.5%;
height:40px;
float: left;
text-align: center;
line-height: 40px;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
color: #42b983
}
.ul{
overflow: hidden;
}
.fl{
float: left;
}
.fr{
float: right;
}
.input_search{
float: left;
margin-left: 10px;
margin-top: -1.4px;
}
.ID{
text-align: center;
font-size: 15px;
font-weight: bold;
color: #1f2d3d
}
.first_li{
border-top: 1px solid #dfe6ec;
overflow-y:scroll
}
.msg_caoz{
width:20%;
min-width:210px;
float: left;
}
.nav{
width: 100%;
height: 35px;
line-height: 35px;
}
.el-icon-d-arrow-right{
line-height: 35px;
margin-left: 15px;
font-weight: bold;
font-size: 20px;
cursor: pointer;
}
.el-icon-d-arrow-right:hover{
color: #42b983
}
.center{
display: block;
margin: 0 auto;
text-align: center;
color: #42b983;
font-size: 12px;
}



/*fenlichuqu*/
.el-dialog__body{
height: 730px;
}

.arl_table{
overflow:hidden;
height: 144px;
margin-right: 20px;
position:relative;
width:100%;
border:1px solid #dfe6ec;
}
.title_arl{
font-weight: bold;
height: 60px;
line-height: 60px;
}
.title_arl span{
cursor: pointer;
	margin-right: 30px;
}
.title_arl .fr:hover{
color: #42b983;
}
.hu_sapn span{
height: 30px;
line-height: 30px;
cursor: pointer;
margin-right: 30px;
}
.hu_sapn .fr:hover{
color: #42b983
}
.arltable{
position:relative;
width:100%;
border:1px solid #dfe6ec;
}
.arltable,.hutable,.tagltable,.tagl_table,.ana_table{
height: 169px;

}
.hutable{
position:relative;
width:100%;
border:1px solid #dfe6ec;
}
.table_content{
float: left;
width:245px;
border-right: 1px solid #dfe6ec;
height: 165px;
font-size: 14px;
background-color: white;
}
.table_title{
height: 30px;
line-height: 30px;
font-weight: bold;
text-align: center;
background:#eef1f6;
font-size: 14px;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
}
.table_msg{
margin: 5px;
overflow: hidden;
text-overflow: ellipsis;
height: 125px;
}
.table_move{
display: block;
margin:30% auto;
}
.dialog{
width: 100%;
height: 100%;
background:rgba(0,0,0,.3);
position: fixed;
top:0;
left: 0;
right: 0;
bottom: 0;
z-index:2000;
}
.dialog_html{
width: 80%;
margin: 0 auto;
height:0px;
margin-top:100px;
background: #fff;
border-radius: 2px;
box-shadow: 0 1px 3px rgba(0,0,0,.3);
padding:10px 10px 10px 20px;
}
.dialog_title{
width: 100%;
height: 45px;
line-height: 45px;
margin-bottom: 30px;
}
.el-icon-close{
line-height:45px;
cursor: pointer;
}
.el-icon-close:hover{
color: #42b983
}
.content_scroll{
overflow-y: scroll;
}
.option{
display: block;
width: 100%;
line-height: 25px;
}
.tagltable{
width: 100%;
border: 1px solid #dfe6ec;
}
.tagl_table{
width: 100%;
border: 1px solid #dfe6ec;
}
.ana_table{
width: 100%;
border: 1px solid #dfe6ec;
}
.center_{
margin: 0;
text-align: center;
width: 100%;
}
.number_now{
margin-right: 76px;
}
.user_name_title{
margin: 0 auto;
margin-left: 16px;

height: 30px;
line-height: 30px;
font-weight:bold;
font-size: 14px;
}
.msy>span{
font-size: 13px;
}
.user_icon{
width: 16px;
vertical-align: middle;
}
.change_time{
margin-right:10.2%;
}
.el-dropdown-menu{
overflow-y: scroll;
  max-height: 60%;
  height: auto;
}
</style>

