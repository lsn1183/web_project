# -*- coding: UTF-8 -*-
import os
import xlrd
import xlwt
import time
from testmanage.models import *
from django.db import transaction
from django.http import FileResponse


class Country():

    def get_country_list(self):
        countys = CountryInfo.objects.all().order_by("iso_code")
        data = []
        for i_cat in countys:
            data.append({
                "id": i_cat.id,
                "code": i_cat.iso_code,
                "en_name": i_cat.eng_name,
                "cn_name": i_cat.cn_name,
            })
        return data

    def add_country(self, json):
        data = {"error":'',"result":''}
        with transaction.atomic():
            if not CountryInfo.objects.filter(iso_code=json["code"]):
                ChangeData = CountryInfo(iso_code=json["code"],
                                         eng_name=json["en_name"],
                                         cn_name=json["cn_name"])
                ChangeData.save()
                data["result"] = ChangeData.id
            else:
                data["error"] = "该国家已存在"
        return data

    def change_country(self, json, _id):
        data = {"error": '', "result": ''}
        with transaction.atomic():
            if CountryInfo.objects.filter(pk=_id):
                ChangeData = CountryInfo.objects.get(pk=_id)
                ChangeData.iso_code = json["code"]
                ChangeData.eng_name = json["en_name"]
                ChangeData.cn_name = json["cn_name"]
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "无此国家信息"
        return data

    def delete_country(self, _id):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            if CountryInfo.objects.filter(pk=_id):
                ChangeData = CountryInfo.objects.get(pk=_id)
                ChangeData.delete()
                if not ChangeData.id:
                    data["result"] = "DELETE OK"
            else:
                data["error"] = "未找到此数据"
        return data

    def batch_delete(self, json):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            for i_data in json["dellist"]:
                if CountryInfo.objects.filter(pk=i_data):
                    ChangeData = CountryInfo.objects.get(pk=i_data)
                    ChangeData.delete()
                    if not ChangeData.id:
                        data["result"] = "DELETE OK"
                else:
                    data["error"] = "未找到此数据"
        return data

    def import_excle(self, file):
        data = {"result": '', "error": ''}
        file_name = file.name
        path = os.path.join('import')
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, file_name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        data_list = self.do_Import("import/" + file_name)
        with transaction.atomic():
            for item in data_list:
                if not CountryInfo.objects.filter(iso_code=item["code"]):
                    ImportData = CountryInfo(iso_code=item["code"], eng_name=item["en_name"], cn_name=item["cn_name"])
                    ImportData.save()
                    data["result"] = "OK"
                else:
                    data["error"] = "该数据已存在"

        return data

    def do_Import(self, xls_filename):
        book = xlrd.open_workbook(xls_filename)
        table = book.sheets()[0]
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        colnames = table.row_values(0)  # 某一行数据
        list = []
        for rownum in range(1, nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                list.append(app)
        return list

    def export_excle(self):
        path = os.path.join('Export')
        if not os.path.exists(path):
            os.makedirs(path)
        the_file_name = "Country_List.xls"
        countys = CountryInfo.objects.all().order_by("id")
        file = xlwt.Workbook(encoding='utf-8')
        ws = file.add_sheet('sheet1')
        ws.write(0, 0, 'code')
        ws.write(0, 1, 'en_name')
        ws.write(0, 2, 'cn_name')
        excel_row = 1
        for obj in countys:
            ws.write(excel_row, 0, obj.iso_code)
            ws.write(excel_row, 1, obj.eng_name)
            ws.write(excel_row, 2, obj.cn_name)
            excel_row = excel_row + 1
        file.save("Export/" + the_file_name)
        resp = FileResponse(open("./Export/" + the_file_name, "rb"))
        resp['Content-Type'] = 'application/vnd.ms-excel'
        resp['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        return resp

    def search_country(self, json):
        list = []
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = CountryInfo.objects.all().order_by("iso_code")
                for ida in search_list:
                    app = {}
                    if ida.get("is_equal"):
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.filter(**app)
                    else:
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.exclude(**app)
                list = self.data_to_json(SearchData)
        else:
            list = self.get_country_list()
        return list

    def link_option_type(self, data):
        code = "iso_code"
        en_name = "eng_name"
        cn_name = "cn_name"
        contains = "__icontains"
        se_list = []

        for i_da in data:
            con = ""
            reback = ""
            if i_da.get("type") == "code":
                con = "{}".format(code)
                if i_da.get("option") == "不等于":
                    reback = False
                    con = '{}'.format(con)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "等于":
                    reback = True
                    con = '{}'.format(con)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "包含":
                    reback = True
                    con = '{}{}'.format(con, contains)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "不包含":
                    reback = False
                    con = '{}{}'.format(con, contains)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
            elif i_da.get("type") == "en_name":
                con = "{}".format(en_name)
                if i_da.get("option") == "不等于":
                    reback = False
                    con = '{}'.format(con)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "等于":
                    reback = True
                    con = '{}'.format(con)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "包含":
                    reback = True
                    con = '{}{}'.format(con, contains)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "不包含":
                    reback = False
                    con = '{}{}'.format(con, contains)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
            elif i_da.get("type") == "cn_name":
                con = "{}".format(cn_name)
                if i_da.get("option") == "不等于":
                    reback = False
                    con = '{}'.format(con)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "等于":
                    reback = True
                    con = '{}'.format(con)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "包含":
                    reback = True
                    con = '{}{}'.format(con, contains)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "不包含":
                    reback = False
                    con = '{}{}'.format(con, contains)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
            else:
                se_list = ""
        return se_list

    def data_to_json(self,data):
        search_list = []
        for i_data in data:
            search_list.append({
                "id": i_data.id,
                "code": i_data.iso_code,
                "en_name": i_data.eng_name,
                "cn_name": i_data.cn_name,
            })
        return search_list
