# -*- coding: UTF-8 -*-
from ..db import db


class Comment(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'comment'

    gid = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer)  # 文档ID
    sec_id = db.Column(db.Integer)  # 章节ID
    content = db.Column(db.String(2048))  # 评论内容
    commentator = db.Column(db.String(30))
    cm_time = db.Column(db.DateTime)

    def __repr__(self):
        return ('<Comment doc_id:%r, sec_id:%r, content:%r>' %
                (self.doc_id, self.sec_id, self.content))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
