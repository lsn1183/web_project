# -*- coding: UTF-8 -*-
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import *
from flask import request
from logging.config import dictConfig
from flask import send_from_directory
import os
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'console': {'class': 'logging.StreamHandler',
                    # 'stream': 'ext: // sys.stdout',
                    'formatter': 'default'
                    },
        'file': {'class': 'logging.FileHandler',
                 'level': 'DEBUG',
                 'formatter': 'default',
                 'filename': 'flask.log'
                 }
    },
    # 'loggers': {
    #     'wsgi': {'level': 'DEBUG',
    #                 'handlers': '[wsgi]',
    #                 'propagate': 'no'
    #                 },
    #     'file': {'level': 'DEBUG',
    #              'handlers': '[file]',
    #              'propagate': 'no'
    #              }
    # },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
})
app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)
app.config.from_pyfile('config.py')


class Login(Resource):
    def get(self):
        from flask_restful import reqparse
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()

        username = args.get('username')
        password = args.get('password')

        from app.login import login
        result = login(username, password)
        return result


class TagTree(Resource):
    def get(self):
        from app.doc_tag import DocTag
        obj = DocTag()
        result = {"result": "NG"}
        tags = obj.get_tag_tree()
        if tags:
            result = {"result": "OK", "content": tags}
        return result

    def post(self):
        from app.doc_tag import DocTag
        obj = DocTag()
        result = {"result": "NG", "error": ''}
        req_json = request.get_json(force=True)
        tags = obj.add_tag(req_json)
        if tags.get("result"):
            result = {"result": "OK"}
        else:
            result = tags
        return result

    def put(self, tag_id):
        """update"""
        from app.doc_tag import DocTag
        obj = DocTag()
        result = {"result": "NG", "error": ''}
        req_json = request.get_json(force=True)
        re = obj.update_tag(tag_id, req_json)
        if re.get("result"):
            result = {"result": "OK"}
        else:
            result = re
        return result

    def delete(self, tag_id):
        from app.doc_tag import DocTag
        obj = DocTag()
        result = {"result": "NG", "error": ''}
        re = obj.delete_tag(tag_id)
        if re.get("result"):
            result = {"result": "OK"}
        else:
            result = re
        return result


class Doc(Resource):
    def post(self):
        result = {"result": "NG", "error": ''}
        from app.doc import Doc
        obj = Doc()
        rst, message = obj.add(request)
        if not rst:
            result["error"] = message
        else:
            result["result"] = "OK"
        return result

    def put(self, doc_id):
        """update"""
        result = {"result": "NG", "error": ''}
        from app.doc import Doc
        obj = Doc()
        rst, message = obj.update(doc_id, request)
        if not rst:
            result["error"] = message
        else:
            result["result"] = "OK"
        return result

    def delete(self, doc_id):
        result = {"result": "NG", "error": ''}
        from app.doc import Doc
        obj = Doc()
        rst, message = obj.delete(doc_id)
        if not rst:
            result["error"] = message
        else:
            result["result"] = "OK"
        return result

    def get(self, doc_id):
        result = {"result": "NG", "content": ''}
        from app.doc import Doc
        obj = Doc()
        doc_info = obj.get_by_key_id(doc_id)
        if doc_info:
            result["result"] = "OK"
            result["content"] = doc_info
        return doc_info


class Doc2(Resource):
    def post(self):
        result = {"result": "NG", "error": ''}
        from app.doc import Doc
        obj = Doc()
        rst, message = obj.add2(request)
        if not rst:
            result["error"] = message
        else:
            result["result"] = "OK"
        return result


class DocByTag(Resource):
    def get(self, tag_id):
        result = {"result": "NG", "content": []}
        from app.doc import Doc
        obj = Doc()
        doc_list = obj.get_by_tag(tag_id)
        if doc_list:
            result["result"] = "OK"
            result["content"] = doc_list
        return result


class DownFile(Resource):
    def get(self, path_info):
        file_name = os.path.basename(path_info)
        path_info = path_info.replace(file_name, '')
        print path_info, file_name
        return send_from_directory(os.path.join(path_info), file_name, as_attachment=True)



api.add_resource(Login, '/login')
api.add_resource(TagTree, '/TagTree', '/TagTree/<int:tag_id>')
api.add_resource(Doc, '/Doc', '/Doc/<int:doc_id>')
api.add_resource(Doc2, '/Doc2', '/Doc2/<int:doc_id>')
api.add_resource(DocByTag, '/DocByTag', '/DocByTag/<int:tag_id>')
api.add_resource(DownFile, '/DownFile', '/DownFile/<path:path_info>')



if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    app.run(debug=True, host='', threaded=True)
    # app.run (debug=True, host='192.168.37.42', port=25000, threaded=True)

