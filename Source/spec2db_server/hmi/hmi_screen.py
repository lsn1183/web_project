# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase


class HmiScreen(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'hmi_screen'
        self.key_col = 'screen_rc_id'
        self.id_col = 'screen_id'
        self.attr_list = ["screen_rc_id", "screen_id", "screen_progress",
                          "external_qa", "remark", "is_enter_screen"
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





def main():
     obj = HmiScreen()
     condition_data = {'page': 1, 'size': 100}
     rowcount, rows = obj.summary(condition_data)
     print rowcount


if __name__ == '__main__':
    import sys, os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()

