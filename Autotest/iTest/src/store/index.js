import Vue from 'vue'
import Vuex from 'vuex'
import app from './module/app'
import getters from './module/getters'
import other from './module/other'
import user from './module/user'

Vue.use(Vuex)

const store = new Vuex.Store({
    modules: {
        app,
        user,
        other
    },
    getters
})

export default store