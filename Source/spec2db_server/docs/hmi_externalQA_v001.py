# -*- coding: UTF-8 -*-

class ExternalQAV001():
    def __init__(self):
        self.doc_type = 'HMI_EXTERNALQA'
        self.version = '0.01'
        self.doc_format_dict = {
            'qa_no': {
                'xlsname': 'No',
                'xlspos': [(1, 12)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'status': {
                'xlsname': '状態',
                'xlspos': [(2, 12)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'summary': {
                'xlsname': '質問->質問概要',
                'xlspos': [(3, 13)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'question': {
                'xlsname': '質問->質問箇所',
                'xlspos': [(4, 13)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail': {
                'xlsname': '質問->質問詳細',
                'xlspos': [(5, 13)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'qa_date': {
                'xlsname': '質問->質問日',
                'xlspos': [(6, 13)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'qa_author': {
                'xlsname': '質問->質問者',
                'xlspos': [(7, 13)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hope_answer_date': {
                'xlsname': '質問->希望回答日',
                'xlspos': [(8, 13)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'qa_reviewer': {
                'xlsname': '質問->査閲者',
                'xlspos': [(9, 13)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'answer_detail': {
                'xlsname': '回答->回答詳細',
                'xlspos': [(10, 13)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'answer_date': {
                'xlsname': '回答->回答日',
                'xlspos': [(12, 13)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'answerer': {
                'xlsname': '回答->回答者',
                'xlspos': [(13, 13)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'answer_reviewer': {
                'xlsname': '回答->査閲者',
                'xlspos': [(14, 13)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'remark': {
                'xlsname': '備考',
                'xlspos': [(15, 12)],
                'datatype': 'STR',
                'needcheck': True,
            },
        }

        self.xls_sheet_name = 'Q&A管理表'
        self.start_data_row = 14
        self.id_col = "qa_no"