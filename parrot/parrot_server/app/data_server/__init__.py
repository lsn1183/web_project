# -*- coding: UTF-8 -*-
from flask_restful import Resource


class Root(Resource):
    def get(self):
        return "This is Koala Server."
    

class Api_1_0():
    def __init__(self, api):
        # Home
        api.add_resource(Root, '/')



