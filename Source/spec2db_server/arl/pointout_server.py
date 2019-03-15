from Source.spec2db_server.arl.arl_base import ServiceBase


class PointOut(ServiceBase):
    """
    """
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "tmc_pointout_index"
        self.key_col = "pointout_rc_id"
        # self.classify = classify  # Hu / def / analysis
        self.attr_list = ["pointout_rc_id", "category", "small_category", "basic_req",
                          "folder", "new_date",
                          ]

    def delete_all(self, new_date):
        self._pg.connect()
        sqlcmd = """
                DELETE FROM spec.tmc_pointout_index WHERE new_date = %s
        """
        self._pg.execute(sqlcmd, (new_date,))
        self._pg.commit()
        self._pg.close()

    def get_date_info(self, point_date):
        self._pg.connect()
        sqlcmd = """
            SELECT category, small_category, basic_req, folder, new_date AS point_date FROM spec.tmc_pointout_index 
            WHERE new_date = %s
        """
        self._pg.execute(sqlcmd, (point_date,))
        row_keys = ["category", "small_category", "basic_req", "folder", "point_date"]

        ret_data_list = []
        for _row in self._pg.fetchall():
            ret_data_list.append(dict(zip(row_keys, _row)))
        self._pg.close()

        return ret_data_list