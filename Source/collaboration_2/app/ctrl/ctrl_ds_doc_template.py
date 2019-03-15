# -*- coding: UTF-8 -*-
from app.db import db
from app.db.ds_doc import Ds_Doc
from app.db.ds_doc_template import DSDocTemplate as DocTemp
from app.db.ds_section import DSSection
from app.db.ds_section import DSSectionType
from app.ctrl.ctrl_ds_section import CtrlDSSection
from app.ctrl.ctrl_doc_tag import CtrlDocTag


class CtrlDSDocTemplate(object):
    def __init__(self):
        pass

    def get_doc_template(self, doc_type=''):
        q = db.session.query(DocTemp)
        if doc_type:
            q = q.filter(DocTemp.doc_type == doc_type)
        templates = []
        for template in q:
            template_id = template.doc_id
            template = template.to_dict()
            sections = self.get_template_sections(template_id)
            template[DocTemp.create_time.name] = template.get(DocTemp.create_time.name).strftime("%Y-%m-%d %H:%M:%S %Z")
            template[DocTemp.update_time.name] = (template.get(DocTemp.update_time.name).strftime("%Y-%m-%d %H:%M:%S %Z"))
            template["sections"] = sections
            templates.append(template)
        return templates

    def get_template_sections(self, doc_id):
        q = db.session.query(DSSection.sec_id,
                             DSSection.sec_type,
                             DSSectionType.describe)
        q = q.filter(DSSection.sec_type == DSSectionType.sec_type)
        q = q.filter(DSSection.doc_id == doc_id)
        q = q.order_by(DSSection.order_id)
        sections = []
        all_tags = CtrlDocTag().get_all_tag()
        ctrl_sec = CtrlDSSection()
        for sec in q:
            sec_id = sec[0]
            data = {DSSection.sec_id.name: sec_id,
                    DSSection.sec_type.name: sec[1],
                    DSSectionType.describe.name: sec[2]}
            tags = ctrl_sec.get_tags(sec_id, all_tags)
            data["tags"] = tags
            sections.append(data)
        return sections
