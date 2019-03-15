<template>
	<div id="Map_Modle_First" >
		<div id="hy" class="header">
			<el-breadcrumb separator="/" class="bread">
				<el-breadcrumb-item :to="{ path: '/tagl/Map_Modle' }">框架图一览</el-breadcrumb-item>
				<el-breadcrumb-item><a href="/">APP</a></el-breadcrumb-item>
				<el-breadcrumb-item>模块一</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="content_box">
			<div class="parent">
				<span></span>
				<div class="add_parent_mod">
					<div class="parent_mod_name" style="margin-top:30px">
						<span>新增</span>
					</div>
					<div class="parent_mod_del">
						<el-button v-popover:add_parent_pop type="success" icon="el-icon-plus" circle></el-button>
					</div>
				</div>
				<div class="parent_mod">
					<div class="parent_mod_info" v-popover:parent_info_pop>
						<i class="el-icon-info"></i>
					</div>
					<div class="parent_mod_name">
						<span>APP</span>
						<span class="parent_mod_chenge"></span>
					</div>
					
					<div class="parent_mod_del">
						<el-button v-popover:del_parent_pop type="danger" icon="el-icon-delete" circle></el-button>
					</div>
				</div>
				
			</div>
			<div class="mid">
				<div class="main_mod">
					<div class="main_mod_info"><i class="el-icon-info main_mod_first"></i></div>
					<div class="main_mod_name">
						<span>模块一</span>
						
					</div>
					<div class="main_mod_del">
						<el-button type="info" icon="el-icon-message" circle @click='anmite_left()'></el-button>
					</div>
				</div>
			</div>
			<div class="children">
				<div class="add_children_mod">
					<div class="children_mod_name" style="margin-top:30px;margin-left: 8px">
						<span>新增</span>
					</div>
					<div class="parent_mod_del">
						<el-button v-popover:add_parent_pop type="success" icon="el-icon-plus" circle></el-button>
					</div>
				</div>
				<div class="children_mod">
					<div class="children_mod_info" v-popover:children_info_pop>
						<i class="el-icon-info"></i>
					</div>
					<div class="children_mod_name">
						<span>子模块一</span>
						<span class="children_mod_chenge"></span>
					</div>
					<div class="children_mod_del">
						<el-button v-popover:del_children_pop type="danger" icon="el-icon-delete" circle></el-button>
					</div>
				</div>
				
			</div>
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
		<el-dialog title="新建模块" :visible.sync="MOD_add_flag" width="30%"
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
		</el-dialog>
		<!-- 右侧隐藏模块 -->
		<div class="right_box">
			<p class="right_title"><i class="el-icon-d-arrow-right right_title_icon" @click='anmite()'></i> 关联技术文档</p>
			<!-- 目录树以及技术文档 -->
			<div class="right_content">
				<div class="fl content_tree">
					<h3 class="title_tree">Tag目录</h3>
					<el-tree class="filter-tree" :data="tree_data" :props="defaultProps" ref="tree2" @node-click="node_click">
					</el-tree>
				</div>
				<div class="fr content_delete">
					<h3 class="title_tree">技术文档</h3>
					<p class="content_delete_msg">
						[技术文档test]
						<span class="content_delete_size">删除</span>
					</p>
				</div>
			</div>
		</div>
		<!--  -->
		<el-popover ref="add_parent_pop" placement="right" width="200" trigger="click">
			<li><el-button type="text" @click="MOD_add_flag = true">新增</el-button></li>
			<li><el-button type="text" @click="MOD_link_flag = true">选择已有模块</el-button></li>
		</el-popover>
		<el-popover ref="parent_info_pop" placement="right" width="200" trigger="click">
			<li><el-button type="text" @click="MOD_add_flag = true">修改模块名称</el-button></li>
			<li><el-button type="text" @click="MOD_link_flag = true">选择已有模块</el-button></li>
		</el-popover>
		<el-popover ref="children_info_pop" placement="right" width="200" trigger="click">
			<li><el-button type="text" @click="MOD_add_flag = true">修改模块名称</el-button></li>
			<li><el-button type="text" @click="MOD_link_flag = true">选择已有模块</el-button></li>
		</el-popover>
		<el-popover ref="del_parent_pop" placement="right" width="200" trigger="click">
			<p>确定要删除该父模块吗？</p>
			<div style="text-align: right; margin: 0">
				<el-button size="mini" type="text" @click="visible2 = false">取消</el-button>
				<el-button type="primary" size="mini" @click="visible2 = false">确定</el-button>
			</div>
		</el-popover>
		<el-popover ref="del_children_pop" placement="right" width="200" trigger="click">
			<p>确定要删除该子模块吗？</p>
			<div style="text-align: right; margin: 0">
				<el-button size="mini" type="text" @click="visible2 = false">取消</el-button>
				<el-button type="primary" size="mini" @click="visible2 = false">确定</el-button>
			</div>
		</el-popover>
	</div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default{
	mounted(){
		//单双击并行方法
		function $(id){
		  return document.getElementById(id);
		}
		var timer=null;
		var self = this;
		$('hy').addEventListener('click',function(e){
			clearTimeout(timer);
			timer=setTimeout(function(){//初始化一个延时
		    self.getTable();
			},250)
		},false);
		$('hy').addEventListener('dblclick',function(){//双击事件会先触发两次单击事件，然后再执行双击事件，使用清除定时器来达到双击只执行双击事件的目的
			clearTimeout(timer);
			self.getTable2();
		},false);
	},
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
			link_mod_options: [
			{
				value: 'shejiyuanze',
				label: '设计原则',
				children: [{
					value: 'yizhi',
					label: '一致'
					}, {
					value: 'fankui',
					label: '反馈'
					}, {
					value: 'xiaolv',
					label: '效率'
					}, {
					value: 'kekong',
					label: '可控'
					}]
				}, 
			{
				value: 'daohang',
				label: '导航',
				children: [{
					value: 'cexiangdaohang',
					label: '侧向导航'
					}, {
					value: 'dingbudaohang',
					label: '顶部导航'
					}]
			}],

		}
      },
    mounted(){
     	this.Get_TAG_data()
    },
    methods:{
    	getTable(){
			this.$axios.get("../../../static/data.json")	
			.then(res =>{
				console.log(res.data,"222")
			})
			.catch(err => {
				console.log(err.data,"222")
			})	
		},
		getTable2(){
			this.$axios.get("../../../static/data.json")	
			.then(res =>{
				console.log(res.data,"3")
			})
			.catch(err => {
				console.log(err.data,"3")
			})	
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
		anmite(){
			$('.right_box').animate({"right":-800},500,function(){
				$('.right_box').hide()
			})
		},
		anmite_left(){
			$('.right_box').show()
			$('.right_box').animate({"right":0},500)
		}
    }
}
</script>

<style scoped>
	#Map_Modle_First{
		position:relative;
		min-width:1024px;
		min-height:768px;
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
		margin-left: 160px;
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
		padding-left: 60px;
	}
	
	.parent_mod_chenge{
		
	}
	.parent_mod_del{
		width: 100%;
		padding-left: 55px;
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
		background: #409EFF;
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
		padding-left: 60px;
	}
	.main_mod .main_mod_del{
		width: 100%;
		padding-left: 55px;
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
		padding-left: 50px;
	}
	.children_mod_del{
		width: 100%;
		padding-left: 55px;
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
		height: 95%;
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

	}
	.content_delete_size:hover,.right_title_icon:hover{
		transition: 0.6s;
		color: #42b983;	
	}
</style>

