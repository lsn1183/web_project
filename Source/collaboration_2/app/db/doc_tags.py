# -*- coding: UTF-8 -*-
from ..db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class DocTags(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'doc_tags'

    gid = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('public.docs.doc_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('public.doc_tag_category.tag_id'))
    # tags = relationship("Doc", backref="doc_tags")
    # doc = relationship("Doc", foreign_keys=[doc_id])

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
