<template>
	<div id="Map_Modle_First" >
		<div id="hy" class="header">
			<el-breadcrumb separator="/" class="bread">
				<el-breadcrumb-item :to="{ path: '/tagl/Map_Modle' }">框架图一览</el-breadcrumb-item>
				<el-breadcrumb-item>iAuto2.0</el-breadcrumb-item>
				<el-breadcrumb-item>17cy</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="content_box">
			<div class="parent">
				<span></span>
				<div class="parent_mod" v-for="item in data1" @dblclick="Get_Other_To_Main(1,item)">
					<div class="parent_mod_info" >
						<el-popover
						placement="top-start" width="200" trigger="hover" >
							<i slot="reference" class="el-icon-info"></i>
							<li><el-button type="text" @click="">增加系统设计</el-button></li>
						</el-popover>
					</div>
					<div class="parent_mod_name">
						<span>{{item.name}}</span>
						<span class="parent_mod_chenge"></span>
					</div>
					
					<div class="parent_mod_del">
						<el-button  type="info" icon="el-icon-message" circle
						@click=''></el-button>
					</div>
				</div>
				
			</div>
			<div class="mid">
				<div class="main_mod" v-model="data2" >
					<div class="main_mod_info">
						<i class="el-icon-info main_mod_first" v-popover:file_info_pop></i>
					</div>
					<div class="main_mod_name">
						<span>{{data2.layer}}</span>
						
					</div>
					<div class="main_mod_del">
						<el-button type="info" icon="el-icon-message" circle @click='go_file_model()'></el-button>
					</div>
				</div>
			</div>
			<!-- <div class="children" >
				<div class="children_mod" v-for="item in data2.modules" @dblclick="Get_Other_To_Main(2,item)">
					<div class="children_mod_info" >
						<el-popover
						placement="top-start" width="200" trigger="hover" >
							<i slot="reference" class="el-icon-info"></i>
							<li>
								<el-button type="text" @click="add_file_basic()">增加基本设计</el-button>
							</li>
							<li>
								<el-button type="text" @click="add_file_detil()">增加详细设计</el-button>
							</li>
						</el-popover>
					</div>
					<div class="children_mod_name">
						<span>{{item}}</span>
						<span class="children_mod_chenge"></span>
					</div>
					<div class="children_mod_del">
						<el-button type="info" icon="el-icon-message" circle
						@click='go_file_model()'></el-button>
					</div>
				</div>
				<div class="children_mod" v-for="item in data2.childlayers" @dblclick="Get_Other_To_Main(3,item)">
					<div class="children_mod_info">
						<el-popover
						placement="top-start" width="200" trigger="hover" >
							<i slot="reference" class="el-icon-info"></i>
							<li>
								<el-button type="text" @click="add_file_basic()">增加基本设计</el-button>
							</li>
							<li>
								<el-button type="text" @click="add_file_detil()">增加详细设计</el-button>
							</li>
						</el-popover>
					</div>
					<div class="children_mod_name">
						<span>{{item}}</span>
						<span class="children_mod_chenge"></span>
					</div>
					<div class="children_mod_del">
						<el-button type="info" icon="el-icon-message" circle
						@click='go_file_model()'></el-button>
					</div>
				</div>
				<div  v-show="" class="children_mod" v-for="item in data2.childlayers" @dblclick="Get_Other_To_Main(4,item)">
					<div class="children_mod_info">
						<el-popover
						placement="top-start" width="200" trigger="hover" >
							<i slot="reference" class="el-icon-info"></i>
							<li>
								<el-button type="text" @click="add_file_basic()">增加基本设计</el-button>
							</li>
							<li>
								<el-button type="text" @click="add_file_detil()">增加详细设计</el-button>
							</li>
						</el-popover>
					</div>
					<div class="children_mod_name">
						<span>{{item}}</span>
						<span class="children_mod_chenge"></span>
					</div>
					<div class="children_mod_del">
						<el-button type="info" icon="el-icon-message" circle
						@click='go_file_model()'></el-button>
					</div>
				</div>
			</div> -->
		</div>
		<!-- 背景 -->
		<div class="particles_box">
			<vue-particles
		        color="#fff"
		        :particleOpacity="0.7"
		        :particlesNumber="60"
		        shapeType="circle"
		        :particleSize="4"
		        linesColor="#fff"
		        :linesWidth="1"
		        :lineLinked="true"
		        :lineOpacity="0.4"
		        :linesDistance="150"
		        :moveSpeed="2"
		        :hoverEffect="true"
		        hoverMode="grab"
		        :clickEffect="true"
		        clickMode="push"
		        class="lizi"
			>
			</vue-particles>
			<router-view></router-view>
		</div>
		<!-- dialog -->
		<!-- <el-dialog title="新建模块" :visible.sync="MOD_add_flag" width="30%"
		:before-close="handleClose">
			<el-form ref="mod_form" :model="newForm" label-width="100px" size="mini">
				<el-form-item label="模块名">
					<el-input v-model="newForm.mod_name"></el-input>
				</el-form-item>
			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button type="primary" @click="Add_mod_Dialog()">确 定</el-button>
				<el-button @click="Cancel()">取 消</el-button>
			</span>
		</el-dialog>
		<el-dialog title="选择已有模块" :visible.sync="MOD_link_flag" width="30%"
		:before-close="handleClose">
			<el-form ref="mod_form" :model="linkForm" label-width="100px" size="mini">
				<el-form-item label="选择模块">
					<el-cascader placeholder="试试搜索" :options="link_mod_options" filterable 
					change-on-select v-model="linkForm .mod_id" class="MOD_link">
					</el-cascader>
				</el-form-item>
			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button type="primary" @click="Link_mod_Dialog()">确 定</el-button>
				<el-button @click="Cancel()">取 消</el-button>
			</span>
		</el-dialog>
		<el-dialog title="修改父模块名称" :visible.sync="MOD_change_parent_flag" width="30%"
		:before-close="handleClose">
			<el-form ref="mod_form" :model="newForm" label-width="100px" size="mini">
				<el-form-item label="新模块名">
					<el-input v-model="newForm.mod_name"></el-input>
				</el-form-item>
			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button type="primary" @click="Change_mod_Dialog()">确 定</el-button>
				<el-button @click="Cancel()">取 消</el-button>
			</span>
		</el-dialog>
		<el-dialog title="修改子模块名称" :visible.sync="MOD_change_children_flag" width="30%"
		:before-close="handleClose">
			<el-form ref="mod_form" :model="newForm" label-width="100px" size="mini">
				<el-form-item label="新模块名">
					<el-input v-model="newForm.mod_name"></el-input>
				</el-form-item>
			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button type="primary" @click="Change_mod_Dialog()">确 定</el-button>
				<el-button @click="Cancel()">取 消</el-button>
			</span>
		</el-dialog> -->
		<!-- 右侧隐藏模块 -->
		<div class="right_box">
			<p class="right_title"><i class="el-icon-d-arrow-right right_title_icon" @click='anmite()'></i> 关联技术文档</p>
			<!-- 目录树以及技术文档 -->
			<div class="right_content">
				<div class="fl content_tree">
					<h3 class="title_tree">Tag内容</h3>
					<li v-for="item in tree_data" style="list-style:none;padding-left:20px;cursor: pointer;" @click="">
						{{item.tag}}
					</li>
				</div>
				<div class="fr content_delete">
					<h3 class="title_tree">技术文档</h3>
					<p class="content_delete_msg">
						[技术文档test]
					</p>
				</div>
			</div>
		</div>
		<!--  -->
		<el-popover ref="file_info_pop" placement="right" width="200" trigger="hover">
			<li><el-button type="text" @click="add_file_basic()">增加基本设计</el-button></li>
			<li><el-button type="text" @click="add_file_detil()">增加详细设计</el-button></li>
		</el-popover>
		<el-popover ref="parent_info_pop" placement="right" width="200" trigger="hover">
			<li><el-button type="text" @click="MOD_add_flag = true">增加系统设计</el-button></li>
		</el-popover>
	</div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')

export default{
	data(){
		return {
			fullscreenLoading:false,
			MOD_add_flag:false,
			MOD_link_flag:false,
			MOD_change_parent_flag:false,
			MOD_change_children_flag:false,
			newForm:{},
			linkForm:{},
			defaultProps: {label: "tag",children: 'sub_tags'},
			tree_data:[],
			data1:[],
			data2:{
				// "layer": "framework",
				// "postion": "(0, 1),(2, 3)",
				// "childlayers": ["abi"],
				// "modules": ["AppFramework"]
			},
			data3:[],
			link_mod_options: [
			{
				"layer": "framework",
				"postion": "(0, 1),(2, 3)",
				"childlayers": ["abi"],
				"modules": ["AppFramework"]
			},
			{
				"layer": "framework",
				"postion": "(0, 1),(2, 3)",
				"childlayers": ["abi"],
				"modules": ["AppFramework"]
			},
			{
				"layer": "framework",
				"postion": "(0, 1),(2, 3)",
				"childlayers": ["abi"],
				"modules": ["AppFramework"]
			},
			{
				"layer": "framework",
				"postion": "(0, 1),(2, 3)",
				"childlayers": ["abi"],
				"modules": ["AppFramework"]
			}],

		}
      },
    mounted(){
     	this.Get_TAG_data()
     	this.getTableMain()
     	this.getTableChildren()
     	this.getTableParent()
    },
    methods:{
    	getTableParent(){
			this.$axios.get("../../../static/DataDevice.json")	
			.then(res =>{
				
				this.data1 = res.data
			})
			.catch(err => {
			})	
		},
		getTableMain(){
			this.$axios.get("../../../static/DataLayer.json")	
			.then(res =>{
				this.data2 = res.data
			})
			.catch(err => {
			})	
		},
		getTableChildren(){
			this.$axios.get("../../../static/DataModule.json")	
			.then(res =>{
				this.data3 = res.data
			})
			.catch(err => {
			})	
		},
		Get_Other_To_Main(type,item){
			if(type ==1){ //是否是device
				this.$axios.get("../../../static/DataDevice.json")	
				.then(res =>{
					this.data2 = res.data
				})
				.catch(err => {
					console.log(err.data,"P")
				})	
			}else if(type==3){//是否是中间层
			}else if(type==2){//是否是底层
			}
			
		},
		Add_mod_Dialog(){

		},
		Link_mod_Dialog(){

		},
		Change_mod_Dialog(){

		},
		Cancel(){
			this.$confirm('确认关闭？')
			.then(_ => {
				// this.sizeForm = {parent_tag_id:'',tag:''};
				this.MOD_add_flag = false;
				this.MOD_link_flag = false;

			})
			.catch(_ => {});
		},
		handleClose(done) {
			this.$confirm('确认关闭？')
			.then(_ => {
				done();
			})
			.catch(_ => {});
		},
		Get_TAG_data(){
			this.$axios.get(this.Ip+'/TagTree').then(res=>{
				if(res.data.result == "OK"){
					this.tree_data = res.data.content
				}else{

				}
			}).catch(err=>{
				console.log(err)
			})
		},
		node_click(data) {

		},
		add_file_basic(){
			this.$router.push('/tagl/File_Modle')
		},
		add_file_detil(){
			this.$router.push('/tagl/File_Modle')
		},
		anmite(){
			$('.right_box').animate({"right":-800},500,function(){
				$('.right_box').hide()
			})
		},
		go_file_model(){
			this.$router.push('/tagl/File_design/basic_design_template')
		},
		go_markdown(){
			this.$router.push('/tagl/Markdown')
		}
    }
}
</script>

<style scoped>
	#Map_Modle_First{
		position:relative;
		min-width:1000px;
		min-height:550px;
		width: 100%;
		height: 100%;
		background: -webkit-linear-gradient(left, #fff , #aaa); /* Safari 5.1 - 6.0 */
		background: -o-linear-gradient(right, #fff, #aaa); /* Opera 11.1 - 12.0 */  
		background: -moz-linear-gradient(right, #fff, #aaa); /* Firefox 3.6 - 15 */ 
		background: linear-gradient(to right, #fff, #aaa); /* 标准的语法 */ 
		overflow: auto;
	}
	.header{
		width: 100%;
		min-height: 80px;
		height: 5%;
		min-height: 28.8px;
		/*background-color:wg;*/
		/*border: solid 1px red;*/
	}
	.parent{
		float: left;
		width: 100%;
		min-width: 533.4px;
		height: 30%;
		min-height: 172.8px;
		/*background-color: pink;*/
		overflow: hidden;
		/*border: solid 1px yellow;*/
	}
	.mid{
		float: left;
		width: 100%;
		min-width: 533.4px;
		height: 30%;
		/*min-height: 203.4px;*/
		margin: 5% 0;
	}
	.right{
		float: right;
		width: 30%;
		min-width: 204.8px;
		height: 70%;
		min-height: 403.2px;
		/*background-color: brown;*/
		/*border: solid 1px green;*/
	}
	.right_close{
		position: absolute;
		right: 0;
		top:40px;
		width: 40%;
		min-width: 204.8px;
		height: 90%;
		min-height: 403.2px;
		/*background-color: brown;*/
		/*display: none;*/
	}
	.children{
		float: left;
		width: 100%;
		min-width: 533.4px;
		height: 30%;
		min-height: 172.8px;
		/*background-color: blue;*/
		/*border: solid 1px green;*/
	}
	.bread{
		padding-top: 12px;
		padding-bottom: 10px;
		padding-left: 20px;
	}
	.parent_mod{
		float: left;
		width: 160px;
		height: 160px;
		background: #409EFF;
		color: white;
		border-radius:25px;
		/*margin-left: 160px;*/
		margin-left: 40%;
		margin-top:20px;
	}
	.parent_mod_info{
		padding-top: 10px;
		padding-left: 132px;
	}
	.parent_mod_name{
		width: 100%;
		height: 40px;
		line-height: 40px;
		text-align: center;
	}
	
	.parent_mod_chenge{
		
	}
	.parent_mod_del{
		width: 100%;
		text-align: center;
		color: black;
	}
	.add_parent_mod{
		float: left;
		width: 160px;
		height: 160px;
		color: black;
		border-radius:25px;
		margin-left: 30px;
		margin-top:20px;
		border: 1px dashed #95C3F4;
	}
	.main_mod{
		width: 160px;
		height: 160px;
		background: #452AF4;
		color: white;
		border-radius:25px;
		margin-left: 40%;
		margin-top:20px;
	}
	.main_mod_info{
		padding-top: 10px;
		padding-left: 132px;
	}
	.main_mod .main_mod_name{
		width: 100%;
		height: 40px;
		line-height: 40px;
		text-align: center;
	}
	.main_mod .main_mod_del{
		width: 100%;
		text-align: center;
		color: black;
	}
	.children_mod{
		float: left;
		width: 160px;
		height: 160px;
		background: #409EFF;
		color: white;
		border-radius:25px;
		margin-left: 160px;
		margin-top:20px;
	}
	.children_mod_info{
		padding-top: 10px;
		padding-left: 132px;
	}
	.children_mod_name{
		width: 100%;
		height: 40px;
		line-height: 40px;
		text-align: center;
	}
	.children_mod_del{
		width: 100%;
		text-align: center;
		color: black;
	}
	.add_children_mod{
		float: left;
		width: 160px;
		height: 160px;
		color: black;
		border-radius:25px;
		margin-left: 30px;
		margin-top:20px;
		border: 1px dashed #95C3F4;
	}
	.particles_box{
		width: 100%;
		height: 600px;
		position: relative;
	}
	#particles-js{
		position: absolute;
		top: 0;
		left: 0;
		height: 700px;
		width: 100%;
	}
	.content_box{
		width: 100%;
		position: absolute;
		z-index: 3
	}
	.right_box{
		width: 670px;
		height: 100%;
		background: rgba(253,253,253,.4);
		position: absolute;
		z-index: 9;
		top: 0;
		right:-800px;
		display: none;
	}
	.filter-tree{
		background: rgba(253,253,253,.01);
	}
	.right_title{
		width: 95%;
		height: 30px;
		line-height: 30px;
		font-size: 16px;
		color: #606266;
		font-weight:700;
		padding-left:20px;
	}
	.right_title_icon{
		cursor: pointer;
		font-size: 22px;
	}
	.right_content{
		width: 100%;
		/*height: 95%;*/
		/*background: pink;*/
		overflow-y: scroll;
	}
	.fl{
		float: left;
	}
	.fr{
		float: right;
	}
	.content_tree{
		width: 40%;
	}
	.title_tree{
		margin: 10px 0 10px 5px;
		width: 50%
	}
	.title_tree span{
		float: right;
		font-weight: 500;
		font-size: 14px;
		transition: all 0.5s linear;
	}
	.title_tree span:hover{
		color: #42b983;
	}
	.content_delete{
		width: 60%;
	}
	.content_delete_msg{
		width: 100%;
		font-size: 14px;
		color: #606266;
	}
	.content_delete_size{
		float: right;
		margin-right:15%;
		cursor: pointer;
		transition: all 0.5s linear;
	}
	.content_delete_size:hover,.right_title_icon:hover{
		transition: 0.6s;
		color: #42b983;	
	}
/*	@media only screen and (max-width: 1024px) {
		
	}*/
</style>

