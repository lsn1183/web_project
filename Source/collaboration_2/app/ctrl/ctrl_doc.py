# -*- coding: UTF-8 -*-
import os, json
import time
import pandas as pd
from app.db.utility import Utillity
from app.ctrl.ctrl_base import CtrlBase
from app.db.doc import Doc
from app.db.doc import Consider
from app.db.doc import FailureMode
from app.db.doc_tags import DocTags
from app.tool.arl_diff import ArlDiff
from flask import current_app
from app.db import db
from sqlalchemy import or_, cast, String
from sqlalchemy import func
from app.ctrl.ctrl_doc_tag import CtrlDocTag
DOC_TYPE_FILE = 'file'
DOC_TYPE_URL = 'url'
DOC_TYPE_TEXT = 'text'


class CtrlDoc(object):

    def __init__(self):
        self.table_name = "docs"
        self.key_col = "doc_id"
        self.id_col = "id_col"
        self.model_table_name = 'doc_tags'
        self.db_schema = 'public'
        self.attr_list = ["doc_id", "doc_type", "doc_title", "path",
                          "ver", "author", "committer", "create_time",
                          "update_time", "summary", "keywords"]

    def get_by_key_id(self, key_id):
        doc = (Doc.query.filter(Doc.doc_id == key_id).all())
        doc_dict = doc[0].to_dict()
        # content = doc_dict.get('content')
        # doc_dict['content'] = content.replace('\n', '<br>')
        if doc_dict.get("doc_type") == 'file':
            file_url = doc_dict.get('content')
            file_name = os.path.basename(file_url)
            doc_dict['file_name'] = file_name
        tag_list = self._get_tags(key_id)
        doc_dict["tags"] = tag_list
        consider_obj = CtrlConsider()
        doc_dict["considers"] = consider_obj.get_considers(key_id)
        failure_obj = CtrlFailureMode()
        doc_dict["failure_mode"] = failure_obj.get_failure_mode(key_id)
        # if doc_dict.get("doc_type") == 'url':
        #     doc_dict['path'] = doc_dict.get("content")
        #     doc_dict["content"] = None
        # elif doc_dict.get("doc_type") == 'file':
        #     doc_dict['file'] = doc_dict.get("content")
        #     doc_dict["content"] = None
        return doc_dict

    def add(self, request_data):
        data = dict()
        file_upload = ''
        if request_data.files:
            file_upload = request_data.files['file']
            if file_upload:
                file_name = file_upload.filename
                curr_app = current_app._get_current_object()
                path = curr_app.config.get("DOC_PATH_ROOT")
                if not os.path.exists(path):
                    os.makedirs(path)
                path = os.path.join(path, file_name)
                if os.path.exists(path):
                    current_app.logger.error('文件已经存在! %s' %file_name)
                    return False, u'文件已经存在!'
                file_upload.save(path)  # 保存上传的文件
                path = Utillity.convert_url(curr_app.config.get('FILE_SRV_URL'), path)
                data["doc_type"] = DOC_TYPE_FILE
                data["doc_title"] = request_data.form.get('doc_title')
                # data["doc_type"] = request_data.form.get('doc_type')
                data["ver"] = request_data.form.get('ver')
                data["author"] = request_data.form.get('author')  # 作者',
                data["committer"] = request_data.form.get('committer')  # 提交者'
                data["tags"] = request_data.form.get('tags')
                if data["tags"]:
                    data["tags"] = data["tags"].split(',')
                data["summary"] = request_data.form.get("summary")
                data["keywords"] = request_data.form.get("keywords")
            else:
                return False, u'缺少文件!'
        else:
            data = request_data.get_json()
            data["doc_type"] = DOC_TYPE_URL
            if 'Tags' in data:
                data["tags"] = data.get("Tags")
            path = data.get("path")
        if not path:
            data["doc_type"] = DOC_TYPE_TEXT
            content = data.get("content")
            if not content:
                return False, u'请指定Url或上传文件或输入文本!'
            path = content
        try:
            if 'path' in data:
                data.pop("path")
            if 'file' in data:
                data.pop('file')
            data["content"] = path
            data["update_time"] = self.get_current_time()
            data["create_time"] = data["update_time"]
            self._common_add(data, data["update_time"])
            return True, 'OK'
        except Exception as e:
            # current_app.logger.info('DownLoad file path=%s, %s' % (path_info, file_name))
            db.session.rollback()
            current_app.logger.error('%s' % e)
            if file_upload:
                os.remove(path)  # 删除文件
            return False, "服务异常！请联系管理员！"

    def add2(self, request_data):
        try:
            data = request_data.get_json(force=True)
            data["doc_type"] = DOC_TYPE_URL
            path = data.get('path')
            if not path:
                return False, u'请指定Url或上传文件!'
            if data.get("Tags"):
                data["tags"] = data.get("Tags")
            data["update_time"] = self.get_current_time()
            data["create_time"] = data["update_time"]
            self._common_add(data, data["update_time"])
            return True, 'OK'
        except Exception as e:
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def _common_add(self, data, update_time='', old_data=None):
        key_id = data.get(self.key_col)
        tags = data.get("tags")
        if 'tags' in data:
            data.pop('tags')
        if key_id:
            old_data = self.get_by_key_id(key_id)
            if 'tags' in old_data:
                old_data.pop('tags')
        ignore_col_list = []
        diff_obj = ArlDiff(self.key_col, self.id_col,
                           self.attr_list, ignore_col_list)
        diff_result = diff_obj.diff(old_data, data)
        action = diff_result.get("action")
        considers = []
        if "considers" in data:
            considers = data.pop("considers")
        failure_mode = []
        if "failure_mode" in data:
            failure_mode = data.pop("failure_mode")
        if action == "same":
            return None
        if action == "add":
            doc = Doc(**data)
            db.session.add(doc)
            db.session.flush()
            data[self.key_col] = doc.doc_id
            diff_result[self.key_col] = doc.doc_id
            self._add_model_list(doc.doc_id, tags)
            consider = CtrlConsider()
            consider.update_considers(doc.doc_id, considers)
            CtrlFailureMode().update_failure_model(failure_mode, doc.doc_id)
            db.session.commit()
        elif action == "change" or old_data:
            # col_change_list = diff_result.get("col_change_list")
            db.session.query(Doc).filter(Doc.doc_id == key_id).update(data)
            data[self.key_col] = old_data.get(self.key_col)
            # ## 先删除, 再添加
            self._delete_tags(key_id)
            self._add_model_list(key_id, tags)
            consider = CtrlConsider()
            consider.update_considers(key_id, considers,
                                      old_data.get("considers"))
            CtrlFailureMode().update_failure_model(failure_mode, key_id)
            db.session.commit()
            # self._add_model_list(pg, data[self.key_col], data.get("tags"))
        else:
            pass
        # log_list = self.convert2log([diff_result])
        return True

    def _add_model_list(self, doc_id, tags):
        if not doc_id or not tags:
            return
        model_list_change = []
        for tag_id in tags:
            doc_tag = DocTags(doc_id=doc_id, tag_id=tag_id)
            db.session.add(doc_tag)
        return model_list_change

    def _delete_tags(self, doc_id):
        if not doc_id:
            return
        db.session.query(DocTags).filter(DocTags.doc_id == doc_id).delete()
        # db.session.commit()

    def delete(self, doc_id):
        rst = False
        message = ''
        try:
            doc_info = self.get_by_key_id(doc_id)
            self._delete_tags(doc_id)
            consider_obj = CtrlConsider()
            consider_obj.delete_considers(doc_id)
            CtrlFailureMode().delete_by_doc_id(doc_id)
            db.session.query(Doc).filter(Doc.doc_id == doc_id).delete()
            db.session.commit()
            self._delete_file(doc_info.get("doc_type"), doc_info.get("content"))
            rst = True
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            message = str(e)
        finally:
            return rst, message

    def _delete_file(self, doc_type, path):
        if doc_type == DOC_TYPE_FILE:
            if os.path.exists(path):
                os.remove(path)

    def update(self, request_data):
        data = dict()
        need_del_old_file = False
        if request_data.files:
            file_upload = request_data.files['file']
            if file_upload:
                data["doc_id"] = request_data.form.get('doc_id')
                old_doc_info = self.get_by_key_id(data.get('doc_id'))
                if not old_doc_info:
                    return False, u'没有这个文件!'
                file_name = file_upload.filename
                curr_app = current_app._get_current_object()
                path = curr_app.config.get("DOC_PATH_ROOT")
                if not os.path.exists(path):
                    os.makedirs(path)
                path = os.path.join(path, file_name)
                if old_doc_info.get("content") != path and old_doc_info.get("doc_type") == "file":  # 文件变化了, 旧的要删除
                    need_del_old_file = True
                file_upload.save(path)  # 保存上传的文件
                path = Utillity.convert_url(curr_app.config.get('FILE_SRV_URL'), path)
                data["doc_type"] = DOC_TYPE_FILE
                data["doc_title"] = request_data.form.get('doc_title')
                # data["doc_type"] = request_data.form.get('doc_type')
                data["ver"] = request_data.form.get('ver')
                data["author"] = request_data.form.get('author')  # 作者',
                data["committer"] = request_data.form.get('committer')  # 提交者'
                data["tags"] = request_data.form.get('tags')
                if data["tags"]:
                    data["tags"] = data["tags"].split(',')
                data["summary"] = request_data.form.get("summary")
                data["keywords"] = request_data.form.get("keywords")
            else:
                return False, u'缺少文件!'
        else:
            data = request_data.get_json()
            if 'file_name' in data:
                data.pop("file_name")
            old_doc_info = self.get_by_key_id(data.get('doc_id'))
            if not old_doc_info:
                return False, u'没有这个文件!'
            # data["doc_type"] = DOC_TYPE_URL
            if 'Tags' in data:
                data["tags"] = data.get("Tags")
            path = data.get("path")
        if not path:
            # data["doc_type"] = DOC_TYPE_TEXT
            content = data.get("content")
            # if not content:
            #     return False, u'请指定Url或上传文件或输入文本!'
            path = content
        try:
            if need_del_old_file:  # 删除旧的文件
                self._delete_file(old_doc_info.get("doc_type"),
                                  old_doc_info.get("content"))
            if 'path' in data:
                data.pop("path")
            if 'file' in data:
                data.pop('file')
            if path:
                data["content"] = path
            else:
                if 'content' in data:
                    data.pop('content')
            data["update_time"] = self.get_current_time()
            # data["create_time"] = data["update_time"]
            self._common_add(data, data["update_time"], old_doc_info)
            return True, 'OK'
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            if file_upload:
                os.remove(path)  # 删除文件
            return False, "服务异常！请联系管理员！"

    # def _get_by_tag(self, tag_id):
    #     tag_id_list = []
    #     tag_id_list.append(str(tag_id))
    #     doc_tag_obj = CtrlDocTag()
    #     sub_list = doc_tag_obj.get_by_parent_id(tag_id)
    #     if sub_list:
    #         for sub in sub_list:
    #             sub_tag_id = sub.get('tag_id')
    #             tag_id_list.append(str(sub_tag_id))
    #             self.get_sub_tag(doc_tag_obj, sub_tag_id, tag_id_list)
    #     return tag_id_list

    def get_sub_tag(self, doc_tag_obj, tag_id, tag_id_list):
        sub_list = doc_tag_obj.get_by_parent_id(tag_id)
        if sub_list:
            for sub in sub_list:
                sub_tag_id = sub.get('tag_id')
                tag_id_list.append(str(sub_tag_id))
                self.get_sub_tag(doc_tag_obj, sub_tag_id, tag_id_list)
        else:
            return

    def get_by_tag(self, condition, tag_id, user, page, size):
        q = (db.session.query(Doc)
             .outerjoin(DocTags, Doc.doc_id == DocTags.doc_id)
             )
        if condition:
            q = q.filter(or_(Doc.doc_title.ilike('%'+condition+'%'),
                             Doc.content.ilike('%'+condition+'%'),
                             Doc.committer.ilike(condition),
                             cast(Doc.doc_id, String).ilike(condition)))
        if user:
            q = q.filter(Doc.committer == user)
        if tag_id:
            doc_tag_obj = CtrlDocTag()
            desc_list = doc_tag_obj.get_descendant_tags(tag_id)
            tag_id_list = [tag_id] + desc_list
            q = q.filter(DocTags.tag_id.in_(tag_id_list))
        q = q.order_by(Doc.doc_id).distinct()
        count = q.count()
        docs = q.limit(size).offset(size * (page - 1))
        # print(q.statement)
        doc_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            if "content" in doc_dict:
                doc_dict.pop("content")
            tag_list = self._get_tags(doc.doc_id)
            doc_dict["tags"] = tag_list
            doc_list.append(doc_dict)
        return count, doc_list

    def get_failuremode_by_tag(self, tag_id):
        sqlcmd = """
        SELECT a.doc_id, doc_title, failure_mode_name as failure_mode
          FROM public.doc_tags as a
          LEFT JOIN public.docs as b
          on a.doc_id = b.doc_id
          inner join public.failure_mode as c
          on a.doc_id = c.doc_id
          where tag_id = {tag_id}
          order by failure_mode_name, a.doc_id
        """.format(tag_id=tag_id)
        failure_mode_list = []
        df = pd.read_sql(sqlcmd, con=db.session.bind)
        failure_modes = df["failure_mode"].unique()
        for failure_mode in failure_modes:
            failure_dict = dict()
            failure_dict["failure_mode"] = failure_mode
            sub = df[df["failure_mode"] == failure_mode]
            sub["value"] = ['']*len(sub)
            doc_list = sub[["doc_id", "doc_title", "value"]].to_dict(orient='records')
            failure_dict["doc_list"] = doc_list
            failure_mode_list.append(failure_dict)
        return failure_mode_list

    def get_by_failure_mode(self, condition, failure_mode, user, page, size):
        q = (db.session.query(Doc)
             .outerjoin(FailureMode, Doc.doc_id == FailureMode.doc_id)
             )
        if condition:
            q = q.filter(or_(Doc.doc_title.ilike('%'+condition+'%'),
                             Doc.content.ilike('%'+condition+'%')))
        if user:
            q = q.filter(Doc.committer == user)
        if failure_mode:
            q = q.filter(FailureMode.failure_mode_name == failure_mode)
        q = q.distinct().order_by(Doc.doc_id)
        count = q.count()
        docs = q.limit(size).offset(size * (page - 1))
        # print(q.statement)
        doc_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            if "content" in doc_dict:
                doc_dict.pop("content")
            tag_list = self._get_tags(doc.doc_id)
            doc_dict["tags"] = tag_list
            doc_list.append(doc_dict)
        return count, doc_list

    def get_by_tags(self, tag_list):
        bug_doc_list = self.get_bug_docs()
        doc_q = (db.session.query(Doc)
                 .outerjoin(DocTags, Doc.doc_id == DocTags.doc_id)
                 .filter(DocTags.tag_id.in_(tag_list)))
        doc_list = []
        for doc in doc_q:
            doc_dict = dict()
            doc_dict[Doc.doc_id.name] = doc.doc_id
            doc_dict[Doc.doc_title.name] = doc.doc_title
            doc_list.append(doc_dict)
        knowledge_docs = []
        bug_list = []
        for doc in doc_list:
            if doc in bug_doc_list:
                bug_list.append(doc)
            else:
                knowledge_docs.append(doc)
        return knowledge_docs, bug_list

    def get_bug_docs(self):
        doc_tag_obj = CtrlDocTag()
        bug_tag_list = doc_tag_obj.get_descendant_tags(240)  # 历史问题重要性tag_id:240
        bug_doc_q = (db.session.query(Doc)
                     .outerjoin(DocTags, Doc.doc_id == DocTags.doc_id)
                     .filter(DocTags.tag_id.in_(bug_tag_list)))
        bug_doc_list = []
        for bug_doc in bug_doc_q:
            doc_dict = dict()
            doc_dict[Doc.doc_id.name] = bug_doc.doc_id
            doc_dict[Doc.doc_title.name] = bug_doc.doc_title
            bug_doc_list.append(doc_dict)
        return bug_doc_list

    def _get_tags(self, doc_id):
        sqlcmd = """
        SELECT a.tag_id, tag
          FROM public.doc_tags as a
          LEFT JOIN public.doc_tag_category as b
          ON a.tag_id = b.tag_id
          where doc_id=:doc_id
          order by tag_id
        """
        tags = db.session.execute(sqlcmd, {'doc_id': doc_id}).fetchall()
        tag_list = []
        for tag in tags:
            tag_list.append(dict(tag))
        return tag_list

    def get_group_users(self, create_time):
        content = []
        datas = db.session.query(Doc.committer, func.count(Doc.doc_id))
        if create_time:
            datas = datas.filter(Doc.create_time.like(create_time+'%')).group_by(Doc.committer)
        else:
            datas = datas.group_by(Doc.committer)
        for data in datas:
            doc_info = dict()
            doc_info['user'] = data[0]
            doc_info['doc_num'] = data[1]
            content.append(doc_info)
        return content

    def get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def _fetch_many(self, datas, size, page):
        """分页查询"""
        offset = size * (page - 1)
        end = offset + size
        count = len(datas)
        if count > 0:
            if offset >= count:
                return count, []
            return count, datas[offset:end]
        return count, []

    def count_doc(self, username):
        """
        统计文档总数
        :return:
        """
        q = db.session.query(Doc)
        if username:
            q = q.filter(Doc.committer == username)
        count = q.count()
        return count


class CtrlConsider(object):
    """考虑点
    """
    def __init__(self):
        pass

    def get_considers(self, doc_id):
        consider_list = []
        q = (db.session.query(Consider).filter(Consider.doc_id == doc_id)
             .order_by(Consider.consider_id)
             )
        for consider in q:
            consider_list.append(consider.to_dict())
        return consider_list

    def update_considers(self, doc_id, consider_list, old_consider_list=None):
        retain_list = []
        if not old_consider_list:
            old_consider_list = []
        for consider_info in consider_list:
            if not consider_info.get(Consider.consider_id.name):
                continue
            consider_id = consider_info.get(Consider.consider_id.name)
            consider_info[Consider.doc_id.name] = doc_id
            if not consider_id:  # 新增
                self.add(consider_info)
            else:  # 更新
                self.update(consider_info)
                retain_list.append(consider_id)
        # 删除旧的
        for consider_info in old_consider_list:
            consider_id = consider_info.get(Consider.consider_id.name)
            if consider_id not in retain_list:
                self.delete(consider_id)

    def delete_considers(self, doc_id):
        if doc_id:
            db.session.query(Consider).filter(
                Consider.doc_id == doc_id).delete()

    def update(self, data):
        consider_id = data.get(Consider.consider_id.name)
        if consider_id:
            new_data = dict()
            new_data[Consider.consider_name.name] = data.get(
                Consider.consider_name.name)
            db.session.query(Consider).filter(
                Consider.consider_id == consider_id).update(new_data)

    def add(self, data):
        consider_id = data.get(Consider.consider_id.name)
        if not consider_id:
            new_data = dict()
            new_data[Consider.consider_name.name] = data.get(
                Consider.consider_name.name)
            new_data[Consider.doc_id.name] = data.get(Consider.doc_id.name)
            obj = Consider(**new_data)
            db.session.add(obj)
            db.session.flush()
            return obj.consider_id
        return None

    def delete(self, consider_id):
        if consider_id:
            db.session.query(Consider).filter(
                Consider.consider_id == consider_id).delete()


class CtrlFailureMode(CtrlBase):
    """
    故障模式
    """
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = FailureMode.failure_id
        self.db_object = FailureMode
        self.col_list = [FailureMode.failure_mode_name.name]

    def get_failure_mode(self, doc_id):
        failure_mode_list = []
        q = (db.session.query(FailureMode).filter(FailureMode.doc_id == doc_id)
             .order_by(FailureMode.failure_id)
             )
        for failure in q:
            failure_mode_list.append(failure.to_dict())
        return failure_mode_list

    def update_failure_model(self, data_list, doc_id):
        new_data_list = []
        for data in data_list:
            data['doc_id'] = doc_id
            if data[FailureMode.failure_mode_name.name]:
                new_data_list.append(data)
        old_data_list = self.get_failure_mode(doc_id)
        self.add_list(self.db_object, new_data_list, old_data_list, self.key_col, self.col_list)

    def delete_by_doc_id(self, doc_id):
        if doc_id:
            db.session.query(FailureMode).filter(
                FailureMode.doc_id == doc_id).delete()

    def get_failermode_by_doc_id(self, doc_id):
        """根据文档id获取"failermode"""
        q = (db.session.query(FailureMode).filter(FailureMode.doc_id == doc_id)
             .order_by(FailureMode.failure_id))
        filermode_list = []
        for filermode in q:
            filermode_dict = dict()
            filermode_dict['failure_id'] = filermode.failure_id
            filermode_dict['failure_mode_name'] = filermode.failure_mode_name
            filermode_list.append(filermode_dict)
        return filermode_list

    def get_failure_mode_df(self, doc_id_list):
        q = (db.session.query(FailureMode.doc_id, FailureMode.failure_mode_name)
             .filter(FailureMode.doc_id.in_(doc_id_list))
             .order_by(FailureMode.failure_id)
             )
        df = pd.read_sql(q.statement, db.session.bind)
        return df
