# -*- coding: UTF-8 -*-
from testmanage.models import *
from testcase.models import *
import datetime
from django.db import transaction
from django.http import FileResponse

class Img():
    def add_img(self, img_url):
        img = ImgInfo(img_url=img_url)
        img.save()
        return img.id

    def get_img_by_id(self, _id):
        data = {"error":""}
        if ImgInfo.objects.filter(pk=_id):
            image = ImgInfo.objects.get(pk=_id)
            data["result"]={
                "url":image.img_url.url
            }
        else:
            data["error"] = "NG"
        return data

    def get_all_img(self):
        return

    def del_img(self):
        return