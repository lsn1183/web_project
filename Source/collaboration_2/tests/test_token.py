import json
from requests import get, put, post, delete
host = "http://192.168.37.112:15000/"
login_url = host + "login"
model_url = host + "TagTree"
print(login_url)
r = post(login_url, json={"username": "Admin", "password": "idesign123456"})
if r.status_code == 200:  # 成功
    result = json.loads(r.content)
    token = result.get('idesignToken')
    headers = {"Authorization": "Token"+" "+token}
    r = get(model_url, headers=headers)
    print(r)


