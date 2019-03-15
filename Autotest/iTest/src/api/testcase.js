import request from '@/utils/request'

export function get_module_tree_node(id) {
    return request({
        url: 'api/1.0/testmanage/CaseTree/' + id,
        method: 'get'
    })
}
export function get_proj_module_tree_node(id) {
    return request({
        url: 'api/1.0/testmanage/ModuleTree/' + id,
        method: 'get'
    })
}

export function get_all_case(page, size) { // 获得所有testcae(分页)
    return request({
        url: 'api/1.0/testcase/AllTestcaseList/' + page + '/' + size,
        method: 'get'
    })
}

export function get_all_case_no_paging(proj_id) { // 获得所有testcase, 不分页
    return request({
        url: 'api/1.0/testcase/TestcaseListAll/' + proj_id ,
        method: 'get'
    })
}

export function get_proj_tree(proj_id) {
    return request({
        url: `api/1.0/testmanage/ProjTree/${proj_id}`,
        method: 'get'
    })
}

export function get_proj_test_case(id, page, size) {
    return request({
        url: 'api/1.0/testcase/TestcaseProjList/' + id + '/' + page + '/' + size,
        method: 'get'
    })
}

export function get_module_test_case(id, page, size) {
    return request({
        url: 'api/1.0/testcase/TestcaseModelList/' + id + '/' + page + '/' + size,
        method: 'get'
    })
}

export function get_one_test_case(id) {
    return request({
        url: 'api/1.0/testcase/TestcaseOne/' + id,
        method: 'get'
    })
}

export function add_test_case(module_id, data) {
    return request({
        url: 'api/1.0/testcase/TestcaseAdd/' + module_id,
        method: 'post',
        data
    })
}

export function edit_test_case(test_case_id, data) {
    return request({
        url: 'api/1.0/testcase/TestcaseInfo/' + test_case_id,
        method: 'put',
        data
    })
}

export function get_three_list(module_id) {
    return request({
        url: 'api/1.0/testcase/Showthreelist/' + module_id,
        method: 'get'
    })
}

export function del_test_case(data) {
    return request({
        url: 'api/1.0/testcase/BatchDeleteTestcase',
        method: 'delete',
        data
    })
}

export function get_filter_data_about_all_case(page, size , data) { // 搜索testcase(分页)
    return request({
        url: 'api/1.0/testcase/TestcaseSearch/' + page + '/' + size,
        method: 'post',
        data
    })
}

export function get_filter_data_about_all_case_no_paging(data) { // 搜索testcase(不分页)
    return request({
        url: 'api/1.0/testcase/TestcaseSearch',
        method: 'post',
        data
    })
}

export function get_filter_data_about_project(id, page, size, data) {
    return request({
        url: 'api/1.0/testcase/ProjTestcaseSearch/' + id + '/' + page + '/' + size,
        method: 'post',
        data
    })
}

export function get_filter_data_about_module(id, page, size, data) {
    return request({
        url: 'api/1.0/testcase/ModelTestcaseSearch/' + id + '/' + page + '/' + size,
        method: 'post',
        data
    })
}

export function improve_case_version(case_id) {
    return request({
        url: `api/1.0/testcase/TestcaseVerUp/${case_id}`,
        method: 'get'
    })
}

//获取历史版本号
export function get_history_ver(case_id){
    return request({
        url: "api/1.0/testcase/TcHistoryVer/" + case_id
    })
}

// 获取俩版历史
export function get_diff(case_id, left_ver=0, right_ver=0){
    return request({
        url: "api/1.0/testcase/TcVerDiff/" + case_id + '/' + left_ver + '/' + right_ver
    })
}
