import request from '@/utils/request'

export function get_test_plan(proj_id, page, size) {
    return request({
        url: `api/1.0/testcase/TestplanList/${proj_id}/${page}/${size}`,
        method: 'get'
    })
}


export function add_test_plan(data) {
    return request({
        url: 'api/1.0/testcase/TestplanAdd',
        method: 'post',
        data
    })
}

export function del_test_plan(data) {
    return request({
        url: 'api/1.0/testcase/BatchDeleteTestplan',
        method: 'delete',
        data
    })
}

export function edit_one_test_plan(id, data) {
    return request({
        url: 'api/1.0/testcase/TestplanInfo/' + id,
        method: 'put',
        data
    })
}

export function get_one_test_plan(id) {
    return request({
        url: 'api/1.0/testcase/TestplanInfo/' + id,
        method: 'get'
    })
}

export function get_filter_data_about_test_plan(page, size, data) {
    return request({
        url: 'api/1.0/testcase/TestplanSearch/' +  page + '/' + size,
        method: 'post',
        data
    })
}

export function req_test_plan_result_list(id) {
    return request({
        url: 'api/1.0/testcase/TestresultList/' + id,
        method: 'get'
    })
}

export function req_case_result_history(plan_id, case_id) {
    return request({
        url: 'api/1.0/testcase/TestresultHistory/' + plan_id + '/' + case_id,
        method: 'get'
    })
}

export function req_one_detail_case(plan_history_id, case_id) {
    return request({
        url: 'api/1.0/testcase/TestresultOne/' + plan_history_id + '/' + case_id,
        method: 'get'
    })
}

export function sub_case_record(plan_history_id, case_id, data) {
    return request({
        url: `api/1.0/testcase/TestresultAdd/${plan_history_id}/${case_id}`,
        method: 'post',
        data
    })
}

export function add_test_plan_history(data) {
    return request({
        url: 'api/1.0/testcase/TestplanHistoryAdd',
        method: 'post',
        data
    })
}

export function req_test_plan_history(plan_id) {
    return request({
        url: `api/1.0/testcase/TestplanHistoryList/${plan_id}`,
        method: 'get'
    })
}

export function del_tese_plan_history(data) {
    return request({
        url: 'api/1.0/testcase/BatchDeleteTestplanHistory',
        method: 'delete',
        data
    })
}

export function del_case_history(data) {
    return request({
        url: 'api/1.0/testcase/BatchDeleteTestresult',
        method: 'delete',
        data
    })
}

export function get_plan_configuration_list(plan_id) {
    return request({
        url: `api/1.0/testcase/SettingOption/${plan_id}`,
        method: 'get'
    })
}


export function set_plan_configuration(plan_id, data) {
    return request({
        url:  `api/1.0/testcase/TestplanSettingInfo/${plan_id}`,
        method: 'post',
        data
    })
}

export function get_selected_plan_configuration(plan_id, data) {
    return request({
        url:  `api/1.0/testcase/TestplanSettingInfo/${plan_id}`,
        method: 'get'
    })
}

export function get_jenkins_node(plan_id) {
    return request({
        url: 'api/1.0/testcase/GetJenkinsNode',
        method: 'get'
    })
}