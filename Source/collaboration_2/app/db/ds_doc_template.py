# -*- coding: UTF-8 -*-
from ..db import db
from sqlalchemy import ForeignKey


class DSDocTemplate(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_doc_template'

    doc_id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.String(30))  # 文档类别: BASIC基本设计, DETAIL: 详细设计
    title = db.Column(db.String(256))  # 文档标题
    ver = db.Column(db.String(30))  # 文档版本
    create_time = db.Column(db.Date)  # 创建时间
    update_time = db.Column(db.Date)  # 更新时间
    creator = db.Column(db.String(30))  # 文档创建者
    editor = db.Column(db.String(30))  # 最后更新人/编辑者

    def __repr__(self):
        return '<Title %r>' % self.title

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
