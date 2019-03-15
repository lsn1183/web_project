# -*- coding: UTF-8 -*-
"""
Created on 2017-8-16

@author: hcz
"""
import os
from spec import SpecBase
from spec import SpecImage
from Source.xls2db.common import log
from spec import SPEC_FILE_NAME
OPE_SCREEN_LIST = 'screen_list'
OPE_SCREEN_NO = 'screen_no'
OPE_SCREENT_NAME = 'screen_name'
OPE_CONTENT_LIST = 'content_list'
OPE_TITLE_INFO = 'title_info'
OPE_ACTION_INFO = 'action_info'
OPE_VIEW_INFO = 'viewimg_info'
OPE_REF_INFO = 'reference'


class OpeSpec(SpecBase):
    def __init__(self):
        SpecBase.__init__(self)
        self._attr_list = [SPEC_FILE_NAME]
        self._log = log.common_log.instance().logger('OpeSpec')

    def parser(self, d):
        """SPEC"""
        SpecBase.parser(self, d)
        # ## SCREEN
        screen_info_list = d.get(OPE_SCREEN_LIST)
        if not screen_info_list:
            return
        for screen_info in screen_info_list:
            obj_screen = OpeScreen()
            obj_screen.parser(screen_info)
            self._children.append(obj_screen)

    def store(self):
        self._pg.connect2()
        self._insert_spec(self._attr_dict.get(SPEC_FILE_NAME))
        self._set_children_pid()
        self._store_children()
        self._store_rel()

    def _insert_spec(self, file_name):
        sqlcmd = """
        INSERT INTO spec.ope_spec(ope_name, file_name)
            VALUES (%s, %s)
            RETURNING ope_spec_id;
        """
        ope_name = os.path.basename(file_name)
        self._pg.execute2(sqlcmd, (ope_name, file_name))
        self.set_id(self.fetch_id())
        self._pg.commit2()

    def _store_rel(self):
        sqlcmd = """
        INSERT INTO spec.ope_spec_screen_rel(
                    ope_spec_id, ope_screen_id)
            VALUES (%s, %s);
        """
        for c in self._children:
            self._pg.execute2(sqlcmd, (self._id, c.get_id()))
        self._pg.commit2()


class OpeScreen(SpecBase):
    def __init__(self):
        SpecBase.__init__(self)
        self._attr_list = [OPE_SCREEN_NO, OPE_SCREENT_NAME]
        self._log = log.common_log.instance().logger('SpecScreen')

    def parser(self, d):
        SpecBase.parser(self, d)
        # ## SCREEN
        content_info_list = d.get(OPE_CONTENT_LIST)
        if not content_info_list:
            return
        for operation_info in content_info_list:
            obj_operation = OpeOperation()
            obj_operation.parser(operation_info)
            self._children.append(obj_operation)

    def store(self):
        print self._attr_dict.get(OPE_SCREEN_NO)
        self._pg.connect2()
        self._insert_screen(self._attr_dict.get(OPE_SCREEN_NO),
                            self._attr_dict.get(OPE_SCREENT_NAME))
        self._set_children_pid()
        self._store_children()
        self._store_rel()

    def _insert_screen(self, screen_no, screen_name):
        sqlcmd = """
        INSERT INTO spec.ope_screen(screen_no, screen_name)
            VALUES (%s, %s)
            RETURNING ope_screen_id;
        """
        self._pg.execute2(sqlcmd, (screen_no, screen_name))
        self.set_id(self.fetch_id())
        self._pg.commit2()

    def _store_rel(self):
        sqlcmd = """
        INSERT INTO spec.ope_screen_operation_rel(
                    ope_screen_id, ope_operation_id)
            VALUES (%s, %s);
        """
        for c in self._children:
            self._pg.execute2(sqlcmd, (self._id, c.get_id()))
        self._pg.commit2()


class OpeOperation(SpecBase):
    def __init__(self):
        SpecBase.__init__(self)
        self._attr_list = [OPE_TITLE_INFO, OPE_ACTION_INFO,
                           OPE_VIEW_INFO, OPE_REF_INFO]
        self._log = log.common_log.instance().logger('SpecOperation')

    def parser(self, d):
        SpecBase.parser(self, d)
        # ## SCREEN
        content_info_list = d.get(OPE_CONTENT_LIST)
        if not content_info_list:
            return
        for operation_info in content_info_list:
            obj_operation = OpeOperation()
            obj_operation.parser(operation_info)
            self._children.append(obj_operation)

    def store(self):
        self._pg.connect2()
        spec_img = SpecImage.instance()
        title = self._attr_dict.get (OPE_TITLE_INFO)
        action_id, view_id, ref_id = None, None, None
        image_file = self._attr_dict.get(OPE_ACTION_INFO)
        if image_file:
            action_id = spec_img.upload(image_file)
        image_file = self._attr_dict.get(OPE_VIEW_INFO)
        if image_file:
            view_id = spec_img.upload(image_file)
        image_file = self._attr_dict.get(OPE_REF_INFO)
        if image_file:
            ref_id = spec_img.upload(image_file)
        params = (title, view_id, action_id, ref_id)
        if set(params) == set([None]):
            pass
        self._insert_operation(params)
        self._set_children_pid()
        self._store_children()
        self._store_rel()

    def _insert_operation(self, params):
        sqlcmd = """
        INSERT INTO spec.ope_operation(
                    title, view_img_id, action_img_id, ref_img_id)
            VALUES (%s, %s, %s, %s)
            RETURNING operation_id;
        """
        self._pg.execute2(sqlcmd, params)
        self.set_id(self.fetch_id())
        self._pg.commit2()

    def _store_rel(self):
        sqlcmd = """
        INSERT INTO spec.ope_operation_rel(
                    parent_operation_id, child_operation_id)
            VALUES (%s, %s);
        """
        for c in self._children:
            self._pg.execute2(sqlcmd, (self._id, c.get_id()))
        self._pg.commit2()
