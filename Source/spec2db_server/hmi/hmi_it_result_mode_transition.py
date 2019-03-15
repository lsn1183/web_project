# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase


class HimItResultModeTransition(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'it_result_mode_transition'
        self.key_col = 'gid'
        self.id_col = 'it_key'
        self.attr_list = ["gid", "file_name", "it_no",
                          "mode_name", "category", "video_content_callback", "video_process_callback",
                          "audio_content_callback", "audio_process_callback", "event_trigger", "action",
                          "action_process", "test_item", "remark", "obstacle_id", "it_key"
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
     obj = HimItResultModeTransition()
     condition_data = {'page': 1, 'size': 100}
     rowcount, rows = obj.summary(condition_data)
     print rowcount


if __name__ == '__main__':
    import sys, os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()

