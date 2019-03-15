<template>
	<div class="DEF_dialog"  id="dialog">
			<div class="DEF_dialog_html">
				<!-- dialog标题 -->
				<h2 class="DEF_dialog_title">
					<span class="DEF_dialog_size fl">标题</span>
					<!-- 点x关闭弹出框 -->
					<i class="fr el-icon-close" @click="DEF_dialog_close()"></i>
				</h2>
				<div class="DEF_arl_table">
					<!-- arl的新建保存等按钮，新建保存等功能都在这俩个地方加事件 -->
		   	    	<p style="height:30px" class="hu_sapn">
		   	    		<span class="fr DEF_hu_span" style="fontWeight:bold">保存</span>
		   	    		<span class="fr DEF_hu_span" style="fontWeight:bold;marginRight:30px">新建</span>
		   	    	</p>


	    	  	    <!-- HU表格 -->
	    	     	<div style="marginLeft:32px">
						<textarea name="" rows="" cols=""></textarea>
						<button>11</button>
						<button>22</button>
	    	     	</div>
		   	   	</div>
			</div>
	</div>
</template>

<script>
	export default{
		methods:{
			DEF_dialog_close(){
				this.$emit('show_dialog','')
			},
		}
	}
</script>

<style>
.DEF_arl_table{
	overflow: hidden;
	overflow: scroll;
	height: 700px;	
}

.DEF_hu_sapn span{
	height: 30px;
	line-height: 30px;
	cursor: pointer;
	margin-right: 30px;
}
.DEF_hu_sapn .fr:hover{
	color: #42b983
}
.DEF_dialog{
	width: 100%;
	height: 100%;
	background:rgba(0,0,0,.3);
	position: fixed;
	top:0;
	left: 0;
	right: 0;
	bottom: 0;
	z-index:2001;
}
.DEF_dialog_html{
	width: 80%;
	margin: 0 auto;
	height:785px;
	margin-top:100px;
    background: white;
    border-radius: 2px;
    box-shadow: 0 1px 3px rgba(0,0,0,.3);
    padding:10px 10px 10px 20px;
}
.DEF_dialog_title{
	width: 100%;
	height: 45px;
	line-height: 45px;
	margin-bottom: 30px;
}

</style>