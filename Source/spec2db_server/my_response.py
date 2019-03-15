# -*- coding: UTF-8 -*-

from flask import Response
from werkzeug.datastructures import Headers


class MyResponse(Response):
    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        # 跨域控制
        origin = ('Access-Control-Allow-Origin', '*')
        # methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        if headers:
            headers.add(*origin)
            # headers.add(*methods)
        # else:
            # headers = Headers([origin, methods])
        kwargs['headers'] = headers
        return super(MyResponse, self).__init__(response, **kwargs)

