# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase


class HmiScreenIt(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'hmi_screen_it'
        self.key_col = 'it_rc_id'
        self.id_col = 'screen_key'
        self.attr_list = ["it_rc_id", "screen_key", "app_name", "first_layer",
                          "second_layer", "third_layer", "layer4", "layer5", "screen_id",
                          "charger", "in_migration_id", "in_migration_date",
                          "followup_migration_id", "followup_migration_date", "test_docker", "remark"
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

    def get_dev_status(self, classify):
        if classify == 'followup_screen':
            table_name = 'hmi_screen_it_followup_status'
        else:
            table_name = 'hmi_screen_it_status'
        sqlcmd = """
            SELECT distinct dev_status_id, status, category
          FROM hmi.{table_name}
          order by dev_status_id
        """.format(table_name=table_name)
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
        if classify == 'followup_screen':
            table_name = 'hmi_screen_it_followup_status'
        else:
            table_name = 'hmi_screen_it_status'
        sqlcmd = """
            INSERT INTO hmi.{table_name}(status, category)
            VALUES (%s, %s)
        """.format(table_name=table_name)
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
        if classify == 'followup_screen':
            table_name = 'hmi_screen_it_followup_status'
        else:
            table_name = 'hmi_screen_it_status'
        sqlcmd = """
            UPDATE hmi.{table_name}
            SET status=%s, category=%s
            WHERE dev_status_id = %s
        """.format(table_name=table_name)
        pg.execute(sqlcmd, tuple(parms) + (dev_status_id, ))



def main():
     obj = HmiScreenIt()
     # condition_data = {'page': 1, 'size': 100}
     # rowcount, rows = obj.summary(condition_data)
     # print rowcount
     data = obj.get_dev_status('screen')
     print 'finish'


if __name__ == '__main__':
    import sys, os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()

