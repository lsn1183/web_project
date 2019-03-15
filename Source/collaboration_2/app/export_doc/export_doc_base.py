# -*- coding: UTF-8 -*-
import os
import json
import pandas as pd
from xlsxwriter import Workbook
from ..ctrl.ctrl_ds_doc import CtrlDsDoc
from ..xl.section_wt import SectionWriter, write_body_title_format, my_box
from ..xl.section_wt import DOS_BULLET
BODY_TILE_FORMAT = {'bg_color': '#ffc000'}
COVER_WIDTH_POINT = 1.75  # 18像素
COVER_WIDTH_PIXEL = 1.75 / 0.75


class ExportDocBase(object):
    def __init__(self, doc_id=None, doc_type='BASIC', export_format="xlsx"):
        self.doc_id = doc_id
        self.export_format = export_format
        self.doc_data = None
        self.wb = None
        self.spec_list = []
        self.title_format = None
        self.doc_type = doc_type
        self.uc_writer = None
        self.uc_ws = None
        self.sequence_ws_names = dict()

    def do_export(self, out_dir, doc_id=None, export_format="xlsx"):
        if doc_id:
            self.doc_id = doc_id
        if export_format:
            self.export_format = export_format
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        # 取数据
        # 写excel
        self.doc_data = CtrlDsDoc().get_doc(self.doc_id, detail=True)
        if self.doc_data:
            file_name = self._get_file_name()
            file_path = os.path.join(out_dir, file_name)
            self.wb = Workbook(file_path)
            self.title_format = self.wb.add_format(BODY_TILE_FORMAT)
            # 表紙
            self._export_cover()
            # 创建目次
            content_ws = self.wb.add_worksheet(u'目次')
            # 软件需求一览
            spec_ws = self.wb.add_worksheet(u'软件需求一览')
            # IF仕様書
            self._export_if()
            self._export_block()  # Block_Component図
            self._export_class()  # Class図
            self._export_usecase()   # UseCase図
            self._export_sequence()  # Sequence/Activity
            self._export_std()  # State
            # UseCase和Sequence关系表
            self._export_uc_seq_rel()
            # 写入目次
            self._export_content(content_ws)
            # 写入软件需求一览(式样书)
            self._export_specs(spec_ws)
            self.wb.worksheets_objs[0].activate()
            file_path = self.wb.filename
            self.wb.close()
            return file_path
        return ''

    def _get_file_name(self):
        return '.'.join([self.doc_data.get("title"), self.export_format])

    def _export_cover(self):
        """表紙
        """
        title = self.doc_data.get("title")
        summary = self.doc_data.get("summary")
        cover_sheet = self.wb.add_worksheet(u'表紙')
        cover_sheet.set_column('A:AQ', COVER_WIDTH_POINT)  #
        # cover_sheet.set_default_row(SEC_CELL_HEIGHT_POINT)
        # ## 框
        my_box(self.wb, cover_sheet, 5, 2, 15, 29)
        # ## 标题
        title = self.filter_title(title)
        properties = {'align': 'center', 'font_size': 22}
        merge_format = self.wb.add_format(properties)
        cover_sheet.merge_range('D10:AC10', title, merge_format)
        type_name = self._get_doc_type_name()
        cover_sheet.merge_range('D12:AC12', type_name, merge_format)
        # ## 概要
        cover_sheet.write(22, 2, DOS_BULLET + u'概要')
        row = 23
        if summary:
            summary = summary.replace('<br>', '\n')
            for s in summary.split('\n'):
                cover_sheet.write(row, 3, s)
                row += 1
        cover_sheet.hide_gridlines(2)
        # cover_sheet.set_h_pagebreaks([43])
        # cover_sheet.set_v_pagebreaks([43])
        cover_sheet.set_page_view()

    def filter_title(self, title):
        if not title:
            return title
        import re
        for doc_type_s in ["BasicDesign", "DetailDesign",
                           "基本设计书", "详细设计书",
                           "基本设计", "详细设计"]:
            r = r"[\s|\-|_]*%s[\s|\-|_]*" % doc_type_s
            p = re.compile(r, re.I)
            m = p.findall(title)
            if m:
                title = title.replace(m[0], ' ')
        return title.strip()

    def _get_doc_type_name(self):
        names = {"BASIC": u'模块基本设计书',
                 "DETAIL": u'模块详细设计书'}
        return names.get(self.doc_type)

    def _export_content(self, ws):
        """目次
        :return:
        """
        write_body_title_format(ws, DOS_BULLET + u'目次', 1, 1,
                                title_format=self.title_format)
        for i, sheet in enumerate(self.wb.worksheets_objs[2:], start=3):
            name = sheet.name
            coor = 'B%s' % i
            ws.write_url(coor, 'internal:%s!A2' % name, string=name)

    def _export_specs(self, spec_ws):
        data = []
        write_body_title_format(spec_ws, DOS_BULLET + u'I式样书中摘取', 1, 1,
                                title_format=self.title_format)
        sections = self.doc_data.get("sub")
        usecase = self._find_section(sections,
                                     "USERCASE")  # table list 放在Usecase下面
        table_list = usecase[0].get("table_list")
        columns = [{'header': u'式样书类型'}, {'header': u'式样书名称'},
                   {'header': u'机能点'}, {'header': u'UsecaseNo'}]
        for uc_data in table_list:
            uc_no = uc_data.get("number")
            uc_spec_list = uc_data.get("spec_list")
            if not uc_spec_list:
                continue
            for spec in uc_spec_list:
                spec_type = spec.get("spec")
                if spec_type == 'FUNC':
                    spec_type = '机能式样书'
                elif spec_type == 'OPE':
                    spec_type = '操作式样书'
                elif spec_type == 'REQ':
                    spec_type = '要求式样书'
                else:
                    spec_type = '机能式样书'
                spec_file_name = spec.get("spec_file_name")
                func_ids = spec.get("func_id")
                data.append([spec_type, spec_file_name, func_ids, uc_no])
        coor = 'B3:E%s' % max(7, len(data) + 3)
        spec_ws.add_table(coor, {'data': data,
                                 "columns": columns})
        spec_ws.set_column(coor, 40)

    def _export_if(self):
        ws = self.wb.add_worksheet(u'IF仕様書')
        write_body_title_format(ws, DOS_BULLET + u'I / F一覧', 1, 1,
                                title_format=self.title_format)
        # ws.write('B2', u'I / F一覧')
        columns = [{'header': u'接口'}, {'header': u'参数'},
                   {'header': u'返回值'}, {'header': u'接口说明'}]
        sections = self.doc_data.get("sub")
        if_data_list = self._find_section(sections, "IF")
        if_list = []
        for if_data in if_data_list:
            if_list.append([if_data.get("if_name"),
                            if_data.get("parameter"),
                            if_data.get("return_val"),
                            if_data.get("description"),
                            ])
        coor = 'B3:E%s' % max(7, len(if_list) + 4)
        ws.add_table(coor, {'data': if_list, "columns": columns})
        ws.set_column(coor, 40)

    def _export_block(self):
        """Block图
        :return:
        """
        sections = self.doc_data.get("sub")
        block_data_list = self._find_section(sections, "BLOCK")
        ws = self.wb.add_worksheet('Block図')
        if block_data_list:
            block_data = block_data_list[0]
        else:
            block_data = dict()
        _, comment, image_urls = self.parse_content(block_data)
        sec_wt = SectionWriter(ws, title='Block図',
                               comment=comment, image_urls=image_urls,
                               title_format=self.title_format)
        sec_wt.write()

    def _export_class(self):
        """类图
        :return:
        """
        sections = self.doc_data.get("sub")
        class_datas = self._find_section(sections, "CLASS")
        ws = self.wb.add_worksheet('Class図')
        if class_datas:
            class_data = class_datas[0]
        else:
            class_data = dict()
        _, comment, image_urls = self.parse_content(class_data)
        sec_wt = SectionWriter(ws, title='Class図',
                               comment=comment, image_urls=image_urls,
                               title_format=self.title_format)
        sec_wt.write()

    def _export_usecase(self):
        """UseCase图
        :return:
        """
        sections = self.doc_data.get("sub")
        common_usecases = self._find_section(sections, "COMMON")
        if common_usecases:
            common_usecase = common_usecases[0]
            title, content, common_image_urls = self.parse_content(common_usecase)
            ws = self.wb.add_worksheet('UseCase_図')
            sec_wt = SectionWriter(ws, title='UseCase図', comment='',
                                   image_urls=common_image_urls,
                                   title_format=self.title_format)
            sec_wt.write()
            self.uc_ws = ws
            self.uc_writer = sec_wt
        # usecase_datas = self._find_section(sections, "USERCASE")
        # for i, usecase_data in enumerate(usecase_datas, start=1):
        #     ws = self.wb.add_worksheet('UseCase_%s図' % i)
        #     comment, image_urls = self.parse_content(usecase_data)
        #     image_urls += common_image_urls + image_urls
        #     sec_wt = SectionWriter(ws, title='UseCase図',
        #                            comment=comment, image_urls=image_urls,
        #                            title_format=self.title_format)
        #     sec_wt.write()
            # sub_sections = usecase_data.get("sub")
            # # Sequence图
            # self._export_sequence(sub_sections, str(i))
            # # spec式样书
            # sub_spec_list = self._find_section(sub_sections, sec_type='SPEC')
            # if sub_spec_list:
            #     specs = sub_spec_list[0].get("specs")
            #     if specs:
            #         self.spec_list += specs

    def _export_sequence(self):
        """Sequence图
        :return:
        """
        sections = self.doc_data.get("sub")
        sequence_list = self._find_section(sections, "SEQUENCE")
        for i, sequence_data in enumerate(sequence_list, start=1):
            seq_no = str(i)
            title, comment, image_urls = self.parse_content(sequence_data)
            if not title:
                title = 'Sequence図'
            ws_name = 'Sequence図_%s' % seq_no
            ws = self.wb.add_worksheet(ws_name)
            sec_wt = SectionWriter(ws, title=title,
                                   comment=comment, image_urls=image_urls,
                                   title_format=self.title_format)
            sec_wt.write()
            sub_sections = sequence_data.get("sub")
            # RESOURCE(资源)
            resource_list = self._find_section(sub_sections, "RESOURCE")
            self._export_resource(ws, resource_list, sec_wt.row + 2, 1)
            # Activity图
            activitys = self._find_section(sub_sections, "Activity")
            if activitys:
                self._export_activity(activitys, seq_no)
            sec_id = sequence_data.get("sec_id")
            self.sequence_ws_names[sec_id] = ws_name

    def _export_resource(self, ws, resources, row, col):
        data = []
        write_body_title_format(ws, DOS_BULLET + u'Resource', row, col,
                                title_format=self.title_format)
        columns = [{'header': u'名称'}, {'header': u'内容'}]
        for rsc in resources:
            content = []
            operator = rsc.get("operator")
            if operator:
                content.append(operator)
            val = rsc.get("value")
            if val:
                content.append(str(val))
            unit = rsc.get("unit")
            if unit:
                content.append(unit)
            content = ' '.join(content)
            data.append([rsc.get("rsc_name"), content])
        coor = 'B%s:C%s' % (row + 2, max(row + 7, row + len(data) + 3))
        ws.add_table(coor, {'data': data, "columns": columns})
        ws.set_column(coor, 25)

    def _export_activity(self, sections, sec_no):
        """activity
        :return:
        """
        # sections = self.doc_data.get("sub")
        # sec_data_list = self._find_section(sections, "Activity")
        for i, sec_data in enumerate(sections, start=1):
            act_no = '.'.join([sec_no, str(i)])
            title, comment, image_urls = self.parse_content(sec_data)
            if not title:
                title = 'Activity図'
            ws_name = 'Activity図_%s' % act_no
            ws = self.wb.add_worksheet(ws_name)
            sec_wt = SectionWriter(ws, title=title,
                                   comment=comment, image_urls=image_urls,
                                   title_format=self.title_format)
            sec_wt.write()

    def _export_std(self):
        """STD图
        :return:
        """
        sections = self.doc_data.get("sub")
        sec_data = self._find_section(sections, "STD")
        ws = self.wb.add_worksheet('StateMachine図')
        if sec_data:
            sec_data = sec_data[0]
        else:
            sec_data = dict()
        title, comment, image_urls = self.parse_content(sec_data)
        sec_wt = SectionWriter(ws, title='StateMachine図',
                               comment=comment, image_urls=image_urls,
                               title_format=self.title_format)
        sec_wt.write()

    def _export_uc_seq_rel(self):
        """UseCase和Sequence关系表
        """
        data = []
        row = self.uc_writer.row + 2
        write_body_title_format(self.uc_ws,
                                DOS_BULLET + u'Usecase和Sequence关系表',
                                row, 1,
                                title_format=self.title_format)
        row += 2
        sections = self.doc_data.get("sub")
        usecase = self._find_section(sections,
                                     "USERCASE")  # table list 放在Usecase下面
        table_list = usecase[0].get("table_list")
        columns = [{'header': u'UsecaseNo'}, {'header': u'Usecase名称'},
                   {'header': u'Usecase说明'}, {'header': u'SequenceNo'},
                   {'header': u'SequenceSheet名称'}]
        seq_sheet_names = []
        seq_nos = []
        for uc_data in table_list:
            uc_no = uc_data.get("number")
            uc_name = uc_data.get("title")
            content = uc_data.get("val")
            uc_seq_list = uc_data.get("seq_list")
            if not uc_seq_list:
                continue
            for sequence in uc_seq_list:
                seq_no = sequence.get("number")
                sec_id = sequence.get("sec_id")
                seq_sheet_name = self.sequence_ws_names.get(sec_id)
                seq_sheet_names.append(seq_sheet_name)
                seq_nos.append(seq_no)
                data.append([uc_no, uc_name, content, seq_no, seq_sheet_name])
        coor = 'B%s:F%s' % (row, max(row + 7, row + len(data) + 3))
        self.uc_ws.add_table(coor, {'data': data, "columns": columns})
        self.uc_ws.set_column(coor, 30)
        # 写入连接
        row += 1
        for i in range(0, len(seq_sheet_names)):
            coor = 'E%s' % (row + i)
            self.uc_ws.write_url(coor, 'internal:%s!A2' % seq_sheet_names[i],
                                 string=seq_nos[i])
            coor = 'F%s' % (row + i)
            self.uc_ws.write_url(coor, 'internal:%s!A2' % seq_sheet_names[i],
                                 string=seq_sheet_names[i])


    def _export_drbfm(self):
        pass

    def parse_content(self, section_data):
        comment = []
        image_urls = []
        if section_data:
            # print(section_data)
            parsed_sect_datas = json.loads(section_data.get("content"))
        else:
            parsed_sect_datas = [{"fileList": [], "val": ""}]
        for parsed_sect_data in parsed_sect_datas:
            title = parsed_sect_data.get("title")
            val = parsed_sect_data.get("val")
            image_info_list = parsed_sect_data.get("fileList")
            if val:
                comment.append(val)
            for image_info in image_info_list:
                url = image_info.get("url")
                if url:
                    image_urls.append(url)
        return title, comment, image_urls

    def _find_section(self, section_list, sec_type):
        sec_data_list = []
        if section_list:
            for section in section_list:
                if section.get("sec_type") == sec_type:
                    sec_data_list.append(section)
        return sec_data_list

    def del_illegal_char(self, s):
        illegal_char = " \/?*[]"  # excel sheet名的非法字符
        s = s.strip()
        for c in illegal_char:
            s = s.replace(c, '')
        return s
