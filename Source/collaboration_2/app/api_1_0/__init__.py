# -*- coding: UTF-8 -*-
import os
from flask_restful import Resource, Api
from flask import current_app

from app.api_1_0.login import Login, Root
from app.api_1_0.api_doc_tag_cat import ApiDocTagCat
from app.api_1_0.api_doc_tag_cat import ApiDocTagIncludeNumber
from app.api_1_0.api_doc_tag_cat import ApiDocTagRequiredGroups
from app.api_1_0.api_doc_tag_cat import ApiDocTagProject
from app.api_1_0.doc_app import DocApp, DocApp2, DocByTag, DocByFailureMode, FailureModeByTag
from app.api_1_0.doc_app import DocAppUpdate, DocGroupUser
from app.api_1_0.api_role import ApiRole, ApiRolePermission
from app.api_1_0.api_permission import ApiPermission
from app.api_1_0.api_user import ApiUser, ApiUserRole, ApiUserPermission, ApiUserRoleCactus
from app.api_1_0.api_model import ApiModel, ApiModelDSDoc, ApiModelTree, ApiModelAuthor
from app.api_1_0.api_model import ApiModelTags, ApiSectionTags
from app.api_1_0.api_model import ApiModelRefGet, ApiSubModel, ApiModelRefPost
from app.api_1_0.api_model import ApiDesignTop, ApiTestDelCache
from app.api_1_0.api_ds_doc import ApiDSDoc, ApiDSDocType, ApiDSectionType
from app.api_1_0.api_ds_doc import ApiNewDSDoc, ApiUpDocVer
from app.api_1_0.api_ds_doc import ApiDsDocIf, ApiDSDocStatus, ApiCopyBasicToDetail
from app.api_1_0.api_ds_doc import ApiDSDoc2, ApiComment, ApiDSection, ApiDSDocUsecase
from app.api_1_0.api_ds_doc import ApiUsecaseDetail, ApiNewDsSection, ApiDsUcSub
from app.api_1_0.api_ds_doc import ApiAllUsecase, ApiDSUcLevel2
from app.api_1_0.api_ds_doc import ApiDSConsider, ApiKnowledgeDoc
from app.api_1_0.api_ds_doc import ApiDSRelSpec, ApiDSDocAstah, ApiUcRelSpec, ApiDSDocInput, ApiDSDocInputGet
from app.api_1_0.api_ds_doc import ApiImportDsDoc, ApiDSDocImport
from app.api_1_0.api_ds_doc import ApiDRBFM, ApiDrbfmExport
from app.api_1_0.api_down_up import DownFile, ApiUploadImage, ImageSize
from app.api_1_0.api_ds_doc_template import ApiDSDocTemplate
from app.api_1_0.api_ds_scene import ApiDSScene, ApiDSTag
from app.api_1_0.api_ds_failure import ApiDSFailure
from app.api_1_0.api_project import ApiProject, ApiProjectFW, ApiProjectTag, ApiProjectModel, ApiProjectGroup
from app.api_1_0.api_project import ApiMergeCactusProject, ApiGetCactusProject
from app.api_1_0.api_resource import ApiResource
from app.api_1_0.api_specification import ApiSpecification, ApiDSDocSpec, ApiUsecaseSpec
from app.api_1_0.api_group_members import ApiGroupMembers, ApiGroup, ApiCactusGroups
from app.api_1_0.api_group_members import ApiModelGroupMessage
from app.api_1_0.api_framework import ApiFramework, ApiFwProject, ApiImportFWModel, ApiImportProjectModel, ApiGetCactusFw
from app.api_1_0.doc_app import ApiKnowledgeClassify
from app.api_1_0.api_journal import ApiJournal, ApiJournalVersion
from app.api_1_0.api_export_doc import ApiExportDoc
from app.api_1_0.api_import_doc import ApiWebImportDoc
from app.api_1_0.api_excel_htm import ApiExcelHtm
from app.api_1_0.api_fun_search import ApiFunSearch, ApiBugSearch, ApiKeyList, ApiAnyPlaceInfo
# from app.api_1_0.api_ds_doc import ApiContentJson
from app.api_1_0.api_if_import import ApiImportIfDoc


class Api_1_0():
    def __init__(self, api):
        # Home
        api.add_resource(Root, '/')
        api.add_resource(Login, '/login')
        api.add_resource(ApiDocTagCat,
                         '/v1.0/ApiDocTagCat',
                         '/v1.0/ApiDocTagCat/<int:tag_id>',
                         '/TagTree',
                         '/TagTree/<int:tag_id>',
                         '/TagTree/<string:rate>',
                         '/TagTree/<string:rate>/<string:username>'
                         )
        api.add_resource(ApiDocTagProject, '/DocTagProject/<string:classify>')
        api.add_resource(ApiDocTagRequiredGroups,
                         '/TagRequiredGroups')
        api.add_resource(ApiDocTagIncludeNumber,
                         '/TagTreeIncludeNumber',
                         '/TagTreeIncludeNumber/<int:user_id>',
                         '/TagTreeIncludeNumber/<string:rate>',
                         '/TagTreeIncludeNumber/<string:rate>/<username>'
                         )
        api.add_resource(DocApp, '/Doc', '/Doc/<int:doc_id>')
        api.add_resource(DocAppUpdate, '/UpdateDoc')
        api.add_resource(DocGroupUser, '/DocGroupUser', '/DocGroupUser/<string:create_time>')
        api.add_resource(DocApp2, '/Doc2/<int:doc_id>')
        api.add_resource(ApiKnowledgeClassify,  # 知识点分级
                         '/KnowledgeClassify',
                         '/KnowledgeClassify/<knowledge_only>',
                         '/KnowledgeClassify/<knowledge_only>/<knowledge>')
        api.add_resource(DocByTag, '/DocByTag/<int:page>/<int:size>/<int:tag_id>',
                         '/DocByTag/<int:page>/<int:size>',
                         '/DocQuery/<int:page>/<int:size>/<path:condition>',
                         '/DocByTag/<int:page>/<int:size>/<string:username>',
                         '/DocQuery/<int:page>/<int:size>/<path:condition>/<string:username>',
                         '/DocByTag/<int:page>/<int:size>/<string:username>/<int:tag_id>')
        api.add_resource(DocByFailureMode,
                         '/DocByFailureMode/<int:page>/<int:size>',
                         '/DocByFailureMode/<int:page>/<int:size>/<failure_mode>',
                         )
        api.add_resource(FailureModeByTag,
                         '/FailureModeByTag/<int:tag_id>')
        # 角色权限
        api.add_resource(ApiRole, '/Role',
                         '/Role/<int:role_id>',
                         '/Role/<string:cls>')
        api.add_resource(ApiUser, '/User')
        api.add_resource(ApiRolePermission, '/RolePermission')
        api.add_resource(ApiPermission, '/Permission')
        api.add_resource(ApiUserRole, '/ApiUserRole',
                         '/ApiUserRole/<int:page>/<int:size>',
                         '/UserRoleQuery/<int:page>/<int:size>/<condition>')
        api.add_resource(ApiUserPermission, '/UserPermission/<int:user_id>')  # 用户权限
        api.add_resource(ApiUserRoleCactus, '/UserRoleCactus')  # 从cactus上拿用户角色
        # Group(组)
        api.add_resource(ApiGroup, '/ApiGroup',
                         '/ApiGroup/<int:group_id>',
                         '/ApiGroup/<group_name>')
        api.add_resource(ApiGroupMembers, '/ApiGroupMembers',
                         '/ApiGroupMembers/<int:group_id>',
                         '/ApiGroupMembers/<int:group_id>/<int:user_id>')
        api.add_resource(ApiCactusGroups, '/CactusGroups')
        api.add_resource(ApiModelGroupMessage, '/ModelGroupMessage')
        # Model(模块)
        api.add_resource(ApiModelDSDoc, '/ModelDSDoc/<int:page>/<int:size>',  # 取所有设计文档列表
                         '/ModelDSDocByPro/<int:page>/<int:size>/<int:proj_id>',  # 获取项目下所有的文档
                         '/ModelDSDocByFw/<int:page>/<int:size>/<int:fw_id>',  # 获取平台下所有的文档
                         '/ModelDSDoc/<int:page>/<int:size>/<int:proj_id>/<int:model_id>',  # 获取模块下所有的文档
                         '/ModelDSDoc/<int:page>/<int:size>/<int:proj_id>/<int:model_id>/<doc_type>',
                         '/ModelDSDoc/<int:page>/<int:size>/<user>',
                         '/ModelDSDoc/<int:page>/<int:size>/<user>/<int:proj_id>/<int:model_id>',
                         '/ModelDSDoc/<int:page>/<int:size>/<user>/<int:proj_id>/<int:model_id>/<doc_type>',
                         '/ModelDSDoc/<int:page>/<int:size>/<user>/<doc_type>',
                         '/ModelDSDocQuery/<int:page>/<int:size>/<condition>',
                         '/ModelDSDocQuery/<int:page>/<int:size>/<user>/<condition>')
        api.add_resource(ApiModel, '/Model',
                         '/Model/<int:page>/<int:size>',
                         '/Model/<int:model_id>',
                         '/ModelQuery/<condition>',
                         '/ModelQuery/<int:page>/<int:size>/<condition>')
        api.add_resource(ApiModelTags,
                         '/ModelTag/<int:model_id>',  # 取Model的关联的TAG
                         '/ModelDSDocTag/<int:model_id>/<doc_type>'  # 取Model下设计文档关联的TAG
                         )
        api.add_resource(ApiModelTree,  # 获取左边的Model树
                         '/ModelTree',
                         '/ModelTree/<int:user_id>')
        api.add_resource(ApiDesignTop, '/DesignTop/<int:proj_id>',
                         '/DesignTop/<int:proj_id>/<type>')  # 开发设计书TOP页表格数据
        api.add_resource(ApiModelAuthor,  # 获取Model相关联的负责人和担当
                         '/ApiModelAuthor/<int:proj_id>/<int:model_id>')
        api.add_resource(ApiModelRefGet, '/ModelRefGet',
                         '/ModelRefGet/<int:doc_id>'  # 获取该设计书所属模块的关联模块
                         )
        api.add_resource(ApiModelRefPost, '/ModelRefPost', )
        api.add_resource(ApiSubModel, '/SubModel/<int:proj_id>')
        api.add_resource(ApiSectionTags, '/SectionTag/<int:sec_id>')  # 获取章节的TAG树
        # DS DOC(设计文档)
        api.add_resource(ApiDSDoc, '/DSDoc', '/DSDoc/<int:doc_id>',
                         '/DSDoc/<int:doc_id>/<type>',
                         '/DSDoc/<int:_id>/<type>/<commit_user>')
        api.add_resource(ApiDSDocType, '/DSDocType')  # 方档类别
        api.add_resource(ApiDSDocStatus, '/DSDocStatus')  # 方档状态
        api.add_resource(ApiDSectionType, '/DSSectionType')  # 章节类别
        api.add_resource(ApiDSDoc2, '/DSDoc2/<int:model_id>/<string:doc_type>/<int:tag_id>')  # tag下的设计文档
        api.add_resource(ApiComment, '/Comment', '/Comment/<int:sec_id>')
        api.add_resource(ApiDSDocSpec, '/ApiDSDocSpec',
                         '/ApiDSDocSpec/<int:doc_id>',
                         '/ApiDSDocSpec/<int:doc_id>/<string:search_str>')
        api.add_resource(ApiDSDocUsecase, '/ApiDSDocUsecase',
                         '/ApiDSDocUsecase/<int:doc_id>')
        api.add_resource(ApiCopyBasicToDetail, '/CopyBasicToDetail',
                         '/CopyBasicToDetail/<int:proj_id>/<int:model_id>')
        api.add_resource(ApiNewDSDoc,  '/NewDSDoc',  # 新增设计书
                         '/NewDSDoc/<int:doc_id>')  # 设计书（查看）
        api.add_resource(ApiTestDelCache, '/TestDelCache/<int:proj_id>')  # （测试用）删除cache
        api.add_resource(ApiUpDocVer, '/UpDocVer')  # 升级文档版本
        # 文档的Astah附件
        api.add_resource(ApiDSDocAstah,
                         '/DSDocAstah',
                         '/DSDocAstah/<int:doc_id>',
                         '/DSDocAstah/<int:doc_id>/<commit_user>/<int:attach_id>')
        # 式样书的附件
        api.add_resource(ApiDSDocInput,
                         '/DSDocInput',
                         '/DSDocInput/<int:proj_id>/<string:_type>',
                         '/DSDocInput/<commit_user>/<int:spec_id>/<int:ver_id>')

        api.add_resource(ApiDSDocInputGet,
                         '/DSDocInputBatch',
                         '/DSDocInputById/<int:proj_id>',
                         '/DSDocSpecById/<int:spec_id>',
                         '/DSDocSpecNum/<int:proj_id>/<string:_type>')
        # .h文件和文件夹上传
        api.add_resource(ApiDSDocImport,
                         '/DSDocIfDel/<int:h_id>',              # 删除IF头文件
                         '/DSDocImport')
        # BugAnalysis搜索
        api.add_resource(ApiBugSearch,
                         '/BugSearch',)                        # 搜索AnyPlace列表
        api.add_resource(ApiAnyPlaceInfo, '/AnyPlaceInfo')     # 搜索AnyPlace单条
        api.add_resource(ApiKeyList,
                         '/GetKeyListByUser/<string:user>',    # 关键字补全获取某人的
                         '/GetKeyList')                        # 关键字补全获取
        # DS Section
        api.add_resource(ApiDSection, '/Section',
                         '/Section/<int:doc_id>/<sec_type>',
                         '/Section/<int:sec_id>/<sec_type>/<condition>')
        api.add_resource(ApiAllUsecase, '/AllUsecase/<int:doc_id>')
        api.add_resource(ApiKnowledgeDoc, '/KnowledgeDoc/<int:sec_id>')
        api.add_resource(ApiUsecaseDetail, '/UsecaseDetail/<int:usecase_id>')
        api.add_resource(ApiNewDsSection, '/NewDsSection',
                         '/NewDsSection/<int:doc_id>/<sec_type>')
        api.add_resource(ApiDsUcSub, '/DsUcSub',  # usecase子章节编辑接口
                         '/DsUcSub/<int:usecase_id>/<sec_type>')
        api.add_resource(ApiDSUcLevel2, '/DSUcLevel2',  # 第二级别的usecase编辑接口
                         '/DSUcLevel2/<int:usecase_id>')
        # 章节(UserCase)Consider
        api.add_resource(ApiDSConsider, '/DSConsider',
                         '/DSConsider/<int:sec_id>',
                         '/DSConsider/<int:sec_id>/<csd_range>')
        # DS式样书
        api.add_resource(ApiDSRelSpec, '/DSRelSpec', '/DSRelSpec/<int:sec_id>')
        api.add_resource(ApiUcRelSpec, '/UcRelSpec', '/UcRelSpec/<int:doc_id>')
        # 场景
        api.add_resource(ApiDSScene, '/Scene',
                         '/Scene/<int:doc_id>',
                         '/Scene/<int:doc_id>/<type>')
        api.add_resource(ApiDSTag, '/DSTag', '/DSTag/<int:doc_id>')
        # 着眼点（failure）
        api.add_resource(ApiDSFailure, '/Failure')
        # 上传下载
        api.add_resource(ApiUploadImage, '/UploadImage')
        api.add_resource(DownFile, '/DownFile', '/DownFile/<path:path_info>')
        api.add_resource(ImageSize, '/ImageSize/<path:image_url>')
        # 设计方档模板
        api.add_resource(ApiDSDocTemplate,
                         '/DSDocTemplate',
                         '/DSDocTemplate/<doc_type>')
        # Project
        api.add_resource(ApiProject, '/Project', '/Project/<int:proj_id>',
                         '/Project/<int:page>/<int:size>',
                         '/ProjectQuery/<int:page>/<int:size>/<condition>',
                         '/Project/<int:proj_id>/<commit_user>')
        api.add_resource(ApiMergeCactusProject, '/MergeCactusProject')   # 合并cactus上的项目
        api.add_resource(ApiGetCactusProject, '/GetCactusProject')  # 从cactus上拿项目
        api.add_resource(ApiProjectFW, '/ProjectFW', '/ProjectFW/<int:proj_id>')
        api.add_resource(ApiProjectTag, '/ProjectTag', '/ProjectTag/<int:proj_id>')
        api.add_resource(ApiProjectModel, '/ProjectModel', '/ProjectModel/<int:proj_id>')
        api.add_resource(ApiProjectGroup, '/ApiProjectGroup', '/ApiProjectGroup/<int:proj_id>')
        # 资源
        api.add_resource(ApiResource, '/Resource')
        # IF
        api.add_resource(ApiDsDocIf,
                         '/DsDocIf',
                         '/DsDocIf/<int:doc_id>',
                         '/DsDocIf/<int:doc_id>/<commit_user>')
        # 式样书
        api.add_resource(ApiSpecification,
                         '/Specification',
                         '/Specification/<int:proj_id>/<string:search_str>')
        api.add_resource(ApiUsecaseSpec, '/UsecaseSpec/<int:proj_id>')
        # 式样书全文检索接口
        api.add_resource(ApiFunSearch, '/FunSearch/<proj_name>/<search>')
        # 平台框架
        api.add_resource(ApiFramework, '/Framework',
                         '/Framework/<int:fw_id>',
                         '/Framework/<type>/<int:fw_id>',
                         '/Framework/<int:fw_id>/<commit_user>')
        api.add_resource(ApiGetCactusFw, '/GetCactusFw')
        api.add_resource(ApiFwProject, '/FwProject/<int:fw_id>')
        api.add_resource(ApiJournal,  # 日志前后两版比较的接口
                         '/JournalDiff/<int:key_id>',
                         '/JournalDiff/<int:key_id>/<left_version>/<right_version>',
                         '/JournalDiff/<int:key_id>/<left_version>/<right_version>/<log_type>')
        api.add_resource(ApiJournalVersion,  # 日志版本信息
                         '/JournalVersion/<int:key_id>')
        api.add_resource(ApiImportFWModel, '/ImportFWModel')
        api.add_resource(ApiImportProjectModel, '/ImportProjectModel',
                         '/ImportProjectModel/<project_name>')
        api.add_resource(ApiExportDoc,
                         '/ExportDoc/<int:proj_id>',
                         '/ExportDoc/<int:proj_id>/<int:model_id>',
                         '/ExportDoc/<int:proj_id>/<int:model_id>/<string:doc_type>',
                         '/ExportDoc/<int:proj_id>/<int:model_id>/<string:doc_type>/<int:doc_id>')
        # api.add_resource(ApiImportDsDoc, '/ImportDsDoc')  # 后台导入时使用
        # api.add_resource(ApiImportIfDoc, '/ImportIfDoc')  # 后台导入时使用
        api.add_resource(ApiWebImportDoc, '/WebImportDsDoc')
        api.add_resource(ApiDRBFM, '/drbfm/<int:doc_id>')
        api.add_resource(ApiDrbfmExport, '/DrbfmExport/<int:proj_id>/<int:doc_id>')
        api.add_resource(ApiExcelHtm, '/ExcelToHtm')

