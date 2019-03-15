import { login, } from '@/api/login'
const other = {
    state: {
        nav_active_index: '',
        backstage_active_index: '',
        operation_type: '',
        operation_data: null,
        tree_node_level: 0,
        tree_node_data_id: 0,
        tree_node_unique_id: 0,
        test_plan_id: 0,
        test_plan_history_id: 0,
        test_plan_page: 1,
        test_case_id: 0,
        test_cae_page: 1,
        token: null,
        proj_id: 0,
        proj_name: null
    },
    // mutations内部必须同步执行
    mutations: {
        SET_NAV_ACTIVE_INDEX: (state, nav_active_index) => {
            state.nav_active_index = nav_active_index
        },
        SET_BACKSTAGE_ACTIVE_INDEX: (state, backstage_active_index) => {
            state.backstage_active_index = backstage_active_index
        },
        SET_OPERATION_TYPE: (state, operation_type) => {
            state.operation_type = operation_type
        },
        SET_OPERATION_DATA: (state, operation_data) => {
            state.operation_data = operation_data
        },
        SET_TREE_NODE_LEVEL: (state, tree_node_level) => {
            state.tree_node_level = tree_node_level
        },
        SET_TREE_NODE_DATA_ID: (state, tree_node_data_id) => {
            state.tree_node_data_id = tree_node_data_id
        },
        SET_TREE_NODE_UNIQUE_ID: (state, tree_node_unique_id) => {
            state.tree_node_unique_id = tree_node_unique_id
        },
        SET_TEST_CASE_ID: (state, test_case_id) => {
            state.test_case_id = test_case_id
        },
        SET_TEST_CASE_PAGE: (state, test_case_page) => {
            state.test_case_page = test_case_page
        },
        SET_TEST_PLAN_PAGE: (state, test_plan_page) => {
            state.test_plan_page = test_plan_page
        },
        SET_TEST_PLAN_ID: (state, test_plan_id) => {
            state.test_plan_id = test_plan_id
        },
        SET_TEST_PLAN_HISTORY_ID: (state, test_plan_history_id) => {
            state.test_plan_history_id = test_plan_history_id
        },
        SET_TOKEN :(state, token)=>{
            state.token = token
        },
        SET_PROJ_ID: (state, proj_id)=>{
            state.proj_id = proj_id
        },
        SET_PROJ_NAME: (state, proj_name)=>{
            state.proj_name = proj_name
        }
    },
    // { commit } ES6 参数解构
    // actions 内部可以执行异步操作
    actions: {
        setNavActiveIndex({ commit }, nav_active_index) {
            commit('SET_NAV_ACTIVE_INDEX', nav_active_index)
        },
        setBackstageActiveIndex({ commit }, backstage_active_index) {
            commit('SET_BACKSTAGE_ACTIVE_INDEX', backstage_active_index)
        },
        setOperationType({ commit }, operation_type) {
            commit('SET_OPERATION_TYPE', operation_type)
        },
        setOperationData({ commit }, operation_data) {
            commit('SET_OPERATION_DATA', operation_data)
        },
        setTreeNodeLevel({ commit }, tree_node_level) {
            commit('SET_TREE_NODE_LEVEL', tree_node_level)
        },
        setTreeNodeDataId({ commit }, tree_node_data_id) {
            commit('SET_TREE_NODE_DATA_ID', tree_node_data_id)
        },
        setTreeNodeUniqueId({ commit }, tree_node_unique_id) {
            commit('SET_TREE_NODE_UNIQUE_ID', tree_node_unique_id)
        },
        setTestCaseId({ commit }, test_case_id) {
            commit('SET_TEST_CASE_ID', test_case_id)
        },
        setTestCasePage({ commit }, test_case_page) {
            commit('SET_TEST_CASE_PAGE', test_case_page)
        },
        setTestPlanPage({ commit }, test_plan_page) {
            commit('SET_TEST_PLAN_PAGE', test_plan_page)
        },
        setTestPlanId({ commit }, test_plan_id) {
            commit('SET_TEST_PLAN_ID', test_plan_id)
        },
        setTestPlanHistoryId({ commit }, test_plan_history_id) {
            commit('SET_TEST_PLAN_HISTORY_ID', test_plan_history_id)
        },
        setProjId({ commit }, proj_id) {
            commit('SET_PROJ_ID', proj_id)
        },
        setProjName({ commit }, proj_name) {
            commit('SET_PROJ_NAME', proj_name)
        }
    }
}

export default other