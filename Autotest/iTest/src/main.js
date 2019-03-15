// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'babel-polyfill'
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'

// import 'normalize.css/normalize.css'// A modern, HTML5-ready alternative to CSS resets


import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import '@/styles/index.scss' // global custom css

import i18n from './languages'
import store from './store'

import echarts from 'echarts'

Vue.prototype.$echarts = echarts 

Vue.use(Element, {
    size: 'small', // set element-ui default style size to medium
    i18n: (key, value ) => i18n.t(key, value)
})

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    i18n,
    components: { App },
    template: '<App/>'
})
