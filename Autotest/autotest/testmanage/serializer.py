from rest_framework import serializers

from testmanage.models import CountryInfo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryInfo
        fields = ("iso_code","eng_name","cn_name")