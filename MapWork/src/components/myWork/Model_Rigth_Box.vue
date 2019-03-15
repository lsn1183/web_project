<template>
	<div class="right_box">
		<!-- <p class="right_title"><i class="el-icon-d-arrow-right right_title_icon" @click='anmite()'></i> 关联技术文档</p> -->
		<!-- 目录树以及技术文档 -->
		<div class="right_content">
			<div class="fl content_tree">
				<i class="el-icon-d-arrow-right right_title_icon" @click='anmite()'><span>隐藏</span></i>
				<h4 class="title_tree">Tag内容</h4>
				<li v-for="item in tree_data" :key="item.key" style="list-style:none;padding-left:20px;cursor: pointer;" @click="treeList_click(item.tag_id)">
					{{item.tag}}
				</li>
			</div>
			<div class="fr content_delete">
				<h4 class="title_tree" style="margin-top: 32px">技术文档</h4>
				<li v-for="(item,index) in  doc_list" :key="item.key">{{index+1}} . {{item.doc_title}}</li>
				<div class="form_page">
					<el-pagination
					id="list_page"
					@current-change="listPageChange"
					:current-page="page"
					:page-size="page_size"
					layout="total, prev, pager, next,jumper"
					:total="changdu"
					></el-pagination>
				</div>
			</div>
		</div>
	</div>
	
</template>
<script>
export default{
	data(){
		return {
			tree_data:[],
			doc_list:[],
			page:1,
			page_size: 30,
			changdu: 0,
			tag_id:null,
			
		}
      },
    mounted(){
		this.Get_TAG_data()
    },
    components: {
    },
    methods:{
		treeList_click(tag_id){
			if(tag_id){
				let id = tag_id
				this.Get_DocList(tag_id);
			}
			
			
		},
    	Get_TAG_data(){
			this.$axios.get(this.Ip+'/TagTree').then(res=>{ 
				if(res.data.result == "OK"){
					this.tree_data = res.data.content
				}
			}).catch(err=>{
				console.log(err)
			})
		},
		Get_DocList(tag_id){
			this.tag_id = tag_id
			this.$axios.get(this.Ip + "/DocByTag/" + this.page +"/"+ this.page_size +"/" + tag_id).then(res => {
				this.doc_list = []
				this.doc_list = res.data.content;
				this.changdu = res.data.count
			})
		},
		// 分页
		listPageChange(val){
			this.page = val;
			this.$axios.get(this.Ip + "/DocByTag/" + this.page +"/"+ this.page_size +"/" + this.tag_id).then(res => {
				this.doc_list = []
				this.doc_list = res.data.content;
				this.changdu = res.data.count
			})	
		},
		anmite(){
			$('.right_ct').animate({"right":-760},500,function(){
				$('.right_ct').hide()
			})
		},
    }
}
</script>

<style scoped>
	.right_box{
		width: 760px;
		min-width: 360px;
		height: 100%;
		background: #ECF3F8;
		position: absolute;
		z-index: 9;
		top: 0;
		right:-10px;
		overflow-y:auto ;
		/* display: none; */
	}
	.right_title{
		width: 100%;
		height: 30px;
		line-height: 30px;
		font-size: 16px;
		color: #606266;
		font-weight:700;
		padding-left:20px;
	}
	.title_tree{
		margin: 10px;
		/*width: 50%*/
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
	.right_title_icon{
		cursor: pointer;
		font-size: 22px;
	}
	.right_title_icon span{
		font-size: 16px;
	}
	.right_content{
		width: 100%;
		/*height: 95%;*/
		/*background: pink;*/
		overflow-y: scroll;
	}
	.fl{
		float: left;
		overflow-y: auto;
	}
	.content_tree{
		width: 25%;
		min-width: 10%;
	}
	.fr{
		float: right;
		overflow-y: auto;
	}
	.content_delete{
		width: 70%;
		min-width: 40%;
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
	.right_content li{
		margin-bottom: 5px;
		font-size:	14px;
		color: #040405;
		width: 100%;
		list-style: none;
		/* min-width: 50%; */
		
	}
	.content_delete li{
		min-width: 45%;
		/* min-width: 200px; */
	}
	.content_delete .form_page{
		width: 60%;
	}
	@media screen and (max-width:1024px){
		.right_content li{
			font-size: 10px;
		}
		.right_box{
			width: 550px;
			min-width: 80px;
			height: 100%;
			background: #ECF3F8;
			position: absolute;
			z-index: 9;
			top: 0;
			right:-10px;
			overflow-y:auto ;
		}
		.content_tree{
			width: 25%;
		}
		.content_delete{
			width: 70%;
		}
	}
	/*@media screen and (max-width:1366px){
		.right_content li{
			font-size: 10px;
		}
		.right_box{
			width: 75%;
			min-width: 180px;
			right:-180px;
		}
	}*/
	
</style>

