# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase
import time


class HmiItProgressReport(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'it_progress_report'
        self.bakup_table_name = 'it_progress_report_history'
        self.key_col = 'git'
        self.id_col = 'req_id'
        self.attr_list = ["git", "step", "remark", "it_group", "gl", "author", "plan_date", "progress_code", "progress_ut",
                          "progress_it", "progress_risk", "comment", "cate_alias", "represent_req", "req_id", "jira_id",
                          "qa_id", "release_ver", "major_category", "medium_category", "small_category", "major", "small",
                          "status", "trigger", "action", "check_status", "trans_status", "trans_trigger", "trans_action",
                          "trans_explain", "progress_status", "author_is_me", "is_same_it", "is_make", "is_have_qa",
                          "dev_update_date", "dev_represent",
                          "dev_fw16_status", "dev_s_date1", "dev_model_status", "dev_s_date2", "dev_ut_status", "dev_s_date3",
                          "dev_it_status", "dev_s_date4", "dev_itn_status", "dev_s_date5", "dev_commit_id", "dev_s_date6",
                          "atsah_path", "ut_path", "it_path", "analysis_path",
                          "dev_status", "dev_remark", "dev_qaid", "dev_qa_status", "unit1", "usercase1", "testcase1",
                          "ut_status1", "ut_no1", "unit2", "usercase2", "testcase2", "ut_status2", "ut_no2", "unit3",
                          "usercase3", "testcase3", "ut_status3", "ut_no3", "unit4", "usercase4", "testcase4", "ut_status4",
                          "ut_no4", "unit5", "usercase5", "testcase5", "ut_status5", "ut_no5", "unit6", "usercase6",
                          "testcase6", "ut_status6", "ut_no6", "unit7", "usercase7", "testcase7", "ut_status7", "ut_no7",
                          "unit8", "usercase8", "testcase8", "ut_status8", "ut_no8", "unit9", "usercase9", "testcase9",
                          "ut_status9", "ut_no9", "unit10", "usercase10", "testcase10", "ut_status10", "ut_no10"
                          ]

    def summary(self, condition_data=None):
        size = condition_data.get('size')
        page = condition_data.get('page')
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [], [self.id_col])
        self._pg.connect()
        screen_list = []
        try:
            rowcount, rows = self._fetch_many(self._pg, sqlcmd, [], size, page)
            for row in rows:
                data = dict()
                for i, val in enumerate(row):
                    data[self.attr_list[i]] = val
                screen_list.append(data)
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return rowcount, screen_list

    def get_authors(self):
        authors = []
        for author in self._get_col_distinct_vals("author"):
            if author:
                authors.append(author)
        return authors

    def _get_col_distinct_vals(self, col_name):
        sqlcmd = """
        SELECT distinct {col_name}
          FROM hmi.{table}
          order by {col_name}
        """.format(col_name=col_name, table=self.table_name)
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        vals = []
        for row in rows:
            val = row[0]
            vals.append(val)
        self._pg.close()
        return vals

    def get_by_id(self, screen_id):
        self._pg.connect()
        data = dict()
        try:
            data = self._get_by_id(screen_id)
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return data

    def _get_by_id(self, pg, screen_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, (screen_id,))
        row = pg.fetchone()
        data = dict()
        if row:
            for i, val in enumerate(row):
                data[self.attr_list[i]] = val
        return data

    def get_old_data(self, pg, screen_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, (screen_id,))
        row = pg.fetchone()
        detail_data_list = []
        if row:
            detail_data_list.append(dict(zip(self.attr_list, row)))

        return detail_data_list

    def backup_It_Progress(self):
        try:
            self._pg.connect()
            bakup_date = time.strftime("%Y-%m-%d")
            bakup_time = time.strftime("%Y-%m-%d %H:%M:%S")
            # bakup_date = '2018-03-27'
            # bakup_time = '2018-03-27'
            if self._has_been_backup(self._pg, bakup_date):
                self._del_backup_by_date(self._pg, bakup_date)
            bakup_data = self.get_ItProgress_all(self._pg)
            col_list = self.attr_list
            col_list.append('backup_date')
            col_list.append('backup_time')
            sqlcmd = self.list_2_insert_sql(self.bakup_table_name, col_list, self.key_col)
            for one_data in bakup_data:
                one_data['backup_date'] = bakup_date
                one_data['backup_time'] = bakup_time
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
            SELECT distinct backup_date, backup_time
              FROM hmi.it_progress_report_history
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
        DELETE FROM hmi.it_progress_report_history
           WHERE backup_date = %s;
        """
        pg.execute(sqlcmd, [date])

    def get_ItProgress_all(self, pg):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [])
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        detail_data_list = []
        for row in rows:
            detail_data_list.append(dict(zip(self.attr_list, row)))
        return detail_data_list

    def get_dev_status(self, classify):
        if classify == 'it_dev':
            sqlcmd = """
                SELECT distinct dev_status_id, dev_status, category
              FROM hmi.it_dev_status
              order by dev_status_id
            """
        else:
            sqlcmd = """
                SELECT distinct process_status_id, process_status, category
              FROM hmi.it_process_status
              order by process_status_id
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
            dev_status.append(status)
        self._pg.close()
        return dev_status

    def add_dev_status(self, req_json):
        classify = req_json.get('classify')
        status_list = req_json.get('status_list')
        self._pg.connect()
        for status_dict in status_list:
            status = status_dict.get('status')
            category = status_dict.get('category')
            self.insert_dev_status(self._pg, status, category, classify)
        self._pg.commit()
        self._pg.close()

    def insert_dev_status(self, pg, status, category, classify):
        if classify == 'it_dev':
            sqlcmd = """
                INSERT INTO hmi.it_dev_status(dev_status, category)
                VALUES (%s, %s)
            """
            pg.execute(sqlcmd, (status, category))
        else:
            sqlcmd = """
                INSERT INTO hmi.it_process_status(process_status, category)
                VALUES (%s, %s)
            """
            pg.execute(sqlcmd, (status, category))

    def update_dev_status(self, req_json):
        classify = req_json.get('classify')
        status_list = req_json.get('status_list')
        self._pg.connect()
        for status_dict in status_list:
            dev_status_id = status_dict.get('status_id')
            update_data = [status_dict.get('status'), status_dict.get('category')]
            self._update_dav_status(self._pg, dev_status_id, update_data, classify)
        self._pg.commit()
        self._pg.close()

    def _update_dav_status(self, pg, dev_status_id, parms, classify):
        if classify == 'it_dev':
            sqlcmd = """
                UPDATE hmi.it_dev_status
                SET dev_status=%s, category=%s
                WHERE dev_status_id = %s
            """
            pg.execute(sqlcmd, tuple(parms) + (dev_status_id,))
        else:
            sqlcmd = """
                UPDATE hmi.it_process_status
                SET process_status=%s, category=%s
                WHERE process_status_id = %s
            """
            pg.execute(sqlcmd, tuple(parms) + (dev_status_id, ))

    def author_update_time(self, update_time_date):
        self._pg.connect()
        for data in update_time_date:
            author = data.get('author')
            date_time = data.get('date_time')
            update_time = data.get('update_time')
            self._author_update_time(self._pg, author, date_time, update_time)
        self._pg.commit()

    def _author_update_time(self, pg, author, date_time, update_time):
        sqlcmd = """
            UPDATE hmi.it_update_date
            SET update_time=%s
            WHERE author = %s and date_time = %s
        """
        pg.execute(sqlcmd, (update_time, author, date_time))


def main():
     obj = HmiItProgressReport()
     # condition_data = {'page': 1, 'size': 100}
     # rowcount, rows = obj.summary(condition_data)
     # print rowcount
     obj.backup_It_Progress()


if __name__ == '__main__':
    import sys, os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()

