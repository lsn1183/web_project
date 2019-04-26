class data {
    hasKeyFn(obj) {
        let newArr = []
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                let item = {
                    header: "",
                    value: '',
                    type: ""
                }
                item.header = obj[key]
                item.value = key
                newArr.push(item)
            }
        }
        return newArr
    }
    
    header_matchup_data4() {
        let obj = { //key:对应表头的props值，value：对应表头key,相反的原因：表头可能有合并，所以必须遵循json结构，
            'hk_chapter': '',
            'hk_sub_chapter': '',
            'hk_dev_name': 'Dev Name',
            'hk_no': 'Normal',
            'hk_state_no': 'Normal',
            'hk_name': 'Normal',
            'hk_ope_type': 'Ope Type',
            'hk_formula': 'Formula',
            // 'hk_condition': 'Condition of Action',
            'hk_condition_branch': 'Condition of Action',
            'hk_condition_phrase': 'Condition of Action',
            'hk_action': 'Action in Such Condition',
            'hk_trans': 'Transition',
            'hk_sound': 'Sound',
            'hk_during_driving': 'DuringDriving',
            'hk_remark': 'Remark',
            'null':'',
            'hk_uuid': 'UUID',
            'hk_event':'HardKey Event',
            'hk_condition_model_branch':'View Model',
            'hk_condition_code':'View Model',
            'hk_action_model':'Func of Model',
            'hk_observer':'Observer',
            'hk_reply':'Reply',
            'hk_trans_type':'TransType',
            'hk_trans_id':'TransID'
        }
        return obj
    }
    header_matchup_data5() {
        let obj = { //key:对应表头的props值，value：对应表头key,相反的原因：表头可能有合并，所以必须遵循json结构，
            'init_chapter': '',
            'init_no': 'Initialized Status',
            'init_state_no': 'Initialized Status',
            'init_status': 'Initialized Status',
            'init_formula': 'Formula',
            'init_condition_branch': 'Condition of Action',
            'init_condition_phrase': 'Condition of Action',
            'init_action': 'Action in Such Condition',
            'init_trans': 'Transition',
            'init_remark': 'Remark',
            // 'hk_action': 'Action in Such Condition',
            // 'hk_trans': 'Transition',
            // 'hk_sound': 'Sound',
            // 'hk_during_driving': 'DuringDriving',
            // 'hk_remark': 'Remark',
            'null': '',
            'init_uuid': 'UUID',
            'init_event': 'Event',
            'init_condition_model_branch': 'View Model',
            'init_condition_code': 'View Model',
            'init_action_model': 'Func of Model',
            'init_observer ': 'Observer',
            'init_reply': 'Reply',
            'init_trans_type':'TransType',
            'init_trans_id':'TransID'
        }
        return obj
    }
    header_matchup_data6() {
        let obj = { //key:对应表头的props值，value：对应表头key,相反的原因：表头可能有合并，所以必须遵循json结构，
            'status_change_chapter': '',
            'status_change_sub_chapter': '',
            'status_change_no': 'Normal',
            'status_change_state_no': 'Normal',
            'status_change_name': 'Normal',
            'status_change_f_formula': 'Formula',
            'active_condition_f_branch': 'Condition',
            'active_condition_f_phrase': 'Condition',
            'status_change_f_action': 'Action',
            'status_change_b_formula': 'Formula',
            'status_change_b_condition_branch': 'Condition',
            'status_change_b_condition_phrase': 'Condition',
            'status_change_b_action': 'Action',
            'status_change_i_formula': 'Formula',

            'status_active_condition_i_branch': 'Condition',
            'status_active_condition_i_phrase': 'Condition',
            'status_change_i_action': 'Action',

            'null': '',

            'status_change_uuid': 'UUID',
            'status_change_event': 'Event',
            'status_change_f_condition_model_branch': 'View Model',
            'status_change_f_condition_model_phrase': 'View Model',
            'status_change_f_action_model': 'Func of Model',
            'status_change_f_observer': 'Observer',
            'status_change_f_reply': 'Reply',
            'status_change_b_condition_branch': 'View Model',
            'status_change_b_condition_phrase': 'View Model',
            'status_change_b_action_model': 'Func of Model',

            'status_change_i_observer': 'Observer',
            'status_change_i_reply': 'Reply'
        }
        return obj
    }
    header_matchup_data7() {
        let obj = { //key:对应表头的props值，value：对应表头key,相反的原因：表头可能有合并，所以必须遵循json结构，
            'transition_chapter': '',
            'transition_sub_chapter': '',
            'transition_no': 'Normal',
            'transition_state_no': 'Normal',
            'transition_name': 'Normal',
            'transition_b_formula': 'Formula',
            'transition_b_condition_branch': 'Condition',
            'transition_b_condition_phrase': 'Condition',
            'transition_b_action': 'Action',
            'transition_f_formula': 'Formula',
            'transition_f_condition_branch': 'Condition',
            'transition_f_condition_phrase': 'Condition',
            'transition_f_action': 'Action',
            'transition_i_formula': 'Formula',
            'transition_i_condition_branch': 'Condition',
            'transition_i_condition_phrase': 'Condition',
            'transition_i_action': 'Action',

            'null': '',

            'transition_uuid': 'UUID',
            'transition_event': 'Event',
            'transition_b_condition_model_branch': 'View Model',
            'transition_b_condition_model_phrase': 'View Model',
            'transition_b_action_model': 'Func of Model',
            'transition_b_observer': 'Observer',
            'transition_b_reply': 'Reply',
            'transition_f_condition_model_branch': 'View Model',
            'transition_f_condition_model_phrase': 'View Model',
            'transition_f_action_model': 'Func of Model',
            'transition_f_observer': 'Observer',
            'transition_f_reply': 'Reply',
            'transition_i_condition_model_branch': 'View Model',
            'transition_i_condition_model_phrase': 'View Model',
            'transition_i_action_model': 'Func of Model',
            'transition_i_observer': 'Observer',
            'transition_i_reply': 'Reply',
        }
        return obj
    }
    header_matchup_data8() {
        let obj = { //key:对应表头的props值，value：对应表头key,相反的原因：表头可能有合并，所以必须遵循json结构，
            'trig_chapter': '',
            'trig_sub_chapter': '',
            'trig_state_no': 'Normal',
            'trig_no': 'Normal',
            'trig_name': 'Normal',
            'trig_formula': 'Formula',
            'trig_condition_branch': 'Condition of Action',
            'trig_condition_phrase': 'Condition of Action',
            'trig_action': 'Action in Such Condition',
            'trig_trans': 'Transition',
            'trig_sound': 'Sound',
            'trig_timer': 'Timer',
            'trig_remark': 'Remark',

            'null': '',

            'trig_uuid': 'UUID',
            'trig_trig': 'Trigger',
            'trig-event': 'ONSID',
            'trig_condition_model_phrase': 'View Model',
            'trig_condition_model_phrase': 'View Model',
            'trig_action_model': 'Func of Model',
            'trig_observer': 'Observer',
            'trig_reply': 'Reply',
            'trig_trans_type': 'TransType',
            'trig_trans_id': 'TrainID',
        }
        return obj
    }

}

export default new data()
