# -*- coding: UTF-8 -*-

class HimItResultModeTransitionV001():
    def __init__(self):
        self.doc_type = 'HMI_IT_RESULT_MODE_TRANSITION'
        self.version = '0.01'
        self.doc_format_dict = {
            'it_no': {
                'xlsname': '番号',
                'xlspos': [(2, 4)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'mode_name': {
                'xlsname': 'モードネーム',
                'xlspos': [(3, 4)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'category': {
                'xlsname': '処理種類',
                'xlspos': [(4, 4)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'video_content_callback': {
                'xlsname': '映像コンテントコールバック(APFWからコール)',
                'xlspos': [(5, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'video_process_callback': {
                'xlsname': '映像コールバック処理内容',
                'xlspos': [(6, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'audio_content_callback': {
                'xlsname': '音声コンテントコールバック(APFWからコール)',
                'xlspos': [(7, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'audio_process_callback': {
                'xlsname': '音声コールバック処理内容',
                'xlspos': [(8, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'event_trigger': {
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
            'test_item': {
                'xlsname': 'テスト項目',
                'xlspos': [(12, 3)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'remark': {
                'xlsname': '備考欄',
                'xlspos': [(13, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'obstacle_id': {
                'xlsname': '障害ID',
                'xlspos': [(14, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
        }

        self.xls_sheet_name = 'モード遷移'
        self.start_data_row = 6
        self.id_col = "it_no"