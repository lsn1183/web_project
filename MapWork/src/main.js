import 'element-ui/lib/theme-chalk/index.css'
import 'babel-polyfill'
import Vue from 'vue';
import Vuex from 'vuex'
import App from './App';
import router from './router';
import ElementUI from 'element-ui'
import axios from 'axios'
import VueParticles from 'vue-particles'
import '../src/assets/css/iconfont.css'
import globalConfig from './assets/js/globalConfig'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(ElementUI)
Vue.use(VueParticles)
Vue.use(globalConfig)
Vue.use(mavonEditor)

axios.interceptors.request.use(config => {
    const token = window.sessionStorage.getItem('token')
    if (token) {
        config.headers.token = token
        config.headers.Authorization = 'Token ' + token;
    }
    return config
}, error => {
    return Promise.reject(error)
})
axios.interceptors.response.use(response => {
    const res = response
    return response
}, error => {
    const err = error
    if (err.response.data.result == 'NT') {
        window.sessionStorage.clear()
        window.localStorage.clear()
        Vue.prototype.$message({
            message: '账号密码已过期，请重新登录',
            type: 'error',
            showClose: false,
            duration: 2 * 1000
        })
        router.replace({
            path: '/login'
        })
    } else {
        // do nothing
    }
    return Promise.reject(error)
})
Vue.prototype.$axios = axios
Vue.prototype.Ip = 'http://192.168.64.172:15000'
let store = new Vuex.Store({
    state: {
        user_data: '',
        basic_type: '',
        release_type: '',
        text_type: '',
        form_item_id: '',
        workType: '',
        doc_id: 0,
        step_id: 0,
        fpm_id: 0,
        desk_id: '',
        high_type: '',
        previewDocId: ''
    },
    mutations: {
        amendDocId(state, val) {
            state.doc_id = val
        }
    }
})

new Vue({
    el: '#app',
    render: h => h(App),
    router,
    store
});
