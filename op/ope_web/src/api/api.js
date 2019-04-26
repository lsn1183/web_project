import request from '@/api/request'

// login
export function login (data){
    return request ({
        url:"/login",
        method:"post",
        data
    })
}

// project
export function project_list() {
    return request({
        url: '/Project/List',
        method: 'get',
    })
}
export function add_project(data) {
    return request({
        url: '/Project/add',
        method: 'post',
        data
    })
}
export function edit_project(data) {
    return request({
        url: '/Project/update',
        method: 'post',
        data
    })
}

export function delete_project(proj_id) {
    return request({
        url: '/Project/delete/'+ proj_id,
        method: 'delete',
    })
}
export function project_detail(proj_id) {
    return request({
        url: '/Project/' + proj_id,
        method: 'get',
        
    })
}
export function get_op_list(proj_id) {
    return request({
        url: '/Project/ope/' + proj_id,
        method: 'get',
    })
}
// 获取某本Ope下的chapter
export function get_chapter_list(screen_gid,type) {
    return request({
        url: '/Chapter/' + screen_gid + "/"+type,
        method: 'get',
    })
}

export function uodate_chapter_list(type,data) {
    return request({
        url: '/Chapter/update/' + type,
        method: 'post',
        data
    })
}

export function select_display(proj_id) {
    return request({
        url: '/Ope/Display/' + proj_id,
        method: 'get',
    })
}

export function select_condition(proj_id) {
    return request({
        url: '/Ope/Condition/' + proj_id,
        method: 'get',
    })
}

export function select_opeType(proj_id) {
    return request({
        url: '/Ope/OpeType/' + proj_id,
        method: 'get',
    })
}

export function select_event(proj_id) {
    return request({
        url: '/Ope/Event/' + proj_id,
        method: 'get',
    })
}

export function select_property(proj_id) {
    return request({
        url: '/Ope/Property/' + proj_id,
        method: 'get',
    })
}

export function ope_list(screen_gid) {
    return request({
        url: '/Ope/' + screen_gid,
        method: 'get',
    })
}