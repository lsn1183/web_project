import os
from flask import current_app
from app.db.models import *
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_screen import CtrlScreen
from app.ctrl.ctrl_chapter import *
from app.ctrl.chapter_key_col import *
import pandas as pd


class CtrlExport(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def get_chapter1_col(self):
        chapter1 = {}
        for chapter in list(chapter1_key_column.items()):
            chapter1[chapter[-1]] = chapter[0]
        return chapter1

    def get_chapter2_col(self):
        chapter2 = {}
        for chapter in list(chapter2_key_column.items()):
            chapter2[chapter[-1]] = chapter[0]
        return chapter2

    def get_chapter3_col(self):
        chapter3 = {}
        for chapter in list(chapter3_key_column.items()):
            chapter3[chapter[-1]] = chapter[0]
        return chapter3

    def get_chapter4_col(self):
        chapter4 = {}
        for chapter in list(chapter4_key_column.items()):
            chapter4[chapter[-1]] = chapter[0]
        return chapter4

    def get_chapter5_col(self):
        chapter5 = {}
        for chapter in list(chapter5_key_column.items()):
            chapter5[chapter[-1]] = chapter[0]
        return chapter5

    def get_chapter6_col(self):
        chapter6 = {}
        for chapter in list(chapter6_key_column.items()):
            chapter6[chapter[-1]] = chapter[0]
        return chapter6

    def get_chapter7_col(self):
        chapter7 = {}
        for chapter in list(chapter7_key_column.items()):
            chapter7[chapter[-1]] = chapter[0]
        return chapter7

    def get_chapter8_col(self):
        chapter8 = {}
        for chapter in list(chapter8_key_column.items()):
            chapter8[chapter[-1]] = chapter[0]
        return chapter8

    def get_chapter1_info_to_df(self, screen_gid):
        chapter1_key = DSChapter1().col_list
        chapter1_column = {"display":list,"fun_of_model":list,"condition":list,
                           "view_model":list,"property_type":list,"property":list}
        q = (db.session.query(Chapter1,Displays.display,Displays.fun_of_model,Conditions.condition,Conditions.view_model,
                              Properties.property_type,Properties.property)
             .join(Displays, Displays.display_id == Chapter1.display_action)
             .join(Conditions, Conditions.condition_id == Chapter1.display_condition)
             .join(Properties, Properties.property_id == Chapter1.display_property)
             .filter(Chapter1.screen_gid ==screen_gid)
             .order_by(Chapter1.display_condition_branch))
        for info in chapter1_key:
            if info != "display_uuid":
                chapter1_column[info] = list
        sqlmd = q.statement
        df = pd.read_sql(sqlmd, db.session.bind)
        group_by_df = df.groupby("display_uuid", as_index=False).agg(chapter1_column)
        # for i, row in group_by_df.iterrows():
        columns = self.get_chapter1_col()
        group_by_df.rename(columns=columns, inplace=True)
        # TODO 将df中每行除chapter1_column中字段外其他字段都取第一个出来
        # TODO 将df中chapter1_column中字段按顺序一一对应
        return

    def get_chapter2_info_to_df(self, screen_gid):
        chapter2_key = DSChapter2().col_list
        chapter2_column = {"display":list,"fun_of_model":list,"condition":list,
                           "view_model":list,"property_type":list,"property":list}
        q = (db.session.query(Chapter2,Displays.display,Displays.fun_of_model,Conditions.condition,Conditions.view_model,
                              Properties.property_type,Properties.property)
             .join(Displays, Displays.display_id == Chapter2.active_action)
             .join(Conditions, Conditions.condition_id == Chapter2.active_condition)
             .join(Properties, Properties.property_id == Chapter2.active_property)
             .filter(Chapter2.screen_gid ==screen_gid)
             .order_by(Chapter2.display_condition_branch))
        for info in chapter2_key:
            if info != "active_uuid":
                chapter2_column[info] = list
        sqlmd = q.statement
        df = pd.read_sql(sqlmd, db.session.bind)
        group_by_df = df.groupby("active_uuid", as_index=False).agg(chapter2_column)
        # for i, row in group_by_df.iterrows():
        columns = self.get_chapter2_col()
        group_by_df.rename(columns=columns, inplace=True)
        # TODO 将df中每行除chapter1_column中字段外其他字段都取第一个出来
        # TODO 将df中chapter1_column中字段按顺序一一对应
        return

    def get_chapter3_info_to_df(self, screen_gid):
        chapter3_key = DSChapter3().col_list
        chapter3_column = {"display":list,"fun_of_model":list,"condition":list,
                           "view_model":list,"ope_type":list,"ope_event":list}
        q = (db.session.query(Chapter3,Displays.display,Displays.fun_of_model,Conditions.condition,Conditions.view_model,
                              OpeTypes.ope_type,OpeTypes.ope_event)
             .join(Displays, Displays.display_id == Chapter3.action_action)
             .join(Conditions, Conditions.condition_id == Chapter3.action_condition)
             .join(OpeTypes, OpeTypes.ope_id == Chapter3.action_ope)
             .filter(Chapter3.screen_gid ==screen_gid)
             .order_by(Chapter3.display_condition_branch))
        for info in chapter3_key:
            if info != "action_uuid":
                chapter3_column[info] = list
        sqlmd = q.statement
        df = pd.read_sql(sqlmd, db.session.bind)
        group_by_df = df.groupby("action_uuid", as_index=False).agg(chapter3_column)
        # for i, row in group_by_df.iterrows():
        columns = self.get_chapter3_col()
        group_by_df.rename(columns=columns, inplace=True)
        # TODO 将df中每行除chapter1_column中字段外其他字段都取第一个出来
        # TODO 将df中chapter1_column中字段按顺序一一对应
        return

    def get_chapter4_info_to_df(self, screen_gid):
        chapter4_key = DSChapter4().col_list
        chapter4_column = {"display":list,"fun_of_model":list,"condition":list,
                           "view_model":list,"ope_type":list,"ope_event":list}
        q = (db.session.query(Chapter4,Displays.display,Displays.fun_of_model,Conditions.condition,Conditions.view_model,
                              OpeTypes.ope_type, OpeTypes.ope_event)
             .join(Displays, Displays.display_id == Chapter4.hk_action)
             .join(Conditions, Conditions.condition_id == Chapter4.hk_condition)
             .join(OpeTypes, OpeTypes.ope_id == Chapter4.hk_ope)
             .filter(Chapter4.screen_gid ==screen_gid)
             .order_by(Chapter4.display_condition_branch))
        for info in chapter4_key:
            if info != "hk_uuid":
                chapter4_column[info] = list
        sqlmd = q.statement
        df = pd.read_sql(sqlmd, db.session.bind)
        group_by_df = df.groupby("hk_uuid", as_index=False).agg(chapter4_column)
        # for i, row in group_by_df.iterrows():
        columns = self.get_chapter4_col()
        group_by_df.rename(columns=columns, inplace=True)
        # TODO 将df中每行除chapter1_column中字段外其他字段都取第一个出来
        # TODO 将df中chapter1_column中字段按顺序一一对应
        return

    def get_chapter5_info_to_df(self, screen_gid):
        chapter5_key = DSChapter5().col_list
        chapter5_column = {"display":list,"fun_of_model":list,"condition":list,
                           "view_model":list}
        q = (db.session.query(Chapter5,Displays.display,Displays.fun_of_model,
                              Conditions.condition,Conditions.view_model)
             .join(Displays, Displays.display_id == Chapter5.init_action)
             .join(Conditions, Conditions.condition_id == Chapter5.init_condition)
             .filter(Chapter5.screen_gid ==screen_gid)
             .order_by(Chapter5.display_condition_branch))
        for info in chapter5_key:
            if info != "init_uuid":
                chapter5_column[info] = list
        sqlmd = q.statement
        df = pd.read_sql(sqlmd, db.session.bind)
        group_by_df = df.groupby("init_uuid", as_index=False).agg(chapter5_column)
        # for i, row in group_by_df.iterrows():
        columns = self.get_chapter5_col()
        group_by_df.rename(columns=columns, inplace=True)
        # TODO 将df中每行除chapter1_column中字段外其他字段都取第一个出来
        # TODO 将df中chapter1_column中字段按顺序一一对应
        return

    def get_chapter6_info_to_df(self, screen_gid):
        chapter6_key = DSChapter6().col_list
        chapter6_column = {"status_change_condition_f_phrase":list,"status_change_condition_f_code":list,
                           "status_change_condition_b_phrase":list,"status_change_condition_b_code":list,
                           "status_change_condition_i_phrase":list,"status_change_condition_i_code":list,
                           "status_change_f_action":list,"status_change_f_action_model":list,
                           "status_change_b_action":list,"status_change_b_action_model":list,
                           "status_change_i_action":list,"status_change_i_action_model":list}
        condition_f = aliased(Conditions)
        condition_b = aliased(Conditions)
        condition_i = aliased(Conditions)
        display_f = aliased(Displays)
        display_b = aliased(Displays)
        display_i = aliased(Displays)
        q = (db.session.query(Chapter6,condition_f.condition.label('status_change_condition_f_phrase'),
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
                              display_i.display.label('status_change_i_action_model'))
             .outerjoin(condition_f, Chapter6.status_change_f_condition == condition_f.condition_id)
             .outerjoin(condition_b, Chapter6.status_change_b_condition == condition_b.condition_id)
             .outerjoin(condition_i, Chapter6.status_change_i_condition == condition_i.condition_id)
             .outerjoin(display_f, Chapter6.status_change_f_action == display_f.display_id)
             .outerjoin(display_b, Chapter6.status_change_b_action == display_b.display_id)
             .outerjoin(display_i, Chapter6.status_change_i_action == display_i.display_id)
             .filter(Chapter6.screen_gid ==screen_gid)
             .order_by(Chapter6.display_condition_branch))
        for info in chapter6_key:
            if info != "status_change_uuid":
                chapter6_column[info] = list
        sqlmd = q.statement
        df = pd.read_sql(sqlmd, db.session.bind)
        group_by_df = df.groupby("status_change_uuid", as_index=False).agg(chapter6_column)
        # for i, row in group_by_df.iterrows():
        columns = self.get_chapter6_col()
        group_by_df.rename(columns=columns, inplace=True)
        # TODO 将df中每行除chapter1_column中字段外其他字段都取第一个出来
        # TODO 将df中chapter1_column中字段按顺序一一对应
        return

    def get_chapter7_info_to_df(self, screen_gid):
        chapter7_key = DSChapter7().col_list
        chapter7_column = {"transition_condition_f_phrase":list,"transition_condition_f_code":list,
                           "transition_condition_b_phrase":list,"transition_condition_b_code":list,
                           "transition_condition_i_phrase":list,"transition_condition_i_code":list,
                           "transition_f_action":list,"transition_f_action_model":list,
                           "transition_b_action":list,"transition_b_action_model":list,
                           "transition_i_action":list,"transition_i_action_model":list}
        condition_f = aliased(Conditions)
        condition_b = aliased(Conditions)
        condition_i = aliased(Conditions)
        display_f = aliased(Displays)
        display_b = aliased(Displays)
        display_i = aliased(Displays)
        q = (db.session.query(Chapter7,condition_f.condition.label('transition_condition_f_phrase'),
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
                              display_i.display.label('transition_i_action_model'))
             .outerjoin(condition_f, Chapter7.transition_f_condition == condition_f.condition_id)
             .outerjoin(condition_b, Chapter7.transition_b_condition == condition_b.condition_id)
             .outerjoin(condition_i, Chapter7.transition_i_condition == condition_i.condition_id)
             .outerjoin(display_f, Chapter7.transition_f_action == display_f.display_id)
             .outerjoin(display_b, Chapter7.transition_b_action == display_b.display_id)
             .outerjoin(display_i, Chapter7.transition_i_action == display_i.display_id)
             .filter(Chapter7.screen_gid ==screen_gid)
             .order_by(Chapter7.display_condition_branch))
        for info in chapter7_key:
            if info != "transition_uuid":
                chapter7_column[info] = list
        sqlmd = q.statement
        df = pd.read_sql(sqlmd, db.session.bind)
        group_by_df = df.groupby("transition_uuid", as_index=False).agg(chapter7_column)
        # for i, row in group_by_df.iterrows():
        columns = self.get_chapter7_col()
        group_by_df.rename(columns=columns, inplace=True)
        # TODO 将df中每行除chapter1_column中字段外其他字段都取第一个出来
        # TODO 将df中chapter1_column中字段按顺序一一对应
        return

    def get_chapter8_info_to_df(self, screen_gid):
        chapter8_key = DSChapter8().col_list
        chapter8_column = {"display":list,"fun_of_model":list,"condition":list,
                           "view_model":list,"event":list,"trigger":list}
        q = (db.session.query(Chapter8,Displays.display,Displays.fun_of_model,Conditions.condition,Conditions.view_model,
                              Events.event,Events.trigger)
             .join(Displays, Displays.display_id == Chapter8.trig_action)
             .join(Conditions, Conditions.condition_id == Chapter8.trig_condition)
             .join(Events, Events.event_id == Chapter8.trig_trig)
             .filter(Chapter8.screen_gid ==screen_gid)
             .order_by(Chapter8.display_condition_branch))
        for info in chapter8_key:
            if info != "trig_uuid":
                chapter8_column[info] = list
        sqlmd = q.statement
        df = pd.read_sql(sqlmd, db.session.bind)
        group_by_df = df.groupby("trig_uuid", as_index=False).agg(chapter8_column)
        # for i, row in group_by_df.iterrows():
        columns = self.get_chapter8_col()
        group_by_df.rename(columns=columns, inplace=True)
        # TODO 将df中每行除chapter1_column中字段外其他字段都取第一个出来
        # TODO 将df中chapter1_column中字段按顺序一一对应
        return



