# -*- coding: UTF-8 -*-
from app.db import db


class Role(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100))
    cls = db.Column(db.String(100))  # 类别

    def __repr__(self):
        return '<Role %r>' % self.role_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d