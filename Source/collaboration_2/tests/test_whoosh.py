from whoosh.fields import Schema, ID, TEXT
from whoosh import index
import os

if not os.path.exists('index'):
    os.mkdir('index')

schema = Schema(path=ID(unique=True, stored=True),
                title=TEXT(stored=True),
                content=TEXT(stored=True),
                tags=TEXT,
                icon=TEXT)
ix = index.create_in("index", schema, indexname='idx1')
writer = ix.writer()

writer.add_document(title=u"My document", content=u"This is my document!",
                    path=u"/a", tags=u"first short", icon=u"/icons/star.png")
writer.add_document(title=u"Second try", content=u"XMモジュールRESET処理機能ON/OFF設定.",
                    path=u"/b", tags=u"second short", icon=u"/icons/sheep.png")
writer.add_document(title=u"Third time's the charm", content=u"Examples are many.",
                    path=u"/c", tags=u"short", icon=u"/icons/book.png")
writer.commit()
ix = index.create_in("index", schema, indexname='idx2')
writer = ix.writer()
writer.update_document(path=u"/a", content="Replacement for the first document", title=u'c')
writer.commit()

from whoosh.analysis import LowercaseFilter, RegexTokenizer, StandardAnalyzer, StemmingAnalyzer

# tokenizer = RegexTokenizer()
# Lowercase = LowercaseFilter
# for token in Lowercase(tokenizer(u"These ARE the things I want!")):
#     print(repr(token.text))
# analyzer = StandardAnalyzer()
# for token in analyzer(u"2.1.1.1.-1通常地図"):
#     print(repr(token.text))

import MeCab

# mecab = MeCab.Tagger("-Ochasen")
# words = mecab.parse("東京スカイツリー")
# print(words)
