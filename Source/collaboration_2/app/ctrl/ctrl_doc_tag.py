# -*- coding: UTF-8 -*-
import pandas as pd
from app.db.doc_tag_cat import DBDocTagCat
from app.db.ds_model_tag_rel import DsModelTagRel
from app.db import db
TAG_RATE_NOR = 'normal'
TAG_RATE_OFTEN = 'often'
TAG_RATE_ALL = 'all'
FW_TAG = '平台'
PROJ_TAG = '项目'
from flask import current_app


class CtrlDocTag(object):
    def __init__(self):
        pass

    # def get_tag_tree2(self, valid=False):
    #     doc_tags = (DBDocTagCat.query.filter()
    #                 .order_by(DBDocTagCat.parent_tag_id, DBDocTagCat.tag_id)
    #                 .all()
    #                 )
    #     tag_dict = {}
    #     for doc_tag in doc_tags:
    #         tag_info = doc_tag.to_dict()
    #         parent_tag_id = doc_tag.parent_tag_id
    #         if not parent_tag_id:
    #             tag_info["sub_tags"] = list()
    #             tag_dict[tag_info["tag_id"]] = tag_info
    #         else:
    #             p_tag_info = tag_dict.get(parent_tag_id)
    #             if p_tag_info:
    #                 sub_tags = p_tag_info["sub_tags"]
    #                 tag_info["parent_tag"] = p_tag_info.get("tag")
    #                 sub_tags.append(tag_info)
    #     tag_list = sorted(tag_dict.itervalues(),
    #                       key=lambda x: x.get("tag_id"))
    #     return tag_list

    def get_tag_tree(self, **agv):
        """
        :param agv: mode_id, doc_type: "BASIC"/"DETAIL"
        :return:
        """
        rate = agv.get("rate")
        if not rate or rate == TAG_RATE_ALL:
            statement = (db.session.query(DBDocTagCat)
                         .filter()
                         .order_by(DBDocTagCat.parent_tag_id,
                                   DBDocTagCat.tag_id)
                         .statement)
        else:
            statement = (db.session.query(DBDocTagCat)
                         .filter(DBDocTagCat.rate == rate)
                         .order_by(DBDocTagCat.required.desc(),
                                   DBDocTagCat.parent_tag_id,
                                   DBDocTagCat.tag_id)
                         .statement)
        tag_df = pd.read_sql(statement, db.session.bind)
        # ## 通过Model和文档类别过滤
        model_id = agv.get("model_id")
        sec_id = agv.get("sec_id")
        if model_id:
            doc_type = agv.get("doc_type")
            filter_tags = self._get_tags_by_model(model_id, doc_type)
            filter_df = self.filter_tags(tag_df, filter_tags)
            if filter_df is None:
                return []
            filter_df = filter_df.sort_values(["parent_tag_id", "tag_id"])
        elif sec_id:
            filter_tags = []
            from app.ctrl.ctrl_ds_section import CtrlDSSection
            sec_tags = CtrlDSSection().get_tags(sec_id)
            for tag in sec_tags:
                filter_tags.append(tag.get("tag_id"))
            filter_df = self.filter_tags(tag_df, filter_tags)
            if filter_df is None:
                return []
            filter_df = filter_df.sort_values(["parent_tag_id", "tag_id"])
        else:
            filter_df = tag_df
        # print(filter_df)
        # ## 第一级Tags
        root_df = filter_df[filter_df["parent_tag_id"] == 0]
        # print(root_df)
        # 求子孙TAG
        tag_list = root_df.to_dict(orient='records')
        self._get_sub_tags(tag_list, filter_df)
        return tag_list

    def get_tag_tree_include_number(self, **agv):
        rate = agv.get("rate")
        username = agv.get("username")
        role = agv.get("role")
        if not rate or rate == TAG_RATE_ALL:
            statement = (db.session.query(DBDocTagCat)
                         .filter()
                         .order_by(DBDocTagCat.parent_tag_id,
                                   DBDocTagCat.tag_id)
                         .statement)
        else:
            statement = (db.session.query(DBDocTagCat)
                         .filter(DBDocTagCat.rate == rate)
                         .order_by(DBDocTagCat.parent_tag_id,
                                   DBDocTagCat.tag_id)
                         .statement)
        tag_df = pd.read_sql(statement, db.session.bind)
        # ## 通过用户名过滤
        tag_docs = self._get_tag_docs(username)
        filter_df = self.filter_tags_by_user(tag_df, username, tag_docs)
        if filter_df is None:
            return []
        filter_df = filter_df.sort_values(["parent_tag_id", "tag_id"])
        filter_df["type"] = ["tag"] * len(filter_df)
        # ## 第一级Tags
        if role:
            root_df = filter_df[filter_df["parent_tag_id"] == 0]
        else:
            root_df = filter_df[filter_df["tag"] == "技术专题"]
        tag_list = root_df.to_dict(orient='records')
        # 求子孙TAG
        self._get_sub_tags(tag_list, filter_df)
        # 计TAG结点和叶子的文档数量
        self._count_doc_num(tag_list, tag_docs)
        return tag_list

    def get_technology_tag(self, rate, username):
        tag_list = self.get_tag_tree_include_number(rate=rate, username=username)
        if username:
            tag = "我的知识库"
        else:
            tag = "知识库"
        tag_head_tree = [
            {
                'tag': tag,
                'required': True,
                'disabled': True,
                "sub_tags": [
                    {
                        'tag': '知识点分类',
                        'type': 'tag',
                        'required': True,
                        'disabled': True,
                        "sub_tags": tag_list,
                    },
                ]
            }

        ]
        return tag_head_tree

    def get_tag_tree_include_head(self, user_id, rate, username):
        """
        给tag树构造一个头部
        :return:
        """
        from app.ctrl.ctrl_knowledge import CtrlKnowledge
        from app.ctrl.ctrl_role import CtrlRole
        role_list = CtrlRole().get_roles_by_user(user_id)
        if 'Admin' in role_list or 'Admin_KnowledgeDB' in role_list:
            role = True
        else:
            role = False
        if not role:
            tag_head_tree = self.get_technology_tag(rate, username)
            return tag_head_tree
        classify_tree = CtrlKnowledge().get_knowledge_classify(knowledge_only='left')
        tag_list = self.get_tag_tree_include_number(rate=rate, username=username, role=True)
        failure_modes = self.get_failure_modes()
        from app.ctrl.ctrl_doc import CtrlDoc
        count = CtrlDoc().count_doc(username)
        if username:
            tag = "我的知识库"
        else:
            tag = "知识库"
        tag_head_tree = [
            {
                'tag': tag,
                'required': True,
                'disabled': True,
                "sub_tags": [
                            classify_tree,
                            {
                                'tag': '知识点',
                                'required': True,
                                'disabled': True,
                                "sub_tags": [
                                    {
                                        'tag': '知识点一览',
                                        'required': True,
                                        'disabled': True,
                                        "sub_tags": [],
                                        'type': 'all',
                                        "num": count
                                    },
                                    {
                                        'tag': '知识点分类',
                                        'type': 'tag',
                                        'required': True,
                                        'disabled': True,
                                        "sub_tags": tag_list,
                                    },
                                    {'tag': 'Failure mode',
                                     'required': True,
                                     'disabled': True,
                                     'type': 'failure_mode',
                                     "sub_tags": failure_modes,
                                     }
                                ]
                            },
                            {
                                'tag': '知识库管理',
                                'type': 'manage',
                                'required': True,
                                'disabled': True,
                                "sub_tags": [
                                    {
                                        'tag': '知识点分类管理',
                                        'type': 'manage',
                                        'required': True,
                                        'disabled': True,
                                        "sub_tags": []
                                    },
                                ]
                            },
                ]
            }
            ]
        return tag_head_tree

    def filter_tags_by_user(self, tag_dataframe, username, tag_docs):
        if username:
            tag_df2 = tag_dataframe.set_index(keys=["tag_id"], drop=False)
            if not tag_docs:
                return None
            ancestors = set()
            for tag_id in tag_docs:
                if tag_id not in tag_df2.index:
                    continue
                temp = self._get_ancestors(tag_df2, tag_id)
                ancestors = ancestors.union(temp + [tag_id])
            # my_tags = ancestors.union(my_tags)
            df = tag_df2.loc[list(ancestors)]
            return df
        return tag_dataframe

    def filter_tags(self, tag_dataframe, fliter_tags):
        if not fliter_tags:
            return None
        tag_df2 = tag_dataframe.set_index(keys=["tag_id"], drop=False)
        ancestors = set()
        for tag_id in fliter_tags:
            if tag_id not in tag_df2.index:
                continue
            temp = self._get_ancestors(tag_df2, tag_id)
            ancestors = ancestors.union(temp + [tag_id])
        # my_tags = ancestors.union(my_tags)
        df = tag_df2.loc[list(ancestors)]
        return df

    def _get_ancestors(self, tag_dataframe, curr_tag_id):
        if curr_tag_id:
            s = tag_dataframe.loc[tag_dataframe.tag_id == curr_tag_id]
            # print s
            if s.empty:
                return []
            parent_tag_id = s.iloc[0, 1]
            if parent_tag_id:
                return [parent_tag_id] + self._get_ancestors(tag_dataframe,
                                                             parent_tag_id)
            else:
                return []
        else:
            return []

    def _get_tags_by_model(self, model_id, doc_type=None):
        tag_list = []
        if not doc_type:
            q = (db.session.query(DsModelTagRel.tag_id)
                 .filter(DsModelTagRel.model_id == model_id)
                 .distinct()
                 .order_by(DsModelTagRel.tag_id)
                 )
            for tag_rel in q:
                tag_list.append(tag_rel.tag_id)
            return tag_list
        else:
            sqlcmd = """
            SELECT DISTINCT t3.tag_id
              FROM ds.ds_doc as t1
              INNER JOIN ds.ds_section as t2
              on t1.doc_id = t2.doc_id
              INNER join ds.ds_section_tag_rel as t3
              on t2.sec_id = t3.sec_id
              WHERE t1.model_id = :val1 and doc_type = :val2
              ORDER BY t3.tag_id
            """
            s = db.session
            query = s.execute(sqlcmd, {'val1': model_id, 'val2': doc_type})
            rows = query.fetchall()
            for row in rows:
                tag_list.append(row[0])
        return tag_list

    def _get_tag_docs(self, username):
        tags = dict()
        s = db.session
        if username:
            sqlcmd = """
            SELECT tag_id, array_agg(a.doc_id)
              FROM public.docs as a
              left join public.doc_tags b
              on a.doc_id = b.doc_id
              where committer = :val
              group by tag_id 
              ORDER BY tag_id
              """
            query = s.execute(sqlcmd, {'val': username})
        else:
            sqlcmd = """
            SELECT tag_id, array_agg(a.doc_id)
              FROM public.docs as a
              left join public.doc_tags b
              on a.doc_id = b.doc_id
              group by tag_id 
              ORDER BY tag_id
              """
            query = s.execute(sqlcmd, {'val': username})
        rows = query.fetchall()
        for row in rows:
            if row[0]:
                tags[row[0]] = set(row[1])
        return tags

    def _get_sub_tags(self, tag_list, df):
        for tag_info in tag_list:
            tag_id = tag_info.get("tag_id")
            sub_df = df.loc[df.parent_tag_id == tag_id]
            sub_num = len(sub_df)
            if sub_num:
                parent_tag_list = [tag_info.get("tag")] * sub_num
                sub_df = sub_df.assign(parent_tag=parent_tag_list)
                sub_tag_list = sub_df.to_dict(orient='records')
                leaf = False  # 非叶子
                father = self._is_father_tag(sub_tag_list, df)
            else:  # 子为空，该TAG是叶子
                leaf = True
                sub_tag_list = []
                father = False
            tag_info["sub_tags"] = sub_tag_list
            tag_info["disabled"] = not leaf
            tag_info["father"] = father
            self._get_sub_tags(sub_tag_list, df)

    def _is_father_tag(self, tag_list, df):
        """
        判断子是否是叶子，目前叶子都在同一级，以后有变化需更改@yuyin
        :param tag_list:
        :param df:
        :return:
        """
        for tag_info in tag_list:
            tag_id = tag_info.get("tag_id")
            sub_df = df.loc[df.parent_tag_id == tag_id]
            sub_num = len(sub_df)
            if sub_num:
                father = False
            else:
                father = True
            return father

    def _count_doc_num(self, tag_tree, tag_doc_num):
        for tag in tag_tree:
            self._count_tag_docs(tag, tag_doc_num)

    def _count_tag_docs(self, tag, tag_doc_num):
        tag_id = tag.get("tag_id")
        doc_id_set = tag_doc_num.get(tag_id, set())
        sub_tags = tag.get("sub_tags", [])
        for sub_tag in sub_tags:
            sub_docs = self._count_tag_docs(sub_tag, tag_doc_num)
            doc_id_set = doc_id_set.union(sub_docs)
        tag["num"] = len(doc_id_set)
        return doc_id_set

    def add(self, tag_info):
        result = {"result": "NG"}
        try:
            parent_tag_id = tag_info.get('parent_tag_id')
            if parent_tag_id and not self._is_parent_tag(parent_tag_id):
                result["error"] = 'TAG分类不存在!'
            else:
                doc_tag = DBDocTagCat(**tag_info)
                db.session.add(doc_tag)
                db.session.commit()
                result["result"] = "OK"
        except Exception as e:
            current_app.logger.error('%s' % e)
            result["error"] = "服务异常！请联系管理员！"
        return result

    def delete(self, tag_id):
        result = {"result": "NG"}
        try:
            db.session.query(DBDocTagCat).filter(DBDocTagCat.tag_id == tag_id).delete()
            db.session.query(DBDocTagCat).filter(DBDocTagCat.parent_tag_id == tag_id).delete()
            db.session.commit()
            result = {"result": "OK"}
        except Exception as e:
            current_app.logger.error('%s' % e)
            result["error"] = "服务异常！请联系管理员！"
        return result

    def update(self, tag_id, tag_info):
        result = {"result": "NG"}
        try:
            parent_tag_id = tag_info.get('parent_tag_id')
            if parent_tag_id and not self._is_parent_tag(parent_tag_id):
                result["error"] = 'TAG分类不存在!'
            else:
                # DBDocTagCat.query.filter_by(tag_id=tag_id).update(**tag_info)
                db.session.query(DBDocTagCat).filter(DBDocTagCat.tag_id == tag_id).update(tag_info)
                db.session.commit()
                result = {"result": "OK"}
        except Exception as e:
            current_app.logger.error('%s' % e)
            result["error"] = "服务异常！请联系管理员！"
        return result

    def _is_parent_tag(self, parent_tag_id):
        doc_tag = DBDocTagCat.query.filter_by(tag_id=parent_tag_id).first()
        if doc_tag:
            return True
        return False

    def get_by_parent_id(self, tag_id):
        doc_tags = DBDocTagCat.query.filter_by(parent_tag_id=tag_id).all()
        doc_tag_list = []
        for doc_tag in doc_tags:
            doc_tag_list.append(doc_tag.to_dict())
        return doc_tag_list

    def get_required_tags(self):
        # username = agv.get("username")
        statement = (db.session.query(DBDocTagCat)
                     .filter()
                     .order_by(DBDocTagCat.parent_tag_id,
                               DBDocTagCat.tag_id)
                     .statement)

        tag_df = pd.read_sql(statement, db.session.bind)
        required_groups = self._get_required_tags(tag_df)
        return required_groups

    def _get_required_tags(self, df):
        # ## 取第一层[必填]
        required_df = df[df["required"] == True]
        tag_list = required_df.to_dict(orient='records')
        required_groups = []
        for tag in tag_list:
            tag_id = tag.get("tag_id")
            descendants = self._get_descendant_tag_id(tag_id, df)
            if descendants:
                required_groups.append(descendants)
            else:
                required_groups.append([tag_id])
        return required_groups

    def get_tag_for_scense(self, tag='技术专题'):
        statement = (db.session.query(DBDocTagCat).filter().order_by(
            DBDocTagCat.parent_tag_id, DBDocTagCat.tag_id).statement)
        tag_df = pd.read_sql(statement, db.session.bind)
        sub_df = tag_df.loc[tag_df.tag == tag]
        if sub_df.empty:
            return []
        tag_s = sub_df.iloc[0]
        tag_id = tag_s["tag_id"]
        return self._get_descendant_tag_id2(tag_id, tag_df)

    def _get_descendant_tag_id2(self, tag_id, df):
        sub_df = df.loc[df.parent_tag_id == tag_id]
        tags = sub_df.to_dict(orient='records')
        # pd.DataFrame.to_dict(orient='records')
        for sub_tag_info in tags:
            sub_tag_id = sub_tag_info["tag_id"]
            sub_tag_info["sub"] = self._get_descendant_tag_id2(sub_tag_id, df)
        return tags

    def get_descendant_tags(self, tag_id, orient='list'):
        statement = (db.session.query(DBDocTagCat)
                     .filter()
                     .order_by(DBDocTagCat.parent_tag_id, DBDocTagCat.tag_id)
                     .statement)
        tag_df = pd.read_sql(statement, db.session.bind)
        return self._get_descendant_tag_id(tag_id, tag_df)

    def _get_descendant_tag_id(self, tag_id, df, orient='list'):
        sub_tag_id_list = []
        sub_df = df.loc[df.parent_tag_id == tag_id]
        for i, sub_row in sub_df.iterrows():
            sub_id = sub_row["tag_id"]
            sub_tag_id_list.append(sub_id)
            sub_tag_id_list += self._get_descendant_tag_id(sub_id, df)
        return sub_tag_id_list

    def get_tag_by_id(self, tag_id):
        q = db.session.query(DBDocTagCat.tag).filter(DBDocTagCat.tag_id == tag_id).all()
        if len(q) > 0:
            return q[0].tag
        else:
            return None

    def get_all_tag(self):
        q = db.session.query(DBDocTagCat).order_by(DBDocTagCat.tag_id)
        tags = {}
        for tag in q:
            tag_id = tag.tag_id
            tags[tag_id] = tag.to_dict()
        return tags

    def get_tag_for_proj(self, classify):
        """
        把平台，项目的tag抽出来
        :param classify: special, common
        :return: 根据类型返回tag树
        """
        tag_tree = self.get_tag_tree(rate='normal')
        take_out_tag = {'fw_tag': None, 'proj_tag': None}
        for tag_dict in tag_tree:
            index = tag_tree.index(tag_dict)
            tag = tag_dict.get('tag')
            if tag == FW_TAG:
                fw_tags = tag_tree.pop(index)
                sub_tags = fw_tags.get('sub_tags')
                take_out_tag['fw_tag'] = sub_tags
            elif tag == PROJ_TAG:
                proj_tags = tag_tree.pop(index)
                sub_tags = proj_tags.get('sub_tags')
                take_out_tag['proj_tag'] = sub_tags
        if classify == 'special':
            return take_out_tag
        elif classify == 'common':
            return tag_tree

    def get_failure_modes(self):
        sqlcmd = """
        SELECT failure_mode_name as failure_mode, array_agg(doc_id)
          FROM public.failure_mode
          group by failure_mode_name
          order by failure_mode_name
        """
        failure_mode_list = []
        # doc_id_set = set()
        query = db.session.execute(sqlcmd)
        rows = query.fetchall()
        for row in rows:
            failure_mode_info = {'type': 'failure_mode'}
            failure_mode_info["tag"] = row[0]
            failure_mode_info["num"] = len(row[1])
            failure_mode_list.append(failure_mode_info)
        return failure_mode_list
