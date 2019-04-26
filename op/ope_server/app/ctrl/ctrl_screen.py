from app.ctrl.ctrl_base import CtrlBase
from app.db.models import Screen
from app.db.models import AvailableModel
from app.db.models import Conditions
from app.db.models import Displays
from app.db.models import Properties
from app.db.models import OpeTypes
from app.db.models import Events


class CtrlScreen(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.screen_key_column = {"ScreenDispRect": Screen.screen_disp_rect.name, "ScreenUUID": Screen.screen_uuid.name,
                                  "ScreenID": Screen.screen_id.name, "ScreenDispPic": Screen.screen_disp_pic.name,
                                  "ScreenName": Screen.screen_name.name}
        self.col_list = [Screen.screen_name.name, Screen.screen_disp_pic.name,
                         Screen.screen_uuid.name, Screen.screen_disp_rect.name,
                         Screen.screen_id.name, Screen.outline.name, Screen.locked.name]

    def add_db_screen(self, new_data, old_data):
        """更新screen信息"""
        log_dict = self.common_add(Screen, new_data, old_data, self.col_list, Screen.screen_gid)
        return log_dict

    def add_db_available_model(self, new_data, old_data):
        """更新available_model"""
        log_dict = self.common_add(AvailableModel, new_data, old_data, [AvailableModel.model_info.name],
                                   AvailableModel.model_id)
        return log_dict

    def add_db_conditions(self, new_data, old_data):
        """更新conditions"""
        log_dict = self.common_add(Conditions, new_data, old_data,
                                   [Conditions.condition.name, Conditions.view_model.name],
                                   Conditions.condition_id)
        return log_dict

    def add_db_displays(self, new_data, old_data):
        """更新displays"""
        log_dict = self.common_add(Displays, new_data, old_data,
                                   [Displays.display.name, Displays.fun_of_model.name],
                                   Displays.display_id)
        return log_dict

    def add_db_properties(self, new_data, old_data):
        """更新properties"""
        log_dict = self.common_add(Properties, new_data, old_data,
                                   [Properties.property.name, Properties.property_type.name],
                                   Properties.property_id)
        return log_dict

    def add_db_ope_types(self, new_data, old_data):
        """更新ope_type"""
        log_dict = self.common_add(OpeTypes, new_data, old_data,
                                   [OpeTypes.ope_type.name, OpeTypes.ope_event.name],
                                   OpeTypes.ope_id)
        return log_dict

    def add_db_events(self, new_data, old_data):
        """更新events"""
        log_dict = self.common_add(Events, new_data, old_data,
                                   [Events.event.name, Events.trigger.name],
                                   Events.event_id)
        return log_dict

    def add_condition(self, proj_id, condition, view_model):
        """
        检测是否存在，不存在就新增
        :param proj_id:
        :param condition:
        :param view_model:
        :return: log_dict, condition_id
        """
        new_condition = {
            Conditions.proj_id.name: proj_id,
            Conditions.condition.name: condition,
            Conditions.view_model.name: view_model
        }
        old_data = self.get_old_data(Conditions, [Conditions.proj_id, Conditions.condition],
                          {Conditions.proj_id.name: proj_id, Conditions.condition.name: condition})
        if old_data:
            old_condition = old_data[0]
            if old_condition.get('view_model') == view_model:
                return None, old_condition.get(Conditions.condition_id.name)
            else:
                new_condition[Conditions.condition_id.name] = old_data[0].get(Conditions.condition_id.name)
        else:
            old_condition = dict()
        log_dict = self.add_db_conditions(new_condition, old_condition)
        condition_id = log_dict.get('key_id')
        return log_dict, condition_id

    def add_display(self, proj_id, display, fun_of_model):
        """
        检测是否存在，不存在就新增
        :param proj_id:
        :param display:
        :param fun_of_model:
        :return: log_dict, display_id
        """
        new_display = {
            Displays.proj_id.name: proj_id,
            Displays.display.name: display,
            Displays.fun_of_model.name: fun_of_model
        }
        old_data = self.get_old_data(Displays, [Displays.proj_id, Displays.display],
                          {Displays.proj_id.name: proj_id, Displays.display.name: display})
        if old_data:
            old_display = old_data[0]
            if old_display.get('fun_of_model') == fun_of_model:
                return None, old_display.get(Displays.display_id.name)
            else:
                new_display[Displays.display_id.name] = old_display.get(Displays.display_id.name)
        else:
            old_display = dict()
        log_dict = self.add_db_displays(new_display, old_display)
        display_id = log_dict.get('key_id')
        return log_dict, display_id

    def add_propertie(self, proj_id, property_type, property):
        """
        检测是否存在，不存在就新增
        :param proj_id:
        :param property_type:
        :param property:
        :return: log_dict, property_id
        """
        new_propertie = {
            Properties.proj_id.name: proj_id,
            Properties.property_type.name: property_type,
            Properties.property.name: property
        }
        old_data = self.get_old_data(Properties, [Properties.proj_id, Properties.property_type],
                          {Properties.proj_id.name: proj_id, Properties.property_type.name: property_type})
        if old_data:
            old_propertie = old_data[0]
            if old_propertie.get("property") == property:
                return None, old_propertie.get(Properties.property_id.name)
            else:
                new_propertie[Properties.property_id.name] = old_propertie.get(Properties.property_id.name)
        else:
            old_propertie = dict()
        log_dict = self.add_db_properties(new_propertie, old_propertie)
        property_id = log_dict.get('key_id')
        return log_dict, property_id

    def add_ope_type(self, proj_id, ope_type, ope_event):
        """
        检测是否存在，不存在就新增
        :param proj_id:
        :param ope_type:
        :param ope_event:
        :return: log_dict, ope_id
        """
        new_ope_type = {
            OpeTypes.proj_id.name: proj_id,
            OpeTypes.ope_type.name: ope_type,
            OpeTypes.ope_event.name: ope_event
        }
        old_data = self.get_old_data(OpeTypes, [OpeTypes.proj_id, OpeTypes.ope_type],
                          {OpeTypes.proj_id.name: proj_id, OpeTypes.ope_type.name: ope_type})
        if old_data:
            old_ope_type = old_data[0]
            if old_ope_type.get('ope_event') == ope_event:
                return None, old_data[0].get(OpeTypes.ope_id.name)
            else:
                new_ope_type[OpeTypes.ope_id.name] = old_data[0].get(OpeTypes.ope_id.name)
        else:
            old_ope_type = dict()
        log_dict = self.add_db_ope_types(new_ope_type, old_ope_type)
        ope_id = log_dict.get('key_id')
        return log_dict, ope_id

    def add_event(self, proj_id, event, trigger):
        """
        检测是否存在，不存在就新增
        :param proj_id:
        :param event:
        :param trigger:
        :return: log_dict, ope_id
        """
        new_event = {
            Events.proj_id.name: proj_id,
            Events.event.name: event,
            Events.trigger.name: trigger
        }
        old_data = self.get_old_data(Events, [Events.proj_id, Events.event],
                          {Events.proj_id.name: proj_id, Events.event.name: event})
        if old_data:
            old_event = old_data[0]
            if old_event.get('trigger') == trigger:
                return None, old_event.get(Events.event_id.name)
            else:
                new_event[Events.event_id.name] = old_event.get(Events.event_id.name)
        else:
            old_event = dict()
        log_dict = self.add_db_events(new_event, old_event)
        event_id = log_dict.get('key_id')
        return log_dict, event_id
