<template>
	<div class="tree-map-box">
		<!-- <div class="particles_box">
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
		</div> -->
		<div id="myChart">
		</div>
	</div>
</template>

<script>
	export default {
		name: 'Tree_Map',
		data() {
			return {
				value_data:require('../../assets/js/data.json')
			}
		},
		mounted() {
			this.drawLine()
		},
		methods: {
			drawLine(){
			        // 基于准备好的dom，初始化echarts实例
			        let myChart = this.$echarts.init(document.getElementById('myChart'))
			        // 绘制图表
			        myChart.hideLoading();
			        function colorMappingChange(value) {
			                var levelOption = getLevelOption(value);
			                chart.setOption({
			                    series: [{
			                        levels: levelOption
			                    }]
			                });
			            }
			        var formatUtil = this.$echarts.format;
			        function getLevelOption() {
						return [
						    {
						        itemStyle: {
						            normal: {
						                borderColor: '#777',
						                borderWidth: 0,
						                gapWidth: 1
						            }
						        },
						        upperLabel: {
						            normal: {
						                show: false
						            }
						        }
						    },
						    {
						        itemStyle: {
						            normal: {
						                borderColor: '#555',
						                borderWidth: 5,
						                gapWidth: 1
						            },
						            emphasis: {
						                borderColor: '#ddd'
						            }
						        }
						    },
						    {
						        colorSaturation: [0.35, 0.5],
						        itemStyle: {
						            normal: {
						                borderWidth: 5,
						                gapWidth: 1,
						                borderColorSaturation: 0.6
						            }
						        }
						    }
						];
			        }
			        myChart.setOption({
			            title: {
			                       text: 'Disk Usage',
			                       left: 'center'
			                   },
			            tooltip: {
	                        formatter: function (info) {
	                            var value = info.value;
	                            var treePathInfo = info.treePathInfo;
	                            var treePath = [];

	                            for (var i = 1; i < treePathInfo.length; i++) {
	                                treePath.push(treePathInfo[i].name);
	                            }

	                            return [
	                                '<div class="tooltip-title">' + formatUtil.encodeHTML(treePath.join('/')) + '</div>',
	                                'Disk Usage: ' + formatUtil.addCommas(value) + ' KB',
	                            ].join('');
	                        }
			            },
			            series: [
	                        {
	                            name:'Disk Usage',
	                            type:'treemap',
	                            visibleMin: 300,
	                            label: {
	                                show: true,
	                                formatter: '{b}'
	                            },
	                            upperLabel: {
	                                normal: {
	                                    show: true,
	                                    height: 30
	                                }
	                            },
	                            itemStyle: {
	                                normal: {
	                                    borderColor: '#fff'
	                                }
	                            },
	                            levels: getLevelOption(),
	                            data: this.value_data
	                        }
	                    ]
			        });
			    }   
		}
	}
</script>

<style>
	*{
		margin: 0;
		padding: 0
	}
	a {
		text-decoration: none;
	}
	ul,ol,li{
		list-style: none;
	}
	.fl{
		float: left;
	}
	.fr{
		float: right;
	}

	#myChart{
		width:100%;
		height: 100%;
		position: fixed;
		z-index: 10;
		left: 0;
		top: 0;
	}
</style>
