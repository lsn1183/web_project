<template>
	<div id="Spec-search">
		<div class="search-box warpper">
			<p class="search-title">Spec Search</p>
			<div class="select-box">
				<span style="font-weight:bold">项目</span>
				<el-select v-model="value" class='select-msg'>
				    <el-option
				      v-for="item in options"
				      :key="item.value"
				      :label="item.label"
				      :value="item.value">
				    </el-option>
				</el-select>
			</div>
			<el-input v-model="val" class='search-ipt'></el-input>
			<button class='search-btn' @click="search_content()">搜索式样书</button>
			<!-- <button class='search-btn search-btn-right'>搜索Anyplace</button> -->
		</div>
		<div class="table-box">
			<div class=" warpper">
				<p class="msg">
					共找到<span style="color:#f12525">{{length}}</span>条，当前返回<span style="color:#f12525">{{length}}</span>记录：
				</p>
				<el-table :data="tableData" border style="width: 100%" class='table-msg'>
				    <el-table-column prop="file_name" label="式样书">
				    	<template slot-scope="scope">
				    	    <a :href="scope.row.url" target="_blank"> &nbsp;{{scope.row.file_name}}</a>
				    	</template>
				    </el-table-column>
				    <el-table-column prop="title" label="章节名" width="350">
				    </el-table-column>
				</el-table>
			</div>
		</div>
	</div>
	
</template>
<script>
export default {
    data () {
        return {
        	val:'',
        	tableData: [],
        	options: [],
        	value:'',
        	length:0
        }
    },
    created () {
        
    },
    mounted () {
    	this.value = this.$route.params.proj
    	this.get_project()
    },
    watch: {
       $route(to, from) {
       		this.value = this.$route.params.proj	
       } 
    },
    methods: {
    	get_project(){
    		this.$axios.get(this.Ip + '/Project').then(res => {
    		    if(res.data.result == 'OK'){
    		    	for(let item = 0; item<res.data.content.length;item++){
    		        	this.options.push({
    		        		"value":res.data.content[item].proj_name,
    		        		"label":res.data.content[item].proj_name
    		        	})		
    		    	}
    		    }
    		})
    	},
    	search_content(){
    		this.$axios.get(this.Ip + '/FunSearch/'+ this.value + "/" +this.val).then(res => {
    		    if(res.data.result == 'OK'){
    		    	this.length = res.data.content.length
    		    	this.tableData = res.data.content
    		    }
    		})
    	}
    }
} 
</script>
<style scoped>
	#Spec-search{
		width: 100%;
		height: 100%;
	}
	.content-box{
		min-width:1000px;
		padding: 0 20px 0 20px;
	}
	.warpper{
		width: 75%;
		min-width: 1000px;
		margin: 0 auto;
	}
	.search-box{
		margin: 0 auto;
		padding-top: 20px;
		height: 62px;
		line-height: 42px;
	}
	.search-title{
		float: left;
		font-size: 20px;
		font-weight: bold;
		padding: 0 10px 0 0;
	}
	.search-ipt{
		position: relative;
		top: 1px;
		float: left;
		width: 40%;
	}
	.select-msg{
		width:100px;
	}
	.search-btn{
		float: left;
		height: 40px;
		border: 0 none;
		color: #fff;
		padding: 0 10px;
		position: relative;
		top: 2px;
		left: -2px;
		background:  #42b983;
		cursor:pointer;
		outline: none;
		border-radius: 2px;
	}
	.select-box{
		float: left;
		padding-right: 5px;
	}
	.search-btn-right{
		left: -4px;
		border-left:1px solid #eee
	}
	.table-box{
		width: 100%;
		overflow-y:scroll;
		margin-top: 20px;
		height: 700px;
	}
	.msg{
		height: 19px; 
		line-height: 19px;
		font-size: 14px;
		color: #909399
	}
	.table-msg{
		margin-top: 20px;
	}
</style>