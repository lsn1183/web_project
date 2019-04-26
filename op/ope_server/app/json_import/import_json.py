import os
import copy
import json
from app.json_import.ope_parser import OpeParser
from app.ctrl.ctrl_screen import *
from app.ctrl.chapter_key_col import *



class ImportJson(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def import_json(self, proj_id, json_file_path=''):
        commit_list = []
        # q = db.session.query(Projects).filter(Projects.proj_name == proj_name).first()
        # proj_id = 3
        update_time = self.get_current_time()
        if not json_file_path:
            json_file_path = "static/17cy/1/___exportspecs___/Page 1.json"
        screen_list = self.parser_ope_json(json_file_path)
        filepath, tempfilename = os.path.split(json_file_path)
        for screen in screen_list:
            attr = screen.attr
            chapter_list = screen.chapter_list
            screen_dict = self.get_screen_dict(attr)
            screen_dict[Screen.image_dir.name] = filepath
            log_dict, screen_id = self.import_db_screen(proj_id, screen_dict, update_time)
            commit_list.append(log_dict)
            model_info = json.dumps(chapter_list[0], ensure_ascii=False)
            log_dict = self.import_db_available_model(screen_id, model_info)
            commit_list.append(log_dict)
            chapter1_list = self.get_chapter1_list(proj_id, chapter_list[1])
            chapter2_list = self.get_chapter2_list(proj_id, chapter_list[2])
            chapter3_list = self.get_chapter3_list(proj_id, chapter_list[3])
            chapter4_list = self.get_chapter4_list(proj_id, chapter_list[4])
            chapter5_list = self.get_chapter5_list(proj_id, chapter_list[5])
            chapter6_list = self.get_chapter6_list(proj_id, chapter_list[6])
            chapter7_list = self.get_chapter7_list(proj_id, chapter_list[7])
            chapter8_list = self.get_chapter8_list(proj_id, chapter_list[8])
            self.import_db_chapter(Chapter1, Chapter1.chapter1_id, screen_id, chapter1_list)
            self.import_db_chapter(Chapter2, Chapter2.chapter2_id, screen_id, chapter2_list)
            self.import_db_chapter(Chapter3, Chapter3.chapter3_id, screen_id, chapter3_list)
            self.import_db_chapter(Chapter4, Chapter4.chapter4_id, screen_id, chapter4_list)
            self.import_db_chapter(Chapter5, Chapter5.chapter5_id, screen_id, chapter5_list)
            self.import_db_chapter(Chapter6, Chapter6.chapter6_id, screen_id, chapter6_list)
            self.import_db_chapter(Chapter7, Chapter7.chapter7_id, screen_id, chapter7_list)
            self.import_db_chapter(Chapter8, Chapter8.chapter8_id, screen_id, chapter8_list)
        # db.session.commit()

    def get_screen_dict(self, attr):
        screen_key_column = CtrlScreen().screen_key_column
        screen_dict = dict()
        attr["ScreenDispRect"] = json.dumps(attr.get("ScreenDispRect"), ensure_ascii=False)
        for key in screen_key_column:
            screen_dict[screen_key_column.get(key)] = attr.get(key)
        return screen_dict

    def get_condition_id(self, proj_id, Condition, ConditionModel):
        key_list = list(Condition.keys())
        condition_dict = dict()
        for key in key_list:
            condition = Condition.get(key)
            condition_model = ConditionModel.get(key)
            log_dict, condition_id = CtrlScreen().add_condition(proj_id, condition, condition_model)
            condition_dict[key] = condition_id
        return condition_dict

    def get_display_id(self, proj_id, Action, ActionModel):
        log_dict, display_id = CtrlScreen().add_display(proj_id, Action, ActionModel)
        return display_id

    def get_property_id(self, proj_id, PropertyType, Property):
        log_dict, property_id = CtrlScreen().add_propertie(proj_id, PropertyType, Property)
        return property_id

    def get_ope_id(self, proj_id, OpeType, ActionEvent):
        log_dict, ope_id = CtrlScreen().add_ope_type(proj_id, OpeType, ActionEvent)
        return ope_id

    def get_event_id(self, proj_id, TrigName, TrigTrig):
        log_dict, event_id = CtrlScreen().add_event(proj_id, TrigName, TrigTrig)
        return event_id

    def get_chapter1_list(self, proj_id, chapter1_list):
        new_chapter_list = []
        for chapter_dict in chapter1_list:
            displayrect = chapter_dict.get("DisplayRect")
            display_dict = chapter_dict.get("Display")
            new_display_dict = dict()
            display_dict['DisplayStates'] = json.dumps(display_dict.get('DisplayStates'), ensure_ascii=False)
            # DisplayPartsType = display_dict.get('DisplayPartsType')
            # if DisplayPartsType == 'ImageBase':
            #     DisplayContent = display_dict.get("DisplayContent")
            #     filepath, imagename = os.path.split(DisplayContent)
            #     display_dict["DisplayContent"] = image_path+'/'+imagename
            DisplayCondition = display_dict.pop("DisplayCondition")
            DisplayConditionModel = display_dict.pop('DisplayConditionModel')
            if not display_dict.get('DisplayAction'):
                display_dict['DisplayAction'] = '-'
            DisplayAction = display_dict.pop('DisplayAction')
            DisplayActionModel = display_dict.pop('DisplayActionModel')
            DisplayProperty = display_dict.pop('DisplayProperty')
            DisplayPropertyType = display_dict.pop('DisplayPropertyType')
            condition_dict = self.get_condition_id(proj_id, DisplayCondition, DisplayConditionModel)
            display_id = self.get_display_id(proj_id, DisplayAction, DisplayActionModel)
            property_id = self.get_property_id(proj_id, DisplayProperty, DisplayPropertyType)
            for key in chapter1_key_column:
                value = display_dict.get(key)
                if not display_dict[key]:
                    print("chapter1缺少："+ key)
                    value = '-'
                new_display_dict[chapter1_key_column.get(key)] = value
            new_display_dict[Chapter1.display_rect.name] = json.dumps(displayrect, ensure_ascii=False)
            for key in condition_dict:
                copy_dict = copy.deepcopy(new_display_dict)
                condition_id = condition_dict.get(key)
                copy_dict[Chapter1.display_condition_branch.name] = key
                copy_dict[Chapter1.display_condition_model_branch.name] = key
                copy_dict[Chapter1.display_condition.name] = condition_id
                copy_dict[Chapter1.display_action.name] = display_id
                copy_dict[Chapter1.display_property.name] = property_id
                new_chapter_list.append(copy_dict)
        return new_chapter_list

    def get_chapter2_list(self, proj_id, chapter2_list):
        new_chapter_list = []
        for chapter_dict in chapter2_list:
            new_chapter_dict = dict()
            chapter_dict['ActiveStates'] = json.dumps(chapter_dict.get('ActiveStates'), ensure_ascii=False)
            ActiveCondition = chapter_dict.pop("ActiveCondition")
            ActiveConditionModel = chapter_dict.pop('ActiveConditionModel')
            ActiveAction = chapter_dict.pop('ActiveAction')
            ActiveActionModel = chapter_dict.pop('ActiveActionModel')
            ActiveProperty = chapter_dict.pop('ActiveProperty')
            ActivePropertyType = chapter_dict.pop('ActivePropertyType')
            condition_dict = self.get_condition_id(proj_id, ActiveCondition, ActiveConditionModel)
            display_id = self.get_display_id(proj_id, ActiveAction, ActiveActionModel)
            property_id = self.get_property_id(proj_id, ActivePropertyType, ActiveProperty)
            for key in chapter2_key_column:
                value = chapter_dict.get(key)
                if not value:
                    print("chapter2缺少：" + key)
                    value = '-'
                new_chapter_dict[chapter2_key_column.get(key)] = value
            for key in condition_dict:
                copy_dict = copy.deepcopy(new_chapter_dict)
                condition_id = condition_dict.get(key)
                copy_dict[Chapter2.active_condition_branch.name] = key
                copy_dict[Chapter2.active_condition_model_branch.name] = key
                copy_dict[Chapter2.active_condition.name] = condition_id
                copy_dict[Chapter2.active_action.name] = display_id
                copy_dict[Chapter2.active_property.name] = property_id
                new_chapter_list.append(copy_dict)
        return new_chapter_list

    def get_chapter3_list(self, proj_id, chapter3_list):
        new_chapter_list = []
        for chapter_dict in chapter3_list:
            new_chapter_dict = dict()
            chapter_dict['ActionStates'] = json.dumps(chapter_dict.get('ActionStates'), ensure_ascii=False)
            ActionCondition = chapter_dict.pop("ActionCondition")
            ActionConditionModel = chapter_dict.pop('ActionConditionModel')
            ActionAction = chapter_dict.pop('ActionAction')
            ActionActionModel = chapter_dict.pop('ActionActionModel')
            if not chapter_dict.get('ActionEvent'):
                chapter_dict['ActionEvent'] = '-'
            ActionEvent = chapter_dict.pop('ActionEvent')
            ActionOpeType = chapter_dict.pop('ActionOpeType')
            condition_dict = self.get_condition_id(proj_id, ActionCondition, ActionConditionModel)
            display_id = self.get_display_id(proj_id, ActionAction, ActionActionModel)
            ope_id = self.get_ope_id(proj_id, ActionOpeType, ActionEvent)
            for key in chapter3_key_column:
                value = chapter_dict.get(key)
                if not value:
                    print("chapter3缺少：" + key)
                    value = '-'
                new_chapter_dict[chapter3_key_column.get(key)] = value
            for key in condition_dict:
                copy_dict = copy.deepcopy(new_chapter_dict)
                condition_id = condition_dict.get(key)
                copy_dict[Chapter3.action_condition_branch.name] = key
                copy_dict[Chapter3.action_condition_model_branch.name] = key
                copy_dict[Chapter3.action_condition.name] = condition_id
                copy_dict[Chapter3.action_action.name] = display_id
                copy_dict[Chapter3.action_ope.name] = ope_id
                new_chapter_list.append(copy_dict)
        return new_chapter_list

    def get_chapter4_list(self, proj_id, chapter4_list):
        new_chapter_list = []
        for chapter_dict in chapter4_list:
            new_chapter_dict = dict()
            HKCondition = chapter_dict.pop("HKCondition")
            HKConditionModel = chapter_dict.pop('HKConditionModel')
            HKAction = chapter_dict.pop('HKAction')
            HKActionModel = chapter_dict.pop('HKActionModel')
            HKEvent = chapter_dict.pop('HKEvent')
            HKOpeType = chapter_dict.pop('HKOpeType')
            condition_dict = self.get_condition_id(proj_id, HKCondition, HKConditionModel)
            display_id = self.get_display_id(proj_id, HKAction, HKActionModel)
            ope_id = self.get_ope_id(proj_id, HKEvent, HKOpeType)
            for key in chapter4_key_column:
                value = chapter_dict.get(key)
                if not value:
                    print("chapter4缺少：" + key)
                    value = '-'
                new_chapter_dict[chapter4_key_column.get(key)] = value
            for key in condition_dict:
                copy_dict = copy.deepcopy(new_chapter_dict)
                condition_id = condition_dict.get(key)
                copy_dict[Chapter4.hk_condition_branch.name] = key
                copy_dict[Chapter4.hk_condition_model_branch.name] = key
                copy_dict[Chapter4.hk_condition.name] = condition_id
                copy_dict[Chapter4.hk_action.name] = display_id
                copy_dict[Chapter4.hk_ope.name] = ope_id
                new_chapter_list.append(copy_dict)
        return new_chapter_list

    def get_chapter5_list(self, proj_id, chapter5_list):
        new_chapter_list = []
        for chapter_dict in chapter5_list:
            new_chapter_dict = dict()
            InitCondition = chapter_dict.pop("InitCondition")
            InitConditionModel = chapter_dict.pop('InitConditionModel')
            InitAction = chapter_dict.pop('InitAction')
            InitActionModel = chapter_dict.pop('InitActionModel')
            condition_dict = self.get_condition_id(proj_id, InitCondition, InitConditionModel)
            display_id = self.get_display_id(proj_id, InitAction, InitActionModel)
            for key in chapter5_key_column:
                value = chapter_dict.get(key)
                if not value:
                    print("chapter5缺少：" + key)
                    value = '-'
                new_chapter_dict[chapter5_key_column.get(key)] = value
            for key in condition_dict:
                copy_dict = copy.deepcopy(new_chapter_dict)
                condition_id = condition_dict.get(key)
                copy_dict[Chapter5.init_condition_branch.name] = key
                copy_dict[Chapter5.init_condition_model_branch.name] = key
                copy_dict[Chapter5.init_condition.name] = condition_id
                copy_dict[Chapter5.init_action.name] = display_id
                new_chapter_list.append(copy_dict)
        return new_chapter_list

    def get_chapter6_list(self, proj_id, chapter6_list):
        new_chapter_list = []
        for chapter_dict in chapter6_list:
            new_chapter_dict = dict()
            StatusChangeBCondition = chapter_dict.pop("StatusChangeBCondition")
            StatusChangeBConditionModel = chapter_dict.pop("StatusChangeBConditionModel")
            StatusChangeFCondition = chapter_dict.pop("StatusChangeFCondition")
            StatusChangeFConditionModel = chapter_dict.pop("StatusChangeFConditionModel")
            StatusChangeICondition = chapter_dict.pop("StatusChangeICondition")
            StatusChangeIConditionModel = chapter_dict.pop("StatusChangeIConditionModel")
            StatusChangeBAction = chapter_dict.pop("StatusChangeBAction")
            StatusChangeBActionModel = chapter_dict.pop('StatusChangeBActionModel')
            StatusChangeFAction = chapter_dict.pop("StatusChangeFAction")
            StatusChangeFActionModel = chapter_dict.pop('StatusChangeFActionModel')
            StatusChangeIAction = chapter_dict.pop("StatusChangeIAction")
            StatusChangeIActionModel = chapter_dict.pop('StatusChangeIActionModel')
            condition_b_dict = self.get_condition_id(proj_id, StatusChangeBCondition, StatusChangeBConditionModel)
            condition_f_dict = self.get_condition_id(proj_id, StatusChangeFCondition, StatusChangeFConditionModel)
            condition_i_dict = self.get_condition_id(proj_id, StatusChangeICondition, StatusChangeIConditionModel)
            display_b_id = self.get_display_id(proj_id, StatusChangeBAction, StatusChangeBActionModel)
            display_f_id = self.get_display_id(proj_id, StatusChangeFAction, StatusChangeFActionModel)
            display_i_id = self.get_display_id(proj_id, StatusChangeIAction, StatusChangeIActionModel)
            for key in chapter6_key_column:
                value = chapter_dict.get(key)
                if not value:
                    print("chapter6缺少：" + key)
                    value = '-'
                new_chapter_dict[chapter6_key_column.get(key)] = value
            for key in condition_b_dict:
                copy_dict = copy.deepcopy(new_chapter_dict)
                condition_b_id = condition_b_dict.get(key)
                condition_f_id = condition_f_dict.get(key)
                condition_i_id = condition_i_dict.get(key)
                copy_dict[Chapter6.status_change_b_condition_branch.name] = key
                copy_dict[Chapter6.status_change_b_condition_model_branch.name] = key
                copy_dict[Chapter6.status_change_f_condition_branch.name] = key
                copy_dict[Chapter6.status_change_f_condition_model_branch.name] = key
                copy_dict[Chapter6.status_change_i_condition_branch.name] = key
                copy_dict[Chapter6.status_change_i_condition_model_branch.name] = key
                copy_dict[Chapter6.status_change_b_condition.name] = condition_b_id
                copy_dict[Chapter6.status_change_f_condition.name] = condition_f_id
                copy_dict[Chapter6.status_change_i_condition.name] = condition_i_id
                copy_dict[Chapter6.status_change_b_action.name] = display_b_id
                copy_dict[Chapter6.status_change_f_action.name] = display_f_id
                copy_dict[Chapter6.status_change_i_action.name] = display_i_id
                new_chapter_list.append(copy_dict)
        return new_chapter_list

    def get_chapter7_list(self, proj_id, chapter7_list):
        new_chapter_list = []
        for chapter_dict in chapter7_list:
            new_chapter_dict = dict()
            TransitionBCondition = chapter_dict.pop("TransitionBCondition")
            TransitionBConditionModel = chapter_dict.pop("TransitionBConditionModel")
            TransitionFCondition = chapter_dict.pop("TransitionFCondition")
            TransitionFConditionModel = chapter_dict.pop("TransitionFConditionModel")
            TransitionICondition = chapter_dict.pop("TransitionICondition")
            TransitionIConditionModel = chapter_dict.pop("TransitionIConditionModel")
            TransitionBAction = chapter_dict.pop("TransitionBAction")
            TransitionBActionModel = chapter_dict.pop('TransitionBActionModel')
            TransitionFAction = chapter_dict.pop("TransitionFAction")
            TransitionFActionModel = chapter_dict.pop('TransitionFActionModel')
            TransitionIAction = chapter_dict.pop("TransitionIAction")
            TransitionIActionModel = chapter_dict.pop('TransitionIActionModel')
            condition_b_dict = self.get_condition_id(proj_id, TransitionBCondition, TransitionBConditionModel)
            condition_f_dict = self.get_condition_id(proj_id, TransitionFCondition, TransitionFConditionModel)
            condition_i_dict = self.get_condition_id(proj_id, TransitionICondition, TransitionIConditionModel)
            display_b_id = self.get_display_id(proj_id, TransitionBAction, TransitionBActionModel)
            display_f_id = self.get_display_id(proj_id, TransitionFAction, TransitionFActionModel)
            display_i_id = self.get_display_id(proj_id, TransitionIAction, TransitionIActionModel)
            for key in chapter7_key_column:
                value = chapter_dict.get(key)
                if not value:
                    print("chapter7缺少：" + key)
                    value = '-'
                new_chapter_dict[chapter7_key_column.get(key)] = value
            for key in condition_b_dict:
                copy_dict = copy.deepcopy(new_chapter_dict)
                condition_b_id = condition_b_dict.get(key)
                condition_f_id = condition_f_dict.get(key)
                condition_i_id = condition_i_dict.get(key)
                copy_dict[Chapter7.transition_b_condition_branch.name] = key
                copy_dict[Chapter7.transition_b_condition_model_branch.name] = key
                copy_dict[Chapter7.transition_f_condition_branch.name] = key
                copy_dict[Chapter7.transition_f_condition_model_branch.name] = key
                copy_dict[Chapter7.transition_i_condition_branch.name] = key
                copy_dict[Chapter7.transition_i_condition_model_branch.name] = key
                copy_dict[Chapter7.transition_b_condition.name] = condition_b_id
                copy_dict[Chapter7.transition_f_condition.name] = condition_f_id
                copy_dict[Chapter7.transition_i_condition.name] = condition_i_id
                copy_dict[Chapter7.transition_b_action.name] = display_b_id
                copy_dict[Chapter7.transition_f_action.name] = display_f_id
                copy_dict[Chapter7.transition_i_action.name] = display_i_id
                new_chapter_list.append(copy_dict)
        return new_chapter_list

    def get_chapter8_list(self, proj_id, chapter8_list):
        new_chapter_list = []
        for chapter_dict in chapter8_list:
            new_chapter_dict = dict()
            TrigCondition = chapter_dict.pop("TrigCondition")
            TrigConditionModel = chapter_dict.pop('TrigConditionModel')
            TrigAction = chapter_dict.pop('TrigAction')
            TrigActionModel = chapter_dict.pop('TrigActionModel')
            TrigName = chapter_dict.pop('TrigName')
            TrigTrig = chapter_dict.pop('TrigTrig')
            condition_dict = self.get_condition_id(proj_id, TrigCondition, TrigConditionModel)
            display_id = self.get_display_id(proj_id, TrigAction, TrigActionModel)
            event_id = self.get_event_id(proj_id, TrigName, TrigTrig)
            for key in chapter8_key_column:
                value = chapter_dict.get(key)
                if not value:
                    print("chapter8缺少：" + key)
                    value = '-'
                new_chapter_dict[chapter8_key_column.get(key)] = value
            for key in condition_dict:
                copy_dict = copy.deepcopy(new_chapter_dict)
                condition_id = condition_dict.get(key)
                copy_dict[Chapter8.trig_condition_branch.name] = key
                copy_dict[Chapter8.trig_condition_model_branch.name] = key
                copy_dict[Chapter8.trig_condition.name] = condition_id
                copy_dict[Chapter8.trig_action.name] = display_id
                copy_dict[Chapter8.trig_trig.name] = event_id
                new_chapter_list.append(copy_dict)
        return new_chapter_list

    def parser_ope_json(self, json_file_path):
        """解析json"""
        obj = OpeParser()
        screen_list = obj.parse(json_file_path)
        return screen_list

    def import_db_screen(self, proj_id, screen_dict, update_time):
        """导入screen信息"""
        old_data = None
        new_data = screen_dict
        new_data["proj_id"] = proj_id
        new_data["create_time"] = update_time
        new_data["update_time"] = update_time
        log_dict = CtrlScreen().add_db_screen(new_data, old_data)
        screen_id = log_dict.get("key_id")
        return log_dict, screen_id

    def import_db_available_model(self, screen_id, model_info):
        """导入available_model"""
        old_data = None
        new_data = dict()
        new_data["screen_id"] = screen_id
        new_data[AvailableModel.model_info.name] = model_info
        log_dict = CtrlScreen().add_db_available_model(new_data, old_data)
        return log_dict

    def import_db_chapter(self, db_obj, key_col, screen_id, chapter_list):
        """导入chapter"""
        for chapter in chapter_list:
            chapter["screen_gid"] = screen_id
        self.add_list(db_obj, chapter_list, old_data_list=[], key_col=key_col, col_list=[])

