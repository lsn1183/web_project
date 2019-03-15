# -*- coding: UTF-8 -*-
import os
# pythoncom.CoInitialize()
from app.db.utility import Utillity


class CtrlExcelHtm():
    def __init__(self):
        pass

    def convert_excel_htm(self, local_file_path, new_file_name, file_path):
        """保存，以htm后缀存取"""
        # from win32com.client import Dispatch
        from win32com.client import DispatchEx
        import pythoncom
        # from win32com.client import constants
        pythoncom.CoInitialize()
        xl = DispatchEx('Excel.Application')
        # xl = Dispatch('Excel.Application')
        xl.DisplayAlerts = False
        wb = xl.Workbooks.Open(local_file_path)
        # 创建新的文件夹用来装转后的htm文件(一个网页一个文件夹）
        uti = Utillity()
        only_id = uti.get_nextval()
        file_dir = os.path.join(file_path, str(only_id), os.path.splitext(new_file_name)[0])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        t_path = os.path.join(file_dir, os.path.splitext(new_file_name)[0])
        print(t_path)
        wb.SaveAs(t_path, FileFormat=44)  # 保存在Z盘 新文件夹下, constants.xlHtml==44
        # xl.Application.Run("SaveHTML")
        xl.Workbooks.Close()
        xl.Quit()
        del xl
        return file_dir

