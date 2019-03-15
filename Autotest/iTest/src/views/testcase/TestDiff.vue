<template>
	<div class='container'>
		<ul class="diff-nav">
			<li>图例:</li>
			<li class="add-li">新增</li>
			<li class='diff-li'>修改</li>
			<li class='delete-li'>删除</li>
		</ul>
		<div class="content-box">
			<div class="left-content-box">
				<h1 class="diff-title">
					<p class="diff-title-content-fl">OldVersion</p>
					<p class="diff-title-content-fr">
						<!-- <el-button type="text">上一版</el-button> -->
						<!-- <el-button type="text">下一版</el-button> -->
					</p>
				</h1>
				<div class="content-left">
					<div class="nav-box">
						<h2 class="nav-title">BasicDesign_GuideDataProvide</h2>
						<p class="title-detail">由 Admin 创建，最终由 Admin 修改于 2018-09-20 版本 0.1.7</p>
						<p class="title-content">详细内容</p>
					</div>
					<!-- 摘要 -->
					<div class="abstract-box">
						<h3 class="title-h3">
							<span>摘要</span>
						</h3>
						<p class="message">暂无变更</p>
					</div>
					<!-- 前提 -->
					<div class="premise-box">
						<h3 class="title-h3">
							<span>前提</span>
						</h3>
						<p class="message">暂无变更</p>
					</div>
					<!-- 重要性 -->
					<div class="importance-box">
						<h3 class="title-h3">
							<span>重要性</span>
						</h3>
						<p class="message">暂无变更</p>
					</div>
					<!-- 测试方式 -->
					<div class="test-mode">
						<h3 class="title-h3">
							<span>测试方式</span>
						</h3>
						<p class="message">暂无变更</p>
					</div>
					<!-- 仕向地 -->
					<div class="place-box">
						<h3 class="title-h3">
							<span>仕向地</span>
						</h3>
						<p class="message">暂无变更</p>
					</div>
					<!-- 自定义字段 -->
					<div class="custom-fields">
						<h3 class="title-h3">
							<span>自定义字段</span>
						</h3>
						<p class="message">暂无变更</p>
					</div>
					<!-- 测试步骤 -->
					<div class="testing-procedure">
						<h3 class="title-h3">
							<span>测试步骤</span>
						</h3>
						<p class="message">暂无变更</p>
					</div>
				</div>
			</div>
			<div class="right-content-box">
				
			</div>
		</div>
	</div>
</template>
<script>
	export default{
		name: 'testCaseDiff',
		data() {
			return {}
		},
		mounted(){

		},
		methods:{

		}
	}
</script>
<style scoped>
	.container{
		position: relative;
		width: 100%;
		height: 100%;
	}
	.diff-nav{
		width: 100%;
		height: 50px;
		border-bottom: 1px solid #ccc;
	}
	.diff-nav li{
		font-weight: 700;
		width: 80px;
		height: 35px;
		line-height: 35px;
		float: left;
		margin-left: 20px;
		margin-top: 8px;
		list-style: none;
		font-size: 18px;
	}
	.diff-nav .add-li, .diff-nav .delete-li, .diff-nav .diff-li {
	    font-weight: 500;
	    font-size: 14px;
	    text-align: center;
	    width: 60px;
	    height: 20px;
	    line-height: 20px;
	    margin-top: 15px;
	    color: #fff;
	}
	.diff-nav .add-li{
		background-color: #5ab7e4
	}
	.diff-nav .diff-li{
		background-color: #f56c6c
	}
	.diff-nav .delete-li{
		background-color: #909399
	}
	.content-box{
		padding: 0 20px;
		min-width: 1000px;
		height: 100%;
	}
	.left-content-box, .right-content-box{
		position: relative;
	    float: left;
	    width: 49.5%;
	    height: 95%;
	}

	.right-content-box{
		background-color: #ccc
	}
	.diff-title{
		font-size: 18px;
		margin-left: 20px;
		color: #606266;
		height: 40px;
		overflow: hidden;
	}
	.diff-title-content-fl{
		float: left;
	}
	.diff-title-content-fr{
		float: right;
		margin-right: 20px;
	}
	.content-left{
		width: 100%;
		height: 100%;
		overflow-y: auto;
	}
	/* 统一边距、背景颜色、下划线 */
	.nav-box, .abstract-box, .premise-box, .importance-box, .test-mode, .place-box, .custom-fields, .testing-procedure{
		width: 96%;
		margin: 0 auto;
		background: #f5fafc;
		margin-top: 10px;
		padding-bottom: 10px;
		border-bottom: 1px solid #a7aaad;
	}
	/**/
	.nav-title{
		font-size: 22px;
	    color: #606266;
	    padding-left: 10px;
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
	.title-h3{
	    font-size: 18px;
	    font-weight: 500;
	    height: 25px;
	    line-height: 25px;
	    background: #6bcca0;
	    padding-left: 10px;
	    color: #fff;
	}
	.message {
	    margin-left: 20px;
	    text-align: center;
	    padding: 20px;
	    font-size: 14px;
	    color: #5e6d82;
	    border: 1px solid #ebeef5;
	    margin-top: 10px;
	}
	.testing-procedure{
		margin-bottom: 60px;
	}
</style>