import { login, logout } from '@/api/login'
import { getToken, setToken, removeToken } from '@/utils/cookies'

const user = {
    state: {
        user: '',
        token: getToken(),
        name: ''
    },

    mutations: {
        SET_TOKEN: (state, token) => {
            state.token = token
        },
        SET_NAME: (state, name) => {
            state.name = name
        }
    },

    actions: {
        Login ({ commit }, user_data) {
            return new Promise((resolve, reject) => {
                login(user_data).then(res => {
                    if (res.data.result == 'OK') {
                        const data = res.data
                        window.sessionStorage.setItem('Token', data.accessToken)
                        setToken(data.accessToken)
                        commit('SET_NAME', data.username)
                        commit('SET_TOKEN', data.accessToken)
                        resolve()
                    }else{
                        reject(res.data)
                    }
                }).catch(error => {
                    reject(error)
                });
            });
        },
        LogOut ({ commit }){
            return new Promise(resolve => {
                window.sessionStorage.clear()
                commit('SET_TOKEN', '')
                removeToken()
                resolve()
            }) 
        }
    }
}


export default user
