import request from '@/utils/request'

export function login(data) {
    return request({
        url: 'api/1.0/userManage/Login',
        method: 'post',
        data
    })
}
export function logout() {
    return request({
        url: '/login/logout',
        method: 'post'
    })
}
export function getUserInfo(token) {
    return request({
        url: '/user/info',
        method: 'get',
        params: {
            token
        }
    })
}

export function get_all_user(query_value) {
    return request({
        url: 'api/1.0/userManage/GetUser/' + query_value,
        method: 'get'
    })
}
