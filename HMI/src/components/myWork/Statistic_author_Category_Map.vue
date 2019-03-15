<template>
	<div v-loading.lock="fullscreenLoading">
		<div id="main_map" style="width:98%;height: 650px;margin-top: 3%"></div>
    <div style="display: inline-block;float: left;margin-top: 1%;margin-left: 4%">
      <!--<el-select class="button_tree" v-model="map_arr_def" @change="select_map" size="small">-->
      <!--<el-option class="button_tree_option" v-for="item in map_arr" :key="item.value" :label="item.label" :value="item.value">-->
      <!--</el-option>-->
      <!--</el-select>-->
      <!--<el-button size="mini" type="#E5E9F2" @click="click_return">返回上级</el-button>-->
      <span style="margin-left: 5%">
        <el-button size="mini" type="info"  :plain="true" @click="click_qa">QA</el-button>
      <el-button size="mini" type="#E5E9F2" @click="click_de">Delay</el-button>
      <el-button size="mini" type="#E5E9F2" @click="click_no"  id="uno"  >未完成</el-button>
      </span>
		<div style="margin-top: 5%;display: block; ">
			<b style="font-size: 15px;">选择查看的日期:</b>
			<el-date-picker v-model="date_value" type="daterange" :picker-options="pickerOptions" placeholder="选择时间范围" align="right" size="small" time-arrow-control="true" :clearable="false" @change="getDate"></el-date-picker>
			<el-select class="button_tree" v-model="arr_v" @change="selectsp" size="small">
				<el-option class="button_tree_option" v-for="item in arr" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>

		</div>

    </div>
	</div>
</template>
<script>
  export default {
    mounted() {
      this.undone_fun();
//      this.click_no();
		},
		data() {
			return {
        			fullscreenLoading:false,
				pickerOptions: {
					shortcuts: [{
						text: "最近7天",
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
							picker.$emit('pick', [start, end])
						}
					}]
				},
				arr_v: "SP31",
				arr: [{
						value: "SP29",
						label: "SP29"
					},
					{
						value: "SP30",
						label: "SP30"
					},
					{
						value: "SP31",
						label: "SP31"
					},
					{
						value: "SP32",
						label: "SP32"
					},
				],
        map_arr_def:'未完成数据表',
        map_arr: [{
          value: "QA",
          label: "QA数据表"
        },
          {
            value: "DELAY",
            label: "Delay数据表"
          },
          {
            value: "UNDONE",
            label: "未完成数据表"
          },
        ],
				select_time: "",
				date_value: [new Date().getTime() - 3600 * 1000 * 24 * 10,new Date().getTime()],
				source_data: '',
				charger_arr: '',
        btnColor_flag:true,
			}
		},
		methods: {
      click_qa(){
        this.default_fun();
        let btn=document.getElementById('uno');
        btn.style.color="";
        btn.style.borderColor="";
      },
      click_de(){
        this.delay_fun();
        let btn=document.getElementById('uno');
        btn.style.color="";
        btn.style.borderColor="";
      },
      click_no(){
        this.undone_fun();
      },
			//加载图表
			default_fun() {
        let sp = this.arr_v;
        if(this.select_time===""){
          var formatDate = function(date) {
            var y = date.getFullYear();
            var m = date.getMonth() + 1;
            m = m < 10 ? '0' + m : m;
            var d = date.getDate();
            d = d < 10 ? ('0' + d) : d;
            return y + '-' + m + '-' + d;
          };
          const start = new Date(),
            end = new Date(),
            start_time = start.setTime(start.getTime() - 3600 * 1000 * 24 * 10);
          let time_start = formatDate(new Date(start_time)),
            time_end = formatDate(end);
          this.charger_arr=[];
          this.source_data=[];
          this.fullscreenLoading=true;
          this.$axios.get(this.Ip + "/TimeReport/" + time_start + "/" + time_end + '/'+sp + "/" + 'qa')
            .then(res => {
//              console.log(res)
              if(res.data.result === "OK") {
                let charger_name = [];
                for(let value of res.data.content) {
                  for(let key in value) {
                    charger_name.push(key)
                  }
                };
                this.charger_arr = Array.from(new Set(charger_name));
                this.source_data = res.data.content;
                //QA
                this.drawLine_QA();
                this.fullscreenLoading=false;
//                console.log(res.data,"res_QA,默認")

              }
            });
        }else {
          let time_start = this.select_time.substring(0, 10),
            time_end = this.select_time.substring(12, 23);
          this.charger_arr=[];
          this.source_data=[];
          this.fullscreenLoading=true;
          this.$axios.get(this.Ip + "/TimeReport/" + time_start + "/" + time_end + "/" + sp + "/" + 'qa')
            .then(res => {
//              console.log(res)
              if(res.data.result === "OK") {
                let charger_name = [];
                for(let value of res.data.content) {
                  for(let key in value) {
                    charger_name.push(key)
                  }
                };
                this.charger_arr = Array.from(new Set(charger_name));
                this.source_data = res.data.content;
                this.drawLine_QA();
                this.fullscreenLoading=false;
              }
            })
        }
			},
			//delay图表加载
			delay_fun() {
        let sp = this.arr_v;
        if(this.select_time===""){
          var formatDate = function(date) {
            var y = date.getFullYear();
            var m = date.getMonth() + 1;
            m = m < 10 ? '0' + m : m;
            var d = date.getDate();
            d = d < 10 ? ('0' + d) : d;
            return y + '-' + m + '-' + d;
          };
          const start = new Date(),
            end = new Date(),
            start_time = start.setTime(start.getTime() - 3600 * 1000 * 24 * 10);
          let time_start = formatDate(new Date(start_time)),
            time_end = formatDate(end);
          this.charger_arr=[];
          this.source_data=[];
          this.fullscreenLoading=true;
          this.$axios.get(this.Ip + "/TimeReport/" + time_start + "/" + time_end + '/' +sp+ "/" + 'delay')
            .then(res => {
//              console.log(res)
              if(res.data.result == "OK") {
                let charger_name = [];
                for(let value of res.data.content) {
                  for(let key in value) {
                    charger_name.push(key)
                  }
                };
                this.charger_arr = Array.from(new Set(charger_name));
                this.source_data = res.data.content;
                //delay
                this.drawLine_delay();
                this.fullscreenLoading=false;
//                console.log(res.data,"res,delay")
              }
            });
        }else {
          let time_start = this.select_time.substring(0, 10),
            time_end = this.select_time.substring(12, 23);
          this.charger_arr=[];
          this.source_data=[];
          this.fullscreenLoading=true;
          this.$axios.get(this.Ip + "/TimeReport/" + time_start + "/" + time_end + "/" + sp + "/" + 'delay')
            .then(res => {
//              console.log(res)
              if(res.data.result == "OK") {
                let charger_name = [];
                for(let value of res.data.content) {
                  for(let key in value) {
                    charger_name.push(key)
                  }
                };
                this.charger_arr = Array.from(new Set(charger_name));
                this.source_data = res.data.content;
                this.drawLine_delay();
                this.fullscreenLoading=false;
              }
            })
        }
			},
			//未完成表
			undone_fun() {
//        设置相应按钮在图表加载时变色
        if(this.btnColor_flag=true){
          let btn=document.getElementById('uno');
          btn.style.color="#20a0ff";
          btn.style.borderColor="#20a0ff";
          this.btnColor_flag=false;
        }
        let sp = this.arr_v;
        if(this.select_time==""){
          var formatDate = function(date) {
            var y = date.getFullYear();
            var m = date.getMonth() + 1;
            m = m < 10 ? '0' + m : m;
            var d = date.getDate();
            d = d < 10 ? ('0' + d) : d;
            return y + '-' + m + '-' + d;
          };
          const start = new Date(),
            end = new Date(),
            start_time = start.setTime(start.getTime() - 3600 * 1000 * 24 * 10);
          let time_start = formatDate(new Date(start_time)),
            time_end = formatDate(end);
          this.charger_arr=[];
          this.source_data=[];
          this.fullscreenLoading=true;
          this.$axios.get(this.Ip + "/TimeReport/" + time_start + "/" + time_end + "/" + sp + "/" + 'no')
            .then(res => {
//              console.log(res)
              if(res.data.result == "OK") {

                let charger_name = [];
                for(let value of res.data.content) {
                  for(let key in value) {
                    charger_name.push(key)

                  }
                };
                this.charger_arr = Array.from(new Set(charger_name));
                this.source_data = res.data.content;
                //未完成\
                this.drawLine_undone();
                this.fullscreenLoading=false;
//                console.log(res.data,"res,undone,未完成")
              }
            });
        }else {
          let time_start = this.select_time.substring(0, 10),
            time_end = this.select_time.substring(12, 23);
          this.charger_arr=[];
          this.source_data=[];
          this.fullscreenLoading=true;
          this.$axios.get(this.Ip + "/TimeReport/" + time_start + "/" + time_end + "/" + sp + "/" + 'no')
            .then(res => {
//              console.log(res,"undone")
              if(res.data.result == "OK") {
                let charger_name = [];
                for(let value of res.data.content) {
                  for(let key in value) {
                    charger_name.push(key)
                  }
                };
                this.charger_arr = Array.from(new Set(charger_name));
                this.source_data = res.data.content;
//                console.log(this.source_data,"source_data",this.charger_arr,"charger_arr")
                this.drawLine_undone();
                this.fullscreenLoading=false;
              }
            })
        }
			},

			//绘图部分：QA图
			drawLine_QA: function() {
        let series_arr=[];
        for(let i =0;i<this.charger_arr.length;i++){
          if(i!= this.charger_arr.length-1){
            series_arr.push({type: 'bar', label: {normal: {show: true, }},});
          }
        };
				let myChart = this.$echarts.init(document.getElementById("main_map"));
				let option = {
					title: {
						text: 'QA数据图',
						subtext: '担当负责人'
					},
					toolbox: {
						show: true,
						feature: {
							magicType: {
								show: true,
								type: ["bar", 'line'],
								title: {
									bar: '柱形图切换',
									line: '折线图切换'
								}
							},
							saveAsImage: {
								show: true,
								title: '保存为图片',
								type: 'png'
							}
						},
					},
					color: ['#990066', "#009999", '#CC0033', "#333399", "#ff0033", "#666699", "#663366", "#003399"],
					grid: {
						left: '4%',
						right: '0%',
						bottom: '0%',
						containLabel: true
					},
					legend: {},
					tooltip: {},
					dataset: [{
						dimensions: this.charger_arr,
						source: this.source_data,
					}, ],
					xAxis: {
						type: 'category',
            triggerEvent:true
					},
					yAxis: {},
					axis: {},
          series: series_arr,
//            [{type: 'bar', label: {normal: {show: true, position: ''}},}],
				};
        myChart.clear();
        myChart.setOption(option);
				var self = this;
        myChart.off('click',);
				myChart.on('click', function(params) {
				  if(params.componentType=='xAxis'){

          }else {
            self.source_data = [];
            self.source_data.push(params.data)
            self.drawLine_QA();
          }
				});
			},
//      delay
			drawLine_delay: function() {
        let series_arr=[];
        for(let i =0;i<this.charger_arr.length;i++){
          if(i!= this.charger_arr.length-1){
            series_arr.push({type: 'bar', label: {normal: {show: true, }},});
          }
        };
				let myChart = this.$echarts.init(document.getElementById("main_map"));
				let option = {
					title: {
						text: 'Delay数据图',
						subtext: '担当负责人'
					},
					toolbox: {
						show: true,
						feature: {
							magicType: {
								show: true,
								type: ["bar", 'line'],
								title: {
									bar: '柱形图切换',
									line: '折线图切换'
								}
							},
							saveAsImage: {
								show: true,
								title: '保存为图片',
								type: 'png'
							}
						},
					},
					color: ['#990066', "#009999", '#CC0033', "#333399", "#ff0033", "#666699", "#663366", "#003399"],
					grid: {
						left: '4%',
						right: '0%',
						bottom: '0%',
						containLabel: true
					},
					legend: {},
					tooltip: {},
					dataset: [{
						dimensions: this.charger_arr,//渲染数组
						source: this.source_data,//渲染的数组
					}, ],
					xAxis: {
						type: 'category',
            triggerEvent:true
          },
					yAxis: {},
					axis: {},
          series: series_arr,
				};
        myChart.clear();
        myChart.setOption(option);
				var self = this;
        myChart.off('click',);
        myChart.on('click', function(params, ) {
          if(params.componentType=='xAxis'){

          }else {
            self.source_data = [];
            self.source_data.push(params.data)
            self.drawLine_delay();
          }

        })
			},
//      未完成
			drawLine_undone: function() {
        let series_arr=[];
        for(let i =0;i<this.charger_arr.length;i++){
          if(i!= this.charger_arr.length-1){
            series_arr.push({type: 'bar', label: {normal: {show: true, }},});
          }
        };
				let myChart = this.$echarts.init(document.getElementById("main_map"));
				let option = {
					title: {
						text: '未完成数据图',
						subtext: '担当负责人'
					},
					toolbox: {
						show: true,
						feature: {
							magicType: {
								show: true,
								type: ["bar", 'line'],
								title: {
									bar: '柱形图切换',
									line: '折线图切换'
								}
							},
							saveAsImage: {
								show: true,
								title: '保存为图片',
								type: 'png'
							}
						},
					},
					color: ['#990066', "#009999", '#CC0033', "#333399", "#ff0033", "#666699", "#663366", "#003399"],
					grid: {
						left: '4%',
						right: '0%',
						bottom: '0%',
						containLabel: true
					},
					legend: {},
					tooltip: {},
					dataset: [{
						dimensions: this.charger_arr,
						source: this.source_data,
					}, ],
					xAxis: {
						type: 'category',
            triggerEvent:true
          },
					yAxis: {},
					axis: {},
          series: series_arr,
				};
				myChart.clear();
				myChart.setOption(option);
        this.fullscreenLoading=false;
        var self = this;
        myChart.off('click',);
        myChart.on('click', function(params ) {
          if(params.componentType=='xAxis'){

          }else {
            self.source_data = [];
            self.source_data.push(params.data)
            self.drawLine_undone();
          }
        })
			},
			//选择框查看日期
			getDate(value, sp) {
        if(value!=""){
          this.select_time = value;
          sp = this.arr_v;
          let time_start = value.substring(0, 10),
            time_end = value.substring(12, 23);
          this.charger_arr=[];
          this.source_data=[];
          this.fullscreenLoading=true;
          this.$axios.get(this.Ip + "/TimeReport/" + time_start + "/" + time_end + "/" + sp + "/" + 'no')
            .then(res => {
              if(res.data.result == "OK") {
                let charger_name = [];
                for(let value of res.data.content) {
                  for(let key in value) {
                    charger_name.push(key)
                  }
                };
                this.charger_arr = Array.from(new Set(charger_name));
                this.source_data = res.data.content;
                this.drawLine_undone();
                this.fullscreenLoading=false;
              }
            })
        }else {
          this.$notify({
            type:"error",
            message:"时间不能为空!"
                       })
        }
			},
			//选择框
			selectsp(sp) {
        if(this.select_time==""){
          var formatDate = function(date) {
            var y = date.getFullYear();
            var m = date.getMonth() + 1;
            m = m < 10 ? '0' + m : m;
            var d = date.getDate();
            d = d < 10 ? ('0' + d) : d;
            return y + '-' + m + '-' + d;
          };
          const start = new Date(),
            end = new Date(),
            start_time = start.setTime(start.getTime() - 3600 * 1000 * 24 * 10);
          let time_start = formatDate(new Date(start_time)),
            time_end = formatDate(end);
          this.charger_arr=[];
          this.source_data=[];
          sp = this.arr_v;
          this.fullscreenLoading=true;
          this.$axios.get(this.Ip + "/TimeReport/" + time_start + "/" + time_end + "/" + sp + "/" + 'no')
            .then(res => {
//              console.log(res)
              if(res.data.result == "OK") {
                let charger_name = [];
                for(let value of res.data.content) {
                  for(let key in value) {
                    charger_name.push(key)
                  }
                };
                this.charger_arr = Array.from(new Set(charger_name));
                this.source_data = res.data.content;
                this.drawLine_undone();
                this.fullscreenLoading=false;
              }
            });
        }else {
          sp = this.arr_v;
          let time_start = this.select_time.substring(0, 10),
            time_end = this.select_time.substring(12, 23);
          this.charger_arr=[];
          this.source_data=[];
          this.fullscreenLoading=true;
          this.$axios.get(this.Ip + "/TimeReport/" + time_start + "/" + time_end + "/" + sp + "/" + 'no')
            .then(res => {
//                console.log(res)
              if(res.data.result == "OK") {
                let charger_name = [];
                for(let value of res.data.content) {
                  for(let key in value) {
                    charger_name.push(key)
                  }
                };
                this.charger_arr = Array.from(new Set(charger_name));
                this.source_data = res.data.content;
                this.drawLine_undone();
                this.fullscreenLoading=false;
              }
            });
        }
			},
		},
	}
</script>
<style scoped>
	.btn:active{
    color: #20a0ff;
    background-color: #20a0ff;
  }
</style>
