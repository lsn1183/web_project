# -*- coding: UTF-8 -*-
from app.db import db


class UserRoles(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'user_roles'

    gid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))  # 用户id
    role_id = db.Column(db.Integer, db.ForeignKey('public.role.role_id'))  # 角色id

    def __repr__(self):
        return '<UserRoles %r:%r>' % (self.user_id, self.role_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

