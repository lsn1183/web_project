# -*- coding: UTF-8 -*-
from app.db import db
from app.db.spec.specification import Specification


class CtrlSpecification(object):
    def __init__(self):
        pass

    def get(self, proj_id=None, search_str=''):
        q = db.session.query(Specification)
        if proj_id:
            q = q.filter(Specification.proj_id == proj_id)
        if search_str:
            q = q.filter(Specification.search_str
                         .ilike('%' + search_str + '%'))
        q = q.order_by(Specification.spec_type.desc(),
                       Specification.spec_name)
        # print(q.statement)
        spec_list = []
        for spec in q:
            spec_dict = spec.to_dict()
            spec_dict.pop(Specification.search_str.name)
            spec_dict["title"] = '[%s]-%s-%s' % (spec.spec_type,
                                                 spec.spec_file_name,
                                                 spec.spec_name)
            spec_list.append(spec_dict)
        return spec_list
