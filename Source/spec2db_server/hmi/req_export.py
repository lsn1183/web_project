# -*- coding: UTF-8 -*-
import os
from Source.spec2db_server.hmi.hmi_base import HMIBase
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
APL_PROGRESS_IDX = 80  # apl_progress
IT_PROGRESS_IDX = 81  # it_progress
IT_FILE_NAME_IDX = 83  # it_file_name
IT_NOS_IDX = 84  # it_nos
IT_RESULTS_IDX = 85 # it_results
APL_TEST_FILE_IDX = 86  # apl_test_files
APL_TEST_NOS_IDX = 87  # apl_test_nos
APL_TEST_RESULTS_IDX = 88 # apl_test_results
EXTERNAL_QA_NO_COL = 94
EXTERNAL_QA_STATUS_COL = EXTERNAL_QA_NO_COL + 1
INTERNAL_QA_NO_COL = 96
INTERNAL_QA_STATUS_COL = INTERNAL_QA_NO_COL + 1
EXTERNAL_BUG_NO_COL = 98
EXTERNAL_BUG_STATUS_COL = EXTERNAL_BUG_NO_COL + 1


class ReqExport(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'req'
        self.key_col = 'req_rc_id'
        self.id_col = 'hu_id'
        self.dev_status_dict = {}
        self._pg.connect()
        self._pg.execute('select dev_status_id, status from hmi.dev_status')
        for db_data in self._pg.fetchall():
            self.dev_status_dict[db_data[0]] = db_data[1]
        self._pg.close()

    def do_export(self, template_file, out_file, filter_dict):
        self._pg.connect()
        filter_sql = ''
        for _k,_v in filter_dict.iteritems():
            if len(filter_sql) > 0:
                filter_sql+=' and '

            if _k == 'step':
                v_str = ','.join([("'" + i_dd + "'") for i_dd in _v])
                filter_sql+= 'step in ('+v_str+')'
            if _k == 'user':
                v_str_list = []
                for i_dd in _v:
                    if i_dd != 'empty':
                        v_str_list.append(i_dd)
                if len(v_str_list) > 0:
                    v_str = ','.join([("'" + i_dd + "'") for i_dd in v_str_list])
                    filter_sql+= '(charger in ('+v_str+')'
                    if 'empty' in _v:
                        filter_sql += " OR charger is null OR charger='')"
                    else:
                        filter_sql += ")"
                else:
                    if 'empty' in _v:
                        filter_sql += "(charger is null OR charger='')"
        
        export_sql = '''
            select represent_req, arl_id, major_category, medium_category,
                small_category, detail, basic_req, req, req.status,
                trigger, action, remark, hmi_spec_no, hmi_version,
                hmi_file_name, hmi_chapter, hmi_page, hmi_screen_id,
                func_spec_no, func_version, func_file_name, func_chapter,
                func_page, hu_id, unique_id, amp, dsrc, dcm,
                rse, touch_pad, separate_disp, system_conf, rel_requirement,
                exception, dcu_status, dcu_trigger, dcu_action,
                meu_status, meu_trigger, meu_action, hu_category_id,
                deal_flow, hmi_ds_screen_id, hmi_ds_no, hmi_ds_remark,
                apl_ds_if_no, apl_ds_service, apl_ds_exception, apl_ds_obj,
                apl_ds_step, apl_ds_remark, sys_ds_name, decompose_id, decompose_content,
                operation, dest_name, testcase_num, sys_remark, apl_status,
                sys_test_status, bi, sp29, sp30, sp31, iauto_complete,
                step, definition_id, ana_unique_id, seq_diagram_file,
                seq_diagram_no, application,
                ana_exception, is_represent_req, parent_rep_req,
                new_date, is_dalian, charger, author, apl_schedule,
                it_schedule, apl_progress, it_progress, it_release_ver,
                it_file_name, it_nos, '' as it_results,
                apl_test_files, apl_test_nos, '' apl_test_results,
                ds.status, dev_status_detail, dev_remark, 
                remark_if_no, remark_service_if, external_qa, 
                external_qa_status, internal_qa, internal_qa_status, bug_no,
                bug_status, ng_num
            from hmi.req as req
            left join hmi.dev_status as ds on req.dev_status = ds.dev_status_id
        '''

        if len(filter_sql) > 0:
            export_sql += ' where '+filter_sql
        export_sql += ' order by arl_id'
        print export_sql
        self._pg.execute(export_sql)
        rows = self._pg.fetchall()
        self.write_excel(template_file, out_file, rows)
        self._pg.close()

    def do_export_daily_finished_detail(self, template_file, out_path, date):
        self._pg.connect()
        closest_date = self._get_closest_date(self._pg, date)
        rows = self._get_daily_finished_detail(self._pg, date, closest_date)
        out_file_name = 'HMI_daily_finished_Detail_All_%s_%s.xlsx' % (date, closest_date)
        out_file = os.path.join(out_path, out_file_name)
        self.write_excel(template_file, out_file, rows)
        self._pg.close()
        return out_file_name

    def count_daily_finished_detail_by_user(self, pg, date, step, represent='No'):
        """
        :param pg:
        :param date:
        :param step:
        :param represent:
        :return:
        """
        req_data_list = self.get_daily_finished_detail(pg, date)
        count_dict = {}
        for req_data in req_data_list:
            if represent == 'No':
                if req_data.get("represent_req"):
                    continue
            elif represent == 'Yes':
                if not req_data.get("represent_req"):
                    continue
            else:
                pass
            if req_data.get("step") == step:
                author = req_data.get("author")
                if not req_data.get("author"):
                    author = '未分配'
                key = (req_data.get("charger"), author)
                if key in count_dict:
                    count_dict[key] = count_dict.get(key) + 1
                else:
                    count_dict[key] = 1
        return count_dict

    def count_daily_finished_detail_by_category(self, pg, date, step, represent='No'):
        req_data_list = self.get_daily_finished_detail(pg, date)
        count_dict = {}
        for req_data in req_data_list:
            if represent == 'No':
                if req_data.get("represent_req"):
                    continue
            elif represent == 'Yes':
                if not req_data.get("represent_req"):
                    continue
            else:
                pass
            if req_data.get("step") == step:
                key = (req_data.get("major_category"), req_data.get("medium_category"), req_data.get("small_category"))
                if key in count_dict:
                    count_dict[key] = count_dict.get(key) + 1
                else:
                    count_dict[key] = 1
        return count_dict

    def get_daily_finished_detail(self, pg, date):
        from Source.spec2db_server.hmi.hmi_req import HmiReq
        reb_obj = HmiReq()
        attr_list = reb_obj.attr_list[1:]
        req_data_list = []
        closest_date = self._get_closest_date(pg, date)
        rows = self._get_daily_finished_detail(pg, date, closest_date)
        for row in rows:
            req_data = dict(zip(attr_list, row))
            req_data_list.append(req_data)
        return req_data_list

    def _get_daily_finished_detail(self, pg, date, closest_date):
        sqlcmd = """
        SELECT a.represent_req, arl_id, major_category, medium_category,
               small_category, detail, basic_req, req, a.status,
               trigger, action, remark, hmi_spec_no, hmi_version,
               hmi_file_name, hmi_chapter, hmi_page, hmi_screen_id,
               func_spec_no, func_version, func_file_name, func_chapter,
               func_page, hu_id, unique_id, amp, dsrc, dcm,
               rse, touch_pad, separate_disp, system_conf, rel_requirement,
               exception, dcu_status, dcu_trigger, dcu_action,
               meu_status, meu_trigger, meu_action, hu_category_id,
               deal_flow, hmi_ds_screen_id, hmi_ds_no, hmi_ds_remark,
               apl_ds_if_no, apl_ds_service, apl_ds_exception, apl_ds_obj,
               apl_ds_step, apl_ds_remark, sys_ds_name, decompose_id, decompose_content,
               operation, dest_name, testcase_num, sys_remark, apl_status,
               sys_test_status, bi, sp29, sp30, sp31, iauto_complete,
               step, definition_id, ana_unique_id, seq_diagram_file,
               seq_diagram_no, application,
               ana_exception, is_represent_req, parent_rep_req,
               new_date, is_dalian, charger, author, apl_schedule,
               it_schedule, apl_progress, it_progress, it_release_ver,
               it_file_name, it_nos, '' as it_results,
               apl_test_files, apl_test_nos, '' as apl_test_results,
               dev_status_str, dev_status_detail, dev_remark,
               remark_if_no, remark_service_if, external_qa, 
               external_qa_status, internal_qa, internal_qa_status, bug_no,
               bug_status, ng_num
          FROM (
                SELECT t1.*, t2.status as dev_status_str, dev_major_category
                  FROM hmi.req_history as t1
                  LEFT JOIN hmi.dev_status as t2
                  on t1.dev_status = t2.dev_status_id
                  WHERE backup_date = %s and
                       (it_progress = '完成' or
                        dev_major_category = '完成'
                        )
          ) AS A
          LEFT JOIN (
            SELECT hu_id as old_hu_id, dev_major_category as old_dev_major_category, it_progress as old_it_progress
              FROM hmi.req_history as t1
              LEFT JOIN hmi.dev_status as t2
              on t1.dev_status = t2.dev_status_id
              WHERE backup_date = %s and 
                   (it_progress = '完成' or 
                    dev_major_category = '完成'
                    )
          ) AS B
          on A.hu_id = B.old_hu_id
          where (it_progress = '完成' and (A.it_progress <> B.old_it_progress or B.old_it_progress is null)) or
                ((A.dev_major_category <> B.old_dev_major_category or B.old_dev_major_category is null) and 
                  A.dev_major_category = '完成')
          ORDER BY a.hu_id
        """
        pg.connect()
        pg.execute(sqlcmd, (date, closest_date))
        rows = pg.fetchall()
        return rows

    def _get_closest_date(self, pg, date):
        sqlcmd = """
        SELECT distinct backup_date
          FROM hmi.req_history
          where backup_date < %s
          order by backup_date DESC
          limit 1
        """
        pg.execute(sqlcmd, [date])
        row = pg.fetchone()
        if row:
            return row[0]
        return ''

    def write_excel(self, template_file, out_file, db_data_list):
        openpyxl_wb = load_workbook(template_file)
        ws = openpyxl_wb.get_sheet_by_name('要件详细'.decode('utf8'))
        self.make_xls_validation(openpyxl_wb, ws, self._pg)
        ws._current_row = 5
        for db_data in db_data_list:
            out_data = list(db_data)
            if out_data[-10]:
                out_data[-10] = out_data[-10].split(" ")[0]
            if out_data[-9]:
                out_data[-9] = out_data[-9].split(" ")[0]
            if out_data[IT_PROGRESS_IDX] == u'完成':  # 结合
                it_files = out_data[IT_FILE_NAME_IDX]
                it_nos = out_data[IT_NOS_IDX]
                it_results = self.get_test_results(self._pg, it_files, it_nos, test_type='IT')
                out_data[IT_RESULTS_IDX] = it_results
            if out_data[APL_PROGRESS_IDX] == 100:  # APL进度
                apl_files = out_data[APL_TEST_FILE_IDX]
                apl_nos = out_data[APL_TEST_NOS_IDX]
                apl_results = self.get_test_results(self._pg, apl_files, apl_nos, test_type='APL')
                out_data[APL_TEST_RESULTS_IDX] = apl_results
            if out_data[EXTERNAL_QA_NO_COL]:  # external_qa QA NO
                out_data[EXTERNAL_QA_STATUS_COL] = self.export_qa(self._pg, out_data[EXTERNAL_QA_NO_COL])
            if out_data[INTERNAL_QA_NO_COL]:  #
                out_data[INTERNAL_QA_STATUS_COL] = self.export_innter_qa(self._pg, out_data[INTERNAL_QA_NO_COL])
            if out_data[EXTERNAL_BUG_NO_COL]:  # external_bug BUG NO
                out_data[EXTERNAL_BUG_STATUS_COL] = self.export_bug(self._pg, out_data[EXTERNAL_BUG_NO_COL])
            ws.append(out_data)
        openpyxl_wb.save(out_file)

    def export_qa(self, pg, id):
        export_sql2 = '''
            SELECT status
            FROM hmi.external_qa
            where qa_keyword = %s;
         '''
        try:
            pg.execute(export_sql2, [id])
            row = self._pg.fetchone()
            if row:
                return row[0]
            return None
        except:
            return None

    def export_innter_qa(self, pg, id):
        export_sql3 = '''
            SELECT status
            FROM hmi.internal_qa
            where qa_no = %s;
         '''
        try:
            id = int(id)
            pg.execute(export_sql3, [id])
            row = self._pg.fetchone()
            if row:
                return row[0]
            return None
        except:
            return None

    def export_bug(self, pg, id):
        export_sql2 = '''
            SELECT status
            FROM hmi.external_bug
            where bug_keyword = %s;
         '''
        try:
            pg.execute(export_sql2, [id])
            row = self._pg.fetchone()
            if row:
                return row[0]
            return None
        except:
            return None

    def parse_test_file_and_no(self, file_names, test_nos):
        test_file_no_list = []
        if not file_names or not test_nos:
            return test_file_no_list
        file_names = [f.strip() for f in file_names.split('&') if f.strip()]
        test_nos_list = [n.strip() for n in test_nos.split('&') if n.strip()]
        for file_name, test_nos in zip(file_names, test_nos_list):
            for test_no in test_nos.split('\n'):
                test_no = test_no.strip()
                if test_no:
                    test_file_no_list.append((file_name, test_no))
        return test_file_no_list

    def get_test_results(self, pg, file_names, test_nos, test_type='IT'):
        test_file_no_list = self.parse_test_file_and_no(file_names, test_nos)
        results_str = ''
        prev_file_name = ''
        for file_name, test_no in test_file_no_list:
            result = self._get_test_result(pg, file_name, test_no, test_type)
            if file_name == prev_file_name:
                results_str += '\n' + result
            else:
                if prev_file_name:
                    results_str += '\n&' + result
                else:
                    results_str += result
                prev_file_name = file_name
        return results_str

    def _get_test_result(self, pg, file_name, test_no, test_type='IT'):
        it_tables = ["it_inside_move", "it_result_init_end", "it_result_mode_transition",
                     "it_result_notify", "it_screen_move"]
        sqlcmd = """
        SELECT test_item
          FROM hmi.{it_table}
          where it_key = %s
        """
        if not file_name or not test_no:
            return ''
        it_key = ', '.join([file_name, test_no])
        for it_table in it_tables:
            sqlcmd2 = sqlcmd.format(it_table=it_table)
            pg.execute(sqlcmd2, [it_key])
            row = pg.fetchone()
            if row:
                if test_type == 'IT':
                    if row[0]:
                        return row[0]
                    else:
                        return '空白'
                else:  # APL
                    return u'○'
        return '空白'

    def make_xls_validation(self, wb, ws_info, pg_info):
        from openpyxl.utils import quote_sheetname
        status_ws = wb.get_sheet_by_name('状态表'.decode('utf8'))

        for ii, _ik in enumerate(sorted(self.dev_status_dict.keys()),1):
            status_ws['z%d' % ii] = self.dev_status_dict[_ik]

        dv_dev_status = DataValidation(type="list", formula1='{0}!$z$1:$z${last_row}'.format(quote_sheetname('状态表'.decode('utf8')),
                                                                                             last_row=len(self.dev_status_dict.keys())),
                                       allow_blank=True)
        dv_dev_status.sqref = 'CL6:CL30000'
        ws_info.add_data_validation(dv_dev_status)

        dv_apl_process = DataValidation(type="decimal", operator="between", formula1=0, formula2=100)
        dv_apl_process.sqref = 'CC6:CC30000'
        ws_info.add_data_validation(dv_apl_process)

        dv_it_result = DataValidation(type="list", formula1='"完成, 未完成"',
                                      allow_blank=True)
        dv_it_result.sqref = 'CD6:CD30000'
        ws_info.add_data_validation(dv_it_result)

        dv_is_dalian = DataValidation(type="list", formula1='"是, 否"',
                                      allow_blank=True)
        dv_is_dalian.sqref = 'BX6:BX30000'
        ws_info.add_data_validation(dv_is_dalian)


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')

    obj = ReqExport()
    print obj.get_current_time()
    obj._pg.connect()
    # a = obj.count_daily_finished_detail_by_user(obj._pg, '2018-03-14', 'SP30')
    # b = obj.count_daily_finished_detail_by_user(obj._pg, '2018-03-14', 'SP30', 'Yes')
    # c = obj.count_daily_finished_detail_by_category(obj._pg, '2018-03-14', 'SP30')
    # d = obj.count_daily_finished_detail_by_category(obj._pg, '2018-03-14', 'SP30', 'Yes')
    #obj.get_daily_finished_detail(obj._pg, '2018-03-18')
#     s = """
# a.represent_req, arl_id, major_category, medium_category,
#                small_category, detail, basic_req, req, a.status,
#                trigger, action, remark, hmi_spec_no, hmi_version,
#                hmi_file_name, hmi_chapter, hmi_page, hmi_screen_id,
#                func_spec_no, func_version, func_file_name, func_chapter,
#                func_page, hu_id, unique_id, amp, dsrc, dcm,
#                rse, touch_pad, separate_disp, system_conf, rel_requirement,
#                exception, dcu_status, dcu_trigger, dcu_action,
#                meu_status, meu_trigger, meu_action, hu_category_id,
#                deal_flow, hmi_ds_screen_id, hmi_ds_no, hmi_ds_remark,
#                apl_ds_if_no, apl_ds_service, apl_ds_exception, apl_ds_obj,
#                apl_ds_step, apl_ds_remark, sys_ds_name, decompose_id, decompose_content,
#                operation, dest_name, testcase_num, sys_remark, apl_status,
#                sys_test_status, bi, sp29, sp30, sp31, iauto_complete,
#                step, definition_id, ana_unique_id, seq_diagram_file,
#                seq_diagram_no, application,
#                ana_exception, is_represent_req, parent_rep_req,
#                new_date, is_dalian, charger, author, apl_schedule,
#                it_schedule, apl_progress, it_progress, it_release_ver,
#                it_file_name, it_nos, '' as it_results,
#                apl_test_files, apl_test_nos, '' as apl_test_results,
#                dev_status_str, dev_status_detail, dev_remark,
#                remark_if_no, remark_service_if, external_qa,
#                external_qa_status, internal_qa, internal_qa_status, bug_no,
#                bug_status, ng_num
#     """
#     for i, col in enumerate(s.split(','), 0):
#         print i, col.strip()
    # ReqExport().do_export_daily_finished_detail('../template/HMI_Detail_template_v005.xlsx', './', '2018-03-18')
    ReqExport().do_export('../template/HMI_Detail_template_v005.xlsx', './ta_2.xlsx', {"step": ['SP31']})
    print obj.get_current_time()
