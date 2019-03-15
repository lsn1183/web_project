# -*- coding: UTF-8 -*-
from ..db import db


class DSFailure(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_failure'

    item_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))  # 文档类别: BASIC基本设计, DETAIL: 详细设计
    major_item = db.Column(db.String(100))  # 主項目
    failure = db.Column(db.String(256))  # 心配点（故障モード）

    def __repr__(self):
        return '<Failure %r>' % self.failure

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
