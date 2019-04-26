import os
from flask import current_app
from app.db.models import *
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_screen import CtrlScreen
from app.ctrl.ctrl_chapter import CtrlChapter


class CtrlOpe(CtrlBase):

    def __init__(self):
        CtrlBase.__init__(self)
        self.chapter_list = CtrlChapter().chapters[1:] # DSChapter1-DSChapter8的对象
        # self.chapter_list = [{"Chapter": Chapter1, "id": "chapter1_id"},{"Chapter": Chapter2, "id": "chapter2_id"},
        #                      {"Chapter": Chapter3, "id": "chapter3_id"},{"Chapter": Chapter4, "id": "chapter4_id"},
        #                      {"Chapter": Chapter5, "id": "chapter5_id"},{"Chapter": Chapter6, "id": "chapter6_id"},
        #                      {"Chapter": Chapter7, "id": "chapter7_id"},{"Chapter": Chapter8, "id": "chapter8_id"}]

    def get_ope_status(self, screen_gid):
        q = (db.session.query(Screen).filter(Screen.screen_gid == screen_gid).first())
        if q:
            ope = dict()
            ope["locked"] = q.locked
            return True, ope
        else:
            return False, "未找到此Ope"

    def get_ope_info(self, screen_gid):
        q = (db.session.query(Screen).filter(Screen.screen_gid == screen_gid).first())
        if q:
            ope = dict()
            ope["screen_gid"] = q.screen_gid
            ope["proj_id"] = q.proj_id
            ope["screen_id"] = q.screen_id
            ope["screen_name"] = q.screen_name
            ope["outline"] = q.outline
            ope["image_dir"] = q.image_dir
            ope["update_user"] = q.update_user
            ope["locked"] = q.locked
            ope["create_time"] = self.time_to_str(q.create_time)
            ope["update_time"] = self.time_to_str(q.update_time)
            return ope
        else:
            return "未找到此Ope"

    def get_ope_list(self, proj_id):
        q = (db.session.query(Screen).filter(Screen.proj_id == proj_id).all())
        ope_list = []
        for i_ope in q:
            ope = dict()
            ope["screen_gid"] = i_ope.screen_gid
            ope["proj_id"] = i_ope.proj_id
            ope["screen_id"] = i_ope.screen_id
            ope["screen_name"] = i_ope.screen_name
            ope["outline"] = i_ope.outline
            ope["image_dir"] = i_ope.image_dir
            ope["update_user"] = i_ope.update_user
            ope["locked"] = i_ope.locked
            ope["create_time"] = self.time_to_str(i_ope.create_time)
            ope["update_time"] = self.time_to_str(i_ope.update_time)
            ope_list.append(ope)
        return True,ope_list

    def lock_ope(self, data):
        screen = (db.session.query(Screen).filter(Screen.screen_gid == data.get("screen_gid")).first())
        if screen:
            if not screen.locked:
                old_data = {"locked": screen.locked, "update_time": screen.update_time,
                            "update_user": screen.update_user}
                new_data = {"locked": True, "update_time": self.get_current_time(),
                            "update_user": data.get("update_user")}
                log_dict = self.common_add(Screen, new_data, old_data, [Screen.locked.name,
                                                                        Screen.update_time.name,
                                                                        Screen.update_user.name
                                                                        ], Screen.screen_gid)
                self.commit_log([log_dict], data.get("user_id"), self.get_current_time())
                return True, "此Ope已上锁"
            else:
                return False, "此Ope已上锁"
        else:
            return False,"未找到此Ope"


    def unlock_ope(self, data):
        screen = (db.session.query(Screen).filter(Screen.screen_gid == data.get("screen_gid")).first())
        if screen:
            if screen.locked:
                if screen.update_user == data.get("update_user"):
                    old_data = {"locked": screen.locked, "update_time": screen.update_time,
                                "update_user": screen.update_user}
                    new_data = {"locked": False, "update_time": self.get_current_time(),
                                "update_user": data.get("update_user")}
                    log_dict = self.common_add(Screen, new_data, old_data, [Screen.locked.name,
                                                                            Screen.update_time.name,
                                                                            Screen.update_user.name
                                                                            ], Screen.screen_gid)
                    self.commit_log([log_dict], data.get("user_id"), self.get_current_time())
                    return True, "此Ope已解锁"
                else:
                    return False, "不是当前更新者无法解锁"
            else:
                return True, "此Ope已解锁"
        else:
            return False, "未找到此Ope"

    def delete_ope_by_id(self, user_id, screen_gid):
        try:
            screen = (db.session.query(Screen).filter(Screen.screen_gid == screen_gid).first())
            if screen:
                log = []
                for chapter in self.chapter_list:
                    old_data = self.get_old_data(chapter.db_table, screen.screen_gid, screen_gid)
                    log += self.add_list(chapter.db_table, [], old_data, chapter.key_id, chapter.col_list)
                log_dict = CtrlScreen().add_db_screen(dict(), screen.to_dict())
                log.append(log_dict)
                self.commit_log(log, user_id, self.get_current_time())
                return True, ""
            else:
                return False, "no screen screen_gid:%s"%screen_gid
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_displays_by_proj_id(self, proj_id):
        q = (db.session.query(Displays).filter(Displays.proj_id == proj_id).all())
        display_list = []
        for dis in q:
            display = dis.to_dict()
            display_list.append(display)
        return display_list

    def get_conditions_by_proj_id(self, proj_id):
        q = (db.session.query(Conditions).filter(Conditions.proj_id == proj_id).all())
        display_list = []
        for dis in q:
            display = dis.to_dict()
            display_list.append(display)
        return display_list

    def get_properties_by_proj_id(self, proj_id):
        q = (db.session.query(Properties).filter(Properties.proj_id == proj_id).all())
        display_list = []
        for dis in q:
            display = dis.to_dict()
            display_list.append(display)
        return display_list

    def get_opetypes_by_proj_id(self, proj_id):
        q = (db.session.query(OpeTypes).filter(OpeTypes.proj_id == proj_id).all())
        display_list = []
        for dis in q:
            display = dis.to_dict()
            display_list.append(display)
        return display_list

    def get_events_by_proj_id(self, proj_id):
        q = (db.session.query(Events).filter(Events.proj_id == proj_id).all())
        display_list = []
        for dis in q:
            display = dis.to_dict()
            display_list.append(display)
        return display_list