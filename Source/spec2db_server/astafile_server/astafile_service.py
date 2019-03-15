# -*- coding: UTF-8 -*-
from Source.spec2db_server.arl.arl_base import ServiceBase
import os
import shutil
import zipfile

class AstaFileRecord(ServiceBase):

    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "arl_file"
        self.key_col = "record_id"

    def astah_to_txt(self, file_url):
        path = os.path.join(file_url)
        cmd = '''java -jar tools/AstaToTxt/AstaToTxt_fat.jar %s''' % \
            (path,)
        print cmd
        os_ret = os.system(cmd)
        if os_ret != 0:
            return "NG"
        return "OK"

    def import_file(self, user_id, group_id, fileName, file_url, create_time):
        res = {"result": "NG"}
        ret = self.astah_to_txt(file_url)
        if ret == 'OK':
            try:
                self._pg.connect()
                file_path = file_url.replace(fileName, 'SequencDiagram.txt')
                sequence_list = self.load_seq2actor_from_file(file_path)
                rc_id = self._import_file(user_id, group_id, fileName, file_url, create_time, self._pg)
                if sequence_list:
                    for sequence in sequence_list:
                        self._import_file_seq(rc_id, sequence, self._pg)
                self._pg.commit()
                self._pg.close()
                res["result"] = "OK"
            except Exception as e:
                print e.message
                res["error"] = e.message
        else:
            res["error"] = "文件解析失败！"
        return res

    def _import_file_seq(self, rc_id, sequence, pg):
        sqlcmd = """
            INSERT INTO spec.arl_file_seq(file_rc_id, seq_diagram) values(%s, %s)
        """
        pg.execute(sqlcmd, (rc_id, sequence))

    def _import_file(self, user_id, group_id, fileName, file_url, create_time, pg):
        sqlcmd = """
            INSERT INTO spec.arl_file(user_id, group_id, file_name, file_url, create_time) values(%s, %s, %s, %s, %s) 
            returning record_id 
        """
        pg.execute(sqlcmd, (user_id, group_id, fileName, file_url, create_time))
        rc_id = self.fetch_id(pg)
        return rc_id

    def load_seq2actor_from_file(self, file_path):
        if not os.path.exists(file_path):
            return []
        file = open(file_path, 'r')
        seq_list = []
        for line in file:
            try:
                line_data = line.decode("utf8")
            except:
                line_data = line.decode("gbk")
            if not line:
                break
            line_data = line_data.replace('\n', '')
            line_data = line_data.replace('\r', '')
            seq_list.append(line_data)
        return seq_list

    def get_file_list(self, group_id):
        result = {"result": "OK"}
        sqlcmd = """
            SELECT record_id, user_name, group_name, file_name, file_url, create_time
            FROM spec.arl_file as t1 left join spec.arl_user as t2 on t1.user_id = t2.user_id
            LEFT JOIN spec.arl_group as t3 ON t1.group_id = t3.group_id
            WHERE t1.group_id = %s order by create_time desc
        """
        col_list = ['record_id', 'user_name', 'group_name', 'file_name', 'file_url', 'create_time']
        self._pg.connect()
        self._pg.execute(sqlcmd, (group_id,))
        rows = self._pg.fetchall()
        file_list = []
        if rows:
            for row in rows:
                file_dict = dict()
                for i in range(len(row)):
                    file_dict[col_list[i]] = row[i]
                file_list.append(file_dict)
        result["data"] = file_list
        return result

    def get_file_by_id(self, record_id):
        sqlcmd = """
                   SELECT file_name, file_url
                   FROM spec.arl_file WHERE record_id = %s
               """
        self._pg.connect()
        self._pg.execute(sqlcmd, (record_id,))
        row = self._pg.fetchone()
        file_name = row[0]
        file_url = row[1]
        return file_name, file_url

    def delete_file(self, record_id):
        data = self._delete_file_by_id(record_id)
        return data

    def _delete_file_by_id(self, record_id):
        result = {"result": "NG"}
        sqlcmd1 = """
            DELETE FROM spec.arl_file_seq WHERE file_rc_id = %s
        """
        sqlcmd2 = """
            DELETE FROM spec.arl_file WHERE record_id = %s
        """
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd1, (record_id,))
            self._pg.execute(sqlcmd2, (record_id,))
            self._pg.commit()
            self._pg.close()
            result["result"] = "OK"
        except Exception as e:
            self._pg.close()
            print e.message
        return result

    def get_file_to_git(self):
        file_list = self._get_groups_file()
        path = os.path.join('./astafile/', "Astah")
        try:
            if not os.path.exists(path):
                os.mkdir(path)
            for file in file_list:
                shutil.copy(file, path)  # 复制文件
        except:
            print "路径错误！"
            return
        return path

    def get_zipfile(self):
        file_list = self._get_groups_file()
        try:
            import zlib
            compression = zipfile.ZIPZIP_DEFLATED
        except:
            compression = zipfile.ZIP_STORED
        path = os.path.join('./astafile/', "AllGroupAstah")
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            cmd = 'rm -rf %s' % path
            os.system(cmd)
            os.mkdir(path)
        for file in file_list:
            shutil.copy(file, path)  # 复制文件
        start = path.rfind(os.sep)+1
        zip_Name = 'AllGroupAstah.zip'
        z = zipfile.ZipFile(zip_Name, mode="w", compression = compression)
        try:
            for dirpath, dirs, files in os.walk(path):
                for file in files:
                    if file.split('.')[-1] != "asta":
                        continue
                    print file
                    z_path = os.path.join(dirpath, file)
                    z.write(z_path, z_path[start:])
            z.close()
        except:
            if z:
                z.close()
        try:
            shutil.move("./"+zip_Name, path)
        except:
            os.remove(os.path.join(path, zip_Name))
            shutil.move("./" + zip_Name, path)
        return path, zip_Name

    def _get_groups_file(self):
        sqlcmd = """
            SELECT file_url FROM spec.arl_file as t1 LEFT JOIN 
            (SELECT group_id,max(create_time) as ct
            FROM spec.arl_file GROUP BY group_id)as t2 on t1.group_id = t2.group_id 
            WHERE t1.create_time = ct
        """
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        file_list = []
        if rows:
            for row in rows:
                file_list.append(row[0])
        return file_list

    def import_seq_diagram(self, file_url, fileName, rc_id):
        ret = self.astah_to_txt(file_url)
        if ret == 'OK':
            self._pg.connect()
            file_path = file_url.replace(fileName, 'SequencDiagram.txt')
            sequence_list = self.load_seq2actor_from_file(file_path)
            if sequence_list:
                for sequence in sequence_list:
                    self._import_file_seq(rc_id, sequence, self._pg)
            self._pg.commit()
            self._pg.close()


def main():
    import os
    os.chdir('../')
    obj = AstaFileRecord()

    file_url = '/home/pset/Downloads/TAGL_RequirementAnalysis_DCUUI.asta'
    fileName = 'TAGL_RequirementAnalysis_DCUUI.asta'
    rc_id = 35
    obj.import_seq_diagram(file_url, fileName, rc_id)


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()







