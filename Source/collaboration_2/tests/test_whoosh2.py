# 方法一 使用FileStorage对象
from whoosh.filedb.filestore import FileStorage
storage = FileStorage('index')  # idx_path 为索引路径
idx1 = storage.open_index(indexname='idx1')

from whoosh import index
# 方法二 使用open_dir函数
from whoosh.index import open_dir
idx2 = open_dir('index', indexname='idx2')  # indexname 为索引名
print(index.exists_in('index', indexname='idx2'))
pass

from whoosh.qparser import QueryParser, MultifieldParser, OrGroup, FieldsPlugin

og = OrGroup.factory(0.9)

qp = QueryParser("content", schema=idx1.schema)  # group=OrGroup
qp.remove_plugin_class(FieldsPlugin)
q = qp.parse("reset")
print(q)
# mqp = MultifieldParser(["title", "content"], schema=idx1.schema)
# mq = mqp.parse(u"many only")
#
# from whoosh.query import *
# myquery = And([Term("title", u"third"), q])
# # myquery = Term("title", u"ird")
# print(myquery)
searcher = idx1.searcher()
r = (searcher.search(q=q, limit=None))
print(len(r))
for hit in r:
    t = dict(hit)
    print(hit)
searcher1 = idx1.searcher()
print(list(searcher1.lexicon("content")))

# print(QueryParser().parse(u"alpha OR beta gamma"))

