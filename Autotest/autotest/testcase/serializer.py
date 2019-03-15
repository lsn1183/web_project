from rest_framework import serializers

# from testcase.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # model = Category
        fields = ("id","category_name","parent_id")