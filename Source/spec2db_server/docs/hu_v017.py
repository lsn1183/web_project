# -*- coding: UTF-8 -*-

class HuV017():
    def __init__(self):
        self.doc_type='HU'
        self.version = '0.17'
        self.doc_format_dict = {
            'author': {
                'xlsname': '担当',
                'xlspos': [(1, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'arl_id':{
                'xlsname': 'ARLから転記->ARLID',
                'xlspos': [(2, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'major_category':{
                'xlsname': 'ARLから転記->大分類',
                'xlspos': [(3, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'medium_category':{
                'xlsname': 'ARLから転記->中分類',
                'xlspos': [(4, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'small_category':{
                'xlsname': 'ARLから転記->小分類',
                'xlspos': [(5, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail':{
                'xlsname': 'ARLから転記->詳細',
                'xlspos': [(6, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'basic_req':{
                'xlsname': 'ARLから転記->基本要件',
                'xlspos': [(7, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'arl_req_post':{
                'xlsname': 'ARLから転記->ARL要件->要件',
                'xlspos': [(8, 9)],
                'datatype': 'STR',
                'needcheck': True
            },
            'arl_status':{
                'xlsname': 'ARLから転記->ARL要件->状態',
                'xlspos': [(9, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'arl_trigger':{
                'xlsname': 'ARLから転記->ARL要件->トリガ',
                'xlspos': [(10, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'arl_action':{
                'xlsname': 'ARLから転記->ARL要件->動作',
                'xlspos': [(11, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'arl_remark':{
                'xlsname': 'ARLから転記->ARL要件->備考',
                'xlspos': [(12, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_id':{
                'xlsname': 'H/U要件定義ID',
                'xlspos': [(13, 9)],
                'datatype': 'FORMULAR_HUID',
                'needcheck': True,
            },
            'unique_id':{
                'xlsname': 'ユニークID',
                'xlspos': [(14, 9)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'amp':{
                'xlsname': 'オプション項目->AMP',
                'xlspos': [(15, 9)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'dsrc':{
                'xlsname': 'オプション項目->DSRC',
                'xlspos': [(16, 9)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'dcm':{
                'xlsname': 'オプション項目->DCM',
                'xlspos': [(17, 9)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'rse':{
                'xlsname': 'オプション項目->RSE',
                'xlspos': [(18, 9)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'touch_pad':{
                'xlsname': 'オプション項目->TouchPad',
                'xlspos': [(19, 9)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'separate_disp':{
                'xlsname': 'オプション項目->SeparateDisp',
                'xlspos': [(20, 9)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'system_conf':{
                'xlsname': 'システム構成',
                'xlspos': [(21, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'rel_requirement':{
                'xlsname': '関連基本要件',
                'xlspos': [(22, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'exception':{
                'xlsname': '除外',
                'xlspos': [(23, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'dcu_status':{
                'xlsname': '責務分担->H/U->DCU->状態',
                'xlspos': [(24, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'dcu_trigger':{
                'xlsname': '責務分担->H/U->DCU->トリガー',
                'xlspos': [(25, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'dcu_action':{
                'xlsname': '責務分担->H/U->DCU->動作',
                'xlspos': [(26, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'meu_status':{
                'xlsname': '責務分担->H/U->MEU->状態',
                'xlspos': [(27, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'meu_trigger':{
                'xlsname': '責務分担->H/U->MEU->トリガー',
                'xlspos': [(28, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'meu_action':{
                'xlsname': '責務分担->H/U->MEU->動作',
                'xlspos': [(29, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_category_id':{
                'xlsname': 'H/U分類ID',
                'xlspos': [(30, 7)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'model_display':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->01.遠隔ディスプレイ(WVGA Display)->表示',
                'xlspos': [(31, 8)],
                'datatype': 'STR',
                'model_id': 1,
                'needcheck': True,
            },
            'model_remote_touch':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->02.Remote Touch I/F->タッチデバイス',
                'xlspos': [(32, 8)],
                'datatype': 'STR',
                'model_id': 2,
                'needcheck': True,
            },
            'model_satellite':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->03.Satellite SW->ヒーコン/オーディオパネル',
                'xlspos': [(33, 8)],
                'datatype': 'STR',
                'model_id': 3,
                'needcheck': True,
            },
            'model_dcm':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->04.DCM->通信用モジュ-ル',
                'xlspos': [(34, 8)],
                'datatype': 'STR',
                'model_id': 4,
                'needcheck': True,
            },
            'model_microphone':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->05.Microphone->音認用、BT用マイク',
                'xlspos': [(35, 8)],
                'datatype': 'STR',
                'model_id': 5,
                'needcheck': True,
            },
            'model_step1_amp':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->06.Step1 AMP->AVC-LANアンプ',
                'xlspos': [(36, 8)],
                'datatype': 'STR',
                'model_id': 6,
                'needcheck': True,
            },
            'model_step3_amp':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->07.Step3 AMP->MOST用アンプ',
                'xlspos': [(37, 8)],
                'datatype': 'STR',
                'model_id': 7,
                'needcheck': True,
            },
            'model_sp':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->08 SP->音の出力',
                'xlspos': [(38, 8)],
                'datatype': 'STR',
                'model_id': 8,
                'needcheck': True,
            },
            'model_rse':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->09.RSE->リアシ-ト用モニタ',
                'xlspos': [(39, 8)],
                'datatype': 'STR',
                'model_id': 9,
                'needcheck': True,
            },
            'model_IFBox':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->10.I/F BOX->2口のUSBジャック',
                'xlspos': [(40, 8)],
                'datatype': 'STR',
                'model_id': 10,
                'needcheck': True,
            },
            'model_usb_adapter':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->11. USB Adapter->USBジャック',
                'xlspos': [(41, 8)],
                'datatype': 'STR',
                'model_id': 11,
                'needcheck': True,
            },
            'model_radio_ant':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->12Radio ANT->ラジオアンテナ',
                'xlspos': [(42, 8)],
                'datatype': 'STR',
                'model_id': 12,
                'needcheck': True,
            },
            'model_xm_ant':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->13XM ANT->衛星用アンテナ',
                'xlspos': [(43, 8)],
                'datatype': 'STR',
                'model_id': 13,
                'needcheck': True,
            },
            'model_dab_ant':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->14DAB ANT->DAB用アンテナ',
                'xlspos': [(44, 8)],
                'datatype': 'STR',
                'model_id': 14,
                'needcheck': True,
            },
            'model_dtv_ant':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->15.DTV ANT->地デジ用アンテナ',
                'xlspos': [(45, 8)],
                'datatype': 'STR',
                'model_id': 15,
                'needcheck': True,
            },
            'model_gps_ant':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->16.GPS ANT->GPS用アンテナ',
                'xlspos': [(46, 8)],
                'datatype': 'STR',
                'model_id': 16,
                'needcheck': True,
            },
            'model_dsrc_etc':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->17. DSRC/ETC',
                'xlspos': [(47, 8)],
                'datatype': 'STR',
                'model_id': 17,
                'needcheck': True,
            },
            'model_mm_clock':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->18. Clock->時計',
                'xlspos': [(48, 8)],
                'datatype': 'STR',
                'model_id': 18,
                'needcheck': True,
            },
            'model_rear_controller':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->19. Rear Controller',
                'xlspos': [(49, 8)],
                'datatype': 'STR',
                'model_id': 19,
                'needcheck': True,
            },
            'model_its_ecu':{
                'xlsname': '責務分担->H/U以外のＭＭ部品->20. ITS-ECU',
                'xlspos': [(50, 8)],
                'datatype': 'STR',
                'model_id': 20,
                'needcheck': True,
            },
            'model_meter':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->20. Meter',
                'xlspos': [(51, 8)],
                'datatype': 'STR',
                'model_id': 21,
                'needcheck': True,
            },
            'model_hud':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->21. HUD',
                'xlspos': [(52, 8)],
                'datatype': 'STR',
                'model_id': 22,
                'needcheck': True,
            },
            'model_steering_switch':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->22. Steering Swith',
                'xlspos': [(53, 8)],
                'datatype': 'STR',
                'model_id': 23,
                'needcheck': True,
            },
            'model_rear_camera':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->23. Rear Camera',
                'xlspos': [(54, 8)],
                'datatype': 'STR',
                'model_id': 24,
                'needcheck': True,
            },
            'model_camera_ecu':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->24. Camera ECU',
                'xlspos': [(55, 8)],
                'datatype': 'STR',
                'model_id': 25,
                'needcheck': True,
            },
            'model_other_clock':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->25. Clock',
                'xlspos': [(56, 8)],
                'datatype': 'STR',
                'model_id': 26,
                'needcheck': True,
            },
            'model_body_ecu':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->26 Body ECU',
                'xlspos': [(57, 8)],
                'datatype': 'STR',
                'model_id': 27,
                'needcheck': True,
            },
            'model_air_controller':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->27. Air Controller',
                'xlspos': [(58, 8)],
                'datatype': 'STR',
                'model_id': 28,
                'needcheck': True,
            },
            'model_smartphone':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->28. SmartPhone',
                'xlspos': [(59, 8)],
                'datatype': 'STR',
                'model_id': 29,
                'needcheck': True,
            },
            'model_center':{
                'xlsname': '責務分担->他部署設計部品(部品名は参考)->29. Center',
                'xlspos': [(60, 8)],
                'datatype': 'STR',
                'model_id': 30,
                'needcheck': True,
            },
            'hu_remark':{
                'xlsname': '備考',
                'xlspos': [(61, 8)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sys_spec_chapter':{
                'xlsname': '機能配置を判断したエビデンス->001 システム仕様書->章　Chapter/Section\nor ページ番号 Page No',
                'xlspos': [(62, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'common_chapter':{
                'xlsname': '機能配置を判断したエビデンス->003 共通アプリ・AVC-LAN仕様書->章　Chapter/Section\nor ページ番号 Page No',
                'xlspos': [(63, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'common_seq_spec':{
                'xlsname': '機能配置を判断したエビデンス->003 共通アプリ・AVC-LAN仕様書->シーケンス仕様\nSequence spec.',
                'xlspos': [(64, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'common_seq_no':{
                'xlsname': '機能配置を判断したエビデンス->003 共通アプリ・AVC-LAN仕様書->シーケンス番号\nSequence No.',
                'xlspos': [(65, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'common_cmd_guide':{
                'xlsname': '機能配置を判断したエビデンス->003 共通アプリ・AVC-LAN仕様書->コマンドガイド\nCommand guide',
                'xlspos': [(66, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'common_opc':{
                'xlsname': '機能配置を判断したエビデンス->003 共通アプリ・AVC-LAN仕様書->OPC',
                'xlspos': [(67, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'inter_loc_spec':{
                'xlsname': '機能配置を判断したエビデンス->318 DCU-MEU間連携仕様書DCU-MEU interaction spec.->機能配置・機能仕様\nFunction location and spec.',
                'xlspos': [(68, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'inter_chapter':{
                'xlsname': '機能配置を判断したエビデンス->318 DCU-MEU間連携仕様書DCU-MEU interaction spec.->章　Chapter/Section\nor ページ番号 Page No',
                'xlspos': [(69, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'other_doc': {
                'xlsname': '機能配置を判断したエビデンス->その他資料Other document.->ドキュメント名\n※トヨタ仕様の場合は仕様番号も記載する事',
                'xlspos': [(70, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'other_chapter': {
                'xlsname': '機能配置を判断したエビデンス->その他資料Other document.->章　Chapter/Section\nor ページ番号 Page No',
                'xlspos': [(71, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'test_results':{
                'xlsname': 'テスト結果',
                'xlspos': [(72, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'future_req':{
                'xlsname': '未要件分析',
                'xlspos': [(73, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_remark1':{
                'xlsname': '備考1',
                'xlspos': [(74, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_remark2':{
                'xlsname': '備考2',
                'xlspos': [(75, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'leak_check':{
                'xlsname': '要件漏れチェック',
                'xlspos': [(76, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'last_modifier':{
                'xlsname': '最終修正担当',
                'xlspos': [(77, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'new_date':{
                'xlsname': '日付',
                'xlspos': [(78, 9)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'reason':{
                'xlsname': '変更理由',
                'xlspos': [(79, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'review_result':{
                'xlsname': 'レビュー結果',
                'xlspos': [(80, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'pointout_no':{
                'xlsname': '指摘No.',
                'xlspos': [(81, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'pointout_status':{
                'xlsname': 'ステータス',
                'xlspos': [(82, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'pointout_comment':{
                'xlsname': 'コメント',
                'xlspos': [(83, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'reader_check':{
                'xlsname': 'リーダチェック',
                'xlspos': [(84, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'reader2_check':{
                'xlsname': 'リーダ２チェック',
                'xlspos': [(85, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'final_check':{
                'xlsname': '最終チェック',
                'xlspos': [(86, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'pointout_charger':{
                'xlsname': '担当',
                'xlspos': [(87, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'pointout_priority':{
                'xlsname': '優先度',
                'xlspos': [(88, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'pointout_date':{
                'xlsname': '指摘提出日',
                'xlspos': [(89, 9)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'suntec_status': {
                'xlsname': 'Suntecステータス',
                'xlspos': [(90, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'fixed':{
                'xlsname': '修正済み',
                'xlspos': [(91, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'suntec_remark':{
                'xlsname': 'Suntec備考',
                'xlspos': [(92, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'arl_rel': {
                'xlsname': 'ARL関連指摘',
                'xlspos': [(93, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'suntec_cannot_modify': {
                'xlsname': 'Suntec修正不可',
                'xlspos': [(94, 9)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'lock_status': {
                'xlsname': '',
                'xlspos': [(95, 9)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'group_name': {
                'xlsname': '',
                'xlspos': [(96, 9)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'hu_md5':{
                'xlsname': '',
                'xlspos': [(97, 9)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'job_status':{
                'xlsname': '',
                'xlspos': [(98, 9)],
                'datatype': 'STR',
                'needcheck': False,
            },
        }

        self.xls_sheet_name = 'HU要件定義書'
        self.start_data_row = 10
        self.id_col = "hu_id"


