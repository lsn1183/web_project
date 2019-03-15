from django.db import models
from testmanage.models import *


class TeststepInfo(models.Model):
    order = models.IntegerField()
    operate = models.CharField(max_length=512, blank=False)
    expected_value = models.CharField(max_length=512, blank=False)
    is_automatically = models.BooleanField()
    step_remark = models.CharField(max_length=1024)
    step_state = models.CharField(max_length=64)


class TestcaseInfo(models.Model):
    source_case_id = models.IntegerField(verbose_name='初始版本case_id', null=True, blank=True)
    case_version = models.IntegerField(verbose_name='版本')
    case_name = models.CharField(max_length=512, blank=False, verbose_name='标题')
    case_abstract = models.CharField(max_length=1024, blank=False, verbose_name='摘要')
    case_premise = models.CharField(max_length=1024, blank=False, verbose_name='前提')
    case_importance = models.CharField(max_length=512, blank=False, verbose_name='重要性')
    case_test_mode = models.CharField(max_length=64, blank=False, verbose_name='测试方式')
    user_name = models.CharField(max_length=64, blank=False)
    charger = models.CharField(max_length=64, blank=False, verbose_name='负责人')
    create_datetime = models.CharField(max_length=32, blank=False)
    update_datetime = models.CharField(max_length=32, blank=False)
    case_model = models.ForeignKey(ModelInfo, on_delete=models.CASCADE)
    case_keyword_list = models.ManyToManyField(KeywordInfo, verbose_name='关键字', through="CaseKeyword",
                                               related_name='key_word_case',)
    case_dest_list = models.ManyToManyField(DestInfo, verbose_name='仕向地', through="CaseDest")
    case_step_list = models.ManyToManyField(TeststepInfo, verbose_name='测试步骤', through="CaseStep")
    case_field_value_list = models.ManyToManyField(FieldInfo, verbose_name='自定义字段的值', through="CaseFieldValue")


class CaseKeyword(models.Model):
    case = models.ForeignKey(TestcaseInfo, on_delete=models.CASCADE, verbose_name='case')
    keyword = models.ForeignKey(KeywordInfo, on_delete=models.CASCADE, verbose_name='关键字')


class CaseDest(models.Model):
    case = models.ForeignKey(TestcaseInfo, on_delete=models.CASCADE, verbose_name='case')
    dest = models.ForeignKey(DestInfo, on_delete=models.CASCADE, verbose_name='仕向地')


class CaseStep(models.Model):
    case = models.ForeignKey(TestcaseInfo, on_delete=models.CASCADE, verbose_name='case')
    step = models.ForeignKey(TeststepInfo, on_delete=models.CASCADE, verbose_name='测试步骤')


class TestcaseHistory(models.Model):
    case_id = models.CharField(max_length=64, blank=False, verbose_name='caseID')
    source_case_id = models.IntegerField(verbose_name='初始版本case_id', null=True, blank=True)
    case_version = models.IntegerField(verbose_name='版本')
    case_name = models.CharField(max_length=512, blank=False, verbose_name='标题')
    case_abstract = models.CharField(max_length=1024, blank=False, verbose_name='摘要')
    case_premise = models.CharField(max_length=1024, blank=False, verbose_name='前提')
    case_importance = models.CharField(max_length=512, blank=False, verbose_name='重要性')
    case_test_mode = models.CharField(max_length=64, blank=False, verbose_name='测试方式')
    user_name = models.CharField(max_length=64, blank=False)
    charger = models.CharField(max_length=64, blank=False, verbose_name='负责人')
    create_datetime = models.CharField(max_length=32, blank=False)
    update_datetime = models.CharField(max_length=32, blank=False)
    case_model = models.TextField(verbose_name='关联模块')
    case_keyword_list = models.TextField(verbose_name='关键字')
    case_dest_list = models.TextField(verbose_name='仕向地')
    case_step_list = models.TextField(verbose_name='测试步骤')
    case_field_value_list = models.TextField(verbose_name='自定义字段的值', null=True, blank=True)


class CaseFieldValue(models.Model):
    case = models.ForeignKey(TestcaseInfo, on_delete=models.CASCADE, verbose_name='case')
    field = models.ForeignKey(FieldInfo, on_delete=models.CASCADE, verbose_name='自定义字段')
    field_value = models.TextField(verbose_name='自定义字段的值')


class TestplanInfo(models.Model):
    plan_name = models.CharField(max_length=512, blank=False)
    user_name = models.CharField(max_length=64, blank=False)
    charger = models.CharField(max_length=64, blank=False)
    proj = models.ForeignKey(ProjInfo, on_delete=models.CASCADE)
    plan_case_list = models.ManyToManyField(TestcaseInfo)


class TestplanhistoryInfo(models.Model):
    h_plan_name = models.CharField(max_length=512, blank=False)
    h_user_name = models.CharField(max_length=64, blank=False)
    h_charger = models.CharField(max_length=64, blank=False)
    h_testplan = models.ForeignKey(TestplanInfo, on_delete=models.CASCADE)
    h_datatime = models.CharField(max_length=32, blank=False)
    h_version = models.IntegerField(verbose_name='版本', null=True, blank=True)
    h_proj = models.ForeignKey(ProjInfo, on_delete=models.CASCADE)
    h_plan_case_list = models.ManyToManyField(TestcaseInfo)


class TestresultInfo(models.Model):
    source_case_id = models.IntegerField(verbose_name='初始版本case_id', null=True, blank=True)
    result_version = models.CharField(max_length=64, blank=False)
    result_name = models.CharField(max_length=512, blank=False)
    result_abstract = models.CharField(max_length=1024, blank=False)
    result_premise = models.CharField(max_length=1024, blank=False)
    result_importance = models.CharField(max_length=512, blank=False)
    result_test_mode = models.CharField(max_length=64, blank=False)
    user_name = models.CharField(max_length=64, blank=False)
    charger = models.CharField(max_length=64, blank=False)
    create_datetime = models.CharField(max_length=32, blank=False)
    update_datetime = models.CharField(max_length=32, blank=False)
    result_model = models.ForeignKey(ModelInfo, on_delete=models.CASCADE)
    result_keyword_list = models.ManyToManyField(KeywordInfo)
    result_dest_list = models.ManyToManyField(DestInfo)
    result_step_list = models.ManyToManyField(TeststepInfo)
    result_value = models.CharField(max_length=64, blank=False)
    result_remarks = models.CharField(max_length=1024, blank=False)
    result_commiter = models.CharField(max_length=64, blank=False)
    case_id = models.CharField(max_length=64, blank=False)
    result_plan = models.ForeignKey(TestplanhistoryInfo, on_delete=models.CASCADE)


# TestfieldInfo表的履历表
class ResultfieldInfo(models.Model):
    result_case = models.ForeignKey(TestresultInfo, on_delete=models.CASCADE)
    field = models.ForeignKey(FieldInfo, on_delete=models.CASCADE)
    field_value = models.TextField()


class ImgInfo(models.Model):
    img_url = models.ImageField(upload_to='img')  # upload_to指定图片上传的途径，如果不存在则自动创建


# testcase变更记录表
class TestcaseChangeLog(models.Model):
    testcase = models.ForeignKey(TestcaseInfo, on_delete=models.CASCADE)
    message = models.CharField(max_length=1024, blank=False)
    data = models.CharField(max_length=1024, blank=False)
    commit_user = models.CharField(max_length=64, blank=False)
    create_time = models.CharField(max_length=32, blank=False)


# testplan显示自定义字段的配置表
class PlanFieldSetting(models.Model):
    plan = models.ForeignKey(TestplanInfo, on_delete=models.CASCADE)
    field_list = models.ManyToManyField(FieldInfo)


# jenkins配置字段表
class JenkinsCreateJob(models.Model):
    job_name = models.CharField(max_length=64, blank=False)
    node = models.CharField(max_length=64, blank=False)
    plan = models.ForeignKey(TestplanInfo, on_delete=models.CASCADE)