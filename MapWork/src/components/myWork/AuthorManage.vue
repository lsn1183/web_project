<template>
    <div id="authorManage" class="wrapper">
        <el-tabs tabPosition="left" class="el-tabs-left" tab-position="left" @tab-click="tab_click(activeName)" v-model="activeName">
            <el-tab-pane label="用户管理" name="user-role">
                <div class="custom-tree-container highlight-col">
                    <div class="table-top">
                        <div class="div-input" @keyup.enter="filterNameFun(filterName)">
                            <el-input :clearable="true" @clear="clearFilterName()" size="small" placeholder="请输入筛选的用户名" v-model="filterName" v-on:input="clearFilterName()">
                                <el-button slot="append" icon="el-icon-search" @click="filterNameFun(filterName)"></el-button>
                            </el-input>
                        </div>
                        <span class="append-span" @click="subUserManage(subUserManageArray)"> &nbsp;[ 确认 ]</span>
                    </div>
                    <el-table :data="userManageBodyData" border :max-height='adaptivePageHeight' style="width: 97%">
                        <el-table-column label="用户" min-width="100">
                            <template slot-scope="scope">
                                <span>
                                    <div>{{scope.row.user_name}}</div>
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column v-for="{ role_name, role_id } in userManageBodyDataRole" :key="role_id" :label="role_name" class="noSty">
                            <template slot-scope="scope">
                                <span v-for="(items, index) in scope.row.role_list" :key="index" v-if="items.role_id ==role_id" @click="AddUserManageData(scope.row.user_id)">
                                    <el-checkbox v-model="items.have_role"></el-checkbox>
                                </span>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="form-page">
                        <el-pagination id="list_page" @current-change="listPageChange" :current-page="page" :page-size="page_size" layout="total, prev, pager, next,jumper" :total="page_count"></el-pagination>
                    </div>
                </div>
            </el-tab-pane>

            <el-tab-pane label="角色/权限管理" name="role-permission">
                <div class="custom-tree-container highlight-col">
                    <div class="table-top">
                        <div class="div-input" @keyup.enter="filterRoleFun(filterRole)">
                            <el-input :clearable="true" @clear="clearFilterRole()" size="small" placeholder="请输入筛选的角色" v-model="filterRole" v-on:input="clearFilterRole()">
                                <el-button slot="append" icon="el-icon-search" @click="filterRoleFun(filterRole)"></el-button>
                            </el-input>
                        </div>
                        <span class="append-span" @click="subCharacterData()"> &nbsp;[ 确认 ]</span>
                    </div>
                    <el-table :data="tableDataRole" border style="width: 97%" :max-height='adaptivePageHeight'>
                        <el-table-column fixed label="角色" min-width="100">
                            <template slot-scope="scope">
                                <span>
                                    <div>{{scope.row.role_name}}</div>
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column :label="item.model_name" v-for="(item,index) in colForConfig" :key="index">
                            <el-table-column v-for="{ perm_id, perm_name } in item.permissions" :key="perm_id" :label="perm_name" class="noSty">
                                <template slot-scope="scope">
                                    <span v-for="(items) in scope.row.permissions" v-if="items.perm_id ==perm_id" :key="items.perm_id">
                                        <el-checkbox v-model="items.assigned"></el-checkbox>
                                    </span>
                                </template>
                            </el-table-column>
                        </el-table-column>
                    </el-table>
                </div>
            </el-tab-pane>

            <!-- <el-tab-pane label="组管理" name="group" >
                <div class="custom-tree-container" v-show="G_flag">
                    <div class="table-top">
                        <div class="div-input" @keyup.enter="filterGroupFun(filterGroup)">
                            <el-input :clearable="true" @clear="clearFilterGroup()" size="small" placeholder="请输入筛选组" v-model="filterGroup" v-on:input="clearFilterGroup()">
                                <el-button slot="append" icon="el-icon-search" @click="filterGroupFun(filterGroup)"></el-button>
                            </el-input>
                        </div>
                        <span class="append-span" @click="createGroup()"> &nbsp;[ 新建组 ]</span>
                    </div>
                    <el-table class="diy-table" :data="tableDataGroup" border style="width: 97%" :max-height='adaptivePageHeight'>
                        <el-table-column type="index" label="No." width="120" header-align="center" align="center"></el-table-column>

                        <el-table-column prop="role_name" label="组名" header-align="center" align="center">
                            <template slot-scope="scope">
                                <span class="a-group" :title="groupTitleValue" type="text" @click="clickGroupUser(scope.$index, scope.row)">{{scope.row.group_name}}</span>
                            </template>
                        </el-table-column>

                        <el-table-column prop="count" label="用户数" align="center" header-align="center"></el-table-column>

                        <el-table-column label="操作" align="center" header-align="center">
                            <template slot-scope="scope">
                                <span @click="editGroup(scope.$index, scope.row)" class="column-span mg10">[ 编辑 ]</span>
                                <span @click="deleteGroup(scope.$index, scope.row)" class="column-span mg10">[ 删除 ]</span>

                            </template>
                        </el-table-column>
                    </el-table>

                </div> -->
            <!-- 组详细 -->
            <!-- <div class="custom-tree-container" v-show="G_flag2">
                    <div class="group-user-list">
                        <div class="table-top group-title">
                            <span>组：{{click_rowData.group_name}}</span>
                        </div>
                        <el-table class="diy_table" :data="tableDataGroupUser" border :max-height='adaptivePageHeight'>
                            <el-table-column prop="username" label="用户" min-width="100" header-align="center" align="center"></el-table-column>
                            <el-table-column prop="role" label="角色" min-width="200" header-align="center" align="left">
                                <template slot-scope="scope">
                                    <span type="text" v-for="(items, index) in scope.row.role_list" :key="index"><img src="../../assets/img/Icon/user_icon_2.png" class="user-icon" />{{items}} </span>
                                </template>
                            </el-table-column>

                            <el-table-column label="操作" min-width="100" header-align="center" align="center">
                                <template slot-scope="scope">
                                    <span @click="deleteGroupUser(scope.$index, scope.row)" class="column-span mg10">[ 删除 ]</span>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                    <div class="add-group-user-list">
                        <p class="createUser">全部用户</p>
                        <span @keyup.enter="searchUserFun(search_user)">
                            <el-input class="search-input" type="text" clearable @clear="clearSearchUser()" v-on:input="clearSearchUser()" placeholder="搜索成员" size='mini' v-model="search_user"></el-input>
                        </span> -->
            <!--多选框用户列表-->
            <!-- <div>
                            <el-checkbox-group class="checkbox-group" v-model="checkUserList">
                                <el-checkbox class="checkbox-item" v-for="GroupUser_item in checkUserList_group" :key="GroupUser_item.user_id" :label="GroupUser_item.user_id">{{GroupUser_item.username }}</el-checkbox>
                            </el-checkbox-group>
                        </div>
                        <el-button class="createUser-submit" @click="Add_GroupUser(checkUserList)" size="mini" type="text">[&nbsp;新&nbsp;增&nbsp;]</el-button>
                    </div>
                </div>
            </el-tab-pane> -->
        </el-tabs>
        <!-- 左边顶部导航栏 -->
        <div class="dialog">
            <!-- 新建组 -->
            <el-dialog title="新建组名称" :visible.sync="createGroupFlag" width="30%" :before-close="closeEditDialog">
                <el-form ref="form" :model="submitNewUserData" label-width="30%">
                    <el-form-item label="新建组名称">
                        <el-input v-model="submitNewUserData.name"></el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" size="mini" @click="SaveEditUserDialog()">确 定</el-button>
                    <el-button size="mini" @click="cancelEditUserDialog()">取 消</el-button>
                </span>
            </el-dialog>
            <!-- 修改组 -->
            <el-dialog title="修改组名称" :visible.sync="editGroupFlag" width="30%" :before-close="closeEditDialog">
                <el-form ref="form" :model="submitNewUserData" label-width="30%">
                    <el-form-item label="修改组名称">
                        <el-input v-model="submitNewUserData.name" :placeholder='showPlaceholder'></el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" size="mini" @click="SaveEditUserDialog()">确 定</el-button>
                    <el-button size="mini" @click="cancelEditUserDialog()">取 消</el-button>
                </span>
            </el-dialog>
            <!-- 修改用户的角色 -->
            <el-dialog title="修改角色名称" :visible.sync="editRoleFlag" width="30%" :before-close="closeEditDialog">
                <el-checkbox-group class="checkbox-role" v-model="checkRoleModel">
                    <el-checkbox class="checkbox-role-item" v-for="items in roleData" :key="items.role_id" :label="items.role_id">{{items.role_name }}</el-checkbox>
                </el-checkbox-group>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" size="mini" @click="SaveEditUserDialog()">确 定</el-button>
                    <el-button size="mini" @click="cancelEditUserDialog()">取 消</el-button>
                </span>
            </el-dialog>
        </div>
    </div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js');
$(document).ready(function () {
    $('.highlight-col table').on('mouseover', 'td', function () {
        let claStyle = $(this).attr('class');
        $('.' + claStyle).css('background-color', '#ecf5ff');
    });
    $('.highlight-col table').on(' mouseout', 'td', function () {
        let claStyle = $(this).attr('class');
        $('.' + claStyle).css('background-color', '');
        $(this).siblings().find('input').css('background-color', '');
    });
});
export default {
    data () {
        return {
            activeName: 'user-role',
            adaptivePageHeight: window.innerHeight - 216,
            click_rowData: {},
            checkRoleModel: [],
            colForConfig: [],
            checkUserList: [],
            checkUserList_groupBegin: [],
            checkUserList_group: [],
            createGroupFlag: false,
            dialogSaveType: "",
            editRoleFlag: false,
            editGroupFlag: false,
            filterRole: '',
            filterName: '',
            filterGroup: '',
            filterData: [],
            filterType: "",
            groupTitleValue: '新建用户',
            G_flag: true,
            G_flag2: false,
            roleData: [{ "role_name": "leader", "role_id": 1 }, { "role_name": "member", "role_id": 0 }],
            search_user: '',
            showPlaceholder: '',
            subUserManageData: [],
            subUserManageArray: [],
            submitNewUserData: {
                name: ''
            },
            tableDataGroup: [],
            tableDataGroupBegin: [],
            tableDataGroupUser: [],
            tableDataRoleBegin: [],
            tableDataRole: [],
            userManageBodyDataRole: [],
            userManageBodyData: [],
            userManageHeadData: [],
            userManageBodyDataBegin: [],
            uniqueArray: [],
            page: 1,
            page_size: 100,
            page_count: 0,

        }
    },
    computed: {
        getUserIcons () {
            return this.$store.state.workType
        },
    },
    watch: {
        getUserIcons (val) {
            this.chooseManageStyle(window.sessionStorage.getItem('activeIndex2'))
        },
    },
    created () {
        this.windowOnresize()
        // 获取用户权限:
        // this.getUserPermission()
    },
    mounted () {
        this.chooseManageStyle(window.sessionStorage.getItem('activeIndex2'))
        // this.reqTableData()
    },
    methods: {
        chooseManageStyle (value) {
            switch (value) {
                case '3-4-4':
                    this.activeName = 'user-role'
                    this.tab_click(this.activeName)
                    break;
                case '3-4-5':
                    this.activeName = 'role-permission'
                    this.tab_click(this.activeName)
                    break;
                case '3-4-6':
                    this.activeName = 'group'
                    this.tab_click(this.activeName)
                    break;
                default:
                    break;
            }
        },
        AddUserManageData (rowUserID) {
            this.subUserManageArray.push(rowUserID)
        },
        // 处理插入表格的数据
        AddNewCol (data) {
            data.push({
                label: '大权限1',
                opt: [
                    { 'prop': 'date', 'label': '权限1' },
                    { 'prop': 'address', 'label': '权限2' },
                    { 'prop': 'checked1', 'label': '权限3' },
                    { 'prop': 'checked2', 'label': '权限4' },
                    { 'prop': 'checked3', 'label': '权限5' }
                ]
            })
        },
        Add_GroupUser (addUser) {
            if (this.userPurviewManage('组管理') == true) {
                var group_id = this.click_rowData.group_id
                var groupData = []
                for (let i = 0; i < addUser.length; i++) {
                    groupData.push({ "group_id": group_id, "user_id": addUser[i] })
                }
                this.$axios.post(this.Ip + "/ApiGroupMembers", groupData).then(res => {
                    if (res.data.result == "OK") {
                        this.getTableDataGroupUser(group_id)
                    } else {
                        this.$message({
                            type: "error",
                            message: "提交失败"
                        })
                    }
                })
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        clearFilterName () {
            if (this.filterName == "") {
                this.userManageBodyData = []
                this.userManageBodyData = this.userManageBodyDataBegin
                // 清空筛选用户的赋值类
                this.filterType = ""
                return
            }
            this.userManageBodyData = []
            this.userManageBodyData = this.userManageBodyDataBegin
            this.filterType = ""
        },
        clearFilterRole () {
            if (this.filterRole == "") {
                this.tableDataRole = []
                this.tableDataRole = this.tableDataRoleBegin
                return
            }
            this.tableDataRole = []
            this.tableDataRole = this.tableDataRoleBegin
        },
        clearFilterGroup () {
            if (this.filterGroup == "") {
                this.tableDataGroup = []
                this.tableDataGroup = this.tableDataGroupBegin
                return
            }
            this.tableDataGroup = []
            this.tableDataGroup = this.tableDataGroupBegin
        },
        clearSearchUser () {
            if (this.search_user == "") {
                this.checkUserList_group = []
                this.checkUserList_group = this.checkUserList_groupBegin
                return
            }
            this.checkUserList_group = []
            this.checkUserList_group = this.checkUserList_groupBegin
        },
        // 弹框关闭
        closeEditDialog (done) {
            this.editGroupFlag = false
            this.editRoleFlag = false
            this.createGroupFlag = false
        },
        // 弹框编辑取消        
        cancelEditUserDialog () {
            this.editGroupFlag = false
            this.editRoleFlag = false
            this.createGroupFlag = false
        },
        // 新建组
        createGroup () {
            if (this.userPurviewManage('组管理') == true) {
                this.submitNewUserData.name = ''
                this.dialogSaveType = "createGroup"
                this.createGroupFlag = true
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        // 新建用户
        clickGroupUser (index, row) {
            this.G_flag = false
            this.G_flag2 = true
            if (this.G_flag2 == true) {
                this.click_rowData = row
                this.getTableDataGroupUser(row.group_id)
                // 右边所有用户列表
                this.$axios.get(this.Ip + "/User").then(res => {
                    this.checkUserList_groupBegin = res.data.content
                    this.checkUserList_group = res.data.content

                }).catch(err => {
                    this.$message({
                        type: "error",
                        message: "服务器异常"
                    })
                })
                // 清空列表勾选
                this.checkUserList = [];
            }
        },
        // 删除组
        deleteGroup (index, row) {
            if (this.userPurviewManage('组管理') == true) {
                this.$confirm(this.globalData.hint.delete, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$axios.delete(this.Ip + "/ApiGroup/" + row.group_id).then(res => {
                        if (res.data.result == "OK") {
                            // 调用组别表格数据请求：
                            this.getTableDataGroup()
                            this.$message({
                                type: "success",
                                message: "删除成功!"
                            })
                        } else {
                            this.$message({
                                type: "error",
                                message: "删除失败，" + res.data.error
                            })
                        }
                    })
                })
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        // 删除单个组内的成员
        deleteGroupUser (index, row) {
            if (this.userPurviewManage('组管理') == true) {
                this.$confirm(this.globalData.hint.delete, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$axios.delete(this.Ip + "/ApiGroupMembers/" + row.group_id + "/" + row.user_id).then(res => {
                        if (res.data.result == "OK") {
                            // 调用组别表格数据请求：
                            this.getTableDataGroupUser(row.group_id)
                            this.$message({
                                type: "success",
                                message: "删除成功!"
                            })
                        } else {
                            this.$message({
                                type: "error",
                                message: "删除失败，" + res.data.error
                            })
                        }
                    })
                })
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        // 单独编辑组
        editGroup (index, row) {
            if (this.userPurviewManage('组管理') == true) {
                this.click_rowData = row
                this.submitNewUserData.name = ''
                this.showPlaceholder = row.group_name
                this.dialogSaveType = "editGroup"
                this.editGroupFlag = true;
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        editRole (index, row) {
            this.checkRoleModel = []
            this.dialogSaveType = "editRole"
            this.click_rowData = row
            this.editRoleFlag = true
        },
        filterNameFun (val) {
            if (this.filterName == '') {
                this.$message.warning("查询名字不能为空")
            } else {
                this.$axios.get(this.Ip + "/UserRoleQuery/" + this.page + "/" + this.page_size + "/" + this.filterName).then(res => {
                    if (res.data.result == 'OK') {
                        this.userManageBodyData = res.data.content
                        this.page_count = res.data.count
                        // 搜索人名赋值一个类，用于确定按钮走全体还是个人接口
                        this.filterType = "filterNameFun"
                    } else {
                        this.$message({
                            type: 'error',
                            showClose: true,
                            message: '无数据'
                        })
                        this.userManageBodyData = []
                        this.page_count = 0
                    }
                }).catch(err => {
                    this.$message({
                        type: 'error',
                        message: '服务异常'
                    })
                })
            }
        },
        filterRoleFun (val) {
            this.tableDataRole = []
            if (this.filterRole == '') {
                this.$message.warning("查询角色不能为空")
            } else {
                for (let item of this.tableDataRoleBegin) {
                    if (item.role_name) {
                        if (item.role_name.indexOf(this.filterRole) >= 0) {
                            this.tableDataRole.push(item)
                        }
                    }
                }
            }
        },
        filterGroupFun (val) {
            this.tableDataGroup = []
            if (this.filterGroup == '') {
                this.$message.warning("查询组名不能为空")
            } else {
                for (let item of this.tableDataGroupBegin) {
                    if (item.group_name) {
                        if (item.group_name.indexOf(this.filterGroup) >= 0) {
                            this.tableDataGroup.push(item)
                        }
                    }
                }
            }
        },
        // 组表格请求后台数据
        getTableDataGroup () {
            this.$axios.get(this.Ip + "/ApiGroup").then(res => {
                if (res.data.result == "OK") {
                    this.tableDataGroupBegin = res.data.content
                    this.tableDataGroup = this.tableDataGroupBegin
                }
            })
        },
        getTableDataGroupUser (group_id) {
            this.$axios.get(this.Ip + "/ApiGroupMembers/" + group_id).then(res => {
                this.tableDataGroupUser = res.data.content
            });
        },
        reqTableData () {
            this.reqUserData()
            this.reqRoleData()
        },
        // 请求角色数据
        reqRoleData () {
            this.tableDataRole = []
            this.$axios.get(this.Ip + '/RolePermission').then(res => {
                if (res.data.result === 'OK') {
                    this.tableDataRoleBegin = res.data.content
                    // 分离数据变量
                    this.tableDataRole = this.tableDataRoleBegin
                    var newArray = []
                    for (const items of this.tableDataRoleBegin) {
                        if (items.role_name == "Admin" || items.role_name == "Admin_KnowledgeDB") {
                            newArray.push(items)
                        } else {
                            break
                        }
                    }
                    // this.userManageBodyDataRole = this.tableDataRoleBegin
                    this.userManageBodyDataRole = newArray
                }
            }).catch(err => {
                this.$message({
                    type: "error",
                    message: '服务异常'
                });
            })

        },
        //请求用户数据
        reqUserData () {
            this.$axios.get(this.Ip + '/ApiUserRole/' + this.page + "/" + this.page_size).then(res => {
                if (res.data.result === 'OK') {
                    this.userManageBodyDataBegin = res.data.content
                    this.userManageBodyData = this.userManageBodyDataBegin;
                    this.page_count = res.data.count
                }
            }).catch(
                err => {
                    this.$message({
                        type: "error",
                        message: '服务异常'
                    });
                })
        },
        // 请求权限数据
        reqAuthorization () {
            this.$axios.get(this.Ip + '/Permission ').then(res => {
                if (res.data.result === 'OK') {
                    this.colForConfig = res.data.content
                }
            }).catch(err => {
                this.$message({
                    type: "error",
                    message: '服务异常'
                });
            })
        },
        // 弹框保存
        SaveEditUserDialog () {
            if (this.dialogSaveType == "editGroup") {
                this.editGroupFlag = false
                // 组别管理修改保存：                
                let editGroup = { "group_id": "", "group_name": "" }
                editGroup.group_id = this.click_rowData.group_id
                editGroup.group_name = this.submitNewUserData.name
                this.$axios.put(this.Ip + "/ApiGroup", editGroup).then(res => {
                    if (res.data.result == "OK") {
                        // 调用组别表格数据请求：
                        this.getTableDataGroup()
                        this.$message({
                            type: "success",
                            message: "修改成功!"
                        })
                    } else {
                        this.$message({
                            type: "error",
                            message: "修改失败，" + res.data.error
                        })
                    }
                })
            } else if (this.dialogSaveType == "createGroup") {
                this.createGroupFlag = false
                // 组别管理新建保存：                
                let creteGroupName = { "group_name": '' }
                creteGroupName.group_name = this.submitNewUserData.name;
                this.$axios.post(this.Ip + "/ApiGroup", creteGroupName).then(res => {
                    if (res.data.result == "OK") {
                        // 调用组别表格数据请求：
                        this.getTableDataGroup()
                        this.$message({
                            type: "success",
                            message: "新建成功!"
                        })
                    } else {
                        this.$message({
                            type: "error",
                            message: "新建失败，" + res.data.error
                        })
                    }
                })
            } else if (this.dialogSaveType == "editRole") {
                let editRoleData = []
                for (let i = 0; i < this.checkRoleModel.length; i++) {
                    editRoleData.push({ "user_id": this.click_rowData.user_id, "group_id": this.click_rowData.group_id, "group_role_id": this.checkRoleModel[i] })
                }
                this.$axios.put(this.Ip + "/ApiGroupMembers", editRoleData).then(res => {
                    if (res.data.result == "OK") {
                        // 调用组别表格数据请求：
                        this.getTableDataGroupUser(this.click_rowData.group_id)
                        this.$message({
                            type: "success",
                            message: "新建成功!"
                        })
                    } else {
                        this.$message({
                            type: "error",
                            message: "新建失败，" + res.data.error
                        })
                    }
                })
                this.editRoleFlag = false
            }
        },
        // 用户搜索：
        searchUserFun () {
            var length = this.checkUserList_group.length
            var userName = []
            if (this.search_user == "") {
                this.$message.warning("用户名不能为空")
            } else {
                for (let i = 0; i < length; i++) {
                    if (this.checkUserList_group[i].username.indexOf(this.search_user) >= 0) {
                        userName.push(this.checkUserList_group[i]);
                    }
                }
                this.checkUserList_group = []
                this.checkUserList_group = userName
            }
        },
        subCharacterData () {
            if (this.userPurviewManage('角色/权限管理') == true) {
                this.$axios.put(this.Ip + '/RolePermission', this.tableDataRole).then(res => {
                    this.$message({
                        type: "success",
                        message: "修改成功"
                    });
                    //重新请求角色和权限数据
                    // this.reqRoleData()
                    // this.reqUserData()
                }).catch(err => {
                    this.$message({
                        type: "error",
                        message: err
                    });
                })
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                });
            }
        },
        subUserManage (userArray) {
            if (this.userPurviewManage('用户管理') == true) {
                this.uniqueArray = []
                this.subUserManageData = []
                this.unique(userArray)
                for (let i = 0; i < this.uniqueArray.length; i++) {
                    let currentUserID = this.uniqueArray[i]
                    for (let j = 0; j < this.userManageBodyData.length; j++) {
                        if (currentUserID == this.userManageBodyData[j].user_id) {
                            this.subUserManageData.push(this.userManageBodyData[j])
                            break
                        }
                    }
                }
                this.$axios.put(this.Ip + '/ApiUserRole', this.subUserManageData).then(res => {
                    this.subUserManageArray = []
                    this.$message({
                        type: "success",
                        message: "修改成功"
                    });
                    //重新请求用户数据
                    if (this.filterType == "filterNameFun") {
                        this.filterNameFun()
                    } else {
                        this.reqUserData()
                    }
                }).catch(err => {
                    this.$message({
                        type: "error",
                        message: err
                    });
                })
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有操作权限！"
                })
            }
        },
        tab_click (activeName) {
            if (activeName == "user-role") {
                // 用户权限表格数据请求
                this.reqTableData()
                window.sessionStorage.setItem('activeIndex2', '3-4-4')
                window.sessionStorage.setItem('diffTitleType', 'userManagement')
                this.$store.state.high_type = "3-4-4"
            } else if (activeName == "role-permission") {
                // 角色权限管理表格数据请求
                this.reqAuthorization()
                this.reqRoleData()
                window.sessionStorage.setItem('activeIndex2', '3-4-5')
                window.sessionStorage.setItem('diffTitleType', 'roleManagement')
                this.$store.state.high_type = "3-4-5"
            } else {
                this.G_flag = true
                this.G_flag2 = false;
                if (this.G_flag == true) {
                    // 调用（组别管理）表格请求：
                    this.getTableDataGroup()
                    window.sessionStorage.setItem('activeIndex2', '3-4-6')
                    window.sessionStorage.setItem('diffTitleType', 'teamManagement')
                    this.$store.state.high_type = "3-4-6"
                }
            }
        },
        unique (numArray) {
            for (let i = 0; i < numArray.length; i++) {
                let current = numArray[i]
                if (this.uniqueArray.indexOf(current) === -1) {
                    this.uniqueArray.push(current)
                }
            }
        },
        windowOnresize () {
            this.adaptivePageHeight = window.innerHeight - 216
            const that = this
            window.onresize = () => {
                return (() => {
                    that.adaptivePageHeight = window.innerHeight - 216
                })()
            }
        },
        listPageChange (pageNum) {
            this.page = pageNum
            this.$axios.get(this.Ip + '/ApiUserRole/' + this.page + "/" + this.page_size).then(res => {
                if (res.data.result === 'OK') {
                    this.userManageBodyDataBegin = res.data.content
                    this.userManageBodyData = this.userManageBodyDataBegin;
                    this.page_count = res.data.count
                }
            }).catch(
                err => {
                    this.$message({
                        type: "error",
                        message: '服务异常'
                    });
                })
        }
    }
}
</script>

<style scoped>
.wrapper .custom-tree-container .el-table thead.is-group th {
    background: white !important;
}
.wrapper {
    margin: 0;
    position: relative;
    display: inline-block;
    width: 100%;
    height: 100%;
    color: #606266;
}
.el-tabs-left {
    width: 100%;
    height: 100%;
    min-width: 1024px;
    overflow: hidden;
}

.custom-tree-container {
    width: 100%;
    padding-left: 20px;
}
.table-top {
    padding: 20px 0 20px 0;
}
.div-input {
    display: inline-block;
    width: 50%;
}
.append-span {
    float: right;
    margin-right: 44px;
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}
.a-group {
    cursor: pointer;
}
.a-group:hover {
    color: #42b983;
}
.group-title {
    font-size: 14px;
}
.user-icon {
    width: 16px;
    vertical-align: middle;
}
.group-user-list {
    width: 70%;
    float: left;
}
.add-group-user-list {
    width: 20%;
    height: 100%;
    float: right;
    margin-top: 26px;
    border: 1px solid rgb(223, 230, 236);
    border-radius: 5px;
}
.createUser {
    position: absolute;
    width: 80px;
    text-align: center;
    line-height: 30px;
    top: 14px;
    right: 6.5%;
    font-size: 14px;
    background: rgb(255, 255, 255);
    font-weight: bold;
}
.createUser-submit {
    margin-left: 45%;
    color: #606266;
}
.checkbox-group {
    width: 80%;
    margin: 20px 0 0 40px;
    height: 500px;
    overflow-y: auto;
}
.search-input {
    width: 80%;
    display: block;
    margin: 20px 0 20px 40px;
    text-align: left;
    letter-spacing: 0.8em;
}
.checkbox-item {
    width: 100%;
    margin-left: 0;
    margin-bottom: 15px;
}

.column-span {
    cursor: pointer;
    padding: 5px;
    /* display: block; */
    /* float: left; */
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear;
}
.column-span:hover {
    color: #6bcca0;
}
.form-page {
    position: absolute;
    bottom: 20px;
}
@media only screen and (max-width: 1024px) {
    .createUser {
        width: 50px;
        line-height: 20px;
        top: 14px;
        right: 6.5%;
        font-size: 12px;
    }
    .createUser-submit {
        margin-left: 45%;
    }
    .checkbox-group {
        width: auto;
        margin: 0 0 0 20px;
        height: 380px;
        overflow-y: auto;
    }
    .search-input {
        width: 80%;
        display: block;
        margin: 10px 0 10px 20px;
        text-align: left;
        letter-spacing: 0.8em;
    }
    .append-span {
        font-size: 12px;
    }
}
@media only screen and (max-width: 1366px) {
    .createUser {
        width: 50px;
        line-height: 20px;
        top: 14px;
        right: 6.5%;
        font-size: 12px;
    }
    .createUser-submit {
        margin-left: 45%;
    }
    .checkbox-group {
        width: auto;
        margin: 0 0 0 20px;
        height: 380px;
        overflow-y: auto;
    }
    .search-input {
        width: 80%;
        display: block;
        margin: 10px 0 10px 20px;
        text-align: left;
        letter-spacing: 0.8em;
    }
    .append-span {
        font-size: 12px;
    }
}
</style>
