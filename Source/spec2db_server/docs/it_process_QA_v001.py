# -*- coding: UTF-8 -*-

class ItProcessQaV001():
    def __init__(self):
        self.doc_type = 'IT_PROCESS_QA'
        self.version = '0.01'
        self.doc_format_dict = {
            'qa_id': {
                'xlsname': '#',
                'xlspos': [(1, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'follow': {
                'xlsname': '跟踪',
                'xlspos': [(2, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'status': {
                'xlsname': '状态',
                'xlspos': [(3, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'priority': {
                'xlsname': '优先级',
                'xlspos': [(4, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'subject': {
                'xlsname': '主题',
                'xlspos': [(5, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'author': {
                'xlsname': '指派给',
                'xlspos': [(6, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'update_date': {
                'xlsname': '更新于',
                'xlspos': [(7, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
        }
        self.xls_sheet_name = 'Users'
        self.start_data_row = 2
        self.id_col = "qa_id"