<template>
	<div id="Map_Modle_First" >
		<div id="hy" class="header">
			<el-breadcrumb separator="/" class="bread">
				<el-breadcrumb-item :to="{ path: '/' }">框架图一览</el-breadcrumb-item>
				<el-breadcrumb-item><a href="/"></a></el-breadcrumb-item>
			</el-breadcrumb>
		</div>
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
		<div class="map_modle_content">
			<ul class="map_modle_fl fl">
				<li v-for="(itme,index) in map_modle_list">
					<div class="map_modle_first_box"  @click="show_li(index)">
						{{itme.name}}
					</div>
					<!-- 第二层 -->
					<ul class="map_modle_fl_two_ul">
						<li @click='go_map_model_deep()'>
							<div class="map_modle_first_box">
								17cy
							</div>
						</li>
					</ul>
				</li>
			</ul>
			<!-- <ul class="map_modle_fr fr">
				<li @click="open_popup()">添加框架图</li>
			</ul> -->
		</div>
		<el-dialog title="框架图添加" :visible.sync="dialogFormVisible">
			<span>框架图名:</span><el-input v-model="map_modle_name" class="map_append_ipt"></el-input>
			<div slot="footer" class="dialog-footer">
				<el-button @click="dialogFormVisible = false">取 消</el-button>
				<el-button type="primary" @click="ipt_append()">确 定</el-button>
			</div>
		</el-dialog>
	</div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default{
	mounted(){
		
	},
	data(){
      return {
      	dialogFormVisible:false,
      	map_modle_name:"",
      	map_modle_list:[{"name":"iauto2.0"}]
      }
    },
    methods: {
    	open_popup(){
    		this.dialogFormVisible = true
    	},
    	ipt_append(){
    		if(this.map_modle_name != ""){
    			this.map_modle_list.push({"name":this.map_modle_name})
    			this.dialogFormVisible = false
    			this.map_modle_name = ""
    		}else{
    			this.$message({
			        message: '框架图名不允许为空!'
		       })
    		}
    	},
    	show_li(index){
    		$(".map_modle_fl_two_ul>li").eq(index).toggle(function(){
    		})
    	},
    	go_map_model_deep(){
    		this.$router.push('/tagl/Map_Modle_Deep')
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
	.fl{
		float: left;
	}
	.fr{
		float: right;
	}
	.header{
		width: 100%;
		min-height: 80px;
		height: 5%;
		min-height: 28.8px;
	}
	
	.bread{
		padding-top: 12px;
		padding-bottom: 10px;
		padding-left: 20px;
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
	.map_modle_content{
		position: absolute;
		top: 36px;
		left: 0;
		width: 100%;
		z-index: 3
	}
	.map_modle_fl{
		width: 20%;
	}
	.map_modle_fl li,.map_modle_fr li{
		width: 90%;
		border: 1px solid #ccc;
		margin: 10px 0 0 10px;
	}
	.map_modle_fl>li .map_modle_first_box,.map_modle_fr li{
		cursor: pointer;
		width: 100%;
		height: 45px;
		padding-left: 50px;
		line-height:45px;
		font-weight: bold;
		font-size: 14px;
		margin-bottom: 20px;
		cursor: pointer;
		background: -webkit-linear-gradient(left, #ccc , #f0f0f0); /* Safari 5.1 - 6.0 */
		background: -o-linear-gradient(right, #ccc, #f0f0f0); /* Opera 11.1 - 12.0 */  
		background: -moz-linear-gradient(right, #ccc, #f0f0f0); /* Firefox 3.6 - 15 */ 
		background: linear-gradient(to right, #ccc, #f0f0f0); /* 标准的语法 */ 
		/*margin-left: 15px;*/
		list-style: none;
	}
	.map_modle_fl>li .map_modle_first_box:hover{
		box-shadow: inset 0 1px 3px rgba(0,0,0,0.2),0 1px 0 #fff;
		transition: 0.6s;
		-moz-transition: 0.6s; /* Firefox 4 */
		-webkit-transition: 0.6s; /* Safari 和 Chrome */
		-o-transition: 0.6s;
	}
	.map_modle_fl_two_ul>li{
		/*display: none;*/
		margin-bottom: 10px;
	}
	.map_modle_fr{
		width:10%;
		min-width: 200px;	 
	}
	.map_append_ipt{
		width: 300px;
		margin-left: 20px;
	}
	.map_modle_fl_two_ul{
		margin-left: 15%;
		list-style: none;
	}
</style>

