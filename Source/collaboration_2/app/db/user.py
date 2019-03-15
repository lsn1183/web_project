# -*- coding: UTF-8 -*-
from app.db import db


class User(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.String(100))
    username = db.Column(db.String(100))
    email = db.Column(db.String(256))
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(50))  # 用户类型：TESE:后台测试账号； NORMAL:员工账号

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
