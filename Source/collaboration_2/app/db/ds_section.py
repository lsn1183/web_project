# -*- coding: UTF-8 -*-
from ..db import db
from sqlalchemy.schema import Sequence


class DSSection(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_section'

    sec_id = db.Column(db.Integer, primary_key=True)
    sec_type = db.Column(db.String(30), db.ForeignKey('ds.ds_section_type.sec_type'))  # 文档章节类别
    content = db.Column(db.String)  # 图片内容文本
    ver = db.Column(db.String(30))  # 本版
    doc_id = db.Column(db.Integer, db.ForeignKey('ds.ds_doc.doc_id'))  # 所属文档ID
    required = db.Column(db.Boolean)  # 模板使用：True: 必选，False：可选。
    order_id = db.Column(db.Integer)  # 排序用ID
    parent_sec_id = db.Column(db.Integer)  # 章节ID。0: 表示没有章节。
    micro_ver = db.Column(db.Integer)  # 微版本
    explain = db.Column(db.String)  # 说明
    complement = db.Column(db.String)  # 补足说明
    sec_title = db.Column(db.String)  # 标题名称

    def __repr__(self):
        return '<Section %r, %s>' % (self.sec_type, self.sec_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSSectionRel(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_section_rel'

    gid = db.Column(db.Integer, primary_key=True)
    sec_id = db.Column(db.Integer, db.ForeignKey('ds.ds_section.sec_id'))
    sec_rel_id = db.Column(db.Integer, db.ForeignKey('ds.ds_section.sec_id'))

    def __repr__(self):
        return '<SectionRel %r %r>' % (self.sec_id, self.sec_rel_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSSectionType(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_section_type'

    sec_type = db.Column(db.String(30), primary_key=True)
    describe = db.Column(db.String(100))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSSectionTag(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_section_tag_rel'

    gid = db.Column(db.Integer, primary_key=True)
    sec_id = db.Column(db.Integer, db.ForeignKey('ds.ds_section.sec_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('public.doc_tag_category.tag_id'))

    def __repr__(self):
        return '<SectionTag %r %r>' % (self.sec_id, self.tag_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSSectionResource(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_section_resource_rel'

    gid = db.Column(db.Integer, primary_key=True)
    sec_id = db.Column(db.Integer, db.ForeignKey('ds.ds_section.sec_id'))
    resource_id = db.Column(db.Integer, db.ForeignKey('ds.ds_resource.resource_id'))
    content = db.Column(db.String(1024))
    operator = db.Column(db.String(100))  # 不低于/不高于
    unit = db.Column(db.String(10))  # 单位
    value = db.Column(db.Integer)  # 数值

    def __repr__(self):
        return '<Resource %r, %r>' % (self.sec_id, self.resource_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

