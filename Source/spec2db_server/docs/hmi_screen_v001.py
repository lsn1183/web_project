# -*- coding: UTF-8 -*-

class HmiScreenV001():
    def __init__(self):
        self.doc_type = 'HMI_SCREEN'
        self.version = '0.01'
        self.doc_format_dict = {
            'screen_id': {
                'xlsname': 'HMI画面ID',
                'xlspos': [(1, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'screen_progress': {
                'xlsname': 'HMI画面进度',
                'xlspos': [(12, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'external_qa': {
                'xlsname': '外部QA',
                'xlspos': [(13, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'remark': {
                'xlsname': '备注',
                'xlspos': [(14, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'is_enter_screen': {
                'xlsname': '是否为入口画面',
                'xlspos': [(15, 2)],
                'datatype': 'DATETIME',
                'needcheck': True,
            }
        }

        self.xls_sheet_name = 'HMI画面进度'
        self.start_data_row = 3
        self.id_col = "screen_id"
