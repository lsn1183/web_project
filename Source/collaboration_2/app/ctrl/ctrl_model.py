# -*- coding: UTF-8 -*-
import pandas as pd
import copy
from app.db import db, cache
from flask import current_app
from sqlalchemy import or_, and_
from app.db.model import Model
from app.db.project import ProjectModelRef
from app.db.ds_doc import Ds_Doc
from app.db.framework import FrameworkModel
from app.db.project import ProjectModel
from app.db.project import ProjectModelRel
from app.db.ds_model_tag_rel import DsModelTagRel
from app.ctrl.ctrl_doc_tag import CtrlDocTag
from app.ctrl.ctrl_ds_section import CtrlDSSection
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_ds_doc import CtrlDsDoc
from app.db.ds_doc import DSDocType
from app.db.group import GroupModel
DOC_TYPE = {'BASIC': '基本设计', 'DETAIL': '详细设计'}


class CtrlModel(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def get(self, page, size, model_id, condition):
        model_q = db.session.query(Model)
        if model_id:
            model_q = model_q.filter(Model.model_id == model_id)
        elif condition:
            model_q = model_q.filter(Model.title.ilike('%'+condition+'%'))
        model_q = model_q.order_by(Model.code, Model.model_id)
        count = None
        if page and size:
            count = model_q.count()
            model_q = model_q.limit(size).offset(size * (page - 1))
        model_list = []
        for model in model_q:
            model_list.append(model.to_dict())
        return count, model_list

    def get_name_by_model_id(self, model_id):
        q = db.session.query(Model).filter(Model.model_id == model_id).first()
        if q:
            return q.title
        else:
            return None

    def add(self, data_json):
        model_id = data_json.get(Model.model_id.name)
        try:
            if not model_id:
                if "model_id" in data_json:
                    data_json.pop("model_id")
                db.session.add(Model(**data_json))
            else:
                db.session.query(Model).filter(Model.model_id == model_id).update(data_json)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def get_model_sub(self, proj_id, model_id, model_list):
        q = (db.session.query(ProjectModelRel)
             .filter(and_(ProjectModelRel.proj_id == proj_id,
                          ProjectModelRel.parent_model_id == model_id)).all())
        for model in q:
            model_id = model.model_id
            model_list.append(model_id)
            self.get_model_sub(proj_id, model_id, model_list)

    def delete(self, model_id):
        try:
            q_pro = db.session.query(ProjectModel).filter(ProjectModel.model_id == model_id).all()
            q_fw = db.session.query(FrameworkModel).filter(FrameworkModel.model_id == model_id).all()
            if q_pro or q_fw:
                return False, "有项目和平台存在该模块，无法删除！"
            # db.session.query(FrameworkModelRel).filter(FrameworkModelRel.model_id == model_id).delete()
            # db.session.query(FrameworkModel).filter(FrameworkModel.model_id == model_id).delete()
            # db.session.query(ProjectModelRel).filter(ProjectModelRel.model_id == model_id).delete()
            # db.session.query(ProjectModel).filter(ProjectModel.model_id == model_id).delete()
            db.session.query(Model).filter(Model.model_id == model_id).delete()
            db.session.commit()
            return model_id, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_projId_list(self, fw_id):
        from app.ctrl.ctrl_framework import CtrlFramework
        pro_list = CtrlFramework().get_fw_project(fw_id)
        proj_id_list = []
        for pro in pro_list:
            proj_id_list.append(pro.get('proj_id'))
        return proj_id_list

    def get_doc_by_type(self, username, fw_id, model_id, proj_id, doc_type, page, size, condition):
        querys = db.session.query(Ds_Doc.doc_id, Ds_Doc.title, Ds_Doc.summary, Ds_Doc.doc_type,
                                  Ds_Doc.proj_id, Ds_Doc.model_id,
                                  Model.title).outerjoin(Model, Ds_Doc.model_id == Model.model_id)
        model_list = []
        if model_id and proj_id:  # 根据模块id查询文档
            model_list.append(model_id)
            self.get_model_sub(proj_id, model_id, model_list)
            querys = querys.filter(and_(Ds_Doc.model_id.in_(model_list),
                                        Ds_Doc.proj_id == proj_id))
        elif not model_id and proj_id:
            querys = querys.filter(Ds_Doc.proj_id == proj_id)
        elif fw_id:
            proj_id_list = self.get_projId_list(fw_id)
            querys = querys.filter(Ds_Doc.proj_id.in_(proj_id_list))
        if doc_type != 'ALL':
            querys = querys.filter(Ds_Doc.doc_type == doc_type)
        if username.strip():
            querys = querys.filter(Ds_Doc.creator == username)
        if condition:
            querys = querys.filter(or_(Ds_Doc.title.ilike('%'+condition+'%'),
                                       Ds_Doc.summary.ilike('%'+condition+'%')))
        querys = querys.order_by(Ds_Doc.doc_type, Model.title, Ds_Doc.title)
        ds_docs = []
        count = querys.count()
        querys = querys.limit(size).offset(size * (page - 1))
        for query in querys:
            ds_doc = dict()
            ds_doc[Ds_Doc.doc_id.name] = query[0]
            ds_doc[Ds_Doc.title.name] = query[1]
            ds_doc[Ds_Doc.summary.name] = query[2]
            ds_doc[Ds_Doc.doc_type.name] = query[3]
            ds_doc[Ds_Doc.proj_id.name] = query[4]
            ds_doc[Ds_Doc.model_id.name] = query[5]
            ds_doc['model'] = query[6]
            ds_docs.append(ds_doc)
        return count, ds_docs

    def get_tag_by_model(self, model_id):
        querys = DsModelTagRel.query.filter(DsModelTagRel.model_id == model_id).all()
        tag_id_list = []
        for query in querys:
            tag_id_list.append(query.tag_id)
        tags = self._get_tag_list(tag_id_list)
        return tags

    def _get_tag_list(self, tag_id_list):
        ctrl_tag = CtrlDocTag()
        tags = []
        for tag_id in tag_id_list:
            tag = {'tag_id': tag_id}
            tag_name = ctrl_tag.get_tag_by_id(tag_id)
            if tag_name:
                tag['tag'] = tag_name
                tags.append(tag)
        return tags

    def model_doc_tree(self, doc_list):
        ctrl_section = CtrlDSSection()
        model_doc_tree = [{"label": "基本设计", "type": "design", "children": []},
                          {"label": "详细设计", "type": "design", "children": []}]
        for doc in doc_list:
            doc_dict = dict()
            doc_id = doc.get('doc_id')
            lable = doc.get('title')
            doc_dict['id'] = str(doc_id)
            doc_dict['type'] = 'doc'
            doc_dict['label'] = lable
            doc_section = ctrl_section.get_sections(doc_id)
            doc_sub = self.section_tree(doc_id, doc_section)
            doc_dict['children'] = doc_sub
            if doc.get('doc_type') == 'BASIC':
                model_doc_tree[0].get('children').append(doc_dict)
            elif doc.get('doc_type') == 'DETAIL':
                model_doc_tree[1].get('children').append(doc_dict)
        return model_doc_tree

    def section_tree(self, doc_id, doc_section):
        doc_sub = []
        i = 1
        for key in doc_section:
            # if key == "SUMMARY":
            sub_dict = {'id': str(doc_id)+'-'+str(i), "label": key, "type": "section", "children": []}
            doc_sub.append(sub_dict)
            i += 1
            # else:
                # sub_dict = {"lable": key, "type": "section"}
                # sec_list = doc_section.get(key)
                # for sec in sec_list:
                #     id = sec.get('sec_id')
                #     label = sec.get('title')
                #     sec_sub = {'id': id, 'label': label, 'sub': [], 'type': "section"}
                #     sub_dict["sub"].append(sec_sub)
                # doc_sub.append(sub_dict)
        return doc_sub

    # @cache.memoize(timeout=7200)
    def get_model_top(self, proj_id, type):
        """
        开发设计书TOP页表格数据
        :param proj_id:
        :param type: ALL:显示所有的模块；PART:只显示有设计书的（TODO）
        :return:
        """
        print('重新加载缓存！proj_id=%s, type=%s' % (proj_id, type))
        print("模块开始时间："+self.get_current_time())
        model_list, top_list = self.get_models(proj_id, type)
        # print("模块结束时间：" + self.get_current_time())
        other_list = ["unit_test", "interface_test", "function_test"]
        basic_list = [
            {
                "name": '基本设计',
                "field": 'basic_design'
            },
            {
                "name": 'IF式样书',
                "field": 'IF_stylebook'
            },
            {
                "name": '详细设计',
                "field": 'detail_design'
            },
            {
                "name": '单元测试',
                "field": 'unit_test'
            },
            {
                "name": '接口测试',
                "field": 'interface_test'
            },
            {
                "name": '机能测试',
                "field": 'function_test'
            },
        ]
        sqlcmd = """SELECT doc_id, doc_type, ver, model_id FROM ds.ds_doc """
        df = pd.read_sql(sqlcmd, con=db.session.bind)
        df.set_index("model_id")
        # print("文档开始时间：" + self.get_current_time())
        for model in model_list:
            for title in top_list:
                if not model.get(title):
                    model[title] = {"id": 0, "title": ""}
            for title in other_list:
                # 暂时TODO以后待做
                if not model.get(title):
                    model[title] = {"id": 0, "title": "TODO"}
            model['basic_design'] = {"id": 0, "title": "TODO"}
            model['detail_design'] = {"id": 0, "title": "TODO"}
            model['IF_stylebook'] = {"id": 0, "title": "TODO"}
            model_id = model[model.get('sub_level')].get('id')
            model_df = df[df["model_id"] == model_id]
            basic_df = model_df[model_df["doc_type"] == "BASIC"]
            detail_df = model_df[model_df["doc_type"] == "DETAIL"]
            if_df = model_df[model_df["doc_type"] == "IF"]
            basics = basic_df[['doc_id', 'ver']].to_dict(orient='records')
            details = detail_df[['doc_id', 'ver']].to_dict(orient='records')
            ifs = if_df[['doc_id', 'ver']].to_dict(orient='records')
            if basics:
                model['basic_design'] = {"id": basics[0].get("doc_id"), "title": basics[0].get("ver")}
            if details:
                model['detail_design'] = {"id": details[0].get("doc_id"), "title": details[0].get("ver")}
            if ifs:
                model['IF_stylebook'] = {"id": ifs[0].get("doc_id"), "title": ifs[0].get("ver")}
        # print("文档结束时间：" + self.get_current_time())
        dynamic_list = []
        for top in top_list:
            dynamic_list.append({"name": top, "field": top})
        return {"dynamic_list": dynamic_list, "basic_list": basic_list, "model_list": model_list}

    def get_models(self, proj_id, type):
        model_list = []
        top_list = []
        sql = """select t1.model_id, title from ds.model t1 left join ds.project_models t2 
                 on t1.model_id = t2.model_id where t2.proj_id = {proj_id} and t2.model_id not in 
                 (select model_id from ds.project_models_rel) order by title""".format(proj_id=proj_id)
        df = pd.read_sql(sql, con=db.session.bind)
        data_list = df[['model_id', 'title']].to_dict(orient='records')
        for data in data_list:
            model_dict = {"layer1": {"id": data["model_id"], "title": data["title"]}}
            self._sub_model(type, model_dict, data["model_id"], proj_id, model_list, top_list)
        return model_list, top_list

    def _sub_model(self, type, model_dict, model_id, proj_id, model_list, top_list, level=1):
        model_sub_q = (db.session.query(Model)
                       .outerjoin(ProjectModelRel, Model.model_id == ProjectModelRel.model_id)
                       .filter(and_(ProjectModelRel.proj_id == proj_id,
                                    ProjectModelRel.parent_model_id == model_id))
                       .order_by(Model.title).all())
        if "layer%s" % str(level) not in top_list:
            top_list.append("layer%s" % str(level))
        if len(model_sub_q):
            for sub in model_sub_q:
                down_level = level + 1
                model_dict["layer%s" % str(down_level)] = {"id": sub.model_id, "title": sub.title}
                self._sub_model(type, model_dict, sub.model_id, proj_id, model_list, top_list, down_level)
                model_dict = dict()
        else:
            model_dict["sub_level"] = "layer%s" % str(level)
            if type == "PART":
                doc_dict = CtrlDsDoc().get_latest_doc(model_id)
                if doc_dict.get('doc_id'):
                    model_list.append(model_dict)
            else:
                model_list.append(model_dict)

    @cache.cached(timeout=7200, key_prefix='get_model_tree')
    def get_model_tree(self, **kwargs):
        print('重新加载缓存！')
        """
        :param kwargs: user_id: "BASIC"/"DETAIL"
        :return: Tree(FW->Project->Model)
        """
        sqlcmd = """
        SELECT t1.fw_id, fw_name, t2.proj_id, proj_name,
               t3.model_id, t5.title, parent_model_id,
               doc_id, t7.title as doc_title, doc_type
          FROM ds.framework as t1
          inner join ds.project_framework_rel as t2
          on t1.fw_id = t2.fw_id
          INNER JOIN ds.project_models as t3
          on t2.proj_id = t3.proj_id
          left join ds.project_models_rel as t4 
          on t3.model_id = t4.model_id and t2.proj_id = t4.proj_id
          left join ds.model as t5
          on t3.model_id = t5.model_id
          LEFT JOIN ds.project AS t6
          on t3.proj_id = t6.proj_id
          left join ds.ds_doc as t7
          on t2.proj_id = t7.proj_id and t3.model_id = t7.model_id
          ORDER BY fw_name, t2.proj_id, parent_model_id is not null, doc_type, doc_title
        """
        model_df = pd.read_sql(sqlcmd, db.session.bind)
        # ## 通过Model和文档类别过滤
        user_id = kwargs.get("user_id")
        if user_id:
            # filter_tags = self._get_tags_by_model(model_id, doc_type)
            # filter_df = self.filter_tags(tag_df, filter_tags)
            # if filter_df is None:
            #     return []
            # filter_df = filter_df.sort_values(["parent_tag_id", "tag_id"])
            pass
        doc_types = self._get_doc_typs()
        filter_df = model_df
        filter_df.set_index(keys=["fw_id", "fw_name", "proj_id", "proj_name"],
                            drop=False)
        # filter_df.to_dict(orient='records')
        fw_ids = filter_df.fw_id.unique()
        model_forest = []
        for fw_id in fw_ids:
            one_fw_df = filter_df[filter_df["fw_id"] == fw_id]
            proj_ids = one_fw_df.proj_id.unique()
            # print(one_fw_df)
            # print(one_fw_df.iloc[0]['fw_name'])
            fw_dict = {"id": int(fw_id),
                       "title": one_fw_df.iloc[0]['fw_name'],
                       "type": "framework",
                       "sub": []}
            for proj_id in proj_ids:
                one_proj_df = one_fw_df[one_fw_df["proj_id"] == proj_id]
                proj_dict = {"id": int(proj_id),
                             "title": one_proj_df.iloc[0]['proj_name'],
                             "type": "project",
                             "sub": []}
                doc_df = one_proj_df[["proj_id", "model_id", "doc_id",
                                      "doc_title", "doc_type"]]
                doc_df = doc_df.dropna(subset=["doc_id"])
                # doc_df["proj_id"] = pd.Series([proj_id] * len(doc_df))
                # print(doc_df)
                one_proj_df = one_proj_df[["fw_id", "proj_id", "model_id",
                                           "title", "parent_model_id"]]
                one_proj_df = one_proj_df.drop_duplicates(keep='first',
                                                          inplace=False)
                type_list = ["model"] * len(one_proj_df)
                one_proj_df = one_proj_df.assign(type=type_list)
                one_proj_df.rename(columns={"model_id": "id"}, inplace=True)
                # 求子孙Model
                model_list = self.df_2_tree(one_proj_df,
                                            key_col="id",
                                            parent_col="parent_model_id",
                                            parent_val=None,
                                            drop_cols=["parent_model_id"],
                                            doc_types=doc_types,
                                            doc_df=doc_df)
                proj_dict["sub"] = model_list
                fw_dict["sub"].append(proj_dict)
            model_forest.append(fw_dict)
        return model_forest

    def _get_doc_typs(self):
        doc_types = CtrlDsDoc().get_doc_type(orient='list')
        for doc_type in doc_types:
            doc_type["id"] = doc_type.pop(DSDocType.doc_type.name)
            doc_type["title"] = doc_type.pop(DSDocType.describe.name)
            doc_type["type"] = "doc_type"
            doc_type["sub"] = []
        return doc_types

    def df_2_tree(self, df, key_col, parent_col, parent_val=None,
                  drop_cols=None, doc_types=None, doc_df=None):
        if parent_val is None:
            root_df = df[df[parent_col].isnull()]
        else:
            root_df = df[df[parent_col] == parent_val]
        root_list = root_df.to_dict(orient='records')
        self.get_subs(root_list, df, key_col, parent_col,
                      drop_cols, doc_types, doc_df=doc_df)
        return root_list

    def get_subs(self, root_list, df, key_col, parent_col,
                 drop_cols=None, doc_types=None, doc_df=None):
        for node_info in root_list:
            key_val = node_info.get(key_col)
            if drop_cols:
                for col in drop_cols:
                    node_info.pop(col)
            sub_df = df[df[parent_col] == key_val]
            sub_num = len(sub_df)
            if sub_num:
                sub_tag_list = sub_df.to_dict(orient='records')
                node_info["sub"] = sub_tag_list
                self.get_subs(sub_tag_list, df, key_col, parent_col,
                              drop_cols=drop_cols, doc_types=doc_types,
                              doc_df=doc_df)
            else:
                if doc_types:
                    doc_types = copy.deepcopy(doc_types)
                    for doc_type in doc_types:
                        for key, val in node_info.items():
                            if key not in doc_type:
                                doc_type[key] = val
                        doc_type[parent_col] = node_info[key_col]
                        # 文档
                        if doc_df is None or doc_df.empty:
                            doc_type["sub"] = []
                        else:
                            doc_type["sub"] = self._get_docs(key_val, doc_type["id"], doc_df)
                    node_info["sub"] = doc_types
                else:
                    node_info["sub"] = []

    def _get_docs(self, model_id, doc_type, doc_df):
        # print("doc_df\n", doc_df)
        docs = doc_df[doc_df["model_id"] == model_id]
        docs = docs[docs["doc_type"] == doc_type]
        docs.drop_duplicates(inplace=True)
        docs.rename(columns={"doc_id": "id", "doc_title": "title"},
                    inplace=True)
        # print("docs\n", docs)
        doc_info_list = docs.to_dict(orient='records')
        for doc_info in doc_info_list:
            doc_info["type"] = 'doc'
            doc_info["sub"] = []
        return doc_info_list

    def get_authors(self, proj_id, model_id):
        q = (db.session.query(GroupModel)
             .filter(# GroupModel.proj_id == proj_id, TODO@hcz:暂时没有
                     GroupModel.model_id == model_id)
             .order_by(GroupModel.gid))
        from app.ctrl.ctrl_group import CtrlGroup
        group = CtrlGroup()
        group_members = []
        for group_model in q:
            group_members += group.get_group_members(group_model.group_id)
        return group_members

    def get_model_ref_model(self, data_json):
        from app.ctrl.ctrl_project import CtrlProject
        from app.ctrl.ctrl_group import CtrlGroup
        proj_id = data_json.get('proj_id')
        accessToken = data_json.get('accessToken')
        username = data_json.get('username')
        try:
            if username in ("Admin", "Test_PMO", "Test_PL", "Test_GL"):
                model_list = CtrlProject().get_leaf_model(proj_id)
            else:
                project_root = CtrlGroup().get_project_root(accessToken, proj_id)
                if not project_root:
                    return None, "您不在该项目体制中！"
                pmo = project_root.get('pmo')
                pl_username = project_root.get('username')
                if username == pmo.get('userName'):
                    model_list = CtrlProject().get_leaf_model(proj_id)
                elif pl_username == username:
                    model_list = CtrlProject().get_leaf_model(proj_id)
                else:
                    group_members = project_root.get('group_members')
                    model_list = self.get_gl_model_list(group_members, username)
            data_list = []
            for model in model_list:
                model_id = model.get('model_id')
                model_ref = self.get_model_ref(proj_id, model_id)
                model['model_ref'] = model_ref
                model['model_list'] = []  # 前端要求加的
                data_list.append(model)
            return data_list, None
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            return None, "服务异常！请联系管理员！"

    def get_gl_model_list(self, group_members, username):
        from app.ctrl.ctrl_group import CtrlGroup
        model_list = []
        for group in group_members:
            if username == group.get('username') and group.get('user_role') == 'GL':
                model_list += CtrlGroup().get_model_by_group(group.get('group_name'))
        return model_list

    def update_model_ref_model(self, data_json):
        try:
            update_time = self.get_current_time()
            commit_user = data_json.get('commit_user')
            proj_id = data_json.get('proj_id')
            model_list = data_json.get('model_list')
            if not proj_id:
                return False, '没有指定项目ID!'
            new_data_list = []
            old_data_list = []
            for model in model_list:
                model_id = model.get('model_id')
                model_ref = model.get('model_ref')
                old_rel_list = self.get_old_data(ProjectModelRef, [ProjectModelRef.proj_id, ProjectModelRef.model_id],
                                                 {'proj_id': proj_id, 'model_id': model_id})
                for mf in model_ref:
                    new_data = {'proj_id': proj_id, 'model_id': model_id, 'ref_model_id': mf.get('model_id')}
                    for old_data in old_rel_list:
                        if (model_id == old_data.get('model_id')
                                and new_data.get('ref_model_id') == old_data.get('ref_model_id')):
                            new_data['gid'] = old_data.get('gid')
                    new_data_list.append(new_data)
                old_data_list += old_rel_list
            commit_log = self.add_list(ProjectModelRef, new_data_list, old_data_list, ProjectModelRef.gid, [])
            self.commit_log(commit_log, commit_user, update_time)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_model_ref(self, proj_id, model_id):
        q = (db.session.query(Model.model_id, Model.title)
             .outerjoin(ProjectModelRef, Model.model_id == ProjectModelRef.ref_model_id)
             .filter(ProjectModelRef.model_id == model_id)
             .filter(ProjectModelRef.proj_id == proj_id)
             .order_by(Model.title))
        model_list = []
        for model in q:
            model_dict = dict()
            model_dict['model_id'] = model[0]
            model_dict['title'] = model[1]
            model_list.append(model_dict)
        return model_list

    def get_sub_model(self, proj_id):
        """
        取所有的子模块
        :param proj_id:
        :param model_id:
        :return:
        """
        model_list = self.get_all_model_sub(proj_id)
        return model_list

    def get_all_model_sub(self, proj_id):
        from app.ctrl.ctrl_project import CtrlProject
        model_list = CtrlProject().get_models(proj_id)
        data_list = []
        model_id_list = []
        for model in model_list:
            model_id = model.get('model_id')
            model.pop('parent_title')
            if model_id in model_id_list:
                continue
            model_id_list.append(model_id)
            data_list.append(model)
        return data_list

    def get_model_ref_by_doc_id(self, doc_id):
        """获取该设计书所属模块的关联模块
        """
        rst_model_list, model_list = [], []
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        doc_info = CtrlDsDoc().get_doc(doc_id)
        if not doc_info:
            return [], '指定的设计书不存在！'
        proj_id, model_id = doc_info.get("proj_id"), doc_info.get("model_id")
        curr_model = self._get_model_by_doc_id(doc_id)
        if curr_model:
            model_list.append({"model_id": curr_model.get("model_id"),
                               "title": curr_model.get("title")})
        model_list += self.get_model_ref(proj_id, model_id)
        if not model_list:
            return [], '没有关联模块！'
        for model in model_list:
            model["model_name"] = model.pop('title')
            model["checked"] = False
            model["failure_id_list"] = {'havething_list': [], 'nothing_list': []}
            rst_model_list.append(model)
        return rst_model_list, 'OK'

    def _get_model_by_doc_id(self, doc_id):
        from app.db.ds_doc import Ds_Doc
        from app.db.model import Model
        q = (db.session.query(Model)
             .outerjoin(Ds_Doc, Model.model_id == Ds_Doc.model_id)
             .filter(Ds_Doc.doc_id == doc_id))
        model = q.first()
        if model:
            return model.to_dict()
        return dict()


