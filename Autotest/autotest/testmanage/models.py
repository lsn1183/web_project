from django.db import models

# Create your models here.
class CountryInfo(models.Model):
    iso_code = models.CharField(max_length=512, blank=False)
    eng_name = models.CharField(max_length=512, blank=False)
    cn_name = models.CharField(max_length=512, blank=False)

class DestInfo(models.Model):
    dest_showname = models.CharField(max_length=512, blank=False)
    data_provider = models.CharField(max_length=16, blank=False)
    dest_introduce = models.TextField()
    country_list = models.ManyToManyField(CountryInfo)

class FieldOptionInfo(models.Model):
    option_value = models.CharField(max_length=1024, blank=False)

class FieldInfo(models.Model):
    field_en_name = models.CharField(max_length=512, null=True, blank=True)
    field_name = models.CharField(max_length=512, blank=False)
    field_type = models.CharField(max_length=512, blank=False)
    field_option_list = models.ManyToManyField(FieldOptionInfo)
    field_show_when_execute = models.BooleanField()
    sort_num = models.IntegerField()
    field_open_use = models.CharField(max_length=512, blank=False)

class KeywordInfo(models.Model):
    keyword = models.CharField(max_length=512, blank=False)

class ProjInfo(models.Model):
    proj_name = models.CharField(max_length=512, blank=False)
    proj_intro = models.CharField(max_length=512, blank=False)
    dest_list = models.ManyToManyField(DestInfo)
    user_name = models.CharField(max_length=64, blank=False)
    charger = models.CharField(max_length=64, blank=False)
    create_datetime = models.CharField(max_length=32, blank=False)
    update_datetime = models.CharField(max_length=32, blank=False)
    finish_datetime = models.CharField(max_length=32, blank=False)
    option_field_list = models.ManyToManyField(FieldInfo)
    is_catus = models.BooleanField()
    keyword_list = models.ManyToManyField(KeywordInfo)

class ModelInfo(models.Model):
    model_name = models.CharField(max_length=512, blank=False)
    model_intro = models.CharField(max_length=512, blank=False)
    user_name = models.CharField(max_length=64, blank=False)
    charger = models.CharField(max_length=64, blank=False)
    create_datetime = models.CharField(max_length=32, blank=False)
    update_datetime = models.CharField(max_length=32, blank=False)
    field_list = models.ManyToManyField(FieldInfo)
    parent_proj = models.ForeignKey(ProjInfo, on_delete=models.CASCADE)
    parent_model = models.ForeignKey('self', blank = True, null = True, related_name = 'children', on_delete=models.CASCADE)

class ModelFieldInfo(models.Model):
    model_info = models.ForeignKey(ModelInfo, on_delete=models.CASCADE)
    field_info = models.ForeignKey(FieldInfo, on_delete=models.CASCADE)





