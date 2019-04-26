from app.db.models import Chapter1, Chapter2, Chapter3, Chapter4
from app.db.models import Chapter5, Chapter6, Chapter7, Chapter8

chapter1_key_column = {'DisplayRemark': Chapter1.display_remark.name, 'DisplayChapter': Chapter1.display_chapter.name,
                        'DisplayStates': Chapter1.display_states.name, 'Visible': Chapter1.visible.name,
                        'DisplayStateNo': Chapter1.display_state_no.name, 'HasDispInfo': Chapter1.has_disp_info.name,
                        'DataRange': Chapter1.data_range.name, 'DisplayUUID': Chapter1.display_uuid.name,
                        'PartsName': Chapter1.parts_name.name, 'DisplayContent': Chapter1.display_content.name,
                        'PartsID': Chapter1.parts_id.name, 'DisplayFormula': Chapter1.display_formula.name,
                        'DisplaySubChapter': Chapter1.display_sub_chapter.name, 'PartsNumber': Chapter1.parts_number.name,
                        'DisplayPartsType': Chapter1.display_parts_type.name, 'StringID': Chapter1.string_id.name,
                        'DisplayDefaultValue': Chapter1.display_default_value.name}
chapter2_key_column = {
    'ActivePartsType': Chapter2.active_parts_type.name, 'HasActiveInfo': Chapter2.has_disp_info.name,
    'ActiveNo': Chapter2.active_no.name, 'ActiveStateNo': Chapter2.active_state_no.name,
    'ActiveBtnName': Chapter2.active_btn_name.name, 'ActiveChapter': Chapter2.active_chapter.name,
    'ActiveFormula': Chapter2.active_formula.name, 'ActiveDuringDriving': Chapter2.active_during_driving.name,
    'ActiveDefaultValue': Chapter2.active_default_value.name, 'ActiveRemark': Chapter2.active_remark.name,
    'ActiveUUID': Chapter2.active_uuid.name, 'ActiveStates': Chapter2.active_states.name,
    'Active': Chapter2.active.name, 'ActiveSubChapter': Chapter2.active_sub_chapter.name,
}

chapter3_key_column = {
    'ActionObserver': Chapter3.action_observer.name, 'ActionTransType': Chapter3.action_trans_type.name,
    'ActionStates': Chapter3.active_states.name, 'HasActionInfo': Chapter3.has_action_info.name,
    'ActionChapter': Chapter3.action_chapter.name, 'ActionStateNo': Chapter3.action_state_no.name,
    'ActionReply': Chapter3.action_reply.name, 'ActionPartsType': Chapter3.action_parts_type.name,
    'ActionBtnName': Chapter3.action_btn_name.name, 'ActionNo': Chapter3.action_no.name,
    'ActionUUID': Chapter3.action_uuid.name, 'ActionSound': Chapter3.action_sound.name,
    'ActionSubChapter': Chapter3.action_sub_chapter.name, 'ActionRemark': Chapter3.action_remark.name,
    'ActionTrans': Chapter3.action_trans.name, 'ActionTransID': Chapter3.action_trans_id.name,
    'ActionFormula': Chapter3.action_formula.name
}

chapter4_key_column = {
    'HKTrans': Chapter4.hk_trans.name, 'HKSound': Chapter4.hk_sound.name,
    'HKNo': Chapter4.hk_no.name, 'HKFormula': Chapter4.hk_formula.name,
    'HKDevType': Chapter4.hk_dev_type.name, 'HKDuringDriving': Chapter4.hk_during_driving.name,
    'HKTransType': Chapter4.hk_trans_type.name, 'HKDevName': Chapter4.hk_dev_name.name,
    'HKTransID': Chapter4.hk_trans_id.name, 'HKSubChapter': Chapter4.hk_sub_chapter.name,
    'HKUUID': Chapter4.hk_uuid.name, 'HKObserver': Chapter4.hk_observer.name,
    'HKRemark': Chapter4.hk_remark.name, 'HKStateNo': Chapter4.hk_state_no.name,
    'HKName': Chapter4.hk_name.name, 'HKChapter': Chapter4.hk_chapter.name,
    'HKReply': Chapter4.hk_reply.name,
}

chapter5_key_column = {
    'InitStatus': Chapter5.init_status.name, 'InitObserver': Chapter5.init_observer.name,
    'InitReply': Chapter5.init_reply.name, 'InitTransID': Chapter5.init_trans_id.name,
    'InitFormula': Chapter5.init_formula.name, 'InitUUID': Chapter5.init_uuid.name,
    'InitChapter': Chapter5.init_chapter.name, 'InitNo': Chapter5.init_no.name,
    'InitStateNo': Chapter5.init_state_no.name, 'InitTransType': Chapter5.init_trans_type.name,
    'InitTrans': Chapter5.init_trans.name, 'InitEvent': Chapter5.init_event.name,
    'InitRemark': Chapter5.init_remark.name
}

chapter6_key_column = {
    'StatusChangeIObserver': Chapter6.status_change_i_observer.name, 'StatusChangeEvent': Chapter6.status_change_event.name,
    'StatusChangeFObserver': Chapter6.status_change_f_observer.name, 'StatusChangeIFormula': Chapter6.status_change_i_formula.name,
    'StatusChangeChapter': Chapter6.status_change_chapter.name, 'StatusChangeStateNo': Chapter6.status_change_state_no.name,
    'StatusChangeBFormula': Chapter6.status_change_b_formula.name, 'StatusChangeBTrans': Chapter6.status_change_b_trans.name,
    'StatusChangeBReply': Chapter6.status_change_b_reply.name, 'StatusChangeFFormula': Chapter6.status_change_f_formula.name,
    'StatusChangeUUID': Chapter6.status_change_uuid.name, 'StatusChangeFTrans': Chapter6.status_change_f_trans.name,
    'StatusChangeName': Chapter6.status_change_name.name, 'StatusChangeITrans': Chapter6.status_change_i_trans.name,
    'StatusChangeFReply': Chapter6.status_change_f_reply.name, 'StatusChangeNo': Chapter6.status_change_no.name,
    'StatusChangeIReply': Chapter6.status_change_i_reply.name, 'StatusChangeSubChapter': Chapter6.status_change_sub_chapter.name,
    'StatusChangeBObserver': Chapter6.status_change_b_observer.name
}

chapter7_key_column = {
    'TransitionIObserver': Chapter7.transition_i_observer.name, 'TransitionEvent': Chapter7.transition_event.name,
    'TransitionFObserver': Chapter7.transition_f_observer.name, 'TransitionIFormula': Chapter7.transition_i_formula.name,
    'TransitionChapter': Chapter7.transition_chapter.name, 'TransitionStateNo': Chapter7.transition_state_no.name,
    'TransitionBFormula': Chapter7.transition_b_formula.name, 'TransitionBTrans': Chapter7.transition_b_trans.name,
    'TransitionBReply': Chapter7.transition_b_reply.name, 'TransitionFFormula': Chapter7.transition_f_formula.name,
    'TransitionUUID': Chapter7.transition_uuid.name, 'TransitionFTrans': Chapter7.transition_f_trans.name,
    'TransitionName': Chapter7.transition_name.name, 'TransitionITrans': Chapter7.transition_i_trans.name,
    'TransitionFReply': Chapter7.transition_f_reply.name, 'TransitionNo': Chapter7.transition_no.name,
    'TransitionIReply': Chapter7.transition_i_reply.name, 'TransitionSubChapter': Chapter7.transition_sub_chapter.name,
    'TransitionBObserver': Chapter7.transition_b_observer.name
}

chapter8_key_column = {
'TrigChapter': Chapter8.trig_chapter.name, 'TrigSubChapter': Chapter8.trig_sub_chapter.name,
'TrigStateNo': Chapter8.trig_state_no.name, 'TrigNo': Chapter8.trig_no.name,
'TrigFormula': Chapter8.trig_formula.name,
'TrigTrans': Chapter8.trig_trans.name, 'TrigSound': Chapter8.trig_sound.name,
'TrigTimer': Chapter8.trig_timer.name, 'TrigRemark': Chapter8.trig_remark.name,
'TrigUUID': Chapter8.trig_uuid.name, 'TrigEvent': Chapter8.trig_event.name,
'TrigObserver': Chapter8.trig_observer.name, 'TrigReply': Chapter8.trig_reply.name,
'TrigTransType': Chapter8.trig_trans_type.name, 'TrigTransID': Chapter8.trig_trans_id.name,
'TrigSignal': Chapter8.trig_signal.name
}



