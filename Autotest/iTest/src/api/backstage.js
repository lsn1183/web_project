import request from '@/utils/request'
import Qs from 'qs'

// COUNTRY MANAGE FUNCTION

export function get_country_list() { // Request country list
    return request({
        url: 'api/1.0/testmanage/CountryList',
        method: 'get'
    })
}

export function add_country(data) { // Add new country
    return request({
        url: 'api/1.0/testmanage/CountryList',
        method: 'post',
        data
    })
}

export function submit_del_country(data) { // Delete a country
    return request({
        url: 'api/1.0/testmanage/CountryInfo/' + data.id,
        method: 'delete'
    })
}

export function edit_country(data) { // Edit a country
    return request({
        url: 'api/1.0/testmanage/CountryInfo/' + data.id,
        method: 'put',
        data
    })
}

export function export_country_excel() { // Export Country List Excel 
    return request({
        url: 'api/1.0/testmanage/ExportExcle',
        method: 'post',
        responseType: 'arraybuffer' //后台返回流文件，设定类型
    })
}

export function get_detail_country(data) { // Request country list accordint filter
    return request({
        url: 'api/1.0/testmanage/CountrySearch',
        method: 'post',
        data
    })
}

export function del_batch_country(data) { //Batch delete country
    return request({
        url: 'api/1.0/testmanage/BatchDeleteCountry',
        method: 'delete',
        data
    })
}

// 仕向地 MANAGE FUNCTION

export function get_land_list() { // Request land list
    return request({
        url: 'api/1.0/testmanage/DestList',
        method: 'get'
    })
}

export function add_land(data) { // Add new land
    return request({
        url: 'api/1.0/testmanage/DestList',
        method: 'post',
        data
    })
}

export function edit_land(data) { // Edit land
    return request({
        url: 'api/1.0/testmanage/DestInfo/' + data.id,
        method: 'put',
        data
    })
}

export function del_batch_land(data) { // Batch delete land
    return request({
        url: 'api/1.0/testmanage/BatchDeleteDest',
        method: 'delete',
        data
    })
}
export function del_land_item(id) {
    return request({
        url: 'api/1.0/testmanage/DestInfo/' + id,
        method: 'delete',
    })
}

export function get_detail_land(data) { //Request detail land list
    return request({
        url: 'api/1.0/testmanage/DestSearch',
        method: 'post',
        data
    })
}

// 自定义字段管理 

export function get_custom_field_list() { // Request custom field list
    return request({
        url: 'api/1.0/testmanage/FieldList',
        method: 'get'
    })
}

export function edit_custom_field(data) { // Edit custom field
    return request({
        url: 'api/1.0/testmanage/FieldInfo/' + data.id,
        method: 'put',
        data
    })
}

export function add_custom_field(data) { // Add new custom field
    return request({
        url: 'api/1.0/testmanage/FieldList',
        method: 'post',
        data
    })
}

export function del_custom_field(data) { // Delete a custom field
    return request({
        url: 'api/1.0/testmanage/FieldInfo/' + data.id,
        method: 'delete',
        data
    })
}

export function get_detail_field(data) { // Get detail field list
    return request({
        url: 'api/1.0/testmanage/FieldSearch',
        method: 'post',
        data
    })
}

export function del_batch_field(data) {
    return request({
        url: 'api/1.0/testmanage/BatchDeleteField',
        method: 'delete',
        data
    })
}

// 项目管理

export function get_project_list() { // Request project data
    return request({
        url: 'api/1.0/testmanage/ProjList',
        method: 'get'
    })
}

export function add_project(data) { // Add a project
    return request({
        url: 'api/1.0/testmanage/ProjList',
        method: 'post',
        data
    })
}

export function edit_project(data) { // Edit project
    return request({
        url: 'api/1.0/testmanage/ProjInfo/' + data.id,
        method: 'put',
        data
    })
}

export function del_project(data) { // Delete project
    return request({
        url: 'api/1.0/testmanage/ProjInfo/' + data.id,
        method: 'delete',
        data
    })
}

export function del_batch_project(data) { // Delete batch project
    return request({
        url: 'api/1.0/testmanage/BatchDeleteProj',
        method: 'delete',
        data
    })
}

export function del_porject(data) { // Delete a project
    return request({
        url: 'api/1.0/testmanage/BatchDeleteProj' + data.id,
        method: 'delete',
        data
    })
}

export function get_detail_project(data) { // Request detail project
    return request({
        url: 'api/1.0/testmanage/ProjSearch',
        method: 'post',
        data
    })
}

export function export_project(data) { // Export project
    return request({
        url: 'api/1.0/testmanage/ExportYaml/' + data.id,
        method: 'post',
        responseType: 'arraybuffer' //后台返回流文件，设定类型
    })
};

export function get_project_list_fun() { // Request detail project
    return request({
        url: 'api/1.0/testmanage/Projects',
        method: 'get',
    })
}


// 关键字管理
export function get_keyword_list() {
    return request({
        url: 'api/1.0/testmanage/KeywordList',
        method: 'get',
    })
}
export function add_keyword(data) {
    return request({
        url: 'api/1.0/testmanage/KeywordList',
        method: 'post',
        data
    })
}
export function edit_keyword(data, id) {
    return request({
        url: 'api/1.0/testmanage/KeywordInfo/' + id,
        method: 'put',
        data
    })
}
export function del_keyword(id) {
    return request({
        url: 'api/1.0/testmanage/KeywordInfo/' + id,
        method: 'delete',
    })
}
export function search_keyword(data) {
    return request({
        url: 'api/1.0/testmanage/KeywordSearch',
        method: 'post',
        data
    })
}
export function del_keyword_list(data) {
    return request({
        url: 'api/1.0/testmanage/BatchDeleteKeyword',
        method: 'delete',
        data
    })
}

// 模块管理
export function get_module_list(proj_id) {
    return request({
        url: `api/1.0/testmanage/ModuleList/${proj_id}`,
        method: 'get',
        // data
    })
}
export function add_module(data) {
    return request({
        url: 'api/1.0/testmanage/ModuleAdd',
        method: 'post',
        data
    })
}
export function delete_module(id) {
    return request({
        url: 'api/1.0/testmanage/ModuleInfo/' + id,
        method: 'delete',

    })
}
export function edit_module(data) {
    return request({
        url: 'api/1.0/testmanage/ModuleInfo/' + data.id,
        method: 'put',
        data
    })
}
export function del_batch_module(data) { //BatchDeleteModule
    return request({
        url: 'api/1.0/testmanage/BatchDeleteModule',
        method: 'delete',
        data
    })
}
export function get_detail_module(data) {
    return request({
        url: 'api/1.0/testmanage/ModuleSearch',
        method: 'post',
        data
    })
}
export function get_edit_module(id) {
    return request({
        url: 'api/1.0/testmanage/ChangeModuleInfo/' + id,
        method: 'get',
    })
}

export function get_project_fields_list(id) {
    return request({
        url: 'api/1.0/testmanage/GetFieldsByProj/' + id,
        method: 'get',
    })
}

// 关键字
export function del_keyword_item(id) {
    return request({
        url: 'api/1.0/testmanage/KeywordInfo/' + id,
        method: 'delete',
    })
}

// 人员/权限管理
export function get_permission_list() {
    return request({
        url: 'api/1.0/userManage/GetPermission',
        method: 'get'
    })
}
export function get_permission_role(role) {
    return request({
        url: 'api/1.0/userManage/GetPermissionRole/'+ role,
        method: 'get'
    })
}

export function edit_permission(data) {
    return request({
        url: 'api/1.0/userManage/ChangePermission',
        method: 'put',
        data
    })
}

export function get_role_list() {
    return request({
        url: 'api/1.0/userManage/GetRole',
        method: 'get',
        
    })
}

export function edit_personnel_role(data) {
    return request({
        url: 'api/1.0/userManage/SavePersonnelRole',
        method: 'post',
        data
    })
}

export function get_all_user_role() {
    return request({
        url: 'api/1.0/userManage/GetUser',
        method: 'get'
        
    })
}

export function get_search_user_list_fun(string) {
    return request({
        url: 'api/1.0/userManage/GetUser/'+string,
        method: 'get'
        
    })
}

// 权限操作
export function get_user_permission_list_fun(user_name,permission_string) {
    const data = {
        "user_name": user_name,
        "per_name": permission_string
    }
    return request({
        url: 'api/1.0/userManage/GetUserPermission',
        method: 'post',
        data
    })
}


