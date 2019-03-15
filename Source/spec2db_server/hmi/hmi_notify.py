# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase


class HmiNotify(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'it_result_notify'
        self.key_col = 'gid'
        self.id_col = 'it_key'
        self.attr_list = ["gid", "file_name", "it_no",
                          "category", "rel_screen_id", "rel_service",
                          "notify_interface", "notify_content", "notify_process",
                          "trigger", "action", "action_process", "uac_if", "uac_if_process",
                          "test_item", "remark", "obstacle_id", "it_key"
                          ]

    def get_old_data(self, pg, screen_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, (screen_id,))
        row = pg.fetchone()
        detail_data_list = []
        if row:
            detail_data_list.append(dict(zip(self.attr_list, row)))

        return detail_data_list



if __name__ == '__main__':
    import sys, os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    # main()

