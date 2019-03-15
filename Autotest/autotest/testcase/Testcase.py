# -*- coding: UTF-8 -*-
from testmanage.models import *
from testcase.models import *
import os
import xlrd
import xlwt
import datetime
import json
from django.db import transaction
from django.http import FileResponse
from diffTool.ctrl_base import CtrlBase


class Testcase(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.col_list = ['case_name', 'case_abstract', 'case_premise',
                         'case_importance', 'case_test_mode', 'charger',
                         ]
        self.key_col = 'id'

    def get_all_testcase_list(self, page, size):
        data = {"error":"","count":0}
        start = (page-1)*size
        first = TestcaseInfo.objects.all().order_by("case_name")
        third = []
        for scend in first:
            if TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version"):
                if not TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version")[0] in third:
                    third.append(TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version")[0])
                    data["count"] += 1
        end = min((page - 1) * size + size, data["count"])
        cases = third[start:end]
        data["result"] = []
        for i_case in cases:
            data["result"].append({
                "id":i_case.id,
                "module_id": i_case.case_model.id,
                "title": i_case.case_name,
                "abstract": i_case.case_abstract,
                "premise": i_case.case_premise,
                "charger": i_case.charger,
                "test_mode": i_case.case_test_mode,
                "version": i_case.case_version,
            })
        return data

    def get_testcase_list(self, p_id):
        data = {"error": "", "count": 0}
        first = TestcaseInfo.objects.filter(case_model__parent_proj=p_id).order_by("case_name")
        third = []
        for scend in first:
            if TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version"):
                if not TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version")[0] in third:
                    third.append(TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version")[0])
                    data["count"] += 1
        cases = third
        data["result"] = []
        for i_case in cases:
            version_list = []
            sc_list = TestcaseInfo.objects.filter(source_case_id=i_case.source_case_id)
            for sc in sc_list:
                version_list.append({
                    "id": sc.id,
                    "version": sc.case_version,
                    "source_id": sc.source_case_id,
                })
            data["result"].append({
                "id": i_case.id,
                "source_id": i_case.source_case_id,
                "module_id": i_case.case_model.id,
                "title": i_case.case_name,
                "abstract": i_case.case_abstract,
                "premise": i_case.case_premise,
                "charger": i_case.charger,
                "test_mode": i_case.case_test_mode,
                "version": i_case.case_version,
                "version_list": version_list,
            })
        return data

    def get_testcase_list_by_model(self, m_id, page, size):
        data = {"error":"","count":0}
        start = (page-1)*size
        first = TestcaseInfo.objects.filter(case_model=m_id).order_by("case_name")
        third = []
        for scend in first:
            if TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version"):
                if not (TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version")[0] in third):
                    third.append(TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version")[0])
                    data["count"]+=1
        end = min((page-1)*size+size, data["count"])
        cases = third[start:end]
        data["result"] = []
        for i_case in cases:
            data["result"].append({
                "id":i_case.id,
                "module_id": i_case.case_model.id,
                "title": i_case.case_name,
                "abstract": i_case.case_abstract,
                "premise": i_case.case_premise,
                "charger": i_case.charger,
                "test_mode": i_case.case_test_mode,
                "version": i_case.case_version,
            })
        return data

    def get_testcase_list_by_proj(self, p_id, page, size):
        data = {"error":"","count":0}
        start = (page-1)*size

        first = TestcaseInfo.objects.filter(case_model__parent_proj=p_id).order_by("case_name")
        third = []
        for scend in first:
            if TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version"):
                if not (TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version")[0] in third):
                    third.append(TestcaseInfo.objects.filter(source_case_id=scend.id).order_by("-case_version")[0])
                    data["count"] += 1
        end = min((page-1)*size+size, data["count"])
        cases = third[start:end]
        data["result"] = []
        for i_case in cases:
            data["result"].append({
                "id":i_case.id,
                "module_id": i_case.case_model.id,
                "title": i_case.case_name,
                "abstract": i_case.case_abstract,
                "premise": i_case.case_premise,
                "charger": i_case.charger,
                "test_mode": i_case.case_test_mode,
                "version": i_case.case_version,
            })
        return data

    def get_testcase_one(self, _id):
        data = {"error":""}
        if TestcaseInfo.objects.filter(pk=_id):
            cases = TestcaseInfo.objects.get(pk=_id)
            # fv = CaseFieldValue.objects.filter(case_id=_id)
            data["result"] = {}
            kd_lis = []
            dest_list = []
            field_value_list = []
            step_list = []
            if cases.case_field_value_list.all():
                fv = cases.case_field_value_list.all()
                for i_fv in fv:
                    if CaseFieldValue.objects.filter(case_id=_id, field=i_fv):
                        ffv = CaseFieldValue.objects.get(case_id=_id, field=i_fv)
                        field_value_list.append({
                            "case_id": _id,
                            "field_id": i_fv.id,
                            "field_value": ffv.field_value,
                        })
                    else:
                        field_value_list.append({
                            "case_id": _id,
                            "field_id": i_fv.id,
                            "field_value": "",
                        })
            if cases.case_keyword_list.all():
                cct = cases.case_keyword_list.all()
                for ct in cct:
                    kd_lis.append({
                        "id": ct.id,
                        "name": ct.keyword,
                    })
            if cases.case_dest_list.all():
                cct = cases.case_dest_list.all()
                for ct in cct:
                    dest_list.append({
                        "id": ct.id,
                        "name": ct.dest_showname,
                        "provider": ct.data_provider,
                        "introduce": ct.dest_introduce,
                    })
            if cases.case_step_list.all():
                cct = cases.case_step_list.all()
                for ct in cct:
                    step_list.append({
                        "id":ct.id,
                        "order":ct.order,
                        "operate":ct.operate,
                        "expected_value":ct.expected_value,
                        "is_automatically": ct.is_automatically,

                    })
            data["result"]={
                "id": cases.id,
                "source_case_id": cases.source_case_id,
                "title": cases.case_name,
                "abstract": cases.case_abstract,
                "premise": cases.case_premise,
                "charger": cases.charger,
                "user_name": cases.user_name,
                "case_version": cases.case_version,
                "importance": cases.case_importance,
                "test_mode": cases.case_test_mode,
                "case_model": cases.case_model.id,
                "keyword_list": kd_lis,
                "dest_list": dest_list,
                "field_value_list":field_value_list,
                "step_list":step_list,
            }
        else:
            data["error"] = "此用例未找到"
        return data


    def get_three_list(self, _id):
        model_data = ModelInfo.objects.filter(pk=_id)
        res = {"dest_list": [], "keyword_list": [], "field_list": [], "error": "没有这个模块"}
        if model_data:
            proj_data = ModelInfo.objects.get(pk=_id).parent_proj
            dest_list = []
            keyword_list = []
            field_list = []
            if proj_data.dest_list.all():
                for i_dest in proj_data.dest_list.all():
                    dest_list.append({
                        "id": i_dest.id,
                        "name": i_dest.dest_showname,
                        "provider": i_dest.data_provider,
                        "introduce": i_dest.dest_introduce,
                    })
            if proj_data.keyword_list.all():
                for i_kd in proj_data.keyword_list.all():
                    keyword_list.append({
                        "id": i_kd.id,
                        "name": i_kd.keyword,
                    })
            if model_data[0].field_list.filter(field_open_use='test_example'):
                for i_field in model_data[0].field_list.filter(field_open_use='test_example'):
                    op_list = []
                    if i_field.field_option_list.all():
                        opt = i_field.field_option_list.all()
                        for i_opt in opt:
                            op_list.append({'id': str(i_opt.id), 'label': i_opt.option_value})
                    if i_field.field_type == "multiSelect":
                        field_list.append({
                            "id": str(i_field.id),
                            "name": i_field.field_name,
                            "type": i_field.field_type,
                            "is_show": i_field.field_show_when_execute,
                            "option_list": op_list,
                            "field_value":[],
                        })
                    else:
                        field_list.append({
                            "id": str(i_field.id),
                            "name": i_field.field_name,
                            "type": i_field.field_type,
                            "is_show": i_field.field_show_when_execute,
                            "option_list": op_list,
                            "field_value": '',
                        })
            res["dest_list"] = dest_list
            res["keyword_list"] = keyword_list
            res["field_list"] = field_list
            res["error"] = ""
        return res



    def add_testcase2(self, json, _id):
        data = {"error": ""}
        commit_user = json.get('commit_user')
        md = ModelInfo.objects.get(pk=_id)
        with transaction.atomic():
            if not TestcaseInfo.objects.filter(case_name=json["title"]):
                new_data = {'case_name': json["title"], 'case_abstract': json["abstract"],
                            'case_premise': json["premise"], 'case_test_mode': json["test_mode"],
                            'case_version': 1, 'case_importance': json["importance"],
                            'charger': json["charger"], 'case_model': md,
                            'create_datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'update_datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                log_dict = self.common_add(TestcaseInfo, new_data, None, self.col_list, self.key_col)
                case_id = log_dict.get('key_id')
                new_case = TestcaseInfo.objects.get(pk=case_id)
                new_case.source_case_id = case_id
                new_case.save()
                if json.get("dest_list"):
                    for i_dest in json.get("dest_list"):
                        dest_obj = DestInfo.objects.get(pk=i_dest.get("id"))
                        CaseDest.objects.create(case=new_case, dest=dest_obj)
                if json.get("keyword_list"):
                    for i_kd in json.get("keyword_list"):
                        keyword_obj = KeywordInfo.objects.get(pk=i_kd.get("id"))
                        CaseKeyword.objects.create(case=new_case, keyword=keyword_obj)
                if json.get("step_list"):
                    for i_step in json.get("step_list"):
                        step_obj = TeststepInfo(order=i_step.get("order"), operate=i_step.get("operate"),
                                                expected_value=i_step.get("expected_value"),
                                                is_automatically=i_step.get("is_automatically"))
                        step_obj.save()
                        CaseStep.objects.create(case=new_case, step=step_obj)
                if json.get("field_value_list"):
                    for i_field_value in json.get("field_value_list"):
                        if type(i_field_value.get("field_value")) == list:
                            CaseFieldValue.objects.create(case=new_case, field=FieldInfo.objects.get(
                                                pk=i_field_value.get("field_id")),
                                                field_value=i_field_value.get("field_value"))
                        else:
                            CaseFieldValue.objects.create(case=new_case, field=FieldInfo.objects.get(
                                                pk=i_field_value.get("field_id")),
                                                field_value=i_field_value.get("field_value"))
                self.commit_case_log(commit_user, log_dict)
                data["result"] = "OK"
            else:
                data["error"] = "名称重复"
        return data

    def change_testcase(self, json, _id):
        data = {"error": ""}
        commit_user = json.get('commit_user')
        with transaction.atomic():
            if TestcaseInfo.objects.filter(pk=_id):
                ChangeData = TestcaseInfo.objects.get(pk=_id)
                old_data = CtrlBase().get_old_data(TestcaseInfo, _id)
                if (old_data[0].get("case_keyword_list") or
                        old_data[0].get("case_dest_list") or
                        old_data[0].get("case_step_list") or
                        old_data[0].get("case_field_value_list")):
                    old_data[0].pop("case_keyword_list")
                    old_data[0].pop("case_dest_list")
                    old_data[0].pop("case_step_list")
                    old_data[0].pop("case_field_value_list")
                self.add_case_history(_id)
                new_data = self.json_to_new_data(json)
                log_dict = CtrlBase().case_common_add(TestcaseInfo, new_data, old_data[0], self.col_list, self.key_col)
                log_dict = self.change_manytomany_list(CaseDest, DestInfo, "dest", ChangeData.case_dest_list.all(),
                                                       ChangeData, json["dest_list"], "case_dest_list", log_dict, _id)
                log_dict = self.change_manytomany_list(CaseKeyword, KeywordInfo, "keyword",
                                                       ChangeData.case_keyword_list.all(),
                                                       ChangeData, json["keyword_list"], "case_dest_list", log_dict, _id)
                log_dict = self.change_field_value_list(CaseFieldValue, FieldInfo, "field",
                                                        ChangeData.case_field_value_list.all(), ChangeData,
                                                        json["field_value_list"], "case_field_value_list", log_dict, _id)
                log_dict = self.change_case_step_list(ChangeData.case_step_list.all(), ChangeData, json["step_list"],
                                                      log_dict, _id)

                self.commit_case_log(commit_user, log_dict)
                data["result"] = "OK"
            else:
                data["error"] = "ID未找到"
        return data

    def change_manytomany_list(self, db_object, db_ob2, db_col , case_list, case_ob, data_list, case_col, log_dict, _id):
        """
        :param db_object: 关系表对象
        :param db_ob2: 关联关系表另一头的表
        :param db_col: 关联表中除了case以外的字段
        :param case_list: 多对多关联字段list
        :param case_col: case_list字段
        :param case_ob: case对象
        :param data_list: 传进来的新值
        :param log_dict: 返回值
        :param _id: case的id
        :return:
        """
        add_list, del_list = [], []
        app_da = {db_col: "", "case": case_ob}
        if data_list:
            if case_list:
                for i_data in case_list:
                    app_da[db_col] = i_data
                    o_data = db_object.objects.get(**app_da)
                    o_flag = False
                    for j_data in data_list:
                        if i_data.id == j_data.get("id"):
                            o_flag = True
                        app_da[db_col] = db_ob2.objects.get(pk=j_data.get("id"))
                        if not db_object.objects.filter(**app_da):
                            db_object.objects.create(**app_da)
                            add_list.append(db_object.id)
                    if not o_flag:
                        del_list.append(o_data.id)
                        o_data.delete()
            else:
                for j_data in data_list:
                    app_da[db_col] = db_ob2.objects.get(pk=j_data.get("id"))
                    if not db_object.objects.filter(**app_da):
                        db_object.objects.create(**app_da)
                        add_list.append(db_object.id)
        else:
            if case_list:
                for i_data in case_list:
                    app_da[db_col] = i_data
                    o_data = db_object.objects.get(**app_da)
                    del_list.append(o_data.id)
                    o_data.delete()
        if add_list or del_list:
            if not log_dict:
                log_dict = {"action": "change", "key_id": _id, "change_col_list": []}
                log_dict["change_col_list"].append(case_col)
            else:
                log_dict["change_col_list"].append(case_col)
        return log_dict

    def change_case_step_list(self, case_list, case_ob, data_list, log_dict, _id):
        """
        :param case_list: 多对多关联字段list
        :param case_ob: case对象
        :param data_list: 传进来的新值
        :param log_dict: 返回值
        :param _id: case的id
        :return:
        """
        add_list, del_list = [], []
        app_da = {"step": "", "case": case_ob}
        if data_list:
            if case_list:
                for i_data in case_list:
                    app_da["step"] = i_data
                    o_data = CaseStep.objects.get(**app_da)
                    o_flag = False
                    for j_data in data_list:
                        if i_data.id == j_data.get("id"):
                            o_flag = True
                        if j_data.get("id"):
                            if TeststepInfo.objects.filter(pk=j_data.get("id")):
                                addData = TeststepInfo.objects.get(pk=j_data.get("id"))
                                if (addData.order != j_data.get("order") or
                                        addData.operate != j_data.get("operate") or
                                        addData.expected_value != j_data.get("expected_value") or
                                        addData.is_automatically != j_data.get("is_automatically")):
                                    addData.order = j_data.get("order")
                                    addData.operate = j_data.get("operate")
                                    addData.expected_value = j_data.get("expected_value")
                                    addData.is_automatically = j_data.get("is_automatically")
                                    addData.save()
                                    add_list.append(addData.id)
                        else:
                            step_obj = TeststepInfo(order=j_data.get("order"), operate=j_data.get("operate"),
                                                    expected_value=j_data.get("expected_value"),
                                                    is_automatically=j_data.get("is_automatically"))
                            step_obj.save()
                            CaseStep.objects.create(case=case_ob, step=step_obj)
                            add_list.append(CaseStep.id)
                    if not o_flag:
                        del_list.append(o_data.id)
                        o_data.delete()
            else:
                for j_data in data_list:
                    app_da["step"] = TeststepInfo.objects.get(pk=j_data.get("id"))
                    if not CaseStep.objects.filter(**app_da):
                        step_obj = TeststepInfo(order=j_data.get("order"), operate=j_data.get("operate"),
                                                expected_value=j_data.get("expected_value"),
                                                is_automatically=j_data.get("is_automatically"))
                        step_obj.save()
                        CaseStep.objects.create(case=case_ob, step=step_obj)
                        add_list.append(CaseStep.id)
        else:
            if case_list:
                for i_data in case_list:
                    app_da["step"] = i_data
                    o_data = CaseStep.objects.get(**app_da)
                    del_list.append(o_data.id)
                    o_data.delete()
        if add_list or del_list:
            if not log_dict:
                log_dict = {"action": "change", "key_id": _id, "change_col_list": []}
                log_dict["change_col_list"].append("case_step_list")
            else:
                log_dict["change_col_list"].append("case_step_list")
        return log_dict

    def change_field_value_list(self, db_object, db_ob2, db_col , case_list, case_ob, data_list, case_col, log_dict, _id):
        """
        :param db_object: 关系表对象
        :param db_ob2: 关联关系表另一头的表
        :param db_col: 关联表中除了case以外的字段
        :param case_list: 多对多关联字段list
        :param case_col: case_list字段
        :param case_ob: case对象
        :param data_list: 传进来的新值
        :param log_dict: 返回值
        :param _id: case的id
        :return:
        """
        add_list, del_list = [], []
        app_da = {db_col: "", "case": case_ob,}
        if data_list:
            if case_list:
                for i_dest in case_list:
                    app_da[db_col] = i_dest
                    o_data = db_object.objects.get(**app_da)
                    o_flag = False
                    for j_data in data_list:
                        if i_dest.id == j_data.get("field_id"):
                            o_flag = True
                        app_da[db_col] = db_ob2.objects.get(pk=j_data.get("field_id"))
                        if db_object.objects.filter(**app_da):
                            fv = db_object.objects.get(**app_da)
                            if not fv.field_value == j_data.get("field_value"):
                                fv.field_value = j_data.get("field_value")
                                fv.save()
                                # db_object.objects.create(**app_da)
                                add_list.append(fv.id)
                        else:
                            app_da2 = {db_col: db_ob2.objects.get(pk=j_data.get("field_id")), "case": case_ob,
                                       "field_value" : j_data.get("field_value")}
                            db_object.objects.create(**app_da2)
                            add_list.append(db_object.id)
                    if not o_flag:
                        del_list.append(o_data.id)
                        o_data.delete()
            else:
                for j_data in data_list:
                    app_da[db_col] = db_ob2.objects.get(pk=j_data.get("field_id"))
                    if not db_object.objects.filter(**app_da):
                        app_da2 = {db_col: db_ob2.objects.get(pk=j_data.get("field_id")), "case": case_ob,
                                   "field_value": j_data.get("field_value")}
                        db_object.objects.create(**app_da2)
                        add_list.append(db_object.id)
        else:
            if case_list:
                for i_data in case_list:
                    app_da[db_col] = i_data
                    o_data = db_object.objects.get(**app_da)
                    del_list.append(o_data.id)
                    o_data.delete()
        if add_list or del_list:
            if not log_dict:
                log_dict = {"action": "change", "key_id": _id, "change_col_list": []}
                log_dict["change_col_list"].append(case_col)
            else:
                log_dict["change_col_list"].append(case_col)
        return log_dict

    def testcase_ver_up(self, Testcase_id):
        data = {"error": ""}
        with transaction.atomic():
            caseDate = TestcaseInfo.objects.get(pk=Testcase_id)
            if not TestcaseInfo.objects.filter(source_case_id=Testcase_id, case_version=caseDate.case_version + 1):
                ChangeData = TestcaseInfo(case_name=caseDate.case_name, case_abstract=caseDate.case_abstract,
                                             case_premise=caseDate.case_premise,
                                             case_test_mode=caseDate.case_test_mode,
                                             case_version=caseDate.case_version + 1,
                                             case_importance=caseDate.case_importance,
                                             charger=caseDate.charger, case_model=caseDate.case_model,
                                             create_datetime=caseDate.create_datetime,
                                             update_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                             source_case_id=caseDate.source_case_id)
                ChangeData.save()
                if caseDate.case_dest_list.all():
                    for i_dest in caseDate.case_dest_list.all():
                        CaseDest.objects.create(dest=i_dest, case=ChangeData)
                if caseDate.case_keyword_list.all():
                    for i_kd in caseDate.case_keyword_list.all():
                        CaseKeyword.objects.create(keyword=i_kd, case=ChangeData)
                if caseDate.case_step_list.all():
                    for i_step in caseDate.case_step_list.all():
                        CaseStep.objects.create(step=i_step, case=ChangeData)
                if caseDate.case_field_value_list.all():
                    for i_fv in caseDate.case_field_value_list.all():
                        CaseFieldValue.objects.create(field=i_fv, case=ChangeData,
                                            field_value=CaseFieldValue.objects.get(field=i_fv, case=caseDate).field_value)
                ChangeData.save()
                data["result"] = {"id":ChangeData.id,"version":ChangeData.case_version}
            else:
                data["error"] = "此case已存在高版本"
        return data

    def add_case_history(self, case_id):
        with transaction.atomic():
            caseDate = TestcaseInfo.objects.get(pk=case_id)
            ChangeData = TestcaseHistory(case_name=caseDate.case_name, case_abstract=caseDate.case_abstract,
                                         case_premise=caseDate.case_premise,
                                         case_test_mode=caseDate.case_test_mode,
                                         case_version=caseDate.case_version,
                                         case_importance=caseDate.case_importance,
                                         charger=caseDate.charger, case_model=caseDate.case_model.id,
                                         create_datetime=caseDate.create_datetime,
                                         update_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                         source_case_id=caseDate.source_case_id, case_id=caseDate.id,)
            ChangeData.save()
            if caseDate.case_dest_list.all():
                dest_list = []
                for i_dest in caseDate.case_dest_list.all():
                    dest_list.append({"id": i_dest.id,
                                      "name": i_dest.dest_showname,
                                      "provider": i_dest.data_provider,
                                      "introduce": i_dest.dest_introduce})

                ChangeData.case_dest_list = json.dumps(dest_list, ensure_ascii=False)
            if caseDate.case_keyword_list.all():
                keyword_list = []
                for i_kd in caseDate.case_keyword_list.all():
                    keyword_list.append({"id": i_kd.id,
                                        "name": i_kd.keyword,
                                         })
                ChangeData.case_keyword_list = json.dumps(keyword_list, ensure_ascii=False)
            if caseDate.case_step_list.all():
                step_list = []
                for i_step in caseDate.case_step_list.all():
                    step_list.append({"id": i_step.id,
                                      "order": i_step.order,
                                      "operate": i_step.operate,
                                      "expected_value": i_step.expected_value,
                                      "is_automatically": i_step.is_automatically})
                ChangeData.case_step_list = json.dumps(step_list, ensure_ascii=False)
            if caseDate.case_field_value_list.all():
                field_value_list = []
                fv = caseDate.case_field_value_list.all()
                for i_fv in fv:
                    if CaseFieldValue.objects.filter(case_id=case_id, field=i_fv):
                        ffv = CaseFieldValue.objects.get(case_id=case_id, field=i_fv)
                        field_value_list.append({
                            "case_id": case_id,
                            "field_id": i_fv.id,
                            "field_value": ffv.field_value,
                        })
                    else:
                        field_value_list.append({
                            "case_id": case_id,
                            "field_id": i_fv.id,
                            "field_value": "",
                        })
                ChangeData.case_field_value_list = json.dumps(field_value_list, ensure_ascii=False)
            ChangeData.save()
            return

    def json_to_new_data(self, json):
        new_data = {'id': json["id"],
                    'case_name': json["title"], 'case_abstract': json["abstract"],
                    'case_premise': json["premise"], 'case_test_mode': json["test_mode"],
                    'case_version': 1, 'case_importance': json["importance"],
                    'charger': json["charger"],
                    'create_datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'update_datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        return new_data

    def delete_testcase(self, _id):
        data = {"error": ""}
        if TestcaseInfo.objects.filter(pk=_id):
            ChangeData = TestcaseInfo.objects.get(pk=_id)
            with transaction.atomic():
                ChangeData.delete()
                if not ChangeData.id:
                    data["result"] = "DELETE OK"
        else:
            data["error"] = "未找到此数据"
        return data

    def batch_delete(self, json):
        data = {"error": ""}
        with transaction.atomic():
            for i_data in json["dellist"]:
                ChangeData = TestcaseInfo.objects.get(pk=i_data)
                if ChangeData:
                    ChangeData.delete()
            data["result"] = "DELETE OK"
        return data

    def search_tsetcase(self, json, page, size):
        data = {"error": ""}
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = TestcaseInfo.objects.all().order_by("case_name")
                for ida in search_list:
                    app = {}
                    if ida.get("is_equal"):
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.filter(**app)
                    else:
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.exclude(**app)
                start = (page - 1) * size
                data["count"] = SearchData.count()
                end = min((page - 1) * size + size, data["count"])
                cases = SearchData.order_by("case_name")[start:end]
                data["result"] = self.data_to_json(cases)
        else:
            data["error"] = "请不要传空数据"
        return data

    def search_tsetcase_no_page(self, json):
        data = {"error": ""}
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = TestcaseInfo.objects.filter(case_version=1).order_by("case_name")
                for ida in search_list:
                    app = {}
                    if ida.get("is_equal"):
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.filter(**app)
                    else:
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.exclude(**app)
                data["count"] = SearchData.count()
                cases = SearchData.order_by("case_name")
                data["result"] = self.data_to_json(cases)
        else:
            data["error"] = "请不要传空数据"
        return data

    def search_tsetcase_by_model(self, m_id, json, page, size):
        data = {"error": ""}
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = TestcaseInfo.objects.filter(case_model=m_id).order_by("case_name")
                for ida in search_list:
                    app = {}
                    if ida.get("is_equal"):
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.filter(**app)
                    else:
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.exclude(**app)
                start = (page - 1) * size
                data["count"] = SearchData.count()
                end = min((page - 1) * size + size, data["count"])
                cases = SearchData.order_by("case_name")[start:end]
                data["result"] = self.data_to_json(cases)
        else:
            data["error"] = "请不要传空数据"
        return data


    def search_tsetcase_by_proj(self, p_id, json, page, size):
        data = {"error": ""}
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                Data = ModelInfo.objects.filter(parent_proj=p_id)
                data["count"] = 0
                for i_data in Data:
                    data["count"] += TestcaseInfo.objects.filter(case_model=i_data.id).count()
                SearchData = TestcaseInfo.objects.filter(case_model__parent_proj=p_id).order_by("case_name")
                for ida in search_list:
                    app = {}
                    if ida.get("is_equal"):
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.filter(**app)
                    else:
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.exclude(**app)
                start = (page - 1) * size
                end = min((page - 1) * size + size, data["count"])
                cases = SearchData.order_by("case_name")[start:end]
                data["result"] = self.data_to_json(cases)
        else:
            data["error"] = "请不要传空数据"
        return data


    def link_option_type(self, data):
        title = "case_name"
        charger = "charger"
        model = "case_model"
        test_mode = "case_test_mode"
        contains = "__icontains"
        se_list = []

        for i_da in data:
            con = ""
            reback = ""
            if i_da.get("type") == "title":
                con = "{}".format(title)
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
            elif i_da.get("type") == "charger":
                con = "{}".format(charger)
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
            elif i_da.get("type") == "test_mode":
                con = "{}".format(test_mode)
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
            version_list = []
            sc_list = TestcaseInfo.objects.filter(source_case_id=i_data.source_case_id)
            for sc in sc_list:
                version_list.append({
                    "id": sc.id,
                    "version": sc.case_version,
                    "source_id": sc.source_case_id,
                })
            search_list.append({
                "id":i_data.id,
                "module_id": i_data.case_model.id,
                "source_id":i_data.source_case_id,
                "title": i_data.case_name,
                "abstract": i_data.case_abstract,
                "premise": i_data.case_premise,
                "charger": i_data.charger,
                "test_mode": i_data.case_test_mode,
                "version": i_data.case_version,
                "version_list": version_list,
            })
        return search_list

    def export_excle(self):
        path = os.path.join('Export')
        if not os.path.exists(path):
            os.makedirs(path)
        the_file_name = "测试Case.xls"
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


    def import_excle(self, file):
        data = {"error": ""}
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
                if not TestcaseInfo.objects.filter(pk = item["id"]):
                    ImportData = TestcaseInfo(iso_code=item["code"], eng_name=item["en_name"], cn_name=item["cn_name"])
                    ImportData.save()
            data["result"] ="OK"
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

    def line_chart_data(self, username):
        """
        折线图数据
        :param username:
        :return:
        """
        q = TestcaseInfo.objects.all().order_by('-create_datetime')
        date_list = []
        size = 7
        for tc in q:
            if len(date_list) == size:
                break
            start_date = tc.create_datetime
            create_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            date_time = create_datetime.strftime("%Y-%m-%d")
            if date_time not in date_list:
                date_list.insert(0, date_time)
            if len(date_list) == 1:
                end_date = start_date
        if not date_list:
            return {"result": "NG", "series": [], "date_list": date_list, "model_list": []}
        q = TestcaseInfo.objects.filter(create_datetime__gte=start_date,
                                        create_datetime__lte=end_date)
        if username:
            q = q.filter(charger=username)
        test_case_dict = dict()
        for case in q:
            if case.case_model.model_name not in test_case_dict:
                test_case_dict[case.case_model.model_name] = []
            create_datetime = datetime.datetime.strptime(case.create_datetime, "%Y-%m-%d %H:%M:%S")
            test_case_dict[case.case_model.model_name].append(create_datetime.strftime("%Y-%m-%d"))
        series = []
        model_list = []
        for model in test_case_dict:
            model_name = model
            time_list = test_case_dict.get(model)
            data = []
            for date in date_list:
                data.append(time_list.count(date))
            model_list.append(model_name)
            series.append({"model": model_name, "data": data})
        if series:
            result = {"result": "OK", "series": series, "date_list": date_list, "model_list": model_list}
        else:
            result = {"result": "NG", "series": series, "date_list": date_list, "model_list": model_list}
        return result

    def get_every_day(self, begin_date, end_date):
        """
        获取两个日期之间所有日期
        :param begin_date:
        :param end_date:
        :return:
        """
        date_list = []
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    def stack_chart_data(self, username):
        """
        堆叠图数据
        :param username:
        :return:
        """
        q = TestresultInfo.objects.all().order_by('-update_datetime')
        date_list = []
        size = 7
        for tc in q:
            if len(date_list) == size:
                break
            start_date = tc.update_datetime
            update_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            date_time = update_datetime.strftime("%Y-%m-%d")
            if date_time not in date_list:
                date_list.insert(0, date_time)
            if len(date_list) == 1:
                end_date = start_date
        if not date_list:
            return {"result": "NG", "series": [], "date_list": date_list, "result_list": []}
        q = TestresultInfo.objects.filter(update_datetime__gte=start_date,
                                          update_datetime__lte=end_date)
        if username:
            q = q.filter(charger=username)
        q = q.order_by('-update_datetime')
        test_result_dict = dict()
        distinct_case = dict()
        for case in q:
            if case.result_value not in test_result_dict:
                test_result_dict[case.result_value] = []
            update_datetime = datetime.datetime.strptime(case.update_datetime, "%Y-%m-%d %H:%M:%S")
            if not distinct_case.get(case.case_id) == update_datetime.strftime("%Y-%m-%d"):
                # 一个case在一天取最后一次结果
                distinct_case[case.case_id] = update_datetime.strftime("%Y-%m-%d")
                test_result_dict[case.result_value].append(update_datetime.strftime("%Y-%m-%d"))
        series = []
        result_data = []
        for test_result in test_result_dict:
            result_value = test_result
            time_list = test_result_dict.get(result_value)
            data = []
            for date in date_list:
                data.append(time_list.count(date))
            result_data.append(result_value)
            series.append({"name": result_value, "data": data})
        if series:
            result = {"result": "OK", "series": series, "date_list": date_list, "result_list": result_data}
        else:
            result = {"result": "NG", "series": series, "date_list": date_list, "result_list": result_data}
        return result

    def pie_chart_data(self, username):
        """
        饼图数据
        :return:
        """
        keys_q = KeywordInfo.objects.all()
        key_word_list = []
        data = []
        for key in keys_q:
            key_word_list.append(key.keyword)
        for key_word in key_word_list:
            key_q = KeywordInfo.objects.get(keyword=key_word)
            if username:
                sum = key_q.key_word_case.all().count()
            else:
                sum = key_q.key_word_case.filter(charger=username).count()
            data.append({'name': key_word, 'value': sum})
        if data:
            result = {"result": "OK", "data": data, "key_word_data": key_word_list}
        else:
            result = {"result": "NG", "data": data, "key_word_data": key_word_list}
        return result

    def commit_case_log(self, commit_user, log_dict):
        """
        保存case更新log
        :param commit_user:
        :param log_dict:
        :return:
        """
        if log_dict:
            commit_time = self.get_current_time()
            action = log_dict.get('action')
            if action == 'add':
                id = log_dict.get('key_id')
                testcase = TestcaseInfo.objects.get(pk=id)
                message = "被%s在%s创建" % (commit_user, commit_time)
                data = log_dict.get('data')
            elif action == 'change':
                id = log_dict.get('key_id')
                testcase = TestcaseInfo.objects.get(pk=id)
                change_col_list = log_dict.get('change_col_list')
                exclude_fields = ['user_name', 'create_datetime', 'update_datetime', 'case_model']
                col_dict = self.get_verbose_name(TestcaseInfo, exclude_fields)
                verbose_name_list = []
                for col in change_col_list:
                    verbose_name_list.append(col_dict.get(col))
                message = "%s在%s修改了%s" % (commit_user, commit_time, ','.join(verbose_name_list))
                data = log_dict.get('data')
            elif action == 'delete':
                testcase = None
                data = log_dict.get()
                message = "被%s在%s删除" % (commit_user, commit_time)
            with transaction.atomic():
                TestcaseChangeLog(testcase=testcase, message=message,
                                  commit_user=commit_user,
                                  create_time=commit_time).save()




















