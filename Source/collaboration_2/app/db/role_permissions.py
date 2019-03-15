# -*- coding: UTF-8 -*-
from app.db import db


class RolePermission(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'role_permissions'

    gid = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('public.role.role_id'))  # 角色id
    perm_id = db.Column(db.Integer, db.ForeignKey('public.permission.perm_id'))  # 权限id

    def __repr__(self):
        return '<RolePermission %r:%r>' % (self.role_id, self.perm_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
