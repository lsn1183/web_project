from sqlalchemy.orm import aliased, joinedload, subqueryload
from sqlalchemy.sql.expression import func
from flask import current_app
from app.db import db
from app.ctrl.ctrl_screen import *
from app.ctrl.chapter_key_col import *
# from sqlalchemy_utils.functions import get_primary_keys


class CtrlChapter(CtrlScreen):
    def __init__(self):
        CtrlScreen.__init__(self)
        self.chapters = [DSChapterBase(), DSChapter1(), DSChapter2(),
                         DSChapter3(), DSChapter4(), DSChapter5(),
                         DSChapter6(), DSChapter7(), DSChapter8()]

    def get_chapter(self, screen_gid, _type):
        if(_type >= 1) and (_type < len(self.chapters)):
            return self.chapters[_type].get_chapter(screen_gid)
        else:
            current_app.logger.error('chapter type error. type[%s] must be between [1, %s]'
                                     % (_type, len(self.chapters)))
            return []

    def update_chapter(self, _type, data_json):
        if (_type >= 1) and (_type < len(self.chapters)):
            return self.chapters[_type].update_chapter(data_json)
        else:
            msg = 'chapter type error. type[%s] must be between [1, %s]' % (_type, len(self.chapters))
            current_app.logger.error(msg)
            return False, msg


class DSChapterBase(CtrlScreen):
    def __init__(self):
        CtrlScreen.__init__(self)
        self.col_list = []
        self.db_table = None
        self.key_id = None

    def get_chapter(self, screen_gid):
        return dict()

    def add_db_chapter(self, new_data, old_data):
        """更新chapter1"""
        log_dict = self.common_add(self.db_table, new_data, old_data, self.col_list, self.key_id)
        return log_dict

    def update_chapter(self, data_dict):
        pass

    def replace_none(self, str1, str2):
        if not str1:
            str1 = '-'
        if not str2:
            str2 = '-'
        return str1, str2

    def get_new_chapter(self, columns_list, chapter_dict, check_chapter):
        if not chapter_dict.get(check_chapter):
            return False
        new_chapter = dict()
        for col in columns_list:
            new_chapter[col.name] = chapter_dict.get(col.name)
        return new_chapter


class DSChapter1(DSChapterBase):
    def __init__(self):
        DSChapterBase.__init__(self)
        self.db_table = Chapter1
        self.key_id = Chapter1.chapter1_id  # list(get_primary_keys(Chapter1).keys())[0]
        self.col_list = list(chapter1_key_column.values()) + [Chapter1.display_condition.name,
                                                              Chapter1.display_action.name,
                                                              Chapter1.display_condition_branch.name,
                                                              Chapter1.display_condition_model_branch.name,
                                                              Chapter1.display_property.name]

    def get_chapter(self, screen_gid):
        """获取chapter1"""
        chapter_list = []
        q = db.session.query(Chapter1).filter(Chapter1.screen_gid == screen_gid)
        q = q.order_by(Chapter1.display_chapter, Chapter1.display_sub_chapter,
                       Chapter1.parts_number.ilike("S").desc(), Chapter1.parts_number.ilike("P").desc(),
                       func.length(Chapter1.parts_number),
                       Chapter1.parts_number, Chapter1.parts_name, Chapter1.display_condition_branch).all()
        for chapter_info in q:
            chapter = chapter_info.to_dict()
            chapter["display_condition_phrase"] = chapter_info.conditions.condition
            chapter["display_condition_code"] = chapter_info.conditions.view_model
            chapter["display_property_type"] = chapter_info.properties.property_type
            chapter["display_property"] = chapter_info.properties.property
            chapter["display_action"] = chapter_info.displays.display
            chapter["display_action_model"] = chapter_info.displays.fun_of_model
            chapter_list.append(chapter)
        return chapter_list

    def update_chapter(self, data_dict):
        """更新chapter1表"""
        update_time = self.get_current_time()
        proj_id = data_dict.get("proj_id")
        screen_gid = data_dict.get("screen_gid")
        if not proj_id or not screen_gid:
            return False, "没有指定项目或操作式样书！"
        commit_user = data_dict.get("commit_user")
        chapter_list = data_dict.get("chapter_list")
        new_chapter_list = []
        try:
            for chapter in chapter_list:
                new_chapter = self.get_new_chapter(Chapter1.__table__.columns, chapter, check_chapter='display_chapter')
                if not new_chapter:
                    db.session.rollback()
                    return False, "数据异常！请传正确的数据！"
                display_condition_phrase, display_condition_code = self.replace_none(chapter.get('display_condition_phrase'),
                                                                                     chapter.get('display_condition_code'))
                log_dict, condition_id = self.add_condition(proj_id, display_condition_phrase, display_condition_code)
                new_chapter[Chapter1.display_condition.name] = condition_id
                display_property_type, display_property = self.replace_none(chapter.get('display_property_type'),
                                                                            chapter.get('display_property'))
                log_dict, property_id = self.add_propertie(proj_id, display_property_type, display_property)
                new_chapter[Chapter1.display_property.name] = property_id
                display_action, display_action_model = self.replace_none(chapter.get('display_action'),
                                                                         chapter.get('display_action_model'))
                log_dict, display_id = self.add_display(proj_id, display_action, display_action_model)
                new_chapter[Chapter1.display_action.name] = display_id
                new_chapter_list.append(new_chapter)
            old_chapter_list = self.get_old_data(Chapter1, Chapter1.screen_gid, screen_gid)
            log_list = self.add_list(Chapter1, new_chapter_list, old_chapter_list,
                                     Chapter1.chapter1_id, self.col_list)
            self.commit_log(log_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return None,  "服务异常！请联系管理员！"


class DSChapter2(DSChapterBase):
    def __init__(self):
        DSChapterBase.__init__(self)
        self.db_table = Chapter2
        self.key_id = Chapter2.chapter2_id
        self.col_list = list(chapter2_key_column.values()) + [Chapter2.active_condition.name,
                                                              Chapter2.active_condition_branch.name,
                                                              Chapter2.active_condition_model_branch.name,
                                                              Chapter2.active_action.name,
                                                              Chapter2.active_property.name]

    def get_chapter(self, screen_gid):
        """获取chapter2"""
        chapter_list = []
        q = db.session.query(Chapter2).filter(Chapter2.screen_gid == screen_gid)
        q = q.order_by(Chapter2.active_chapter, Chapter2.active_sub_chapter, func.length(Chapter2.active_no),
                       Chapter2.active_no, func.length(Chapter2.active_state_no),
                       Chapter2.active_state_no, Chapter2.active_condition_branch).all()
        for chapter_info in q:
            chapter = chapter_info.to_dict()
            chapter["active_condition_phrase"] = chapter_info.conditions.condition
            chapter["active_condition_code"] = chapter_info.conditions.view_model
            chapter["active_property_type"] = chapter_info.properties.property_type
            chapter["active_property"] = chapter_info.properties.property
            chapter["active_action"] = chapter_info.displays.display
            chapter["active_action_model"] = chapter_info.displays.fun_of_model
            chapter_list.append(chapter)
        return chapter_list

    def update_chapter(self, data_dict):
        """更新chapter2表"""
        update_time = self.get_current_time()
        proj_id = data_dict.get("proj_id")
        screen_gid = data_dict.get("screen_gid")
        if not proj_id or not screen_gid:
            return False, "没有指定项目或操作式样书！"
        commit_user = data_dict.get("commit_user")
        chapter_list = data_dict.get("chapter_list")
        new_chapter_list = []
        try:
            for chapter in chapter_list:
                new_chapter = self.get_new_chapter(Chapter2.__table__.columns, chapter, check_chapter="active_chapter")
                if not new_chapter:
                    db.session.rollback()
                    return False, "数据异常！请传正确的数据！"
                active_condition_phrase, active_condition_code = self.replace_none(
                    chapter.get('active_condition_phrase'),
                    chapter.get('active_condition_code'))
                log_dict, condition_id = self.add_condition(proj_id, active_condition_phrase, active_condition_code)
                new_chapter[Chapter2.active_condition.name] = condition_id
                active_property_type, active_property = self.replace_none(chapter.get('active_property_type'),
                                                                          chapter.get('active_property'))
                log_dict, property_id = self.add_propertie(proj_id, active_property_type, active_property)
                new_chapter[Chapter2.active_property.name] = property_id
                active_action, active_action_model = self.replace_none(chapter.get('active_action'),
                                                                       chapter.get('active_action_model'))
                log_dict, display_id = self.add_display(proj_id, active_action, active_action_model)
                new_chapter[Chapter2.active_action.name] = display_id
                new_chapter_list.append(new_chapter)
            old_chapter_list = self.get_old_data(Chapter2, Chapter2.screen_gid, screen_gid)
            log_list = self.add_list(Chapter2, new_chapter_list, old_chapter_list,
                                     Chapter2.chapter2_id, self.col_list)
            self.commit_log(log_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return None, "服务异常！请联系管理员！"


class DSChapter3(DSChapterBase):
    def __init__(self):
        DSChapterBase.__init__(self)
        self.db_table = Chapter3
        self.key_id = Chapter3.chapter3_id
        self.col_list = list(chapter3_key_column.values()) + [Chapter3.action_condition.name,
                                                              Chapter3.action_condition_branch.name,
                                                              Chapter3.action_condition_model_branch.name,
                                                              Chapter3.action_ope.name,
                                                              Chapter3.action_action.name]

    def get_chapter(self, screen_gid):
        """获取chapter3"""
        chapter_list = []
        q = db.session.query(Chapter3).filter(Chapter3.screen_gid == screen_gid)
        q = q.order_by(Chapter3.action_chapter, Chapter3.action_sub_chapter,
                       func.length(Chapter3.action_no), Chapter3.action_no, func.length(Chapter3.action_state_no),
                       Chapter3.action_state_no, Chapter3.action_condition_branch).all()
        for chapter_info in q:
            chapter = chapter_info.to_dict()
            chapter["action_condition_phrase"] = chapter_info.conditions.condition
            chapter["action_condition_code"] = chapter_info.conditions.view_model
            chapter["action_ope_type"] = chapter_info.opetypes.ope_type
            chapter["action_event"] = chapter_info.opetypes.ope_event
            chapter["action_action"] = chapter_info.displays.display
            chapter["action_action_model"] = chapter_info.displays.fun_of_model
            chapter_list.append(chapter)
        return chapter_list

    def update_chapter(self, data_dict):
        """更新chapter3表"""
        update_time = self.get_current_time()
        proj_id = data_dict.get("proj_id")
        screen_gid = data_dict.get("screen_gid")
        if not proj_id or not screen_gid:
            return False, "没有指定项目或操作式样书！"
        commit_user = data_dict.get("commit_user")
        chapter_list = data_dict.get("chapter_list")
        new_chapter_list = []
        try:
            for chapter in chapter_list:
                new_chapter = self.get_new_chapter(Chapter3.__table__.columns, chapter, check_chapter='action_chapter')
                if not new_chapter:
                    db.session.rollback()
                    return False, "数据异常！请传正确的数据！"
                action_condition_phrase, action_condition_code = self.replace_none(
                    chapter.get('action_condition_phrase'),
                    chapter.get('action_condition_code'))
                log_dict, condition_id = self.add_condition(proj_id, action_condition_phrase, action_condition_code)
                new_chapter[Chapter3.action_condition.name] = condition_id
                action_ope_type, action_event = self.replace_none(chapter.get('action_ope_type'),
                                                                  chapter.get('action_event'))
                log_dict, ope_id = self.add_ope_type(proj_id, action_ope_type, action_event)
                new_chapter[Chapter3.action_ope.name] = ope_id
                action_action, action_action_model = self.replace_none(chapter.get('action_action'),
                                                                       chapter.get('action_action_model'))
                log_dict, display_id = self.add_display(proj_id, action_action, action_action_model)
                new_chapter[Chapter3.action_action.name] = display_id
                new_chapter_list.append(new_chapter)
            old_chapter_list = self.get_old_data(Chapter3, Chapter3.screen_gid, screen_gid)
            log_list = self.add_list(Chapter3, new_chapter_list, old_chapter_list,
                                     Chapter3.chapter3_id, self.col_list)
            self.commit_log(log_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return None, "服务异常！请联系管理员！"


class DSChapter4(DSChapterBase):
    def __init__(self):
        DSChapterBase.__init__(self)
        self.db_table = Chapter4
        self.key_id = Chapter4.chapter4_id
        self.col_list = list(chapter4_key_column.values()) + [Chapter4.hk_condition.name,
                                                              Chapter4.hk_condition_branch.name,
                                                              Chapter4.hk_condition_model_branch.name,
                                                              Chapter4.hk_action.name,
                                                              Chapter4.hk_ope.name]

    def get_chapter(self, screen_gid):
        """获取chapter4"""
        # import datetime
        # t1 = datetime.datetime.now()
        # print(datetime.datetime.now())
        chapter_list = []
        q = (db.session.query(Chapter4).filter(Chapter4.screen_gid == screen_gid)
             # .options(subqueryload('displays'),  # 多的时候可以提高性能，少的时候没有效果
             #          subqueryload('conditions'),
             #          subqueryload('opetypes'))
             )
        q = q.order_by(Chapter4.hk_chapter, Chapter4.hk_sub_chapter,
                       Chapter4.hk_dev_name, func.length(Chapter4.hk_no),
                       Chapter4.hk_no, func.length(Chapter4.hk_state_no),
                       Chapter4.hk_state_no, Chapter4.hk_condition_branch
                       ).all()
        for chapter_info in q:
            chapter = chapter_info.to_dict()
            chapter["hk_condition_phrase"] = chapter_info.conditions.condition
            chapter["hk_condition_code"] = chapter_info.conditions.view_model
            chapter["hk_ope_type"] = chapter_info.opetypes.ope_type
            chapter["hk_event"] = chapter_info.opetypes.ope_event
            chapter["hk_action"] = chapter_info.displays.display
            chapter["hk_action_model"] = chapter_info.displays.fun_of_model
            chapter_list.append(chapter)
        # t2 = datetime.datetime.now()
        # print(t2)
        # print(t2 - t1)
        return chapter_list

    def update_chapter(self, data_dict):
        """更新chapter4表"""
        update_time = self.get_current_time()
        proj_id = data_dict.get("proj_id")
        screen_gid = data_dict.get("screen_gid")
        if not proj_id or not screen_gid:
            return False, "没有指定项目或操作式样书！"
        commit_user = data_dict.get("commit_user")
        chapter_list = data_dict.get("chapter_list")
        new_chapter_list = []
        try:
            for chapter in chapter_list:
                new_chapter = self.get_new_chapter(Chapter4.__table__.columns, chapter, check_chapter='hk_chapter')
                if not new_chapter:
                    db.session.rollback()
                    return False, "数据异常！请传正确的数据！"
                hk_condition_phrase, hk_condition_code = self.replace_none( chapter.get('hk_condition_phrase'),
                                                                            chapter.get('hk_condition_code'))
                log_dict, condition_id = self.add_condition(proj_id, hk_condition_phrase, hk_condition_code)
                new_chapter[Chapter4.hk_condition.name] = condition_id
                hk_ope_type, hk_event = self.replace_none(chapter.get('hk_ope_type'), chapter.get('hk_event'))
                log_dict, property_id = self.add_ope_type(proj_id, hk_ope_type, hk_event)
                new_chapter[Chapter4.hk_ope.name] = property_id
                hk_action, hk_action_model = self.replace_none(chapter.get('hk_action'), chapter.get('hk_action_model'))
                log_dict, display_id = self.add_display(proj_id, hk_action, hk_action_model)
                new_chapter[Chapter4.hk_action.name] = display_id
                new_chapter_list.append(new_chapter)
            old_chapter_list = self.get_old_data(Chapter4, Chapter4.screen_gid, screen_gid)
            log_list = self.add_list(Chapter4, new_chapter_list, old_chapter_list,
                                     Chapter4.chapter4_id, self.col_list)
            self.commit_log(log_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return None, "服务异常！请联系管理员！"


class DSChapter5(DSChapterBase):
    def __init__(self):
        DSChapterBase.__init__(self)
        self.db_table = Chapter5
        self.key_id = Chapter5.chapter5_id
        self.col_list = list(chapter5_key_column.values()) + [Chapter5.init_condition.name,
                                                              Chapter5.init_condition_branch.name,
                                                              Chapter5.init_condition_model_branch.name,
                                                              Chapter5.init_action.name]

    def get_chapter(self, screen_gid):
        """获取chapter5"""
        chapter_list = []
        q = db.session.query(Chapter5).filter(Chapter5.screen_gid == screen_gid)
        q = q.order_by(Chapter5.init_chapter, func.length(Chapter5.init_no),
                       Chapter5.init_no, func.length(Chapter5.init_state_no), Chapter5.init_state_no,
                       Chapter5.init_condition_branch).all()
        for chapter_info in q:
            chapter = chapter_info.to_dict()
            chapter["init_condition_phrase"] = chapter_info.conditions.condition
            chapter["init_condition_code"] = chapter_info.conditions.view_model
            chapter["init_action"] = chapter_info.displays.display
            chapter["init_action_model"] = chapter_info.displays.fun_of_model
            chapter_list.append(chapter)
        return chapter_list

    def update_chapter(self, data_dict):
        """更新chapter5表"""
        update_time = self.get_current_time()
        proj_id = data_dict.get("proj_id")
        screen_gid = data_dict.get("screen_gid")
        if not proj_id or not screen_gid:
            return False, "没有指定项目或操作式样书！"
        commit_user = data_dict.get("commit_user")
        chapter_list = data_dict.get("chapter_list")
        new_chapter_list = []
        try:
            for chapter in chapter_list:
                new_chapter = self.get_new_chapter(Chapter5.__table__.columns, chapter, check_chapter='init_chapter')
                if not new_chapter:
                    db.session.rollback()
                    return False, "数据异常！请传正确的数据！"
                init_condition_phrase, init_condition_code = self.replace_none(
                    chapter.get('init_condition_phrase'),
                    chapter.get('init_condition_code'))
                log_dict, condition_id = self.add_condition(proj_id, init_condition_phrase, init_condition_code)
                new_chapter[Chapter5.init_condition.name] = condition_id
                init_action, init_action_model = self.replace_none(chapter.get('init_action'),
                                                                   chapter.get('init_action_model'))
                log_dict, display_id = self.add_display(proj_id, init_action, init_action_model)
                new_chapter[Chapter5.init_action.name] = display_id
                new_chapter_list.append(new_chapter)
            old_chapter_list = self.get_old_data(Chapter5, Chapter5.screen_gid, screen_gid)
            log_list = self.add_list(Chapter5, new_chapter_list, old_chapter_list,
                                     Chapter5.chapter5_id, self.col_list)
            self.commit_log(log_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return None, "服务异常！请联系管理员！"


class DSChapter6(DSChapterBase):
    def __init__(self):
        DSChapterBase.__init__(self)
        self.db_table = Chapter6
        self.key_id = Chapter6.chapter6_id
        self.col_list = list(chapter6_key_column.values()) + [Chapter6.status_change_b_condition.name,
                                                              Chapter6.status_change_b_condition_branch.name,
                                                              Chapter6.status_change_b_condition_model_branch.name,
                                                              Chapter6.status_change_f_condition.name,
                                                              Chapter6.status_change_f_condition_branch.name,
                                                              Chapter6.status_change_f_condition_model_branch.name,
                                                              Chapter6.status_change_i_condition.name,
                                                              Chapter6.status_change_i_condition_branch.name,
                                                              Chapter6.status_change_i_condition_model_branch.name,
                                                              Chapter6.status_change_b_action.name,
                                                              Chapter6.status_change_f_action.name,
                                                              Chapter6.status_change_i_action.name]

    def get_chapter(self, screen_gid):
        """获取chapter6"""
        condition_f = aliased(Conditions)
        condition_b = aliased(Conditions)
        condition_i = aliased(Conditions)
        display_f = aliased(Displays)
        display_b = aliased(Displays)
        display_i = aliased(Displays)
        q = (db.session.query(Chapter6, condition_f.condition.label('status_change_condition_f_phrase'),
                              condition_f.condition.label('status_change_condition_f_code'),
                              condition_b.condition.label('status_change_condition_b_phrase'),
                              condition_b.condition.label('status_change_condition_b_code'),
                              condition_i.condition.label('status_change_condition_i_phrase'),
                              condition_i.condition.label('status_change_condition_i_code'),
                              display_f.display.label('status_change_f_action'),
                              display_f.display.label('status_change_f_action_model'),
                              display_b.display.label('status_change_b_action'),
                              display_b.display.label('status_change_b_action_model'),
                              display_i.display.label('status_change_i_action'),
                              display_i.display.label('status_change_i_action_model')
                              )
             .outerjoin(condition_f, Chapter6.status_change_f_condition == condition_f.condition_id)
             .outerjoin(condition_b, Chapter6.status_change_b_condition == condition_b.condition_id)
             .outerjoin(condition_i, Chapter6.status_change_i_condition == condition_i.condition_id)
             .outerjoin(display_f, Chapter6.status_change_f_action == display_f.display_id)
             .outerjoin(display_b, Chapter6.status_change_b_action == display_b.display_id)
             .outerjoin(display_i, Chapter6.status_change_i_action == display_i.display_id)
             .filter(Chapter1.screen_gid == screen_gid)
             .order_by(Chapter6.status_change_chapter, Chapter6.status_change_sub_chapter,
                       func.length(Chapter6.status_change_no), Chapter6.status_change_no,
                       func.length(Chapter6.status_change_state_no), Chapter6.status_change_state_no,
                       Chapter6.status_change_f_condition_branch).all())
        chapter_list = []
        for row in q:
            chapter = row.Chapter6.to_dict()
            chapter['status_change_condition_f_phrase'] = row.status_change_condition_f_phrase
            chapter['status_change_condition_f_code'] = row.status_change_condition_f_code
            chapter['status_change_condition_b_phrase'] = row.status_change_condition_f_phrase
            chapter['status_change_condition_b_code'] = row.status_change_condition_f_code
            chapter['status_change_condition_i_phrase'] = row.status_change_condition_f_phrase
            chapter['status_change_condition_i_code'] = row.status_change_condition_f_code
            chapter['status_change_f_action'] = row.status_change_f_action
            chapter['status_change_f_action_model'] = row.status_change_f_action_model
            chapter['status_change_b_action'] = row.status_change_b_action
            chapter['status_change_b_action_model'] = row.status_change_b_action_model
            chapter['status_change_i_action'] = row.status_change_i_action
            chapter['status_change_i_action_model'] = row.status_change_i_action_model
            chapter_list.append(chapter)
        return chapter_list

    def update_chapter(self, data_dict):
        """更新chapter6表"""
        update_time = self.get_current_time()
        proj_id = data_dict.get("proj_id")
        screen_gid = data_dict.get("screen_gid")
        if not proj_id or not screen_gid:
            return False, "没有指定项目或操作式样书！"
        commit_user = data_dict.get("commit_user")
        chapter_list = data_dict.get("chapter_list")
        new_chapter_list = []
        try:
            for chapter in chapter_list:
                new_chapter = self.get_new_chapter(Chapter6.__table__.columns, chapter, check_chapter='status_change_chapter')
                if not new_chapter:
                    db.session.rollback()
                    return False, "数据异常！请传正确的数据！"
                status_change_condition_f_phrase, status_change_condition_f_code = self.replace_none(
                    chapter.get('status_change_condition_f_phrase'),
                    chapter.get('status_change_condition_f_code'))
                log_dict, condition_f_id = self.add_condition(proj_id, status_change_condition_f_phrase,
                                                              status_change_condition_f_code)
                new_chapter[Chapter6.status_change_f_condition.name] = condition_f_id
                status_change_condition_b_phrase, status_change_condition_b_code = self.replace_none(
                    chapter.get('status_change_condition_b_phrase'),
                    chapter.get('status_change_condition_b_code'))
                log_dict, condition_b_id = self.add_condition(proj_id, status_change_condition_b_phrase,
                                                              status_change_condition_b_code)
                new_chapter[Chapter6.status_change_b_condition.name] = condition_b_id
                status_change_condition_i_phrase, status_change_condition_i_code = self.replace_none(
                    chapter.get('status_change_condition_i_phrase'),
                    chapter.get('status_change_condition_i_code'))
                log_dict, condition_i_id = self.add_condition(proj_id, status_change_condition_i_phrase,
                                                              status_change_condition_i_code)
                new_chapter[Chapter6.status_change_i_condition.name] = condition_i_id
                status_change_f_action, status_change_f_action_model = self.replace_none(
                    chapter.get('status_change_f_action'),
                    chapter.get('status_change_f_action_model'))
                log_dict, display_f_id = self.add_display(proj_id, status_change_f_action,
                                                          status_change_f_action_model)
                new_chapter[Chapter6.status_change_f_action.name] = display_f_id
                status_change_b_action, status_change_b_action_model = self.replace_none(
                    chapter.get('status_change_b_action'),
                    chapter.get('status_change_b_action_model'))
                log_dict, display_b_id = self.add_display(proj_id, status_change_b_action,
                                                          status_change_b_action_model)
                new_chapter[Chapter6.status_change_f_action.name] = display_b_id
                status_change_i_action, status_change_i_action_model = self.replace_none(
                    chapter.get('status_change_i_action'),
                    chapter.get('status_change_i_action_model'))
                log_dict, display_i_id = self.add_display(proj_id, status_change_i_action,
                                                          status_change_i_action_model)
                new_chapter[Chapter6.status_change_i_action.name] = display_i_id
                new_chapter_list.append(new_chapter)
            old_chapter_list = self.get_old_data(Chapter6, Chapter6.screen_gid, screen_gid)
            log_list = self.add_list(Chapter6, new_chapter_list, old_chapter_list,
                                     Chapter6.chapter1_id, self.col_list)
            self.commit_log(log_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return None, "服务异常！请联系管理员！"


class DSChapter7(DSChapterBase):
    def __init__(self):
        DSChapterBase.__init__(self)
        self.db_table = Chapter7
        self.key_id = Chapter7.chapter7_id
        self.col_list = list(chapter7_key_column.values()) + [Chapter7.transition_b_condition.name,
                                                              Chapter7.transition_b_condition_branch.name,
                                                              Chapter7.transition_b_condition_model_branch.name,
                                                              Chapter7.transition_f_condition.name,
                                                              Chapter7.transition_f_condition_branch.name,
                                                              Chapter7.transition_f_condition_model_branch.name,
                                                              Chapter7.transition_i_condition.name,
                                                              Chapter7.transition_i_condition_branch.name,
                                                              Chapter7.transition_i_condition_model_branch.name,
                                                              Chapter7.transition_b_action.name,
                                                              Chapter7.transition_f_action.name,
                                                              Chapter7.transition_i_action.name]

    def get_chapter(self, screen_gid):
        """获取chapter7"""
        condition_f = aliased(Conditions)
        condition_b = aliased(Conditions)
        condition_i = aliased(Conditions)
        display_f = aliased(Displays)
        display_b = aliased(Displays)
        display_i = aliased(Displays)
        q = (db.session.query(Chapter7, condition_f.condition.label('transition_condition_f_phrase'),
                              condition_f.condition.label('transition_condition_f_code'),
                              condition_b.condition.label('transition_condition_b_phrase'),
                              condition_b.condition.label('transition_condition_b_code'),
                              condition_i.condition.label('transition_condition_i_phrase'),
                              condition_i.condition.label('transition_condition_i_code'),
                              display_f.display.label('transition_f_action'),
                              display_f.display.label('transition_f_action_model'),
                              display_b.display.label('transition_b_action'),
                              display_b.display.label('transition_b_action_model'),
                              display_i.display.label('transition_i_action'),
                              display_i.display.label('transition_i_action_model')
                              )
             .outerjoin(condition_f, Chapter7.transition_f_condition == condition_f.condition_id)
             .outerjoin(condition_b, Chapter7.transition_b_condition == condition_b.condition_id)
             .outerjoin(condition_i, Chapter7.transition_i_condition == condition_i.condition_id)
             .outerjoin(display_f, Chapter7.transition_f_action == display_f.display_id)
             .outerjoin(display_b, Chapter7.transition_b_action == display_b.display_id)
             .outerjoin(display_i, Chapter7.transition_i_action == display_i.display_id)
             .filter(Chapter1.screen_gid == screen_gid)
             .order_by(Chapter7.transition_chapter, Chapter7.transition_sub_chapter,
                       func.length(Chapter7.transition_no), Chapter7.transition_no,
                       func.length(Chapter7.transition_state_no), Chapter7.transition_state_no,
                       Chapter7.transition_f_condition_branch)
             )
        chapter_list = []
        for row in q:
            chapter = row.Chapter7.to_dict()
            chapter['transition_condition_f_phrase'] = row.transition_condition_f_phrase
            chapter['transition_condition_f_code'] = row.transition_condition_f_code
            chapter['transition_condition_b_phrase'] = row.transition_condition_f_phrase
            chapter['transition_condition_b_code'] = row.transition_condition_f_code
            chapter['transition_condition_i_phrase'] = row.transition_condition_f_phrase
            chapter['transition_condition_i_code'] = row.transition_condition_f_code
            chapter['transition_f_action'] = row.transition_f_action
            chapter['transition_f_action_model'] = row.transition_f_action_model
            chapter['transition_b_action'] = row.transition_b_action
            chapter['transition_b_action_model'] = row.transition_b_action_model
            chapter['transition_i_action'] = row.transition_i_action
            chapter['transition_i_action_model'] = row.transition_i_action_model
            chapter_list.append(chapter)
        return chapter_list

    def update_chapter(self, data_dict):
        """更新chapter7表"""
        update_time = self.get_current_time()
        proj_id = data_dict.get("proj_id")
        screen_gid = data_dict.get("screen_gid")
        if not proj_id or not screen_gid:
            return False, "没有指定项目或操作式样书！"
        commit_user = data_dict.get("commit_user")
        chapter_list = data_dict.get("chapter_list")
        new_chapter_list = []
        try:
            for chapter in chapter_list:
                new_chapter = self.get_new_chapter(Chapter7.__table__.columns, chapter, check_chapter='transition_chapter')
                if not new_chapter:
                    db.session.rollback()
                    return False, "数据异常！请传正确的数据！"
                transition_condition_f_phrase, transition_condition_f_code = self.replace_none(
                    chapter.get('transition_condition_f_phrase'),
                    chapter.get('transition_condition_f_code'))
                log_dict, condition_f_id = self.add_condition(proj_id, transition_condition_f_phrase,
                                                              transition_condition_f_code)
                new_chapter[Chapter7.transition_f_condition.name] = condition_f_id
                transition_condition_b_phrase, transition_condition_b_code = self.replace_none(
                    chapter.get('transition_condition_b_phrase'),
                    chapter.get('transition_condition_b_code'))
                log_dict, condition_b_id = self.add_condition(proj_id, transition_condition_b_phrase,
                                                              transition_condition_b_code)
                new_chapter[Chapter7.transition_b_condition.name] = condition_b_id
                transition_condition_i_phrase, transition_condition_i_code = self.replace_none(
                    chapter.get('transition_condition_i_phrase'),
                    chapter.get('transition_condition_i_code'))
                log_dict, condition_i_id = self.add_condition(proj_id, transition_condition_i_phrase,
                                                              transition_condition_i_code)
                new_chapter[Chapter7.transition_i_condition.name] = condition_i_id
                transition_f_action, transition_f_action_model = self.replace_none(
                    chapter.get('transition_f_action'),
                    chapter.get('transition_f_action_model'))
                log_dict, display_f_id = self.add_display(proj_id, transition_f_action,
                                                          transition_f_action_model)
                new_chapter[Chapter7.transition_f_action.name] = display_f_id
                transition_b_action, transition_b_action_model = self.replace_none(
                    chapter.get('transition_b_action'),
                    chapter.get('transition_b_action_model'))
                log_dict, display_b_id = self.add_display(proj_id, transition_b_action,
                                                          transition_b_action_model)
                new_chapter[Chapter7.transition_f_action.name] = display_b_id
                transition_i_action, transition_i_action_model = self.replace_none(
                    chapter.get('transition_i_action'),
                    chapter.get('transition_i_action_model'))
                log_dict, display_i_id = self.add_display(proj_id, transition_i_action,
                                                          transition_i_action_model)
                new_chapter[Chapter7.transition_i_action.name] = display_i_id
                new_chapter_list.append(new_chapter)
            old_chapter_list = self.get_old_data(Chapter7, Chapter7.screen_gid, screen_gid)
            log_list = self.add_list(Chapter7, new_chapter_list, old_chapter_list,
                                     Chapter7.chapter1_id, self.col_list)
            self.commit_log(log_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return None, "服务异常！请联系管理员！"


class DSChapter8(DSChapterBase):
    def __init__(self):
        DSChapterBase.__init__(self)
        self.db_table = Chapter8
        self.key_id = Chapter8.chapter8_id
        self.col_list = list(chapter8_key_column.values()) + [Chapter8.trig_condition.name,
                                                              Chapter8.trig_condition_branch.name,
                                                              Chapter8.trig_condition_model_branch.name,
                                                              Chapter8.trig_trig.name,
                                                              Chapter8.trig_action.name]

    def get_chapter(self, screen_gid):
        """获取chapter8"""
        chapter_list = []
        q = db.session.query(Chapter8).filter(Chapter8.screen_gid == screen_gid)
        q = q.order_by(Chapter8.trig_chapter, Chapter8.trig_sub_chapter,
                       func.length(Chapter8.trig_no), Chapter8.trig_no,
                       func.length(Chapter8.trig_state_no), Chapter8.trig_state_no,
                       Chapter8.trig_condition_branch).all()
        for chapter_info in q:
            chapter = chapter_info.to_dict()
            chapter["trig_condition_phrase"] = chapter_info.conditions.condition
            chapter["trig_condition_code"] = chapter_info.conditions.view_model
            chapter["trig_name"] = chapter_info.events.event
            chapter["trig_trig"] = chapter_info.events.trigger
            chapter["trig_action"] = chapter_info.displays.display
            chapter["trig_action_model"] = chapter_info.displays.fun_of_model
            chapter_list.append(chapter)
        return chapter_list

    def update_chapter(self, data_dict):
        """更新chapter8表"""
        update_time = self.get_current_time()
        proj_id = data_dict.get("proj_id")
        screen_gid = data_dict.get("screen_gid")
        if not proj_id or not screen_gid:
            return False, "没有指定项目或操作式样书！"
        commit_user = data_dict.get("commit_user")
        chapter_list = data_dict.get("chapter_list")
        new_chapter_list = []
        try:
            for chapter in chapter_list:
                new_chapter = self.get_new_chapter(Chapter8.__table__.columns, chapter, check_chapter='trig_chapter')
                if not new_chapter:
                    db.session.rollback()
                    return False, "数据异常！请传正确的数据！"
                trig_condition_phrase, trig_condition_code = self.replace_none( chapter.get('trig_condition_phrase'),
                                                                                chapter.get('trig_condition_code'))
                log_dict, condition_id = self.add_condition(proj_id, trig_condition_phrase, trig_condition_code)
                new_chapter[Chapter8.trig_condition.name] = condition_id
                trig_name, trig_trig = self.replace_none(chapter.get('trig_name'), chapter.get('trig_trig'))
                log_dict, event_id = self.add_event(proj_id, trig_name, trig_trig)
                new_chapter[Chapter8.trig_trig.name] = event_id
                trig_action, trig_action_model = self.replace_none(chapter.get('trig_action'),
                                                                   chapter.get('trig_action_model'))
                log_dict, display_id = self.add_display(proj_id, trig_action, trig_action_model)
                new_chapter[Chapter8.trig_action.name] = display_id
                new_chapter_list.append(new_chapter)
            old_chapter_list = self.get_old_data(Chapter8, Chapter8.screen_gid, screen_gid)
            log_list = self.add_list(Chapter8, new_chapter_list, old_chapter_list,
                                     Chapter8.chapter1_id, self.col_list)
            self.commit_log(log_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return None, "服务异常！请联系管理员！"
