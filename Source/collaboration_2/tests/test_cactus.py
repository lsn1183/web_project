import json
from requests import get, put, post, delete
import urllib
host = "http://192.168.3.126:8080/"
login_url = host + "cactuswebapi/auth/login"
proj_url = host + "cactuswebapi/project/list"
projectgroup_url = host + "cactuswebapi/projectgroup/list"


employ = {"employeeNo": '1004',
          "password": "123456",
          "clientType": 0
          }

# employ = {"employeeNo": '1949',
#           "password": "chaiyu1984",
#           "clientType": 0
#           }

r = post(login_url, employ)
if r.status_code == 200:  # 成功
    result = json.loads(r.content)
    if result.get("code") == 0:  # 表示成功
        accessToken = result.get("info").get("accessToken")
        refreshToken = result.get("info").get("refreshToken")
        print(accessToken)
        # if accessToken:
        #     headers = {"authToken": accessToken,
        #                "Content-Type": "application/x-www-form-urlencoded"}
        #     proj_info = {"searchWord": ""}  # {"searchWord": "P1001"}
        #     r = post(proj_url, proj_info, headers=headers)
        #     print(r.status_code)
        #     if r.status_code == 200:
        #         result = json.loads(r.content)
        #         print(result)
        if accessToken:
            headers = {"authToken": accessToken,
                       "Content-Type": "application/json"}
            proj_group_info = {"minorProjectId": 10004}
            s = json.dumps(proj_group_info)
            r = post(projectgroup_url, s, headers=headers)
            print(r.status_code)
            if r.status_code == 200:
                result = json.loads(r.content)
                print(result)

