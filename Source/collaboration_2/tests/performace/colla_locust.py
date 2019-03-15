from locust import HttpLocust, TaskSet, task
import subprocess
import json


class UserBehavior(TaskSet):
    """This is the TaskSet class."""

    def on_start(self):
        """on_start is called when a Locust start before any task is scheduled."""
        pass

    # the @task takes an optional weight argument.
    @task
    def test_login(self):
        response = self.client.get("/login?username=hongcz&password=GyY3czv1")
        print("login", type(response))
        # print(response.json())

    @task
    def test_doc_tag_project(self):
        response = self.client.get("/DocTagProject/common")
        print("DocTagProject", type(response))
        # print(response.json())

    @task
    def test_tag_required_groups(self):
        response = self.client.get("/TagRequiredGroups")
        print("TagRequiredGroups", type(response))
        # print(response.json())

    @task
    def test_tag_tree_include_number(self):
        response = self.client.get("/TagTreeIncludeNumber")
        print("TagTreeIncludeNumber", type(response))
        # print(response.json())

    @task
    def test_tag_tree_include_number_often(self):
        response = self.client.get("/TagTreeIncludeNumber/often")
        print("TagTreeIncludeNumber_often", type(response))
        # print(response.json())

    @task
    def test_tag_tree_include_number_normal(self):
        response = self.client.get("/TagTreeIncludeNumber/normal")
        print("TagTreeIncludeNumber_normal", type(response))
        # print(response.json())

    @task
    def test_tag_tree_include_number_normal(self):
        response = self.client.get("/TagTreeIncludeNumber/normal")
        print("TagTreeIncludeNumber_normal", type(response))
        # print(response.json())

    @task
    def test_tag_tree_include_number_user(self):
        response = self.client.get("/TagTreeIncludeNumber/all/wangjian")
        print("TagTreeIncludeNumber_user", type(response))
        # print(response.json())

    @task  # @task(1)
    def tag_tree(self):
        response = self.client.get("/TagTree")
        print("TagTree", type(response))
        # print(response.json())

    @task  # @task(2)
    def doc(self):
        response = self.client.get("/Doc/100")
        print("Doc", response)
        # print(response.json())


class WebUserLocust(HttpLocust):
    """This is one HttpLocust class."""
    # Speicify the weight of the locust.
    weight = 1
    # The taskset class name is the value of the task_set.
    task_set = UserBehavior
    # Wait time between the execution of tasks.
    min_wait = 5000
    max_wait = 15000


# class MobileUserLocust(HttpLocust):
#     """This is another HttpLocust class."""
#     weight = 3
#     task_set = UserBehavior
#     min_wait = 3000
#     max_wait = 6000


if __name__ == '__main__':
    host = '--host=http://192.168.37.143'
    file_path = r'.\colla_locus.py'
    subprocess.Popen('locust -f colla_locus.py --host=http://192.168.37.143 --no-web -c1',
                     shell=True)
    # subprocess.Popen('locust -f %s %s' % (file_path, host),
    #                  shell=True)
