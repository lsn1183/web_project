# -*- coding: UTF-8 -*-
"""
Created on 2017-7-18

@author: hcz
"""
import os
import json
import copy
import hashlib
import psycopg2
from Source.xls2db.common import log
from Source.xls2db.common.db import pg
LANGUAGE_CODE_JPN = 'jpn'
SPEC_FILE_NAME = "fileName"  # 机能式样书件名称
SPEC_NUM = 'chapterInfo'
SPEC_NAME = 'titleInfo'
SPEC_VERSION = "verInfo"  # 版本
SPEC_TERMINOLOGY = "nameDefInfo"  # 用語定義
SPEC_TERMINOLOGY_LIST = 'nameDefList'
SPEC_TERM_NAME = 'nameInfo'
SPEC_TERM_NAME_DEF = 'nameDef'
SPEC_CHAPTER_LIST = 'chapterInfoList'
SPEC_SUB_CHAPTER_LIST = 'subChapterList'
SPEC_CHAPTER_NUM = 'chapterInfo'  # 章节编号
SPEC_CHAPTER_TITLE = 'titleInfo'  # 机能章节
SPEC_CHAPTER_SUMMARY = 'summaryInfo'  # 机能概要
SPEC_CHAPTER_PREMISE = 'preCondition'  # 前提
SPEC_CHAPTER_CALL = 'callInfo'  # 呼出条件
SPEC_FUNC_LIST = 'funcInfoList'
SPEC_SUB_FUNC_LIST = 'subFuncList'
FUNCTION_TYPE = "funcType"  # 机能种别
FUNCTION_TYPE_IMG = 'IMG'  # 机能种别-图片
FUNCTION_CONTENT = "funcContent"
FUNCTION_ID = 'ID'  #
FUNCTION_TEST_TYPE = "testType"
FUNCTION_MODEL_LIST = 'modelList'
SEPC_HISTORY = 'history'
H_MODIFY_REASON = 'modify_reason'  # 修改原因
H_OLD_CONTENT = 'old_content'
H_NEW_CONTENT = 'new_content'
H_MODIFY_DATE = 'modify_date'
SPEC_DATA_TYPE = 'dataType'
SPEC_DATA_VAL = 'dataValue'
CHAPTER_TYPE_TERM = "terminology"
CHAPTER_TYPE_CPT = 'chapter'


class SpecBase(object):
    """
    """
    def __init__(self):
        self._permanent_id = 0
        self._type = ''
        self._id = 0
        self._parent_id = 0
        self._attr_list = []
        self._attr_dict = {}
        self._siblings = []
        self._children = []
        self._cmp_status = 'new'  # new, update, delete
        self._pg = pg()
        self._image_id = None
        # self._log = common.log.common_log.instance().logger('SpecBase')

    def parser(self, d):
        """Base"""
        for attr in self._attr_list:
            self._attr_dict[attr] = d.get(attr)
        for c in self._children:
            c.parser(d)

    def store(self):
        pass

    def set_attr(self, attr_dict):
        self._attr_dict = attr_dict

    def set_id(self, Id=0):
        self._id = Id

    def get_id(self):
        return self._id

    def set_permanent_id(self, permanent_id):
        self._permanent_id = permanent_id

    def fetch_id(self):
        Id = 0
        row = self._pg.fetchone2()
        if row:
            Id = row[0]
        return Id

    def set_parent_id(self, parnt_id):
        self._parent_id = parnt_id

    def _set_children_pid(self):
        for c in self._children:
            c.set_parent_id(self._id)

    def _store_children(self):
        for c in self._children:
            c.store()

    def load(self, Id):
        self._id = Id
        return False

    def load_by_name(self, name):
        print name
        return False

    def get_attr(self):
        return self._attr_dict

    def dump_attr(self, load_flag=True):
        attr_dict = copy.deepcopy(self._attr_dict)
        for c in self._children:
            c_attr = c.dump_attr(load_flag)
            attr_dict.update(c_attr)
        return attr_dict

    def get_file_name(self):
        return None

    def get_name(self):
        return None

    def get_children(self):
        return self._children

    def get_new_permanent_id(self):
        # self._pg.connect2()
        sqlcmd = """
        INSERT INTO spec.spec_permanent_id(type)
          VALUES(%s) RETURNING permanent_id;
        """
        self._pg.execute2(sqlcmd, (self._type,))
        self._permanent_id = self.fetch_id()

    def set_image_id(self, image_id):
        self._image_id = image_id

    def download_images(self):
        if self._image_id:
            spec_im = SpecImage.instance()
            spec_im.download_image(self._image_id, str(self._image_id))
        for c in self._children:
            c.download_images()


class SpecSpecification(SpecBase):
    """机能式样书
    """
    def __init__(self):
        SpecBase.__init__(self)
        self._type = 'spec'
        self._attr_list = [SPEC_NUM,
                           SPEC_NAME,
                           SPEC_FILE_NAME,
                           SPEC_VERSION,
                           ]
        self._children = [
                          # SpecTerminology(),
                          # SpecHistory(),
                          ]
        self._chapter_pos = len(self._children)
        self._log = log.common_log.instance().logger('SPEC')

    def get_num(self):
        return self._attr_dict.get(SPEC_NUM)

    def get_name(self):
        return self._attr_dict.get(SPEC_NAME)

    def get_file_name(self):
        return self._attr_dict.get(SPEC_FILE_NAME)

    def dump_attr(self, load_flag=True):
        attr_dict = copy.deepcopy(self._attr_dict)
        chapter_list = []
        for c in self._children:
            c_attr = c.dump_attr(load_flag)
            chapter_list.append(c_attr)
            # if type(c) == SpecChapter:  # 章节
            #     c_attr = c.dump_attr(load_flag)
            #     chapter_list.append(c_attr)
            # else:
            #     c_attr = c.dump_attr(load_flag)
            #     attr_dict.update(c_attr)
        attr_dict[SPEC_CHAPTER_LIST] = chapter_list
        return attr_dict

    def parser(self, d):
        """SPEC"""
        SpecBase.parser(self, d)
        # ## 章节
        chapter_info_list = d.get(SPEC_CHAPTER_LIST)
        if not chapter_info_list:
            return
        for chapter_info in chapter_info_list:
            if SPEC_TERMINOLOGY in chapter_info:
                obj_chapter = SpecTerminology()
            else:
                obj_chapter = SpecChapter()
            obj_chapter.parser(chapter_info)
            self._children.append(obj_chapter)

    def store(self):
        self._pg.connect2()
        sqlcmd = """
        INSERT INTO spec.spec_specification(permanent_id, spec_num, spec_name,
                                            spec_file_name, language, version)
            values(%s, %s, %s,
                   %s, %s, %s) returning spec_id;
        """
        if not self._permanent_id:
            self.get_new_permanent_id()
        spec_num = self._attr_dict.get(SPEC_NUM)
        spec_name = self._attr_dict.get(SPEC_NAME)
        file_name = self._attr_dict.get(SPEC_FILE_NAME)
        ver = self._attr_dict.get(SPEC_VERSION)
        language = LANGUAGE_CODE_JPN
        self._pg.execute2(sqlcmd, (self._permanent_id, spec_num, spec_name,
                                   file_name, language, ver))
        self.set_id(self.fetch_id())
        self._pg.commit2()
        self._set_children_pid()
        self._store_children()
        self._store_rel()
        self._set_dirty_flag(False)

    def _store_rel(self):
        sqlcmd = """
        INSERT INTO spec.spec_spec_chapter_rel(
                    spec_id, chapter_id)
            VALUES (%s, %s);
        """
        for c in self._children[self._chapter_pos:]:
            self._pg.execute2(sqlcmd, (self._id, c.get_id()))
        self._pg.commit2()

    def _set_children_pid(self):
        for c in self._children:
            c.set_parent_id(self._id)

    def _store_children(self):
        for c in self._children:
            c.store()

    def _set_dirty_flag(self, dirty=False):
        self._pg.commit2()
        sqlcmd = """
        UPDATE spec.spec_specification SET dirty=%s
         WHERE spec_id = %s;
        """
        self._pg.execute2(sqlcmd, (dirty, self._id))
        self._pg.commit2()

    def get_chapters(self):
        return self._children[self._chapter_pos:]

    def load(self, Id):
        if not Id:
            return False
        self._pg.connect2()
        sqlcmd = """
        SELECT permanent_id, spec_num, spec_name, spec_file_name,
               version, dirty, proj_id
          FROM spec.spec_specification
          WHERE spec_id = %s
        """
        self._pg.execute2(sqlcmd, (Id,))
        row = self._pg.fetchone2()
        if row:
            self._id = Id
            self._permanent_id = row[0]
            self._attr_dict[SPEC_NUM] = row[1]
            self._attr_dict[SPEC_NAME] = row[2]
            self._attr_dict[SPEC_FILE_NAME] = row[3]
            self._attr_dict[SPEC_VERSION] = row[4]
            self.load_children()
            return True
        return False

    def load_by_name(self, name):
        self._pg.connect2()
        sqlcmd = """
        SELECT spec_id, permanent_id, spec_num, spec_name,
               spec_file_name, version, dirty, proj_id
          FROM spec.spec_specification
          where (spec_num = %s or spec_name = %s) and dirty = False
          ORDER BY spec_id DESC
        """
        self._pg.execute2(sqlcmd, (name, name))
        row = self._pg.fetchone2()
        if row:
            self._id = row[0]
            self._permanent_id = row[1]
            self._attr_dict[SPEC_NUM] = row[2]
            self._attr_dict[SPEC_NAME] = row[3]
            self._attr_dict[SPEC_FILE_NAME] = row[4]
            self._attr_dict[SPEC_VERSION] = row[5]
            if not self.load_children():
                return False
            return True
        return False

    def load_children(self):
        for c in self._children:
            c.load(self._id)
        # 章节
        sqlcmd = """
        SELECT b.chapter_id, permanent_id, chapter_number,
               title, chapter_type
          FROM spec.spec_spec_chapter_rel as a
          LEFT JOIN spec.spec_chapter as b
          ON a.chapter_id = b.chapter_id
          WHERE spec_id = %s
          ORDER BY order_no
        """
        for chapter_info in self._pg.get_batch_data2(sqlcmd, (self._id,)):
            attr_dict = dict()
            chapter_id = chapter_info[0]
            permanent_id = chapter_info[1]
            attr_dict[SPEC_CHAPTER_NUM] = chapter_info[2]
            attr_dict[SPEC_CHAPTER_TITLE] = chapter_info[3]
            chapter_type = chapter_info[4]
            if chapter_type == CHAPTER_TYPE_TERM:
                obj_chapter = SpecTerminology()
            else:
                obj_chapter = SpecChapter()
            obj_chapter.set_id(chapter_id)
            obj_chapter.set_permanent_id(permanent_id)
            obj_chapter.set_attr(attr_dict)
            obj_chapter.load(chapter_id)
            self._children.append(obj_chapter)
        return True


class SpecChapter(SpecBase):
    """章节
    """
    def __init__(self):
        SpecBase.__init__(self)
        self._type = 'chapter'
        self._attr_list = [SPEC_CHAPTER_NUM,
                           SPEC_CHAPTER_TITLE,
                           FUNCTION_MODEL_LIST
                           ]
        self._sub_chapters = []  # 子章节
        self._log = log.common_log.instance().logger('CHAPTER')

    def dump_attr(self, load_flag=True):
        attr_dict = copy.deepcopy(self._attr_dict)
        # 子机能
        function_list = []
        for func in self._children:
            func_attr = func.dump_attr(load_flag)
            function_list.append(func_attr)
        if function_list:
            attr_dict[SPEC_FUNC_LIST] = function_list
        chapter_list = []
        for c in self._sub_chapters:
            chapter_attr = c.dump_attr(load_flag)
            chapter_list.append(chapter_attr)
        attr_dict[SPEC_SUB_CHAPTER_LIST] = chapter_list
        return attr_dict

    def parser(self, d):
        """Chapter"""
        SpecBase.parser(self, d)
        function_list = d.get(SPEC_FUNC_LIST)
        if not function_list:
            function_list = []
        chapter_num = self._attr_dict.get(SPEC_CHAPTER_NUM)
        # 机能
        for func in function_list:
            ojb_func = SpecFunction()
            ojb_func.set_parent_chapter_num(chapter_num)
            ojb_func.parser(func)
            self._children.append(ojb_func)
        # 子章节
        sub_chapters = d.get(SPEC_SUB_CHAPTER_LIST)
        for sub_chapter in sub_chapters:
            obj_chapter = SpecChapter()
            obj_chapter.parser(sub_chapter)
            self._sub_chapters.append(obj_chapter)

    def store(self):
        self._pg.connect2()
        sqlcmd = """
        INSERT INTO spec.spec_chapter(
                    permanent_id, chapter_number, title)
            VALUES (%s, %s, %s)
            returning chapter_id;
        """
        chapter_num = self._attr_dict.get(SPEC_CHAPTER_NUM)
        print chapter_num
        if not self._permanent_id:
            self.get_new_permanent_id()
        tile = self._attr_dict.get(SPEC_CHAPTER_TITLE)
        self._pg.execute2(sqlcmd, (self._permanent_id, chapter_num, tile))
        self.set_id(self.fetch_id())
        self._pg.commit2()
        self._set_children_pid()
        self.set_children_chapter_id()
        self._store_children()
        self._store_model_list()
        self._store_sub_chapters()
        self._store_rel()

    def _store_rel(self):
        # 章节与机能
        sqlcmd = """
        INSERT INTO spec.spec_chapter_func_rel(
                    chapter_id, func_id)
            VALUES (%s, %s);
        """
        for c in self._children:
            self._pg.execute2(sqlcmd, (self._id, c.get_id()))
        self._pg.commit2()
        # 章节与子章节
        sqlcmd = """
        INSERT INTO spec.spec_chapter_chapter_rel(
                    parent_chapter_id, child_chapter_id)
            VALUES (%s, %s);
        """
        for c in self._sub_chapters:
            self._pg.execute2(sqlcmd, (self._id, c.get_id()))
        self._pg.commit2()

    def _set_children_pid(self):
        for c in self._children:
            c.set_parent_id(self._id)

    def set_children_chapter_id(self):
        for c in self._children:
            c.set_parent_chapter_id(self._id)

    def set_children_chapter_num(self):
        for c in self._children:
            c.set_parent_chapter_num(self._attr_dict.get(SPEC_CHAPTER_NUM))

    def _store_children(self):
        for c in self._children:
            c.store()

    def _store_sub_chapters(self):
        for c in self._sub_chapters:
            c.store()

    def _store_model_list(self):
        model_list = self._attr_dict.get(FUNCTION_MODEL_LIST)
        if not model_list:
            return
        sqlcmd = """
        INSERT INTO spec.spec_chapter_model_rel(
                    chapter_id, model_id, val)
            VALUES (%s, %s, %s);
        """
        s_model = SpecModelList.instance()
        for mode_dict in model_list:
            for model, val in mode_dict.iteritems():
                if len(val) > 20:
                    chapter_num = self._attr_dict.get(SPEC_CHAPTER_NUM)
                    self._log.error('%s,Length of val too long.model=%s,val=%s'
                                    % (chapter_num, model, val))
                    continue
                model_id = s_model.get_model_id(model)
                self._pg.execute2(sqlcmd, (self._id, model_id, val))
        self._pg.commit2()

    def load(self, Id):
        self.load_model_list()
        self.load_child_function()
        self.load_child_chapter()

    def load_model_list(self):
        sqlcmd = """
        SELECT model, val
          FROM spec.spec_chapter_model_rel as a
          LEFT JOIN spec.spec_model b
          ON a.model_id = b.model_id
          WHERE chapter_id = %s
          ORDER BY order_no;
        """
        self._pg.execute2(sqlcmd, (self._id,))
        rows = self._pg.fetchall2()
        model_list = []
        for row in rows:
            model = row[0]
            val = row[1]
            model_list.append({model: val})
        self._attr_dict[FUNCTION_MODEL_LIST] = model_list

    def load_child_function(self):
        sqlcmd = """
        SELECT a.func_id, permanent_id, func_type,
               func_content, b.image_id, update_date,
               test_type, status, image_blob,
               id
          FROM spec.spec_chapter_func_rel as a
          LEFT JOIN spec.spec_functions as b
          ON a.func_id = b.func_id
          LEFT JOIN spec.spec_image as c
          ON b.image_id = c.image_id
          WHERE chapter_id = %s
          ORDER BY order_no;
        """
        self._pg.execute2(sqlcmd, (self._id,))
        for func_info in self._pg.fetchall2():
            func_id = func_info[0]
            permanent_id = func_info[1]
            attr_dict = dict()
            attr_dict[FUNCTION_TYPE] = func_info[2]
            func_content = func_info[3]
            image_id = func_info[4]
            attr_dict[FUNCTION_TEST_TYPE] = func_info[6]
            if func_info[9]:
                attr_dict[FUNCTION_ID] = func_info[9]
            if func_content:
                attr_dict[FUNCTION_CONTENT] = func_content
            else:
                attr_dict[FUNCTION_CONTENT] = []
            chapter_num = func_info[4]
            ojb_func = SpecFunction()
            ojb_func.set_id(func_id)
            ojb_func.set_permanent_id(permanent_id)
            ojb_func.set_attr(attr_dict)
            ojb_func.set_parent_chapter_num(chapter_num)
            ojb_func.set_image_id(image_id)
            ojb_func.load(func_id)
            self._children.append(ojb_func)

    def load_child_chapter(self):
        sqlcmd = """
        SELECT chapter_id, permanent_id, chapter_number,
               title, chapter_type
          FROM spec.spec_chapter_chapter_rel as a
          LEFT JOIN spec.spec_chapter as b
          ON a.child_chapter_id = b.chapter_id
          WHERE parent_chapter_id = %s
          ORDER BY order_no;
        """
        self._pg.execute2(sqlcmd, (self._id,))
        for chapter_info in self._pg.fetchall2():
            attr_dict = dict()
            chapter_id = chapter_info[0]
            permanent_id = chapter_info[1]
            attr_dict[SPEC_CHAPTER_NUM] = chapter_info[2]
            attr_dict[SPEC_CHAPTER_TITLE] = chapter_info[3]
            chapter_type = chapter_info[4]
            if chapter_type == CHAPTER_TYPE_TERM:
                obj_chapter = SpecTerminology()
            else:
                obj_chapter = SpecChapter()
            obj_chapter.set_id(chapter_id)
            obj_chapter.set_permanent_id(permanent_id)
            obj_chapter.set_attr(attr_dict)
            obj_chapter.load(chapter_id)
            self._sub_chapters.append(obj_chapter)

    def download_images(self):
        if self._image_id:
            spec_im = SpecImage.instance()
            spec_im.download_image(self._image_id, str(self._image_id))
        for c in self._children:
            c.download_images()
        for s in self._sub_chapters:
            s.download_images()


class SpecTerminology(SpecChapter):
    """用語定義
    """

    def __init__(self):
        SpecChapter.__init__(self)
        self._attr_list = [SPEC_CHAPTER_NUM,
                           SPEC_CHAPTER_TITLE,
                           FUNCTION_MODEL_LIST,
                           SPEC_TERMINOLOGY,
                           ]
        self._attr_dict[SPEC_TERMINOLOGY] = {}
        self._type = CHAPTER_TYPE_TERM
        self._log = log.common_log.instance().logger('Terminology')

    def store(self):
        self._pg.connect2()
        self._store_terminology()
        self._store_terminology_name()
        self._store_model_list()
        self._pg.commit2()

    def _store_terminology(self):
        sqlcmd = """
        INSERT INTO spec.spec_chapter(
                    permanent_id, chapter_number, title, chapter_type)
            VALUES (%s, %s, %s, %s)
            returning chapter_id;
        """
        if not self._permanent_id:
            self.get_new_permanent_id()
        chapter_num = self._attr_dict.get(SPEC_CHAPTER_NUM)
        print chapter_num
        chapter_title = self._attr_dict.get(SPEC_CHAPTER_TITLE)
        self._pg.execute2(sqlcmd, (self._permanent_id, chapter_num,
                                   chapter_title, CHAPTER_TYPE_TERM))
        self.set_id(self.fetch_id())
        self._pg.commit2()

    def _store_terminology_name(self):
        sqlcmd = """
        INSERT INTO spec.spec_terminology_name(
                    chapter_id, name, definition)
            VALUES (%s, %s, %s);
        """
        name_list = []
        terminology = self._attr_dict.get(SPEC_TERMINOLOGY)
        if terminology:
            name_list = terminology.get(SPEC_TERMINOLOGY_LIST)
        for name_info in name_list:
            name = json.dumps(name_info.get(SPEC_TERM_NAME),
                              ensure_ascii=False,
                              encoding='utf8')
            definition = json.dumps(name_info.get(SPEC_TERM_NAME_DEF),
                                    ensure_ascii=False,
                                    encoding='utf8')
            if len(name) > 256:
                chapter_num = self._attr_dict.get(SPEC_CHAPTER_NUM)
                self._log.error('%s, Length of name too long. name=%s'
                                % (chapter_num, name))
                continue
            self._pg.execute2(sqlcmd, (self._id, name, definition))
        self._pg.commit2()

    def _store_terminology_rel(self):
        sqlcmd = """
        INSERT INTO spec.spec_spec_terminology_rel(
                    spec_id, terminology_id)
            VALUES (%s, %s);
        """
        self._pg.execute2(sqlcmd, (self._parent_id, self._id))
        self._pg.commit2()

    def load(self, Id):
        self._id = Id
        self._load_terminology()
        self._load_terminology_name()
        self.load_model_list()

    def load_by_pid(self, parent_id):
        self._parent_id = parent_id
        self._load_terminology()
        self._load_terminology_name()
        self.load_model_list()

    def _load_terminology(self):
        sqlcmd = """
        SELECT chapter_number, title
          FROM spec.spec_chapter
          WHERE chapter_id = %s
        """
        self._pg.execute2(sqlcmd, (self._id,))
        row = self._pg.fetchone2()
        if row:
            self._attr_dict[SPEC_CHAPTER_NUM] = row[0]
            self._attr_dict[SPEC_CHAPTER_TITLE] = row[1]

    def _load_terminology_name(self):
        sqlcmd = """
        SELECT name, definition
          FROM spec.spec_terminology_name
          ORDER BY order_no
        """
        self._pg.execute2(sqlcmd, (self._id,))
        rows = self._pg.fetchall2()
        if rows:
            name_def_list = []
            for row in rows:
                name_dict = dict()
                name_dict[SPEC_TERM_NAME] = row[0]
                name_dict[SPEC_TERM_NAME_DEF] = row[1]
                name_def_list.append(name_dict)
            nameDefInfo = {SPEC_TERMINOLOGY_LIST: name_def_list}
            self._attr_dict[SPEC_TERMINOLOGY] = nameDefInfo
            return True
        return False

    def dump_attr(self, load_flag=True):
        attr_dict = copy.deepcopy(self._attr_dict)
        if load_flag:
            new_list = []
            name_dict_list = self._attr_dict.get(SPEC_TERMINOLOGY)
            if not name_dict_list:
                return attr_dict
            name_def_list = name_dict_list.get(SPEC_TERMINOLOGY_LIST)
            for name_dict in name_def_list:
                name = name_dict.get(SPEC_TERM_NAME)
                name_def = name_dict.get(SPEC_TERM_NAME_DEF)
                if type(name) in (str, unicode):
                    name = json.loads(name)
                if type(name_def) in (str, unicode):
                    name_def = json.loads(name_def)
                name_dict[SPEC_TERM_NAME] = name
                name_dict[SPEC_TERM_NAME_DEF] = name_def
                new_list.append(name_dict)
            attr_dict[SPEC_TERMINOLOGY] = {SPEC_TERMINOLOGY_LIST: new_list}
        return attr_dict


class SpecFunction(SpecBase):
    """机能点
    """
    def __init__(self):
        SpecBase.__init__(self)
        self._type = 'function'
        self._attr_list = [FUNCTION_TYPE,
                           FUNCTION_ID,
                           FUNCTION_CONTENT,
                           FUNCTION_TEST_TYPE,
                           FUNCTION_MODEL_LIST,
                           ]
        self._parent_chapter_id = None
        self._parent_chapter_num = None  # 章节编号
        self._log = log.common_log.instance().logger('FUNC')

    def dump_attr(self, load_flag=True):
        attr_dict = copy.deepcopy(self._attr_dict)
        if load_flag:
            content = attr_dict.get(FUNCTION_CONTENT)
            if type(content) in (str, unicode):
                content = json.loads(content)
            attr_dict[FUNCTION_CONTENT] = content
        sub_func_list = []
        for c in self._children:
            c_attr = c.dump_attr(load_flag)
            sub_func_list.append(c_attr)
        attr_dict[SPEC_SUB_FUNC_LIST] = sub_func_list
        return attr_dict

    def set_parent_chapter_id(self, chapter_id):
        self._parent_chapter_id = chapter_id

    def set_parent_chapter_num(self, chapter_num):
        self._parent_chapter_num = chapter_num

    def set_children_chapter_id(self):
        for c in self._children:
            c.set_parent_chapter_id(self._parent_chapter_id)

    def set_children_chapter_num(self):
        for c in self._children:
            c.set_parent_chapter_num(self._parent_chapter_num)

    def parser(self, d):
        """Function"""
        SpecBase.parser(self, d)
        sub_function_list = d.get(SPEC_SUB_FUNC_LIST)
        if not sub_function_list:
            return
        for func_info in sub_function_list:
            ojb_function = SpecFunction()
            ojb_function.set_parent_chapter_num(self._parent_chapter_num)
            ojb_function.parser(func_info)
            self._children.append(ojb_function)

    def store(self):
        self._pg.connect2()
        sqlcmd = """
        INSERT INTO spec.spec_functions(
                    permanent_id, func_type, func_content,
                    parent_chapter_num, status, test_type,
                    image_id, id
                    )
            VALUES(%s, %s, %s,
                   %s, %s, %s,
                   %s, %s)
            RETURNING func_id;
        """
        if not self._permanent_id:
            self.get_new_permanent_id()
        func_type = self._attr_dict.get(FUNCTION_TYPE)
        image_id = None
        if not self._attr_dict.get(FUNCTION_CONTENT):
            content = ''
        else:
            content = json.dumps(self._attr_dict.get(FUNCTION_CONTENT),
                                 ensure_ascii=False,
                                 encoding='utf8')
            if func_type == FUNCTION_TYPE_IMG:  # 图
                content2 = self._attr_dict.get(FUNCTION_CONTENT)
                image_file = self._get_image_file(content2)
                spec_img = SpecImage.instance()
                image_id = spec_img.upload(image_file)
        if not content and not self._children and func_type == 'FUNCTION':
            self._log.warning('Chapter_num=%s, This Func is no Content'
                              % (self._parent_chapter_num, ))
            content = ''
        status = None
        chapter_num = self._parent_chapter_num
        test_type = self._attr_dict.get(FUNCTION_TEST_TYPE)
        f_id = self._attr_dict.get(FUNCTION_ID)
        self._pg.execute2(sqlcmd, (self._permanent_id, func_type, content,
                                   chapter_num, status, test_type,
                                   image_id, f_id)
                          )
        self.set_id(self.fetch_id())
        self._pg.commit2()
        self._set_children_pid()
        self.set_children_chapter_id()
        self._store_children()
        self._store_model_list()
        self._store_rel()

    def _get_image_file(self, content):
        image_file = None
        if content:
            if type(content) in (str, unicode):
                content = json.loads(content)
            for el_list in content:
                for el in el_list:
                    if el.get(SPEC_DATA_TYPE) == FUNCTION_TYPE_IMG:
                        image_file = el.get(SPEC_DATA_VAL)[0]
                        break
        if not image_file:
            self._log.error('Chapter_num=%s, Does not identify Image file. '
                            'content=%s' % (self._parent_chapter_num, content))
        return image_file

    def _store_model_list(self):
        model_list = self._attr_dict.get(FUNCTION_MODEL_LIST)
        if not model_list:
            return
        sqlcmd = """
        INSERT INTO spec.spec_func_model_rel(
                    func_id, model_id, val)
            VALUES (%s, %s, %s);
        """
        sModel = SpecModelList.instance()
        for mode_dict in model_list:
            for model, val in mode_dict.iteritems():
                if len(val) > 20:
                    content = self._attr_dict.get(FUNCTION_CONTENT)
                    chapter_num = self._attr_dict.get(SPEC_CHAPTER_NUM)
                    self._log.error('%s,Length of val too long.model=%s,val=%s'
                                    % (chapter_num, model, val))
                    continue
                model_id = sModel.get_model_id(model)
                self._pg.execute2(sqlcmd, (self._id, model_id, val))
        self._pg.commit2()

    def _store_rel(self):
        sqlcmd = """
        INSERT INTO spec.spec_func_func_rel(
                    parent_func_id, child_func_id)
            VALUES (%s, %s);
        """
        for c in self._children:
            self._pg.execute2(sqlcmd, (self._id, c.get_id()))
        self._pg.commit2()

    def load(self, Id):
        self.load_model_list()
        sqlcmd = """
        SELECT func_id, func_type, func_content, 
               parent_chapter_num, test_type, id,
               image_id
          FROM spec.spec_func_func_rel AS a
          LEFT JOIN spec.spec_functions AS b
          ON a.child_func_id = func_id
          WHERE parent_func_id = %s
          ORDER BY order_no;
        """
        self._pg.execute2(sqlcmd, (self._id,))
        for func_info in self._pg.fetchall2():
            attr_dict = dict()
            func_id = func_info[0]
            attr_dict[FUNCTION_TYPE] = func_info[1]
            func_content = func_info[2]
            chapter_num = func_info[3]
            attr_dict[FUNCTION_TEST_TYPE] = func_info[4]
            if func_info[5]:
                attr_dict[FUNCTION_ID] = func_info[5]
            if func_content:
                attr_dict[FUNCTION_CONTENT] = func_content
            else:
                attr_dict[FUNCTION_CONTENT] = []
            image_id = func_info[6]
            ojb_func = SpecFunction()
            ojb_func.set_id(func_id)
            ojb_func.set_attr(attr_dict)
            ojb_func.set_parent_chapter_num(chapter_num)
            ojb_func.set_image_id(image_id)
            ojb_func.load(func_id)
            self._children.append(ojb_func)

    def load_model_list(self):
        sqlcmd = """
        SELECT model, val
          FROM spec.spec_func_model_rel as a
          LEFT JOIN spec.spec_model b
          ON a.model_id = b.model_id
          WHERE func_id = %s
          order by order_no;
        """
        self._pg.execute2(sqlcmd, (self._id,))
        rows = self._pg.fetchall2()
        model_list = []
        for row in rows:
            model = row[0]
            val = row[1]
            model_list.append({model: val})
        self._attr_dict[FUNCTION_MODEL_LIST] = model_list

    def download_images(self):
        if self._image_id:
            spec_im = SpecImage.instance()
            content = self._attr_dict.get(FUNCTION_CONTENT)
            image_file = self._get_image_file(content)
            spec_im.download_image(self._image_id, image_file)
        for c in self._children:
            c.download_images()


class SpecHistory(SpecBase):
    """式样书更新履歴
    """
    def __init__(self):
        SpecBase.__init__(self)
        self._attr_dict[SEPC_HISTORY] = []

    def dump_attr(self, load_flag=True):
        attr_dict = copy.deepcopy(self._attr_dict)
        if load_flag:
            history_list = self._attr_dict.get(SEPC_HISTORY)
            for h_dict in history_list:
                old_content = h_dict[H_OLD_CONTENT]
                new_content = h_dict[H_NEW_CONTENT]
                if load_flag:
                    if type(old_content) in (str, unicode):
                        old_content = json.loads(old_content)
                    if type(new_content) in (str, unicode):
                        new_content = json.loads(new_content)
                h_dict[H_OLD_CONTENT] = old_content
                h_dict[H_NEW_CONTENT] = new_content
            attr_dict[SEPC_HISTORY] = history_list
        return attr_dict

    def load(self, _parent_id):
        sqlcmd = """
        SELECT modify_reason, chapter, old_content,
               new_content, modify_date
          FROM (
            SELECT spec_id, spec_file_name
              FROM spec.spec_specification
              WHERE spec_file_name in (
                SELECT spec_file_name
                  FROM spec.spec_specification
                  WHERE spec_id  = %s
              )
          ) AS s
          INNER JOIN spec.spec_history AS h
          ON s.spec_id = h.spec_id
          ORDER BY s.spec_id, serial_no
        """
        self._pg.execute2(sqlcmd, (_parent_id,))
        rows = self._pg.fetchall2()
        if rows:
            history_list = []
            for row in rows:
                history_dict = {}
                history_dict[H_MODIFY_REASON] = row[0]
                history_dict[SPEC_CHAPTER_NUM] = row[1]
                history_dict[H_OLD_CONTENT] = row[2]
                history_dict[H_NEW_CONTENT] = row[3]
                history_dict[H_MODIFY_DATE] = str(row[4])
                history_list.append(history_dict)
            self._attr_dict[SEPC_HISTORY] = history_list
            return True
        self._attr_dict[SEPC_HISTORY] = []
        return False


class SpecReference(SpecBase):
    """参照先仕様書情報
    """
    def __init__(self):
        SpecBase.__init__(self)


class SpecCarInfo(SpecBase):
    """车型信息
    """
    def __init__(self):
        SpecBase.__init__(self)


class SpecModelList(SpecBase):
    __instance = None

    @staticmethod
    def instance():
        """create a instance"""
        if SpecModelList.__instance is None:
            SpecModelList.__instance = SpecModelList()
        return SpecModelList.__instance

    def __init__(self):
        SpecBase.__init__(self)

    def get_model_id_dict(self, modelList):
        for model_dict in modelList:
            for model in model_dict.iterkeys():
                model_id = self._attr_dict.get(model)
                if not model_id:
                    model_id = self._get_model_id(model)
                    self._attr_dict[model] = model_id
        return self._attr_dict

    def get_model_id(self, model):
        model_id = self._attr_dict.get(model)
        if not model_id:
            model_id = self._get_model_id(model)
            self._attr_dict[model] = model_id
        return model_id

    def _get_model_id(self, model):
        self._pg.connect2()
        sqlcmd = """
        SELECT model_id
          FROM spec.spec_model
          WHERE model = %s;
        """
        self._pg.execute2(sqlcmd, (model,))
        row = self._pg.fetchone2()
        if row and row[0]:
            return row[0]
        sqlcmd = """
        INSERT INTO spec.spec_model(model)
            VALUES (%s) RETURNING model_id;
        """
        self._pg.execute2(sqlcmd, (model,))
        model_id = self.fetch_id()
        self._pg.commit2()
        return model_id


class SpecImage(SpecBase):
    """
    """
    __instance = None

    @staticmethod
    def instance():
        """create a instance"""
        if SpecImage.__instance is None:
            SpecImage.__instance = SpecImage()
        return SpecImage.__instance

    def __init__(self):
        SpecBase.__init__(self)
        self._in_dir = r'./'
        self._out_dir = r'./'
        self._log = log.common_log.instance().logger('Image')

    def set_in_dir(self, in_dir):
        self._in_dir = in_dir

    def set_out_dir(self, out_dir):
        self._out_dir = out_dir

    def upload(self, image_file):
        if image_file:
            path = os.path.join(self._in_dir, image_file)
            if os.path.isfile(path):
                base_name = os.path.basename(path)
                image_name, image_ext = os.path.splitext(base_name)
                fp = open(path, 'rb')
                image_data = fp.read()
                fp.close()
                hash_key = hashlib.md5(image_data).hexdigest()
                old_image_id = self._get_image_id(image_name, hash_key)
                if old_image_id:
                    return old_image_id
                sqlcmd = """
                INSERT INTO spec.spec_image(image_name, image_type,
                                            image_blob, hash_key)
                    VALUES (%s, %s, %s, %s) RETURNING image_id;
                """
                self._pg.execute2(sqlcmd, (image_name, image_ext,
                                           psycopg2.Binary(image_data),
                                           hash_key)
                                  )
                image_id = self.fetch_id()
                self._pg.commit2()
                return image_id
            else:
                self._log.error('Dose not exist file: %s' % (image_file,))
        return None

    def _get_image_id(self, image_name, hash_key):
        self._pg.connect2()
        sqlcmd = """
        SELECT image_id
          FROM spec.spec_image
          where image_name = %s and hash_key = %s
        """
        self._pg.execute2(sqlcmd, (image_name, hash_key))
        row = self._pg.fetchone2()
        if row:
            return row[0]
        return None

    def download_image(self, image_id, image_file, image_type='jpeg'):
        if image_id:
            image_data = self.get_image_data(image_id)
            if not image_data:
                return None
            from PIL import Image
            import StringIO
            im = Image.open(StringIO.StringIO(image_data))
            path = os.path.join(self._out_dir, image_file)
            d = os.path.dirname(path)
            if not os.path.exists(d):
                os.mkdir(d)
            im.save(path)
        return path

    def get_image_data(self, image_id):
        sqlcmd = """
        SELECT image_blob
          FROM spec.spec_image
          WHERE image_id = %s
          limit 1
        """
        self._pg.connect2()
        self._pg.execute2(sqlcmd, (image_id,))
        row = self._pg.fetchone2()
        if row:
            return row[0]
        return None, None
