# -*- coding: UTF-8 -*-
from testmanage.models import *
from testcase.models import *
import os
import xlrd
import xlwt
import datetime
from django.db import transaction
from django.http import FileResponse



class Testresult():
    def get_all_testresult_list(self, page, size):
        data = {"error":""}
        start = (page-1)*size
        data["count"] = TestresultInfo.objects.count()
        end = min((page-1)*size+size, data["count"])
        cases = TestresultInfo.objects.all().order_by("-update_datetime")[start:end]
        data["result"] = []
        for i_case in cases:
            data["result"].append({
                "id":i_case.id,
                "module_id": i_case.result_model.id,
                "title": i_case.result_name,
                "abstract": i_case.result_abstract,
                "premise": i_case.result_premise,
                "charger": i_case.charger,
                "test_mode": i_case.result_test_mode,
            })
        return data

    def get_testresult_list(self):
        data = {"error": ""}
        cases = TestresultInfo.objects.all().order_by("-update_datetime")
        data["count"] = TestresultInfo.objects.count()
        data["result"] = []
        for i_case in cases:
            data["result"].append({
                "id": i_case.id,
                "module_id": i_case.result_model.id,
                "title": i_case.result_name,
                "abstract": i_case.result_abstract,
                "premise": i_case.result_premise,
                "charger": i_case.charger,
                "test_mode": i_case.result_test_mode,
            })
        return data

    def get_testresult_history_by_plan(self, result_plan_id, case_id):
        data = {"error": ""}
        # data["count"] = TestresultInfo.objects.filter(result_plan_id=plan_id,result_case_id=case_id).count()
        cases = TestresultInfo.objects.filter(result_plan_id=result_plan_id, case_id=case_id).order_by("-update_datetime")
        data["result"] = []
        if cases:
            for i_case in cases:
                data["result"].append({
                    "id": i_case.id,
                    "module_id": i_case.result_model.id,
                    "title": i_case.result_name,
                    "charger": i_case.charger,
                    "commter": i_case.result_commiter,
                    "result_value": i_case.result_value,
                    "remarks": i_case.result_remarks,
                    "case_id": i_case.case_id,
                    "test_mode": i_case.result_test_mode,
                    "updatetime": i_case.update_datetime
                })
        return data

    def get_one_testresult_history(self, result_id):
        data = {"error": "","result": {}}
        if TestresultInfo.objects.filter(pk=result_id):
            cases = TestresultInfo.objects.get(pk=result_id)
            step_list = []
            if cases.result_step_list.all():
                cct = cases.result_step_list.all()
                for ct in cct:
                    step_list.append({
                        "id": ct.id,
                        "order": ct.order,
                        "operate": ct.operate,
                        "expected_value": ct.expected_value,
                        "is_automatically": ct.is_automatically,
                        "remark": ct.step_remark,
                        "state": ct.step_state,
                    })
            data["result"] = {
                "id": cases.id,
                "module_id": cases.result_model.id,
                "version": cases.result_version,
                "title": cases.result_name,
                "charger": cases.charger,
                "abstract": cases.result_abstract,
                "importance": cases.result_importance,
                "commter": cases.result_commiter,
                "result_value": cases.result_value,
                "remarks": cases.result_remarks,
                "case_id": cases.case_id,
                "test_mode": cases.result_test_mode,
                "updatetime": cases.update_datetime,
                "step_list": step_list,
            }
        else:
            data["error"] = "没有信息"
        return data


    def add_testresult(self, json, plan_id):
        data = ""
        with transaction.atomic():
            plan = TestplanInfo.objects.filter(pk= plan_id)
            if json["case_list"]:
                for i_case in json["case_list"]:
                    caseDate = TestcaseInfo.objects.get(pk=i_case.get("id"))
                    ChangeData = TestresultInfo(result_name=caseDate.case_name, result_abstract=caseDate.case_abstract,
                                        result_premise=caseDate.case_premise, result_test_mode=caseDate.case_test_mode,
                                        result_version=caseDate.case_version, result_importance=caseDate.case_importance,
                                        charger=caseDate.charger, result_model=caseDate.case_model,
                                        create_datetime=caseDate.create_datetime, source_case_id =caseDate.source_case_id,
                                        update_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                        result_plan=caseDate, case_id =caseDate.id)
                    # ChangeData.plan_case_list.add(TestcaseInfo.objects.get(pk=i_plan.get("id")))
                    ChangeData.save()
                    ChangeData.result_value = i_case.get("result_value")
                    ChangeData.result_remarks = i_case.get("result_remarks")
                    ChangeData.result_commiter = i_case.get("result_commiter")
                    if  caseDate.case_dest_list.all():
                        for i_dest in caseDate.case_dest_list.all():
                            ChangeData.result_dest_list.add(i_dest)
                    if  caseDate.case_keyword_list.all():
                        for i_kd in i_case.case_keyword_list.all():
                            ChangeData.result_keyword_list.add(i_kd)
                    if json["step_list"]:
                        for v_step in json["step_list"]:
                            addData = TeststepInfo(order=v_step.get("order"), operate=v_step.get("operate"),
                                                   expected_value=v_step.get("expected_value"),
                                                   step_remark=v_step.get("step_remark"),
                                                   step_state=v_step.get("step_state"),
                                                   is_automatically=v_step.get("is_automatically"))
                            addData.save()
                            ChangeData.result_step_list.add(addData)
                    if json.get("field_list"):
                        for i_field_value in json.get("field_list"):
                            valueData = ResultfieldInfo(result_case=ChangeData,
                                                        field=FieldInfo.objects.get(pk=i_field_value.get("field_id")),
                                                        field_value=i_field_value.get("field_value"))
                            valueData.save()
                    ChangeData.save()
                    data = "OK"
                    return data
            return data

    def add_testresult_one(self, json, result_plan_id, case_id):
        data = {"error": ""}
        with transaction.atomic():
            if TestplanhistoryInfo.objects.filter(pk= result_plan_id):
                plan = TestplanhistoryInfo.objects.get(pk= result_plan_id)
                if json:
                    caseDate = TestcaseInfo.objects.get(pk=case_id)
                    ChangeData = TestresultInfo(result_name=caseDate.case_name, result_abstract=caseDate.case_abstract,
                                        result_premise=caseDate.case_premise, result_test_mode=caseDate.case_test_mode,
                                        result_version=caseDate.case_version, result_importance=caseDate.case_importance,
                                        charger=caseDate.charger, result_model=caseDate.case_model,
                                        create_datetime=caseDate.create_datetime,
                                        update_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                        result_plan=plan, case_id =caseDate.id,source_case_id =caseDate.source_case_id)
                    # ChangeData.plan_case_list.add(TestcaseInfo.objects.get(pk=i_plan.get("id")))
                    ChangeData.save()
                    ChangeData.result_value = json.get("result_value")
                    ChangeData.result_remarks = json.get("result_remarks")
                    ChangeData.result_commiter = json.get("result_commiter")
                    if  caseDate.case_dest_list.all():
                        for i_dest in caseDate.case_dest_list.all():
                            ChangeData.result_dest_list.add(i_dest)
                    if  caseDate.case_keyword_list.all():
                        for i_kd in caseDate.case_keyword_list.all():
                            ChangeData.result_keyword_list.add(i_kd)
                    if  json["step_list"]:
                        for v_step in json["step_list"]:
                            addData = TeststepInfo(order=v_step.get("order"), operate=v_step.get("operate"),
                                                   expected_value=v_step.get("expected_value"),
                                                   step_remark=v_step.get("step_remark"),
                                                   step_state=v_step.get("step_state"),
                                                   is_automatically=v_step.get("is_automatically"))
                            addData.save()
                            ChangeData.result_step_list.add(addData)
                    if caseDate.case_field_value_list.all():
                        for i_fd in caseDate.case_field_value_list.all():
                            cfv = CaseFieldValue.objects.get(field=i_fd, case=caseDate)
                            valueData = ResultfieldInfo(result_case=ChangeData,
                                                        field=i_fd,
                                                        field_value=cfv.field_value)
                            valueData.save()
                    if json.get("field_list"):
                        for i_field_value in json.get("field_list"):
                            if i_field_value.get("field_open_use")=="test_execution":
                                valueData = ResultfieldInfo(result_case=ChangeData,
                                                          field=FieldInfo.objects.get(pk=i_field_value.get("id")),
                                                          field_value=i_field_value.get("field_value"))
                                valueData.save()
                    ChangeData.save()
                    data["result"] = "OK"
                    return data
            else:
                data["error"] = "NG"
            return data


    def delete_testresult(self, _id):
        data = ""
        ChangeData = TestresultInfo.objects.get(pk=_id)
        with transaction.atomic():
            if ChangeData:
                ChangeData.delete()
                if not ChangeData.id:
                    data = "DELETE OK"
        return data

    def batch_delete(self, json):
        data = {"error": ""}
        with transaction.atomic():
            for i_data in json["dellist"]:
                ChangeData = TestresultInfo.objects.get(pk=i_data)
                if ChangeData:
                    ChangeData.delete()
            data["result"] = "DELETE OK"
        return data

    def change_testresult(self):
        return