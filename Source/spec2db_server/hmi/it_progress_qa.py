from Source.spec2db_server.hmi.hmi_base import HMIBase
import re

class ItProgressQA(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'it_progress_qa'
        self.key_col = 'gid'
        self.id_col = 'qa_id'
        self.attr_list = ['gid', 'qa_id', 'follow', 'status', 'priority',
                          'req_id', 'subject', 'author', 'update_date', 'jira_id']

    def get_old_data(self, pg, id_val):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, (str(id_val),))
        row = pg.fetchone()
        detail_data_list = []
        if row:
            detail_data_list.append(dict(zip(self.attr_list, row)))
        return detail_data_list

    def get_req_id(self, s):
        p = re.compile(r'[\d+.]+\d+')
        d = re.compile(r'HMIMMDEV-\d+')
        m = p.search(s)
        jira_id_list = d.findall(s)
        if m:
            req_id = m.group(0)
        else:
            req_id = ''
        return req_id, jira_id_list