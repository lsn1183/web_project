# -*- coding: UTF-8 -*-
from Source.spec2db_server.arl.arl_base import ServiceBase
from openpyxl import Workbook
import copy
import re
import json

class update_schedule(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)

    def find_schedule(self):
        sqlcmd = """
            SELECT arl_id, group_name, req_post
            FROM public.base_schedule
        """
        schedule_list = []

        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        if rows:
            for row in rows:
                schedule_dict = dict()
                schedule_dict['arl_id'] = row[0]
                schedule_dict['group_name'] = row[1]
                schedule_dict['req_post'] = row[2]
                schedule_list.append(schedule_dict)
        self._pg.close()
        return schedule_list

    def find_schedule_by_id(self, arl_id):
        sqlcmd = """
            SELECT arl_id, "group", req_post from spec.arl_schedule
            where arl_id = %s
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        self._pg.close()
        if row:
            return True
        else:
            return False

    def update_arl_schedule(self, schedule_dict):
        sqlcmd = """
            UPDATE spec.arl_schedule set "group" = %s, req_post = %s
            where arl_id = %s
        """
        arl_id = schedule_dict.get('arl_id')
        group = schedule_dict.get('group_name')
        req_post = schedule_dict.get('req_post')
        self._pg.connect()
        self._pg.execute(sqlcmd, (group, req_post, arl_id))
        self._pg.commit()
        self._pg.close()

    def add_arl_schedule(self, schedule_dict):
        sqlcmd = """
            INSERT INTO spec.arl_schedule(arl_id, req_post, "group", author, charger, hu_date, def_date, analysis_date)
            VALUES (%s, %s, %s, %s, %s, '-', '-', '-')
        """
        arl_id = schedule_dict.get('arl_id')
        group = schedule_dict.get('group_name')
        req_post = schedule_dict.get('req_post')
        user_name = self.find_charge_by_group(group)

        self._pg.connect()
        self._pg.execute(sqlcmd, (arl_id, req_post, group, user_name, user_name))
        self._pg.commit()
        self._pg.close()

    def find_charge_by_group(self, group_name):
        sqlcmd = """
            SELECT user_name From spec.arl_user t1  left join spec.arl_group_member t2
            on t1.user_id = t2.user_id left join spec.arl_group t3
            on t2.group_id = t3.group_id where t3.group_name = %s and t2.role = 1
        """
        if group_name == 'Media':
            user_name = 'wangsiyuan'
            return user_name
        self._pg.connect()
        self._pg.execute(sqlcmd, (group_name,))
        row = self._pg.fetchone()
        if not row:
            print group_name
        return row[0]



def main():
    ana_obj = update_schedule()
    schedule_list = ana_obj.find_schedule()
    for schedule in schedule_list:
        arl_id = schedule.get('arl_id')
        re = ana_obj.find_schedule_by_id(arl_id)
        if re:
            ana_obj.update_arl_schedule(schedule)
        else:
            ana_obj.add_arl_schedule(schedule)

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()