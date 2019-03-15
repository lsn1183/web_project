# -*- coding: UTF-8 -*-

class PointV001():

    def __init__(self):
        self.doc_type = 'POINTOUT'
        self.version = '0.01'
        self.doc_format_dict = {
            'category': {
                'xlsname': 'カテゴリ',
                'xlspos': [(1, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'small_category': {
                'xlsname': '小分類',
                'xlspos': [(4, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'basic_req': {
                'xlsname': '基本要件',
                'xlspos': [(5, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'folder': {
                'xlsname': '対象フォルダ',
                'xlspos': [(9, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
        }

        self.xls_sheet_name = '詳細計画'
        self.start_data_row = 3
        self.id_col = "folder"