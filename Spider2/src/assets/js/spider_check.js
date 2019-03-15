var SpiderCheck;
export default SpiderCheck = {};

SpiderCheck.CHECK_COMMON_NOT_EMPTY = 1;
SpiderCheck.CHECK_COMMON_RESPONSIBLE_SEQ_FORMAT = 2;
SpiderCheck.CHECK_COMMON_RESPONSIBLE_SEQ_NUMBER = 3;
SpiderCheck.CHECK_COMMON_RESPOINSIBLE_STATUS = 4;
SpiderCheck.CHECK_COMMON_RESPOINSIBLE_TRIGGER = 5;
SpiderCheck.CHECK_COMMON_RESPOINSIBLE_ACTION = 6;
SpiderCheck.CHECK_COMMON_RESPOINSIBLE_DEVICE = 7;

SpiderCheck.CHECK_HUDEF_DOC_SYSTEM = 20;
SpiderCheck.CHECK_HUDEF_DOC_AVCLAN = 21;

SpiderCheck.CHECK_TAGLDEF_REMARK = 30;
SpiderCheck.CHECK_TAGLDEF_REF_DOC = 31;

SpiderCheck.check_data = function (rule_id, ...data_info) {
    switch (rule_id) {
        case SpiderCheck.CHECK_COMMON_NOT_EMPTY : {
            if (data_info.length != 1) {
                console.log('CHECK_COMMON_NOT_EMPTY param error!!');
                return false
            }
            else {
                return SpiderCheck.check_common_not_empty_info(data_info[0])
            }
        }
        case SpiderCheck.CHECK_COMMON_RESPONSIBLE_SEQ_FORMAT : {
            if (data_info.length != 1) {
                console.log('CHECK_COMMON_RESPONSIBLE_SEQ_FORMAT param error!!');
                return false
            }
            else {
                return SpiderCheck.check_common_responsible_seq_format_info(data_info[0])
            }
        }
        case SpiderCheck.CHECK_COMMON_RESPONSIBLE_SEQ_NUMBER : {
            if (data_info.length != 1) {
                console.log('CHECK_COMMON_RESPONSIBLE_SEQ_NUMBER param error!!');
                return false
            }
            else {
                return SpiderCheck.check_common_responsible_seq_number_info(data_info[0]);
            }
        }
        case SpiderCheck.CHECK_COMMON_RESPOINSIBLE_STATUS : {
            if (data_info.length != 1) {
                console.log('CHECK_COMMON_RESPOINSIBLE_STATUS param error!!');
                return false
            }
            else {
                return SpiderCheck.check_common_responsible_status_info(data_info[0]);
            }
        }
        case SpiderCheck.CHECK_COMMON_RESPOINSIBLE_TRIGGER : {
            if (data_info.length != 1) {
                console.log('CHECK_COMMON_RESPOINSIBLE_TRIGGER param error!!');
                return false
            }
            else {
                return SpiderCheck.check_common_responsible_trigger_info(data_info[0]);
            }
        }
        case SpiderCheck.CHECK_COMMON_RESPOINSIBLE_ACTION : {
            if (data_info.length != 1) {
                console.log('CHECK_COMMON_RESPOINSIBLE_ACTION param error!!');
                return false
            }
            else {
                return SpiderCheck.check_common_responsible_action_info(data_info[0]);
            }
        }
        case SpiderCheck.CHECK_COMMON_RESPOINSIBLE_DEVICE : {
            if (data_info.length != 1) {
                console.log('CHECK_COMMON_RESPOINSIBLE_DEVICE param error!!');
                return false
            }
            else {
                return SpiderCheck.check_common_responsible_device_info(data_info[0]);
            }
        }
        case SpiderCheck.CHECK_HUDEF_DOC_SYSTEM : {
            if (data_info.length != 1) {
                console.log('CHECK_HUDEF_DOC_SYSTEM param error!!');
                return false
            }
            else {
                return SpiderCheck.check_hudef_doc_system_info(data_info[0]);
            }
        }
        case SpiderCheck.CHECK_HUDEF_DOC_AVCLAN : {
            if (data_info.length != 1) {
                console.log('CHECK_HUDEF_DOC_AVCLAN param error!!');
                return false
            }
            else {
                return SpiderCheck.check_hudef_doc_avclan_info(data_info[0]);
            }
        }
        case SpiderCheck.CHECK_TAGLDEF_REMARK : {
            if (data_info.length != 1) {
                console.log('CHECK_TAGLDEF_REMARK param error!!');
                return false
            }
            else {
                return SpiderCheck.check_tagldef_remark_info(data_info[0]);
            }
        }
        case SpiderCheck.CHECK_TAGLDEF_REF_DOC : {
            if (data_info.length != 1) {
                console.log('CHECK_TAGLDEF_REF_DOC param error!!');
                return false
            }
            else {
                return SpiderCheck.check_tagldef_refdoc_info(data_info[0]);
            }
        }
    }
};

SpiderCheck.is_equal_char = function (src_char, cmp_char) {
    return src_char == cmp_char;
};

SpiderCheck.check_common_not_empty_info = function (char_info) {
    return !SpiderCheck.is_equal_char(char_info, '');
};

SpiderCheck.check_common_responsible_seq_format_info = function (data_info) {
    let pattern_normal = /^\(\d+\)/
    let pattern_multi_no = /^\(\d+\[\w+\]\)/
    if (pattern_normal.test(data_info) == true){
        return true;
    }
    else if(pattern_multi_no.test(data_info) == true){
        return true;
    }
    return false;

}

//检查动作的序号必须是1,2,3的顺序排列，当中可以重复，但是数字不能跳跃
SpiderCheck.check_common_responsible_seq_number_info = function (responsible_list) {
    if (responsible_list.length == 0) {
        return true;
    }
    let seq_number_list = [];
    let seq_number_pattern = /^\((\d+)\D/
    for (let responsible_dict of responsible_list) {
        let action_match = seq_number_pattern.exec(responsible_dict.action)
        if (action_match) {
            seq_number_list.push(Number(action_match[1]))
        }
        else {
            continue;
        }
    }

    for (let check_index = 1; check_index < seq_number_list.length; check_index++) {
        if (seq_number_list[check_index] < seq_number_list[check_index-1]) {
            return false;
        }
        if (seq_number_list[check_index] - seq_number_list[check_index-1] > 1){
            return false;
        }
    }

    return true;
};

SpiderCheck.check_common_responsible_status_info = function(status_info) {
    if (status_info == null || status_info.length == 0){
        return false;
    }
    else if(status_info.length == 1) {
        return SpiderCheck.is_equal_char(status_info,"-")
    }

    return true
}

SpiderCheck.check_common_responsible_trigger_info = function(trigger_info) {
    if (trigger_info == null || trigger_info.length == 0){
        return false;
    }
    else if(trigger_info.length == 1) {
        return SpiderCheck.is_equal_char(trigger_info,"-")
    }
    else if(trigger_info.length < 3) {
        return false;
    }
    else {
        return SpiderCheck.check_common_responsible_seq_format_info(trigger_info);
    }
}

SpiderCheck.check_common_responsible_action_info = function(action_info) {
    if (action_info== null || action_info.length == 0){
        return false;
    }
    else if(action_info.length == 1) {
        return SpiderCheck.is_equal_char(action_info,"-")
    }
    else if(action_info.length < 3) {
        return false;
    }
    else {
        return SpiderCheck.check_common_responsible_seq_format_info(action_info);
    }
}

SpiderCheck.check_common_responsible_device_info = function(device_info) {
    if (device_info == null || device_info.length == 0){
        return false;
    }
    else if(device_info.length == 1) {
        return SpiderCheck.is_equal_char(device_info,"-")
    }
    else if(device_info.length == 2) {
        return SpiderCheck.is_equal_char(device_info,"-※")
    }
    
    return true
}

SpiderCheck.check_hudef_doc_system_info = function(doc_info) {
    if (doc_info == null || doc_info.length == 0){
        return false;
    }
    let hu_doc_system_pattern = /[^(\d+|\.)]/
    return !hu_doc_system_pattern.test(doc_info)
} 

SpiderCheck.check_hudef_doc_avclan_info = function(doc_info) {
    if (doc_info == null || doc_info.length == 0) {
        return false;
    }
    else if (doc_info.length == 1) {
        return SpiderCheck.is_equal_char(doc_info,"-")
    }
    else {
        let hu_doc_avclan_pattern = /\d/
        return hu_doc_avclan_pattern.test(doc_info)
    }
} 

SpiderCheck.check_tagldef_remark_info = function(remark_info) {
    if (remark_info == null) {
        return true;
    }
    else if (remark_info.length == 1){
        return SpiderCheck.is_equal_char(remark_info,"-");
    }

    return true;
}

SpiderCheck.check_tagldef_refdoc_info = function (doc_info) {
    if (doc_info == null) {
        return true;
    }
    else if (doc_info.length == 1){
        return SpiderCheck.is_equal_char(doc_info,"-");
    }

    return true;
}
