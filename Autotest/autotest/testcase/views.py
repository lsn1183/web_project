# -*- coding: UTF-8 -*-
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
# from testcase.serializer import CategorySerializer
import json
from testcase.Testcase import Testcase
from testcase.Testplan import Testplan
from testcase.Testresult import Testresult
from testcase.testcase_ver_diff import TestcaseVerDiff
from testcase.Image import Img
import logging

# Create your views here.
@api_view(['GET'])
def AllTestcaseList(request, page, size):
    try:
        if request.method == "GET":
            res = Testcase().get_all_testcase_list(page, size)
            if not res["error"]:
                return Response(res)
            else:
                error = {"error": "请不要传空数据"}
                return Response("NG",status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def TestcaseListAll(request, Proj_id):
    try:
        if request.method == "GET":
            res = Testcase().get_testcase_list(Proj_id)
            if not res["error"]:
                return Response(res)
            else:
                return Response("NG",status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestcaseModelList(request, Model_id, page, size):
    try:
        if request.method == "GET":
            res = Testcase().get_testcase_list_by_model(Model_id, page, size)
            if not res["error"]:
                return Response(res)
            else:
                return Response("NG",status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestcaseProjList(request, Proj_id, page, size):
    try:
        if request.method == "GET":
            res = Testcase().get_testcase_list_by_proj(Proj_id, page, size)
            if not res["error"]:
                return Response(res)
            else:
                return Response("NG",status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def TestcaseAdd(request, Model_id):
    try:
        if request.method == "POST":
            data = request.data
            if data:
                res = Testcase().add_testcase2(data, Model_id)
                if not res["error"]:
                    return Response(res)
                else:
                    return Response(res,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def Getthreelist(request, Model_id):
    try:
        if request.method == "GET":
            res = Testcase().get_three_list(Model_id)
            if not res["error"]:
                return Response(res)
            else:
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestcaseOne(request, Testcase_id):
    try:
        if request.method == "GET":
            res = Testcase().get_testcase_one(Testcase_id)
            if not res["error"]:
                return Response(res,status=200)
            else:
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestcaseVerUp(request, Testcase_id):
    try:
        if request.method == "GET":
            res = Testcase().testcase_ver_up(Testcase_id)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
def ChangeTestcase(request, Testcase_id):
    try:
        if request.method == "PUT":
            data = request.data
            if data:
                res = Testcase().change_testcase(data, Testcase_id)
                if not res["error"]:
                    return Response(res)
                else:
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                error = {"error":"请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
        elif request.method == "DELETE":
            res = Testcase().delete_testcase(Testcase_id)
            if not res["error"]:
                return Response(res)
            else:
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def BatchDeleteTestcase(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                res = Testcase().batch_delete(data)
                if not res["error"]:
                    return Response(res, status=200)
                else:
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def search_tsetcase(request, page, size):
    try:
        if request.method == "POST":
            data = request.data
            res = Testcase().search_tsetcase(data, page, size)
            if not res["error"]:
                return Response(res,status=200)
            else:
                return Response(res, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def search_tsetcase_no_page(request):
    try:
        if request.method == "POST":
            data = request.data
            res = Testcase().search_tsetcase_no_page(data)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def search_tsetcase_by_model(request, m_id, page, size):
    try:
        if request.method == "POST":
            data = request.data
            res = Testcase().search_tsetcase_by_model(m_id,data, page, size)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def search_tsetcase_by_proj(request, p_id, page, size):
    try:
        if request.method == "POST":
            data = request.data
            res = Testcase().search_tsetcase_by_proj(p_id, data, page, size)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def ImportExcle(request):
    try:
        if request.method =="POST":
            file_upload = request.FILES.get('file')
            if file_upload:
                res = Testcase().import_excle(file_upload)
                if not res["error"]:
                    return Response(res, status=200)
                else:
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def ExportExcle(request):
    try:
        if request.method == "POST":
            result = Testcase().export_excle()
            return result
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestplanHistoryList(request, plan_id):
    try:
        if request.method == "GET":
            res = Testplan().get_historyplan_list_by_id(plan_id)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res,status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestplanList(request, Proj_id, page, size):
    try:
        if request.method == "GET":
            res = Testplan().get_testplan_list(Proj_id ,page, size)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res,status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def TestplanAdd(request):
    try:
        if request.method == "POST":
            data = request.data
            if data:
                res = Testplan().add_testplan(data)
                if not res["error"]:
                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def TestplanHistoryAdd(request):
    try:
        if request.method == "POST":
            res = Testplan().add_plan_history(request.data)
            if not res["error"]:
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','PUT'])
def ChangePlan(request, Testplan_id):
    try:
        if request.method == "PUT":
            data = request.data
            if data:
                res = Testplan().change_testplan(data, Testplan_id)
                if not res["error"]:
                    return Response(res, status=200)
                else:
                    return Response(res, status=200)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
        elif request.method == "GET":
            res = Testplan().get_one_testplan(Testplan_id)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def SettingOption(request, Testplan_id):
    try:
        if request.method == "GET":
            res = Testplan().get_PlanSetting_options(Testplan_id)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res, status=200)
    except Exception as e:
        error = {}
        print(e)
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST','GET' ])
def ChangePlanSetting(request, plan_id):
    try:
        if request.method == "POST":
            data = request.data
            res = Testplan().add_or_change_PlanSetting(data, plan_id)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res, status=200)
        elif request.method == "GET":
            res = Testplan().get_PlanSetting_by_id(plan_id)
            if not res["error"]:
                return Response(res, status=200)
            else:
                return Response(res, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def BatchDeletePlan(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                result = Testplan().batch_delete(data)
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def BatchDeleteTestplanHistory(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                result = Testplan().batch_delete_history(data)
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def Search_Tsetplan(request, page, size):
    try:
        if request.method == "POST":
            data = request.data
            result = Testplan().search_tsetplan(data, page, size)
            if not result["error"]:
                return Response(result, status=200)
            else:
                return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def UploadImg(request):
    try:
        if request.method == "POST":
            url = request.FILES.get('file')
            if url:
                img_id = Img().add_img(url)
                result = Img().get_img_by_id(img_id)
                if not result["error"]:
                    return Response(result, status=status.HTTP_201_CREATED)
                else:
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def TestresultAdd(request, result_plan_id, case_id):
    try:
        if request.method == "POST":
            data = request.data
            if data:
                res = Testresult().add_testresult_one(data, result_plan_id, case_id)
                if not res["error"]:
                    return Response(res, status=200)
                else:
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET','PUT'])
# def ChangeTestresult(request, Testplan_id):
#     try:
#         if request.method == "PUT":
#             data = request.data
#             if data:
#                 result = Testresult().change_testplan(data, Testplan_id)
#                 if result:
#                     return Response("OK", status=200)
#             else:
#                 return Response("NG", status=status.HTTP_204_NO_CONTENT)
#         elif request.method == "GET":
#             result = Testresult().get_one_testplan(Testplan_id)
#             if not result["error"]:
#                 return Response(result, status=200)
#             else:
#                 return Response("NG", status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         logging.warning(e)
#         return Response([str(e)], status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def BatchDeleteTestresult(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                result = Testresult().batch_delete(data)
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestresultHistory(request, result_plan_id, case_id):
    try:
        if request.method == "GET":
            # data = request.data
            result = Testresult().get_testresult_history_by_plan(result_plan_id, case_id)
            if not result["error"]:
                return Response(result)
            else:
                return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestresultHistoryOne(request, result_case_id):
    try:
        if request.method == "GET":
            # data = request.data
            result = Testresult().get_one_testresult_history(result_case_id)
            if not result["error"]:
                return Response(result)
            else:
                return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestresultList(request, result_plan_id):
    try:
        if request.method == "GET":
            # data = request.data
            result = Testplan().get_allcase_on_testplan(result_plan_id)
            if not result["error"]:
                return Response(result)
            else:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def TestresultOne(request, plan_id, case_id):
    try:
        if request.method == "GET":
            # data = request.data
            result = Testplan().get_one_case_on_testplan(plan_id, case_id)
            if not result["error"]:
                return Response(result)
            else:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def LineChart(request, username=None):
    if request.method == "GET":
        result = Testcase().line_chart_data(username)
        return Response(result)


@api_view(['GET'])
def StackChart(request, username=None):
    if request.method == "GET":
        result = Testcase().stack_chart_data(username)
        return Response(result)


@api_view(['GET'])
def PieChart(request, username=None):
    if request.method == "GET":
        result = Testcase().pie_chart_data(username)
        return Response(result)


@api_view(['GET'])
def TcHistoryVer(request, source_case_id):
    if request.method == "GET":
        history_id_list = TestcaseVerDiff().get_history_id(source_case_id)
        return Response(history_id_list)


@api_view(['GET'])
def TcVerDiff(request, case_id, lefet_ver=0, right_ver=0):
    if request.method == "GET":
        result = {"result": "NG"}
        left_data, right_data, msg = TestcaseVerDiff().get_history_testcase(lefet_ver, right_ver, case_id)
        if left_data or right_data:
            result["content"] = {"left": left_data,
                                 "right": right_data,
                                 }
            result["result"] = "OK"
        else:
            result["message"] = msg
        return Response(result)


# CreateJenkinsJob
@api_view(['POST'])
def CreateJenkinsJob(request):
    try:
        if request.method == "POST":
            data = request.data
            result = Testplan().create_jenkins_job(data)
            if not result["error"]:
                return Response(result, status=200)
            else:
                return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#GetJenkinsNode
@api_view(['GET'])
def GetJenkinsNode(request):
    if request.method == 'GET':
        result = Testplan().get_jenkins_node()
        return Response(result)