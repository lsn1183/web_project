# -*- coding: UTF-8 -*-
from ..db import db


class KnowledgeClassify(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'knowledge_classify'

    gid = db.Column(db.Integer, primary_key=True)
    knowledge = db.Column(db.String(100))
    classify1 = db.Column(db.String(100))
    classify2 = db.Column(db.String(100))
    classify3 = db.Column(db.String(100))
    classify4 = db.Column(db.String(100))
    classify5 = db.Column(db.String(100))
    classify6 = db.Column(db.String(100))
    classify7 = db.Column(db.String(100))
    classify8 = db.Column(db.String(100))
    classify9 = db.Column(db.String(100))
    classify10 = db.Column(db.String(100))
    doc_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Title %r>' % (self.knowledge, self.classify1, self.classify2,
                               self.classify3, self.classify4, self.classify5)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
