# -*- coding: UTF-8 -*-

class HmiNotifV001():
    def __init__(self):
        self.doc_type = 'Hmi_Notify'
        self.version = '0.01'
        self.doc_format_dict = {
            'it_no': {
                'xlsname': '番号',
                'xlspos': [(2, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'category': {
                'xlsname': '処理種類',
                'xlspos': [(3, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'rel_screen_id': {
                'xlsname': '関連画面ID',
                'xlspos': [(4, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'rel_service': {
                'xlsname': '関連Service/Utility',
                'xlspos': [(5, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'notify_interface': {
                'xlsname': 'Notifyインターフェース',
                'xlspos': [(6, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'notify_content': {
                'xlsname': 'Notify内容',
                'xlspos': [(7, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'notify_process': {
                'xlsname': 'Notifyに対する処理',
                'xlspos': [(8, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'trigger': {
                'xlsname': 'イベント（トリガー）',
                'xlspos': [(9, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'action': {
                'xlsname': 'アクション',
                'xlspos': [(10, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'action_process': {
                'xlsname': 'アクション処理内容',
                'xlspos': [(11, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'uac_process_content': {
                'xlsname': 'インターフェース(ServiceBridge/MCからのコール)',
                'xlspos': [(12, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'uac_if_process': {
                'xlsname': 'インターフェース処理内容',
                'xlspos': [(13, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'test_item': {
                'xlsname': 'テスト項目',
                'xlspos': [(14, 3)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'remark': {
                'xlsname': '備考欄',
                'xlspos': [(15, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'obstacle_id': {
                'xlsname': '障害ID',
                'xlspos': [(16, 4)],
                'datatype': 'STR',
                'needcheck': False,
            }

        }

        self.xls_sheet_name = 'Notify'
        self.start_data_row = 6
        self.id_col = "it_no"