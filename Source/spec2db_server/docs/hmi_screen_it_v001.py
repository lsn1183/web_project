# -*- coding: UTF-8 -*-

class HmiScreenItV001():
    def __init__(self):
        self.doc_type = 'HMI_SCREEN_IT'
        self.version = '0.01'
        self.doc_format_dict = {
            'app_name': {
                'xlsname': 'APP名',
                'xlspos': [(2, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'first_layer': {
                'xlsname': '第一阶层画面',
                'xlspos': [(3, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'second_layer': {
                'xlsname': '第二阶层画面',
                'xlspos': [(4, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'third_layer': {
                'xlsname': '第三阶层画面',
                'xlspos': [(5, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'layer4': {
                'xlsname': '第四阶层画面',
                'xlspos': [(6, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'layer5': {
                'xlsname': '第五阶层画面',
                'xlspos': [(7, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'screen_id': {
                'xlsname': '画面ID',
                'xlspos': [(8, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'charger': {
                'xlsname': '负责人',
                'xlspos': [(9, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'in_migration_id': {
                'xlsname': '迁入状态',
                'xlspos': [(10, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'in_migration_date': {
                'xlsname': '对应预定日',
                'xlspos': [(11, 2)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'followup_migration_id': {
                'xlsname': '后续画面是否可以迁移',
                'xlspos': [(12, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'followup_migration_date': {
                'xlsname': '对应预定日',
                'xlspos': [(13, 2)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'test_docker': {
                'xlsname': '测试Docker分支',
                'xlspos': [(14, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'remark': {
                'xlsname': '备注',
                'xlspos': [(15, 2)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'delete': {
                'xlsname': '删除',
                'xlspos': [(16, 2)],
                'datatype': 'STR',
                'needcheck': False,
            }
        }

        self.xls_sheet_name = '画面进度'
        self.start_data_row = 3
        self.id_col = "screen_id"