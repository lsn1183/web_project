<template>
	<div class='dashbardShow-box'>
		<div class="quantity-box">
			<div class="content-top">
				<h2 class="quantity-title">
					<span>数量统计列表</span>
				</h2>
				<div class="quantity-content">
					<div class="quantity-left" id="quantity-left">
						
					</div>
					<div class="quantity-right" id="quantity-right">
						
					</div>
				</div>
			</div>
			<div class="content-bottom">
				<h2 class="quantity-title">
					<span>执行结果统计</span>
				</h2>
				<div class="result-content">
					<div class="result-msg" id="result-msg"></div>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
import {get_dashboard, get_StackChart, get_PieChart} from '@/api/dashboard'
export default {
    name: 'dashbardShow',
    data() {
        return {
        	screenWidth: document.body.clientWidth,
        	timer:false,
        }
    },
    // 路由迁移钩子函数
    activated: function() {
        const self = this
        window.onresize = function(){
            self.screenWidth = document.body.clientWidth
        }
        this.left_drawLine();
        this.right_drawLine();
        this.bottom_drawLine();
    },
    mounted() {

    },
    watch :{
    	screenWidth(val){
    		this.screenWidth = val
    		if(!this.timer){
    			this.timer = true
    			let self = this
    			setTimeout(function(){
    				self.left_drawLine();
    				self.right_drawLine();
    				self.bottom_drawLine();
    				self.timer = false
    			},400)
    		}
    	}
    },
    methods: {
    	left_drawLine(){
            // 获取节点
            let myChart_left = this.$echarts.init(document.getElementById('quantity-left'))
            // 初始化折线图数据
            let option_left = {
                    title: {
                        text: '测试用例统计'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data:[]
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    toolbox: {
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    },
                    yAxis: {    
                        type: 'value'
                    },
                    series: [
                    ]
                };
            // 获取折线图数据
            get_dashboard('a').then(res=>{
                option_left.xAxis.data = res.data.date_list
                if(res.data.result == 'OK'){
                    option_left.legend.data = res.data.model_list
                    for(let series_i = 0; series_i<res.data.series.length;series_i++){
                        option_left.series.push({
                            name:res.data.series[series_i].model,
                            type:'line',
                            stack: '总量',    
                            data:res.data.series[series_i].data
                        }) 
                    }
                }
                // 生成折线图
                myChart_left.setOption(option_left);
            })

    		
    		// 监听屏幕缩放  图表自适应
    		window.addEventListener("resize",function(){
    		    myChart_left.resize();
    		 });
            // 图表上的点击方法
    		myChart_left.on('click', function (params) {
    			console.log(params)
    		})
    	},
    	right_drawLine(){
    		let myChart_right = this.$echarts.init(document.getElementById('quantity-right'))
    		let option_right = {
    			title : {
    			        text: '关键字统计',
    			        subtext: '',
    			        x:'center'
    			    },
    			    tooltip : {
    			        trigger: 'item',
    			        formatter: "{a} <br/>{b} : {c} ({d}%)"
    			    },
    			    legend: {
    			        orient: 'vertical',
    			        left: 'left',
    			        data: []
    			    },
    			    series : [
    			        {
    			            name: '访问来源',
    			            type: 'pie',
    			            radius : '55%',
    			            center: ['50%', '60%'],
    			            data:[], // 显示数据
    			            itemStyle: {
    			                emphasis: {
    			                    shadowBlur: 10,
    			                    shadowOffsetX: 0,
    			                    shadowColor: 'rgba(0, 0, 0, 0.5)'
    			                }
    			            }
    			        }
    			    ]
    		}
            get_PieChart().then(res=>{
                if(res.data.result == 'OK'){
                    option_right.series[0].data = res.data.data
                    option_right.legend.data = res.data.key_word_data
                }
                // 生成饼图
                myChart_right.setOption(option_right);
                // 监听屏幕缩放  图表自适应
                window.addEventListener("resize",function(){
                    myChart_right.resize();
                });
            })
    	},
    	bottom_drawLine(){
    		let myChart_bottom = this.$echarts.init(document.getElementById('result-msg'))
    		let option_bottom = {
    		    tooltip : {
    		        trigger: 'axis',
    		        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
    		            type : 'line'        // 默认为直线，可选为：'line' | 'shadow'
    		        }
    		    },
    		    legend: {
    		        data:[]
    		    },
    		    grid: {
    		        left: '5%',
    		        right: '4%',
    		        bottom: '10%',
    		        containLabel: false
    		    },
    		    xAxis : [
    		        {
    		            type : 'category',
    		            data : []
    		        }
    		    ],
    		    yAxis : [
    		        {
    		            type : 'value'
    		        }
    		    ],
    		    series : [
    		        
    		    ]
    		};
            get_StackChart().then(res=>{
                console.log(res,'bottom')
                option_bottom.xAxis[0].data = res.data.date_list
                if(res.data.result == 'OK'){
                    option_bottom.legend.data = res.data.result_list
                    for(let item = 0;item<res.data.series.length;item++){
                        option_bottom.series.push({
                            'name':res.data.series[item].name,
                            'data':res.data.series[item].data,
                            'type':'bar',
                            'stack': '总量',
                            'label': {
                                normal: {
                                    show: true,
                                    position: 'insideRight'
                                }
                            }
                        })
                    }
                }
                myChart_bottom.setOption(option_bottom);
            })
            // 监听屏幕缩放  图表自适应
            window.addEventListener("resize",function(){
                myChart_bottom.resize();
             });
    	}
    }
}
</script>
<style scoped>
	.dashbardShow-box{
		position: relative;
		width: 100%;
		height: 100%;
		overflow:scroll;
	}
	.quantity-box{
		width: 90%;
		margin:0 auto;
		margin-top:20px;
		min-width: 1000px;
	}
	.quantity-title{
		height: 40px;
		line-height: 40px;
	}
	.quantity-content,.result-content{
		overflow: hidden;
		height: 350px;
		margin-top: 30px;
	}
	.quantity-left{
		width: 60%;
		float: left;
		height: 100%;
	}
	.quantity-right{
		width: 39.5%;
		float: left;
		height: 100%;
	}
	.result-msg{
		width: 100%;
		height: 100%;
	}
</style>