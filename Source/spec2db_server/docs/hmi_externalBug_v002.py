# -*- coding: UTF-8 -*-


class ExternalBug002():
    def __init__(self):
        self.doc_type = 'HMI_EXTERNALBUG'
        self.version = '0.02'
        self.doc_format_dict = {
            'bug_type': {
                'xlsname': '问题类型',
                'xlspos': [(1, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'bug_keyword': {
                'xlsname': '问题关键字',
                'xlspos': [(2, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'bug_id': {
                'xlsname': '问题ID',
                'xlspos': [(3, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'summary': {
                'xlsname': '概要',
                'xlspos': [(4, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'charger': {
                'xlsname': '经办人',
                'xlspos': [(5, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'reporter': {
                'xlsname': '报告人',
                'xlspos': [(6, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'priority': {
                'xlsname': '优先级',
                'xlspos': [(7, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'status': {
                'xlsname': '状态',
                'xlspos': [(8, 1)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'create_date': {
                'xlsname': '创建日期',
                'xlspos': [(9, 1)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'update_date': {
                'xlsname': '已更新',
                'xlspos': [(10, 1)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'arrive_date': {
                'xlsname': '到期日',
                'xlspos': [(11, 1)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'detail': {
                'xlsname': '自定义字段(質問詳細)',
                'xlspos': [(12, 1)],
                'datatype': 'STR',
                'needcheck': True,
            }
        }

        self.xls_sheet_name = 'Suntec_TAGL_Bug (NEDL JIRA) 201'
        self.start_data_row = 2
        self.id_col = "bug_id"
