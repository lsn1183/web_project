# -*- coding: UTF-8 -*-
from testmanage.models import *
from django.db import transaction


class Keyword():
    def get_keyword_list(self):
        Key = KeywordInfo.objects.all().order_by("keyword")
        result = []
        for i_cat in Key:
            result.append({
                "id": i_cat.id,
                "name": i_cat.keyword,
            })
        return result

    def add_keyword(self, json):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            if not KeywordInfo.objects.filter(keyword=json["name"]):
                ChangeData = KeywordInfo(keyword=json["name"])
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "此关键字已存在"
        return data

    def change_keyword(self, json, _id):
        data = {"resilt": '', "error": ''}
        with transaction.atomic():
            if KeywordInfo.objects.filter(pk=_id):
                ChangeData = KeywordInfo.objects.get(pk=_id)
                ChangeData.keyword = json["name"]
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "未找到此数据"
        return data

    def delete_keyword(self, _id):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            if KeywordInfo.objects.filter(pk=_id):
                ChangeData = KeywordInfo.objects.get(pk=_id)
                ChangeData.delete()
                if not ChangeData.id:
                    data["result"] = "OK"
            else:
                data["error"] = "未找到此数据"
        return data


    def link_option_type(self, data):
        keyword = "keyword"
        contains = "__icontains"
        se_list = []

        for i_da in data:
            con = ""
            reback = ""
            if i_da.get("type") == "keyword":
                con = "{}".format(keyword)
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


    def search_keword(self, json):
        list = []
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = KeywordInfo.objects.all().order_by("keyword")
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
            list = self.get_keyword_list()
        return list


    def data_to_json(self, data):
        search_list = []

        for i_data in data:
            search_list.append({
                "id": i_data.id,
                "name": i_data.keyword,
            })
        return search_list

    def batch_delete(self, json):
        data = {"error": '', "result": ''}
        with transaction.atomic():
            if json["dellist"]:
                for i_data in json["dellist"]:
                    ChangeData = KeywordInfo.objects.get(pk=i_data)
                    ChangeData.delete()
                    data["result"] = "DELETE OK"
            else:
                data["error"] = "请不要传空数据"
        return data
