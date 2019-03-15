import time
from os import walk
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class EsSearch:
    def __init__(self, index_name, index_type, ip="127.0.0.1", port=9200):
        """
        :param index_name: 索引名称
        :param index_type: 索引类型
        """
        self.index_name = index_name
        self.index_type = index_type
        # 无用户名密码状态
        self.es = Elasticsearch([ip], port=port)
        # 用户名密码状态
        # self.es = Elasticsearch([ip], http_auth=('elastic', 'password'), port=port)

    def _create_index(self, index_name=None, index_type=None, index_type_dict=None):
        """
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param ex: Elasticsearch对象
        :return:
        """
        if not index_name:
            index_name = self.index_name
        if not index_type:
            index_type = self.index_type
        # 创建映射
        _index_mappings = {
            "mappings": {
                index_type: index_type_dict
            }
        }
        if not self.es.indices.exists(index=index_name):
            res = self.es.indices.create(index=index_name, body=_index_mappings)
            print('Created index %s' % index_name)
            print(res)

    def delete_index(self, index_name=None):
        if not index_name:
            index_name = self.index_name
        if self.es.indices.exists(index=index_name):
            print('delete index %s' % index_name)
            res = self.es.indices.delete(index_name)
            print(res)

    def insert_dataframe(self, df, id_col="", index_name=None, index_type=None):
        # import pandas as pd
        # pd.DataFrame.to_dict(orient="records")
        self.bulk(df.to_dict(orient="records"), id_col=id_col, index_name=index_name, index_type=index_type)

    def bulk(self, data_dict_list, id_col="", index_name=None, index_type=None):
        """
        用bulk将批量数据存储到es
        :return:
        """
        if not index_name:
            index_name = self.index_name
        if not index_type:
            index_type = self.index_type
        actions = []
        for data_dict in data_dict_list:
            action = {
                "_index": index_name,
                "_type": index_type,
                "_id": data_dict.get(id_col),  # id 也可以默认生成，不赋值
                "_source": data_dict
            }
            actions.append(action)
        success, _ = bulk(self.es, actions, raise_on_error=True)
        print('Performed %d actions' % success)

    def index_data(self):
        es = Elasticsearch()
        csvdir = 'D:/work/ElasticSearch/exportExcels'
        filenamelist = []
        for (dirpath, dirnames, filenames) in walk(csvdir):
            filenamelist.extend(filenames)
            break
        total = 0
        for file in filenamelist:
            csvfile = csvdir + '/' + file
            self.Index_Data_FromCSV(csvfile, es)
            total += 1
            print(total)
            time.sleep(10)

    def Index_Data_FromCSV(self, csvfile):
        """
        从CSV文件中读取数据，并存储到es中
        :param csvfile: csv文件，包括完整路径
        :return:
        """
        # list = CSVOP.ReadCSV(csvfile)
        index = 0
        doc = {}
        for item in list:
            if index > 1:# 第一行是标题
                doc['title'] = item[0]
                doc['link'] = item[1]
                doc['date'] = item[2]
                doc['source'] = item[3]
                doc['keyword'] = item[4]
                res = self.es.index(index=self.index_name, doc_type=self.index_type, body=doc)
                print(res['created'])
            index += 1
            print(index)

    def Index_Data(self):
        """
        数据存储到es
        :return:
        """
        list = [
            {"date": "2017-09-13",
                "source": "慧聪网",
                "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
                "keyword": "电视",
                "title": "付费 电视 行业面临的转型和挑战"
             },
            {"date": "2017-09-13",
                "source": "中国文明网",
                "link": "http://www.wenming.cn/xj_pd/yw/201709/t20170913_4421323.shtml",
                "keyword": "电视",
                "title": "电视 专题片《巡视利剑》广获好评：铁腕反腐凝聚党心民心"
             }
              ]
        for item in list:
            res = self.es.index(index=self.index_name, doc_type=self.index_type, body=item)
            print(res)

    def search(self, index_name=None, query_string='', from_=0, size=20):
        if not index_name:
            index_name = self.index_name
        body = {
            "query": {
                "query_string": {
                    "default_operator": "AND",
                    "query": query_string
                }
            },
        }
        return self.es.search(index=index_name, body=body, size=size, from_=from_)

    def total(self):
        res = self.es.search(index=self.index_name, body={"query": {"match_all": {}}})
        return res['hits']['total']

    def search_unique(self, index_name=None, field_name=None):
        if not index_name:
            index_name = self.index_name
        body = {
            "size": 0,
            "aggs": {
                "uniq_gender": {
                    "terms": {"field": field_name}
                }
                # "street_values": {
                #     "cardinality": {
                #         "field": field_name  # '%s.%s_raw' % (field_name, field_name)
                #      }
                # }
            }
        }
        # body = {
        #     "size": 0,
        #     "aggs": {
        #         "distinct_terminals": {
        #             "cardinality": {
        #                 "field": field_name
        #             }
        #         }
        #     }
        # }
        return self.es.search(index=index_name, body=body)

    # def bulk_Index_Data(self, datalist):
    #     """
    #     用bulk将批量数据存储到es
    #     :return:
    #     """
    #     list = [
    #         {"date": "2017-09-13",
    #          "source": "慧聪网",
    #          "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
    #          "keyword": "电视",
    #          "title": "付费 电视 行业面临的转型和挑战"
    #          },
    #         {"date": "2017-09-13",
    #          "source": "中国文明网",
    #          "link": "http://www.wenming.cn/xj_pd/yw/201709/t20170913_4421323.shtml",
    #          "keyword": "电视",
    #          "title": "电视 专题片《巡视利剑》广获好评：铁腕反腐凝聚党心民心"
    #          },
    #         {"date": "2017-09-13",
    #          "source": "人民电视",
    #          "link": "http://tv.people.com.cn/BIG5/n1/2017/0913/c67816-29533981.html",
    #          "keyword": "电视",
    #          "title": "中国第21批赴刚果（金）维和部隊启程--人民 电视 --人民网"
    #          },
    #         {"date": "2017-09-13",
    #          "source": "站长之家",
    #          "link": "http://www.chinaz.com/news/2017/0913/804263.shtml",
    #          "keyword": "电视",
    #          "title": "电视 盒子 哪个牌子好？ 吐血奉献三大选购秘笈"
    #          }
    #     ]
    #     ACTIONS = []
    #     i = 1
    #     for line in list:
    #         action = {
    #             "_index": self.index_name,
    #             "_type": self.index_type,
    #             "_id": i,  # id 也可以默认生成，不赋值
    #             "_source": {
    #                 "date": line['date'],
    #                 "source": line['source'].decode('utf8'),
    #                 "link": line['link'],
    #                 "keyword": line['keyword'].decode('utf8'),
    #                 "title": line['title'].decode('utf8')}
    #         }
    #         i += 1
    #         ACTIONS.append(action)
    #         # 批量处理
    #     success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
    #     print('Performed %d actions' % success)
    #
    # def Delete_Index_Data(self,id):
    #     """
    #     删除索引中的一条
    #     :param id:
    #     :return:
    #     """
    #     res = self.es.delete(index=self.index_name, doc_type=self.index_type, id=id)
    #     print(res)
    #
    # def Get_Data_Id(self, id):
    #     res = self.es.get(index=self.index_name, doc_type=self.index_type,id=id)
    #     print(res['_source'])
    #     print('------------------------------------------------------------------')
    #     #
    #     # # 输出查询到的结果
    #     for hit in res['hits']['hits']:
    #         # print hit['_source']
    #         print(hit['_source']['date'],hit['_source']['source'],hit['_source']['link'],hit['_source']['keyword'],hit['_source']['title'])
    #
    # def Get_Data_By_Body(self):
    #     # doc = {'query': {'match_all': {}}}
    #     doc = {
    #         "query": {
    #             "match": {
    #                 "keyword": "电视"
    #             }
    #         }
    #     }
    #     _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=doc)
    #     for hit in _searched['hits']['hits']:
    #         # print hit['_source']
    #         print(hit['_source']['date'], hit['_source']['source'], hit['_source']['link'], hit['_source']['keyword'],
    #               hit['_source']['title'])


if __name__ == "__main__":
    obj = EsSearch("ott", "ott_type", ip="192.168.64.172")
    # obj = ElasticObj("ott1", "ott_type1")
    # # obj.create_index()
    obj.Index_Data()
    obj.Get_Data_By_Body()

