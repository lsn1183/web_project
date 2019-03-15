# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

class ExternalQAExport(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)

    def do_export(self, template_file, out_file):
        self._pg.connect()

        export_sql = '''
            SELECT qa_type, qa_keyword, qa_id, summary, charger, reporter, 
                   priority, status, create_date, update_date, arrive_date, 
                   detail
              FROM hmi.external_qa
              ORDER BY qa_rc_id

        '''
        print export_sql

        self._pg.execute(export_sql)
        openpyxl_wb = load_workbook(template_file)
        ws = openpyxl_wb.get_sheet_by_name('Suntec_TAGL_QA (NEDL JIRA) 2018')

        ws._current_row = 1
        for db_data in self._pg.fetchall():
            out_data = list(db_data)
            ws.append(out_data)

        openpyxl_wb.save(out_file)

        self._pg.close()