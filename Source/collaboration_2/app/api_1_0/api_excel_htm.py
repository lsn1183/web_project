import os
from flask_restful import Resource
from flask import request
from flask import current_app
from token_manage import auth
from app.ctrl.ctrl_excel_htm import CtrlExcelHtm
from app.db.utility import Utillity



class ApiExcelHtm(Resource):
    # @auth.login_required
    def post(self):
        # import pythoncom
        # pythoncom.CoInitialize()
        result = {"result": "NG", 'error': ''}
        try:
            file_upload = request.files['file']  # 前端拿文件
            file_name = file_upload.filename
            curr_app = current_app._get_current_object()
            file_path = curr_app.config.get("TEMP_HTML_PATH_ROOT")  # Z:\temp\spec_html

            # 保存到的路径
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            uti = Utillity()
            only_id = uti.get_nextval()
            new_file_name = file_name
            # new_file_name = Utillity.get_new_file_name(file_name, only_id)  # 给文件加上唯一id
            # new_file_name = '%s-%s' % (str(only_id), file_name)
            # local_file_path = os.path.join(file_path, new_file_name)
            temp_dir = os.path.abspath(os.path.join(os.getcwd(), r'docs/spec_excel/'))

            local_file_path = os.path.join(temp_dir, str(only_id))
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
            local_file = os.path.join(local_file_path, new_file_name)
            file_upload.save(local_file)  # 保存在本地
            # file_upload.save(os.path.join(os.path.abspath(os.path.join(os.getcwd(), r'../../docs/spec_excel')), new_file_name))

            # 把本地文件转换成htm文件
            # 保存在Z:\temp\spec_html\创建的文件夹名 下
            file_url = CtrlExcelHtm().convert_excel_htm(local_file, new_file_name, file_path)
            # os.remove(local_file_path)
            from shutil import rmtree
            rmtree(local_file_path)
            # cmd = "rm -rf %s" % local_file
            # print(cmd)
            # if os.system(cmd):
            #     print("delete ok")
            # content 里返回这个htm文件的位置
            # file_url = os.path.join(file_path, os.path.splitext(new_file_name)[0]+'.htm')
            # file_url = Utillity.convert_url(curr_app.config.get('FILE_SRV_URL'), file_url)
            _, file_url = os.path.splitdrive(file_url)  # 去掉盘符
            result["content"] = file_url
            result["result"] = "ok"
        except Exception as e:
            current_app.logger.error('%s' % e)
            result["error"] = str(e)
            result['result'] = "NG"
        finally:
            return result




        #     CtrlExcelHtm().convert_excel_htm(excel_path)  # 传一个本地文件路径
        #     result = {"result": "Save OK"}
        # except Exception as e:
        #     result['error'] = str(e)
        # return result


