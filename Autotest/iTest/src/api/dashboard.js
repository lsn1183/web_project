import request from '@/utils/request'
// 柱状图
export function get_dashboard(name) {
    return request({
        url: 'api/1.0/testcase/LineChart/' + name,
        method: 'get'
    })
}
// 堆叠图
export function get_StackChart(name) {
	if(name != '' && name != null){
		return request({
		    url: 'api/1.0/testcase/StackChart/' + name,
		    method: 'get'
		})
	}else{
		return request({
		    url: 'api/1.0/testcase/StackChart',
		    method: 'get'
		})
	}   
}
// 饼图
export function get_PieChart(name) {
	if(name != '' && name != null){
		return request({
		    url: 'api/1.0/testcase/PieChart/' + name,
		    method: 'get'
		})
	}else{
		return request({
		    url: 'api/1.0/testcase/PieChart',
		    method: 'get'
		})
	}
}