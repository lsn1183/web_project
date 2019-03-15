import requests
import json
import time
import commands

base_url = "http://localhost:5000/"
username = "1001"
password = "123456"
test_file = "if_test_config.ini"
login_token = ""

# quotation pei diagram
# start_time = time.clock()
# res = requests.get("http://localhost:5000/GetQuotationPie/2")
# end_time = time.clock()
# cost_time = (end_time - start_time) * 1000 #ms
# print cost_time

# print res
# print res.text

# # project list
# start_time = time.clock()
# res = requests.get("http://localhost:5000/Project/List")
# end_time = time.clock()
# cost_time = (end_time - start_time) * 1000 #ms
# print cost_time

# print res
# print res.text

class testCase(object):
    def __init__(self, no, url, method, input={}, postdata={}, output={}):
        self.no = no
        self.url = url
        self.method = method
        self.input = input
        self.postdata = postdata
        self.output = output


def login():
    params = dict(username=username, password=password)
    data = json.dumps(params)
    res = requests.post(base_url + "login", data = data)
    # print res
    print res.text
    if res.status_code == requests.codes.ok:
        res_json_data = json.loads(res.text)
        login_token = res_json_data["LoginToken"]
        print login_token
        return True
    else:
        return False

def load_test_file():
    test_case_list = []
    if_test_file = open(test_file)
    line = if_test_file.readline()
    while line:
        if line[0] == "#":
            line = if_test_file.readline()
            continue
        case = eval(line)
        test_case = testCase(case["no"], case["url"], case["method"], case["input"], case["postdata"], case["output"])
        test_case_list.append(test_case)
        line = if_test_file.readline()
    if_test_file.close()
    return test_case_list

def decode_input_params(input_dict):
    text = ""
    if input_dict:
        for key in input_dict:
            if input_dict[key]:
                text = text + "/" + input_dict[key]
    
    return text

def check_result(output, res):
    if res.status_code == requests.codes.ok:
        print "check_result todo"
        # check result param
        return True
    else:
        print "http_code:" + str(res.status_code)
        print res.raise_for_status()
        return False

def write_result(filename, status, output):
    file = open(filename, "w")
    file.write("status:" + str(status) + "\n" + output + "\n")
    file.close()

def execute_test(test_case):
    status = 0
    if test_case.method == "get":
        input_text = decode_input_params(test_case.input)
        start_time = time.clock()
        # res = requests.get(base_url + test_case.url + input_text, headers=dict(Authorization=login_token))
        # res = requests.get(base_url + test_case.url + input_text)
        url = base_url + test_case.url + input_text
        status, output = commands.getstatusoutput('ab -n 100 -c 10 ' + url)
        write_result(test_case.url.replace("/", "_") + "_result.txt", status, output)
        end_time = time.clock()
        cost_time = (end_time - start_time) * 1000 #ms
        print "testcase[" + test_case.no + "][" + test_case.url + "] costs:" + str(cost_time) + "ms"
    else:
        print "todo"

    # return check_result(test_case.output, res)
    return (status == 0 & (output.find("Non-2xx responses") < 0))

def mark_failed_case(test_case):
    print "case no[" + test_case.no + "][" + test_case.url  + "] failed"
    # write into report

def run():
    test_case_list = load_test_file()

    success = login()
    if not success:
        print "login failed"
        return

    for test_case in test_case_list:
        # login()
        ret = execute_test(test_case)
        if not ret:
            mark_failed_case(test_case)

if __name__ == "__main__":
    start_time = time.clock()

    run()

    end_time = time.clock()
    cost_time = (end_time - start_time) * 1000 #ms
    print "test totally costs:" + str(cost_time) + "ms"
