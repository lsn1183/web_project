import json
from testcase.models import TestcaseHistory
from testcase.models import TestcaseInfo
from django.forms.models import model_to_dict
from testcase.Testcase import Testcase


class TestcaseVerDiff(object):
    def __init__(self):
        pass

    def get_history_id(self, source_case_id):
        q = TestcaseHistory.objects.filter(source_case_id=source_case_id).order_by('-id')
        right_id_list = []
        left_id_list = []
        for testcase in q:
            left_id_list.append(testcase.pk)
            right_id_list.append(testcase.pk)
        right_id_list.append(0)  # 0代表当前版本
        result = {"left": left_id_list, "right": right_id_list}
        return result

    def get_history_testcase(self, left_id, right_id, case_id):
        try:
            error = ""
            if left_id:
                left_q = TestcaseHistory.objects.get(pk=left_id)
                left_data = self.model_to_dict(left_q)
            else:
                left_data = dict()
            if right_id:
                right_q = TestcaseHistory.objects.get(pk=right_id)
                right_data = self.model_to_dict(right_q)
            else:
                right_data = dict()
                case_data = Testcase().get_testcase_one(case_id)
                error = case_data.pop('error')
                if not error:
                    right_data = case_data.get("result")
            return left_data, right_data, error
        except Exception as e:
            return dict(), dict(), str(e)

    def model_to_dict(self, case_model):
        case_dict = dict()
        if case_model:
            keyword_list, dest_list, field_value_list, step_list = [], [], [], []
            if case_model.case_keyword_list:
                keywords = case_model.case_keyword_list
                keyword_list = json.loads(case_model.case_keyword_list)
            if case_model.case_dest_list:
                dest_list = json.loads(case_model.case_dest_list)
            if case_model.case_step_list:
                step_list1 = case_model.case_step_list
                step_list = json.loads(case_model.case_step_list)
            if case_model.case_field_value_list:
                field_value_list = json.loads(case_model.case_field_value_list)
            case_dict = {
                "id": case_model.case_id,
                "source_case_id": case_model.source_case_id,
                "title": case_model.case_name,
                "abstract": case_model.case_abstract,
                "premise": case_model.case_premise,
                "charger": case_model.charger,
                "user_name": case_model.user_name,
                "case_version": case_model.case_version,
                "importance": case_model.case_importance,
                "test_mode": case_model.case_test_mode,
                "case_model": case_model.case_model.id,
                "keyword_list": keyword_list,
                "dest_list": dest_list,
                "field_value_list": field_value_list,
                "step_list": step_list,
            }
        return case_dict









