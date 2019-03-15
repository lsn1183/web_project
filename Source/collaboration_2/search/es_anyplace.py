import os
import re
import pandas as pd
import datetime
from search.es_search import EsSearch



class EsAnyplace(EsSearch):
    def __init__(self, index_name='anyplace', index_type="bugs", ip="192.168.64.172", port=9200):
        """
        :param index_name: 索引名称
        """
        EsSearch.__init__(self, index_name, index_type=index_type, ip=ip, port=port)
        # self.proj_index_name = '_'.join([index_name, 'proj'])
        # self.proj_index_type = 'projects'

    def create_index(self):
        """
        :return:
        """
        index_type_dict = {
            "properties": {
                "number": {  # 管理番号
                    "type": "text",  #
                    "index": True,
                    # "analyzer": "keyword",
                    # "analyzer": "keyword",
                    # "fielddata": True,
                },
                "status": {  # ステータス
                    "type": "text",
                    "index": True,
                    "analyzer": "keyword",
                    # "analyzer": "not_analyzed",
                    # "index": True,
                    "fielddata": True,
                },
                "rank": {  # ランク
                    "type": "text",  # keyword只能完整的检索
                    "index": True,
                    # "analyzer": "keyword",
                    "fielddata": True,
                },
                "subject": {
                    "type": "text",
                    "index": True,
                },
                "症状詳細": {
                    "type": "text",
                    "index": True,
                },
                "調査結果": {
                    "type": "text",
                    "index": True,
                },
                "原因の説明": {
                    "type": "text",
                    "index": True,
                },
                "対策方針": {
                    "type": "text",
                    "index": True,
                },
                "対策内容": {
                    "type": "text",
                    "index": True,
                },
                "発見日": {
                    "type": "text",
                    "index": True,
                },
                "所属(発見者)": {
                    "type": "text",
                    "index": True,
                },
                "発見者": {
                    "type": "text",
                    "index": True,
                },
                "配布日": {
                    "type": "text",
                    "index": True,
                },
                "調査・対策日": {
                    "type": "text",
                    "index": True,
                },
                "所属（調査・対策者）": {
                    "type": "text",
                    "index": True,
                },
                "調査・対策者": {
                    "type": "text",
                    "index": True,
                },
                "調査・対策3（機能G名）": {
                    "type": "text",
                    "index": True,
                },
                "調査・対策4（修正めどの有無）": {
                    "type": "text",
                    "index": True,
                },
                "調査・対策5（修正予定日）": {
                    "type": "text",
                    "index": True,
                },
                "確認日(対策側)": {
                    "type": "text",
                    "index": True,
                },
                "確認日(発行側)": {
                    "type": "text",
                    "index": True,
                },
                "照査日": {
                    "type": "text",
                    "index": True,
                },
                "承認日": {
                    "type": "text",
                    "index": True,
                },
                "作成日": {
                    "type": "text",
                    "index": True,
                },
                "作成者": {
                    "type": "text",
                    "index": True,
                },
                "最終回覧日": {
                    "type": "text",
                    "index": True,
                },
                "所属（回覧者）": {
                    "type": "text",
                    "index": True,
                },
                "回覧者":{
                    "type": "text",
                    "index": True,
                },
                "作成2": {
                    "type": "text",
                    "index": True,
                },
                "作成5": {
                    "type": "text",
                    "index": True,
                },
                "作成6": {
                    "type": "text",
                    "index": True,
                },
                "原因区分": {
                    "type": "text",
                    "index": True,
                },
                "作り込み工程": {
                    "type": "text",
                    "index": True,
                },
                "確認日（対策側）・時刻": {
                    "type": "text",
                    "index": True,
                },
                "問処展開先管理番号": {
                    "type": "text",
                    "index": True,
                },
                "問処展開元管理番号": {
                    "type": "text",
                    "index": True,
                },
                "問処展開元の元": {
                    "type": "text",
                    "index": True,
                },
                "問処展開元の元の元": {
                    "type": "text",
                    "index": True,
                },
                "調査・対策2（水平展開結果）": {
                    "type": "text",
                    "index": True,
                },
                "対策バージョン": {
                    "type": "text",
                    "index": True,
                },
                "重複問処": {
                    "type": "text",
                    "index": True,
                },
                "project": {  # プロジェクト名
                    "type": "keyword",  # keyword只能完整的检索
                    "index": True,
                    # "fielddata": True,
                    # "index": "not_analyzed",
                },
                "最終回覧日・時刻": {
                    "type": "text",
                    "index": True,
                },
                "open_date": {
                    "type": "text",
                    "index": True,
                },
                "close_date": {
                    "type": "text",
                    "index": True,
                },
                "問処更新日": {
                    "type": "text",
                    "index": True,
                },
                "作成7(検出グレード)": {
                    "type": "text",
                    "index": True,
                },
                "作成8(検出仕向け)": {
                    "type": "text",
                    "index": True,
                },
                "作成9(検出工程(車両))": {
                    "type": "text",
                    "index": True,
                },
                "発見工程": {
                    "type": "text",
                    "index": True,
                },
                "共通02": {
                    "type": "text",
                    "index": True,
                },
                "作成日・時刻": {
                    "type": "text",
                    "index": True,
                },
                "共通01": {
                    "type": "text",
                    "index": True,
                },
                # "title": {
                #     "type": "text",
                #     "index": True,
                #     "analyzer": "ik_max_word",
                #     "search_analyzer": "ik_max_word"
                # },
                # "date": {
                #     "type": "text",
                #     "index": True
                # },
                # "keyword": {
                #     "type": "string",
                #     "index": "not_analyzed"
                # },
                # "source": {
                #     "type": "string",
                #     "index": "not_analyzed"
                # },
                # "link": {
                #     "type": "string",
                #     "index": "not_analyzed"
                # }
            }
        }
        self._create_index(index_type_dict=index_type_dict)
        # self._create_proj_index()

    def delete_all_index(self):
        self.delete_index(self.index_name)
        # self.delete_index(self.proj_index_name)

    def _create_proj_index(self):
        """创建项目名称的索引
        :return:
        """
        index_type_dict = {
            "properties": {
                "project": {
                    "type": "text",
                    "index": True,
                }
            }
        }
        self._create_index(index_name=self.proj_index_name,
                           index_type=self.proj_index_type,
                           index_type_dict=index_type_dict)

    def import_anyplace_csv_dir(self, dir_path):
        print(datetime.datetime.now())
        for file_name in os.listdir(dir_path):
            if os.path.splitext(file_name)[1] == '.csv':
                full_path = os.path.join(dir_path, file_name)
                print(full_path)
                self.import_anyplace_csv_file(full_path)
        print(datetime.datetime.now())

    def import_anyplace_csv_file(self, file):
        df = pd.read_csv(file)
        columns = {"管理番号": "number",
                   "ランク": "rank",
                   "プロジェクト名": "project",
                   "ステータス": "status",
                   "件名（概略）": "subject"}
        df.rename(columns=columns, inplace=True)
        df.fillna('', inplace=True)
        self.insert_dataframe(df, id_col="number")


if __name__ == "__main__":
    obj = EsAnyplace(ip="192.168.64.172")
    ######################################
    # obj.delete_all_index()
    # obj.create_index()
    # # # # obj.import_anyplace_csv_file(r'C:\Users\hongchenzai\Desktop\latest_history\17TMOP-370B-APL.csv')
    # obj.import_anyplace_csv_dir(r'Y:')
    ######################################
    # print(obj.total())
    # result = obj.search(query_string='status:配布 rank:S', size=40)
    # result = obj.search(query_string='17', size=40)
    # result = obj.search(query_string='project:17TMOP-L2-APL')
    # for hit in result["hits"]["hits"]:
    #     print(hit.get("_source"))
    # res = obj.search_one_anyplace('number:14-609-1-00002')
    result2 = obj.search_unique(field_name='number')
    print(result2)

    # result3 = obj.find_key_name()
    # print(result2)
    # result3 = obj.search_unique(field_name='status')
    # print(result3)
    pass
