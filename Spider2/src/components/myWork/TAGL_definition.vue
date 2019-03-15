<template>
	<div id="myWorkChildren2">
		<div id='ARLFix'>
			<p>ARLから転記</p>
			<el-table :data="TAGL_arlc_Data" border  height='200' >
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
		<div id="TAGL_Header_fixed">
				<div class="Asa_content_tagl" v-for="(item,index) in list">
				<!-- 查看ARL -->
				<div class="Asa_arl_tagl fl">
					<h4 class="arl_size" title="ARL要件转记">H/U要件定義</h4>
					<!--<p class="ARL_msg"><span class="ARL_msg_title">HU-ID:</span><span>{{arlc_Data[0].hu_id}}</span></p>-->
					<p class="ARL_msg"><span class="ARL_msg_title">HU-ID:</span><span>{{list[0].hu_def_id}}</span></p>
					<el-button type="text" size="small" class="arl_btn" @click="examine_hu(index)">查看</el-button>
				</div>
				<!-- HU -->
				<div class="Asa_Hu_tagl fl">
					<h4 class="arl_size" title="HU_unique_ID">unique_ID</h4>
					<span class="Hu_Id"><span class="HU_size" >{{index}}</span></span>
				</div>
				<!-- 模块 -->
				<div class="Asa_moudel_tagl fl">
					<h4 class="arl_size" title="TAGL-PF">TAGL-PF</h4>
					<p class="tagl_msg">
						<el-input  class="opt_ipt2" :rows="1" value="DCU/MEU" v-model="list[index].dcu_meu"></el-input>
					</p>
					<p class="tagl_msg">
						<span>状态:</span>
						<el-input type="textarea" class="opt_ipt2" :rows="1" v-model="list[index].pf_status"></el-input>
					</p>
					<p class="tagl_msg">
						<span>トリガー ::</span>
						<el-input type="textarea" class="opt_ipt2" :rows="1" v-model="list[index].pf_trigger"></el-input>
					</p>
					<p class="tagl_msg">
						<span>動作:</span>
						<el-input type="textarea" class="opt_ipt2" :rows="1" v-model="list[index].pf_action"></el-input>
					</p>
				</div>
				<!-- 责任分担 -->
				<div class="Asa_duty_tagl fl">
					<h4 class="arl_size" title="责任分担">责任分担</h4>
					<el-button type="text" size="small" class="operation_btn" @click="examine(index)">查看Model_list</el-button>
				</div>
				
				<!-- 备考 -->
				<div class="Asa_remark_tagl fl">
					<h4 class="arl_size" title="备注">其他</h4>
					<el-button type="text" size="small" class="operation_btn" @click="texTarea(index)">備考</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="literature(index)">責務分担の特記事項</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="Unrequire(index)">未要件分析</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="tiem(index)">日付</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="change_reason(index)">更改理由</el-button>
				</div>
				<!-- delete -->
				<div class="Asa_dele_tagl fl">
					<h4 class="arl_size" title="操作">操作</h4>
					<el-button type="text" size="small" class="operation_btn" @click="copy(index)">复制添加</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="Delete()">删除</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="Up(index)">上移动</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="Down(index)">下移动</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="ach(index)" v-if="list[index].complete_flag ==1">已完成</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="ach(index)" v-else>完成</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="translate(index)" v-if="list[index].translation_flag ==1">已翻译</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="translate(index)" v-else>翻译</el-button>
					<el-button type="text" size="small" class="operation_btn" @click="recognize(index)" v-if="list[index].agree_flag ==1">已承认</el-button>
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

		<el-dialog title="Model_list" :visible.sync="DCU_flag" :modal-append-to-body="false">
			<el-table :data="TAGL_arlc_Data" border  height='200' >
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
			<div class="HUM" v-for="(item2,index) in list_model">
				<div class="HUM_name fl" >
					<h3 class="HUM_title">
						<span class="HUM_span">部品</span>
					</h3>
					<div class="HUM_content">
						<el-select v-model="item2.title" placeholder="请选择">
					           <el-option 
					           v-for="name in namesss" 
					           :label="name.title" 
					           :value="name.title"
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
					    <el-button type="primary" class="rel_btn" @click="edothm_del()">-</el-button>
					</div>
				</div>
			</div>
			<el-button class="save fr" @click="dutyhumsave()">保存</el-button>
			<el-button class="save fr" @click="edhm_add(index)" style="margin-right: 15px;">添加</el-button>
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
				<el-button  size="small" class="operation_btn fr" @click='MEU_dele()'>删除</el-button>
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
		<el-dialog title="責務分担の特記事項" :visible.sync="literature_flag" :modal-append-to-body="false" >
			<el-input
			  type="textarea" :rows="10" placeholder="请输入内容"
			  v-model="val_literature">
			</el-input>
			<el-button class="save fr" @click="literaturesave()">保存</el-button>
		</el-dialog>
		<el-dialog title="未要件分析" :visible.sync="unrequire_flag" :modal-append-to-body="false" >
			<el-input
			  type="textarea" :rows="10" placeholder="请输入内容"
			  v-model="unrequire">
			</el-input>
			<el-button class="save fr" @click="unrequiresave()">保存</el-button>
		</el-dialog>

		<el-dialog title="H/U以外のＭＭ部品" :visible.sync="HU_moudel" class="ed_hm" :modal-append-to-body="false">
			 <el-table :data="HUm_Data" border style="width: 100%; margin: auto;" max-height="250">
			    <el-table-column fixed prop="hu_key" label="hu_key" width="200">
			    </el-table-column>
			    <el-table-column prop="hu_value" label="hu_value" width="601">
			       <template scope="scope">
			       <el-input placeholder="请输入内容"></el-input>
			      </template>
			    </el-table-column>
			    <el-table-column fixed="right" label="移除" width="100">
			      <template scope="scope">
			      	<el-button type="primary" class="rel_btn" @click="edhm_del(index)">-</el-button> 
			      </template>
			    </el-table-column>
			  </el-table>
			  <el-button class="save fr" @click="humsave()">保存</el-button>
		</el-dialog>
		<el-dialog title="H/U以外のＭＭ部品" :visible.sync="other_moudel" class="ed_hm"  :modal-append-to-body="false">
			 <el-table :data="otherm_Data" border style="width: 100%; margin: auto;" max-height="250">
			    <el-table-column fixed prop="other_key" label="other_key" width="200">
			    </el-table-column>
			    <el-table-column prop="other_value" label="other_value" width="601">
			       <template scope="scope">
			       <el-input placeholder="请输入内容"></el-input>
			      </template>
			    </el-table-column>
			    <el-table-column fixed="right" label="移除" width="100">
			      <template scope="scope">
			      	<el-button type="primary" class="rel_btn" @click="edothm_del(index)">-</el-button> 
			      </template>
			    </el-table-column>
			  </el-table>
			  <el-button class="save fr" @click="othmsave()">保存</el-button>
		</el-dialog>
		<el-dialog title="日付" :visible.sync="tiem_flag" class="ed_hm"  :modal-append-to-body="false">
		  <template>
		 	<el-date-picker v-model="value2" type="date" placeholder="选择日期" :picker-options="pickerOptions1" @change="setEndDate">
		 	 </el-date-picker>
		  </template>
		  <el-button class="save fr" @click="save_date()">保存</el-button>
		</el-dialog>
		<el-dialog title="变更理由" :visible.sync="change_flag" class="ed_hm"  :modal-append-to-body="false">
		  <el-input
		    type="textarea" :rows="10" placeholder="请输入内容"
		    v-model="reason">
		  </el-input>
		  <el-button class="save fr" @click="save_reason()">保存</el-button>
		</el-dialog>
	</div>
</template>

<script>
	export default{
		data(){
			return{
				model_list:[
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                "", 
			                ""
			            ],
				reason: '',
				index_reason: 0,
				examine_index: 0,
				val_literature: '',
				change_content:'',
				unrequire:'',
				unrequire_flag: false,
				change_flag:false,
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
				tiem_flag:false,
				change_flag:false,
				flag:false,
				DCU_flag:false,
				MEU_flag:false,
				MEU_disabled:true,
				dcu_action:"",
				dcu_status:'',
				dcu_trigger:'',
				index:0,
				index_meu:0,
				index_tiem: 0,
				meu_action:'',
				meu_status:'',
				meu_trigger:'',
				texTarea_index:0,
				Unrequire_index:0,
				remark:'',
				rels:[
					 { text: '' }
				],
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
				tdata:'',
				arlc_Data: [{
					arl_id:'',
					small_category:'',
					detail:'',
					from_info:'',
					status:'',
					trigger:'',
					action:''
				}],
				TAGL_arlc_Data: [{
					arl_id:'',
					small_category:'',
					detail:'',
					from_info:'',
					status:'',
					trigger:'',
					action:''
				}],
		        HU_moudel: false,
		        other_moudel: false,
		        HUm_Data: [{
		          hu_key: '01.遠隔ディスプレイ(WVGA Display)',
		          hu_value: ''
		        },
		        {
		          hu_key: '02.Remote Touch I/F',
		          hu_value: ''
		        },
		        {
		          hu_key: '03.Satellite SW',
		          hu_value: ''
		        },
		        {
		          hu_key: '04.DCM',
		          hu_value: ''
		        },
		        {
		          hu_key: '05.Microphone',
		          hu_value: ''
		        },
		        {
		          hu_key: '06.Step1 AMP',
		          hu_value: ''
		        },
		        {
		          hu_key: '07.Step3 AMP',
		          hu_value: ''
		        },
		        {
		          hu_key: '08 SP',
		          hu_value: ''
		        },
		        {
		          hu_key: '09.RSE',
		          hu_value: ''
		        },
		        {
		          hu_key: '10.I/F BOX',
		          hu_value: ''
		        },	
		        {
		          hu_key: '11. USB Adapter',
		          hu_value: ''
		        },
		        {
		          hu_key: '12Radio ANT',
		          hu_value: ''
		        },
		        {
		          hu_key: '13XM ANT',
		          hu_value: ''
		        },
		        {
		          hu_key: '14DAB ANT',
		          hu_value: ''
		        },
		        {
		          hu_key: '15.DTV ANT',
		          hu_value: ''
		        },
		        {
		          hu_key: '16.GPS ANT',
		          hu_value: ''
		        },
		        {
		          hu_key: '17. DSRC/ETC',
		          hu_value: ''
		        },
		        {
		          hu_key: '18. Clock',
		          hu_value: ''
		        },
		        {
		          hu_key: '19. Rear Controller',
		          hu_value: ''
		        },
		        {
		          hu_key: '20. ITS-ECU',
		          hu_value: ''
		        }],
		        otherm_Data:[{
		            other_key: '20. Meter',
		          	other_value: ''
		        },{
		            other_key: '21. HUD',
		          	other_value: ''
		        },{
		            other_key: '22. Steering Swith',
		          	other_value: ''
		        },{
		            other_key: '23. Rear Camera',
		          	other_value: ''
		        },{
		            other_key: '24. Camera ECU',
		          	other_value: ''
		        },{
		            other_key: '25. Clock',
		          	other_value: ''
		        },{
		            other_key: '26 Body ECU',
		          	other_value: ''
		        },{
		            other_key: '27. Air Controller',
		          	other_value: ''
		        }],
			ARL_id: '',
			namesss:[],
			list_model:[]
			}
		},
		created:function(){
					if(typeof(this.$route.params.HU_id) == 'string'){
						window.sessionStorage.setItem('TAGL',this.$route.params.HU_id)
						this.$axios.get(this.Ip+'/HuSubDef/'+window.sessionStorage.getItem('TAGL'))
							.then(res => {
								this.list=res.data.content;
								if(this.list!=""){
									this.tdata=this.list[0].definition_id;
								}
								
							})
						this.$axios.get(this.Ip+'/ARLContent/'+window.sessionStorage.getItem('sion_Id'))
							.then(res => {
								this.TAGL_arlc_Data[0].arl_id=res.data.content.arl_id
								this.TAGL_arlc_Data[0].detail=res.data.content.detail
								this.TAGL_arlc_Data[0].from_info=res.data.content.from_info
								this.TAGL_arlc_Data[0].memo=res.data.content.memo
								this.TAGL_arlc_Data[0].status=res.data.content.status
								this.TAGL_arlc_Data[0].trigger=res.data.content.trigger
								this.TAGL_arlc_Data[0].action=res.data.content.action
						})
					}
					else{
						this.$axios.get(this.Ip+'/HuSubDef/'+window.sessionStorage.getItem('TAGL'))
							.then(res => {
								this.list=res.data.content;

								if(this.list!=""){
									this.tdata=this.list[0].definition_id;
								}
							})
						this.$axios.get(this.Ip+'/ARLContent/'+window.sessionStorage.getItem('sion_Id'))
							.then(res => {
								this.TAGL_arlc_Data[0].arl_id=res.data.content.arl_id
								this.TAGL_arlc_Data[0].detail=res.data.content.detail
								this.TAGL_arlc_Data[0].from_info=res.data.content.from_info
								this.TAGL_arlc_Data[0].memo=res.data.content.memo
								this.TAGL_arlc_Data[0].status=res.data.content.status
								this.TAGL_arlc_Data[0].trigger=res.data.content.trigger
								this.TAGL_arlc_Data[0].action=res.data.content.action
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
				        	message: '上移成功!'
				        });	        
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
				        	message: '下移成功!'
				        });
					}
				}
			},
			edhm_del:function(index, rows){
				this.HUm_Data.splice(index, 1);
			},
			edothm_del:function(index, rows){
				this.otherm_Data.splice(index, 1);
			},
			copy:function(index){
				var item=[];
				item=this.list[index];
				item=JSON.parse(JSON.stringify(item))
				var msg =this.list;
				msg.push(item)
				this.list = [];
				this.list = msg;
				this.$message('添加成功');
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
			Unrequire(index){
				this.Unrequire_index=index
				this.unrequire=this.list[this.Unrequire_index].unrequire
				this.unrequire_flag = !this.unrequire_flag;
			},
			unrequiresave(){
				this.list[this.Unrequire_index].unrequire=this.unrequire
				this.unrequire_flag = !this.unrequire_flag;
			},
			save_date(){
				this.list[this.index_tiem].new_date = this.value2
				this.tiem_flag=!this.tiem_flag
			},
			setEndDate(val){
				this.new_Date = val
			},
			save_reason(){
				this.list[this.index_reason].reason = this.reason
				this.change_flag = !this.change_flag
			},
			examine(index){
				this.examine_index=index
				this.DCU_flag = !this.DCU_flag
				this.list_model=this.list[this.examine_index].model_list
			
				this.$axios.get(this.Ip+"/DEFModelList").then(res=>{
					for(var i=0;i<res.data.content.length;i++){
						this.namesss.push(res.data.content[i])
					}

				})

			},

			examine_MEU(index){
				this.index_meu=index
				this.MEU_flag = !this.MEU_flag
				this.meu_action=this.list[this.index_meu].meu_action
				this.meu_status=this.list[this.index_meu].meu_status
				this.meu_trigger=this.list[this.index_meu].meu_trigger
			},

			tiem(index){
				this.index_tiem=index
				this.tiem_flag=!this.tiem_flag
				this.value2 = this.list[this.index_meu=index].new_date
			},
			change_reason(index){
				this.index_reason= index
				this.reason = this.list[this.index_reason].reason
				this.change_flag = !this.change_flag 
			},
			literature(index){
				this.literature_index=index;
				this.literature_flag = !this.literature_flag
				this.val_literature = this.list[this.literature_index].notice

			},
			literaturesave(){

				this.list[this.literature_index].notice=this.val_literature
				this.literature_flag = !this.literature_flag
			},
			itp_blur(index){
				var state_= this
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
					          this.$notify({
					            message: '更新成功'
					          });
					        }).catch(() => {
								  state_.list[index].hu_category_id=""     
					  });
				}
			},	
			ach(index){
				this.$confirm('确定完成吗？', '提示', {
				          confirmButtonText: '确定',
				          cancelButtonText: '取消',
				          type: 'warning'
				      }).then(() => {
				      		if(this.list[index].complete_flag == 1){
				      			this.list[index].complete_flag = 0;
				      		}else{
				      			this.list[index].complete_flag = 1
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
							this.$confirm('确定更改翻译状态吗？', '提示', {
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
			recognize(index){
				if(this.re_g!=""&&this.mo_g!=""&&this.re_s!=""&&this.mo_s!=""&&this.mn_m!=""&&this.mn_g!=""&&this.mo_a!=""&&this.re_a!=""){
					if((this.re_g==1&&this.mo_g==1&&this.re_s==1&&this.mo_s==1&&this.mn_m==1&&this.mn_g==1&&this.mo_a==1&&this.re_a==1)||
					(this.re_g==1&&this.mo_g==1&&this.re_s==1&&this.mo_s==1&&this.mn_m==1&&this.mn_g==0&&this.mo_a==0&&this.re_a==0)){
						this.$confirm('确定更改该状态？', '提示', {
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
						this.$confirm('确定更改指摘状态？', '提示', {
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
						            message: '指摘成功'
						          });     
					        }).catch(() => {
								this.$notify({
								  message: '指摘取消'
							});      
						});
					}else{
						this.$notify({
							  message: '您无权限操作'
						}) 
					}
				}
			},
			save(){
				this.$axios.post(this.Ip+'/DEFContent',this.list)
				.then(res => {
					this.$notify({
					  message: '保存成功!'
					});	
				})
			},
			back(){
				this.$router.go(-1)
			},
			save_back(){
				this.$axios.post(this.Ip+'/DEFContent',this.list)
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
				item.agree_flag = null 
	            item.analysis =  ""
	            item.author_name =  ""
	            item.dcu_meu= "" 
	            item.def_rc_id= 740 
	            item.exception= ""  	            
	            item.complete_flag = 0
				item.agree_flag = 0
				item.has_problem = 0 
				item.translation_flag= null
	            item.hu_def_id= window.sessionStorage.getItem('TAGL')
	            item.implementation= ""
		    item.unrequire=""
				item.model_list= [
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                "", 
	                ""
	            ]
				item.new_date ="" 
	            item.notice = "" 
	            item.other_spec= "" 
	            item.pf_action= "" 
	            item.pf_status= ""
	            item.pf_trigger= ""
	            item.reason= ""
	            item.rel_flow_diagram= ""
	            item.rel_hal_design= ""
	            item.remark= ""
	            item.title= ""
	            item.unique_id= ""
            	item.model_list=[]
            	item.list_model=[]
				var msg =this.list;
				msg.push(item)
				this.list = [];
				this.list = msg;
				this.$notify({message: '保存成功!'}); 
			},
			examine_hu(){
				this.$router.push({name: 'TAGL',params:{DEF_id: this.tdata}})
			},
			humsave(){
				this.HU_moudel=!this.HU_moudel
			},
			othmsave(){
				this.other_moudel=!this.other_moudel
			},
			edothm_del(index){
				this.list_model.splice(index,1)	
				
			},
			edhm_add(){
				var model={};
				model=JSON.parse(JSON.stringify(model))
				model.title=""
				model.model_id=""
				model.val=""
				var msg2 =this.list_model;
				msg2.push(model)
				this.list_model = [];
				this.list_model = msg2;
			},
			dutyhumsave(){
				this.DCU_flag = !this.DCU_flag
				this.list[this.examine_index].model_list=this.list_model
				for(let i=0;i<this.list[this.examine_index].model_list.length;i++){
					for(let j=0;j<this.namesss.length;j++){
						if(this.list[this.examine_index].model_list[i].title==this.namesss[j].title){
							this.list[this.examine_index].model_list[i].model_id=this.namesss[j].model_id
							break
						}
					}
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
		width: 100%;
		height: 100%;
		overflow: scroll;
	}
	.Asa_content_tagl{
		width:98%;
		box-shadow: 2px 1px 9px #ccc;
		height:300px;
		margin: 0 auto;
		margin-top: 30px;
	}
	.Asa_arl_tagl{
		width:18%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_Hu_tagl{
		width:10%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_moudel_tagl{
		width:20%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_duty_tagl{
		width:20%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_remark_tagl{
		width:15%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_remark_tagl_2{
		width:12%;
		height:300px;
		border: 1px solid #dfe6ec;
	}
	.Asa_dele_tagl{
		width:17%;
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
    .Asa_content_tagl .arl_btn{
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
  	position: fixed;
  	height: 60px;
  	bottom:0;
  	left: 300px;
  	right:0;
  	background-color: white;
  }
 .Asa_dele_tagl .operation_btn,.Asa_remark_tagl .operation_btn,.Asa_duty_tagl .operation_btn{
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
	    height: 65px;
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
	    margin-left: 10%;
	    line-height: 13px;
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
	.el-dialog--small{
		width:80%;
	}
	h5{
		width: 100%;
		margin-top: 20px;
	}
	#myWorkChildren2 .el_c .el-dialog--small{
		width: 57.6%;
		/*height: 22%;*/
	}
	#myWorkChildren2 .ed_hm .el-dialog--small{
		/*height: 41%;*/
	}
	.ARL_msg{
		margin: 15px 10% 0 25%;
		font-size: 12px;
		height: 16px;
		overflow: hidden;
		text-overflow:ellipsis;
		white-space: nowrap;
	}
	.ARL_msg_title{
		font-weight: bold;
	}
	.tagl_size{
		font-size: 12px;
		font-weight: bold;
		padding:5px;
	}
	.tagl_msg{
		font-size: 12px;
		font-weight: bold;
		width:100%;
		/*line-height: 36px;*/
	}
	.tagl_msg>span{
		/*width: 100px;*/
		display: block;
		/*margin: 10px;*/
		line-height: 16px;
	}
	.opt_ipt2{
		/*height:45px;*/
	}
	#ARLFix{
		position: fixed;
		left: 300px;
		right: 0;
  		height: 250px;
  		z-index: 99;
  		border: double 5px black;	
  		top: 60px;
	}
	#ARLFix p{
		text-align: center;
		font-size: 30px;
		background-color: white;
	}
	#TAGL_Header_fixed{
		width: 100%;
		margin-top: 250px;
		margin-bottom:60px;
	}
	.Asa_dele_tagl .operation_btn, .Asa_remark_tagl .operation_btn, .Asa_duty_tagl .operation_btn{
		margin-top: 6px;
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
	.rel_btn {
	    display: block;
	    margin: 0 auto;
	    margin-top: 12px;
	}
	.el-select{
   	   margin-top: 12px;
       margin-left: 10px;
	}
</style>
