# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""


from Source.spec2db_server.common.db_access_base import DBAccessBase


class DocTag(DBAccessBase):
    """
    """
    def __init__(self):
        DBAccessBase.__init__(self)
        self.table_name = ""
        self.model_table_name = ""
        self.model_type_table_name = ""
        self.key_col = ""
        self.id_col = ""
        self.attr_list = []
        self.sub_list_name = ""
        self.parent_col_name = ""
        self.child_id_col = ""

    def get_tag_tree(self, valid=False):
        self._pg.connect(cursor_type=True)
        sqlcmd = """
        SELECT tag_id, parent_tag_id, tag
          FROM public.doc_tag_category
          order by parent_tag_id, tag_id 
        """
        tag_list = []
        try:
            self._pg.execute(sqlcmd)
            rows = self._pg.fetchall()
            tag_dict = {}
            for row in rows:
                tag_info = dict(row)
                parent_tag_id = tag_info["parent_tag_id"]
                if not parent_tag_id:
                    tag_info["sub_tags"] = list()
                    tag_dict[tag_info["tag_id"]] = tag_info
                else:
                    p_tag_info = tag_dict.get(parent_tag_id)
                    if p_tag_info:
                        sub_tags = p_tag_info["sub_tags"]
                        tag_info["parent_tag"] = p_tag_info.get("tag")
                        sub_tags.append(tag_info)
            tag_list = sorted(tag_dict.itervalues(), key=lambda x: x.get("tag_id"))
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return tag_list

    def add_tag(self, request_data):
        result = {}
        self._pg.connect(cursor_type=True)
        sqlcmd = """
                INSERT INTO public.doc_tag_category(
                parent_tag_id, tag)
                VALUES (%s,%s);
                """
        try:
            parent_tag_id = request_data.get('parent_tag_id')
            if parent_tag_id and not self._is_parent_tag(self._pg, parent_tag_id):
                result = {"result": "NG", "error": 'TAG分类不存在!'}
            else:
                tag = request_data.get('tag')
                self._pg.execute(sqlcmd, [parent_tag_id, tag])
                self._pg.commit()
                result = {"result": "OK"}
        except Exception as e:
            print e
            result["error"] = str(e)
        finally:
            self._pg.close()
        return result

    def update_tag(self, tag_id, request_data):
        result = {}
        self._pg.connect(cursor_type=True)
        sqlcmd = """
                UPDATE public.doc_tag_category
                SET parent_tag_id=%s, tag=%s
                WHERE tag_id =%s;
                """
        try:
            parent_tag_id = request_data.get('parent_tag_id')
            if parent_tag_id and not self._is_parent_tag(self._pg, parent_tag_id):
                result = {"result": "NG", "error": 'TAG分类不存在!'}
            else:
                tag = request_data.get('tag')
                self._pg.execute(sqlcmd, [parent_tag_id, tag, tag_id])
                self._pg.commit()
                result = {"result": "OK"}
        except Exception as e:
            print e
            result["error"] = str(e)
        finally:
            self._pg.close()
        return result

    def _is_parent_tag(self, pg, tag_id):
        sqlcmd = """
        select *
        from public.doc_tag_category
        where tag_id = %s and parent_tag_id = 0
        """
        pg.execute(sqlcmd, [tag_id])
        row = pg.fetchone()
        if row:
            return True
        return False

    def delete_tag(self, tag_id):
        result = {}
        self._pg.connect(cursor_type=True)
        sqlcmd = """
                DELETE
                FROM
                public.doc_tag_category
                WHERE tag_id = %s or parent_tag_id = %s;
                        """
        try:
            self._pg.execute(sqlcmd, [tag_id, tag_id])
            self._pg.commit()
            result = {"result": "OK"}
        except Exception as e:
            print e
            result["error"] = str(e)
        finally:
            self._pg.close()
        return result


if __name__ == '__main__':
    import os
    os.chdir('../')
    obj = DocTag()
    obj._pg.connect(cursor_type=True)
    print obj._is_parent_tag(obj._pg, 1)
