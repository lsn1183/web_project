from django.urls import path
from userManage import views

app_name = 'userManage'

urlpatterns = [
    path('Login', views.UserLogin),
    path('GetPermission/<str:username>', views.Permission),  # 获取某人的权限
    path('GetRoleUser/<str:user_name>', views.GetRoleUser),  # 获取某人角色
    path('GetPermission', views.Permission),  # 获取所有权限
    path('GetPermissionRole/<int:permission>', views.PermissionRole),  # 获取某角色下的权限
    path('CheckPermission', views.CheckPermission),  # 角色分配权限
    path('ChangePermission', views.ChangePermission),  # 修改权限
    path('GetRole', views.GetRole),  # 获取所有角色
    path('SavePersonnelRole', views.SavePersonnelRole),  # 给人分角色
    path('GetUser', views.get_user),
    path('GetUser/<str:username>', views.get_user),
    path('GetUserPermission', views.GetUserPermission)
]
