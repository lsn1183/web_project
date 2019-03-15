from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from userManage.login import Login
from userManage.user_role import UserRole
from userManage.user_basic import *
import  logging

@api_view(['POST'])
def UserLogin(request):
    if request.method == "POST":
        data_json = request.data
        username = data_json.get('username')
        password = data_json.get('password')
        result = Login().login_from_cactus(username, password)
        return Response(result)


@api_view(['GET'])
def Permission(request, username=None):
    try:
        if not username:  # 如果没有人名 传全部
            result = UserRole().get_all_perm()
        else:  # 查找对应
            result = UserRole().get_username_role(username)
        return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def GetRoleUser(request, user_name):
    try:
        if request.method == "GET":
            result = result = UserRole().get_role_user(user_name)
        return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def GetUserPermission(request):
    try:
        if request.method == "POST":
            data_json = request.data
            if data_json.get('user_name'):
                result = UserRole().get_user_permission(data_json.get('user_name'), data_json.get('per_name'))
            else:
                result = {"error": "未收到人名"}
        return Response(result)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def CheckPermission(request):
    if request.method == "POST":
        data_json = request.data
        result = UserRole().check_permission(data_json)
        if not result["error"]:
            return Response(result, status=200)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def SavePersonnelRole(request):
    if request.method == "POST":
        data_json = request.data
        result = UserRole().save_personne_role(data_json)
        if not result["error"]:
            return Response(result, status=200)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def ChangePermission(request):
    if request.method == "PUT":
        data_json = request.data
        result = UserRole().change_permission(data_json)
        if not result["error"]:
            return Response(result, status=200)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def PermissionRole(request, permission):
    try:
        if request.method == "GET":
            if permission:  #
                result = UserRole().get_role_by_promission(permission)
                if not result["error"]:
                    return Response(result)
                else:
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def GetRole(request):
    try:
        if request.method == "GET":
            if id:  #
                result = UserRole().get_role()
                if not result["error"]:
                    return Response(result)
                else:
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_user(request, username=None):       #
    try:
        if username:
            result = UserBasic().search_user_info(username)
        else:
            result = UserBasic().get_all_user_info()
        if not result["error"]:
            return Response(result)
        else:
            return Response(result, status=200)
    except Exception as e:
        error = {}
        logging.warning(e)
        error["error"] = [str(e)]
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
