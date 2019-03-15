const getters = {
    language: state => state.app.language,
    device: state => state.app.device,
    token: state => state.user.token,
    name: state => state.user.name,
    nav_active_index: state => state.other.nav_active_index,
    backstage_active_index: state => state.other.backstage_active_index,
    operation_type: state => state.other.operation_type,
    operation_data: state => state.other.operation_data,
    tree_node_level: state => state.other.tree_node_level,
    tree_node_data_id: state => state.other.tree_node_data_id,
    tree_node_unique_id: state => state.other.tree_node_unique_id,
    test_plan_id: state => state.other.test_plan_id,
    test_plan_history_id: state => state.other.test_plan_history_id,
    test_case_id: state => state.other.test_case_id,
    test_case_page: state => state.other.test_case_page,
    test_plan_page: state => state.other.test_plan_page,
    proj_id: state => state.other.proj_id,
    proj_name: state => state.other.proj_name
}

export default getters