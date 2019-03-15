# -*- coding: UTF-8 -*-
from app.db import db


class Project(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'project'

    proj_id = db.Column(db.Integer, primary_key=True)
    proj_name = db.Column(db.String(100))  # 项目标题
    manager = db.Column(db.String(30))  # 管理者
    summary = db.Column(db.String())  # 概述
    ver = db.Column(db.String(30))
    proj_tag_id = db.Column(db.Integer)  # 知识点分类项目下的tag_id
    create_time = db.Column(db.Date)  # 创建时间
    update_time = db.Column(db.Date)  # 更新时间

    def __repr__(self):
        return '<Project %r:%r>' % (self.proj_id, self.proj_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class ProjectFW(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'project_framework_rel'

    gid = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('ds.project.proj_id'))  # 项目ID
    fw_id = db.Column(db.Integer)  # 框架ID

    def __repr__(self):
        return '<ProjectFW %r:%r>' % (self.proj_id, self.fw_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class ProjectModel(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'project_models'

    gid = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('ds.project.proj_id'))  # 项目ID
    model_id = db.Column(db.Integer, db.ForeignKey('ds.model.model_id'))  # 模块ID

    def __repr__(self):
        return '<ProjectModel %r:%r>' % (self.proj_id, self.model_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class ProjectTag(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'project_tags'

    gid = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('ds.project.proj_id'))  # 项目ID
    tag_id = db.Column(db.Integer, db.ForeignKey('public.doc_tag_category.tag_id'))  # 模块ID

    def __repr__(self):
        return '<ProjectTag %r:%r>' % (self.proj_id, self.tag_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class ProjectModelRel(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'project_models_rel'

    gid = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('ds.project.proj_id'))  # 项目ID
    model_id = db.Column(db.Integer, db.ForeignKey('ds.model.model_id'))  # 模块ID
    parent_model_id = db.Column(db.Integer, db.ForeignKey('ds.model.model_id'))  # 父模块ID
    # model_gid = db.Column(db.Integer)
    # parent_gid = db.Column(db.Integer)  # 父GID

    def __repr__(self):
        return '<ProjectModelRel %r:%r>' % (self.proj_id, self.model_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class ProjectModelRef(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'project_models_ref_rel'

    gid = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('ds.project.proj_id'))  # 项目ID
    model_id = db.Column(db.Integer, db.ForeignKey('ds.model.model_id'))  # 模块ID
    ref_model_id = db.Column(db.Integer, db.ForeignKey('ds.model.model_id'))  # 关联模块ID

    def __repr__(self):
        return '<project_models_ref_rel %r:%r>' % (self.proj_id, self.model_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


