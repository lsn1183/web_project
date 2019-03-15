# -*- coding: UTF-8 -*-
import re
from Source.spec2db_server.hmi.hmi_base import HMIBase
from Source.spec2db_server.hmi.hmi_log import HmiLog
import time


class HmiReq(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'req'
        self.bakup_table_name = 'req_history'
        self.key_col = 'req_rc_id'
        self.id_col = 'hu_id'
        self.attr_list = ['req_rc_id', 'represent_req', 'arl_id', 'major_category', 'medium_category',
                          'small_category', 'detail', 'basic_req', 'req', 'status',
                          'trigger', 'action', 'remark', 'hmi_spec_no', 'hmi_version',
                          'hmi_file_name', 'hmi_chapter', 'hmi_page', 'hmi_screen_id',
                          'func_spec_no', 'func_version', 'func_file_name', 'func_chapter',
                          'func_page', 'hu_id', 'unique_id', 'amp', 'dsrc', 'dcm',
                          'rse', 'touch_pad', 'separate_disp', 'system_conf', 'rel_requirement',
                          'exception', 'dcu_status', 'dcu_trigger', 'dcu_action',
                          'meu_status', 'meu_trigger', 'meu_action', 'hu_category_id',
                          'deal_flow', 'hmi_ds_screen_id', 'hmi_ds_no', 'hmi_ds_remark',
                          'apl_ds_if_no', 'apl_ds_service', 'apl_ds_exception', 'apl_ds_obj',
                          'apl_ds_step', 'apl_ds_remark', 'sys_ds_name', 'decompose_id', 'decompose_content',
                          'operation', 'dest_name', 'testcase_num', 'sys_remark', 'apl_status',
                          'sys_test_status', 'bi', 'sp29', 'sp30', 'sp31', 'iauto_complete',
                          'step', 'definition_id', 'ana_unique_id', 'seq_diagram_file',
                          'seq_diagram_no', 'application',
                          'ana_exception', 'is_represent_req',
                          'parent_rep_req', 'new_date', 'is_dalian', 'charger', 'author', 'apl_schedule',
                          'it_schedule', 'apl_progress', 'it_progress', 'it_release_ver',
                          'it_file_name', 'it_nos', 'it_results',
                          'apl_test_files', 'apl_test_nos', 'apl_test_results',
                          'dev_status', 'dev_status_detail', 'dev_remark',
                          'remark_if_no', 'remark_service_if', 'external_qa',
                          'external_qa_status', 'internal_qa', 'internal_qa_status',
                          'bug_no', 'bug_status', 'ng_num']

    def get_category_tree(self, user_id=None):
        cat_tree = dict(result="NG", content=[{"category_id": "",
                                               "category_name": "XXX",
                                               "sub_category_list": [{}]
                                               }])
        cat_tree["content"] = self._get_category()
        if cat_tree.get("content"):
            cat_tree["result"] = "OK"
        return cat_tree

    def _get_category(self):
        sqlcmd = """
        SELECT distinct major_category, medium_category, small_category
          FROM hmi.req
          order by major_category, medium_category, small_category;
        """
        self._pg.connect()
        self._pg.execute(sqlcmd)
        category_list = []
        for row in self._pg.fetchall():
            sub_category_list = category_list
            j = 0
            while j < len(row):
                cat_id = ','.join(row[0:j + 1])
                cat_name = row[j]
                cat_dict = dict()
                cat_dict["category_id"] = cat_id
                cat_dict["category_name"] = cat_name
                if sub_category_list:
                    if cat_id == sub_category_list[-1].get("category_id"):
                        sub_category_list = sub_category_list[-1].get("sub_category_list")
                    else:
                        cat_dict["sub_category_list"] = []
                        sub_category_list.append(cat_dict)
                        sub_category_list = cat_dict.get("sub_category_list")
                else:
                    cat_dict["sub_category_list"] = []
                    sub_category_list.append(cat_dict)
                    sub_category_list = cat_dict.get("sub_category_list")
                j += 1
        self._pg.close()
        return category_list

    def get_hmi_all(self, pg):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [])
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        detail_data_list = []
        for row in rows:
            detail_data_list.append(dict(zip(self.attr_list, row)))
        return detail_data_list

    def get_hmi_screen(self, pg):
        sqlcmd = """
            SELECT hmi_ds_screen_id, hu_id
            FROM hmi.req
        """
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        hmi_screen_list = []
        for row in rows:
            hmi_screen_dict = dict()
            hmi_screen_dict['hmi_ds_screen_id'] = row[0]
            hmi_screen_dict['hu_id'] = row[1]
            hmi_screen_list.append(hmi_screen_dict)
        return hmi_screen_list

    def fist_add_hmi_screen(self):
        self._pg.connect()
        hmi_screen_list = self.get_hmi_screen(self._pg)
        for hmi_screen in hmi_screen_list:
            hu_id = hmi_screen.get('hu_id')
            hmi_screen_id = hmi_screen.get('hmi_ds_screen_id')
            hmi_screen_id_list = self.parse_screen_id(hmi_screen_id)
            for screen_id in hmi_screen_id_list:
                rows = self.select_hmi_screen(self._pg, screen_id)
                if not rows:
                    self.insert_hmi_screen(self._pg, screen_id)
            self.insert_screen(self._pg, hu_id, hmi_screen_id_list)
        self._pg.commit()
        self._pg.close()

    def summary_category(self, condition_data, page, size):
        condition_list = condition_data.split(',')
        condition = 'where '
        if len(condition_list) == 1:
            condition += "major_category = %s "
        elif len(condition_list) == 2:
            condition += "major_category = %s" + " and medium_category = %s "
        else:
            condition += "major_category = %s " + " and medium_category = %s" + " and small_category = %s "
        # if type == 'HMI':
        #     pass

        sqlcmd = """
            SELECT distinct hu_id, is_dalian, charger, author, apl_schedule, it_schedule, 
            apl_progress, it_progress, it_release_ver, dev_status, dev_remark, 
            external_qa, internal_qa, ng_num, length(hu_id) as len
          FROM hmi.req {condition}
          order by len
        """.format(condition=condition)
        self._pg.connect()
        rowcount, rows = self._fetch_many(self._pg, sqlcmd, condition_list, size, page)
        attr_dict_list = self._rows_arl_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def _rows_arl_summay_data(self, rows):
        attr_list = ["hu_id",
                     'is_dalian', 'charger', 'author', 'apl_schedule', 'it_schedule',
                     'apl_progress', 'it_progress', 'it_release_ver', 'dev_status', 'dev_remark',
                     'external_qa', 'internal_qa', 'ng_num'
                     ]
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(attr_list):
                attr_dict[attr_list[i]] = row[i]
                i += 1
            attr_dict['title'] = 'HU: ' + attr_dict['hu_id']
            attr_dict_list.append(attr_dict)
        return attr_dict_list

    def get_old_data(self, pg, hu_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, (hu_id,))
        row = pg.fetchone()
        
        detail_data_list = []
        if row:
            detail_data_list.append(dict(zip(self.attr_list, row)))

        return detail_data_list

    def get_detail_by_hu_id(self, hu_id):
        self._pg.connect()
        detail_data = self.get_old_data(self._pg, hu_id)
        status = self.get_dev_status_by_id(self._pg, detail_data[0]['dev_status'])
        detail_data[0]['dev_status'] = status
        self._pg.close()
        return detail_data

    def get_hmi_by_screen(self, screen_id):
        self._pg.connect()
        hmi_list = []
        hu_id_list = self.select_hu_id_by_screen(self._pg, screen_id)
        for hu_id in hu_id_list:
            data = self.get_old_data(self._pg, hu_id)
            hmi_list += data
        self._pg.close()
        return hmi_list

    def get_dev_status(self, classify=None):
        sqlcmd = """
           SELECT distinct t1.dev_status_id, status, category, dev_major_category, array_agg(val) detail_list
          FROM hmi.dev_status as t1 left join hmi.dev_status_rel as t2 
          on t1.dev_status_id = t2.dev_status_id group by t1.dev_status_id, status, category, dev_major_category
          order by dev_status_id
        """
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        dev_status = []
        for row in rows:
            status = dict()
            status["status_id"] = row[0]
            status["status"] = row[1]
            status["category"] = row[2]
            status["dev_major_category"] = row[3]
            status["detail"] = row[4]
            dev_status.append(status)
        self._pg.close()
        return dev_status

    def _update_dav_status(self, pg, dev_status_id, parms):
        pass
        sqlcmd = """
            UPDATE hmi.dev_status
            SET status=%s, category=%s, dev_major_category=%s
            WHERE dev_status_id = %s
        """
        pg.execute(sqlcmd, tuple(parms) + (dev_status_id, ))

    def get_dev_status_by_id(self, pg, dev_status_id):
        sqlcmd = """
            SELECT status
          FROM hmi.dev_status where dev_status_id = %s 
        """
        pg.execute(sqlcmd, (dev_status_id, ))
        row = pg.fetchone()
        if row:
            return row[0]  # 返回状态
        else:
            return None

    def select_dev_status(self, pg, status):  #  检查状态是否存在
        sqlcmd = """
            SELECT dev_status_id, status
          FROM hmi.dev_status where status = %s 
        """
        pg.execute(sqlcmd, (status,))
        row = pg.fetchone()
        if row:
            return row[0]  # 返回状态id
        else:
            return None

    def update_dev_status(self, req_json):
        status_list = req_json.get('status_list')
        self._pg.connect()
        for status_dict in status_list:
            dev_status_id = status_dict.get('status_id')
            detail_list = status_dict.get('detail')
            update_data = [status_dict.get('status'), status_dict.get('category'),
                           status_dict.get('dev_major_category')]
            self._update_dav_status(self._pg, dev_status_id, update_data)
            self.delete_dev_status_detail(self._pg, dev_status_id)
            for detail_val in detail_list:
                self.insert_dev_status_detail(self._pg, dev_status_id, detail_val)
        self._pg.commit()
        self._pg.close()

    def insert_dev_status(self, pg, status, category, major_category):
        sqlcmd = """
            INSERT INTO hmi.dev_status(status, category, dev_major_category)
            VALUES (%s, %s, %s) returning dev_status_id
        """
        pg.execute(sqlcmd, (status, category, major_category))
        dev_status_id = self.fetch_id(pg)
        return dev_status_id

    def insert_dev_status_detail(self, pg, dev_status_id, detail_val):
        sqlcmd = """
            INSERT INTO hmi.dev_status_rel(
            dev_status_id, val)
            VALUES (%s, %s);
        """
        pg.execute(sqlcmd, (dev_status_id, detail_val))

    def delete_dev_status_detail(self, pg, dev_status_id):
        sqlcmd = """
            DELETE FROM hmi.dev_status_rel
            WHERE dev_status_id = %s
        """
        pg.execute(sqlcmd, (dev_status_id, ))

    def add_dev_status(self, req_json):
        self._pg.connect()
        status_list = req_json.get('status_list')
        for status_dict in status_list:
            status = status_dict.get('status')
            category = status_dict.get('category')
            major_category = status_dict.get('dev_major_category')
            detail_list = status_dict.get('detail')
            dev_status_id = self.insert_dev_status(self._pg, status, category, major_category)
            for detail_val in detail_list:
                self.insert_dev_status_detail(self._pg, dev_status_id, detail_val)
        self._pg.commit()
        self._pg.close()

    def hmi_full_content_post(self, hmi_list):
        commit_user_id = hmi_list[0].get("user_id")
        result = {"result": "NG", "error": ''}
        if not commit_user_id:
            print 'Modify User Id is None.'
            result["error"] = u'未指定提交者.'
            return result
        self._pg.connect()
        commit_list = []
        try:
            update_time = self.get_current_time()
            for hmi in hmi_list:
                status_id = self.select_dev_status(self._pg, hmi['dev_status'])
                hmi['dev_status'] = status_id
                curr_commit_list = self._common_add(self._pg, hmi)
                if curr_commit_list:
                    commit_list += curr_commit_list
            if commit_list:
                log_info = {'user_id': commit_user_id, "commit_list": commit_list}
                commit_log = HmiLog()
                log_commit_data = commit_list[0].get("data")
                log_commit_data["update_time"] = update_time
                flag, commit_id = commit_log.add_commit_log2(self._pg, log_info)
                if flag:
                    self._pg.commit()
                result["result"] = "OK"
        except Exception as e:
            print e
            result["error"] = str(e)
        finally:
            self._pg.close()
            return result


    def get_chargers(self):
        chargers = []
        for i_ch in self._get_col_distinct_vals("charger"):
            if i_ch:
                chargers.append(i_ch)
        return chargers

    def get_steps(self):
        steps = self._get_col_distinct_vals("step")
        return steps

    def _get_col_distinct_vals(self, col_name):
        sqlcmd = """
        SELECT distinct {col_name}
          FROM hmi.req
          order by {col_name}
        """.format(col_name=col_name)
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        vals = []
        for row in rows:
            val = row[0]
            vals.append(val)
        self._pg.close()
        return vals

    def parse_screen_id(self, screen_id_str):
        screen_id_list = []
        if screen_id_str and screen_id_str != '-':
            org_screen_id_list = screen_id_str.split('\n')
            for org_screen_id in org_screen_id_list:
                org_screen_id = org_screen_id.strip()
                if org_screen_id:
                    if org_screen_id in (u"ALL", u"All"):
                        screen_id_list.append(u"任意画面")
                        continue
                    # p = re.compile(r'\w{2}-\w{3}-\d{3,4}(-\w+){0,1}')
                    p = re.compile(r'\w+\d*(-\w*\d*)*')
                    temp_screen_id_list = []
                    for m in p.finditer(org_screen_id):
                        temp_screen_id_list.append(m.group())
                    if temp_screen_id_list:
                        screen_id_list += temp_screen_id_list
                    else:
                        if org_screen_id.find(u"任意画面") >=0:
                            screen_id_list.append(u"任意画面")
                        else:
                            print 'Error screen id: %s' % org_screen_id
        return list(set(screen_id_list))

    def select_hu_id_by_screen(self, pg, screen_id):
        sqlcmd = """
            select hu_id from hmi.req_screen_rel where screen_id = %s
        """
        hu_id_list = []
        pg.execute(sqlcmd, (screen_id,))
        rows = pg.fetchall()
        for row in rows:
            hu_id_list.append(row[0])
        return hu_id_list

    def delete_scree_by_hu_id(self, pg, hu_id):
        sqlcmd = """
            DELETE from hmi.req_screen_rel where hu_id = %s
        """
        pg.execute(sqlcmd, (hu_id, ))

    def insert_screen(self, pg, hu_id, screen_id_list):
        sqlcmd = """
            INSERT INTO hmi.req_screen_rel(hu_id, screen_id)
            VALUES (%s, %s)
        """
        for screen_id in screen_id_list:
            pg.execute(sqlcmd, (hu_id, screen_id))

    def select_hmi_screen(self, pg, screen_id):
        sqlcmd = """
            SELECT * from hmi.hmi_screen where screen_id = %s
        """
        pg.execute(sqlcmd, (screen_id,))
        rows = pg.fetchall()
        return rows

    def insert_hmi_screen(self, pg, screen_id):
        sqlcmd = """
            INSERT INTO hmi.hmi_screen(screen_id)
            VALUES (%s)
        """
        pg.execute(sqlcmd, (screen_id,))

    def update_screen_rel(self, pg, data, col_change_list, action):
        _id = data.get(self.id_col)
        if action == "add":
            hmi_ds_screen_id = data.get('hmi_ds_screen_id')
            screen_id_list = self.parse_screen_id(hmi_ds_screen_id)
            if screen_id_list:
                self.insert_screen(pg, _id, screen_id_list)
                for screen_id in screen_id_list:
                    rows = self.select_hmi_screen(pg, screen_id)
                    if not rows:
                        self.insert_hmi_screen(pg, screen_id)
        else:
            if 'hmi_ds_screen_id' in col_change_list:
                hmi_screen_id = data.get('hmi_ds_screen_id')
                screen_id_list = self.parse_screen_id(hmi_screen_id)
                if screen_id_list:
                    self.delete_scree_by_hu_id(pg, _id)
                    self.insert_screen(pg, _id, screen_id_list)
                    for screen_id in screen_id_list:
                        rows = self.select_hmi_screen(pg, screen_id)
                        if not rows:
                            self.insert_hmi_screen(pg, screen_id)

    def _status_log(self, pg, _id, old_status, new_status, update_time):
        sqlcmd = """
        INSERT INTO hmi.status_log(
                    hu_id, old_status, new_status, update_date)
            VALUES (%s, %s, %s, %s);
        """
        if not old_status:
            old_status = None
        pg.execute(sqlcmd, (_id, old_status, new_status, update_time))

    def backup_req(self):
        try:
            self._pg.connect()
            bakup_date = time.strftime("%Y-%m-%d")
            bakup_time = time.strftime("%Y-%m-%d %H:%M:%S")
            # bakup_date = '2018-03-20'
            # bakup_time = '2018-03-20'
            if self._has_been_backup(self._pg, bakup_date):
                self._del_backup_by_date(self._pg, bakup_date)
            bakup_data = self.get_hmi_all(self._pg)
            col_list = self.attr_list
            col_list.append('backup_date')
            col_list.append('bakup_time')
            sqlcmd = self.list_2_insert_sql(self.bakup_table_name, col_list, self.key_col)
            for one_data in bakup_data:
                one_data['backup_date'] = bakup_date
                one_data['bakup_time'] = bakup_time
                params = self.get_params(one_data, col_list)
                self._pg.execute(sqlcmd, params)
            self._pg.commit()
        except Exception as e:
            print str(e)
        finally:
            self._pg.close()

    def _has_been_backup(self, pg, date):
        sqlcmd = """
        SELECT COUNT(*)
          FROM (
            SELECT distinct backup_date, bakup_time
              FROM hmi.req_history
              where backup_date = %s
          ) AS A
        """
        pg.execute(sqlcmd, [date])
        row = pg.fetchone()
        if row:
            if row[0] > 0:
                return True
        return False

    def _del_backup_by_date(self, pg, date):
        sqlcmd = """
        DELETE FROM hmi.req_history
           WHERE backup_date = %s;
        """
        pg.execute(sqlcmd, [date])


def main():
    obj = HmiReq()
    obj.backup_req()

#     detail_data_list = obj.get_old_data(obj._pg, '30.20.20.2.0.1.0')
#     result = obj.parse_screen_id(r"""USBV002
# USBV001
# """)
#     print result
#     result = obj.parse_screen_id(r"""USBV0001-00
#     """)
#     print result
#     result = obj.parse_screen_id(r"""RAD-JP001-01""")
#     print result
#     result = obj.parse_screen_id(r"""HF-MSG-010-A""")
#     print result
#     result = obj.parse_screen_id(r"""DVV006、DVD009""")
#     print result
#     result = obj.parse_screen_id(r"""遷移元：ONS-SLIB-004
#     遷移先：SLIB006
#     """)
#     print result


    # result = obj.get_category_tree()
    # result1 = obj.summary_category(condition_data='HF')
    # result2 = obj.get_detail_by_hu_id(hu_id='40.2.2.4.6.1.0')
    # obj._pg.connect()
    # id = obj.select_dev_status(obj._pg, '效确NG')
    # obj._pg.close()
    # result2[0]['dev_status'] = id
    # result2[0]['user_id'] = 310
    # result2[0]['hmi_ds_screen_id'] = "HF-SET-028\nHF-SET-030"
    # result = obj.hmi_full_content_post(result2)
    # print result
    # return result
    # obj.fist_add_hmi_screen()


if __name__ == '__main__':
    import sys, os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()
