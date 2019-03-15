from app.db import db
import json
import re
import os
import shutil
import os, sys
from PIL import Image
from PIL import BmpImagePlugin,GifImagePlugin,Jpeg2KImagePlugin,JpegImagePlugin,PngImagePlugin,TiffImagePlugin,WmfImagePlugin # added this line
from app.db.utility import Utillity
from flask import current_app
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_ds_doc import CtrlDsDoc
from app.db.ds_doc import Ds_Doc
from app.db.ds_section import DSSectionRel
from app.db.ds_doc_if import DSDocIf
from app.db.ds_section import DSSection
from app.db.ds_section import DSSectionResource
from app.ctrl.ctrl_ds_section import CtrlDSSection


class DsDocImport(CtrlBase):

    def __init__(self):
        CtrlBase.__init__(self)
        self.image_source_url = ""

    def excel_to_json(self, file_url):
        """
        把excel文档解析成json文件
        :param file_url:
        :return:
        """
        path = os.path.join(file_url)
        path = path.replace('\\', '/')
        cmd = "java -Xms4g -Xmx16g -jar C:/JavaWorkSpase/DesignImport_1/DesignImport_fat_1.jar %s" % (path,)
        # print(cmd)
        os_ret = os.system(cmd)
        if os_ret != 0:
            return None, "解析文件失败！文件名不能含有&，空格，()等字符！"
        excel_file = os.path.basename(file_url)
        file_name = os.path.splitext(excel_file)[0]
        file_path = file_url.replace(excel_file, file_name)
        json_url = os.path.join(file_path, "json", file_name+".json")
        json_url = json_url.replace("^", "")
        return json_url, None

    def replace_image_url(self, image_path):
        curr_app = current_app._get_current_object()
        if ".emf" in image_path:
            image_path = self.emf_to_jpeg(image_path)
        image_name = os.path.basename(image_path)
        uti = Utillity()
        only_id = uti.get_nextval()
        new_image_name = Utillity.get_new_file_name(image_name, only_id)
        new_image_url = os.path.join(curr_app.config.get("IMG_PATH_ROOT"), new_image_name)
        shutil.copyfile(image_path, new_image_url)
        image_url = Utillity.convert_url(curr_app.config.get('FILE_SRV_URL'), new_image_url)
        return image_url

    def read_json(self, json_url, model_id, creator, doc_type, proj_id=27, f_txt=None):
        update_time = self.get_current_time()
        try:
            with open(json_url, 'r', encoding='gbk') as load_f:
                load_dict = json.load(load_f)
        except:
            try:
                with open(json_url, 'r', encoding='utf8') as load_f:
                    load_dict = json.load(load_f)
            except:
                f_txt.write("异常文件："+json_url+"\n")
                return
        if not load_dict:
            print("空json文件！")
        doc_name = load_dict.get('basicDesignName')
        doc_id = self.get_doc_by_name(doc_name)
        if doc_id:
            CtrlDsDoc().delete(doc_id, "Admin", commit=False)
            # seq_list = CtrlDSSection().get_sequence2(doc_id)
            # if seq_list:
            #     # 把activity图都放在第一个时序图下面
            #     seq_id = seq_list[0].get('sec_id')
            #     act_list = load_dict.get('activityImaList')
            #     self.import_sequence(act_list, "Activity", doc_id, parent_sec_id=seq_id)
            #     db.session.commit()

        usecase_list = load_dict.get('usecaseImaList')
        if not usecase_list:
            f_txt.write("没有usecase的文件：" + json_url + "\n")
            return
        doc_data = {'doc_type': doc_type, 'title': doc_name, 'proj_id': proj_id,
                    'model_id': model_id, 'create_time': update_time, 'update_time': update_time,
                    'creator': creator, 'editor': creator, 'summary': '',
                    'ver': '', 'status': 1}
        self.init_version(doc_data, 'doc')
        commit_list = []
        doc_log = self.import_db(doc_data, Ds_Doc, Ds_Doc.doc_id)
        doc_id = doc_log.get('key_id')
        commit_list.append(doc_log)
        if_list = load_dict.get('ifList')
        commit_list += self.import_if(if_list, doc_id)
        usecase_log = self.import_section(usecase_list, "COMMON", doc_id)
        if usecase_log:
            commit_list.append(usecase_log)
        seq_list = load_dict.get('sequenceImaList')
        seq_commit = self.import_sequence(seq_list, "SEQUENCE", doc_id)
        commit_list = commit_list + seq_commit
        if seq_commit:
            seq_id = seq_commit[0].get('key_id')
            act_list = load_dict.get('activityImaList')
            commit_list += self.import_sequence(act_list, "Activity", doc_id, parent_sec_id=seq_id)
        std_list = load_dict.get('stateImaList')
        std_log = self.import_section(std_list, "STD", doc_id)
        if std_log:
            commit_list.append(std_log)
        block_list = load_dict.get('blockImgList')
        block_log = self.import_section(block_list, 'BLOCK', doc_id)
        if block_log:
            commit_list.append(block_log)
        class_list = load_dict.get('classImaList')
        class_log = self.import_section(class_list, 'CLASS', doc_id)
        if class_log:
            commit_list.append(class_log)
        self.commit_log(commit_list, creator, update_time)
        db.session.commit()
        from app.db import cache
        cache.delete('get_model_tree')  # 删除缓存

    def import_if(self, if_list, doc_id):
        commit_list = []
        if not if_list:
            return commit_list
        for if_dict in if_list:
            new_if = dict()
            new_if['doc_id'] = doc_id
            new_if['if_name'] = if_dict.get('ifName')
            new_if['parameter'] = if_dict.get('ifParam')
            new_if['return_val'] = if_dict.get('ifReturn')
            new_if['description'] = if_dict.get('ifRemake')
            new_if['micro_ver'] = 1
            if_log = self.import_db(new_if, DSDocIf, DSDocIf.if_id)
            commit_list.append(if_log)
        return commit_list

    def import_section(self, section_list, type, doc_id, parent_sec_id=0):
        if not section_list:
            return None
        fileList = []
        for section in section_list:
            image_list = section.get('imageInfo')
            if not image_list:
                return None
            for image in image_list:
                url = image.get('imgFilePath')
                url = self.replace_image_url(url)
                val = self.cut_introduce(image.get("imgIntroduce"))
                title = image.get("title")
                if title:
                    title = title.strip("■")
                    title.strip(" ")
                    title.strip("\n")
                fileList.append({"url": url, "name": "img"})
        content = [{"fileList": fileList, "val": val, "title": title}]
        str_content = json.dumps(content, ensure_ascii=False)
        section_dict = {'sec_type': type, 'content': str_content, 'ver': '',
                        'doc_id': doc_id, 'required': None, 'order_id': None,
                        'parent_sec_id': parent_sec_id, 'micro_ver': 1}
        log_dict = self.import_db(section_dict, DSSection, DSSection.sec_id)
        return log_dict

    def import_sequence(self, section_list, type, doc_id, parent_sec_id=0):
        commit_list = []
        if not section_list:
            return commit_list
        for section in section_list:
            image_list = section.get('imageInfo')
            for image in image_list:
                fileList = []
                url = image.get('imgFilePath')
                url = self.replace_image_url(url)
                fileList.append({"url": url, "name": "img"})
                val = self.cut_introduce(image.get("imgIntroduce"))
                title = image.get("title")
                if title:
                    title = title.strip("■")
                    title.strip(" ")
                    title.strip("\n")
                content = [{"fileList": fileList, "val": val, "title": title}]
                str_content = json.dumps(content, ensure_ascii=False)
                section_dict = {'sec_type': type, 'content': str_content, 'ver': '',
                                'doc_id': doc_id, 'required': None, 'order_id': None,
                                'parent_sec_id': parent_sec_id, 'micro_ver': 1}
                log_dict = self.import_db(section_dict, DSSection, DSSection.sec_id)
                if log_dict and type == "SEQUENCE":
                    seq_id = log_dict.get('key_id')
                    commit_list.append(log_dict)
                    commit_list += self.import_resource(seq_id)
        return commit_list

    # def import_section(self, section_list, type, doc_id, parent_sec_id=0):
    #     if not section_list:
    #         return None
    #     fileList = []
    #     val = ''
    #     for section in section_list:
    #         image_list = section.get('imageInfo')
    #         for image in image_list:
    #             url = image.get('imgFilePath')
    #             url = url.replace('/home/huangyp/temp', 'http://192.168.37.112:15000/DownFile/data/Image')
    #             fileList.append({"url": url, "name": "img"})
    #             if not val:
    #                 val = image.get("imgIntroduce")
    #             else:
    #                 val = val + '\n' + image.get("imgIntroduce")
    #     content = [{"fileList": fileList, "val": val, "title": ""}]
    #     str_content = json.dumps(content, ensure_ascii=False)
    #     section_dict = {'sec_type': type, 'content': str_content, 'ver': '',
    #                     'doc_id': doc_id, 'required': None, 'order_id': None,
    #                     'parent_sec_id': 0, 'micro_ver': 1}
    #     log_dict = self.import_db(section_dict, DSSection, DSSection.sec_id)
    #     return log_dict

    def cut_introduce(self, introduce):
        result = re.findall("■.*\n", introduce)
        if result:
            return introduce.replace(result[0], "")
        else:
            return introduce

    def emf_to_jpeg(self, emf_imag_file):
        Image._initialized = 2  # added this line
        f, e = os.path.splitext(emf_imag_file)
        outfile = f + ".jpg"
        if emf_imag_file != outfile:
            im = Image.open(emf_imag_file).convert('RGB')
            im.save(outfile, "JPEG")  # added "JPEG"
            im.close()
            del im
        return outfile

    def import_resource(self, seq_id):
        resource_list = [{'sec_id': seq_id, 'resource_id': 1, 'content': '',
                          'operator': '', 'unit': '', 'value': None},
                         {'sec_id': seq_id, 'resource_id': 2, 'content': '',
                          'operator': '', 'unit': '', 'value': None},
                         {'sec_id': seq_id, 'resource_id': 3, 'content': '',
                          'operator': '', 'unit': '', 'value': None},
                         {'sec_id': seq_id, 'resource_id': 4, 'content': '',
                          'operator': '', 'unit': '', 'value': None},
                         ]
        commit_list = self.add_list(DSSectionResource, resource_list, [], DSSectionResource.gid, [])
        return commit_list

    def import_db(self, doc_data, db_object, key_id):
        log_dict = self.common_add(db_object, doc_data, None, [], key_id)
        return log_dict

    def get_doc_by_name(self, doc_name):
        from app.db.ds_doc import Ds_Doc
        q = db.session.query(Ds_Doc).filter(Ds_Doc.title == doc_name).all()
        if q:
            return q[0].doc_id
        return False




