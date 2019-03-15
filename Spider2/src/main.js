import 'element-ui/lib/theme-default/index.css'
import 'babel-polyfill'
import Vue from 'vue';
import Vuex from 'vuex'
import App from './App';
import router from './router';
import ElementUI from 'element-ui'
import axios from 'axios'
import echarts from 'echarts'
import VueScroller from 'vue-scroller'  
import SpiderCheck from './assets/js/spider_check'
import Check from './assets/js/SpiderCheck'
import HUCheck from './assets/js/HU_Check'
let check = new Check()

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(ElementUI)
Vue.use(VueScroller)

Vue.prototype.$axios = axios
Vue.prototype.$echarts = echarts
Vue.prototype.Ip = 'http://192.168.37.143:5000'
Vue.prototype.SpiderCheck = SpiderCheck
Vue.prototype.$HUCheck = HUCheck
Vue.prototype.$Check = check 
let store = new Vuex.Store({
	state: {
		user_data:'',
		basic_type:'',
		release_type: ''
	},
	mutations: {
		
	}
})

new Vue({
	el: '#app',
	render:h=>h(App),
	router,
	store
});
