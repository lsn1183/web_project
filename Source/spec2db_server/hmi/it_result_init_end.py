# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase


class ItResultInitEnd(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'it_result_init_end'
        self.key_col = 'gid'
        self.id_col = 'it_key'
        self.attr_list = [
            'gid', 'file_name', 'it_no', 'category', 'inteface', 'if_process_content',
            'mc_process_content', 'uac_interface', 'uac_process_content', 'uac_nofity_no',
            'sb_inteface', 'sb_process_content', 'sb_nofity_no', 'sb_uac_callback', 'rel_service',
            'test_item', 'remark', 'obstacle_id', 'it_key'
        ]

    def get_old_data(self, pg, screen_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, (screen_id,))
        row = pg.fetchone()
        detail_data_list = []
        if row:
            detail_data_list.append(dict(zip(self.attr_list, row)))
        return detail_data_list


