# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""
import os
from Source.spec2db_server.hmi.hmi_base import HMIBase
from Source.spec2db_server.arl.arl_diff import ArlDiff
from Source.spec2db_server.hmi.hmi_base import HMIBase
import json

DOC_TYPE_FILE = 'file'
DOC_TYPE_URL = 'url'


class Doc(HMIBase):
    """
    """
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = "docs"
        self.key_col = "doc_id"
        self.model_table_name = 'doc_tags'
        self.db_schema = 'public'
        self.attr_list = ["doc_id", "doc_type", "doc_title", "path",
                          "ver", "author", "committer", "create_time",
                          "update_time", "summary"]

    def get_by_key_id(self, key_id, pg=None):
        if not pg:
            self._pg.connect(cursor_type=True)
            data = self._get_by_key_id(self._pg, key_id)
        return data

    def _get_by_key_id(self, pg, key_id):
        sqlcmd = """
        SELECT *
        FROM public.{table}
        where {key_col} = %s;
        """.format(table=self.table_name, key_col=self.key_col)
        pg.execute(sqlcmd, [key_id])
        data = dict()
        row = pg.fetchone()
        if row:
            data = dict(row)
            tags = self._get_tags(pg, key_id)
            data["tags"] = tags
        return data

    def _get_tags(self, pg, key_id):
        sqlcmd = """
        SELECT a.tag_id, tag
          FROM public.doc_tags as a
          LEFT JOIN public.doc_tag_category as b
          ON a.tag_id = b.tag_id
          where doc_id = %s
          order by tag_id
        """
        pg.execute(sqlcmd, [key_id])
        rows = pg.fetchall()
        tags = []
        for row in rows:
            tags.append(dict(row))
        return tags

    def get_by_tag(self, tag_id):
        sqlcmd = """
        SELECT distinct a.*
          FROM public.docs as a
          INNER JOIN (
            SELECT gid, doc_id, tag_id
              FROM public.doc_tags
              where tag_id = %s or tag_id in (
                SELECT tag_id
                  FROM public.doc_tag_category
                  where parent_tag_id = %s
              )
          ) AS b
          on a.doc_id = b.doc_id
          order by a.doc_id
        """
        self._pg.connect(cursor_type=True)
        self._pg.execute(sqlcmd, [tag_id, tag_id])
        rows = self._pg.fetchall()
        doc_list = []
        for row in rows:
            doc = dict(row)
            doc["tags"] = self._get_tags(self._pg, doc[self.key_col])
            doc_list.append(doc)
        return doc_list

    def add(self, request_date):
        data = dict()
        file_upload = ''
        if request_date.files:
            file_upload = request_date.files['file']
            if file_upload:
                file_name = file_upload.filename
                from Source.collaboration.api_if import app
                path = app.config.get("DOC_PATH_ROOT")
                if not os.path.exists(path):
                    os.makedirs(path)
                path = os.path.join(path, file_name)
                if os.path.exists(path):
                    print ("文件已经存在!", file_name)
                    return False, u'文件已经存在!'
                file_upload.save(path)  # 保存上传的文件
                data["doc_type"] = DOC_TYPE_FILE
                data["doc_title"] = request_date.form.get('doc_title')
                # data["doc_type"] = request_date.form.get('doc_type')
                data["ver"] = request_date.form.get('ver')
                data["author"] = request_date.form.get('author')  # 作者',
                data["committer"] = request_date.form.get('committer')  # 提交者'
                data["tags"] = request_date.form.get('Tags')
                if data["tags"]:
                    data["tags"] = data["tags"].split(',')
                data["summary"] = request_date.form.get("summary")
            else:
                return False, u'缺少文件!'
        else:
            data = request_date.get_json()
            data["doc_type"] = DOC_TYPE_URL
            if 'Tags' in data:
                data["tags"] = data.get("Tags")
            path = data.get("path")
        if not path:
            return False, u'请指定Url或上传文件!'
        try:
            self._pg.connect(cursor_type=True)
            data["path"] = path
            data["update_time"] = self.get_current_time()
            data["create_time"] = data["update_time"]
            self._common_add(self._pg, data, data["update_time"])
            self._pg.commit()
            self._pg.close()
            return True, 'OK'
        except Exception as e:
            print(e)
            if file_upload:
                os.remove(path)  # 删除文件
            if self._pg.connected:
                self._pg.conn.rollback()
            self._pg.close()
            return False, str(e)

    def add2(self, request_date):
        try:
            data = request_date.get_json(force=True)
            data["doc_type"] = DOC_TYPE_URL
            path = data.get('path')
            if not path:
                return False, u'请指定Url或上传文件!'
            self._pg.connect(cursor_type=True)
            if data.get("Tags"):
                data["tags"] = data.get("Tags")
            data["update_time"] = self.get_current_time()
            data["create_time"] = data["update_time"]
            self._common_add(self._pg, data, data["update_time"])
            self._pg.commit()
            self._pg.close()
            return True, 'OK'
        except Exception as e:
            print(e)
            if self._pg.connected:
                self._pg.conn.rollback()
            self._pg.close()
            return False, str(e)

    def delete(self, doc_id):
        rst = False
        message = ''
        try:
            self._pg.connect(cursor_type=True)
            doc_info = self._get_by_key_id(self._pg, doc_id)
            self._delete_tags(self._pg, doc_id)
            sqlcmd = self.list_2_delete_sql(self.table_name, [self.key_col])
            self._pg.execute(sqlcmd, [doc_id])
            self._delete_file(doc_info.get("doc_type"), doc_info.get("path"))
            self._pg.commit()
            rst = True
        except Exception as e:
            print(e)
            self._pg.conn.rollback()
            message = str(e)
        finally:
            self._pg.close()
            return rst, message

    def _delete_tags(self, pg, doc_id):
        sqlcmd = "DELETE FROM doc_tags where doc_id = %s"
        pg.execute(sqlcmd, [doc_id])

    def _delete_file(self, doc_type, path):
        if doc_type == DOC_TYPE_FILE:
            if os.path.exists(path):
                os.remove(path)

    def update(self, doc_id, request_date):
        data = dict()
        need_del_old_file = False
        self._pg.connect(cursor_type=True)
        old_doc_info = self._get_by_key_id(self._pg, doc_id)
        if not old_doc_info:
            return False, u'没有这个文件!'
        if request_date.files:
            file_upload = request_date.files['file']
            if file_upload:
                file_name = file_upload.filename
                from Source.collaboration.api_if import app
                path = app.config.get("DOC_PATH_ROOT")
                if not os.path.exists(path):
                    os.mkdir(path)
                path = os.path.join(path, file_name)
                if old_doc_info.get("path") != path:  # 文件变化了, 旧的要删除
                    need_del_old_file = True
                file_upload.save(path)  # 保存上传的文件
                data["doc_type"] = DOC_TYPE_FILE
            else:
                path = request_date.form.get('path')
                data["doc_type"] = request_date.form.get('doc_type')
                if data.get("doc_type") == DOC_TYPE_URL:
                    need_del_old_file = True
        if not path:
            return False, u'请指定Url或上传文件!'
        try:
            data["path"] = path
            data["doc_title"] = request_date.form.get('doc_title')
            data["ver"] = request_date.form.get('ver')
            data["author"] = request_date.form.get('author')  # 作者',
            data["committer"] = request_date.form.get('committer')  # 提交者'
            data["tags"] = request_date.form.get('tags')
            if data["tags"]:
                data["tags"] = json.loads(data["tags"])
            data["summary"] = request_date.form.get ("summary")
            data["update_time"] = self.get_current_time()
            data["create_time"] = data["update_time"]
            self._common_add(self._pg, data, data["update_time"])
            if need_del_old_file:  # 删除旧的文件
                self._delete_file(old_doc_info.get("doc_type"),
                                  old_doc_info.get("path"))
            self._pg.commit()
            self._pg.close()
            return True, 'OK'
        except Exception as e:
            print(e)
            if file_upload:
                os.remove(path)  # 删除文件
            if self._pg.connected:
                self._pg.conn.rollback()
            self._pg.close()
            return False, str(e)

    def common_add(self, pg, data, update_time=''):
        self._common_add(pg, data, update_time)
        pg.commit()

    def _common_add(self, pg, data, update_time=''):
        key_id = data.get(self.key_col)
        old_data = None
        if key_id:
            old_data = self._get_by_key_id(pg, key_id)
        ignore_col_list = []
        diff_obj = ArlDiff(self.key_col, self.id_col,
                           self.attr_list, ignore_col_list)
        diff_result = diff_obj.diff(old_data, data)
        action = diff_result.get("action")
        if action == "same":
            return None
        if action == "add":
            rc_id = self._add_one2(pg, data, self.attr_list[1:])
            data[self.key_col] = rc_id
            diff_result[self.key_col] = rc_id
            self._add_model_list(pg, rc_id, data.get("tags"))
        elif action == "change" or old_data:
            col_change_list = self.attr_list[1:]
            data[self.key_col] = old_data.get(self.key_col)
            # col_change_list = diff_result.get("col_change_list")
            if col_change_list:
                self.update_col_change_list(pg, data[self.key_col], data,
                                            col_change_list)
                # if not self.update_col_change_list(pg, data[self.key_col],
                #                                    data, col_change_list):
                #     return None
                # ## 先删除, 再添加
                self._delete_tags(pg, key_id)
                self._add_model_list(pg, data[self.key_col], data.get("tags"))
        else:
            pass
        # log_list = self.convert2log([diff_result])
        return True

    def _add_model_list(self, pg, doc_id, tags):
        if not doc_id or not tags:
            return
        model_list_change = []
        for tag_id in tags:
            # model_id = d.get("model_id")
            order_no = self._insert_model(pg, doc_id, tag_id)
        return model_list_change

    def _insert_model(self, pg, doc_id, tag_id):
        sqlcmd = """
        INSERT INTO {db_schema}.{table_name}(
                    {record_col}, tag_id)
            VALUES (%s, %s) returning gid;
        """.format(table_name=self.model_table_name,
                   record_col=self.key_col,
                   db_schema=self.db_schema)
        pg.execute(sqlcmd, (doc_id, tag_id))
        return self.fetch_id(pg)


def main():
    data = {"doc_type": 'url', # u'file:本地方件，url：url地址',
            "doc_title": '文档Tile',
            "path": u'Url地址',  # 注：上传文件时，不是填
            "file": u'方件',   # 注：如果上似是的文件
            "ver": u'版本号',
            "author": u'作者',
            "committer": '提交者',  # 注：当前用户
            "tags": [10, 12]
    }
    obj = Doc()
    obj._pg.connect(cursor_type=True)
    # obj.delete(11)
    data["update_time"] = obj.get_current_time()
    data["create_time"] = data["update_time"]
    obj.update()
    # obj.common_add(obj._pg, data, data["update_time"])
    pass


if __name__ == '__main__':
    import sys, os
    os.chdir('../')
    main()

