# -*- coding: UTF-8 -*-
from app.db import db


class DBDocTagCat(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'doc_tag_category'

    tag_id = db.Column(db.Integer, primary_key=True)
    parent_tag_id = db.Column(db.Integer)  # 所属分类的TAG_ID
    tag = db.Column(db.String(256))  # TAG 名称
    rate = db.Column(db.String(10), default='normal')  # 使用频率
    remark = db.Column(db.String(1024))  # 备注、Title
    required = db.Column(db.Boolean, default=False)  # 必填

    def __repr__(self):
        return '<TAG Category %r>' % self.tag

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

