import axios from 'axios'
import {
    Message
} from 'element-ui'
import store from '@/store'
import Qs from 'qs'
import Ip from './address'

// create an axios instance
// 自定义配置创建axios的新实例
const service = axios.create({
    headers: {
        'Content-Type': 'application/json'
    },
    timeout: 10000, // request timeout  // `timeout`指定请求超时之前的毫秒数。如果请求的时间超过'timeout'，请求将被中止。
    // baseURL: 'http://192.168.37.143:15000',
    baseURL: Ip,
})

// request interceptor
service.interceptors.request.use(config => {
    return config
}, error => {
    console.log(error, 'error')
    Promise.reject(error)
})

// response interceptor
// 响应拦截器
// 在接收到响应准备处理之前，可以通过 axios.interceptor.response.use 做一些操作
service.interceptors.response.use(response => {
    // 可以根据后台返回code status 判断状态（如果后台用 status 状态标识）
    return response
}, error => {
    Message({
        message: error.response.data.error,
        type: 'error',
        showClose: true,
        duration: 5 * 1000
    })
    return Promise.reject(error)
})

export default service
