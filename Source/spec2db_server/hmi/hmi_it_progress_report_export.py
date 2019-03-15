# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
HMI_START_ROW_NUM = 4


class HmiItProgressReportExport(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)

    def do_export(self, template_file, out_file, filter_dict):
        self._pg.connect()
        process_status_dict = {}
        dev_status_dict2 = {}
        self._pg.execute('select  process_status_id, process_status from hmi.it_process_status')
        for db_data in self._pg.fetchall():
            process_status_dict[db_data[0]] = db_data[1]
        self._pg.execute('select dev_status_id, dev_status from hmi.it_dev_status')
        for db_data in self._pg.fetchall():
            dev_status_dict2[db_data[0]] = db_data[1]
        # 选择负责人
        filter_sql = ''
        for _k, _v in filter_dict.iteritems():
            if len(filter_sql) > 0:
                filter_sql += ' and '
            if _k == 'user':
                v_str_list = []
                for i_dd in _v:
                    if i_dd != 'empty':
                        v_str_list.append(i_dd)
                if len(v_str_list) > 0:
                    v_str = ','.join([("'" + i_dd + "'") for i_dd in v_str_list])
                    filter_sql += '(author in ('+v_str+')'
                    if 'empty' in _v:
                        filter_sql += " OR author is null OR author='')"
                    else:
                        filter_sql += ")"
                else:
                    if 'empty' in _v:
                        filter_sql += "(author is null OR author='')"
            # if _k == 'user':
            #     v_str_list = []
            #     for i_dd in _v:
            #         v_str_list.append(i_dd)
            #     if len(v_str_list) > 0:
            #         v_str = ','.join([("'" + i_dd + "'") for i_dd in v_str_list])
            #         filter_sql += '(author in (' + v_str + ')' + ")"
        export_sql = '''
            SELECT step, remark, it_group, gl, author, plan_date, progress_code, 
                   progress_ut, progress_it, progress_risk, comment, cate_alias, 
                   represent_req, req_id, jira_id, qa_id, release_ver, major_category, 
                   medium_category, small_category, major, small, status, trigger, 
                   action, check_status, trans_status, trans_trigger, trans_action, 
                   trans_explain, progress_status, author_is_me, is_same_it, is_make, 
                   is_have_qa, dev_update_date, dev_represent, dev_fw16_status, 
                   dev_s_date1, dev_model_status, dev_s_date2, dev_ut_status, dev_s_date3, 
                   dev_it_status, dev_s_date4, dev_itn_status, dev_s_date5, dev_commit_id, 
                   dev_s_date6, atsah_path, ut_path, it_path, analysis_path, dev_status, 
                   dev_remark, dev_qaid, dev_qa_status, '' as qa_author, '' as QAIDCheck,
                   unit1, usercase1, testcase1, 
                   ut_status1, ut_no1, unit2, usercase2, testcase2, ut_status2, 
                   ut_no2, unit3, usercase3, testcase3, ut_status3, ut_no3, unit4, 
                   usercase4, testcase4, ut_status4, ut_no4, unit5, usercase5, testcase5, 
                   ut_status5, ut_no5, unit6, usercase6, testcase6, ut_status6, 
                   ut_no6, unit7, usercase7, testcase7, ut_status7, ut_no7, unit8, 
                   usercase8, testcase8, ut_status8, ut_no8, unit9, usercase9, testcase9, 
                   ut_status9, ut_no9, unit10, usercase10, testcase10, ut_status10, 
                   ut_no10
            FROM hmi.it_progress_report 
        '''
        if len(filter_sql) > 0:
            export_sql += ' where '+filter_sql
        export_sql += ' ORDER by req_id'
        print export_sql
        self._pg.execute(export_sql)
        screen_db_list = []
        for db_data in self._pg.fetchall():
            screen_db_list.append(db_data)
        openpyxl_wb = load_workbook(template_file)
        ws = openpyxl_wb.get_sheet_by_name('SP30SP31对象进度'.decode('utf8'))
        # xls_row = HMI_START_ROW_NUM
        self.make_xls_validation(ws, len(screen_db_list), self._pg)
        ws._current_row = HMI_START_ROW_NUM - 1
        for screen_data in screen_db_list:
            screen_data = list(screen_data)
            screen_data[37] = process_status_dict.get(screen_data[37])
            screen_data[39] = process_status_dict.get(screen_data[39])
            screen_data[41] = process_status_dict.get(screen_data[41])
            screen_data[43] = process_status_dict.get(screen_data[43])
            screen_data[45] = process_status_dict.get(screen_data[45])
            screen_data[53] = dev_status_dict2.get(screen_data[53])
            qa_ids = screen_data[55]
            qa_status, qa_author = self.get_qa_info(self._pg, qa_ids)
            screen_data[56] = qa_status
            screen_data[57] = qa_author
            req_id = screen_data[13]
            jira_id = screen_data[14]
            qa_id_check = self._get_qa_ids_by_id(self._pg, req_id, jira_id)
            screen_data[58] = qa_id_check
            screen_data[62] = dev_status_dict2.get(screen_data[62])
            screen_data[67] = dev_status_dict2.get(screen_data[67])
            screen_data[72] = dev_status_dict2.get(screen_data[72])
            screen_data[77] = dev_status_dict2.get(screen_data[77])
            screen_data[82] = dev_status_dict2.get(screen_data[82])
            screen_data[87] = dev_status_dict2.get(screen_data[87])
            screen_data[92] = dev_status_dict2.get(screen_data[92])
            screen_data[97] = dev_status_dict2.get(screen_data[97])
            screen_data[102] = dev_status_dict2.get(screen_data[102])
            screen_data[107] = dev_status_dict2.get(screen_data[107])
            ws.append(screen_data)
        openpyxl_wb.save(out_file)
        self._pg.close()

    def _get_qa_ids_by_id(self, pg, req_id, jira_id):
        if jira_id:
            jira_cond = "or jira_id like '%%' || %s || '%%'"
            param = [req_id, jira_id]
        else:
            jira_cond = ''
            param = [req_id]
        sqlcmd = """
        SELECT DISTINCT qa_id
          FROM hmi.it_progress_qa
          where req_id = %s {jira_cond}
          ORDER BY qa_id
        """.format(jira_cond=jira_cond)
        pg.execute(sqlcmd, param)
        rows = pg.fetchall()
        qa_id_list = []
        for row in rows:
            qa_id_list.append(row[0])
        return '\n'.join(qa_id_list)

    def get_qa_info(self, pg, qa_ids):
        qa_id_list = self.parse_qa_id(qa_ids)
        status_list = []
        author_list = []
        for qa_id in qa_id_list:
            qa_info = self._get_qa_info_by_id(pg, qa_id)
            if qa_info:
                status_list.append(qa_info.get("status"))
                author_list.append(qa_info.get("author"))
        return '\n'.join(status_list), '\n'.join(author_list)

    def _get_qa_info_by_id(self, pg, qa_id):
        sqlcmd = """
        SELECT status, author
          FROM hmi.it_progress_qa
          where qa_id = %s
        """
        info = dict()
        pg.execute(sqlcmd, [qa_id])
        row = pg.fetchone()
        if row:
            info["status"] = row[0]
            info["author"] = row[1]
        return info

    def parse_qa_id(self, qa_ids):
        if qa_ids:
            return qa_ids.split('\n')
        return []

    def get_it_status_list(self, pg):
        """开发流程分类
        :param pg:
        :return:
        """
        sqlcmd = """
                SELECT process_status
                  FROM hmi.it_process_status
                  order by process_status_id
                """
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        it_status_list = []
        for row in rows:
            it_status_list.append(row[0])
        return it_status_list

    def get_it_followup_status_list(self, pg):
        """开发状态分类
        """
        sqlcmd = """
                SELECT dev_status
                  FROM hmi.it_dev_status
                  order by dev_status_id
                """
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        it_followup_status_list = []
        for row in rows:
            it_followup_status_list.append(row[0])
        return it_followup_status_list

    def make_xls_validation(self, ws, row_count, pg):
        # 开发流程分类
        for colm in ('AL%s:AL%s', 'AN%s:AN%s', 'AP%s:AP%s', 'AR%s:AR%s', 'AT%s:AT%s'):
            it_status_list = self.get_it_status_list(pg)
            status_str = '"%s"' % ', '.join(it_status_list)
            dv_it_result = DataValidation(type="list", formula1=status_str, allow_blank=True)
            dv_it_result.sqref = colm % (HMI_START_ROW_NUM, row_count + HMI_START_ROW_NUM)
            ws.add_data_validation(dv_it_result)
        # 开发状态分类
        for colm2 in ('BB%s:BB%s', 'BK%s:BK%s', 'BP%s:BP%s', 'BU%s:BU%s', 'BZ%s:BZ%s', 'CE%s:CE%s', 'CJ%s:CJ%s',
                      'CO%s:CO%s', 'CT%s:CT%s', 'CY%s:CY%s', 'DD%s:DD%s'):
            it_followup_status_list = self.get_it_followup_status_list(pg)
            followup_status_str = '"%s"' % ', '.join(it_followup_status_list)
            dv_is_dalian = DataValidation(type="list", formula1=followup_status_str, allow_blank=True)
            dv_is_dalian.sqref = colm2 % (HMI_START_ROW_NUM, row_count + HMI_START_ROW_NUM)
            ws.add_data_validation(dv_is_dalian)


if __name__ == '__main__':
    import sys, os
    reload(sys)
    os.chdir('../')
    # s = """
    # step, remark, it_group, gl, author, plan_date, progress_code,
    #                progress_ut, progress_it, progress_risk, comment, cate_alias,
    #                represent_req, req_id, jira_id, qa_id, release_ver, major_category,
    #                medium_category, small_category, major, small, status, trigger,
    #                action, check_status, trans_status, trans_trigger, trans_action,
    #                trans_explain, progress_status, author_is_me, is_same_it, is_make,
    #                is_have_qa, dev_update_date, dev_represent, dev_fw16_status,
    #                dev_s_date1, dev_model_status, dev_s_date2, dev_ut_status, dev_s_date3,
    #                dev_it_status, dev_s_date4, dev_itn_status, dev_s_date5, dev_commit_id,
    #                dev_s_date6, atsah_path, ut_path, it_path, analysis_path, dev_status,
    #                dev_remark, dev_qaid, dev_qa_status, '' as qa_author, '' as QAIDCheck,
    #                unit1, usercase1, testcase1,
    #                ut_status1, ut_no1, unit2, usercase2, testcase2, ut_status2,
    #                ut_no2, unit3, usercase3, testcase3, ut_status3, ut_no3, unit4,
    #                usercase4, testcase4, ut_status4, ut_no4, unit5, usercase5, testcase5,
    #                ut_status5, ut_no5, unit6, usercase6, testcase6, ut_status6,
    #                ut_no6, unit7, usercase7, testcase7, ut_status7, ut_no7, unit8,
    #                usercase8, testcase8, ut_status8, ut_no8, unit9, usercase9, testcase9,
    #                ut_status9, ut_no9, unit10, usercase10, testcase10, ut_status10,
    #                ut_no10
    # """
    # for i, t in enumerate(s.split(','), 1):
    #     print i, t.strip()

    sys.setdefaultencoding('UTF-8')
    obj = HmiItProgressReportExport()
    obj.do_export(r'./template/IT_Progress_Report.xlsx', './test.xlsx', {"user": ['mpty']})
    print obj.get_current_time()
