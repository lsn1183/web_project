# -*- coding: UTF-8 -*-
from Source.xls2db.common.db import pg
import json
import sys
class PaarsedContent(object):

    def __init__(self):
        self._pg = pg()

    def select_table(self, pg2):
        sqlcmd = """
            SELECT func_id, func_content
        FROM spec.spec_functions
        """
        pg2.execute2(sqlcmd)
        rows = pg2.fetchall2()
        data_list = []
        for row in rows:
            data_dict = dict()
            data_dict['func_id'] = row[0]
            data_dict['func_content'] = row[1]
            data_list.append(data_dict)
        return data_list

    def load_json(self, pg2, data_list):
        for data in data_list:
            func_id = data.get('func_id')
            try:
                func_content = data.get('func_content')
                if func_content != '' and data != None:
                    content_list = json.loads(func_content)
                else:
                    continue
            except:
                print data.get('func_content')
                print func_id
            parsed_content_list = []
            if func_id == 1995:
                pass
            for con_list in content_list:
                for con in con_list:
                    if isinstance(con, (list,)):
                        for c in con:
                            parsed_content_list.append(''.join(c.get('dataValue')))
                        continue
                    parsed_content_list.append(''.join(con.get('dataValue')))
            parsed_content = ' '.join(parsed_content_list)
            self.update_function(pg2, func_id, parsed_content)
        pg2.commit2()
        pg2.close2()


    def update_function(self, pg2, func_id, parsed_content):
        sqlcmd = '''
            update spec.spec_functions set parsed_content = %s
            where func_id = %s
        '''
        pg2.execute2(sqlcmd, (parsed_content, func_id))


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    obj = PaarsedContent()
    obj._pg.connect2()
    data_list = obj.select_table(obj._pg)
    obj.load_json(obj._pg, data_list)





