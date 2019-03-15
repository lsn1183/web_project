# -*- coding: UTF-8 -*-
from app.db import db


class DsResource(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_resource'

    resource_id = db.Column(db.Integer, primary_key=True)
    rsc_name = db.Column(db.String(100))  # 资源
    type = db.Column(db.String(100))  # 填写类型

    def __repr__(self):
        return '<Resource %r>' % self.rsc_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
