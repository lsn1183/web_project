# -*- coding: UTF-8 -*-
from app.db import db


class Permission(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'permission'

    perm_id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(100))  # 模块名
    perm_name = db.Column(db.String(100))  # 权限名称
    cls = db.Column(db.String(100))  # 类别

    def __repr__(self):
        return '<Permission %r-->%r>' % (self.module_name, self.perm_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
