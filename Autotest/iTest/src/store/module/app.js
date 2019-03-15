import Cookies from 'js-cookie'

const app = {
    state: {
        device: 'desktop',
        language: Cookies.get('language') || 'zh'
    },
    // 更改 Vuex 的 store 中的状态的唯一方法是提交 mutation （其实也能直接更改 state中的值）
    mutations: {
        SET_LANGUAGE: (state, language) => {
            state.language = language
            Cookies.set('language', language)
        }
    },
    // actions 其实相当于一个虚拟层，只是为了让vuex的动作都变为同步
    // Action 提交的是 mutation，而不是直接变更状态。
    // Action 可以包含任意异步操作
    actions: {
        setLanguage({ commit }, language) {
            commit('SET_LANGUAGE', language)
        }
    }
}

export default app
