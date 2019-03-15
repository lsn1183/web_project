<template>
	<div id="StyleTool">
		<div class="big_content">
			<form>
				<a href="javascript:;" class="file"><input type="file" @change="getFile($event)"/>点击选择文件<span style="color: #ccc;">(*zip)</span></a>
				<el-button size="small" type="primary" @click="upload($event)" v-loading.fullscreen.lock="fullscreenLoading" style="position: absolute;left:70%;">开始上传</el-button>
			</form>	
				
		</div>
	</div>
</template>

<script>
	export default {
		name:'StyleTool',
		data(){
			return{
				file:'',
				fullscreenLoading:false,
			}
		},
		mounted: function () {
			
		},
		methods:{
			getFile(event){
				this.file = event.target.files[0]
			},
			upload(event){
				if (this.file == ''){
					alert('请选择一个文件!');
					return;
				}
				this.fullscreenLoading=true;
				event.preventDefault()
				let formData = new FormData()
				formData.append('file',this.file)
				let config={
					headers:{
						'Content-Type':'multipart/form-data',
					}
				}
				
				this.$axios.post(this.Ip+'/StyleTool', formData, config)
				.then(res => {
					if (res.data.result=="OK") {
						window.location.href=this.Ip+res.data.data_path
						this.fullscreenLoading = false;
					} else {
						this.fullscreenLoading = false;
					}
				})
				.catch(res => {
					this.fullscreenLoading = false;
				})
			}
		}
	}
</script>

<style>
	.big_content {
	    width: 45%;
	    -webkit-box-shadow: 2px 1px 9px #ccc;
	    box-shadow: 2px 1px 9px #ccc;
	    margin: 0 auto;
	    margin-top:10%;
	    padding: 15px;
		position: relative;
	}
	.file{
		position: relative;
		display: inline-block;
		background-color: #fff;
		border-radius: 4px;
		border: 1px solid #42b983;
		padding: 5px 9px;
		overflow: hidden;
		color: #42b983 !important;
		text-decoration: none;
		text-indent: 0;
		font-size: 12px;
		width: 350px;
		margin-left: 2%;
	}
	.file input{
		position: absolute;
		right: 0;
		top: 0;
		opacity: 0;
		width: 100%;
    	height: 100%;
	}

</style>
