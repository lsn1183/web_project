import os
from app.db import db
from flask import current_app
from sqlalchemy import or_, and_
from ..export_doc.export_factory import ExportFactory
from .ctrl_ds_doc import CtrlDsDoc
from app.db.ds_doc import Ds_Doc
from app.ctrl.ctrl_project import CtrlProject
from app.db.model import Model
import pandas as pd
from app.db.utility import Utillity
from ..tool.my_zip import zip_file
EXPORT_ROOT_DIR = r'export_root'
DOC_TYPE_DIR = {"BASIC": "BasicDesign",
                "DETAIL": "DetailedDesign"
                }


class CtrlExportDoc(object):
    def __init__(self):
        self.proj_name = ''

    def do_export(self, proj_id=None, model_id=None, doc_type=None, doc_id=None):
        msg, file_path = '', ''
        _, proj_list = CtrlProject().get(proj_id)
        if proj_list:
            self.proj_name = proj_list[0].get("proj_name")
        else:
            msg = '指定的项目不存在!'
            return False, msg, file_path
        if doc_id:  # 导出一个文档
            doc_data = CtrlDsDoc().get_doc(doc_id, detail=False)
            if not doc_data:
                msg = '不存在文档。doc_id = %s' % doc_id
                return False, msg, file_path
            doc_type = doc_data.get("doc_type")
            export_obj = ExportFactory.create(self.proj_name, doc_type)
            unique = str(Utillity.get_nextval('doc_export_seq'))
            out_dir = os.path.join(EXPORT_ROOT_DIR, unique)
            file_path = export_obj.do_export(out_dir, doc_id)
            return True, msg, file_path
        elif doc_type:  # 模块下的基本设计or详细设计
            doc_type = doc_type.upper()
            if not model_id:
                msg = '没有指定Model.'
                return False, msg, file_path
            if not proj_id:
                msg = '没有指定项目.'
                return False, msg, file_path
            if doc_type not in DOC_TYPE_DIR:
                msg = '指定的文档类型不对. type=%s' % doc_type
                return False, msg, file_path
            model = self._get_model(model_id)
            if model:
                model_name = model.get("title")
            else:
                msg = '指定的Model不对.'
                return False, msg, file_path
            unique = str(Utillity.get_nextval('doc_export_seq'))
            root_dir = os.path.join(EXPORT_ROOT_DIR,
                                    unique,
                                    DOC_TYPE_DIR.get(doc_type))
            model_name = model_name.replace(' ', '_')
            out_dir = os.path.join(root_dir, model_name)
            export_obj = ExportFactory.create(self.proj_name, doc_type)
            for doc_info in self._get_docs(proj_id, model_id, doc_type):
                doc_id = doc_info.get("doc_id")
                export_obj.do_export(out_dir, doc_id)
            # 压缩文件夹
            file_path = zip_file([out_dir], root_dir, '%s.zip' % model_name)
            return True, msg, file_path
        elif model_id:  # 模块下的所有文档
            if not proj_id:
                msg = '没有指定项目.'
                return False, msg, file_path
            return self._export_model_docs(proj_id, model_id)
        elif proj_id:  # 项目下的所有文档
            return self._export_proj_docs(proj_id)
        return True, msg, file_path

    def _export_proj_docs(self, proj_id):
        return self._export_model_docs(proj_id)

    def _export_model_docs(self, proj_id, model_id=None):
        msg, file_path = '', ''
        model_df = self._get_model_df(proj_id)
        model_df.fillna(value=0, inplace=True)
        if model_id:
            root_models = [model_id]
            model_name = self._get_model_name(model_df, model_id)
            if not model_name:
                msg = '指定的模块不存在!'
                return False, msg, file_path
            zip_name = '%s.zip' % model_name
        else:
            root_df = model_df[model_df["parent_model_id"] == 0]
            root_models = list(root_df["model_id"].unique())
            zip_name = '%s.zip' % self.proj_name
        unique = str(Utillity.get_nextval('doc_export_seq'))
        root_dir = os.path.join(EXPORT_ROOT_DIR, unique)
        basic_obj = ExportFactory.create(self.proj_name, "BASIC")
        detail_obj = ExportFactory.create(self.proj_name, "DETAIL")
        for model_id in root_models:
            model_name = self._get_model_name(model_df, model_id)
            for model_names, leaf_model_id in self._get_models(model_df,
                                                               model_id,
                                                               model_name):
                model_names = [n.replace(' ', '_') for n in model_names]
                model_dir = os.path.sep.join(model_names)
                for doc_type, export_obj in zip(["BASIC", "DETAIL"],
                                                [basic_obj, detail_obj]):
                    out_dir = os.path.join(root_dir,
                                           DOC_TYPE_DIR.get(doc_type),
                                           model_dir)
                    leaf_model_id = int(leaf_model_id)
                    for doc_info in self._get_docs(proj_id,
                                                   leaf_model_id,
                                                   doc_type):
                        doc_id = doc_info.get("doc_id")
                        export_obj.do_export(out_dir, doc_id)
        # 压缩文件夹
        in_dir_list = []
        for doc_type_dir in DOC_TYPE_DIR.values():
            in_dir = os.path.join(root_dir, doc_type_dir)
            if os.path.isdir(in_dir):
                in_dir_list.append(in_dir)
        if in_dir_list:
            file_path = zip_file([root_dir], root_dir, zip_name)
            return True, msg, file_path
        else:
            msg = '没有设计书!'
            return False, msg, file_path

    def _get_docs(self, proj_id, model_id, doc_type):
        q = (db.session.query(Ds_Doc)
             .filter(and_(Ds_Doc.proj_id == proj_id,
                          Ds_Doc.model_id == model_id,
                          Ds_Doc.doc_type == doc_type))
             )
        for doc in q:
            yield doc.to_dict()

    def _get_model(self, model_id):
        model = (db.session.query(Model)
                 .filter(Model.model_id == model_id).first())
        if model:
            return model.to_dict()
        else:
            return dict()

    def _get_model_df(self, proj_id):
        sqlcmd = """
        SELECT a.model_id, parent_model_id, title as model_name
          FROM ds.project_models as a
          left join ds.project_models_rel as b
          on a.proj_id = b.proj_id and a.model_id = b.model_id
          left join ds.model as c
          on a.model_id = c.model_id
          where a.proj_id = {proj_id}
          order by a.gid
        """.format(proj_id=proj_id)
        df = pd.read_sql(sqlcmd, con=db.session.bind)
        df.set_index(keys='model_id', drop=False, inplace=True)
        return df

    # def _get_models2(self, df, model_names, model_id):
    #     sub_df = self._get_sub_df(df, model_id)
    #     if sub_df.empty:
    #         return model_names, model_id
    #     else:
    #         for _, row in sub_df.iterrows():
    #             sub_model_id = row["model_id"]
    #             model_name = row["model_name"]
    #             sub_model_nams = model_names + [model_name]
    #             self._get_models(df, sub_model_nams, sub_model_id)

    def _get_sub_df(self, df, model_id):
        return df[df["parent_model_id"] == model_id]

    def _get_model_name(self, df, model_id):
        s = df.loc[model_id]
        if isinstance(s, pd.Series):
            return s.model_name
        else:
            return s.iloc[0]["model_name"]

    def _get_models(self, df, model_id, model_name):
        """深度搜索
        :param df:
        :param model_id:
        :param model_name:
        :return:
        """
        visited = [model_name]
        child_df = self._get_sub_df(df, model_id)
        if child_df.empty:
            yield visited, model_id
        child_models = list(child_df.to_dict(orient='record'))
        stack = [iter(child_models)]
        while stack:
            children = stack[-1]
            child = next(children, None)
            if child is None:
                stack.pop()
                visited.pop()
            else:
                child_model_id = child.get("model_id")
                sub_df = self._get_sub_df(df, child_model_id)
                if sub_df.empty:
                    # print(visited + [child.get("model_name")])
                    yield visited + [child.get("model_name")], child_model_id
                else:
                    child_models = list(sub_df.to_dict(orient='record'))
                    visited.append(child.get("model_name"))
                    stack.append(iter(child_models))
