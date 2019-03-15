# -*- coding: UTF-8 -*-
from arl_base import ServiceBase
from openpyxl import Workbook
from commit_log import CommitLog
from tabulate import tabulate
import os
import zipfile
import shutil
import time


class ExportCkecklist(ServiceBase):

    def __int__(self):
        ServiceBase.__init__(self)

    def write_to_xls(self, _sheet, lines_data):
        for line in lines_data:
            _sheet.append(line)

    def export_excel(self, start_time, end_time):
        wb = Workbook()
        ws = wb.active
        log = CommitLog()
        self._pg.connect()
        check_list_data = log.get_checklist_brief(self._pg, start_time, end_time)
        start_time = start_time.replace('-', '')
        end_time = end_time.replace('-', '')
        file_name = start_time.split(' ')[0]+'-'+end_time.split(' ')[0]
        path = os.path.join('./ChecklistFile/', file_name)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            cmd = 'rm -rf %s' % path
            os.system(cmd)
            os.makedirs(path)
        line_datas = [['类型', 'ID', '担当确认履历ID', '组长确认履历ID', '差分'],]
        all_commit_ids = []
        for data in check_list_data:
            line_data = []
            classify = data.get('table_name')
            id = data.get('id')
            action_type = data.get('action_type')
            author_check_results = data.get('author_check_results')
            charger_check_results = data.get('charger_check_results')
            commit_ids = data.get('commit_ids')
            author_commit_ids, charger_commit_ids = self.diff_commit_id(author_check_results, charger_check_results,
                                                                        commit_ids)
            if author_commit_ids or charger_commit_ids:
                self.check_txt(author_commit_ids, charger_commit_ids, path, all_commit_ids)
                all_commit_ids += commit_ids
                diff_data = data.get('diff_data')
                data_list = self.diff_data_list(diff_data, action_type)
                line_data.append(classify)
                line_data.append(id)
                line_data.append(author_commit_ids)
                line_data.append(charger_commit_ids)
                if data_list:
                    line_data += data_list
                    line_datas.append(line_data)

        self.write_to_xls(ws, line_datas)
        self._pg.close()
        wb.save(os.path.join(path, 'checklist.xlsx'))
        zip_Name = file_name+'.zip'
        try:
            import zlib
            compression = zipfile.ZIPZIP_DEFLATED
        except:
            compression = zipfile.ZIP_STORED
        start = path.rfind(os.sep) + 1
        z = zipfile.ZipFile(zip_Name, mode="w", compression=compression)
        try:
            for dirpath, dirs, files in os.walk(path):
                for file in files:
                    # print file
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

    def diff_commit_id(self, author_check_results, charger_check_results, commit_ids):
        author_commit = ''
        charger_commit = ''
        for i in range(len(commit_ids)):
            commit_id = commit_ids[i]
            if author_check_results[i]:
                author_commit += str(commit_id)+'/'
            elif charger_check_results[i]:
                charger_commit += str(commit_id)+'/'
        return author_commit, charger_commit

    def diff_data_list(self, diff_data, action_type):
        data_list = []
        if action_type == 'change':
            model_list = diff_data.get('model_list')
            if model_list:
                for model in model_list:
                    mo = model.get('model')
                    category = model.get('category')
                    title = model.get('title')
                    name = model.get('name')
                    if not title:
                        title = ''
                    old_val = str(model.get('old_val'))
                    val = str(model.get('val'))
                    title_name = ''
                    if mo:
                        for m in mo:
                            if m:
                                title_name += str(m)
                    else:
                        title_name = str(category) + '->' + str(name) + '->' + str(title)
                    data = "标题：" + title_name + '\n' + "旧值：" + old_val + '\n' + "新值：" + val
                    data_list.append(data)
            for key in diff_data:
                if key in ('id', 'model_list'):
                    continue
                title = str(diff_data[key].get('title'))
                old_val = str(diff_data[key].get('old_val'))
                val = str(diff_data[key].get('val'))
                data = "标题："+ title + '\n' + "旧值："+old_val+'\n'+"新值："+val
                data_list.append(data)
        elif action_type == 'add':
            data_list = ['新增']
        else:
            data_list = ['删除']
        return data_list

    def check_txt(self, author_commit_ids, charger_commit_ids, path, all_commit_ids):
        if author_commit_ids:
            comit_ids = author_commit_ids.split('/')
            for commit_id in comit_ids:
                if commit_id:
                    if int(commit_id) in all_commit_ids:
                        continue
                    check_type = '担当'
                    self.write_to_txt(int(commit_id), check_type, path)
        if charger_commit_ids:
            comit_ids = charger_commit_ids.split('/')
            for commit_id in comit_ids:
                if commit_id:
                    if int(commit_id) in all_commit_ids:
                        continue
                    check_type = '组长'
                    self.write_to_txt(int(commit_id), check_type, path)

    def write_to_txt(self, commit_id, check_type, path):
        log = CommitLog()
        commit_data = log.get_cimmit_log_by_id(commit_id)
        rows = self.get_check_list(commit_id)
        title = "检查项目"+ (150-len("检查项目"))*" "
        headers = [title, "结果"]
        table = []
        for row in rows:
            table_row = []
            if row[1]:
                check_flag = str(row[1])
            else:
                check_flag = str(row[2])
            table_row.append(row[0].decode('utf8'))
            table_row.append(check_flag.decode('utf8'))
            table.append(table_row)
        check_table = tabulate(table, headers, tablefmt="grid")
        txtName = os.path.join(path, str(commit_id) + '.txt')
        with open(txtName, 'w') as f:
            f.write('角色：'+check_type+'\n')
            f.write('上传人：' + commit_data.get('user_name')+'\n')
            f.write('组名：' + str(commit_data.get('group_name'))+'\n')
            f.write('上传时间：' + commit_data.get('commit_time')+'\n')
            f.write(check_table)

    def get_check_list(self, commit_id):
        sqlcmd = """
        SELECT check_subject, author_check, charger_check FROM spec.check_list as t1 
        left join spec.check_list_item as t2 on t1.cl_item_id = t2.check_item_id
        where commit_id = %s
        """
        self._pg.execute(sqlcmd, (commit_id,))
        rows = self._pg.fetchall()
        return rows


def main():
    import os
    os.chdir('../')
    check = ExportCkecklist()
    # result = log.get_commit_log_detail(96, commit_log_ref_id=0)
    start_time, end_time = '2018-01-18 23:59:59', '2018-01-24 23:59:59'
    check.export_excel(start_time, end_time)



if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()

