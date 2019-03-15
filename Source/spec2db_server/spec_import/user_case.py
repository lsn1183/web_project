import os
import csv
from Source.spec2db_server.arl.arl_base import ServiceBase


class UserCase(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)

    def parse_file(self, dir):
        file_list = []
        for dirpath, dirs, files in os.walk(dir):
            for file in files:
                base, ext = os.path.splitext(file)
                if ext in (".xlsx", ".ods"):
                    path = dirpath.replace(dir, '')
                    path = os.path.join(path, file)
                    file_list.append((path, base))
        # with open('user_case.csv', 'wb') as f:
        #     w = csv.writer(f, delimiter='\t')
        #     w.writerows(file_list)
        return file_list

    def store(self, file_list):
        self._pg.connect()
        sqlcmd = """
        delete from public.analysis_usercase_file;
        """
        self._pg.execute(sqlcmd)
        for file_info in file_list:
            self.insert(file_info)
        self._pg.commit()

    def insert(self, file_info):
        sqlcmd = """
        INSERT INTO public.analysis_usercase_file(
                    path, file_name)
            VALUES (%s, %s);
        """
        self._pg.execute(sqlcmd, file_info)


if __name__ == '__main__':
    import sys, os
    reload(sys)
    os.chdir('../')
    sys.setdefaultencoding('UTF-8')
    dir = r'C:\SpiderInput\Repository_0.1.5'
    uc = UserCase()
    file_list = uc.parse_file(dir)
    uc.store(file_list)
