# -*- coding: UTF-8 -*-
from app.db import db


class Framework(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'framework'

    fw_id = db.Column(db.Integer, primary_key=True)
    fw_name = db.Column(db.String(100))  # 框架名
    summary = db.Column(db.String())  # 概述
    content = db.Column(db.String())  # 框架图
    manager = db.Column(db.String(100))  # 管理者

    def __repr__(self):
        return '<Framework %r:%r>' % (self.proj_id, self.proj_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class FrameworkModel(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'framework_models'

    gid = db.Column(db.Integer, primary_key=True)
    fw_id = db.Column(db.Integer, db.ForeignKey('ds.framework.fw_id'))  # 框架ID
    model_id = db.Column(db.Integer, db.ForeignKey('ds.model.model_id'))  # 模块ID

    def __repr__(self):
        return '<FrameworkModels %r:%r>' % (self.fw_id, self.model_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class FrameworkModelRel(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'framework_models_rel'

    gid = db.Column(db.Integer, primary_key=True)
    fw_id = db.Column(db.Integer, db.ForeignKey('ds.framework.fw_id'))  # 框架ID
    model_id = db.Column(db.Integer, db.ForeignKey('ds.model.model_id'))  # 模块ID
    parent_model_id = db.Column(db.Integer)  # 父模块ID

    def __repr__(self):
        return '<FrameworkModelsRel %r:%r>' % (self.fw_id, self.model_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
