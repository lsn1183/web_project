import os
import json
import shutil
from app.db.utility import Utillity
from flask import current_app
from app.ctrl.ctrl_base import CtrlBase
from app.db.ds_doc import Ds_Doc
from app.db.spec.specification import Specification
from app.db.ds_rel_specification import DSRelSpec
from app.db.ds_doc_if import DSDocIf
from app.db.ds_section import DSSection
from app.db.ds_section import DSSectionResource
from app.ctrl.ctrl_ds_section import CtrlDSSection, CtrlDSResource


class ImportDocBase(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.image_source_url = ""  # 图片的原地址

    def excel_to_json(self, file_url):
        """
        把excel文档解析成json文件
        :param file_url:
        :return:
        """
        path = os.path.join(file_url)
        path = path.replace('\\', '/')
        file_url = file_url.replace('&', '%26')
        cmd = '''java -Xms4g -Xmx16g -jar DesignImport/DesignImport_fat.jar %s''' % (path,)
        print(cmd)
        os_ret = os.system(cmd)
        if os_ret != 0:
            return None, "解析文件失败！请检查文档格式是否正确！"
        excel_file = os.path.basename(file_url)
        self.image_source_url = "import_root"
        file_name = os.path.splitext(excel_file)[0]
        file_path = file_url.replace(excel_file, file_name)
        json_url = os.path.join(file_path, "json", file_name+".json")
        return json_url, None

    def read_json(self, json_url, model_id, creator, doc_type, proj_id=27):
        commit_list = []
        update_time = self.get_current_time()
        try:
            with open(json_url, 'r', encoding='gbk') as load_f:
                load_dict = json.load(load_f)
        except:
            with open(json_url, 'r', encoding='utf8') as load_f:
                load_dict = json.load(load_f)
        key_id_dict = dict()
        doc_name = load_dict.get('basicDesignName')
        if not doc_name:
            error = "文档名不能为空！"
            return [], error
        doc_summary = load_dict.get('basicDesignSummary')
        new_doc_data = {'doc_type': doc_type, 'title': doc_name, 'proj_id': proj_id,
                        'model_id': model_id, 'create_time': update_time, 'update_time': update_time,
                        'creator': creator, 'editor': creator, 'summary': doc_summary,
                        'ver': '', 'status': 1}
        doc_log = self.add_ds_doc(new_doc_data, key_id_dict)
        if doc_log:
            commit_list.append(doc_log)
        if_list = load_dict.get("ifList")
        commit_list += self.add_if_list(if_list, key_id_dict)
        usecase_list = load_dict.get("usecaseImaList")
        if not usecase_list:
            error = "缺少USECASE图信息！"
            return [], error
        common_data = self.get_new_sections(usecase_list, 'COMMON', key_id_dict)
        if common_data:
            commit_list += self.add_section(common_data, key_id_dict, "COMMON")
        ucInfo = usecase_list[0].get('ucInfo')
        usecase_data, usecase_rel_list = self.usecase_info(ucInfo, key_id_dict, parent_sec_id=0, sec_type="USERCASE")
        if usecase_data:
            commit_list += self.add_section(usecase_data, key_id_dict, 'USERCASE')
            log_list, error = self.add_func_list(load_dict.get("reqFuncList"), key_id_dict)
            if error:
                return [], error
            commit_list += log_list
        block_data = self.get_new_sections(load_dict.get("blockImgList"), 'BLOCK', key_id_dict)
        if block_data:
            commit_list += self.add_section(block_data, key_id_dict, "BLOCK")
        class_data = self.get_new_sections(load_dict.get("classImaList"), 'CLASS', key_id_dict)
        if class_data:
            commit_list += self.add_section(class_data, key_id_dict, "CLASS")
        std_data = self.get_new_sections(load_dict.get("stateImaList"), 'STD', key_id_dict)
        if std_data:
            commit_list += self.add_section(std_data, key_id_dict, "STD")
        seq_data, resource_data = self.get_new_sections(load_dict.get("sequenceImaList"), 'SEQUENCE', key_id_dict)
        if seq_data:
            commit_list += self.add_section(seq_data, key_id_dict, "SEQUENCE")
            log_list, error = self.update_resource(resource_data, key_id_dict)
            if error:
                return [], error
            commit_list += log_list
        section_dict, error = self.get_new_activity(load_dict.get("activityImaList"), key_id_dict)
        if error:
            return [], error
        if section_dict:
            commit_list += self.update_activity(section_dict, key_id_dict)
        log_list, error = self.add_section_rel(usecase_rel_list, key_id_dict)
        if error:
            return [], error
        if log_list:
            commit_list += log_list
        return commit_list, None

    def add_ds_doc(self, new_doc_data, key_id_dict):
        col_list = [Ds_Doc.title.name, Ds_Doc.summary.name]
        old_data = dict()
        title = new_doc_data.get('title')
        proj_id = new_doc_data.get('proj_id')
        model_id = new_doc_data.get('model_id')
        old_data_list = self.get_old_data(Ds_Doc, [Ds_Doc.proj_id, Ds_Doc.model_id, Ds_Doc.title],
                                          {"proj_id": proj_id, "model_id": model_id, "title": title})
        if old_data_list:
            old_data = old_data_list[0]
            new_doc_data["doc_id"] = old_data.get("doc_id")
            new_doc_data["creator"] = old_data.get("creator")
            new_doc_data["create_time"] = old_data.get("create_time")
            new_doc_data["status"] = self.update_version(old_data.get("status"))
        log_dict = self.common_add(Ds_Doc, new_doc_data, old_data, col_list, Ds_Doc.doc_id)
        if log_dict:
            doc_id = log_dict.get('key_id')
        else:
            doc_id = old_data.get("doc_id")
        key_id_dict["doc_id"] = doc_id
        return log_dict

    def add_if_list(self, if_list, key_id_dict):
        col_list = [DSDocIf.if_name.name, DSDocIf.description.name,
                    DSDocIf.parameter.name, DSDocIf.return_val.name]
        doc_id = key_id_dict.get("doc_id")
        new_data_list = []
        for if_data in if_list:
            new_if = dict()
            new_if['doc_id'] = doc_id
            new_if['if_name'] = if_data.get('ifName')
            new_if['parameter'] = if_data.get('ifParam')
            new_if['return_val'] = if_data.get('ifReturn')
            new_if['description'] = if_data.get('ifRemake')
            new_if['micro_ver'] = 1
            old_if = self.get_old_data(DSDocIf, [DSDocIf.if_name, DSDocIf.doc_id],
                                       {"if_name": if_data.get('ifName'), "doc_id": doc_id})
            if old_if:
                new_if['if_id'] = old_if[0].get("if_id")
                new_if['micro_ver'] = self.update_version(old_if[0].get("micro_ver"))
            new_data_list.append(new_if)
        old_data_list = self.get_old_data(DSDocIf, DSDocIf.doc_id, doc_id)
        commit_list = self.add_list(DSDocIf, new_data_list, old_data_list, DSDocIf.if_id, col_list)
        return commit_list

    def add_func_list(self, funcList, key_id_dict):
        commit_list = []
        doc_id = key_id_dict.get("doc_id")
        new_data_list = []
        for func in funcList:
            file_name = func.get("funcFileName")
            spec_data = self.get_old_data(Specification, Specification.spec_file_name, file_name)
            if not spec_data:
                error = "%s不在数据库中！" % file_name
                return commit_list, error
            ucNo = func.get("usecaseNo")
            uc_id = key_id_dict.get(ucNo)
            if not uc_id:
                error = "%s对应的%s不存在！" % (file_name, ucNo)
                return commit_list, error
            func_id = func.get("funcID")
            spec_id = spec_data[0].get('spec_id')
            new_data = {"doc_id": doc_id, "sec_id": None, "spec_id": spec_id, "func_id": ""}
            doc_spec_data = self.get_old_data(DSRelSpec, [DSRelSpec.doc_id, DSRelSpec.spec_id],
                                              {"doc_id": doc_id, "spec_id": spec_id})
            if not doc_spec_data:
                # 文档缺少式样书时先添加
                commit_list.append(self.common_add(DSRelSpec, new_data, None, [], DSRelSpec.gid))
            sec_spec_data = self.get_old_data(DSRelSpec, [DSRelSpec.sec_id, DSRelSpec.spec_id],
                                              {"sec_id": uc_id, "spec_id": spec_id})
            if sec_spec_data:
                new_data["gid"] = sec_spec_data[0].get("gid")
            new_data["sec_id"] = uc_id
            new_data["func_id"] = func_id
            new_data_list.append(new_data)
        old_spec_list = self.get_old_data(DSRelSpec, DSRelSpec.doc_id, doc_id)
        old_data_list = []
        for old_data in old_spec_list:
            if old_data.get('sec_id'):
                old_data_list.append(old_data)
        commit_list += self.add_list(DSRelSpec, new_data_list, old_data_list,
                                     DSRelSpec.gid, [DSRelSpec.func_id.name])
        return commit_list, None

    def add_section(self, section_data, key_id_dict, sec_type):
        commit_list = []
        col_list = [DSSection.content.name]
        doc_id = key_id_dict.get("doc_id")
        old_data_list = CtrlDSSection().get_session_by_doc(doc_id, sec_type)
        if sec_type in ('BLOCK', 'CLASS', 'STD', 'COMMON'):
            # 只有一个， section_data是个字典
            old_data = None
            if old_data_list:
                old_data = old_data_list[0]
                section_data['sec_id'] = old_data.get('sec_id')
                section_data['micro_ver'] = self.update_version(old_data.get('micro_ver'))
                old_content = old_data.get('content')
            else:
                old_content = [{'fileList': [], 'val': '', 'title': ''}]
                old_content = json.dumps(old_content, ensure_ascii=False)
            section_data['content'] = self.diff_section_image(section_data.get('content'), old_content)
            log_dict = self.common_add(DSSection, section_data, old_data, col_list, DSSection.sec_id)
            if log_dict:
                commit_list.append(log_dict)
        elif sec_type in ('SEQUENCE', 'USERCASE'):
            # 可能有多个，section_data是个list
            if sec_type == 'SEQUENCE':
                secNo = 'seqNo'
            if sec_type == 'USERCASE':
                secNo = 'ucNo'
            for old_data in old_data_list:
                if sec_type == 'SEQUENCE':
                    old_data[secNo] = 'Sequence%s' % str(old_data_list.index(old_data)+1)
                if sec_type == 'USERCASE':
                    old_data[secNo] = 'UC%s' % str(old_data_list.index(old_data)+1)
            sec_nos = []
            for section in section_data:
                sec_nos.append(section.get(secNo))
            del_section_data = []
            for old_data in old_data_list:
                if old_data.get(secNo) not in sec_nos:
                    old_data.pop(secNo)
                    del_section_data.append(old_data)
            commit_list += self.delete_section(del_section_data)
            for section in section_data:
                old_data = None
                old_content = [{'fileList': [], 'val': '', 'title': ''}]
                old_content = json.dumps(old_content, ensure_ascii=False)
                sec_no = section.pop(secNo)
                for old_sec in old_data_list:
                    if old_sec.get(secNo) == sec_no:
                        old_sec.pop(secNo)
                        old_data = old_sec
                        section['sec_id'] = old_data.get('sec_id')
                        section['micro_ver'] = self.update_version(old_data.get('micro_ver'))
                        old_content = old_data.get('content')
                        break
                section['content'] = self.diff_section_image(section.get('content'), old_content)
                log_dict = self.common_add(DSSection, section, old_data, col_list, DSSection.sec_id)
                if log_dict:
                    sec_id = log_dict.get('key_id')
                    key_id_dict[sec_no] = sec_id
                    commit_list.append(log_dict)
                else:
                    sec_id = old_data.get("sec_id")
                    key_id_dict[sec_no] = sec_id
        return commit_list

    def diff_section_image(self, new_content, old_content):
        """
        比较新旧图片是否相同，相同使用旧图片，不同拷贝新图片到文件服务器
        并使用新地址
        :param new_content:
        :param old_content:
        :return:
        """
        new_content_json = json.loads(new_content)
        old_content_json = json.loads(old_content)
        new_file_list = new_content_json[0].get('fileList')
        old_file_list = old_content_json[0].get('fileList')
        for image in new_file_list:
            new_url = image.get("url")
            index = new_file_list.index(image)
            if index < len(old_file_list):
                old_url = old_file_list[index].get("url")
                result = Utillity.diff_image(new_url, old_url)
                if result:
                    image["url"] = old_url
                    continue
            image["url"] = self.replace_image_url(new_url)
        new_content = json.dumps(new_content_json, ensure_ascii=False)
        return new_content

    def replace_image_url(self, image_path):
        curr_app = current_app._get_current_object()
        image_name = os.path.basename(image_path)
        uti = Utillity()
        if ".emf" in image_path:
            image_path = Utillity.emf_to_jpeg(image_path)
        only_id = uti.get_nextval()
        new_image_name = Utillity.get_new_file_name(image_name, only_id)
        new_image_url = os.path.join(curr_app.config.get("IMG_PATH_ROOT"), new_image_name)
        shutil.copyfile(image_path, new_image_url)
        image_url = Utillity.convert_url(curr_app.config.get('FILE_SRV_URL'), new_image_url)
        return image_url

    def add_section_rel(self, usecase_rel_list, key_id_dict):
        commit_list = []
        sec_rel_dict = dict()
        for usecase_rel in usecase_rel_list:
            ucNo = usecase_rel.get("ucNo")
            seqNo = usecase_rel.get("seqNo")
            uc_id = key_id_dict.get(ucNo)
            seq_id = key_id_dict.get(seqNo)
            if not uc_id or not seq_id:
                error = "%s或%s不存在！" % (ucNo, seqNo)
                return [], error
            else:
                if seq_id not in sec_rel_dict:
                    sec_rel_dict[seq_id] = [uc_id]
                else:
                    sec_rel_dict[seq_id].append(uc_id)
        for seq_id in sec_rel_dict:
            uc_id_list = sec_rel_dict.get(seq_id)
            commit_list += CtrlDSSection().update_sec_rel(seq_id, uc_id_list)
        return commit_list, None

    def update_resource(self, resource_data, key_id_dict):
        commit_list = []
        col_list = ['content', 'operator', 'unit', 'value']
        for resource in resource_data:
            old_resource = None
            seqNo = resource.pop("seqNo")
            sec_id = key_id_dict.get(seqNo)
            if not sec_id:
                error = seqNo+"不存在！"
                return [], error
            resource['sec_id'] = sec_id
            old_data = self.get_old_data(DSSectionResource, [DSSectionResource.sec_id, DSSectionResource.resource_id],
                                         {"sec_id": sec_id, "resource_id": resource["resource_id"]})
            if old_data:
                old_resource = old_data[0]
                resource['gid'] = old_resource.get('gid')
            log_dict = self.common_add(DSSectionResource, resource, old_resource, col_list, DSSectionResource.gid)
            if log_dict:
                commit_list.append(log_dict)
        return commit_list, None

    def delete_section(self, old_section_list):
        commit_list = []
        for old_section in old_section_list:
            sec_id = old_section.get('sec_id')
            commit_list += CtrlDSSection()._delete(sec_id, None, delete='')
            # commit_list += CtrlDSSection().delete_sec_rel(sec_id)
            # commit_list += CtrlDSSection().delete_resource(sec_id)
        # commit_list += self.add_list(DSSection, [], old_section_list, DSSection.sec_id, [])
        return commit_list

    def get_new_sections(self, section_data, sec_type, key_id_dict, parent_sec_id=0):
        doc_id = key_id_dict.get('doc_id')
        if sec_type in ('BLOCK', 'CLASS', 'STD', 'COMMON'):
            if not section_data:
                return None
            section = section_data[0]
            image_data = section.get('imageInfo')
            section_dict = self._section_dict(image_data, doc_id, parent_sec_id, sec_type)
            return section_dict
        elif sec_type == 'SEQUENCE':
            section_list = []
            resource_data = []
            if not section_data:
                return []
            for section in section_data:
                image_data = section.get('imageInfo')
                section_dict = self._section_dict(image_data, doc_id, parent_sec_id, sec_type)
                section_dict['seqNo'] = 'Sequence%s' % str(section_data.index(section)+1)
                resourInfo = section.get("resourInfo")
                resource_data += self.get_resource_info(resourInfo, section_dict['seqNo'])
                section_list.append(section_dict)
            return section_list, resource_data

    def get_new_activity(self, section_data, key_id_dict):
        doc_id = key_id_dict.get('doc_id')
        if not section_data:
            return [], None
        activity_dict = dict()
        for section in section_data:
            sheetName = section.get("sheetName")
            ind = sheetName.index("_")
            seq_id = key_id_dict.get("Sequence%s" % sheetName[ind + 1])
            act_no = int(sheetName[ind + 3])
            if not seq_id:
                error = "%s的父级Sequence%s不存在！" % (sheetName, sheetName[ind + 1])
                return [], error
            else:
                if seq_id not in activity_dict:
                    activity_dict[seq_id] = []
                image_data = section.get('imageInfo')
                section_dict = self._section_dict(image_data, doc_id, seq_id, sec_type="Activity")
                section_dict['act_no'] = act_no
                activity_dict[seq_id].append(section_dict)
        return activity_dict, None

    def update_activity(self, activity_dict, key_id_dict):
        commit_list = []
        col_list = [DSSection.content.name]
        for key in key_id_dict:
            if 'Sequence' in key:
                seq_id = key_id_dict.get(key)
                if seq_id not in activity_dict:
                    old_data_list = self.get_old_data(DSSection, [DSSection.parent_sec_id, DSSection.sec_type],
                                                      {"parent_sec_id": seq_id, "sec_type": "Activity"})
                    commit_list += self.delete_section(old_data_list)
        for seq_id in activity_dict:
            activity_list = activity_dict.get(seq_id)
            old_data_list = self.get_old_data(DSSection, [DSSection.parent_sec_id, DSSection.sec_type],
                                              {"parent_sec_id": seq_id, "sec_type": "Activity"})
            for old_data in old_data_list:
                old_data["act_no"] = old_data_list.index(old_data) + 1
            act_no_list = []
            for activity in activity_list:
                act_no_list.append(activity.get('act_no'))
            del_section_data = []
            for old_data in old_data_list:
                if old_data.get('act_no') not in act_no_list:
                    old_data.pop('act_no')
                    del_section_data.append(old_data)
            commit_list += self.delete_section(del_section_data)
            for activity in activity_list:
                old_data = None
                old_content = [{'fileList': [], 'val': '', 'title': ''}]
                old_content = json.dumps(old_content, ensure_ascii=False)
                act_no = activity.pop('act_no')
                for old_sec in old_data_list:
                    if old_sec.get('act_no') == act_no:
                        old_sec.pop('act_no')
                        old_data = old_sec
                        activity['sec_id'] = old_data.get('sec_id')
                        activity['micro_ver'] = self.update_version(old_data.get('micro_ver'))
                        old_content = old_data.get('content')
                        break
                activity['content'] = self.diff_section_image(activity.get('content'), old_content)
                log_dict = self.common_add(DSSection, activity, old_data, col_list, DSSection.sec_id)
                if log_dict:
                    commit_list.append(log_dict)
        return commit_list

    def _section_dict(self, image_data, doc_id, parent_sec_id, sec_type):
        fileList = []
        title = image_data.get('imgTitle')
        val = image_data.get("imgIntroduce")
        url_list = image_data.get('imgFilePath')
        for url in url_list:
            fileList.append({"url": url, "name": "img"})
        content = [{"fileList": fileList, "val": val, "title": title}]
        str_content = json.dumps(content, ensure_ascii=False)
        section_dict = {'sec_type': sec_type, 'content': str_content, 'ver': '',
                        'doc_id': doc_id, 'required': None, 'order_id': None,
                        'parent_sec_id': parent_sec_id, 'micro_ver': 1}
        return section_dict

    def usecase_info(self, usecase_info, key_id_dict, parent_sec_id, sec_type):
        doc_id = key_id_dict.get("doc_id")
        usecse_list, usecase_rel_list = [], []
        ucNo_list = []
        for usecase in usecase_info:
            title = usecase.get('ucTile')
            val = usecase.get("ucIntroduce")
            ucNo = usecase.get("ucNo")
            seqNo = usecase.get("seqNo")
            content = [{"fileList": [], "val": val, "title": title}]
            str_content = json.dumps(content, ensure_ascii=False)
            section_dict = {'ucNo': ucNo, 'sec_type': sec_type, 'content': str_content, 'ver': '',
                            'doc_id': doc_id, 'required': None, 'order_id': None,
                            'parent_sec_id': parent_sec_id, 'micro_ver': 1}
            rel_dict = {"ucNo": ucNo, "seqNo": seqNo}
            if ucNo not in ucNo_list:
                usecse_list.append(section_dict)
                ucNo_list.append(ucNo)
            usecase_rel_list.append(rel_dict)
        return usecse_list, usecase_rel_list

    def get_resource_info(self, resource_info, seqNo):
        resource_list = CtrlDSResource().get_resource()
        resource_id_dict = dict()
        for resource in resource_list:
            resource_id_dict[resource['rsc_name']] = resource.get('resource_id')
        resource_data = []
        for resource in resource_info:
            rsc_name = resource.get('title')
            content = resource.get('value')
            resource_id = resource_id_dict.get(rsc_name)
            rs_dict = {'seqNo': seqNo, 'resource_id': resource_id, 'content': content,
                       'operator': '', 'unit': '', 'value': None}
            if rsc_name in ("CPU", "内存") and content:
                value_list = content.split(" ")  # 用空格分解内容
                rs_dict['content'] = ""
                rs_dict['operator'] = value_list[0]
                rs_dict['value'] = value_list[1]
                rs_dict['unit'] = value_list[2]
            resource_data.append(rs_dict)
        return resource_data
