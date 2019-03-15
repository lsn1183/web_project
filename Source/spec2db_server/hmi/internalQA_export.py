# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

class InternalQAExport(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)

    def do_export(self, template_file, out_file):
        self._pg.connect()

        export_sql = '''
            SELECT qa_no, status, question, qa_date, qa_author, hope_answer_date, 
                   answer_detail, answer_date, answerer
            FROM hmi.internal_qa
            order by qa_no
        '''
        print export_sql

        self._pg.execute(export_sql)
        openpyxl_wb = load_workbook(template_file)
        ws = openpyxl_wb.get_sheet_by_name('Q&A管理表'.decode('utf8'))

        ws._current_row = 6
        for db_data in self._pg.fetchall():
            out_data = list(db_data)
            ws.append(out_data)

        openpyxl_wb.save(out_file)

        self._pg.close()
