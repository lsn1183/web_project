# -*- coding: UTF-8 -*-

class InternalQAV001():
    def __init__(self):
        self.doc_type = 'HMI_INTERNALQA'
        self.version = '0.01'
        self.doc_format_dict = {
            'qa_no': {
                'xlsname': 'No',
                'xlspos': [(1, 6)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'status': {
                'xlsname': '状态',
                'xlspos': [(2, 6)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'question': {
                'xlsname': '内容',
                'xlspos': [(3, 6)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'qa_date': {
                'xlsname': '提问日',
                'xlspos': [(4, 6)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'qa_author': {
                'xlsname': '提问者',
                'xlspos': [(5, 6)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hope_answer_date': {
                'xlsname': '回答希望日',
                'xlspos': [(6, 6)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'answer_detail': {
                'xlsname': '回答',
                'xlspos': [(7, 6)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'answer_date': {
                'xlsname': '回答日',
                'xlspos': [(8, 6)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'answerer': {
                'xlsname': '回答者',
                'xlspos': [(9, 6)],
                'datatype': 'STR',
                'needcheck': True,
            }
        }

        self.xls_sheet_name = 'Q&A管理表'
        self.start_data_row = 7
        self.id_col = "qa_no"