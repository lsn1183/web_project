# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase
from openpyxl import load_workbook


class ItProgressQAExport(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)

    def do_export(self, template_file, out_file):
        self._pg.connect()

        export_sql = '''
            SELECT qa_id, follow, status, priority, subject, author, 
            update_date
            FROM hmi.it_progress_qa
        '''
        print export_sql
        self._pg.execute(export_sql)
        openpyxl_wb = load_workbook(template_file)
        ws = openpyxl_wb.get_sheet_by_name('Users')
        ws._current_row = 1
        for db_data in self._pg.fetchall():
            out_data = list(db_data)
            ws.append(out_data)
        openpyxl_wb.save(out_file)
        self._pg.close()


if __name__ == '__main__':
    import sys
    reload(sys)
    import os
    os.chdir('../')
    sys.setdefaultencoding('UTF-8')
    obj = ItProgressQAExport()
    template_file = r'./template/IT_Progress_QA.xlsx'
    out_file = r'./export/hmi/IT_Progress_QA_test.xlsx'
    obj.do_export(template_file, out_file)
