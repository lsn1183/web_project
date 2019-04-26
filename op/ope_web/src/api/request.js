import axios from 'axios'
import { Message } from 'element-ui'
import Ip from './ip_address'
import router from '@/router/index';

const service = axios.create({
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    baseURL: Ip,
    timeout: 100000,
});
// service.interceptors.request.use(config => {
//     var token = $cookies.get('token')
//     config.headers.Authorization = 'Token ' + token;
//     return config;
// }, error => {
//     Message.error({ message: '请求超时!' });
//     return Promise.reject(error);
// }),
service.interceptors.response.use(response => {
    // if (response.data.result == 'NG') {
    //     Message.error({ message: response.data.error });
    //     return Promise.reject(response);
    // }
    // if (response.status && response.status == 200 && response.data.status == 'error') {
    //     Message.error({ message: response.data.error });
    //     return Promise.reject(response)
    // }
    return response;
}, error => {
    // if (error.response.data.result == 'NT') {
    //     Message.error({ message: error.response.data.error });
    //     router.replace({ path: '/login' })
    //     return Promise.reject(error);
    // }
    Message.error({ message: '服务异常!', showClose: true })
    return Promise.reject(error);
});

export default service