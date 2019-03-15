# -*- coding: UTF-8 -*-
from ..db import db
from sqlalchemy.schema import Sequence


class Ds_Doc(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_doc'

    doc_id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.String(10), db.ForeignKey('ds.ds_doc_type.doc_type'))  # 文档类别: BASIC基本设计, DETAIL: 详细设计
    title = db.Column(db.String(256))  # 文档标题
    ver = db.Column(db.String(30))  # 文档版本
    model_id = db.Column(db.Integer, db.ForeignKey('ds.model.model_id'))  # 文档所属模块
    proj_id = db.Column(db.Integer, db.ForeignKey('ds.project.proj_id'))  # 文档所属项目
    create_time = db.Column(db.Date)  # 创建时间
    update_time = db.Column(db.Date)  # 更新时间
    creator = db.Column(db.String(30))  # 文档创建者
    editor = db.Column(db.String(30))  # 最后更新人/编辑者
    summary = db.Column(db.String)  # 概要信息
    major_ver = db.Column(db.Integer)  # 主版本
    minor_ver = db.Column(db.Integer)  # 小版本
    micro_ver = db.Column(db.Integer)  # 微版本
    status = db.Column(db.Integer, db.ForeignKey('ds.ds_doc_status.status_id'))  # 作业状态

    def __repr__(self):
        return '<Title %r>' % self.title

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSDocType(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_doc_type'

    # doc_type_id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.String(30), primary_key=True)
    describe = db.Column(db.String(100))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSDocStatus(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_doc_status'

    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(100))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSDocConsider(db.Model):
    """考虑点
    """
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_doc_consider'

    gid = db.Column(db.Integer, primary_key=True)
    sec_id = db.Column(db.Integer)  # 设计文档ID
    consider_id = db.Column(db.Integer)  # 技术文档ID
    consider_content = db.Column(db.String(2048))  # 考虑内容
    checked = db.Column(db.Boolean)

    def __repr__(self):
        return '<Consider %r>' % self.consider

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSDocAstahRel(db.Model):
    """Astah文件
    """
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_doc_astah_rel'

    gid = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('ds.ds_attach.attach_id'))  # 设计文档ID
    attach_id = db.Column(db.Integer)  # 关联文件id

    def __repr__(self):
        return '<Astah文件 %r>' % self.gid

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSDocDetailRel(db.Model):
    """基本设计与详细设计父子关系表
    """
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'detail_doc_rel'

    gid = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('ds.ds_doc.doc_id'))  # 详细设计文档id
    parent_doc_id = db.Column(db.Integer)  # 基本设计文档id

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d




