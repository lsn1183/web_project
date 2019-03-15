<template>
	<div id="myWorkChildren2">
		<div id='ARLFix'>
			<p>ARLから転記</p>
			<el-table :data="arlc_Data" border  height='200' >
		      <el-table-column prop="arl_id" label="ARLID" width="100">
		      </el-table-column>
		      <el-table-column prop="detail" label="詳細" width="100">
		      </el-table-column>
		      <el-table-column prop="from_info" label="転記してきた要件" width="300">
		      </el-table-column>
		      <el-table-column prop="memo" label="備考、不明点" width="100">
		      </el-table-column>
		      <el-table-column prop="status" label="状態" >
		      </el-table-column>
		      <el-table-column prop="trigger" label="トリガー" width="200">
		      </el-table-column>
		      <el-table-column prop="action" label="動作" >
		      </el-table-column>
			</el-table>
		</div>
		<div class="top_panel"></div>
		<div id="Asa_body">
		<div class="Asa_content" v-for="(item,index) in list" >
		
			<!-- HU -->
			<div class="Asa_Hu fl">
				<h4 class="arl_size" title="ユニークID">ユニークID</h4>
				<span class="Hu_Id"><span class="HU_size" >{{index}}</span></span>
				<el-button type="text" size="small" class="arl_btn" @click="examine_hu(index)">查看</el-button>
			</div>
			<!-- option -->
			<div class="Asa_option fl">
				<h4 class="arl_size" title="オプション項目">オプション項目</h4>
				<p class="option_size">
					<span class="option_title">AMP:</span>
						<!--AMP下拉框-->
						<el-select v-model="item.amp" placeholder="请选择" size='mini' class="opt_ipt_id" @change="option_change(index)">
						    <el-option v-for="(item,index) in AMP" :key="item.value" :label="item.value" :value="item.value" >
						      <span style="float: left">{{ item.label }}</span>
						      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
						    </el-option>
						</el-select>	
				</p>
				<p class="option_size">
					<span class="option_title">DSRC:</span>
					<el-select v-model="item.dsrc" placeholder="请选择" size='mini' class="opt_ipt_id" :key="index" @change="option_change(index)">
					    <el-option v-for="(item,index) in DSRC" :key="item.value" :label="item.value" :value="item.value">
					      <span style="float: left">{{ item.label }}</span>
					      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
					    </el-option>
					</el-select>
				</p>
				<p class="option_size">
					<span class="option_title">DCM:</span>
						<el-select v-model="item.dcm" placeholder="请选择" size='mini' class="opt_ipt_id" :key="index" @change="option_change(index)">
						    <el-option v-for="(item,index) in PCM" :key="item.value" :label="item.value" :value="item.value">
						      <span style="float: left">{{ item.label }}</span>
						      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
						    </el-option>
						</el-select>	
				</p>
				<p class="option_size">
					<span class="option_title">RSE:</span>
					<el-select v-model="item.rse" placeholder="请选择" size='mini' class="opt_ipt_id" :key="index" @change="option_change(index)">
						    <el-option v-for="(item,index) in RSE" :key="item.value" :label="item.value" :value="item.value">
						      <span style="float: left">{{ item.label }}</span>
						      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
						    </el-option>
						</el-select>
				</p>
				<p class="option_size">
					<span class="option_title opt_line">Touch Pad:</span>
					<el-select v-model="item.touch_pad" placeholder="请选择" size='mini' class="opt_ipt_id" :key="index" @change="option_change(index)">
						    <el-option v-for="(item,index) in TouchPad" :key="item.value" :label="item.value" :value="item.value">
						      <span style="float: left">{{ item.label }}</span>
						      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
						    </el-option>
						</el-select>
				</p>
				<p class="option_size">
					<span class="option_title opt_line" >Soparate Disp:</span>
						<el-select v-model="item.separate_disp" placeholder="请选择" size='mini' class="opt_ipt_id" :key="index" @change="option_change(index)">
						    <el-option v-for="(item,index) in SeparateDisp" :key="item.value" :label="item.value" :value="item.value">
						      <span style="float: left">{{ item.label }}</span>
						      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
						    </el-option>
						</el-select>
				</p>
				<p class="option_size_id">
					<span class="option_title_id">システム構成:</span>
						<el-input type="textarea" :rows="1"  class="opt_ipt_id" v-model="item.system_conf"></el-input>
				</p>
			</div>
			<!-- 关联 -->
			<div class="Asa_relevance fl">
				<h4 class="arl_size" title="関連基本要件">関連基本要件</h4> 
				<!-- <el-button type="text" size="small" class="arl_btn" @click="correlation(index)">添加/查看</el-button> -->
				<el-input  type="textarea" :rows="8"  v-model="item.rel_requirement" @blur="replace(index)"></el-input>
			</div>
			<!-- 责任分担 -->
			
			<!-- 全都没有 -->
			<div class="Asa_duty fl" v-if="item.meu_action=='-'&&item.meu_status=='-'&&item.meu_trigger=='-'&&item.dcu_action=='-'&&item.dcu_status=='-'&&item.dcu_trigger=='-'">
				<h4 class="arl_size" title="責務分担">責務分担</h4>
				<p class="append_dcu_meu">
					<i class="el-icon-plus" @click="dutyshow(index)"></i>
				</p>
				<span class="duty_Id">H/U分類ID: <span class="duty_size" :title="item.hu_id">
				<el-input  class="opt_ipt" v-model="item.hu_category_id"  @blur="itp_blur(index)"></el-input>
				</span></span>
			</div>
			<!-- 没有dcu -->
			<div class="Asa_duty fl" v-else-if="item.dcu_action=='-'&&item.dcu_status=='-'&&item.dcu_trigger=='-'">
				<h4 class="arl_size" title="責務分担">責務分担</h4>
				<p class="append_dcu_meu">
					<i class="el-icon-plus" @click="dutyshow(index)"></i>
				</p>
				<el-button type="text" size="small" class="operation_btn" @click="examine_MEU(index)">MEU</el-button>
				<span class="duty_Id">H/U分類ID: <span class="duty_size" :title="item.hu_id">
				<el-input  class="opt_ipt" v-model="item.hu_category_id"  @blur="itp_blur(index)"></el-input>
				</span></span>
			</div>
			<!-- 没有meu -->
			<div class="Asa_duty fl" v-else-if="item.meu_action=='-'&&item.meu_status=='-'&&item.meu_trigger=='-'">
				<h4 class="arl_size" title="責務分担">責務分担</h4>
				<p class="append_dcu_meu">
					<i class="el-icon-plus" @click="dutyshow(index)"></i>
				</p>
				<el-button type="text" size="small" class="operation_btn" @click="examine(index)">DCU</el-button>
				
				<span class="duty_Id">H/U分類ID: <span class="duty_size" :title="item.hu_id">
				<el-input  class="opt_ipt" v-model="item.hu_category_id"  @blur="itp_blur(index)"></el-input>
				</span></span>
			</div>
			<!-- 全都有 -->
			<div class="Asa_duty fl" v-else>
				<h4 class="arl_size" title="責務分担">責務分担</h4>
				<el-button type="text" size="small" class="operation_btn" @click="examine(index)">DCU</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="examine_MEU(index)">MEU</el-button>
				<span class="duty_Id">H/U分類ID: <span class="duty_size" :title="item.hu_id">
				<el-input  class="opt_ipt" v-model="item.hu_category_id"  @blur="itp_blur(index)"></el-input>
				</span></span>
			</div>
			<!-- 模块 -->
			<div class="Asa_moudel fl">
				<h4 class="arl_size" title="部品">部品</h4>
				<el-button type="text" size="small" class="arl_btn" @click="HU_moudel(index)">H/U以外のＭＭ部品</el-button>
				<el-button type="text" size="small" class="arl_btn" @click="other_moudel(index)">他部署設計部品<br /><br />(部品名は参考)</el-button>
			</div>
			<!-- 备考 -->
			<div class="Asa_remark fl">
				<h4 class="arl_size" title="备注">其他</h4>
				<el-button type="text" size="small" class="operation_btn" @click="texTarea(index)">备考</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="literature(index)">参考文献</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="tiem(index)">日付</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="change_reason(index)">更改理由</el-button>
			</div>
			<!-- delete -->
			<div class="Asa_dele fl">
				<h4 class="arl_size" title="操作">操作</h4>
				<el-button type="text" size="small" class="operation_btn" @click="copy(index)">复制添加</el-button>
				<!-- <el-button type="text" size="small" class="operation_btn" @click="Delete()">删除</el-button> -->
				<el-button type="text" size="small" class="operation_btn" @click="Up(index)">上移动</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="Down(index)">下移动</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="ach(index)" v-if="list[index].complete_flag ==1">已完成</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="ach(index)" v-else>完成</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="translate(index)" v-if="list[index].translation_flag ==1">已翻译</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="translate(index)" v-else>翻译</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="recognize(index)"  v-if="list[index].agree_flag ==1">已承认</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="recognize(index)" v-else>承认</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="zhizhai(index)" v-if="list[index].has_problem ==1">已指摘</el-button>
				<el-button type="text" size="small" class="operation_btn" @click="zhizhai(index)" v-else>指摘</el-button>
			</div>
		</div>
	</div>
		<!-- 悬浮保存按钮 -->
		<div class="Asa_btutton">
			<el-button  class="arl_btn" @click="save()">保存</el-button>
			<el-button  class="arl_btn" @click="add()">添加</el-button>
			<el-button  class="arl_btn" @click="back()">返回</el-button>
			<el-button  class="arl_btn" @click="save_back()">保存返回</el-button>
		</div>
		<el-dialog title="添加DCU" :visible.sync="DCU_flag" :modal-append-to-body="false">
		   <el-table :data="arlc_Data" border style="width: 100%;">
		      <el-table-column prop="arl_id" label="ARLID">
		      </el-table-column>
		      <el-table-column prop="detail" label="詳細">
		      </el-table-column>
		      <el-table-column prop="from_info" label="転記してきた要件">
		      </el-table-column>
		      <el-table-column prop="memo" label="備考、不明点">
		      </el-table-column>
		      <el-table-column prop="status" label="状態">
		      </el-table-column>
		      <el-table-column prop="trigger" label="トリガー">
		      </el-table-column>
		      <el-table-column prop="action" label="動作">
		      </el-table-column>
			</el-table>	
			<p class="DCU_size">
				<h5 class="fl">動作 :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="dcu_action" v-model="dcu_action"  class="DCU_ipt" ></el-input>
			</p>
			<p class="DCU_size">
				<h5 class="fl">状態 :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="dcu_status" v-model="dcu_status"  class="DCU_ipt" ></el-input>
			</p>
			<p class="DCU_size">
				<h5 class="fl">トリガー :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="dcu_trigger" v-model="dcu_trigger"  class="DCU_ipt" ></el-input>
			</p>
			<p class="DCU_btn">
				<!-- <el-button  size="small" class="operation_btn fr" @click='DCU_dele(index)'>删除</el-button> -->
				<el-button  size="small" class="operation_btn fr" @click='DCU_save(index)'>保存</el-button>
				<el-button  size="small" class="operation_btn fr" @click='DCU_back(index)'>返回</el-button>
			</p>
		</el-dialog>
		<el-dialog title="添加MEU" :visible.sync="MEU_flag" :modal-append-to-body="false">
		   <el-table :data="arlc_Data" border style="width: 100%;">
		      <el-table-column prop="arl_id" label="ARLID">
		      </el-table-column>
		      <el-table-column prop="detail" label="詳細">
		      </el-table-column>
		      <el-table-column prop="from_info" label="転記してきた要件">
		      </el-table-column>
		      <el-table-column prop="memo" label="備考、不明点">
		      </el-table-column>
		      <el-table-column prop="status" label="状態">
		      </el-table-column>
		      <el-table-column prop="trigger" label="トリガー">
		      </el-table-column>
		      <el-table-column prop="action" label="動作">
		      </el-table-column>
			</el-table>
			<p class="DCU_size">
				<h5 class="fl">動作 :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="meu_action" v-model="meu_action"  class="DCU_ipt"></el-input>
			</p>
			<p class="DCU_size">
				<h5 class="fl">状態 :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="meu_status" v-model="meu_status"  class="DCU_ipt"></el-input>
			</p>
			<p class="DCU_size">
				<h5 class="fl">トリガー :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="meu_trigger" v-model="meu_trigger"  class="DCU_ipt"></el-input>
			</p>
			<p class="DCU_btn">
				<!-- <el-button  size="small" class="operation_btn fr" @click='MEU_dele()'>删除</el-button> -->
				<el-button  size="small" class="operation_btn fr" @click='MEU_save()'>保存</el-button>
				<el-button  size="small" class="operation_btn fr" @click='MEU_back()'>返回</el-button>
			</p>
		</el-dialog>
		<el-dialog title="备考" :visible.sync="flag" :modal-append-to-body="false" >
			<el-input
			  type="textarea" :rows="10" placeholder="请输入内容"
			  v-model="remark">
			</el-input>
			<el-button class="save fr" @click="texTareasave()">保存</el-button>
		</el-dialog>
		<el-dialog title="機能配置を判断したエビデンス" :visible.sync="literature_flag" :modal-append-to-body="false" >
			<p class="DCU_size">
				<h2 class="fl">001 システム仕様書 :</h2>
				<h5 class="fl">章　Chapter/Sectionor ページ番号 Page No :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="sys_spec_chapter" v-model="sys_spec_chapter"  class="DCU_ipt" ></el-input>
			</p>
			<p class="DCU_size">
				<h2 class="fl">003 共通アプリ・AVC-LAN仕様書 :</h2>
				<h5 class="fl">章　Chapter/Sectionor ページ番号 Page No :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="common_chapter" v-model="common_chapter"  class="DCU_ipt" ></el-input>
				<h5 class="fl">シーケンス仕様Sequence spec. :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="common_seq_spec" v-model="common_seq_spec"  class="DCU_ipt" ></el-input>
				<h5 class="fl">シーケンス番号Sequence No. :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="common_seq_no" v-model="common_seq_no"  class="DCU_ipt" ></el-input>
				<h5 class="fl">コマンドガイドCommand guide :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="common_cmd_guide" v-model="common_cmd_guide"  class="DCU_ipt" ></el-input>
				<h5 class="fl">OPC :</h5>
				<el-input  type="textarea" :rows="2" :placeholder="common_opc" v-model="common_opc"  class="DCU_ipt" ></el-input>
			</p>
			<p class="DCU_size">
				<h2 class="fl">318 DCU-MEU間連携仕様書 DCU-MEU interaction spec. :</h2>
				<h5 class="fl">機能配置・機能仕様Function location and spec.</h5>
				<el-input  type="textarea" :rows="2" :placeholder="inter_loc_spec" v-model="inter_loc_spec"  class="DCU_ipt" ></el-input>
				<h5 class="fl">章　Chapter/Sectionor ページ番号 Page No</h5>
				<el-input  type="textarea" :rows="2" :placeholder="inter_chapter" v-model="inter_chapter"  class="DCU_ipt" ></el-input>
			</p>
			<p class="DCU_size">
				<h2 class="fl">その他資料 Other document. </h2>
				<h5 class="fl">ドキュメント名※トヨタ仕様の場合は仕様番号も記載する事</h5>
				<el-input  type="textarea" :rows="2" :placeholder="other_chapter" v-model="other_chapter"  class="DCU_ipt" ></el-input>
				<h5 class="fl">章　Chapter/Sectionor ページ番号 Page No</h5>
				<el-input  type="textarea" :rows="2" :placeholder="other_doc" v-model="other_doc"  class="DCU_ipt" ></el-input>
			</p>
			<el-button class="save fr" @click="literaturesave()">保存</el-button>
		</el-dialog>
		<el-dialog title="查看" :visible.sync="arl_check" class="el_c" :modal-append-to-body="false">
		   <el-table :data="arlc_Data" border style="width: 100%;">
		      <el-table-column prop="arl_id" label="ARLID">
		      </el-table-column>
		      <el-table-column prop="detail" label="詳細">
		      </el-table-column>
		      <el-table-column prop="from_info" label="転記してきた要件">
		      </el-table-column>
		      <el-table-column prop="memo" label="備考、不明点">
		      </el-table-column>
		      <el-table-column prop="status" label="状態">
		      </el-table-column>
		      <el-table-column prop="trigger" label="トリガー">
		      </el-table-column>
		      <el-table-column prop="action" label="動作">
		      </el-table-column>
			</el-table>
		</el-dialog>


		<el-dialog title="H/U以外のＭＭ部品" :visible.sync="HUM_flag" class="ed_hm" :modal-append-to-body="false">
		   <el-table :data="arlc_Data" border style="width: 100%;">
		      <el-table-column prop="arl_id" label="ARLID">
		      </el-table-column>
		      <el-table-column prop="detail" label="詳細">
		      </el-table-column>
		      <el-table-column prop="from_info" label="転記してきた要件">
		      </el-table-column>
		      <el-table-column prop="memo" label="備考、不明点">
		      </el-table-column>
		      <el-table-column prop="status" label="状態">
		      </el-table-column>
		      <el-table-column prop="trigger" label="トリガー">
		      </el-table-column>
		      <el-table-column prop="action" label="動作">
		      </el-table-column>
			</el-table>	
			<div class="HUM" v-for="(item2,index) in list_model[0].models">
				<div class="HUM_name fl" >
					<h3 class="HUM_title">
						<span class="HUM_span">部品</span>
					</h3>
					<div class="HUM_content">
						<el-select v-model="item2.name" placeholder="请选择" class="HUM_content_select">
				           <el-option 
				           v-for="name in names" 
				           :label="name.name" 
				           :value="name.name"
				           :key="name.name"
				           >
			               </el-option>
				          </el-select>
					</div>
				</div>
				<div class="HUM_textar fl">
					<h3 class="HUM_title">
						<span class="HUM_span">值</span>
					</h3>
					<div class="HUM_content">
						<el-input  type="textarea"  :rows="2"  placeholder="请输入内容" v-model='item2.val'></el-input>
					</div>
				</div>
				<div class="HUM_caozuo fl">
					<h3 class="HUM_title">
						<span class="HUM_span">操作</span>
					</h3>
					<div class="HUM_content">
					    <el-button type="primary" class="rel_btn" @click="edothm_del(index)">-</el-button>
					</div>
				</div>
			</div>
			<el-button class="save fr" @click="humsave()">保存</el-button>
			<el-button class="save fr" @click="edhm_add(index)" style="margin-right: 15px;">添加</el-button>
		</el-dialog>


		<el-dialog title="他部署設計部品" :visible.sync="othm_flag" class="ed_hm" :modal-append-to-body="false">
		   <el-table :data="arlc_Data" border style="width: 100%;">
		      <el-table-column prop="arl_id" label="ARLID">
		      </el-table-column>
		      <el-table-column prop="detail" label="詳細">
		      </el-table-column>
		      <el-table-column prop="from_info" label="転記してきた要件">
		      </el-table-column>
		      <el-table-column prop="memo" label="備考、不明点">
		      </el-table-column>
		      <el-table-column prop="status" label="状態">
		      </el-table-column>
		      <el-table-column prop="trigger" label="トリガー">
		      </el-table-column>
		      <el-table-column prop="action" label="動作">
		      </el-table-column>
			</el-table>	

			<div class="HUM" v-for="(item,index) in list_model[1].models">
				<div class="HUM_name fl" >
					<h3 class="HUM_title">
						<span class="HUM_span">部品</span>
					</h3>
					<div class="HUM_content">
						<el-select v-model="item.name" placeholder="请选择" class="HUM_content_select">
				           <el-option 
				           v-for="name in namess" 
				           :label="name.name" 
				           :value="name.name"
				           :key="name.name"
				           >
			               </el-option>
				          </el-select>
					</div>
				</div>
				<div class="HUM_textar fl">
					<h3 class="HUM_title">
						<span class="HUM_span">值</span>
					</h3>
					<div class="HUM_content">
						<el-input  type="textarea"  :rows="2"  placeholder="请输入内容" v-model='item.val'></el-input>
					</div>
				</div>
				<div class="HUM_caozuo fl">
					<h3 class="HUM_title">
						<span class="HUM_span">操作</span>
					</h3>
					<div class="HUM_content">
					    <el-button type="primary" class="rel_btn" @click="othm_del(index)">-</el-button>
					</div>
				</div>
			</div>
			<el-button class="save fr" @click="othmsave()">保存</el-button>
			<el-button class="save fr" @click="edoth_add()" style="margin-right: 15px;">添加</el-button>
		</el-dialog>

		<el-dialog title="日付" :visible.sync="tiem_flag" class="ed_hm"  :modal-append-to-body="false">
		  <template>
		 	<el-date-picker v-model="new_Date" type="date" placeholder="选择日期" :picker-options="pickerOptions1" @change="setEndDate">
		 	 </el-date-picker>
		  </template>
		  <el-button class="save fr" @click="save_time(index)">保存</el-button>
		</el-dialog>
		<el-dialog title="变更理由" :visible.sync="change_flag" class="ed_hm"  :modal-append-to-body="false">
		  <el-input
		    type="textarea" :rows="10" placeholder="请输入内容"
		    v-model="change_content">
		  </el-input>
		  <el-button class="save fr" @click="change_save()">保存</el-button>
		</el-dialog>

		<!-- 责任分担~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
		<el-dialog title="责任分担" :visible.sync="dutyshow_flag" :modal-append-to-body="false">
		   <el-table :data="arlc_Data" border style="width: 100%;">
		      <el-table-column prop="arl_id" label="ARLID">
		      </el-table-column>
		      <el-table-column prop="detail" label="詳細">
		      </el-table-column>
		      <el-table-column prop="from_info" label="転記してきた要件">
		      </el-table-column>
		      <el-table-column prop="memo" label="備考、不明点">
		      </el-table-column>
		      <el-table-column prop="status" label="状態">
		      </el-table-column>
		      <el-table-column prop="trigger" label="トリガー">
		      </el-table-column>
		      <el-table-column prop="action" label="動作">
		      </el-table-column>
			</el-table>	
			<template>
			  <el-select v-model="value2" placeholder="请选择" class="select_ipt" @change="pd(value2)">
			    <el-option  v-for="item in options2" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled">
			    </el-option>
			  </el-select>
			</template>
			<div v-if="dcu_show">
				<p class="DCU_size">
					<h5 class="fl">動作 :</h5>
					<el-input  type="textarea" :rows="2" :placeholder="dcu_action" v-model="dcu_action"  class="DCU_ipt"></el-input>
				</p>
				<p class="DCU_size">
					<h5 class="fl">状態 :</h5>
					<el-input  type="textarea" :rows="2" :placeholder="dcu_status" v-model="dcu_status"  class="DCU_ipt" ></el-input>
				</p>
				<p class="DCU_size">
					<h5 class="fl">トリガー :</h5>
					<el-input  type="textarea" :rows="2" :placeholder="dcu_trigger" v-model="dcu_trigger"  class="DCU_ipt" ></el-input>
				</p>
				<p class="DCU_btn">
					<!-- <el-button  size="small" class="operation_btn fr" @click='dutyDCU_dele(index)'>删除</el-button> -->
					<el-button  size="small" class="operation_btn fr" @click='dutyDCU_save(index)'>保存</el-button>
					<el-button  size="small" class="operation_btn fr" @click='dutyDCU_back(index)'>返回</el-button>
				</p>
			</div>
			<div v-if="meu_show">
				<p class="DCU_size">
					<h5 class="fl">動作 :</h5>
					<el-input  type="textarea" :rows="2" :placeholder="meu_action" v-model="meu_action"  class="DCU_ipt"></el-input>
				</p>
				<p class="DCU_size">
					<h5 class="fl">状態 :</h5>
					<el-input  type="textarea" :rows="2" :placeholder="meu_status" v-model="meu_status"  class="DCU_ipt"></el-input>
				</p>
				<p class="DCU_size">
					<h5 class="fl">トリガー :</h5>
					<el-input  type="textarea" :rows="2" :placeholder="meu_trigger" v-model="meu_trigger"  class="DCU_ipt"></el-input>
				</p>
				<p class="DCU_btn">
					<!-- <el-button  size="small" class="operation_btn fr" @click='dutyMEU_dele()'>删除</el-button> -->
					<el-button  size="small" class="operation_btn fr" @click='dutyMEU_save()'>保存</el-button>
					<el-button  size="small" class="operation_btn fr" @click='dutyMEU_back()'>返回</el-button>
				</p>
			</div>
		</el-dialog>
	</div>
</template>

<script>
	export default{
		data(){
			return{
				HuOption:{},
				option_data:'111111',
				//HU_compile页面    オプション項目   AMP下拉框
				AMP: [
					{
			        	value: '0',
			        	label: 'don’t care'
			      	},
			      	 {
			        	value: '1',
			        	label: 'MOSTAMP'
			        }, 
			        {
			          value: '2',
			          label: 'D0AMP(AVCLAN外付け)'
			        }, 
			        {
			          value: '3',
			          label: 'D4AMP(内臓)'
			        }
			    ],
			    valueAMP: '',
				//HU_compile页面    オプション項目   DSRC下拉框
				DSRC: [
					{
			        	value: '0',
			        	label: 'don’t care'
			       },
			        {
			        	value: '1',
			        	label: '無'
			        },
			         {
			          value: '2',
			          label: 'USB接続'
			        }, 
			        {
			          value: '3',
			          label: 'LAN接続'
			        }
			    ],
			    valueDSRC: '',
				//HU_compile页面    オプション項目   PCM下拉框
				PCM: [
					{
			        	value: '0',
			        	label: 'don’t care'
			       }, 
			       {
			        	value: '1',
			        	label: '無'
			        },
			         {
			          value: '2',
			          label: '有'
			        }
			    ],
			    valuePCM: '',
				//HU_compile页面    オプション項目   RSE下拉框
				RSE: [
					{
			        	value: '0',
			        	label: 'don’t care'
			       }, 
			       {
			        	value: '1',
			        	label: '無'
			        }, 
			        {
			          value: '2',
			          label: 'フルRSE/シートバックRSE'
			        },{
			          value: '3',
			          label: '簡易RSE'
			        }
			    ],
			    valueRSE: '',
				//HU_compile页面    オプション項目   Touch Pad下拉框
				TouchPad: [
					{
			        	value: '0',
			        	label: 'don’t care'
			       }, 
			       {
			        	value: '1',
			        	label: '無'
			        }, 
			        {
			          value: '2',
			          label: '有'
			        }
			     ],
			    valueTouchPad: '',
				//HU_compile页面    オプション項目   Soparate Disp下拉框
				SeparateDisp: [
					{
			        	value: '0',
			        	label: 'don’t care'
			       }, 
			       {
			        	value: '1',
			        	label: '無'
			        }, 
			        {
			          value: '2',
			          label: '有'
			        }],
			    valueSeparateDisp: '',
				list:[],
				p_list:[],
				mn_m:'',
				mn_g:'',
				mo_a:'',
				mo_g:'',
				mo_s:'',
				re_a:'',
				re_g:'',
				re_s:'',
				new_Date: '',
				new_Date_num: '',
				flag:false,
				DCU_flag:false,
				MEU_flag:false,
				HUM_flag:false,
				othm_flag:false,
				disabled:true,
				MEU_disabled:true,
				dcu_action:"",
				dcu_status:'',
				dcu_trigger:'',
				data_time:"",
				dcu_if:false,
				dcu_show:false,
				meu_show:false,
				meu_if:false,
				index:0,
				category:[],
				index_meu:0,
				index_hum:0,
				meu_action:'',
				meu_status:'',
				meu_trigger:'',
				hum_value:'',
				texTarea_index:0,
				remark:'',
				change_content:'',
				activeNames: ['1'],
				arl_id:this.$route.params.ARL_id,
				literature_index:0,
				literature_flag:false,
				sys_spec_chapter:'',
				common_chapter:'',
				common_seq_spec:'',
				common_seq_no:'',
				common_cmd_guide:'',
				common_opc:'',
				inter_loc_spec:'',
				inter_chapter:'',
				other_chapter:'',
				other_doc:'',
				state:'',
				list_model:[{"category":"", "models": []},{"category":"", "models": []}],
				hdata:'',
				list_model2:"",
				tiem_flag:false,
				change_flag:false,
				val:'',
				change_index:0,
				names: [],
		        namess:[],
				pickerOptions0: {
				         disabledDate(time) {
				           return time.getTime() < Date.now() - 8.64e7;
				         }
				       },
				       pickerOptions1: {
				         shortcuts: [{
				           text: '今天',
				           onClick(picker) {
				             picker.$emit('pick', new Date());
				           }
				         }, {
				           text: '昨天',
				           onClick(picker) {
				             const date = new Date();
				             date.setTime(date.getTime() - 3600 * 1000 * 24);
				             picker.$emit('pick', date);
				           }
				         }, {
				           text: '一周前',
				           onClick(picker) {
				             const date = new Date();
				             date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
				             picker.$emit('pick', date);
				           }
				         }]
				       },
				value2: '',
				arl_check: false,
				arlc_Data: [{
					arl_id:'',
					small_category:'',
					detail:'',
					from_info:'',
					status:'',
					trigger:'',
					action:''
				}],		       
			        model_id: '',
				ARL_id: '',
				dutyshow_flag:false,
				options2: [
						{
				          value: 'DCU',
				          label: 'DCU',
				          disabled: false
				        }, 
				        {
				          value: 'MEU',
				          label: 'MEU	',
				          disabled: false
				        }
				],
				 value2:''
				}
		},
		created:function(){
				if(typeof(this.$route.params.ARL_id) == 'string'){
					window.sessionStorage.setItem('sion_Id',this.$route.params.ARL_id)			
					this.$axios.get(this.Ip+'/ARLSubHu/'+window.sessionStorage.getItem('sion_Id'))
						.then(res => {

							this.list=res.data.content;
							this.hdata=this.list[0].hu_id;
							for(var i=0;i<this.list.length;i++){
								if(this.list[i].dcu_status=="-"&&this.list[i].dcu_action=="-"&&this.list[i].dcu_trigger=="-"&&this.list[i].meu_action=="-"&&this.list[i].meu_status=="-"&&this.list[i].meu_trigger=="-"){
									this.list[i].hu_category_id=""
									
								}
							}
						})
					this.$axios.get(this.Ip+'/ARLContent/'+window.sessionStorage.getItem('sion_Id'))
						.then(res => {
							this.arlc_Data[0].arl_id=res.data.content.arl_id
							this.arlc_Data[0].detail=res.data.content.detail
							this.arlc_Data[0].from_info=res.data.content.from_info
							this.arlc_Data[0].memo=res.data.content.memo
							this.arlc_Data[0].status=res.data.content.status
							this.arlc_Data[0].trigger=res.data.content.trigger
							this.arlc_Data[0].action=res.data.content.action
					})
					this.$axios.get(this.Ip+'/HuOption')
					.then(res =>{
						this.HuOption = res.data
					})
				}else{
					this.$axios.get(this.Ip+'/ARLSubHu/'+window.sessionStorage.getItem('sion_Id'))
					.then(res => {
						this.list=res.data.content;
						this.hdata=this.list[0].hu_id;
					})
					this.$axios.get(this.Ip+'/ARLContent/'+window.sessionStorage.getItem('sion_Id'))
						.then(res => {
							this.arlc_Data[0].arl_id=res.data.content.arl_id
							this.arlc_Data[0].detail=res.data.content.detail
							this.arlc_Data[0].from_info=res.data.content.from_info
							this.arlc_Data[0].memo=res.data.content.memo
							this.arlc_Data[0].status=res.data.content.status
							this.arlc_Data[0].trigger=res.data.content.trigger
							this.arlc_Data[0].action=res.data.content.action
					})
					this.$axios.get(this.Ip+'/HuOption')
					.then(res =>{
						this.HuOption = res.data
						
//						console.log(this.HuOption)
//						var arr = [];
//						for(var i in this.HuOption){
//							var str = i + ',' + this.HuOption[i]
//							console.log(JSON.parse(str))
//							arr.push(str)
//						}
						
					})	
				}		
		},
		mounted: function () {
					this.$axios.get(this.Ip+'/UserContent/'+window.sessionStorage.getItem('admin'))
						.then(res => {
							this.p_list=res.data.content;
							this.mn_m=this.p_list.permission_list[0].mng_member;
							this.mn_g=this.p_list.permission_list[0].mng_group;
							this.mo_a=this.p_list.permission_list[0].modify_all;
							this.mo_g=this.p_list.permission_list[0].modify_group;
							this.mo_s=this.p_list.permission_list[0].modify_self;
							this.re_a=this.p_list.permission_list[0].read_all;
							this.re_g=this.p_list.permission_list[0].read_group;
							this.re_s=this.p_list.permission_list[0].read_self;
					})
		},
		methods:{
			Delete:function(index){
				this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
				          confirmButtonText: '确定',
				          cancelButtonText: '取消',
				          type: 'warning'
				        }).then(() => {
				          var item = []
				          item = this.list
				          item.splice(index,1)
				          this.list= [] 
				          this.list=item
				          this.$notify({
				            message: '删除成功!'
				          });
				        }).catch(() => {
				          this.$notify({
				            type: 'info',
				            message: '已取消删除'
				      });          
				});
				
			},
			Up:function(index){
				if(this.list.length>1){
					if(index!=0){
						var item=[];
						item = this.list[index]
						this.list[index] = this.list[index-1]
						this.list[index-1] = item
						var im = this.list;
						this.list = [];
						this.list = im;
						    this.$notify({
						      type: 'info',
						      message: '向上移动成功'
						})
					}
				}
			},
			Down:function(index){
				if(this.list.length>1){
					if(index!=this.list.length-1){
						var item=[];
						item=this.list[index]
						this.list[index]=this.list[index+1]
						this.list[index+1]=item
						var im = this.list;
						this.list = [];
						this.list = im;
						    this.$notify({
						      type: 'info',
						      message: '向下移动成功'
						})
					}
				}
			},
			copy:function(index){
				var item=[];
				item=this.list[index];
				item=JSON.parse(JSON.stringify(item))
				var msg =this.list;
				msg.push(item)
				this.list = [];
				this.list = msg;
				this.$message('添加ユニークID'+(this.list.length-1)+'成功');
			},
			texTarea(index){
				this.texTarea_index=index
				this.remark=this.list[this.texTarea_index].remark
				this.flag = !this.flag;
			},
			texTareasave(){
				this.list[this.texTarea_index].remark=this.remark
				this.flag = !this.flag;

			},
			examine(index){
				this.index=index
				this.DCU_flag = !this.DCU_flag
				this.dcu_action=this.list[index].dcu_action
				this.dcu_status=this.list[index].dcu_status
				this.dcu_trigger=this.list[index].dcu_trigger
			},
			DCU_save(index){
				var patt = /^[\(][0-9][\)]/;
				
				if(patt.test(this.dcu_action)&&patt.test(this.dcu_status)){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.DCU_flag = !this.DCU_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
				}
				else if((this.dcu_action!=""&&this.dcu_action=="-")&&(this.dcu_status!=""&&this.dcu_status=="-")&&(this.dcu_trigger!=""&&this.dcu_trigger=="-")){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.DCU_flag = !this.DCU_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}
					

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}
					

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}

				}else if((this.dcu_action!=""&&this.dcu_action!="-"&&patt.test(this.dcu_action))&&(this.dcu_status!=""&&this.dcu_status=="-")&&(this.dcu_trigger!=""&&this.dcu_trigger=="-")){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.DCU_flag = !this.DCU_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}

				}else if((this.dcu_action!=""&&this.dcu_action=="-")&&(this.dcu_status!=""&&this.dcu_status!="-"&&patt.test(this.dcu_status))&&(this.dcu_trigger!=""&&this.dcu_trigger=="-")){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.DCU_flag = !this.DCU_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
				}else if((this.dcu_action!=""&&this.dcu_action=="-")&&(this.dcu_status!=""&&this.dcu_status=="-")&&(this.dcu_trigger!=""&&this.dcu_trigger!="-"&&patt.test(this.dcu_trigger))){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.DCU_flag = !this.DCU_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
				}else{
					this.$notify({
					  message: '请检查您的信息输入是否追加序号'
					})
				}
				
			},
			DCU_dele(){
				this.DCU_flag = !this.DCU_flag
				this.list[this.index].dcu_action='-'
				this.list[this.index].dcu_status='-'
				this.list[this.index].dcu_trigger='-'

				if(this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
					this.list[this.index].hu_category_id=2
				}else{
					this.list[this.index].hu_category_id=""
				}

				if(this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
					this.list[this.index].hu_category_id=2
				}else{
					this.list[this.index].hu_category_id=""
				}

				if(this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
					this.list[this.index].hu_category_id=2
				}else{
					this.list[this.index].hu_category_id=""
				}

			},
			DCU_back(){
				this.DCU_flag = !this.DCU_flag
			},
			dutyDCU_save(){
				var patt = /^[\(][0-9][\)]/;
				
				if(patt.test(this.dcu_action)&&patt.test(this.dcu_status)){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.dutyshow_flag = !this.dutyshow_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					
				}
				else if((this.dcu_action!=""&&this.dcu_action=="-")&&(this.dcu_status!=""&&this.dcu_status=="-")&&(this.dcu_trigger!=""&&this.dcu_trigger=="-")){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.dutyshow_flag = !this.dutyshow_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}
					

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}
					

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	

				}else if((this.dcu_action!=""&&this.dcu_action!="-"&&patt.test(this.dcu_action))&&(this.dcu_status!=""&&this.dcu_status=="-")&&(this.dcu_trigger!=""&&this.dcu_trigger=="-")){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.dutyshow_flag = !this.dutyshow_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	


				}else if((this.dcu_action!=""&&this.dcu_action=="-")&&(this.dcu_status!=""&&this.dcu_status!="-"&&patt.test(this.dcu_status))&&(this.dcu_trigger!=""&&this.dcu_trigger=="-")){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.dutyshow_flag = !this.dutyshow_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
				}else if((this.dcu_action!=""&&this.dcu_action=="-")&&(this.dcu_status!=""&&this.dcu_status=="-")&&(this.dcu_trigger!=""&&this.dcu_trigger!="-"&&patt.test(this.dcu_trigger))){
					this.list[this.index].dcu_action=this.dcu_action
					this.list[this.index].dcu_status=this.dcu_status
					this.list[this.index].dcu_trigger=this.dcu_trigger
					this.dutyshow_flag = !this.dutyshow_flag

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"){
						this.list[this.index].hu_category_id=1
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}

					if(this.list[this.index].dcu_action!=""&&this.list[this.index].dcu_action!="-"&&this.list[this.index].meu_action!=""&&this.list[this.index].meu_action!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_action==""){
						this.list[this.index].dcu_action="-"
					}

					if(this.list[this.index].dcu_status!=""&&this.list[this.index].dcu_status!="-"&&this.list[this.index].meu_status!=""&&this.list[this.index].meu_status!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_status==""){
						this.list[this.index].dcu_status="-"
					}

					if(this.list[this.index].dcu_trigger!=""&&this.list[this.index].dcu_trigger!="-"&&this.list[this.index].meu_trigger!=""&&this.list[this.index].meu_trigger!="-"){
						this.list[this.index].hu_category_id=0
					}else if(this.list[this.index].dcu_trigger==""){
						this.list[this.index].dcu_trigger="-"
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
					if(this.list[this.index].meu_trigger =="(DCUと同様)"&&this.list[this.index].meu_action =="(DCUと同様)"&&this.list[this.index].meu_status =="(DCUと同様)"){
						this.list[this.index].hu_category_id=3
					}	
				}else{
					this.$notify({
					  message: '请检查您的信息输入是否追加序号'
					})
				}
			},
			dutyDCU_back(){
				this.dutyshow_flag = !this.dutyshow_flag	
			},
			examine_MEU(index){
				this.index_meu=index
				this.MEU_flag = !this.MEU_flag
				this.meu_action=this.list[this.index_meu].meu_action
				this.meu_status=this.list[this.index_meu].meu_status
				this.meu_trigger=this.list[this.index_meu].meu_trigger
			},
			HU_moudel(index){
				this.index_hum=index
				if(this.list[this.index_hum].model_list[0].models==""){
					this.list_model[0].models=[]
				}else{
					this.list_model[0].models=this.list[this.index_hum].model_list[0].models
				}
				this.$axios.get(this.Ip+"/HUModelList").then(res=>{
					for(var i=0;i<20;i++){
						this.names.push(res.data.content[i])
					}

				})
				this.HUM_flag = !this.HUM_flag
				this.hum_value=this.list[this.index_hum].hum_value
			},
			other_moudel(index){
				this.index_oth=index
				if(this.list[this.index_oth].model_list.length==2){	
					this.list_model[1].models=this.list[this.index_oth].model_list[1].models
				}else{
					this.list_model[1].models=[];
				}
				
				this.$axios.get(this.Ip+"/HUModelList").then(res=>{
					for(var i=0;i<res.data.content.length;i++){
						this.namess.push(res.data.content[i])
					}
					for(var j=0;j<20;j++){
						this.namess.splice(0,1)	
					}
				})
				this.othm_flag = !this.othm_flag
			},
			edhm_del(index){
				this.list_model[0].models.splice(index,1)				
			},
			edothm_del(index){
				this.list_model[0].models.splice(index,1)	
				
			},
			edhm_add(){
				var model={};
				model=JSON.parse(JSON.stringify(model))
				model.name=""
				model.model_id=""
				model.val=""
				var msg2 =this.list_model[0].models;
				msg2.push(model)
				this.list_model[0].models = [];
				this.list_model[0].models = msg2;
			},
			edoth_add(){
				var models={};
				models=JSON.parse(JSON.stringify(models))
				models.name=""
				models.model_id=""
				models.val=""
				var msg2 =this.list_model[1].models;
				msg2.push(models)
				this.list_model[1].models = [];
				this.list_model[1].models = msg2;
			},
			othm_del(index){
				this.list_model[1].models.splice(index,1)
			},


			humsave(){
				this.HUM_flag = !this.HUM_flag
				this.list[this.index_hum].model_list[0].models=this.list_model[0].models
				for(let i=0;i<this.list[this.index_hum].model_list[0].models.length;i++){
					for(let j=0;j<this.names.length;j++){
						if(this.list[this.index_hum].model_list[0].models[i].name==this.names[j].name){
							this.list[this.index_hum].model_list[0].models[i].model_id=this.names[j].model_id
							break;
						}
					}
				}
			},


			othmsave(){
				this.othm_flag = !this.othm_flag
				if(this.list[this.index_oth].model_list.length==1){
					this.list[this.index_oth].model_list.push({"category":"", "models": []})
					this.list[this.index_hum].model_list[1].models=this.list_model[1].models
				}else{
					this.list[this.index_hum].model_list[1].models=this.list_model[1].models
				}
				for(let i=0;i<this.list[this.index_hum].model_list[1].models.length;i++){
					for(let j=0;j<this.namess.length;j++){
						if(this.list[this.index_hum].model_list[1].models[i].name==this.namess[j].name){
							this.list[this.index_hum].model_list[1].models[i].model_id=this.namess[j].model_id
							break;
						}
					}
				}
			},



			MEU_save(index){
				var patt = /^[\(][0-9][\)]/;
				if(patt.test(this.meu_action)&&patt.test(this.meu_status)){
						
						this.list[this.index_meu].meu_action=this.meu_action
						this.list[this.index_meu].meu_status=this.meu_status
						this.list[this.index_meu].meu_trigger=this.meu_trigger
						if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_action==""){
							this.list[this.index_meu].meu_action="-"
						}

						if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_status==""){
							this.list[this.index_meu].meu_status="-"
						}

						if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_trigger==""){
							this.list[this.index_meu].meu_trigger="-"
						}
						if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_action==""){
							this.list[this.index_meu].meu_action="-"
						}

						if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_status==""){
							this.list[this.index_meu].meu_status="-"
						}

						if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_trigger==""){
							this.list[this.index_meu].meu_trigger="-"
						}
						this.MEU_flag = !this.MEU_flag
				}
				else if((this.meu_action!=""&&this.meu_action=="-")&&(this.meu_status!=""&&this.meu_status=="-")&&(this.meu_trigger!=""&&this.meu_trigger=="-")){
						this.list[this.index_meu].meu_action=this.meu_action
						this.list[this.index_meu].meu_status=this.meu_status
						this.list[this.index_meu].meu_trigger=this.meu_trigger
						if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_action==""){
							this.list[this.index_meu].meu_action="-"
						}

						if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_status==""){
							this.list[this.index_meu].meu_status="-"
						}

						if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_trigger==""){
							this.list[this.index_meu].meu_trigger="-"
						}
						if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_action==""){
							this.list[this.index_meu].meu_action="-"
						}

						if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_status==""){
							this.list[this.index_meu].meu_status="-"
						}

						if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_trigger==""){
							this.list[this.index_meu].meu_trigger="-"
						}
						this.MEU_flag = !this.MEU_flag
				}else if((this.meu_action!=""&&this.meu_action!="-"&&patt.test(this.meu_action))&&(this.meu_status!=""&&this.meu_status=="-")&&(this.meu_trigger!=""&&this.meu_trigger=="-")){
					this.list[this.index_meu].meu_action=this.meu_action
					this.list[this.index_meu].meu_status=this.meu_status
					this.list[this.index_meu].meu_trigger=this.meu_trigger
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					this.MEU_flag = !this.MEU_flag
				}else if((this.meu_action!=""&&this.meu_action=="-")&&(this.meu_status!=""&&this.meu_status!="-"&&patt.test(this.meu_status))&&(this.meu_trigger!=""&&this.meu_trigger=="-")){
					this.list[this.index_meu].meu_action=this.meu_action
					this.list[this.index_meu].meu_status=this.meu_status
					this.list[this.index_meu].meu_trigger=this.meu_trigger
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					this.MEU_flag = !this.MEU_flag
				}else if((this.meu_action!=""&&this.meu_action=="-")&&(this.meu_status!=""&&this.meu_status=="-")&&(this.meu_trigger!=""&&this.meu_trigger!="-"&&patt.test(this.meu_trigger))){
					this.list[this.index_meu].meu_action=this.meu_action
					this.list[this.index_meu].meu_status=this.meu_status
					this.list[this.index_meu].meu_trigger=this.meu_trigger
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					this.MEU_flag = !this.MEU_flag
					
				}else{
					this.$notify({
					  message: '请检查您的信息输入是否追加序号'
					})
				}
			},
			MEU_dele(index){
				this.list[this.index_meu].meu_action='-'
				this.list[this.index_meu].meu_status='-'
				this.list[this.index_meu].meu_trigger='-'


				if(this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
					this.list[this.index_meu].hu_category_id=1
				}else{
					this.list[this.index_meu].hu_category_id=""
				}

				if(this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
					this.list[this.index_meu].hu_category_id=1
				}else{
					this.list[this.index_meu].hu_category_id=""
				}

				if(this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
					this.list[this.index_meu].hu_category_id=1
				}else{
					this.list[this.index_meu].hu_category_id=""
				}
				this.MEU_flag = !this.MEU_flag
			},
			MEU_back(index){
				this.MEU_flag = !this.MEU_flag
			},
			dutyMEU_save(){
				var patt = /^[\(][0-9][\)]/;
				if(patt.test(this.meu_action)&&patt.test(this.meu_status)){
						
						this.list[this.index_meu].meu_action=this.meu_action
						this.list[this.index_meu].meu_status=this.meu_status
						this.list[this.index_meu].meu_trigger=this.meu_trigger
						if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_action==""){
							this.list[this.index_meu].meu_action="-"
						}

						if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_status==""){
							this.list[this.index_meu].meu_status="-"
						}

						if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_trigger==""){
							this.list[this.index_meu].meu_trigger="-"
						}
						if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_action==""){
							this.list[this.index_meu].meu_action="-"
						}

						if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_status==""){
							this.list[this.index_meu].meu_status="-"
						}

						if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_trigger==""){
							this.list[this.index_meu].meu_trigger="-"
						}
						this.dutyshow_flag = !this.dutyshow_flag
				}
				else if((this.meu_action!=""&&this.meu_action=="-")&&(this.meu_status!=""&&this.meu_status=="-")&&(this.meu_trigger!=""&&this.meu_trigger=="-")){
						this.list[this.index_meu].meu_action=this.meu_action
						this.list[this.index_meu].meu_status=this.meu_status
						this.list[this.index_meu].meu_trigger=this.meu_trigger
						if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_action==""){
							this.list[this.index_meu].meu_action="-"
						}

						if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_status==""){
							this.list[this.index_meu].meu_status="-"
						}

						if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
							this.list[this.index_meu].hu_category_id=2
						}else if(this.list[this.index_meu].meu_trigger==""){
							this.list[this.index_meu].meu_trigger="-"
						}
						if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_action==""){
							this.list[this.index_meu].meu_action="-"
						}

						if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_status==""){
							this.list[this.index_meu].meu_status="-"
						}

						if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
							this.list[this.index_meu].hu_category_id=0
						}else if(this.list[this.index_meu].meu_trigger==""){
							this.list[this.index_meu].meu_trigger="-"
						}
						this.dutyshow_flag = !this.dutyshow_flag
				}else if((this.meu_action!=""&&this.meu_action!="-"&&patt.test(this.meu_action))&&(this.meu_status!=""&&this.meu_status=="-")&&(this.meu_trigger!=""&&this.meu_trigger=="-")){
					this.list[this.index_meu].meu_action=this.meu_action
					this.list[this.index_meu].meu_status=this.meu_status
					this.list[this.index_meu].meu_trigger=this.meu_trigger
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					this.dutyshow_flag = !this.dutyshow_flag
				}else if((this.meu_action!=""&&this.meu_action=="-")&&(this.meu_status!=""&&this.meu_status!="-"&&patt.test(this.meu_status))&&(this.meu_trigger!=""&&this.meu_trigger=="-")){
					this.list[this.index_meu].meu_action=this.meu_action
					this.list[this.index_meu].meu_status=this.meu_status
					this.list[this.index_meu].meu_trigger=this.meu_trigger
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					this.dutyshow_flag = !this.dutyshow_flag
				}else if((this.meu_action!=""&&this.meu_action=="-")&&(this.meu_status!=""&&this.meu_status=="-")&&(this.meu_trigger!=""&&this.meu_trigger!="-"&&patt.test(this.meu_trigger))){
					this.list[this.index_meu].meu_action=this.meu_action
					this.list[this.index_meu].meu_status=this.meu_status
					this.list[this.index_meu].meu_trigger=this.meu_trigger
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=2
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					if(this.list[this.index_meu].meu_action!=""&&this.list[this.index_meu].meu_action!="-"&&this.list[this.index_meu].dcu_action!=""&&this.list[this.index_meu].dcu_action!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_action==""){
						this.list[this.index_meu].meu_action="-"
					}

					if(this.list[this.index_meu].meu_status!=""&&this.list[this.index_meu].meu_status!="-"&&this.list[this.index_meu].dcu_status!=""&&this.list[this.index_meu].dcu_status!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_status==""){
						this.list[this.index_meu].meu_status="-"
					}

					if(this.list[this.index_meu].meu_trigger!=""&&this.list[this.index_meu].meu_trigger!="-"&&this.list[this.index_meu].dcu_trigger!=""&&this.list[this.index_meu].dcu_trigger!="-"){
						this.list[this.index_meu].hu_category_id=0
					}else if(this.list[this.index_meu].meu_trigger==""){
						this.list[this.index_meu].meu_trigger="-"
					}
					this.dutyshow_flag = !this.dutyshow_flag
					
				}else{
					this.$notify({
					  message: '请检查您的信息输入是否追加序号'
					})
				}
			},
			dutyMEU_back(){
				this.dutyshow_flag = !this.dutyshow_flag
			},
			literature(index){
				this.literature_index=index;
				this.literature_flag = !this.literature_flag
				this.sys_spec_chapter=this.list[this.literature_index].sys_spec_chapter
				this.common_chapter=this.list[this.literature_index].common_chapter
				this.common_seq_spec=this.list[this.literature_index].common_seq_spec
				this.common_seq_no=this.list[this.literature_index].common_seq_no
				this.common_cmd_guide=this.list[this.literature_index].common_cmd_guide
				this.common_opc=this.list[this.literature_index].common_opc
				this.inter_loc_spec=this.list[this.literature_index].inter_loc_spec
				this.inter_chapter=this.list[this.literature_index].inter_chapter
				this.other_chapter=this.list[this.literature_index].other_chapter
				this.other_doc=this.list[this.literature_index].other_doc
			},
			literaturesave(){
				this.list[this.literature_index].sys_spec_chapter=this.sys_spec_chapter
				this.list[this.literature_index].common_chapter=this.common_chapter
				this.list[this.literature_index].common_seq_spec=this.common_seq_spec
				this.list[this.literature_index].common_seq_no=this.common_seq_no
				this.list[this.literature_index].common_cmd_guide=this.common_cmd_guide
				this.list[this.literature_index].common_opc=this.common_opc
				this.list[this.literature_index].inter_loc_spec=this.inter_loc_spec
				this.list[this.literature_index].inter_chapter=this.inter_chapter
				this.list[this.literature_index].other_chapter=this.other_chapter
				this.list[this.literature_index].other_doc=this.other_doc
				this.literature_flag = !this.literature_flag
			},
			itp_blur(index){
				var state_= this
				if(this.list[index].hu_category_id!=""){
					if(this.list[index].hu_category_id==0){
						this.$confirm('确定将状态ID更新为0吗？', '提示', {
						          confirmButtonText: '确定',
						          cancelButtonText: '取消',
						          type: 'warning'
						        }).then(() => {
						          state_.list[index].hu_category_id=0
						          this.$notify({
						            message: '更新成功'
						          });
						        }).catch(() => {
									  state_.list[index].hu_category_id=""      
						        });
					}
					if(this.list[index].hu_category_id==3){
						this.$confirm('确定将状态ID更新为3吗？', '提示', {
						          confirmButtonText: '确定',
						          cancelButtonText: '取消',
						          type: 'warning'
						        }).then(() => {
						          state_.list[index].hu_category_id=3   
						        

						          this.list[this.index_meu].meu_trigger ="(DCUと同様)"
						          this.list[this.index_meu].meu_action ="(DCUと同様)"
						          this.list[this.index_meu].meu_status ="(DCUと同様)"
						          this.$notify({
						            message: '更新成功'
						          });
						        }).catch(() => {
									  state_.list[index].hu_category_id=""     
						  });
					}
				}
			},
			ach(index){

					this.$confirm('确定完成吗？', '提示', {
				          confirmButtonText: '确定',
				          cancelButtonText: '取消',
				          type: 'warning'
				      }).then(() => {
				      	if(this.list[index].complete_flag == 1){
				      		this.list[index].complete_flag = 0
				      	}else{
				      		this.list[index].complete_flag = 1;
				      	}   		
				          this.$notify({
				            message: '成功完成'
				          });
				        }).catch(() => {
							this.$notify({
							  message: '取消完成'
						});      
					});	
				
			},
			translate(index){
				if(this.re_g!=""&&this.mo_g!=""&&this.re_s!=""&&this.mo_s!=""&&this.mn_m!=""&&this.mn_g!=""&&this.mo_a!=""&&this.re_a!=""){
					if((this.re_g==1&&this.mo_g==1&&this.re_s==1&&this.mo_s==1&&this.mn_m==1&&this.mn_g==1&&this.mo_a==1&&this.re_a==1)||
					(this.re_g==1&&this.mo_g==1&&this.re_s==1&&this.mo_s==1&&this.mn_m==1&&this.mn_g==0&&this.mo_a==0&&this.re_a==0)){
							this.$confirm('确定翻译吗？', '提示', {
						          confirmButtonText: '确定',
						          cancelButtonText: '取消',
						          type: 'warning'
							    }).then(() => {
							    		if(this.list[index].translation_flag == 1){
							    			this.list[index].translation_flag = 0
							    		}else{
							    			this.list[index].translation_flag = 1
							    		}						        	
							          	this.$notify({
							            	message: '更改成功'
							          	});
			
							       }).catch(() => {
										this.$notify({
										  message: '取消翻译'
									});      
							});
					}else{
						this.$notify({
							  message: '您无权限操作'
						})
					}
				}
			},
			recognize(index){
				if(this.re_g!=""&&this.mo_g!=""&&this.re_s!=""&&this.mo_s!=""&&this.mn_m!=""&&this.mn_g!=""&&this.mo_a!=""&&this.re_a!=""){
					if((this.re_g==1&&this.mo_g==1&&this.re_s==1&&this.mo_s==1&&this.mn_m==1&&this.mn_g==1&&this.mo_a==1&&this.re_a==1)||
					(this.re_g==1&&this.mo_g==1&&this.re_s==1&&this.mo_s==1&&this.mn_m==1&&this.mn_g==0&&this.mo_a==0&&this.re_a==0)){
						this.$confirm('确定更改承认状态？', '提示', {
						          confirmButtonText: '确定',
						          cancelButtonText: '取消',
						          type: 'warning'
						       }).then(() => {
						       	if(this.list[index].agree_flag == 1){
						       		this.list[index].agree_flag = 0
						       	}else{
						       		this.list[index].agree_flag = 1
						       	}	
					          	this.$notify({
					            	message: '更改成功'
					          	}); 	
						        }).catch(() => {
									this.$notify({
									  message: '更改取消'
								});      
						});
					}else{
						this.$notify({
							  message: '您无权限操作'
						})
					}
				}	
			},
			zhizhai(index){
				if(this.re_g!=""&&this.mo_g!=""&&this.re_s!=""&&this.mo_s!=""&&this.mn_m!=""&&this.mn_g!=""&&this.mo_a!=""&&this.re_a!=""){
					if((this.re_g==1&&this.mo_g==1&&this.re_s==1&&this.mo_s==1&&this.mn_m==1&&this.mn_g==1&&this.mo_a==1&&this.re_a==1)||
					(this.re_g==1&&this.mo_g==1&&this.re_s==1&&this.mo_s==1&&this.mn_m==1&&this.mn_g==0&&this.mo_a==0&&this.re_a==0)){
						this.$confirm('确定更改指摘状态吗？', '提示', {
					          confirmButtonText: '确定',
					          cancelButtonText: '取消',
					          type: 'warning'
					      }).then(() => {
					      	if(this.list[index].has_problem == 1){
					      		this.list[index].has_problem = 0
					      	}else{
					      		this.list[index].has_problem = 1
					      	} 	
					          this.$notify({
					            message: '指摘更改成功'
					          });     
					        }).catch(() => {
								this.$notify({
								  message: '取消更改'
							});      
						});
					}else{
						this.$notify({
							  message: '您无权限操作'
						}) 
					}
				}
			},
			back(){
				this.$router.go(-1)
			},
			save_back(){
				this.$axios.post(this.Ip+'/HUContent',this.list)
					.then(res => {
						this.$notify({
						  message: '保存成功!'
						});
					})
				this.$router.go(-1)
			},
			add(){
				var item={};
				item=JSON.parse(JSON.stringify(item))
				item.dcu_action="-"
				item.arl_id=this.$route.params.ARL_id
				item.dcu_status="-"
				item.dcu_trigger="-"
				item.meu_action="-"
				item.meu_status="-"
				item.meu_trigger="-"
				item.common_chapter="未確認"
				item.common_cmd_guide="未確認"
				item.common_opc="未確認"
				item.common_seq_no="未確認"
				item.common_seq_spec="未確認"
				item.inter_chapter="未確認"
				item.inter_loc_spec="未確認"
				item.sys_spec_chapter="未確認"
				item.system_conf=""
				item.amp="0"
				item.dsrc="0"
				item.dcm="0"
				item.rse="0"
				item.touch_pad="0"
				item.separate_disp="0"
				item.hu_category_id=""
				item.rel_requirement=""
				item.remark="-"
				item.complete_flag = 0
				item.translation_flag = 0	
				item.agree_flag = 0
				item.has_problem = 0 
				item.hu_record_id=0
				item.model_list=[{"category":"", "models": []},{"category":"", "models": []}]
				item.list_model=[{"category":"", "models": []},{"category":"", "models": []}]
				var msg =this.list;
				msg.push(item)
				this.list = [];
				this.list = msg;
				this.$message('添加ユニークID'+(this.list.length-1)+'成功');
			},
			save(){
				this.$axios.post(this.Ip+'/HUContent',this.list)
					.then(res => {
						this.$notify({
						  message: '保存成功!'
						});	
					})
			},
			examine_hu(){
				this.$router.push({name: 'HU',params:{HU_id: this.hdata}})
			},
			tiem(index){
				this.new_Date_num = index
				this.new_Date = this.list[this.new_Date_num].new_date
				this.tiem_flag=!this.tiem_flag
			},
			save_time(index){
				this.list[this.new_Date_num].new_date = this.new_Date
				this.tiem_flag=!this.tiem_flag
			},
			setEndDate(val){
				this.new_Date = val
			},
			change_reason(index){
				this.change_flag = !this.change_flag 
				this.change_index=index;
				this.change_content=this.list[this.change_index].reason
				
			},
			change_save(){
				this.change_flag = !this.change_flag 
				this.list[this.change_index].reason=this.change_content
			},
			dutyshow(index){
				this.index=index
				this.dcu_action=this.list[index].dcu_action
				this.dcu_status=this.list[index].dcu_status
				this.dcu_trigger=this.list[index].dcu_trigger
				this.index_meu=index
				this.meu_action=this.list[this.index_meu].meu_action
				this.meu_status=this.list[this.index_meu].meu_status
				this.meu_trigger=this.list[this.index_meu].meu_trigger
				this.dutyshow_flag=!this.dutyshow_flag
			},
			pd(){
				if(this.value2=='DCU'){
					this.dcu_show=true
					this.meu_show=false
					this.options2[0].disabled=true
					this.options2[1].disabled=false
				}
				if(this.value2=='MEU'){
					this.meu_show=true
					this.dcu_show=false
					this.options2[1].disabled=true
					this.options2[0].disabled=false
				}
			},
			replace(index){
				if(this.list[index].rel_requirement!=null&&this.list[index].rel_requirement!=""){
					this.list[index].rel_requirement.replace(/\*/g,"※")
				}
			},
			option_change(index){
				//如果this.option_data[index] == '111111'时，触发请求判断
//				if(this.option_data[index] == '111111'){
//					//循环判断是否有符合的值
////					for(var i=0;i<this.HuOption.length;i++){
////						if(this.HuOption[i] == ){
////							
////						}else{
////							//如果没有，就初始化 ？？？？？？？？？
////						}
////					}
//				}else{
//					//如果this.option_data[index] == '111111'时，不触发请求判断
//					if(){
//						//判断6个点击按钮是否全部点击，如果全部点击,触发请求
//						//判断是不是点击同一个按钮
//						
//					}else{
//						//判断6个点击按钮是否全部点击，如果没有全部点击,this.option_data[index] += '1'
//						this.option_data[index] += '1';
//					}
//				}
				if(this.option_data == '111111'){
					var number_team = this.list[index].amp+','+this.list[index].dsrc+','+this.list[index].dcm+','+this.list[index].rse+ ','+this.list[index].touch_pad+','+this.list[index].separate_disp
					var node_data = this.HuOption[this.list[index].amp+','+this.list[index].dsrc+','+this.list[index].dcm+','+this.list[index].rse+ ','+this.list[index].touch_pad+','+this.list[index].separate_disp];
					if(node_data != undefined){
						switch (number_team){
							case "1,1,1,1,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,1,1,1,1,2":this.list[index].system_conf = "1:JPE2,NAE2,EUE2,GEE2";
								break;
							case "1,1,1,1,2,2":this.list[index].system_conf = "2:JPL2,NAL2,EUL2,GEL2,CHL2";
								break;
							case "1,1,1,2,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,1,1,2,1,2":this.list[index].system_conf = "1:JPE2,NAE2,EUE2,GEE2";
								break;	
							case "1,1,1,2,2,2":this.list[index].system_conf = "2:JPL2,NAL2,EUL2,GEL2,CHL2";
								break;
							case "1,1,2,1,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,1,2,1,1,2":this.list[index].system_conf = "1:JPE2,NAE2,EUE2,GEE2";
								break;
							case "1,1,2,1,2,2":this.list[index].system_conf = "2:JPL2,NAL2,EUL2,GEL2,CHL2";
								break;
							case "1,1,2,2,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,1,2,2,1,2":this.list[index].system_conf = "1:JPE2,NAE2,EUE2,GEE2";
								break;
							case "1,1,2,2,2,2":this.list[index].system_conf = "2:JPL2";
								break;
							case "1,2,1,1,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,2,1,1,1,2":this.list[index].system_conf = "1:JPE2";
								break;
							case "1,2,1,1,2,2":this.list[index].system_conf = "2:JPL2";
								break;
							case "1,2,1,2,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,2,1,2,1,2":this.list[index].system_conf = "1:JPE2";
								break;
							case "1,2,1,2,2,2":this.list[index].system_conf = "2:JPL2";
								break;
							case "1,2,2,1,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,2,2,1,1,2":this.list[index].system_conf = "1:JPE2";
								break;
							case "1,2,2,1,2,2":this.list[index].system_conf = "2:JPL2";
								break;
							case "1,2,2,2,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,2,2,2,1,2":this.list[index].system_conf = "1:JPE2";
								break;
							case "1,2,2,2,2,2":this.list[index].system_conf = "2:JPL2";
								break;
							case "1,3,1,1,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,3,1,1,1,2":this.list[index].system_conf = "1:JPE2";
								break;	
							case "1,3,1,2,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,3,1,2,1,2":this.list[index].system_conf = "1:JPE2";
								break;
							case "1,3,2,1,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,3,2,1,1,2":this.list[index].system_conf = "1:JPE2";
								break;
							case "1,3,2,2,1,1":this.list[index].system_conf = "14:JPE1";
								break;
							case "1,3,2,2,1,2":this.list[index].system_conf = "1:JPE2";
								break;
							case "2,1,1,1,1,1":this.list[index].system_conf = "4:NAT2,EUT2,GET2,CHT2,NAT1,EUT1,GET1,CHT1,OTHT1,NAT0";
								break;
							case "2,1,1,1,2,2":this.list[index].system_conf = "16:NA\uff2c1,EULS,EUL1,CHLS,GEL1,CHL1";
								break;
							case "2,1,1,3,1,1":this.list[index].system_conf = "4:NAT2,EUT2,GET2,CHT2,NAT1,EUT1,GET1,CHT1,OTHT1,NAT0";
								break;
							case "2,1,2,1,1,1":this.list[index].system_conf = "4:NAT2,EUT2,GET2,CHT2,NAT1,EUT1,GET1,CHT1,OTHT1";
								break;
							case "2,1,2,1,2,2":this.list[index].system_conf = "16:NA\uff2c1,EULS,EUL1,CHLS,GEL1,CHL1";
								break;
							case "2,1,2,3,1,1":this.list[index].system_conf = "4:NAT2,EUT2,GET2,CHT2,NAT1,EUT1,GET1,CHT1,OTHT1";
								break;
							case "3,1,1,1,1,1":this.list[index].system_conf = "4:NAT2,EUT2,GET2,CHT2,NAT1,EUT1,GET1,CHT1,OTHT1,NAT0";
								break;
							case "3,1,1,1,2,2":this.list[index].system_conf = "16:NA\uff2c1,EULS,EUL1,CHLS,GEL1,CHL1";
								break;
							case "3,1,1,3,1,1":this.list[index].system_conf = "4:NAT2,EUT2,GET2,CHT2,NAT1,EUT1,GET1,CHT1,OTHT1,NAT0";
								break;
							case "3,1,2,1,1,1":this.list[index].system_conf = "4:NAT2,EUT2,GET2,CHT2,NAT1,EUT1,GET1,CHT1,OTHT1";
								break;
							case "3,1,2,1,2,2":this.list[index].system_conf = "16:NA\uff2c1,EULS,EUL1,CHLS,GEL1,CHL1";
								break;
							case "3,1,2,3,1,1":this.list[index].system_conf = "4:NAT2,EUT2,GET2,CHT2,NAT1,EUT1,GET1,CHT1,OTHT1";
								break;								
							default:
								break;
						}
					}
				}else{
					
				}
			}
		}
	}
</script>

<style spoced>
	*{
		margin: 0;
		padding: 0;
	}
	.fl{
		float: left;
	}
	.fr{
		float: right;
	}
	a{
		text-decoration: none;
	}
	ul,li{
		list-style: none;
	}
	html,body{
		font-size:14px;
		font-family: "微软雅黑";
		color: #1f2d3d;
	}
	#myWorkChildren2{
		position: absolute;
		width: 100%;
		height: 100%;
		overflow: scroll;
	}
	.Asa_content{
		width:98%;
		box-shadow: 2px 1px 9px #ccc;
		height:300px;
		margin: 0 auto;
		margin-top: 20px;
	}
	#Asa_body{
		width: 100%;
		margin-top: 260px;
		margin-bottom:60px;
	}
	.Asa_arl{
		width:18%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_Hu{
		width:9%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_option,.Asa_relevance,.Asa_moudel{
		width:16%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_duty{
		width:22%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_remark{
		width:10%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_remark_2{
		width:12%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_dele{
		width:11%;
		height:300px;
	}
	.arl_size{
		text-align: center;
		width: 100%;
		height:50px;
		line-height: 50px;
		background: rgb(231,231,231);
		border-bottom: 1px solid #dfe6ec;
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 3;
		overflow: hidden;
	}
    .Asa_content .arl_btn{
		display: block;
		margin: 0 auto;
		margin-top: 30px;
	}
    .option_size {
	    width: 100%;
	    text-align: center;
	    height: 31px;
	    line-height: 31px;
	    border-bottom: 1px solid #dfe6ec;
	    display: -webkit-box;
	    display: -ms-flexbox;
	    display: flex;
	}
	.option_size_id {
	    width: 100%;
	    text-align: center;
	    height: 62px;
	    line-height: 62px;
	    border-bottom: 1px solid #dfe6ec;
	    display: -webkit-box;
	    display: -ms-flexbox;
	    display: flex;
	}
    .option_title {
	    color: #ccc;
	    -webkit-box-flex: 3; 
	    -ms-flex: 3;
	    flex: 3; 
	    width: 60%;
	}
	.option_title_id{
		color: #ccc;
	    -webkit-box-flex: 1; 
	    -ms-flex: 1;
	    flex: 1; 
	    width: 30%;
	    overflow: hidden;
	    text-overflow:ellipsis;
	    white-space: nowrap;
	}
	.option_content{
	 	color: #999
	}
	.option_last{
		border: 0 none;
	}
  .HU_id{
  	text-align: center;
  	margin-top: 30px;
  	color: #333;
  }
  .Hu_Id{
  	display: block;
  	text-align: center;
  	margin-top: 30px;
  	color: #666
  }    
  .HU_size{
  	display: -webkit-box;
  	-webkit-box-orient: vertical;
  	-webkit-line-clamp: 3;
  	overflow: hidden;
  }
  .Asa_btutton{
  	height: 60px;
  	
	position: fixed;
	bottom: 0;
  	left: 300px;
	right: 0;
	background-color: white;
  }
 .Asa_dele .operation_btn,.Asa_remark .operation_btn,.Asa_duty .operation_btn{
  	display: block;
  	margin: 0 auto;
  	margin-top: 10px;
  }
  .save{
	margin-top: 22px;
	margin-bottom:15px;
  }

  .duty_Id{
  	width: 100%;
  	text-align: center;
  	display: block;
  	margin-top: 20px;
  	color: #666
  }
  .DCU_ipt,.MEU_ipt{
  	margin-top:10px;
  }
  .DCU_btn .operation_btn,.MEU_btn .operation_btn{
  	display: block;
  	margin: 10px 0 10px 10px;
  }
  .opt_ipt {
	    position: relative;
	    font-size: 14px;
	    width: 40%;
	}
	.opt_ipt  .el-input__inner {
	    height: 31px;
	    text-align: center;
	}
	.opt_ipt_id {
	    -webkit-box-flex: 3;
	    -ms-flex: 3;
	    flex: 3;
	    width: 70%;
	}
	
	.opt_line{
		line-height: 15px;
	}
	.relevance_size {
	    width: 100%;
	    text-align: center;
	    height: 31px;
	    justify-content: center;
	    line-height: 31px;
	    border-bottom: 1px solid #dfe6ec;
	    display: -webkit-box;
	    display: -ms-flexbox;
	    display: flex;
	}
	.relevance_size .el-input__inner{
	    height: 31px;
	}
	.opt_ipt_id .el-textarea__inner {
		/*height: 62px;*/
	}
	.rel_ipt {
	    -webkit-box-flex: 19;
	    -ms-flex: 4;
	    flex: 19;
	}
	.rel_btn {
	   display: block;
	   margin: 0 auto;
	   margin-top: 12px;
	}
	.arl_over{
		height: 248px;
		overflow: auto;
		border: none;
	}
	.arl_over .el-collapse-item__header {
	    height: 31px;
	    line-height: 31px;
	    padding-left: 2px;
	    font-size: 13px;
	    letter-spacing: -1px;
	}
	.arl_over .el-collapse-item__content {
	    padding: 5px 8px;
	    font-size: 12px;
	}
	/*.arl_over> el-collapse-item >div:nth-child(odd) {
		background-color: #EFF2F7;
	}*/
	.arl_over .el_none .el-collapse-item__header {
		display: none;
	}
	.arl_over .el-collapse-item__header__arrow {
	    margin-right: 2px;
	}
	h5{
		width: 100%;
		margin-top: 20px;
	}
	.el-dialog--small{
		width: 80%;
	}
	#myWorkChildren2 .el_c .el-dialog--small{
		width: 57.6%;
	}
	#myWorkChildren2 .ed_hm .el-dialog--small{
		height: auto;

	}
	.ARL_msg{
		margin: 5px 0 0 5px;
		font-size: 12px;
		height: 16px;
		overflow: hidden;
		text-overflow:ellipsis;
		white-space: nowrap;
	}
	.ARL_msg_title{
		font-weight: bold;
	}
	.append_dcu_meu{
		width: 100%;
		text-align: center;
		margin-top: 10px;
		color: #4db3ff
	}
	.el-icon-plus{
		font-size: 17px;
		cursor: pointer;
	}
	.select_ipt{
		margin-top: 30px;
	}
	.top_panel{
		position: fixed;
		left: 300px;
		top: 60px;
		right: 0;
		height: 10px;
		z-index: 99990;
		background-color: rgb(243,243,243);
	}
	#ARLFix{
  		position: fixed;
		left: 300px;
		right: 0;
  		height: 250px;
  		z-index: 99;
  		border: double 5px black;	
  		top: 70px;	
	}
	#ARLFix p{
		text-align: center;
		font-size: 30px;
		background-color: white;
	}
	.el-table .info-row{
		background: #c9e5f5;
	}
	.HUM{
		width:100%;
		margin-top: 30px;
		border:1px solid #dfe6ec;
		height: 96px;
	}
	.HUM_name,.HUM_textar{
		width: 40%;
		border: 1px solid #dfe6ec;
		border-bottom:0 none;
		
	}
	.HUM_caozuo{
		width: 20%
	}
	.HUM_title{
		background:#eef1f6;
		padding:8px;
		/*text-align: center;*/
		font-size: 14px;
		color: #1f2d3d
	}
	.HUM_span{
		padding-left: 10px;
	}
	.HUM_content{
		height:60px;
	}
	.Asa_dele .operation_btn, .Asa_remark .operation_btn, .Asa_duty .operation_btn{
		margin-top: 6px;
	}
	.HUM_content_select{
		margin-top: 12px;
		margin-left: 10px;
	}
</style>
