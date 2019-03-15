import pandas as pd
from flask import current_app
from app.db import db
from app.db.model import Model
from app.db.ds_doc import Ds_Doc
from app.db.project import Project, ProjectModel, ProjectModelRel
from app.ctrl.ctrl_project import CtrlProject
from .import_fw_model import ImportFwModel, LAYER_COLS
from ..architecture.architecture import Architecture


class ImportProjectModel(ImportFwModel):
    """导入项目模块
    """

    def __init__(self):
        ImportFwModel.__init__(self)
        # self.proj_name = proj_name.lower()
        # self.layer_columns = LAYER_COLS

    def import_model(self, proj_name):
        proj_list = CtrlProject().get_project_byname(proj_name)
        if proj_list:
            proj_info = proj_list[0]
            proj_id = proj_info.get(Project.proj_id.name)
            # 读取框架的Layer信息
            arcitecture_obj = Architecture(current_app.config["ARCHITECTURE_SRV"])
            layers = arcitecture_obj.get_all_layers(proj_name)
            if not layers:
                return False, '框架服务器没有项目%s的模块信息。' % proj_name
            model_df = arcitecture_obj.layer2df(layers)
            model_df = model_df[LAYER_COLS]
            # 去重,并改为小写
            new_model_df, lower_model_df = self.my_drop_duplicates(model_df)
            # 获取当前模块信息
            curr_df = self.get_project_models(proj_id)
            curr_df = self.tree_2_record_df(curr_df)
            curr_df, lower_curr_df = self.my_drop_duplicates(curr_df)  # 转为小写
            diff_df = self.difference(lower_curr_df, lower_model_df)
            modules = self.get_exist_doc_modules(diff_df, proj_id)
            if modules:
                msg = '以下模块存设计书，请先清除设计书，再删除模块。\n'
                msg += '\n'.join(modules)
                return False, msg
            # ## TODO@hcz:删除项目下的旧模块
            db.session.query(ProjectModel).filter(
                ProjectModel.proj_id == proj_id).delete()
            db.session.query(ProjectModelRel).filter(
                ProjectModelRel.proj_id == proj_id).delete()
            # 生成模块编号
            # model_id_dict = self._get_model_dict(model_df)
            # db.session.commit()
            # add 项目 model
            self._add_proj_model(new_model_df, proj_id)
            # 保存
            db.session.commit()
            return True, 'OK'
        else:
            current_app.logger.error('Dose not Exist Project. %s' % proj_name)
            return False, '没有项目%s. 请PL先添加项目%s' % (proj_name, proj_name)

    def _add_proj_model(self, model_df, proj_id):
        # 叶子，使用唯一ID
        # 结点，路径相同，就生成一个新的ID
        # 结点，路径不同，就生成一个新的ID
        model_id_dict = {}
        model_info_df = self._get_model_df()
        for _, row in model_df.iterrows():
            path_list = []
            parent_model_id = 0
            for i, col in enumerate(LAYER_COLS):
                model_name = row[col]
                if not model_name:
                    break
                # 叶子
                leaf = False
                if (i == len(LAYER_COLS) - 1) or not row[LAYER_COLS[i + 1]]:
                    path = ''
                    leaf = True
                else:  # 结点
                    path = '/'.join(path_list)
                key = (model_name.lower(), path.lower())
                if key not in model_id_dict:
                    model_id, flag = self._get_model_id(model_info_df,
                                                        model_name, path)
                    model_id_dict[key] = model_id
                    if flag == 'new':
                        model_info = {Model.model_id.name: model_id,
                                      Model.title.name: model_name,
                                      Model.path.name: path}
                        model_info_df = model_info_df.append(model_info,
                                                             ignore_index=True)
                    self._store_proj_model(proj_id, model_id, parent_model_id)
                else:
                    if leaf:
                        model_id = model_id_dict[key]
                        self._store_proj_model(proj_id, model_id,
                                               parent_model_id)
                parent_model_id = model_id_dict[key]
                path_list.append(model_name)
        return model_id_dict

    def _store_proj_model(self, proj_id, model_id, parent_model_id):

        project_model_data = {"proj_id": proj_id,
                              "model_id": model_id,
                              }
        project_model = ProjectModel(**project_model_data)
        db.session.add(project_model)
        db.session.flush()
        # gid = project_model.gid
        # Framework Model Rel
        if parent_model_id:
            proj_model_rel = ProjectModelRel()
            proj_model_rel.proj_id = proj_id
            proj_model_rel.model_id = model_id
            proj_model_rel.parent_model_id = parent_model_id
            # proj_model_rel.model_gid = gid
            # proj_model_rel.parent_gid = parent_gid
            db.session.add(proj_model_rel)

    def get_project_models(self, proj_id):
        sqlcmd = """
        SELECT a.gid as model_id, title as model_name, parent_model_id
          FROM ds.project_models as a
          left join ds.model as b
          on a.model_id = b.model_id
          left join ds.project_models_rel as c
          on a.proj_id = c.proj_id and a.model_id = c.model_id 
          where a.proj_id = {proj_id}
          order by parent_model_id, a.gid
        """.format(proj_id=proj_id)
        df = pd.read_sql(sqlcmd, db.session.bind)
        df["parent_model_id"].fillna(value=0, inplace=True)
        return df

    def tree_2_record_df(self, model_df):
        print('**********************************************************')
        data = []
        root_df = model_df[model_df["parent_model_id"] == 0]
        print(root_df)
        for _, row in root_df.iterrows():
            model_id = row["model_id"]
            model_name = row["model_name"]
            for model_names in self._deep_search_model(model_df,
                                                       model_id,
                                                       model_name):
                blank_num = (len(self.layer_columns) - len(model_names))
                model_names = model_names + [None] * blank_num
                # if len(model_names) < 5:
                #     print(model_names)
                # print(len(model_names), model_names)
                data.append(model_names)
        df = pd.DataFrame(data=data, columns=self.layer_columns)
        return df

    def _deep_search_model(self, df, model_id, model_name):
        """深度搜索
        :param df:
        :param model_id:
        :param model_name:
        :return:
        """
        visited = [model_name]
        child_df = self._get_sub_df(df, model_id)
        if child_df.empty:
            yield visited
        child_models = list(child_df.to_dict(orient='record'))
        stack = [iter(child_models)]
        while stack:
            children = stack[-1]
            child = next(children, None)
            if child is None:
                stack.pop()
                visited.pop()
            else:
                # print(visited + [child.get("model_name")])
                child_model_id = child.get("model_id")
                sub_df = self._get_sub_df(df, child_model_id)
                if sub_df.empty:
                    # print(visited + [child.get("model_name")])
                    if isinstance(child, pd.Series):
                        pass
                    yield visited + [child.get("model_name")]
                else:
                    child_models = list(sub_df.to_dict(orient='record'))
                    visited.append(child.get("model_name"))
                    stack.append(iter(child_models))

    def _get_sub_df(self, df, model_id):
        return df[df["parent_model_id"] == model_id]

    def difference(self, old_df, new_df):
        """求差集"""
        old_df = old_df.append(new_df)
        old_df = old_df.append(new_df)
        diff = old_df.drop_duplicates(keep=False)  # 去掉所有重复
        return diff

    def get_exist_doc_modules(self, diff_df, proj_id):
        modules = []
        for _, row in diff_df.iterrows():
            for i, column in enumerate(self.layer_columns[::-1]):
                module_name = row[column]
                if module_name:
                    if self.check_model_exist_doc(proj_id, module_name):
                        module_names = list(row)
                        modules.append('/'.join(module_names[:len(module_names) - i]))
        return modules

    def check_model_exist_doc(self, proj_id, module_name):
        """判断模块下面是否有设计书
        :param proj_id:
        :param model_name:
        :return:
        """
        model = (db.session.query(Model)
                 .filter(Model.title.ilike(module_name)).first())
        if model:
            model_id = model.model_id
            doc = (db.session.query(Ds_Doc)
                   .filter(Ds_Doc.proj_id == proj_id)
                   .filter(Ds_Doc.model_id == model_id).first())
            if doc:
                return True
        return False
