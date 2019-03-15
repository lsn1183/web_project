import pandas as pd
from flask import current_app
from app.db import db
# from app.db.model import ModelCode
from app.db.framework import Framework
from app.db.framework import FrameworkModel, FrameworkModelRel
from app.ctrl.ctrl_framework import CtrlFramework
from app.ctrl.ctrl_framework import CtrlFwModel
from app.db.model import Model
LAYER_COLS = ["Layer1",	"Layer2", "Layer3", "Layer4", "Layer5"]
# MD_CODE_COLS = [ModelCode.model_name.name, ModelCode.match1.name,
#                 ModelCode.match2.name, ModelCode.match3.name]


class ImportFwModel(object):
    """导入平台模块
    """
    def __init__(self):
        self.layer_columns = LAYER_COLS

    def import_model(self, fw_name, file, sheet_names=None):
        """ 平台模块导入
        :param fw_name: 平台
        :param file: excel
        :param sheet_names: sheet name list
        :return:
        1. 读取excel
        2. 生成模块编号
        3. 清除平台下的旧模块。
        4. 导入平台模块
        """
        if not sheet_names:
            sheet_names = ["MEU責務", "DCU責務"]
        fw_list = CtrlFramework().get_fw_byname(fw_name)
        if fw_list:
            fw_info = fw_list[0]
            fw_id = fw_info.get(Framework.fw_id.name)
            # 读取excel
            model_df = self._read_model_df(file, sheet_names)
            model_df.dropna(subset=[LAYER_COLS[0]], inplace=True)
            # 去重,并改为小写
            model_df = self.my_drop_duplicates(model_df)
            # 删除平台下的旧模块
            CtrlFwModel().delete(fw_id)
            # 生成模块编号
            model_id_dict = self._get_model_dict(model_df)
            # add model
            self._add_fw_model(model_id_dict, model_df, fw_id, layer_idx=0,
                               parent_model_id=None)
            # 保存
            db.session.commit()
            return True
        else:
            current_app.logger.error('Dose not Exist Framework %s' % fw_name)
            return False

    def my_drop_duplicates(self, df):
        right_df = pd.DataFrame(df, copy=True)
        for col in right_df.columns:
            right_df[col] = right_df[col].str.lower()
        right_df.drop_duplicates(inplace=True)
        joined_df = df.join(right_df, how='inner', rsuffix='_a')
        return joined_df[LAYER_COLS], right_df

    def _add_fw_model(self, model_id_dict, fw_model_df, fw_id,
                      layer_idx=0, parent_model_id=None):
        if layer_idx >= len(LAYER_COLS):
            return
        layer_col = LAYER_COLS[layer_idx]
        fw_model_df = fw_model_df.dropna(subset=[layer_col])
        model_serial = pd.Series(fw_model_df[layer_col], copy=True)
        model_names = list(model_serial.unique())
        for model_name in model_names:
            if not model_name:
                continue
            # model_obj = Model()
            # model_obj.code = model_id_dict.get(model_name)
            # model_obj.title = model_name
            # db.session.add(model_obj)
            # db.session.flush()
            model_id = model_id_dict.get(model_name)
            # if not model_id:
            #     print(model_name)
            # Framework Model
            fw_model = FrameworkModel()
            fw_model.fw_id = fw_id
            fw_model.model_id = model_id
            db.session.add(fw_model)
            # Framework Model Rel
            if parent_model_id:
                fw_model_rel = FrameworkModelRel()
                fw_model_rel.fw_id = fw_id
                fw_model_rel.model_id = model_id
                fw_model_rel.parent_model_id = parent_model_id
                db.session.add(fw_model_rel)
            # sub Model
            condition = "%s == @model_name" % layer_col
            sub_df = fw_model_df.query(condition)
            # sub_df = fw_model_df[fw_model_df[layer_col] == model_name]
            self._add_fw_model(model_id_dict, sub_df, fw_id,
                               layer_idx + 1, model_id)

    def _read_model_df(self, file, sheet_names):
        df_list = []
        for sheet_name in sheet_names:
            model_df = pd.read_excel(file, sheetname=sheet_name,
                                     header=0, skiprows=[0])
            # print(model_df)
            model_df = model_df[LAYER_COLS]
            for col in LAYER_COLS:
                model_df[col] = model_df[col].str.strip()
            df_list.append(model_df)
        model_cat = pd.concat(df_list)
        model_cat = model_cat.reset_index(drop=True)
        return model_cat

    def _get_model_df(self):
        q = db.session.query(Model).order_by(Model.model_id)
        code_df = pd.read_sql(q.statement, con=db.session.bind)
        return code_df

    def _get_model_dict(self, model_df):
        # 叶子，使用唯一ID
        # 结点，路径相同，就生成一个新的ID
        # 结点，路径不同，就生成一个新的ID
        model_id_dict = {}
        model_info_df = self._get_model_df()
        model_info_df.fillna(value='')
        for _, row in model_df.iterrows():
            path_list = []
            for i, col in enumerate(LAYER_COLS):
                model_name = row[col]
                # 叶子
                if (i == len(LAYER_COLS) - 1) or not row[LAYER_COLS[i + 1]]:
                    path = ''
                else:  # 结点
                    path = '/'.join(path_list)
                key = (model_name.lower(), path.lower())
                if key in model_id_dict:
                    path_list.append(model_name)
                    continue
                model_id, flag = self._get_model_id(model_info_df,
                                                    model_name,
                                                    path)
                model_id_dict[key] = model_id
                if flag == 'new':
                    model_info = {Model.model_id.name: model_id,
                                  Model.title.name: model_name,
                                  Model.path.name: path}
                    model_info_df = model_info_df.append(model_info,
                                                         ignore_index=True)
        return model_id_dict

    def _get_model_id(self, model_info_df, model_name, path=''):
        temp_df = model_info_df[model_info_df[Model.title.name].str.lower() == model_name.lower()]
        temp_df = temp_df[temp_df[Model.path.name].str.lower() == path.lower()]
        if not temp_df.empty:
            row = temp_df.iloc[0]
            model_id = int(row[Model.model_id.name])
            return model_id, 'old'
        return self._add_model(model_name, path), 'new'

    def _add_model(self, model_name, path):
        # print(model_name)
        data = {Model.title.name: model_name,
                Model.path.name: path}
        model = Model(**data)
        db.session.add(model)
        db.session.flush()
        code = "A" + str(model.model_id)
        model.code = code
        return model.model_id

