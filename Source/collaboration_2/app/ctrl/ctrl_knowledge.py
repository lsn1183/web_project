# -*- coding: UTF-8 -*-
import pandas as pd
# from app.ctrl.ctrl_base import CtrlBase
from app.db import db
from flask import current_app
from app.db.knowledge import KnowledgeClassify
KNOWLEDGE_TEMPLATE = {
    "sheet_name": "knowledge",
    "header_row": 1,
    "column": ["知识点",
               "分级一", "分级二", "分级三", "分级四", "分级五",
               "分级六", "分级七"	, "分级八", "分级九", "分级十",
               "文档编号"],
    "re_column": ["knowledge",
                  "classify1", "classify2", "classify3", "classify4", "classify5",
                  "classify6", "classify7", "classify8", "classify9", "classify10",
                  "doc_id"
                  ]
}


class CtrlKnowledge():
    def __init__(self):
        # CtrlBase.__init__(self)
        pass

    def import_excel(self, file_path):
        data_list = self._import_excel(file_path)
        try:
            db.session.query(KnowledgeClassify).delete()
            for data in data_list:
                db.session.add(KnowledgeClassify(**data))
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def _import_excel(self, file_path):
        df = pd.read_excel(file_path,
                           sheetname=KNOWLEDGE_TEMPLATE.get("sheet_name"),
                           header=KNOWLEDGE_TEMPLATE.get("header_row"),
                           )
        title_errors = self.check_column(df, KNOWLEDGE_TEMPLATE.get("column"))
        if title_errors:
            # TODO@hcz: log
            return '\n'.join(title_errors)
        df["知识点"] = df[["知识点"]].ffill()
        columns = dict(zip(KNOWLEDGE_TEMPLATE.get("column"),
                           KNOWLEDGE_TEMPLATE.get("re_column")))
        df.rename(columns=columns, inplace=True)
        columns = KNOWLEDGE_TEMPLATE.get("re_column")
        # self.deal_with_classify(df, curr_col_idx=0)
        one_col = df.iloc[:, 0]
        col = list(one_col)
        data_list = []
        for i in range(0, len(col)):
            one_row = df.iloc[i, :]
            row = dict(one_row)
            row['doc_id'] = int(row.get('doc_id'))
            row = self.replace_nan(row)
            if i == 0:
                data_list.append(row)
            else:
                row = self.get_sub_row(data_list[-1], row, columns)
                data_list.append(row)
        return data_list

    def get_sub_row(self, parent_row, sub_row, columns):
        for col in columns:
            if parent_row[col] != sub_row[col]:
                if sub_row[col]:
                    break
                sub_row[col] = parent_row[col]
        return sub_row

    def replace_nan(self, row):
        """
        把一行的nan替换成空
        :param row:
        :return:
        """
        for key in row:
            if str(row[key]) == 'nan':
                row[key] = None
        return row

    def deal_with_classify(self, df, curr_col_idx=0):
        classfy_list = pd.unique(df.iloc[:, curr_col_idx])
        print(classfy_list)
        for classfy in classfy_list:
            sub_df = classfy_list[classfy_list[curr_col_idx] == classfy]
            for sub_df in sub_df:
                pass

    def check_column(self, df, columns):
        curr_cols = list(df.columns.values)
        error_list = []
        if curr_cols != columns:
            for curr, temp in zip(curr_cols, columns):
                if curr != temp:
                    s = 'title不对，当前[%s], 正确[%s]' % (curr, temp)
                    error_list.append(s)
        return error_list

    def get_knowledge_classify(self, knowledge_only='right', knowledge=''):
        """
        :param knowledge: 知识点类别（线程、等）
        :param knowledge_only: 只取知识点，下面的分级不要。
        :return: Tree(知识点->分级1->分级2...->方档编号)
        """
        q = db.session.query(KnowledgeClassify).order_by(KnowledgeClassify.gid)
        curr_col_idx = 1  # skip: GID
        if knowledge_only and knowledge_only.lower() in ('left',):
            k_df = pd.read_sql(q.statement, db.session.bind)
            knowledge_list = list(pd.unique(k_df.iloc[:, curr_col_idx]))
            knowledge_tree = {"tag": "技术文档", 'required': True,
                              'disabled': True, "sub_tags": [],
                              'type': "技术文档"}
            if knowledge_list:
                knowledge_tree["sub_tags"] = [{"tag": k, 'required': True,
                                               'disabled': True,
                                               'type': 'knowledge',
                                               "sub_tags": []}
                                              for k in list(knowledge_list)]
            return knowledge_tree
        else:
            if knowledge:
                q = q.filter(KnowledgeClassify.knowledge == knowledge)
            k_df = pd.read_sql(q.statement, db.session.bind)
            max_col = len(KnowledgeClassify.__table__.columns) - 2
            classify_tree = self._get_tree(k_df, curr_col_idx, max_col)
            return classify_tree

    def _get_tree(self, df, curr_col_idx, max_col=11):
        classify_list = list(pd.unique(df.iloc[:, curr_col_idx]))
        # column = KNOWLEDGE_TEMPLATE.get("re_column")[curr_col_idx + 1]
        # na_df = df[df[column].isnull]
        sub_list = []
        for classify in classify_list:
            classify_dict = {"title": classify, "doc_list": [], "sub": []}
            column = KNOWLEDGE_TEMPLATE.get("re_column")[curr_col_idx - 1]
            sub_df = df[df[column] == classify]
            if curr_col_idx == max_col:
                doc_list = self._get_doc_ids(sub_df, curr_col_idx, max_col)
                classify_dict["doc_list"] = doc_list
            else:
                doc_list = self._get_doc_ids(sub_df, curr_col_idx, max_col)
                classify_dict["doc_list"] = doc_list
                next_column = KNOWLEDGE_TEMPLATE.get("re_column")[curr_col_idx]
                sub_df = sub_df.dropna(subset=[next_column])
                # print(classify, column)
                # print(sub_df)
                sub = self._get_tree(sub_df, curr_col_idx + 1)
                classify_dict["sub"] = sub
            # doc_list
            sub_list.append(classify_dict)
        return sub_list

    def _get_doc_ids(self, df, curr_col_idx, max_col):
        """当前分类下的文档
        :param df:
        :param curr_col_idx:
        :return:
        """
        if curr_col_idx == max_col:
            doc_id_list = list(pd.unique(df.iloc[:, -1]))
        else:
            next_column = KNOWLEDGE_TEMPLATE.get("re_column")[curr_col_idx]
            # print(next_column)
            na_df = df[df[next_column].isnull()]  # 空：是叶子
            # print(na_df)
            doc_id_list = list(pd.unique(na_df.iloc[:, -1]))
        doc_id_list = [int(n) for n in doc_id_list]
        return doc_id_list


if __name__ == '__main__':
    obj = CtrlKnowledge()
    file_path = r'C:\Users\yuyin\Desktop\knowledge_20180626.xls'
    obj._import_excel(file_path)
