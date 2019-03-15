# -*- coding: UTF-8 -*-
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from testmanage.models import *
from django.db import transaction
from testmanage.Country import Country
from testmanage.Dest import Dest
from testmanage.Field import Field
from testmanage.Keyword import Keyword
from testmanage.Proj import Proj
from testmanage.Module import Module
import logging
# Create your views here.
@api_view(['GET', 'POST'])
def CountryList(request):
    try:
        if request.method == "GET":
            data = Country().get_country_list()
            return Response(data)
        elif request.method == "POST":
            data = Country().add_country(request.data)
            if not data["error"]:
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(data, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT', 'DELETE'])
def ChangeCountry(request, country_id):
    try:
        if request.method == "PUT":
            data = request.data
            if data:
                result = Country().change_country(data, country_id)
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result, status=200)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
        elif request.method == "DELETE":
            result = Country().delete_country(country_id)
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
def ImportExcle(request):
    try:
        if request.method =="POST":
            file_upload = request.FILES.get('file')
            if file_upload:
                result = Country().import_excle(file_upload)
                if result:
                    return Response(result, status=200)
                else:
                    error = {"error": "NG"}
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def ExportExcle(request):
    try:
        if request.method == "POST":
            result = Country().export_excle()
            return result
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def CountrySearch(request):
    try:
        if request.method == "POST":
            data = request.data
            result = Country().search_country(data)
            if result:
                return Response(result, status=200)
            else:
                error = {"error": "NG"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def DestSearch(request):
    try:
        if request.method == "POST":
            data = request.data
            result = Dest().search_dest(data)
            return Response(result)
        else:
            error = {"error": "NG"}
            return Response(error, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def DestList(request):
    try:
        if request.method == "GET":
            result = Dest().get_dest_list()
            return Response(result)
        elif request.method == "POST":
            data = request.data
            if data:
                result = Dest().add_dest(data)
                if not result["error"]:
                    return Response(result, status=status.HTTP_201_CREATED)
                else:
                    return Response(result, status=200)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
def ChangeDest(request, Dest_id):
    try:
        if request.method == "PUT":
            data = request.data
            if data:
                result = Dest().change_dest(data, Dest_id)      # 不能因为键值为空就判断字典为空
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result,status=200)
        elif request.method == "DELETE":
            result = Dest().delete_dest(Dest_id)
            if not result["error"]:
                return Response(result,status=200)
            else:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def BatchDeleteCountry(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                result = Country().batch_delete(data)
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def BatchDeleteDest(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                result = Dest().batch_delete(data)
                if result:
                    return Response("DELETE OK", status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def BatchDeleteField(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                result = Field().batch_delete(data)
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def KeywordList(request):
    try:
        if request.method == "GET":
            result = Keyword().get_keyword_list()
            return Response(result)
        elif request.method == "POST":
            data = request.data
            if data:
                result = Keyword().add_keyword(data)
                if not result["error"]:
                    return Response(result, status=status.HTTP_201_CREATED)
                else:
                    return Response(result, status=200)
            else:
                return Response("NG", status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
def ChangeKeyword(request, Keyword_id):
    try:
        if request.method == "PUT":
            data = request.data
            if data:
                result = Keyword().change_keyword(data, Keyword_id)
                if not result["error"]:
                    return Response(result,status=200)
                else:
                    return Response(result,status=200)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error,status=status.HTTP_204_NO_CONTENT)
        elif request.method == "DELETE":
            result = Keyword().delete_keyword(Keyword_id)
            if not result["error"]:
                return Response(result,status=200)
            else:
                return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def KeywordSearch(request):
    try:
        if request.method == "POST":
            data = request.data
            result = Keyword().search_keword(data)
            return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def FieldSearch(request):
    try:
        if request.method == "POST":
            data = request.data
            result = Field().search_field(data)
            return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def BatchDeleteKeyword(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                result = Keyword().batch_delete(data)
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def FieldList(request):
    try:
        if request.method == "GET":
            result = Field().get_field_list()
            return Response(result)
        elif request.method == "POST":
            data = request.data
            if data:
                result = Field().add_field(data)
                if not result["error"]:
                    return Response(result, status=status.HTTP_201_CREATED)
                else:
                    return Response(result, status=200)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
def ChangeField(request, Field_id):
    try:
        if request.method == "PUT":
            data = request.data
            if data:
                result = Field().change_field(data, Field_id)
                if not result["error"]:
                    return Response(result,status=200)
                else:
                    return Response(result,status=200)
        elif request.method == "DELETE":
            result = Field().delete_field(Field_id)
            if not result["error"]:
                return Response(result,status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def ProjList(request):
    try:
        if request.method == "GET":
            result = Proj().get_proj_list()
            return Response(result)
        elif request.method == "POST":
            data = request.data
            if data:
                result = Proj().add_proj(data)
                if not result["error"]:
                    return Response(result, status=status.HTTP_201_CREATED)
                else:
                    return Response(result, status=200)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def projects(request):
    try:
        if request.method == "GET":
            result = Proj().get_projects()
            return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def BatchDeleteProj(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                result = Proj().batch_delete(data)
                if result["result"] == "DELETE OK":
                    return Response(result, status=200)
                else:
                    return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def ProjSearch(request):
    try:
        if request.method == "POST":
            data = request.data
            result = Proj().search_proj(data)
            return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
def ChangeProj(request, Proj_id):
    try:
        if request.method == "PUT":
            data = request.data
            if data:
                result = Proj().change_proj(data, Proj_id)
                if result["result"] == "OK":
                    return Response(result,status=200)
                else:
                    return Response(result, status=200)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
        elif request.method == "DELETE":
            result = Proj().delete_proj(Proj_id)
            if not result["error"]:
                return Response(result, status=200)
            else:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def ExportYaml(request, Proj_id):
    try:
        if request.method == "POST":
            result = Proj().export_yaml(Proj_id)
            if result:
                return result
            else:
                error = {"error": "NG"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def ImportYaml(request):
    try:
        if request.method =="POST":
            file_upload = request.FILES.get('file')
            if file_upload:
                result, error = Proj().import_yaml(file_upload)
                if not error:
                    return Response(result, status=200)
                else:
                    return Response(error , status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def ProjListTree(request, Proj_id):
    try:
        if request.method == "GET":
            result = Proj().get_proj_tree(Proj_id)
            return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def ChangeModuleInfo(request, id):
    try:
        if request.method == "GET":
            result = Module().get_module_field_list(id)
            if result:
                return Response(result, status=200)
            else:
                return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def GetFieldsByProj(request, id):
    try:
        if request.method == "GET":
            result = Module().get_module_field_list_by_proj(id)
            if result:
                return Response(result, status=200)
            else:
                return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT', 'DELETE'])
def ChangeModule(request, id):
    try:
        if request.method == "PUT":
            data = request.data
            if data:
                result = Module().change_module(data, id)
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result,status=200)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
        elif request.method == "DELETE":
            result = Module().delete_module(id)
            if not result["error"]:
                return Response(result, status=200)
            else:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def ModuleSearch(request):
    try:
        if request.method == "POST":
            data = request.data
            result = Module().search_model(data)
            return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def ModuleList(request, Proj_id):
    try:
        if request.method == "GET":
            result = Module().get_module_list(Proj_id)
            return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def ModuleAdd(request):
    try:
        if request.method == "POST":
            data = request.data
            if data:
                result = Module().add_module(data)
                if not result["error"]:
                    return Response(result, status=status.HTTP_201_CREATED)
                else:
                    return Response(result, status=200)
            else:
                error = {"error": "请不要传空数据"}
                return Response(error, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def BatchDeleteModule(request):
    try:
        if request.method == "DELETE":
            data = request.data
            if data.get("dellist"):
                result = Module().batch_delete(data)
                if not result["error"]:
                    return Response(result, status=200)
                else:
                    return Response(result,status= 200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def GetCaseTree(request, id):
    try:
        result = Module().get_module_tree(id)
        return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def GetModuleTree(request, id):
    try:
        result = Module().get_proj_module_tree(id)
        return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def GetCactusProj(request):
    try:
        data = request.data
        result = Proj().get_proj_for_cactus(data)
        return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)