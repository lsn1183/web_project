from app.db import db
from app.ctrl.ctrl_base import CtrlBase
from app.db.ds_section import DSSection
import json


class UpdateOldSection(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def update(self):
        q = db.session.query(DSSection).order_by(DSSection.sec_id)
        for section in q:
            content = section.content
            if not content:
                continue
            file_list, val, title = self.dismantling_json(content)
            section.content = json.dumps(file_list, ensure_ascii=False)
            if val in (None, 'null'):
                val = ''
            if title in (None, 'null'):
                title = ''
            section.explain = val
            section.sec_title = title
        db.session.commit()

    def dismantling_json(self, str_content):
        json_content = json.loads(str_content)
        fileList = json_content[0].get("fileList")
        val = json_content[0].get("val")
        title = json_content[0].get("title")
        return fileList, val, title