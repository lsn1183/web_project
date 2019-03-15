# -*- coding: UTF-8 -*-
"""
Created on 2017-8-16

@author: hcz
"""
import re
from spec import SpecBase
from spec import SPEC_CHAPTER_NUM, SPEC_CHAPTER_TITLE
from Source.xls2db.common import log
# 要求式样书
REQ_SPEC = 'req_spec'
REQ_CMD_FILENAME = 'cmd_filename'
REQ_VERSION = 'version'
REQ_ARTICLE = 'article'
REQ_SPEC_NO = 'spec_no'
REQ_RELATION_INFO = 'relation_info'
REQ_FILENAME = 'file_name'
# 记录
REQ_RC_CHAPTER_NUM = 'cmd_chapter_no'  # 8章
REQ_RC_CHAPTER_TITLE = "cmd_chapter_title"  # 章タイトル
REQ_RC_PAGE = "cmd_page"  # ページ/シート名/画面/表/番号等
REQ_RC_UPATE_DATE = 'cmd_update_date'  # 更新日
REQ_FUNC_NO_LIST = "func_no_list"  # 仕様書番号
REQ_FUNC_DOC_LIST = 'func_doc_list'  # 仕様書名(Document名)
REQ_FUNC_VER_LIST = 'func_ver_list'  # # version
REQ_FUNC_CHAPTER_LIST = "func_chapter_list"  # 章番号
REQ_RC_VALID = "cmd_valid_info"  # 要/不要
REQ_RC_REASON = "cmd_valid_reason"  # 不要な場合の理由
REQ_RC_DEPARTMENT = "author_depart"  # 所属
REQ_RC_GROUP = "author_group"  # Gr名
REQ_RC_AUTHOR_NAME = "author_name"  # 氏名
REQ_RC_WRITE_DATE = "author_write_date"  # 記載日
REQ_RC_COMMENT = "author_comment"  # 備考
# 分類
REQ_RC_CAT_FUN = r'機能仕様書'


class ReqSpec(SpecBase):
    """要求式样书
    """
    def __init__(self):
        SpecBase.__init__(self)
        self._type = 'REQ'
        self._attr_list = [REQ_SPEC,
                           REQ_CMD_FILENAME,
                           REQ_VERSION,
                           REQ_ARTICLE,
                           REQ_SPEC_NO,
                           REQ_FILENAME
                           ]
        self._log = log.common_log.instance().logger('REQ')

    def parser(self, d):
        SpecBase.parser(self, d)
        # ## 章节
        record_list = d.get(REQ_RELATION_INFO)
        if not record_list:
            return
        for record_info in record_list:
            obj_rc = ReqSpecRecord()
            obj_rc.parser(record_info)
            self._children.append(obj_rc)

    def store(self):
        sqlcmd = """
        INSERT INTO spec.req_spec_info(
                    req_spec, req_spec_no, version,
                    req_spec_name, req_spec_file_name, file_name)
            VALUES (%s, %s, %s,
                    %s, %s, %s)
            RETURNING req_spec_id;
        """
        params = (self._attr_dict.get(REQ_SPEC),
                  self._attr_dict.get(REQ_SPEC_NO),
                  self._attr_dict.get(REQ_VERSION),
                  self._attr_dict.get(REQ_ARTICLE),
                  self._attr_dict.get(REQ_CMD_FILENAME),
                  self._attr_dict.get(REQ_FILENAME)
                  )
        self._pg.connect2()
        self._pg.execute2(sqlcmd, params)
        self.set_id(self.fetch_id())
        self._pg.commit2()
        for c in self._children:
            c.set_parent_id(self.get_id())
            c.file_name = self._attr_dict.get(REQ_CMD_FILENAME)
            c.store()


class ReqSpecRecord(SpecBase):
    """要求记录
    """
    def __init__(self):
        SpecBase.__init__(self)
        self._type = 'ReqRecord'
        self._attr_list = [REQ_RC_CHAPTER_NUM,
                           REQ_RC_CHAPTER_TITLE,
                           REQ_RC_PAGE,
                           REQ_RC_UPATE_DATE,
                           REQ_FUNC_NO_LIST,
                           REQ_FUNC_DOC_LIST,
                           REQ_FUNC_VER_LIST,
                           REQ_FUNC_CHAPTER_LIST,
                           REQ_RC_VALID,
                           REQ_RC_REASON,
                           REQ_RC_DEPARTMENT,
                           REQ_RC_GROUP,
                           REQ_RC_AUTHOR_NAME,
                           REQ_RC_WRITE_DATE,
                           REQ_RC_COMMENT,
                           ]
        self.file_name = ''
        self._log = log.common_log.instance().logger('ReqRecord')

    def parser(self, d):
        SpecBase.parser(self, d)

    def store(self):
        func_no_list = self._attr_dict.get(REQ_FUNC_NO_LIST)
        func_doc_list = self._attr_dict.get(REQ_FUNC_DOC_LIST)
        func_ver_list = self._attr_dict.get(REQ_FUNC_VER_LIST)
        func_chapter_list = self._attr_dict.get(REQ_FUNC_CHAPTER_LIST)
        update_date = self._attr_dict.get(REQ_RC_UPATE_DATE)
        if not update_date or update_date == '-':
            update_date = None
        write_date = self._attr_dict.get(REQ_RC_WRITE_DATE)
        if not write_date or write_date == '-':
            write_date = None
        update_date, write_date = None, None
        for func_num, func_doc, func_ver in zip(func_no_list,
                                                func_doc_list,
                                                func_ver_list):
            # print func_chapter_list
            if len(func_chapter_list) == 1:
                chapter_infos = self._split_chapter_num(func_chapter_list[0])
                if not chapter_infos:
                    chapter_infos = func_chapter_list
            else:
                chapter_infos = func_chapter_list
            for chapter in chapter_infos:
                chapter_num, chapter_title = self._get_chapter_info(func_doc,
                                                                    chapter)
                if not chapter_num:
                    print '%s\t%s\t%s' % (self.file_name, func_doc, chapter)
                else:
                    if len(chapter_title) > 100:
                        print chapter
                        continue
                    category = REQ_RC_CAT_FUN
                    parames = (None,
                               self._attr_dict.get(REQ_RC_CHAPTER_NUM),
                               self._attr_dict.get(REQ_RC_CHAPTER_TITLE),
                               self._attr_dict.get(REQ_RC_PAGE),
                               update_date,
                               category,
                               func_num,
                               func_doc,
                               func_ver,
                               chapter_num,
                               chapter_title,
                               self._attr_dict.get(REQ_RC_VALID),
                               self._attr_dict.get(REQ_RC_REASON),
                               self._attr_dict.get(REQ_RC_DEPARTMENT),
                               self._attr_dict.get(REQ_RC_GROUP),
                               self._attr_dict.get(REQ_RC_AUTHOR_NAME),
                               write_date,
                               self._attr_dict.get(REQ_RC_COMMENT),
                               )
                    self._insert(parames)

    def _get_chapter_info(self, spec_file, chapter):
        result_num, result_title = None, None
        # r_list = [r"^\d+(\.\d+)+(\.|\s)", r"^\d+(\.\d+)+"]
        r_list = [r"^\d+(\.\d+)+((\.|\s)*|([A-Za-z_]{0}))",
                  r"^\d+(\.\d+)+(\.|\s)",
                  r"^別紙(\d|０|１|２|３|４|５|６|７|８|９])*\.*(_|\b)*",
                  ]
        obj_chapter = ReqChapter.instance()
        chapter_dict = obj_chapter.get_attr()
        for r in r_list:
            m = re.match(r, chapter)
            if m:
                num = m.group(0)
                title = chapter[m.end():]
                if num:
                    num = num.rstrip('_')
                    num = self._del_blank(num)
                    if num in chapter_dict:
                        result_num = num
                        result_title = title
                        break
                    # 去掉最后的点
                    num2 = self._del_dot(num)
                    if num2 != num:
                        if num2 in chapter_dict:
                            result_num, result_title = num2, title
                            break
                    # 加点
                    num3 = num2 + '.'
                    if num3 in chapter_dict:
                        result_num, result_title = num3, title
                        break
                    # 去掉'4.44.'
                    m = re.match('4.44.', num)
                    if m:
                        num4 = num[m.end():]
                        if num4 in chapter_dict:
                            result_num, result_title = num4, title
                            break
                        num5 = num4 + '0'
                        if num5 in chapter_dict:
                            result_num, result_title = num5, title
                            break
                    # 通过Title
                    obj_chapter = ReqChapter.instance()
                    num = obj_chapter.match_chater_num(spec_file, title)
                    if num:
                        result_num, result_title = num, title
                        break
        if not result_num:
            # 通过Title
            obj_chapter = ReqChapter.instance()
            title = chapter
            num = obj_chapter.match_chater_num(spec_file, title)
            if num:
                result_num, result_title = num, title
        return result_num, result_title

    def _split_chapter_num(self, chapter_num):
        r = r'\[.+?\]'
        p = re.compile(r)
        chapter_infos = []
        temp_chapter_list = p.findall(chapter_num)
        if temp_chapter_list:
            for info in temp_chapter_list:
                chapter_infos.append(info[1:-1])
            return chapter_infos
        r = r'(\d+(\.\d+)+(\.|\s)*\D+\d{0})'
        p = re.compile(r)
        temp_chapter_list = p.findall(chapter_num)
        if temp_chapter_list and len(temp_chapter_list) > 1:
            for info in temp_chapter_list:
                chapter_infos.append(info[0])
            return chapter_infos
        return []

    def _del_blank(self, s):
        r = r"^\d+(\.\d+)+\.*"
        m = re.match(r, s)
        if m:
            return m.group(0)
        return None

    def _del_dot(self, s):
        """去掉最后的点或空白"""
        r = r"^\d+(\.\d+)+"
        m = re.match(r, s)
        if m:
            return m.group(0)
        return None

    def _insert(self, params):
        sqlcmd = """
        INSERT INTO spec.req_spec_record(
                    no, req_chapter_num, req_chapter_title,
                    req_page, update_date, category,
                    spec_num, spec_file_name, version,
                    spec_chapter_num, spec_chapter_title, need,
                    reason, department, group_name,
                    name, date, remark)
            VALUES (%s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s) RETURNING req_rc_id;
        """
        self._pg.execute2(sqlcmd, params)
        req_rc_id = self.fetch_id()
        self._pg.commit2()
        self._insert_rel((self._parent_id, req_rc_id))

    def _insert_rel(self, params):
        sqlcmd = """
        INSERT INTO spec.req_spec_rel(
                    req_spec_id, req_rc_id)
            VALUES (%s, %s);
        """
        self._pg.execute2(sqlcmd, params)
        self._pg.commit2()


class ReqChapter(SpecBase):
    """
    """
    __instance = None

    @staticmethod
    def instance():
        if ReqChapter.__instance is None:
            ReqChapter.__instance = ReqChapter()
        return ReqChapter.__instance

    def __init__(self):
        SpecBase.__init__(self)
        self._func_specs = dict()
        self._log = log.common_log.instance().logger('ReqChapter')

    def load(self):
        for spec_file_name, spec_id in self._get_func_specs():
            chapters = self.load_chapter_by_spec_id(spec_id)
            self._func_specs[spec_file_name] = chapters

    def match_chater_num(self, spec_file_name, title):
        if spec_file_name == 'func_5_1_12_DataCommunicationCommon':
            pass
        if spec_file_name in self._func_specs:
            chapters = self._func_specs.get(spec_file_name)
        else:
            import os
            base_name, _ = os.path.splitext(spec_file_name)
            chapters = self._func_specs.get(base_name)
        if not chapters:
            return None
        for chapter_attr in chapters:
            if title == chapter_attr.get(SPEC_CHAPTER_TITLE):
                return chapter_attr[SPEC_CHAPTER_NUM]
        return None

    def load_chapter_num(self):
        sqlcmd = """
        SELECT distinct chapter_number, title
          FROM spec.spec_chapter
          WHERE chapter_number IS NOT NULL
                AND chapter_number <> ''
                and chapter_number <> '-'
          ORDER BY chapter_number
        """
        self._pg.connect2()
        for chapter_info in self._pg.get_batch_data2(sqlcmd):
            num = chapter_info[0]
            self._attr_dict[num] = chapter_info[1]  # Title

    def load_chapter(self):
        pass

    def _get_func_specs(self):
        sqlcmd = """
        SELECT spec_file_name, (array_agg(spec_id))[1] as max_spec_id
          FROM (
            SELECT spec_id, spec_num, spec_file_name
              FROM spec.spec_specification
              ORDER BY spec_file_name, spec_id DESC
          ) as a
          GROUP BY spec_file_name
          ORDER BY max_spec_id
        """
        self._pg.connect2()
        self._pg.execute2(sqlcmd)
        rows = self._pg.fetchall2()
        for row in rows:
            yield row[0], row[1]

    def load_chapter_by_spec_id(self, spec_id):
        sqlcmd = """
        SELECT a.chapter_id, chapter_number, title
          from spec.spec_spec_chapter_rel as a
          LEFT JOIN spec.spec_chapter as b
          ON a.chapter_id = b.chapter_id
          where spec_id = %s
          ORDER BY chapter_id
        """
        self._pg.connect2()
        chapter_list = []
        self._pg.execute2(sqlcmd, (spec_id,))
        rows = self._pg.fetchall2()
        for row in rows:
            chapter_id, chapter_number, title = row[0], row[1], row[2]
            attr = dict()
            attr[SPEC_CHAPTER_NUM] = chapter_number
            attr[SPEC_CHAPTER_TITLE] = title
            self._attr_dict[chapter_number] = title
            chapter_list.append(attr)
            sub_chapters = self.load_sub_chapter(chapter_id)
            chapter_list += sub_chapters
        return chapter_list

    def load_sub_chapter(self, chapted_id):
        sqlcmd = """
        SELECT chapter_id, chapter_number, title
          FROM spec.spec_chapter_chapter_rel as a
          LEFT JOIN spec.spec_chapter as b
          on a.child_chapter_id = b.chapter_id
          WHERE parent_chapter_id = %s
          ORDER BY a.order_no
        """
        self._pg.connect2()
        chapter_list = []
        self._pg.execute2(sqlcmd, (chapted_id,))
        rows = self._pg.fetchall2()
        if not rows:
            return []
        for row in rows:
            attr = dict()
            chapter_id, chapter_number, title = row[0], row[1], row[2]
            attr[SPEC_CHAPTER_NUM] = chapter_number
            attr[SPEC_CHAPTER_TITLE] = title
            self._attr_dict[chapter_number] = title
            chapter_list.append(attr)
            sub_chapters = self.load_sub_chapter(chapter_id)
            chapter_list += sub_chapters
        return chapter_list
