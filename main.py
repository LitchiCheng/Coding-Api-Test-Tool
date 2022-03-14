import json
import requests

header = {
    "User-Agent": "PostmanRuntime/7.28.2",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Content-Length": "423",
    "Connection": "keep-alive",
    "Authorization":"Bearer xx"
}

body = {
  "Action": "DescribeIssueListWithPage",
  "ProjectName": "SRC",
  "IssueType": "ALL",
  "PageNumber": 1,
  "PageSize": 20,
  "Conditions": [
    {
      "Key": "ASSIGNEE",
      "Value": "8079645"
    }
  ]
}

# body = {
#   "Action": "DescribeCodingCurrentUser"
# }

body_json = json.dumps(body)
s = requests.session()
login_url = "https://e.coding.net/open-api"
login_ret = s.post(login_url, headers=header, data=body_json)

print(login_ret)

ret_josn = json.loads(login_ret.text)
list = ret_josn["Response"]["Data"]["List"]
for i in list:
    print(i["Name"] + " ")