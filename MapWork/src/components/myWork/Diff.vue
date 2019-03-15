<template>
	<div id="File-Modle-box" v-loading.fullscreen.lock="fullscreenLoading" element-loading-text="正在加载中">
		<div class="tree-box" onselectstart="return false">
			<div class="technicalDoc">
			</div>
		</div>
		<div class="content-box">
			<ul class="message-box">
				<li>图例 :</li>
				<li class="add-li">新增</li>
				<li class="diff-li">修改</li>
				<li class="delete-li">删除</li>
				<li class="return_btn" @click='return_index()'>【返回】</li>
			</ul>
			<div class="content-box-left-box">
				<h1 class="diff-title">
					<p class="diff-title-content-fl">
						OldVersion
					</p>
					<p class="diff-title-content-fr">
						<el-button type="text" @click='get_last_left_version()'>上一版</el-button>
						<el-button type="text" @click='get_next_left_version()'>下一版</el-button>
					</p>
				</h1>
				<div class="content-box-left">
					<!-- title -->
					<div class="nav-box">
						<h2 class="nav-title" v-html='left_title'></h2>
						<p class="title-detail" v-html='left_doc_update_info'></p>
						<p class="title-content" v-html='left_doc_summary'></p>
					</div>
					<!-- Asat -->
					<div class="Asat-box">
						<h3 class="title-h3">
							<span>成果物文件</span>
						</h3>
						<div class="content-msg" v-if='left_sub_list.Asat.length != 0'>
							<el-table :data="left_sub_list.Asat" border>
							    <el-table-column label="文件名" header-align='center'>
									<template slot-scope="scope">
										<span v-html='scope.row.file_name'></span>
									</template>	
							    </el-table-column>
							    <el-table-column label="上传时间" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.update_time'></span>
							    	</template>	
							    </el-table-column>
							</el-table>
						</div>
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- Block -->
					<div class="Block-box">
						<h3 class="title-h3">
							<span>Block</span>
						</h3>
						<div class="img-box"  v-if='left_sub_list.Block.length != 0'>
							<img :src="left_sub_list.Block[0].fileList[0].url" alt="" class='img-style'>
						</div>
						<div class="content-size"  v-else-if='left_sub_list.Block.length != 0'>
							<span>Block说明</span>
							<div class="content-size">
								<span v-html = "left_sub_list.Block[0].val"></span>
							</div>
						</div>
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- Class -->
					<div class="Class-box">
						<h3 class="title-h3">
							<span>Class</span>
						</h3>
						<div  v-if='left_sub_list.Class.length != 0'>
							<div class="img-box" >
								<img :src="left_sub_list.Class[0].fileList[0].url" alt="" class='img-style' v-if='left_sub_list.Class[0].fileList[0].url!=""'>
							</div>
							<div class="content-size">
								<span>Class说明</span>
								<div class="content-size">
									<span v-html = "left_sub_list.Class[0].val"></span>
								</div>
							</div>
						</div>
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- IF -->
					<div class="IF-box">
						<h3 class="title-h3">
							<span>IF</span>
						</h3>
						<div class="content-msg" v-if='left_sub_list.IF.length != 0'>
							<el-table :data="left_sub_list.IF" border >
							    <el-table-column label="I/F名" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.if_name'></span>
							    	</template>	
							    </el-table-column>
							    <el-table-column label="参数" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.parameter'></span>
							    	</template>	
							    </el-table-column>
							    <el-table-column label="返回值" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.return_val'></span>
							    	</template>	
							    </el-table-column>
							    <el-table-column label="接口说明" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.description'></span>
							    	</template>
							    </el-table-column>
							</el-table>
						</div>
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- Usecase -->
					<div class="Usecase-box">
						<h3 class="title-h3">
							<span>Usecase</span>
						</h3>
						<div class="usecase-common-pic-box">
							<h4 class="title-h4" style="border:0 none;paddingTop:0">Usecase共通图</h4>
							<div class="img-box" v-if="user_left_common.length != 0">
								<img :src="user_left_common[0].url" alt="" class='img-style'>
							</div>
						</div>
						<!-- Usecase, Sequence, Statemachine, 式样书关系表-->
						<div class="Usecase_content">
							<el-table :data="left_sub_list.Usecase" border style="width:98.5%;margin-left:1.5%">
							    <el-table-column prop="number" label="编号" header-align='center' width='150'></el-table-column>
							    <el-table-column prop="title" label="名称" header-align='center' width='200'>
							        <template  slot-scope="scope">
							            <span class='Asa-display' :title='scope.row.val' v-html='scope.row.title'></span>
							        </template>
							    </el-table-column>
							    <el-table-column label="时序图" header-align='center'>
							        <template slot-scope="scope">
							            <span v-for='item in scope.row.seq_list'>
							               <span class='Asa-display' v-html='item.number'></span>
							            </span>
							        </template>
							    </el-table-column>
							    <el-table-column label="机能点" header-align='center' title="式样书机能点">
							        <template slot-scope="scope">
							            <span v-for='item in scope.row.spec_list'>
							               <span class='Asa-display' :title='item.title'  target="_Blank" v-html='item.func_id'></span>
							            </span>
							        </template>
							    </el-table-column>
							</el-table>	
						</div>
						<!-- 式样书 -->
						<div class="input-box" v-if='false'>
							<h4 class="title-h4">式样书</h4>
							<div class="content-msg" v-if='left_spec_list.length != 0'>
								<el-table :data="left_spec_list" border>
								    <el-table-column label="式样书类型" header-align='center' >
								    	<template slot-scope="scope">
								    		<span v-html='scope.row.spec_type'></span>
								    	</template>		
								    </el-table-column>
								    <el-table-column label="式样书名称" header-align='center' min-width='300'>
								    	<template slot-scope="scope">
								    		<span v-html='scope.row.spec_name'></span>
								    	</template>	
								    </el-table-column>
								    <el-table-column label="机能点" header-align='center' min-width='200'>
								    	<template slot-scope="scope">
								    		<span v-html='scope.row.func_id'></span>
								    	</template>	
								    </el-table-column>
								</el-table>
							</div>
							<p class="message" v-else>暂无数据</p>
						</div>
					</div>
					<!-- Squence -->
					<div class="Squence-box">
						<h3 class="title-h3">
							<span>Sequence</span>
						</h3>
						<div v-for='(seq_item, seq_index) in left_sequence' v-if='left_sequence.length != 0' :key="seq_index" style="marginLeft:20px">
							<h4 class="title-h4">Sequence{{seq_index + 1}}</h4>
							<div class="img-box" v-if='seq_item.url!=""'>
								<img :src="seq_item.url" alt="" class='img-style'>
							</div>
							<div class="content-size" style="marginLeft:20px">
								<span>Sequence说明</span>
								<div class="content-size">
									<span v-html='seq_item.val'></span>
								</div>
							</div>
							<!-- activities -->
							<div class="activities-box Resource-box">
								<div class="activities" v-for='(activities_item,activities_index) in seq_item.activities' v-if='seq_item.activities.length != 0'>
									<h4 class="title-h4">Activity{{activities_index + 1}}</h4>
									<div class="img-box">
										<img :src="activities_item[0].fileList[0].url" alt="" class='img-style'>
									</div>
									<div class="content-size">
										<span>Activity说明</span>
										<div class="content-size">
											<span v-html='activities_item[0].val'></span>
										</div>
									</div>
								</div>
								<div v-else>
									<h4 class="title-h4">Activity</h4>
									<p class="message">暂无数据</p>
								</div>
							</div>
							<!-- Resource -->
							<div class="Resource-box">
								<h4 class="title-h4">Resource</h4>
								<div class="content-msg" v-if='seq_item.resource.length != 0'>
									<el-table :data="seq_item.resource" border>
										<el-table-column label="资源类型" header-align='center'>
											<template slot-scope="scope">
												<span v-html='scope.row.rsc_name'></span>
											</template>	
										</el-table-column>
										<el-table-column label="确认内容" header-align='center' min-width='500'>
											<template slot-scope="scope">
												<span v-html='scope.row.operator + scope.row.value + scope.row.unit'></span>
											</template>	
										</el-table-column>
									</el-table>
								</div>
								<p class="message" v-else>暂无数据</p>
							</div>
						</div>
						<div v-else>
							<p class="message">暂无数据</p>
							<div class="Resource-box">
								<h4 class="title-h4">Resource</h4>
								<p class="message">暂无数据</p>
							</div>
						</div>
					</div>
					<!-- Statemachine -->
					<div class="Statemachine">
						<h3 class="title-h3"><span>Statemachine</span></h3>
						<div class="img-box"  v-if='left_std.length != 0'>
							<img :src="left_std[0].url" alt="" class='img-style'>
						</div>
						<div class="content-size" v-if='left_std.length != 0'>
							<span>Statemachine说明</span>
							<div class="content-size">
								<span v-html = "left_std[0].val"></span>
							</div>
						</div>
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- DRBFM -->
					<div class="DRBFM">
						<h4 class="title-h3">DRBFM</h4>
						<p class="message"  v-if="left_drbfm.length === 0">暂无数据</p>
                        <drbfm-preview :prop_drbfm_data="left_drbfm" v-else></drbfm-preview>
					</div>
				</div>
			</div>
			<div class="content-box-right-box">
				<h1 class="diff-title">
					<p class="diff-title-content-fl">
						NewVersion
					</p>
					<p class="diff-title-content-fr">
						<el-button type="text" @click='get_last_right_version()'>上一版</el-button>
						<el-button type="text" @click='get_next_right_version()'>下一版</el-button>
					</p>
				</h1>
				<div class="content-box-right">
					<!-- title -->
					<div class="nav-box">
						<h2 class="nav-title" v-html='right_title'></h2>
						<p class="title-detail" v-html='right_doc_update_info'></p>
						<p class="title-content" v-html='right_doc_summary'></p>
					</div>
					<!-- Asat -->
					<div class="Asat-box">
						<h3 class="title-h3">
							<span>成果物文件</span>
						</h3>
						<div class="content-msg" v-if='right_sub_list.Asat.length != 0'>
							<el-table :data="right_sub_list.Asat" border>
							    <el-table-column label="文件名" header-align='center'>
									<template slot-scope="scope">
										<span v-html='scope.row.file_name'></span>
									</template>	
							    </el-table-column>
							    <el-table-column label="上传时间" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.update_time'></span>
							    	</template>	
							    </el-table-column>
							</el-table>
						</div>
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- Block -->
					<div class="Block-box">
						<h3 class="title-h3">
							<span>Block</span>
						</h3>
						<div class="img-box"  v-if='right_sub_list.Block.length != 0'>
							<img :src="right_sub_list.Block[0].fileList[0].url" alt="" class='img-style'>
						</div>
						<div class="content-size"  v-else-if='right_sub_list.Block.length != 0'>
							<span>Block说明</span>
							<div class="content-size">
								<span v-html = "right_sub_list.Block[0].val"></span>
							</div>
						</div>
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- Class -->
					<div class="Class-box">
						<h3 class="title-h3">
							<span>Class</span>
						</h3>
						<div  v-if='right_sub_list.Class.length != 0'>
							<div class="img-box" >
								<img :src="right_sub_list.Class[0].fileList[0].url" alt="" class='img-style' v-if='right_sub_list.Class[0].fileList[0].url!=""'>
							</div>
							<div class="content-size">
								<span>Class说明</span>
								<div class="content-size">
									<span v-html = "right_sub_list.Class[0].val"></span>
								</div>
							</div>
						</div>
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- IF -->
					<div class="IF-box">
						<h3 class="title-h3">
							<span>IF</span>
						</h3>
						<div class="content-msg" v-if='right_sub_list.IF.length != 0'>
							<el-table :data="right_sub_list.IF" border >
							    <el-table-column label="I/F名" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.if_name'></span>
							    	</template>	
							    </el-table-column>
							    <el-table-column label="参数" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.parameter'></span>
							    	</template>	
							    </el-table-column>
							    <el-table-column label="返回值" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.return_val'></span>
							    	</template>	
							    </el-table-column>
							    <el-table-column label="接口说明" header-align='center'>
							    	<template slot-scope="scope">
							    		<span v-html='scope.row.description'></span>
							    	</template>
							    </el-table-column>
							</el-table>
						</div>
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- Usecase -->
					<div class="Usecase-box">
						<h3 class="title-h3">
							<span>Usecase</span>
						</h3>
						<div class="usecase-common-pic-box">
							<h4 class="title-h4" style="border:0 none;paddingTop:0">Usecase共通图</h4>
							<div class="img-box" v-if="user_right_common.length != 0">
								<img :src="user_right_common[0].url" alt="" class='img-style'>
							</div>
						</div>
						<!-- Usecase, Sequence, Statemachine, 式样书关系表-->
						<div class="Usecase_content">
							<el-table :data="right_sub_list.Usecase" border style="width:98.5%;margin-left:1.5%">
							    <el-table-column prop="number" label="编号" header-align='center' width='150'></el-table-column>
							    <el-table-column prop="title" label="名称" header-align='center' width='200'>
							        <template  slot-scope="scope">
							            <span class='Asa-display' :title='scope.row.val' v-html='scope.row.title'></span>
							        </template>
							    </el-table-column>
							    <el-table-column label="时序图" header-align='center'>
							        <template slot-scope="scope">
							            <span v-for='item in scope.row.seq_list'>
							               <span class='Asa-display' v-html='item.number'></span>
							            </span>
							        </template>
							    </el-table-column>
							    <el-table-column label="机能点" header-align='center' title="式样书机能点">
							        <template slot-scope="scope">
							            <span v-for='item in scope.row.spec_list'>
							               <span class='Asa-display' :title='item.title'  target="_Blank" v-html='item.func_id'></span>
							            </span>
							        </template>
							    </el-table-column>
							</el-table>	
						</div>

						<!-- usecase设计所有内容 -->
						<div class="Usecase_content" v-for='(item, index) in right_sub_list.Usecase' :key="index"  v-if='false'>
							<!-- 式样书 -->
							<div class="input-box">
								<h4 class="title-h4">式样书</h4>
								<div class="content-msg" v-if='right_spec_list.length != 0'>
									<el-table :data="right_spec_list" border>
									    <el-table-column label="式样书类型" header-align='center' >
									    	<template slot-scope="scope">
									    		<span v-html='scope.row.spec_type'></span>
									    	</template>		
									    </el-table-column>
									    <el-table-column label="式样书名称" header-align='center' min-width='300'>
									    	<template slot-scope="scope">
									    		<span v-html='scope.row.spec_name'></span>
									    	</template>	
									    </el-table-column>
									    <el-table-column label="机能点" header-align='center' min-width='200'>
									    	<template slot-scope="scope">
									    		<span v-html='scope.row.func_id'></span>
									    	</template>	
									    </el-table-column>
									</el-table>
								</div>
								<p class="message" v-else>暂无数据</p>
							</div>
							
						</div>
					</div>
					<!-- Sequence -->
					<div class="Squence-box">
						<h3 class="title-h3">
							<span>Sequence</span>
						</h3>
						<div v-for='(seq_item, seq_index) in right_sequence' v-if='right_sequence.length != 0' :key="seq_index" style="marginLeft:20px">
							<h4 class="title-h4">Sequence{{seq_index + 1}}</h4>
							<div class="img-box" v-if='seq_item.url!=""'>
								<img :src="seq_item.url" alt="" class='img-style'>
							</div>
							<div class="content-size">
								<span>Squence说明</span>
								<div class="content-size">
									<span v-html='seq_item.val'></span>
								</div>
							</div>
							<!-- activities -->
							<div class="activities-box Resource-box">
								<div class="activities" v-for='(activities_item,activities_index) in seq_item.activities' v-if='seq_item.activities.length != 0'>
									<h4 class="title-h4">Activity{{activities_index + 1}}</h4>
									<div class="img-box">
										<img :src="activities_item[0].fileList[0].url" alt="" class='img-style'>
									</div>
									<div class="content-size">
										<span>Activity说明</span>
										<div class="content-size">
											<span v-html='activities_item[0].val'></span>
										</div>
									</div>
								</div>
								<div v-else>
									<h4 class="title-h4">Activity</h4>
									<p class="message">暂无数据</p>
								</div>
							</div>
							<!-- Resource -->
							<div class="Resource-box">
								<h4 class="title-h4">Resource</h4>
								<div class="content-msg" v-if='seq_item.resource.length != 0'>
									<el-table :data="seq_item.resource" border>
										<el-table-column label="资源类型" header-align='center'>
											<template slot-scope="scope">
												<span v-html='scope.row.rsc_name'></span>
											</template>	
										</el-table-column>
										<el-table-column label="确认内容" header-align='center' min-width='500'>
											<template slot-scope="scope">
												<span v-html='scope.row.operator + scope.row.value + scope.row.unit'></span>
											</template>	
										</el-table-column>
									</el-table>
								</div>
								<p class="message" v-else>暂无数据</p>
							</div>
						</div>
						<div v-else>
							<h4 class="title-h4">Squence设计</h4>
							<p class="message">暂无数据</p>
							<div class="Resource-box">
								<h4 class="title-h4">Resource</h4>
								<p class="message">暂无数据</p>
							</div>
						</div>
					</div>
					<!-- Statemachine -->
					<div class="Statemachine">
						<h3 class="title-h3">
							<span>Statemachine</span>
						</h3>
						<div class="img-box"  v-if='right_std.length != 0'>
							<img :src="right_std[0].url" alt="" class='img-style'>
						</div>
						<div class="content-size" v-if='right_std.length != 0'>
							<span>Statemachine说明</span>
							<div class="content-size">
								<span v-html = "right_std[0].val"></span>
							</div>
						</div>
					
						<p class="message" v-else>暂无数据</p>
					</div>
					<!-- DRBFM -->
					<div class="DRBFM">
						<h3 class="title-h3">
							<span>DRBFM</span>
						</h3>
						<p class="message" v-if="right_drbfm.length === 0">暂无数据</p>
                        <drbfm-preview :prop_drbfm_data="right_drbfm" v-else></drbfm-preview>
					</div>
				</div>
			</div>
			
		</div>
	</div>
</template>
<script>
require('../../assets/js/jquery-1.8.3.min.js')
// import diffDrbfm from './DiffDrbfm.vue'
import drbfmPreview from './DRBFM_diff_preview'

export default {
    components: {
        // diffDrbfm: diffDrbfm,
        'drbfmPreview': drbfmPreview
    },
	data () {
		return {
			left_data:{},
			right_data:{},
			left_doc_update_info:'',
			right_doc_update_info:'',
			left_doc_summary:'',
			right_doc_summary:'',
			left_title:'',
			right_title:'',
			left_sub_list:{
				Asat:[],
				IF:[],
				Block:[],
				Usecase:[],
				Class:[]
			},
			right_sub_list:{
				Asat:[],
				IF:[],
				Block:[],
				Usecase:[],
				Class:[]
			},
			left_spec_list:[],
			right_spec_list:[],
			left_secne_list:[],
			right_secne_list:[],
			left_std:[],
			right_std:[],
			left_sequence:[],
			right_sequence:[],
			left_resource:[],
			right_resource:[],
			user_left_common:[],
			user_right_common:[],
			right_drbfm:[],
			left_drbfm:[],
			left_Consider:[],
			right_Consider:[],
			fullscreenLoading:true,
			key_id:0,
			version_list:[],
			left_version:null,
			right_version:null,
			left_index:null,
			right_index:null,
		}
	},
	mounted(){
		// this.get_diff_data()
		this.get_journal_Version()
	},
	methods: {
		get_journal_Version(){
			this.$axios.get(this.Ip+"/JournalVersion/"+ Number(window.sessionStorage.getItem('DocId'))).then(res=>{
				if(res.data.result == 'OK'){
					this.version_list = res.data.content
					if(this.version_list.length == 0){
						this.$alert('该版本暂无Diff','提示!')
						return
					}
					if(this.version_list.length == 1){
						this.$axios.get(this.Ip+"/JournalDiff/"+ Number(window.sessionStorage.getItem('DocId'))).then(res=>{
							this.fullscreenLoading = false
							console.log(res.data)
							if(res.data.result == 'OK'){
								this.Initialization()
								if(JSON.stringify(res.data.content.left) != '{}'){
									this.get_diff_left_data(res.data.content.left)
								}
								if(JSON.stringify(res.data.content.right) != '{}'){
									this.get_diff_right_data(res.data.content.right)
								}
							}else{
								this.$message({
								    showClose: true,
								    message: '服务异常',
								    type: 'error'
								})
							}
						})
						return
					}
					this.left_index = this.version_list.length-2
					this.right_index = this.version_list.length-1
					this.left_version = this.version_list[this.left_index]
					this.right_version = this.version_list[this.right_index]
					this.get_diff_data(this.left_version,this.right_version)
				}
			})
		},
		// 获取上一个版本 左侧
		get_last_left_version(){
			this.left_index = this.left_index-1
			if(this.left_index<0){
				this.$alert('无上一版本信息','提示!')
				this.left_index = 0
				return
			}
			this.fullscreenLoading=true
			this.left_version = this.version_list[this.left_index]
			this.right_version = this.version_list[this.right_index]
			this.get_diff_data(this.left_version,this.right_version)
		},
		get_next_left_version(){
			this.left_index = this.left_index+1
			if(this.left_index>this.version_list.length-2){
				this.$alert('无下一版本信息','提示!')
				this.left_index = this.version_list.length-2
				return
			}
			this.fullscreenLoading=true
			this.left_version = this.version_list[this.left_index]
			this.right_version = this.version_list[this.right_index]
			this.get_diff_data(this.left_version,this.right_version)
		},
		// 获取上一个版本 右侧
		get_last_right_version(){
			this.right_index = this.right_index-1
			if(this.right_index<0){
				this.$alert('无上一版本信息','提示!')
				this.right_index = 0
				return
			}
			this.fullscreenLoading=true
			this.left_version = this.version_list[this.left_index]
			this.right_version = this.version_list[this.right_index]
			this.get_diff_data(this.left_version,this.right_version)
		},
		get_next_right_version(){
			this.right_index = this.right_index+1
			if(this.right_index>this.version_list.length-1){
				this.$alert('无下一版本信息','提示!')
				this.right_index = this.version_list.length-1
				return
			}
			this.fullscreenLoading=true
			this.left_version = this.version_list[this.left_index]
			this.right_version = this.version_list[this.right_index]
			this.get_diff_data(this.left_version,this.right_version)
		},
		get_diff_data(left_version,right_version){
			this.$axios.get(this.Ip+"/JournalDiff/"+ Number(window.sessionStorage.getItem('DocId')) +'/'+ left_version + '/' + right_version).then(res=>{
				this.fullscreenLoading = false
				if(res.data.result == 'OK'){
					this.Initialization()
					if(JSON.stringify(res.data.content.left) != '{}'){
						this.get_diff_left_data(res.data.content.left)
					}
					if(JSON.stringify(res.data.content.right) != '{}'){
						this.get_diff_right_data(res.data.content.right)
					}
				}else{
					this.$message({
					    showClose: true,
					    message: '服务异常',
					    type: 'error'
					})
				}
			})
		},
		// 初始化
		Initialization(){
			this.left_sub_list.Asat = []
			this.left_sub_list.IF = []
			this.left_sub_list.Block = []
			this.left_sub_list.Usecase = []
			this.left_sub_list.Class = []

			this.right_sub_list.Asat = []
			this.right_sub_list.IF = []
			this.right_sub_list.Block = []
			this.right_sub_list.Usecase = []
			this.right_sub_list.Class = []
			this.left_spec_list= []
			this.right_spec_list= []
			this.left_secne_list= []
			this.right_secne_list= []
			this.left_std= []
			this.right_std= []
			this.left_sequence= []
			this.right_sequence= []
			this.left_resource= []
			this.right_resource= []
			this.user_left_common= []
			this.user_right_common= []
			this.right_drbfm= []
			this.left_drbfm= []
			this.left_Consider= []
			this.right_Consider= []
		},
		get_diff_left_data(data){
			console.log(data,'---')
			let update_date_re = new RegExp(/^\d+-\d+-\d+/)
			this.left_doc_update_info = 
				'由 ' +
                data.creator +
                ' 创建，最终由 ' +
                data.editor +
                ' 修改于 ' +
                data.update_time
                // data.update_time.match(update_date_re) 
                +
                ' 版本 ' + 
                data.major_ver + '.' +
                data.minor_ver + '.' +
                data.micro_ver

            this.left_doc_summary = data.summary
            this.left_title = data.title
            this.get_left_sub_data_list(data.sub)
		},
		get_left_sub_data_list(sub_data_list){
			if (sub_data_list.length == 0) {
			    return
			}
			for(let i = 0 ;i< sub_data_list.length; i++){
				if(sub_data_list[i].sec_type == 'ASTAH'){
					this.left_sub_list.Asat = []
					for(let k = 0;k<sub_data_list[i].astah_files.length;k++){
						this.left_sub_list.Asat.push(sub_data_list[i].astah_files[k])
					}
				}else if(sub_data_list[i].sec_type == 'IF'){
					this.left_sub_list.IF.push(sub_data_list[i])
				}else if(sub_data_list[i].sec_type == 'BLOCK'){
					let block_json_data = JSON.parse(sub_data_list[i].content)
					this.left_sub_list.Block = block_json_data
				}else if(sub_data_list[i].sec_type == "CLASS"){
					let class_json_data = JSON.parse(sub_data_list[i].content)
					if(class_json_data[0].fileList.length == 0){
						let img_src_and_val = {
							url:'',
							val:''
						}
						class_json_data[0].fileList.push(img_src_and_val)
					}
					this.left_sub_list.Class = class_json_data
				}else if(sub_data_list[i].sec_type == 'USERCASE'){
					if(sub_data_list[i].table_list.length == 0){
						this.left_sub_list.Usecase = []
					}else{
						this.left_sub_list.Usecase = sub_data_list[i].table_list
					}
					this.get_usercasesub_list(sub_data_list[i].sub)	
					
				}else if(sub_data_list[i].sec_type == "SEQUENCE"){

					let seq_data = JSON.parse(sub_data_list[i].content)
					let src_and_val_data = {
						'url':'',
						'val':'',
						'resource':[],
						'activities':[]
					}
					var activities_data = []
					if(sub_data_list[i].activities.length != 0){
						for(let activities_i = 0; activities_i<sub_data_list[i].activities.length;activities_i++){
							let activities_json_data = JSON.parse(sub_data_list[i].activities[activities_i].content)
							activities_data.push(activities_json_data)
						}
					}
					if(seq_data[0].fileList.length != 0){
						src_and_val_data = {
							'url':seq_data[0].fileList[0].url,
							'val':seq_data[0].val,
							'resource':sub_data_list[i].sub,
							'activities':activities_data
						}
					}
					this.left_sequence.push(src_and_val_data)

				}else if(sub_data_list[i].sec_type == 'COMMON'){
					let user_common_json_data = JSON.parse(sub_data_list[i].content)
					if(user_common_json_data[0].fileList.length != 0){
						this.user_left_common.push({'url':user_common_json_data[0].fileList[0].url})
					}
				}else if(sub_data_list[i].sec_type == "STD"){
					let std_data = JSON.parse(sub_data_list[i].content)
					let src_and_val_data = {
						url:'',
						val:''
					}
					if(std_data[0].fileList.length != 0){
						src_and_val_data = {
							'url':std_data[0].fileList[0].url,
							'val':std_data[0].val
						}
						this.left_std.push(src_and_val_data)
					}
				}else if(sub_data_list[i].sec_type === 'DRBFM') {
                    this.left_drbfm = sub_data_list[i].checklist
                }
			}
		},
		get_left_usercase(sub_list){
					
			
		},
		get_usercasesub_list(list){
			for(let i = 0;i<list.length;i++){
				if(list[i].sec_type == "SPEC"){
					this.left_spec_list = list[i].specs
				}else if(list[i].sec_type == "SCENE"){
					this.left_secne_list = list[i].scenes
				}else if(list[i].sec_type === 'CONSIDER'){
					this.left_Consider = list[i].considers
				}else{
                    //do nothing momentarily
                }
			}
		},
		get_diff_right_data(data){
			let update_date_re = new RegExp(/^\d+-\d+-\d+/)
			this.right_doc_update_info = 
				'由 ' +
                data.creator +
                ' 创建，最终由 ' +
                data.editor +
                ' 修改于 ' +
                data.update_time
                // data.update_time.match(update_date_re)
                 +
                ' 版本 ' + 
                data.major_ver + '.' +
                data.minor_ver + '.' +
                data.micro_ver

            this.right_doc_summary = data.summary
            this.right_title = data.title
            this.get_right_sub_data_list(data.sub)
		},
		get_right_sub_data_list(sub_data_list){
			if (sub_data_list.length == 0) {
			    return
			}
			for(let i = 0 ;i< sub_data_list.length; i++){
				if(sub_data_list[i].sec_type == 'ASTAH'){
					this.right_sub_list.Asat = []
					for(let k = 0;k<sub_data_list[i].astah_files.length;k++){
						this.right_sub_list.Asat.push(sub_data_list[i].astah_files[k])
					}
				}else if(sub_data_list[i].sec_type == 'IF'){
					this.right_sub_list.IF.push(sub_data_list[i])
				}else if(sub_data_list[i].sec_type == 'BLOCK'){
					let block_json_data = JSON.parse(sub_data_list[i].content)
					this.right_sub_list.Block = block_json_data
				}else if(sub_data_list[i].sec_type == "CLASS"){
					let class_json_data = JSON.parse(sub_data_list[i].content)
					if(class_json_data[0].fileList.length == 0){
						let img_src_and_val = {
							url:'',
							val:''
						}
						class_json_data[0].fileList.push(img_src_and_val)
					}
					this.right_sub_list.Class = class_json_data
				}else if(sub_data_list[i].sec_type == 'USERCASE'){
					if(sub_data_list[i].table_list.length == 0){
						this.right_sub_list.Usecase = []
					}else{
						this.right_sub_list.Usecase = sub_data_list[i].table_list
					}
					this.get_right_usercasesub_list(sub_data_list[i].sub)
				}else if(sub_data_list[i].sec_type == "SEQUENCE"){
					let seq_data = JSON.parse(sub_data_list[i].content)
					let src_and_val_data = {
						'url':'',
						'val':'',
						'resource':[],
						'activities':[]
					}
					var activities_data = []
					if(sub_data_list[i].activities.length != 0){
						for(let activities_i = 0; activities_i<sub_data_list[i].activities.length;activities_i++){
							let activities_json_data = JSON.parse(sub_data_list[i].activities[activities_i].content)
							activities_data.push(activities_json_data)
						}
					}
					if(seq_data[0].fileList.length != 0){
						src_and_val_data = {
							'url':seq_data[0].fileList[0].url,
							'val':seq_data[0].val,
							'resource':sub_data_list[i].sub,
							'activities':activities_data
						}
					}
					this.right_sequence.push(src_and_val_data)
				}else if(sub_data_list[i].sec_type == "STD"){
					let std_data = JSON.parse(sub_data_list[i].content)
					let src_and_val_data = {
						'url':'',
						'val':""
					}
					if(std_data[0].fileList.length != 0){
						src_and_val_data = {
							'url':std_data[0].fileList[0].url,
							'val':std_data[0].val
						}
						this.right_std.push(src_and_val_data)
					}
				}else if(sub_data_list[i].sec_type == 'COMMON'){
					let user_common_json_data = JSON.parse(sub_data_list[i].content)
					if(user_common_json_data[0].fileList.length != 0){
						this.user_right_common.push({'url':user_common_json_data[0].fileList[0].url})
					}
				}else if(sub_data_list[i].sec_type === 'DRBFM') {
                    this.right_drbfm = sub_data_list[i].checklist
                }
			}
		},
		get_right_usercase(sub_list){

			
		},
		get_right_usercasesub_list(list){
			for(let i = 0;i<list.length;i++){
				if(list[i].sec_type == "SPEC"){
					this.right_spec_list = list[i].specs
					console.log(this.right_spec_list)
				}else if(list[i].sec_type == "SCENE"){
					this.right_secne_list = list[i].scenes
				}else if(list[i].sec_type === 'CONSIDER'){
					this.right_Consider = list[i].considers
				} else {
                    //do nothing momentarily
                }
			}
		},
		return_index(){
			this.$router.push('/tagl/File_design/Preview/'+window.sessionStorage.getItem('DocId'))
		}
	}
}
</script>
<style scoped>
	#File-Modle-box {
		width: 100%;
		height: 100%;
		min-width: 1024px;
		color: #606266;
		overflow: hidden;
	}
	.tree-box {
		/*float: left;*/
		position: relative;
		top: 0;
		left: 0;
		z-index: 9;
		margin: 0;
		padding: 0;
		width: 15%;
		height: 98%;
		background-color:white;
		border-right: 2px solid rgba(216, 231, 223, 0.5);
		overflow: scroll;
		overflow-x: hidden;
	}

	.technicalDoc {
		margin-left: 0;
		padding-left: 10px;
		height: 100%;
		margin-right: 0;
		padding-right: 0;
		padding-top: 20px;
	}

	.content-box {
		/*float: right;*/
		position: absolute;
		top: 0;
		right: 0;
		height: 100%;
		width: 85%;

	}
	.nav_bar{
		position: absolute;
		top:50%;
		margin-top:-15px;
		right: 0;
		width: 10px;
		height: 30px;
		line-height: 30px;
		background-color: #42b983;
		cursor: pointer;
		color: white;

	}
	.message-box{
		width: 98%;
		height: 50px;
		border-bottom: 1px solid #ccc
	}
	.message-box li{
		font-weight: 700;
		width: 80px;
		height: 35px;
		line-height: 35px;
		float: left;
		margin-left: 20px;
		margin-top: 8px;
		list-style: none;
	}
	.message-box .add-li,.message-box .delete-li,.message-box .diff-li{
		font-weight: 500;
		font-size: 14px;
		text-align: center;
		width: 60px;
		height: 20px;
		line-height: 20px;
		margin-top: 15px; 
		color: #fff;
	}
	.message-box .add-li,.add_bg{
		background: #5ab7e4;
	}
	.message-box .delete-li,.delete_bg{
		background: #909399;
	}
	.message-box .diff-li{
		background: #f56c6c;
	}
	.diff_bg{
		background: #f56c6c !important;
	}
	.delete_bg{
		background: #909399 !important;
	}
	.add_bg{
		background: #5ab7e4 !important;
	}
	.content-box-left,.content-box-right{
		float: left;
		width: 100%;
		height: 100%;
		overflow-y: auto;
	}
	.nav-box,.Asat-box,.Block-box,.IF-box,.Usecase-box,.Class-box,.Squence-box,.Statemachine,.DRBFM{
		width: 96%;
		margin: 0 auto;
		background: #f5fafc;
		margin-top: 10px;
		padding-bottom:10px;
		border-bottom:1px solid #a7aaad;
	}
	.DRBFM{
		margin-bottom: 50px;
	}

	/* 标题 */
	.nav-title{
		font-size: 22px;
		color: #606266;
		padding-left: 10px;
	}
	.title-h3{
		font-size: 18px;
		font-weight: 500;
		height: 25px;
		line-height: 25px;
		background: #6bcca0;
		padding-left: 10px;
		color: #fff;
	}
	.title-detail{
	    font-size: 12px;
	    color: #5e6d82;
	    text-align: left;
	    height: 20px;
	    line-height: 20px;
	    padding-left: 10px;
	}
	.title-content{
	    display: block;
	    margin-top: 10px;
	    margin-left: 20px;
	    font-size: 14px;
	}
	.content-msg{
		margin: 10px 0 0 20px;
	}
	.message{
		margin-left: 20px;
		text-align: center;
		padding: 12px;
		font-size: 14px;
		color: #5e6d82;
		border: 1px solid #ebeef5;
		margin-top: 10px;
	}
	.usecase-common-pic-box,.img-box,.Usecase_content,.input-box,.Resource-box,.Consider,{
		margin:10px 0 0 20px;
	}
	.content-size{
		color: #000;
	    font-size: 14px;
	    line-height:25px;
	    text-align: left;
	    margin:10px 0 0 20px;
	}
	.title-h4{
		font-size: 16px;
		font-weight: 500;
		padding-top: 10px;
		border-top: 1px solid #ccc;
	}
	.img-style{
		display: block;
		width: 95%;
		/*cursor: pointer;*/
	}
	.message-box .return_btn{
		float: right;
		text-align: center;
		cursor: pointer;
	}
	.diff-title{
		font-size: 18px;
		margin-left: 20px;
		color: #606266;
		overflow: hidden;
	}
	.diff-title-content-fl{
		float: left;
	}
	.diff-title-content-fr{
		float: right;
		margin-right: 20px;
	}
	.content-box-left-box,.content-box-right-box{
		position: relative;
		float: left;
		width: 49.5%;
		height: 95%;
	}
	.oldversion{
		color: #6bcca0
	}
	.table-span{
		display: block;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		-o-text-overflow:ellipsis
	}
	.Asa-display{
		padding: 5px;
	}
	@media screen and (max-width: 1420px) {
	    .table-span{
	    	width: 180px
	    }
	}
	@media screen and (max-width: 1200px) {
	    .table-span{
	    	width: 100px
	    }
	}
	@media screen and (max-width: 1366px) {
		.tree-box {
			width: 180px;
		}
		.content-box {
			width: 840px;
		}
		.tree-box {
			width: 20%;
		}
		.content-box {
			width: 80%;
		}
	}
	@media screen and (max-width: 1024px) {
		#File-Modle-box{
			width: 1024px;
		}
		.tree-box {
			width: 20%;
		}
		.content-box {
			width: 80%;
		}
	}
</style>
