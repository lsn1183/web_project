from app.db import db
import json
import re
import os
from app.import_doc.ds_doc_import import DsDocImport
from app.ctrl.ctrl_ds_doc import CtrlDsDoc
from app.ctrl.ctrl_ds_section import CtrlDSSection
from app.db.ds_doc import Ds_Doc
from app.db.ds_section import DSSection
from app.db.spec.specification import HeaderFile


class IfDocImport(DsDocImport):

    def __init__(self):
        DsDocImport.__init__(self)
        self.image_source_url = ""

    def if_import(self, file_url, model_id, creator, doc_type, proj_id, f_txt, only_doc):
        if "&" in file_url:
            file_url = file_url.replace("&", "^&")
        json_url, result = DsDocImport().excel_to_json(file_url)
        if result:
            f_txt.write("解析出错的文件：" + file_url + "\n")
            return
        self.read_if_json(json_url, model_id, creator, doc_type, proj_id, f_txt, only_doc)

    def read_if_json(self, json_url, model_id, creator, doc_type, proj_id, f_txt, only_doc):
        update_time = self.get_current_time()
        try:
            with open(json_url, 'r', encoding='gbk') as load_f:
                load_dict = json.load(load_f)
        except:
            try:
                with open(json_url, 'r', encoding='utf8') as load_f:
                    load_dict = json.load(load_f)
            except:
                f_txt.write("异常文件：" + json_url + "\n")
                return
        if not load_dict:
            print("空json文件！")
        commit_list = []
        doc_name = load_dict.get('basicDesignName')
        doc_id = self.get_doc_by_model(model_id)
        doc_data = {'doc_type': doc_type, 'proj_id': proj_id,
                    'model_id': model_id, 'create_time': update_time, 'update_time': update_time,
                    'creator': creator, 'editor': creator,
                    'ver': '0.001', 'status': 1}
        self.init_version(doc_data, 'doc')
        parent_sec_id = 0
        if only_doc == "YES":
            if doc_id:
                CtrlDsDoc().delete(doc_id, "Admin", commit=False)
            doc_log = self.import_db(doc_data, Ds_Doc, Ds_Doc.doc_id)
            doc_id = doc_log.get('key_id')
            commit_list.append(doc_log)
            parent_usecase = {'sec_type': 'USERCASE', 'sec_title': doc_name, 'ver': '',
                              'doc_id': doc_id, 'explain': '', 'content': '[]', 'complement': '',
                              'parent_sec_id': 0, 'micro_ver': 1}
            uc_log = self.import_db(parent_usecase, DSSection, DSSection.sec_id)
            usecase_id = uc_log.get('key_id')
            commit_list.append(uc_log)
        else:
            if not doc_id:
                doc_log = self.import_db(doc_data, Ds_Doc, Ds_Doc.doc_id)
                doc_id = doc_log.get('key_id')
                commit_list.append(doc_log)
            else:
                commit_list += self.delete_section_by_name(doc_name, doc_id)
            parent_usecase = {'sec_type': 'USERCASE', 'sec_title': doc_name, 'ver': '',
                              'doc_id': doc_id, 'explain': '', 'content': '[]', 'complement': '',
                              'parent_sec_id': 0, 'micro_ver': 1}
            uc_log = self.import_db(parent_usecase, DSSection, DSSection.sec_id)
            parent_sec_id = uc_log.get('key_id')
            usecase_id = uc_log.get('key_id')
            commit_list.append(uc_log)
        commit_list += self.add_section(load_dict, doc_id, usecase_id, parent_sec_id)
        self.commit_log(commit_list, creator, update_time)
        db.session.commit()

    def add_section(self, load_dict, doc_id, usecase_id, parent_sec_id=0):
        usecase_list = load_dict.get('usecaseImaList')
        commit_list = self.import_section(usecase_list, "COMMON", doc_id, parent_sec_id)
        block_list = load_dict.get('blockImgList')
        commit_list += self.import_section(block_list, 'BLOCK', doc_id, parent_sec_id)
        class_list = load_dict.get('classImaList')
        commit_list += self.import_section(class_list, 'CLASS', doc_id, parent_sec_id)
        std_list = load_dict.get('stateImaList')
        commit_list += self.import_section(std_list, "STD", doc_id, parent_sec_id)
        seq_list = load_dict.get('sequenceImaList')
        commit_list += self.import_section(seq_list, "SEQUENCE", doc_id, usecase_id)
        return commit_list

    def import_section(self, section_list, type, doc_id, parent_sec_id=0):
        commit_list = []
        if not section_list:
            return commit_list
        for section in section_list:
            image_list = section.get('imageInfo')
            if not image_list:
                continue
            for image in image_list:
                url_list = image.get('imgFilePath')
                fileList = []
                for url in url_list:
                    url = self.replace_image_url(url)
                    fileList.append({"url": url, "name": "img"})
                fileList = self.remove_ip_message(fileList)
                explain = self.cut_introduce(image.get("imgIntroduce"))
                sec_title = image.get("imgTitle")
                complement = image.get("imgComplement")
                if sec_title:
                    sec_title = sec_title.strip("■")
                    sec_title.strip(" ")
                    sec_title.strip("\n")
                break
            str_content = json.dumps(fileList, ensure_ascii=False)
            section_dict = {'sec_type': type, 'sec_title': sec_title, 'ver': '',
                            'doc_id': doc_id, 'explain': explain, 'content': str_content, 'complement': complement,
                            'parent_sec_id': parent_sec_id, 'micro_ver': 1}
            log_dict = self.import_db(section_dict, DSSection, DSSection.sec_id)
            if log_dict and type == "SEQUENCE":
                seq_id = log_dict.get('key_id')
                commit_list += self.import_resource(seq_id)
            commit_list.append(log_dict)
        return commit_list

    def get_doc_by_model(self, model_id):
        from app.db.ds_doc import Ds_Doc
        q = (db.session.query(Ds_Doc).filter(Ds_Doc.model_id == model_id)
             .filter(Ds_Doc.doc_type == "IF").all())
        if q:
            return q[0].doc_id
        return False

    def delete_section_by_name(self, sec_name, doc_id):
        commit_list = []
        q = (db.session.query(DSSection).filter(DSSection.sec_title == sec_name)
             .filter(DSSection.doc_id == doc_id)
             .filter(DSSection.parent_sec_id == 0).first())
        if q:
            sec_id = q.sec_id
            commit_list = CtrlDSSection()._delete(sec_id, "Admin", delete="")
        return commit_list

    def insert_htm_url(self, sheet):
        start_row = 2
        max_row = sheet.max_row
        for row in range(start_row, max_row + 1):
            file_url = sheet.cell(row=row, column=2).value
            model_id = sheet.cell(row=row, column=4).value
            only_doc = sheet.cell(row=row, column=5).value
            if not model_id:
                continue
            proj_id = 10004
            doc_type = "IF"
            print("正在执行:" + file_url)
            q = (db.session.query(Ds_Doc).filter(Ds_Doc.model_id == model_id)
                 .filter(Ds_Doc.doc_type == doc_type)
                 .filter(Ds_Doc.proj_id == proj_id).first())
            doc_id = q.doc_id
            file_name = os.path.basename(file_url)
            new_file_name = file_name.replace(".xlsx", ".files")
            new_file_url = "Doxygen/if_html/%s/%s" % (new_file_name, "sheet002.htm")
            new_time = self.get_current_time()
            file_data = {'doc_id': doc_id, 'html_url': new_file_url, 'create_time': new_time}
            db.session.add(HeaderFile(**file_data))
        db.session.commit()
